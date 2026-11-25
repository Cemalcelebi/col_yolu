"""MACD_UYUM_ES — K47 EŞ KİRLİLİĞİ ÖLÇÜMÜ (25 Kasım 2026; iş tanımı: ana model mesajı).

Cemal'in itirazı (25 Kas 2026): "Belki de seçilen eşlerin içinde aynı uyumsuzluk vardı." Ç217 / Ç218 / Ç219'da (hepsi TUTMADI, fark ~ 0) olay
hisseleri, aynı giriş günü d ve aynı kovadaki (ATRP tercili x likidite üçlüsü x F15 çeyreği) eş hisselerle kıyaslandı; eş dışı yalnız AYNI GÜN
U1 olayı olan hisselerdi. Birkaç gün önce sinyal vermiş ya da uyumsuzluğu hâlâ "yanık" olan hisseler eş olarak kalıyordu.
Bu iş iki soruyu sayıyla cevaplar: (1) eşlerin yüzde kaçı aynı uyumsuzluğu taşıyordu (kirlilik payı)? (2) uyumsuzluk taşıyan eşler çıkarılınca
(temiz eş) sonuç değişiyor mu?

TANIMLAR (ES_ESIK; sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
  HAM U1 DURUMU (bar düzeyi): MACD_UYUM.mu_hisse'deki kosul['U1'] maskesi (S10 ∧ F68 ∧ DİPTE, aday gün tanımı aynen) doğru olan bütün geçerli
  barlar; "dip başına ilk gün" ve "15 bar aralığı" UYGULANMADAN. HAM S10F68: aynı, DİPTE şartsız (kosul['U1b']).
  b = eşin giriş günü d'den ÖNCEKİ geçerli bar sayısı (= d'de geçerli barı varsa onun sırası). Bayraklar yalnız d'den önceki barlardan:
  K20 (ANA) b-20 .. b-1'de en az bir ham U1; K1 (bilgi) b-1'de ham U1; KG (bilgi) b-20 .. b-1'de en az bir ham S10F68.
  BARIZ = U1 ∧ F65 <= -0,05 (uyum_satir.csv.gz F65).
ÖLÇÜLER  A kirlilik payı (getirisiz, ön kayıtta); B temiz eşle ölçüm (ANA; K20, bilgi KG); C kirli eş - temiz eş (bilgi); D denge (F15 / ATRP).
HÜKÜM    C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum, plasebo HARİÇ (plasebo_gecti = True), Ç217 / Ç219 tohumlarıyla.

Komut:  python MACD_UYUM_ES.py hazirlik [--uzerine]   bayraklar + D1-D4 + A tablosu -> ES_ON_KAYIT.md (getirisiz; DURUR)
        python MACD_UYUM_ES.py kos                    kapı (ön kayıt git'te, sha'lar, kontrol listesi, KASA) -> B / C / D -> çıktılar
        python MACD_UYUM_ES.py sha                    kod / eşik / veri sha'ları
Colab:  exec(open('MACD_UYUM_ES.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri -> /tmp/kasa/acik (KASA açık kesik 2022-12-31). Evren bugün işlem gören hisseler (hayatta kalma: sonuç yukarı yanlı).
MACD_UYUM / CETVEL2 / YAPI_HEDEF / KASA / IZ_KARNE DEĞİŞTİRİLMEZ; içe alınır.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_ES = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from numpy.lib.stride_tricks import sliding_window_view as _swv  # noqa: E402

KOK_ES = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_ES not in sys.path:
    sys.path.insert(0, KOK_ES)

import CETVEL2 as C2  # noqa: E402
import MACD_UYUM as MU  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

eslog = logging.getLogger("col.macd_uyum_es")
if not eslog.handlers:
    _es_h = logging.StreamHandler(sys.stderr)
    _es_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s macd_uyum_es: %(message)s", "%H:%M:%S"))
    eslog.addHandler(_es_h)
    eslog.setLevel(logging.INFO)
    eslog.propagate = False

ES_SURUM = "MACD_UYUM_ES v1.0 (2026-11-25): K47 eş kirliliği (ham U1 durumu taşıyan eşler) payı ve temiz eşle yeniden ölçüm; açık veri"
ES_YOL = {"cikti": os.path.join(KOK_ES, "arastirma_cikti", "macd_uyum"), "veri": os.environ.get("MU_VERI", "/tmp/veri"),
          "kod": os.path.join(KOK_ES, "MACD_UYUM_ES.py")}
ES_DOSYA = {"onkayit": "ES_ON_KAYIT.md", "rapor": "ES_RAPOR.md", "satir": "es_satir.csv.gz", "sonuc": "es_sonuc.json",
            "hazirlik": "es_hazirlik.json", "olay": "uyum_olay.csv.gz", "c217_satir": "uyum_satir.csv.gz", "c217_sonuc": "sonuc.json",
            "c219_sonuc": "uyum_b_sonuc.json"}
ES_PAZAR = ["ABD", "AVR", "BIST"]
ES_KARAR_PAZAR = ["ABD", "AVR"]
ES_DONEM = dict(MU.MU_DONEM)
ES_BAYRAK = ["K20", "K1", "KG"]
ES_ESIK: Dict[str, Any] = {
    "pencere": 20,                      # K20 / KG: b-20 .. b-1
    "bariz_F65": -0.05,                 # BARIZ: F65 <= -0,05
    "es_min": 5,                        # temiz eş en az (C2_ESIK es_min ile aynı)
    "ufuk": 15,
    "tekil_gun": 15,                    # Ç217 c2_olc22 tekil (ufuk) aynen
    "pay_esik": 0.25,                   # A: payı >= %25 olan olay payı
    "d2_rtol": 1e-9,
    "d3": {"n": 30, "tohum": 2611, "kirli_pay": 0.5},
    "d4": {"n": 20, "tohum": 2612},
    "C": {"kirli_min": 1, "temiz_min": 5, "B": 2000, "tohum": 2613, "alt": 0.025, "ust": 0.975},
    "D": {"f15_uyari": 0.05, "atrp_goreli_uyari": 0.10},
    "tohum_U1": "100000 + pazar_sira x 100 + donem_sira (Ç217 mu_olc_r, tohum0 = 1)",
    "tohum_BARIZ": "300 + 10 x pazar_sira + donem_sira (Ç219 u1b_olc)",
    "karar": ("EŞ KİRLİLİĞİ SONUCU DEĞİŞTİRDİ <=> temiz eşle (K20) U1'in 4 karar hücresinin (ABD / AVR x d1619 / d2022) HEPSİNDE hüküm TUTAR "
              "(plasebo hariç şartlar: n >= 30, güç >= 0,80, FARK > 0, FARK boot alt > 0, SIRA > 0,50, SIRA boot alt > 0,50, L3O > 0). "
              "BARIZ için ayrı satır, aynı kural. Aksi halde DEĞİŞTİRMEDİ. Her hücrede FARK_temiz - FARK_eski yazılır."),
}


class ESHata(RuntimeError):
    """Durdurucu hata: doğrulama (D1-D4), kapı, sha, KASA."""


# ================================================================ 0) ORTAK
def _es_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def es_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or ES_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _es_sha(yol: str) -> str:
    try:
        h = hashlib.sha256()
        with open(yol, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        return h.hexdigest()
    except OSError as ex:
        raise ESHata(f"sha okunamadı: {yol}: {ex}") from ex


def _es_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or ES_YOL["cikti"], ES_DOSYA[ad])


def _es_git(args: List[str]) -> str:
    try:
        return subprocess.run(["git"] + args, cwd=KOK_ES, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as ex:
        raise ESHata(f"git {' '.join(args)} başarısız: {ex}") from ex


def _es_json(o: Any) -> Any:
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (pd.Timestamp, _dt.date)):
        return str(o)
    return str(o)


def _es_temiz_nan(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _es_temiz_nan(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_es_temiz_nan(v) for v in o]
    if isinstance(o, (float, np.floating)):
        return None if not np.isfinite(o) else float(o)
    return o


def _es_jyaz(yol: str, J: Any, ad: str) -> None:
    YH._yh_yaz(yol, json.dumps(_es_temiz_nan(J), ensure_ascii=False, indent=1, default=_es_json), ad)


def es_sha_simdi(veri: Optional[str] = None) -> Dict[str, str]:
    v = veri or ES_YOL["veri"]; c = ES_YOL["cikti"]
    S = {"kod": _es_sha(ES_YOL["kod"]), "esik": es_esik_sha(), "MACD_UYUM.py": _es_sha(os.path.join(KOK_ES, "MACD_UYUM.py")),
         "CETVEL2.py": _es_sha(os.path.join(KOK_ES, "CETVEL2.py")), "uyum_olay": _es_sha(_es_yol("olay", c)),
         "uyum_satir": _es_sha(_es_yol("c217_satir", c))}
    for p in ES_PAZAR:
        S[f"V_{p}"] = _es_sha(os.path.join(v, f"V_{p}.pkl"))
    return S


# ================================================================ 1) HAM DURUM (mu_hisse ile aynı yapı taşları; MACD_UYUM değişmez)
def es_ham(d: pd.DataFrame, E: Dict[str, Any] = MU.MU_ESIK, E8: Dict[str, Any] = YH.YH_ESIK8) -> Dict[str, Any]:
    """Hazır (geçerli bar) seri -> bar düzeyi ham U1 ve ham S10F68 maskeleri + bu maskelerden mu_hisse olay seçimi ('dip başına ilk gün' +
    15 bar) ile üretilmiş U1 olay bar sıraları (D1 için). mu_hisse'nin aday gün / DİPTE / S10 / F68 adımlarının AYNISI."""
    L = d["Low"].to_numpy(float); H = d["High"].to_numpy(float); C = d["Close"].to_numpy(float); n = len(L)
    bos = {"n": n, "u1": np.zeros(n, bool), "s10f68": np.zeros(n, bool), "olay_u1": np.array([], np.int64)}
    if n <= int(E8["dip"]["pencere"]):
        return bos
    Dp = E["dipte"]; Ol = E["olay"]
    isd = MU.mu_dip(L, E8); son = MU._mu_son_dip(isd); dips = np.flatnonzero(isd)
    if not len(dips):
        return bos
    sag = int(E8["dip"]["sag"]); pen = int(E8["dip"]["pencere"]); taze = int(Ol["taze_azami"])
    nxt = np.r_[dips[1:], n + 10 ** 6]
    a = np.maximum(dips + sag + 1, pen); b = np.minimum(np.minimum(dips + taze, nxt + sag), n - 1)
    ln = np.clip(b - a + 1, 0, None)
    g = int(Dp["geri"]); dipte = np.zeros(len(dips), bool)
    if n > g:
        mnL = _swv(L, g).min(axis=1); mxH = _swv(H, g + 1).max(axis=1)
        okk = dips >= g
        jj = np.clip(dips - g, 0, len(mxH) - 1)
        tepe = np.where(okk, mxH[jj], np.nan)
        with np.errstate(invalid="ignore"):
            dipte = okk & (L[dips] <= mnL[np.clip(dips - g, 0, len(mnL) - 1)] * (1.0 + float(Dp["dip_tol"]))) & \
                (C[dips] <= float(Dp["tepe_pay"]) * tepe)
    tot = int(ln.sum())
    if tot == 0:
        return bos
    di = np.repeat(np.arange(len(dips)), ln)
    I = np.repeat(a, ln) + (np.arange(tot) - np.repeat(np.cumsum(ln) - ln, ln))
    K2 = dips[di]
    L2c, L1c = MU.mu_l2l1(I, son, E8)
    if not np.array_equal(L2c, K2):
        raise ESHata("aday gün L2'si dip sırasıyla tutmuyor (iç tutarlılık)")
    if len(I) > 1 and not (np.diff(I) > 0).all():
        raise ESHata("aday günler tekil ve artan değil (bar başına tek aday beklenir)")
    isn = int(E8["macd"]["isinma"]); pw = int(E8["macd"]["pencere"])
    with np.errstate(invalid="ignore"):
        s65ham = (L1c >= 0) & (L[K2] <= L[np.clip(L1c, 0, n - 1)] * (1.0 + float(E8["esik"]["F65_ust"])))
    macdok = (L1c >= 0) & ((I >= pw) | (L1c >= isn))
    gerek = s65ham & macdok
    V = MU.mu_s10_vektor(L, C, I[gerek], E8, son=son)
    if not (np.array_equal(V["L2"], K2[gerek]) and np.array_equal(V["L1"], L1c[gerek])):
        raise ESHata("vektör L1 / L2 aday günlerle tutmuyor (iç tutarlılık)")
    Ig = I[gerek]; dg = di[gerek]
    S10 = V["S10"] == 1.0; F68 = V["F68"] == 1.0; dp = dipte[dg]
    mk_u1 = S10 & F68 & dp; mk_b = S10 & F68
    u1 = np.zeros(n, bool); u1[Ig[mk_u1]] = True
    sb = np.zeros(n, bool); sb[Ig[mk_b]] = True
    # mu_hisse olay seçimi (D1): dip başına ilk gün + aynı hissede >= 15 bar
    q = np.flatnonzero(mk_u1); ol: List[int] = []
    if len(q):
        _, ilk = np.unique(dg[q], return_index=True); q = q[ilk]; q = q[np.argsort(Ig[q], kind="stable")]
        son_t = -10 ** 9
        for x in q:
            if Ig[x] - son_t >= int(Ol["ara"]):
                ol.append(int(Ig[x])); son_t = Ig[x]
    return {"n": n, "u1": u1, "s10f68": sb, "olay_u1": np.array(ol, np.int64)}


def es_bayrak_seri(tarih: np.ndarray, u1: np.ndarray, sb: np.ndarray, gunler: np.ndarray, pencere: int = 20) -> Dict[str, np.ndarray]:
    """Bir hisse: hazır bar tarihleri, ham maskeler -> panel günleri için K20 / K1 / KG. b = (tarih < gün) bar sayısı; yalnız b-pencere .. b-1."""
    t = np.asarray(tarih).astype("datetime64[ns]"); g = np.asarray(gunler).astype("datetime64[ns]")
    b = np.searchsorted(t, g, "left").astype(np.int64)
    cu = np.r_[0, np.cumsum(np.asarray(u1, np.int64))]; cs = np.r_[0, np.cumsum(np.asarray(sb, np.int64))]
    lo = np.maximum(b - int(pencere), 0)
    k20 = (cu[b] - cu[lo]) > 0
    kg = (cs[b] - cs[lo]) > 0
    k1 = (b >= 1) & np.asarray(u1, bool)[np.clip(b - 1, 0, max(len(u1) - 1, 0))] if len(u1) else np.zeros(len(g), bool)
    return {"K20": k20, "K1": k1, "KG": kg}


def es_panel_bayrak(Pn: Dict[str, Any]) -> Dict[str, Any]:
    """Panelin her hissesi: hazır seri -> ham durum -> (gün x hisse) K20 / K1 / KG matrisleri + D1 olayları."""
    t0 = time.time(); P = Pn["P"]; idx = P["tarih"]; S = P["sembol"]; nd, u = len(idx), len(S)
    M = {k: np.zeros((nd, u), bool) for k in ES_BAYRAK}; olay: List[Tuple[str, pd.Timestamp]] = []; ham_say = 0
    for jx, s in enumerate(S):
        try:
            hz = YH._yh_hazir(Pn["Vd"]["V"][s])
            H = es_ham(hz)
        except ESHata:
            raise
        except Exception as ex:   # bir hissenin hatası tüm ölçümü bozar: dur
            raise ESHata(f"{P['pazar']} {s}: ham durum hesaplanamadı: {type(ex).__name__}: {ex}") from ex
        B = es_bayrak_seri(hz.index.values, H["u1"], H["s10f68"], idx.values, ES_ESIK["pencere"])
        for k in ES_BAYRAK:
            M[k][:, jx] = B[k]
        ham_say += int(H["u1"].sum())
        olay += [(s, pd.Timestamp(hz.index[i])) for i in H["olay_u1"]]
    eslog.info("%s bayrak: %d hisse, ham U1 bar %d, U1 olay %d (%.0f sn)", P["pazar"], u, ham_say, len(olay), time.time() - t0)
    return {**M, "olay": olay, "ham_u1_bar": ham_say}


# ================================================================ 2) OLAYLAR, EŞ KÜMESİ, KİRLİ SAYISI
def es_olay(Pn: Dict[str, Any], O: pd.DataFrame, satir: pd.DataFrame) -> pd.DataFrame:
    """Ç217 U1 olayları (uyum_olay) -> c2_olay (Ç217 c2_olc22 ile aynı: tekil 15) + dönem + F65 (satır dosyası)."""
    p = Pn["pazar"]; Oh = O[(O.pazar == p) & (O.hipotez == "U1")][["sembol", "tarih"]].copy()
    X, _ = C2.c2_olay(Oh, Pn, int(ES_ESIK["tekil_gun"]))
    X["donem"] = C2._c2_donem22(X.giris, ES_DONEM)
    Sp = satir[(satir.hipotez == "U1") & (satir.pazar == p)][["sembol", "tarih", "F65", "es_r15", "n_es", "fark", "sira"]].copy()
    Sp = Sp.rename(columns={c: f"c217_{c}" for c in ("es_r15", "n_es", "fark", "sira")})
    Sp["tarih"] = pd.to_datetime(Sp.tarih)
    X = X.merge(Sp, on=["sembol", "tarih"], how="left", validate="one_to_one")
    X["bariz"] = X.F65.to_numpy(float) <= float(ES_ESIK["bariz_F65"])
    return X


def es_dislanan(Pn: Dict[str, Any], d: np.ndarray, j: np.ndarray) -> np.ndarray:
    """(d, j) çiftlerinin havuz sırası (havuzda olanlar, tekil) -> havuz uzunluğunda bool maske."""
    m = np.zeros(len(Pn["h_r"]), bool)
    pp = Pn["h_pix"][np.asarray(d, np.int64), np.asarray(j, np.int64)]
    m[pp[pp >= 0]] = True
    return m


def es_kirli_cift(Pn: Dict[str, Any], F: np.ndarray, gunler: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Verilen günlerde F bayraklı ve havuzda olan (d, j) çiftleri (ek dışlama girdisi)."""
    g = np.unique(np.asarray(gunler, np.int64))
    sub = F[g] & (Pn["h_pix"][g] >= 0)
    a, b = np.nonzero(sub)
    return g[a].astype(np.int64), b.astype(np.int64)


def es_kume_say(Pn: Dict[str, Any], d: np.ndarray, j: np.ndarray, isaret: np.ndarray, haric: np.ndarray) -> np.ndarray:
    """Olay başına eş kümesinde (aynı (d, kova) havuzu, 'haric' havuz üyeleri dışarıda) 'isaret' (havuz maskesi) taşıyan üye sayısı."""
    kv = Pn["KV"][d, j].astype(np.int64); key = np.asarray(d, np.int64) * C2.C2_KOVA_SAYI + kv
    hk = Pn["h_key"]; lo = np.searchsorted(hk, key, "left"); hi = np.searchsorted(hk, key, "right")
    cf = np.r_[0, np.cumsum((isaret & ~haric).astype(np.int64))]
    return np.where(kv >= 0, cf[hi] - cf[lo], 0).astype(np.int64)


def es_es(Pn: Dict[str, Any], X: pd.DataFrame, ek_d: Optional[np.ndarray] = None, ek_j: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """c2_es: Ç217 dışlaması (olayların kendisi) + ek dışlama (kirli çiftler)."""
    d = X.d.to_numpy(np.int64); j = X.j.to_numpy(np.int64); x = X.r15.to_numpy(float)
    if ek_d is None:
        return C2.c2_es(Pn, d, j, x, d, j)
    return C2.c2_es(Pn, d, j, x, np.r_[d, np.asarray(ek_d, np.int64)], np.r_[j, np.asarray(ek_j, np.int64)], int(ES_ESIK["es_min"]))


def es_kaba(Pn: Dict[str, Any], d: int, j: int, x: float, haric: np.ndarray) -> Dict[str, float]:
    """Kaba kuvvet: (d, kova) havuz üyeleri tek tek, 'haric' dışarıda; ortalama, sayı, sıra."""
    kv = int(Pn["KV"][d, j]); key = int(d) * C2.C2_KOVA_SAYI + kv
    uy = np.flatnonzero((Pn["h_key"] == key) & ~haric)
    r = Pn["h_r"][uy]; N = len(uy)
    if kv < 0 or N < int(ES_ESIK["es_min"]) or not np.isfinite(x):
        return {"n_es": float(N if kv >= 0 else 0), "es_r15": np.nan, "sira": np.nan}
    return {"n_es": float(N), "es_r15": float(sum(float(v) for v in r) / N), "sira": float(((r < x).sum() + 0.5 * (r == x).sum()) / N)}


# ================================================================ 3) DOĞRULAMALAR
def es_d1(Pn: Dict[str, Any], B: Dict[str, Any], O: pd.DataFrame) -> Dict[str, Any]:
    p = Pn["pazar"]; ref = O[(O.pazar == p) & (O.hipotez == "U1")]
    a = set((s, pd.Timestamp(t)) for s, t in zip(ref.sembol, pd.to_datetime(ref.tarih)))
    b = set(B["olay"])
    r = {"pazar": p, "olay_dosya": len(a), "ham_uretim": len(b), "ortak": len(a & b), "yalniz_dosya": len(a - b), "yalniz_ham": len(b - a),
         "tuttu": a == b}
    if not r["tuttu"]:
        raise ESHata(f"D1 TUTMADI {p}: {r}; örnek {sorted(a ^ b)[:3]} -> DURDU")
    return r


def es_d2(X: pd.DataFrame, e: Dict[str, np.ndarray]) -> Dict[str, Any]:
    p = str(X.pazar.iloc[0]) if len(X) else "?"; rt = float(ES_ESIK["d2_rtol"]); bozuk = {}
    if X[["c217_n_es"]].isna().any().any():
        raise ESHata(f"D2 {p}: {int(X.c217_n_es.isna().sum())} olay Ç217 satır dosyasında yok -> DURDU")
    for c in ("es_r15", "n_es", "fark", "sira"):
        a = np.asarray(e[c], float); b = X[f"c217_{c}"].to_numpy(float)
        ok = np.isclose(a, b, rtol=rt, atol=0.0, equal_nan=True) | (np.isnan(a) & np.isnan(b))
        if not ok.all():
            bozuk[c] = int((~ok).sum())
    r = {"pazar": p, "n": int(len(X)), "olculen": int(np.isfinite(e["fark"]).sum()), "bozuk": bozuk, "tuttu": not bozuk}
    if bozuk:
        raise ESHata(f"D2 TUTMADI {p}: {r} -> DURDU")
    return r


def es_uyeler(Pn: Dict[str, Any], X: pd.DataFrame, haric: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Olay başına eş kümesi üyeleri (olay sırası, havuz sırası) — Ç217 eş kümesi ('haric' = olay çiftleri)."""
    d = X.d.to_numpy(np.int64); j = X.j.to_numpy(np.int64); kv = Pn["KV"][d, j].astype(np.int64)
    key = d * C2.C2_KOVA_SAYI + kv; hk = Pn["h_key"]
    lo = np.searchsorted(hk, key, "left"); hi = np.searchsorted(hk, key, "right"); c = np.where(kv >= 0, hi - lo, 0)
    ii = np.repeat(np.arange(len(X)), c); pp = np.arange(int(c.sum())) - np.repeat(np.cumsum(c) - c, c) + np.repeat(lo, c)
    k = ~haric[pp]
    return ii[k], pp[k]


def es_d3(Pn: Dict[str, Any], B: Dict[str, Any], ii: np.ndarray, pp: np.ndarray, pi: int) -> Dict[str, Any]:
    """K2: 30 (d, eş) çifti (yarısı K20 kirli); eşin verisi d'den önceki son barda kesilir, ham durum ve bayraklar yeniden; aynı olmalı."""
    Ed = ES_ESIK["d3"]; rng = np.random.default_rng([int(Ed["tohum"]), pi]); P = Pn["P"]; idx = P["tarih"]
    hd, hj = Pn["h_d"][pp], Pn["h_j"][pp]; kir = B["K20"][hd, hj]
    nk = int(round(int(Ed["n"]) * float(Ed["kirli_pay"])))
    qk = np.flatnonzero(kir); qt = np.flatnonzero(~kir)
    sec = list(rng.choice(qk, min(nk, len(qk)), replace=False)) if len(qk) else []
    sec += list(rng.choice(qt, min(int(Ed["n"]) - len(sec), len(qt)), replace=False)) if len(qt) else []
    sat, bozuk = [], []
    for q in sec:
        dd, jj = int(hd[q]), int(hj[q]); s = P["sembol"][jj]; gun = idx[dd]
        ham = Pn["Vd"]["V"][s]; kes = YH._yh_hazir(ham[ham.index < gun])
        H = es_ham(kes)
        Bk = es_bayrak_seri(kes.index.values, H["u1"], H["s10f68"], np.array([gun]).astype("datetime64[ns]"), ES_ESIK["pencere"])
        a = {k: bool(B[k][dd, jj]) for k in ES_BAYRAK}; b = {k: bool(Bk[k][0]) for k in ES_BAYRAK}
        sat.append({"sembol": s, "gun": str(pd.Timestamp(gun).date()), **{f"{k}": a[k] for k in ES_BAYRAK}, "tuttu": a == b})
        if a != b:
            bozuk.append({**sat[-1], "kesik": b})
    r = {"pazar": Pn["pazar"], "n": len(sat), "kirli_K20": int(sum(x["K20"] for x in sat)), "tuttu": len(sat) - len(bozuk), "cift": sat}
    if bozuk:
        raise ESHata(f"D3 (K2) TUTMADI {Pn['pazar']}: {bozuk[:3]} -> DURDU")
    return r


def es_d4(Pn: Dict[str, Any], X: pd.DataFrame, e_eski: Dict[str, np.ndarray], e_temiz: Dict[str, np.ndarray], haric_eski: np.ndarray,
          haric_temiz: np.ndarray, pi: int) -> Dict[str, Any]:
    """20 rastgele ölçülen olay: c2_es (eski ve K20 temiz dışlama) = kaba kuvvet (ortalama, sayı, sıra). Değerler yazılmaz, yalnız eşitlik."""
    Ed = ES_ESIK["d4"]; rng = np.random.default_rng([int(Ed["tohum"]), pi])
    q = np.flatnonzero(np.isfinite(X.r15.to_numpy(float)) & (X.kova.to_numpy() >= 0))
    sec = rng.choice(q, min(int(Ed["n"]), len(q)), replace=False) if len(q) else []
    bozuk = []; n_ok = 0
    for x in sec:
        d, j, r = int(X.d.iloc[x]), int(X.j.iloc[x]), float(X.r15.iloc[x])
        for ad, e, h in (("eski", e_eski, haric_eski), ("temiz", e_temiz, haric_temiz)):
            k = es_kaba(Pn, d, j, r, h)
            ok = (k["n_es"] == float(e["n_es"][x])) and all(
                (np.isnan(k[c]) and np.isnan(e[c][x])) or np.isclose(k[c], e[c][x], rtol=1e-9, atol=1e-15) for c in ("es_r15", "sira"))
            n_ok += int(ok)
            if not ok:
                bozuk.append({"olay": int(x), "tur": ad})
    r = {"pazar": Pn["pazar"], "olay": int(len(sec)), "karsilastirma": int(2 * len(sec)), "tuttu": n_ok}
    if bozuk:
        raise ESHata(f"D4 TUTMADI {Pn['pazar']}: {bozuk[:3]} -> DURDU")
    return r


# ================================================================ 4) A: KİRLİLİK PAYI (getirisiz)
def es_pay_tablo(Z: pd.DataFrame, havuz: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """Z: olay satırları (pazar, donem, bariz, n_es, n_kirli_K20 / K1 / KG, olculen). Hücre başına pay istatistikleri + taban."""
    sat = []
    for grup, gm in (("U1", np.ones(len(Z), bool)), ("BARIZ", Z.bariz.to_numpy(bool))):
        for p in ES_PAZAR:
            for h in ES_DONEM:
                x = Z[gm & (Z.pazar == p).to_numpy() & (Z.donem == h).to_numpy() & Z.olculen.to_numpy(bool)]
                for k in ES_BAYRAK:
                    pay = (x[f"n_kirli_{k}"] / x.n_es).to_numpy(float) if len(x) else np.array([])
                    sat.append({"grup": grup, "pazar": p, "hucre": h, "bayrak": k, "n_olay": int(len(x)),
                                "pay_ort": float(pay.mean()) if len(pay) else np.nan, "pay_med": float(np.median(pay)) if len(pay) else np.nan,
                                "pay_p90": float(np.quantile(pay, 0.9)) if len(pay) else np.nan,
                                "en_az_bir": float((x[f"n_kirli_{k}"] > 0).mean()) if len(x) else np.nan,
                                "pay_ge25": float((pay >= float(ES_ESIK["pay_esik"])).mean()) if len(pay) else np.nan,
                                "taban": havuz.get(p, {}).get(f"{h}|{k}", np.nan)})
    return pd.DataFrame(sat)


def es_havuz_taban(Pn: Dict[str, Any], B: Dict[str, Any]) -> Dict[str, float]:
    don = C2._c2_donem22(Pn["P"]["tarih"][Pn["h_d"]], ES_DONEM); out = {}
    for h in ES_DONEM:
        m = don == h
        for k in ES_BAYRAK:
            out[f"{h}|{k}"] = float(B[k][Pn["h_d"][m], Pn["h_j"][m]].mean()) if m.any() else np.nan
        out[f"{h}|n"] = int(m.sum())
    return out


# ================================================================ 5) B: HÜCRE HÜKMÜ
def es_hucre(Z: pd.DataFrame, p: str, h: str, tek: int, es_kol: str, sira_kol: str) -> Dict[str, Any]:
    x = Z[(Z.pazar == p) & (Z.donem == h)]
    x = x[np.isfinite(x.r15.to_numpy(float)) & np.isfinite(x[es_kol].to_numpy(float))]
    if len(x) < 2:
        return {"n": int(len(x)), "fark": np.nan, "hukum": "ÖLÇÜLEMEDİ", "neden": "n < 2"}
    c = C2.c2_hucre(x.r15.to_numpy(float), x[es_kol].to_numpy(float), x[sira_kol].to_numpy(float), x.giris.to_numpy(), "+",
                    tohum_ek=int(tek), egri=C2._c2_egri22_al(p, h, int(ES_ESIK["ufuk"]), None))
    ay = pd.to_datetime(x.giris).dt.strftime("%Y-%m").to_numpy()
    c["sira_alt"], c["sira_ust"] = MU.mu_sira_boot(x[sira_kol].to_numpy(float), ay, int(tek))
    c["plasebo_gecti"] = True     # plasebo HARİÇ hüküm (ön kayıt)
    hk, neden = MU.mu_hukum(c)
    return {k: c.get(k) for k in ("n", "fark", "med", "boot_alt", "boot_ust", "sira", "sira_alt", "l3o", "guc", "r15_ort", "es_ort")} | \
        {"hukum": hk, "neden": neden}


def es_tohum(grup: str, p: str, h: str) -> int:
    pi = ES_PAZAR.index(p); hi = list(ES_DONEM).index(h)
    return 100000 + pi * 100 + hi if grup == "U1" else 300 + 10 * pi + hi


def es_karar(H: Dict[str, Dict[str, Any]], grup: str, kol: str) -> Dict[str, Any]:
    hk = {f"{p}|{h}": H[f"{grup}|{kol}|{p}|{h}"]["hukum"] for p in ES_KARAR_PAZAR for h in ES_DONEM}
    deg = all(v == "TUTAR" for v in hk.values())
    return {"karar": "DEĞİŞTİRDİ" if deg else "DEĞİŞTİRMEDİ", "hukum": hk}


# ================================================================ 6) C: KİRLİ EŞ - TEMİZ EŞ (havuz) ve D: DENGE
def es_c(Pn: Dict[str, Any], F: np.ndarray, haric: Optional[np.ndarray], tohum_ek: int) -> Dict[str, Any]:
    """Bütün havuz: (d, kova) hücresi en az 1 kirli ve en az 5 temiz üye; fark = ort R15 kirli - ort R15 temiz; dönem başına kirli sayısıyla
    ağırlıklı ortalama + giriş ayı kümeli bootstrap. haric: havuzdan çıkarılacak üyeler (bilgi: U1 olay çiftleri)."""
    Ce = ES_ESIK["C"]; hd, hj, hk, r = Pn["h_d"], Pn["h_j"], Pn["h_key"], Pn["h_r"]
    k = np.ones(len(r), bool) if haric is None else ~haric
    hd, hj, hk, r = hd[k], hj[k], hk[k], r[k]
    f = F[hd, hj]
    uk, ilk, inv = np.unique(hk, return_index=True, return_inverse=True)
    nk = np.bincount(inv, weights=f.astype(float)); nt = np.bincount(inv, weights=(~f).astype(float))
    sk = np.bincount(inv, weights=np.where(f, r, 0.0)); st = np.bincount(inv, weights=np.where(f, 0.0, r))
    ok = (nk >= int(Ce["kirli_min"])) & (nt >= int(Ce["temiz_min"]))
    with np.errstate(invalid="ignore", divide="ignore"):
        fark = sk / nk - st / nt
    gun = Pn["P"]["tarih"][hd[ilk]]; don = C2._c2_donem22(gun, ES_DONEM); ay = pd.DatetimeIndex(gun).strftime("%Y-%m").to_numpy()
    out = {}
    for hi, h in enumerate(ES_DONEM):
        m = ok & (don == h)
        if not m.any():
            out[h] = {"n_hucre": 0, "n_kirli": 0, "fark": np.nan, "alt": np.nan, "ust": np.nan}
            continue
        w = nk[m]; fx = fark[m]; a = ay[m]
        ua, ai = np.unique(a, return_inverse=True); K = len(ua)
        sw = np.bincount(ai, weights=w * fx, minlength=K); ww = np.bincount(ai, weights=w, minlength=K)
        rng = np.random.default_rng([int(Ce["tohum"]), int(tohum_ek), hi])
        W = rng.multinomial(K, np.full(K, 1.0 / K), size=int(Ce["B"])).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            bs = (W @ sw) / (W @ ww)
        bs = bs[np.isfinite(bs)]
        out[h] = {"n_hucre": int(m.sum()), "n_kirli": int(w.sum()), "n_temiz": int(nt[m].sum()), "fark": float((w * fx).sum() / w.sum()),
                  "alt": float(np.quantile(bs, float(Ce["alt"]))), "ust": float(np.quantile(bs, float(Ce["ust"]))), "ay": int(K),
                  "kirli_r15": float(sk[m].sum() / w.sum()), "temiz_r15_agirliksiz": float(st[m].sum() / nt[m].sum())}
    return out


def es_denge(Pn: Dict[str, Any], X: pd.DataFrame, ii: np.ndarray, pp: np.ndarray, F: np.ndarray) -> Dict[str, Any]:
    """Ç217 eş kümelerinde (üyelik başına) K20 kirli ve temiz eşlerin ortalama F15 / ATRP; dönem başına."""
    hd, hj = Pn["h_d"][pp], Pn["h_j"][pp]; f = F[hd, hj]; f15 = Pn["F15"][hd, hj]; at = Pn["ATRP"][hd, hj]
    don = X.donem.to_numpy()[ii]; olc = np.isfinite(X.r15.to_numpy(float))[ii]; out = {}
    for h in ES_DONEM:
        m = (don == h) & olc
        r = {"n_kirli": int((m & f).sum()), "n_temiz": int((m & ~f).sum())}
        for ad, v in (("F15", f15), ("ATRP", at)):
            a = v[m & f]; b = v[m & ~f]
            r[f"{ad}_kirli"] = float(np.nanmean(a)) if len(a) else np.nan
            r[f"{ad}_temiz"] = float(np.nanmean(b)) if len(b) else np.nan
        r["F15_fark"] = r["F15_kirli"] - r["F15_temiz"]
        r["ATRP_goreli"] = r["ATRP_kirli"] / r["ATRP_temiz"] - 1 if r["ATRP_temiz"] else np.nan
        r["uyari"] = bool((np.isfinite(r["F15_fark"]) and abs(r["F15_fark"]) > float(ES_ESIK["D"]["f15_uyari"]))
                          or (np.isfinite(r["ATRP_goreli"]) and abs(r["ATRP_goreli"]) > float(ES_ESIK["D"]["atrp_goreli_uyari"])))
        out[h] = r
    return out


# ================================================================ 7) PAZAR İŞÇİSİ
def es_pazar(p: str, pi: int, veri: Optional[str], O: pd.DataFrame, satir: pd.DataFrame, olcum: bool) -> Dict[str, Any]:
    """Bir pazar: panel -> bayraklar -> D1 -> olaylar -> D2 -> kirli sayıları -> D3 -> (temiz eş: D4) -> A girdileri; olcum ise B / C / D."""
    t0 = time.time()
    Pn = C2.c2_panel22_al(p, veri, int(ES_ESIK["ufuk"]))
    B = es_panel_bayrak(Pn)
    d1 = es_d1(Pn, B, O)
    X = es_olay(Pn, O, satir)
    e0 = es_es(Pn, X)
    d2 = es_d2(X, e0)
    n_sat = int(((satir.hipotez == "U1") & (satir.pazar == p)).sum())
    if n_sat != len(X):
        raise ESHata(f"D2 {p}: olay satırı {len(X)} != Ç217 satır dosyası {n_sat} -> DURDU")
    d2["satir_dosya"] = n_sat
    d = X.d.to_numpy(np.int64); j = X.j.to_numpy(np.int64)
    har0 = es_dislanan(Pn, d, j)
    for k in ES_BAYRAK:
        isr = B[k][Pn["h_d"], Pn["h_j"]]
        X[f"n_kirli_{k}"] = es_kume_say(Pn, d, j, isr, har0)
    X["n_es"] = e0["n_es"]; X["olculen"] = np.isfinite(e0["fark"])
    if not (X[[f"n_kirli_{k}" for k in ES_BAYRAK]].to_numpy() <= X.n_es.to_numpy()[:, None]).all():
        raise ESHata(f"{p}: kirli sayısı eş sayısını aşıyor (iç tutarlılık)")
    ii, pp = es_uyeler(Pn, X, har0)
    d3 = es_d3(Pn, B, ii, pp, pi)
    # temiz eş (K20 ve KG ek dışlama); D4 kaba kuvvet
    ET = {}
    for k in ("K20", "KG"):
        kd, kj = es_kirli_cift(Pn, B[k], d)
        ET[k] = es_es(Pn, X, kd, kj)
        if k == "K20":
            d4 = es_d4(Pn, X, e0, ET[k], har0, har0 | es_dislanan(Pn, kd, kj), pi)
        n_ts = ET[k]["n_es"]; beklenen = X.n_es.to_numpy() - X[f"n_kirli_{k}"].to_numpy()
        if not np.array_equal(n_ts.astype(np.int64), beklenen.astype(np.int64)):
            raise ESHata(f"{p} {k}: temiz eş sayısı (c2_es) = eş - kirli tutmuyor (iç tutarlılık)")
    taban = es_havuz_taban(Pn, B)
    out = {"pazar": p, "D1": d1, "D2": d2, "D3": d3, "D4": d4, "taban": taban, "ham_u1_bar": B["ham_u1_bar"]}
    kol = ["pazar", "sembol", "tarih", "giris", "donem", "F65", "bariz", "r15", "d", "j", "kova", "n_es", "olculen",
           "n_kirli_K20", "n_kirli_K1", "n_kirli_KG"]
    Z = X[kol].copy()
    if olcum:
        Z["es_r15"] = e0["es_r15"]; Z["fark"] = e0["fark"]; Z["sira"] = e0["sira"]
        for k, ek in (("K20", ""), ("KG", "_KG")):
            Z[f"es_r15_temiz{ek}"] = ET[k]["es_r15"]; Z[f"n_es_temiz{ek}"] = ET[k]["n_es"]
            Z[f"fark_temiz{ek}"] = ET[k]["fark"]; Z[f"sira_temiz{ek}"] = ET[k]["sira"]
        har_olay = es_dislanan(Pn, d, j)
        out["C"] = {"K20": es_c(Pn, B["K20"], None, pi), "K20_olay_haric": es_c(Pn, B["K20"], har_olay, 10 + pi)}
        out["D"] = es_denge(Pn, X, ii, pp, B["K20"])
    out["Z"] = Z
    eslog.info("%s tamam (%.0f sn): olay %d, ölçülen %d", p, time.time() - t0, len(X), int(X.olculen.sum()))
    return out


def _es_girdi(c: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    try:
        O = pd.read_csv(_es_yol("olay", c), parse_dates=["tarih"])
        S = pd.read_csv(_es_yol("c217_satir", c), parse_dates=["tarih", "giris"])
    except (OSError, ValueError) as ex:
        raise ESHata(f"Ç217 girdileri okunamadı: {ex}") from ex
    return O, S


# ================================================================ 8) ÖN KAYIT
ES_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = Ç217 c2_es aynen (aynı giriş günü d, aynı ATRP x likidite x F15 kovası, aynı R15 açılıştan 15. bar kapanışı); taban = Ç217 eş "
                   "ortalaması; temiz eşte yalnız K20 kirli çiftler ek dışlanır (c2_es exc_d / exc_j); mekanik fark denetimi: D bölümü (kirli / "
                   "temiz eş F15 ve ATRP); 200 eş portföy plasebosu bu işte KOŞULMADI (hüküm plasebo hariç, raporda yazılı)"),
    "K2": ("EVET", "bayraklar yalnız b-20 .. b-1 barlarından (b = d'den önceki geçerli bar sayısı, searchsorted tarih < d); ham durum mu_hisse yapı "
                   "taşlarıyla (dipler [t-60, t-1], MACD [t-250, t]); D3: pazar başına 30 (d, eş) çifti veri d'den önce kesilip yeniden -> aynı; "
                   "kova / evren Ç217 paneli; KASA açık kesik 2022-12-31"),
    "K3": ("EVET", "ham durum YH._yh_hazir geçerli barlarında (H > L, V > 0); b geçerli bar sayısı; eş havuzu CETVEL2 (P ok, H >= 0, R15 sonlu)"),
    "K4": ("EVET", "olaylar Ç217'nin aynısı (dip başına ilk gün + aynı hissede 15 bar + c2_olay tekil 15; 60 gün kuralı Ç217 tanımında yok, tanım "
                   "değişmez); n = ölçülen olay; her olay bir kez; kirlilik payında ortalama + medyan + %90 birlikte"),
    "K5": ("EVET", "giriş = sinyalden sonraki ilk işlem günü açılışı (c2_olay / OC, Ç217 aynen); R15 = 15. geçerli bar kapanışı / E0 - 1"),
    "K6": ("EVET", "V_*.pkl açık kısım tek kip (sha ön kayıtta); R15 / ATRP / F15 oran; bölünme şüphesi havuz dışı (OC, Ç217 aynen)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler: batanlar yok -> sonuç yukarı yanlı okunur; raporda yazılı"),
    "K8": ("EVET", "n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ (mu_hukum); iki alt dönem d1619 / d2022 ayrı hücre; tek önceden yazılı karar kuralı (BH "
                   "gerekmez, çoklu bilgi satırları hüküm taşımaz); küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "ES_ON_KAYIT.md: ES_ESIK sha + MACD_UYUM_ES.py sha + bağımlı kod ve veri sha'ları + D1-D4 + A tablosu + karar kuralı; kos "
                   "kapısı: ön kayıt git'te işlenmiş ve değişmemiş, sha'lar aynı, ik_kontrol_kapisi, KASA kapısı, es_sonuc.json yok"),
    "K10": ("UYGULANMAZ", "metin / haber ayrıştırması yok; yalnız OHLCV ve Ç217 satır / olay dosyaları (D1 / D2 ile birebir denetlendi)"),
    "K11": ("EVET", "raporda >= 2 hücre (U1 ABD d1619 ve AVR d2022 temiz FARK / n) es_satir.csv.gz'den bağımsız düz pandas ile yeniden üretilir "
                    "(göreli 1e-9); tutmazsa DURUR"),
    "K12": ("EVET", "hüküm yalnız önceden yazılı kuralla (DEĞİŞTİRDİ / DEĞİŞTİRMEDİ; hücre TUTAR / TUTMADI / ÖLÇÜLEMEDİ); C ve D bilgi; 'iz / "
                    "emare' sözü yok; sayı ile yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_es; es_ / ES_ önekleri; test); yasak dosyalar ve mevcut macd_uyum çıktıları değişmez (git "
                    "diff); KASA bloğu açılmaz; e-posta / anahtar taraması YH._yh_yaz; push yok"),
    "K14": ("UYGULANMAZ", "bu işte alım-satım önerisi yok; ölçüm"),
}


def _y(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"{v * 100:+.{n}f}".replace(".", ",")


def _p(x: Any, n: int = 1) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"%{v * 100:.{n}f}".replace(".", ",")


def es_pay_md(T: pd.DataFrame) -> List[str]:
    L = ["| grup | pazar | hücre | bayrak | n olay | pay ort | pay medyan | pay %90 | >= 1 kirli eşli olay | pay >= %25 olay | taban (havuz) |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in T.to_dict("records"):
        L.append(f"| {r['grup']} | {r['pazar']} | {r['hucre']} | {r['bayrak']} | {r['n_olay']} | {_p(r['pay_ort'])} | {_p(r['pay_med'])} | "
                 f"{_p(r['pay_p90'])} | {_p(r['en_az_bir'])} | {_p(r['pay_ge25'])} | {_p(r['taban'])} |")
    return L


def es_hazirlik(veri: Optional[str] = None, cikti: Optional[str] = None, uzerine: bool = False) -> str:
    c = cikti or ES_YOL["cikti"]; yol = _es_yol("onkayit", c)
    if os.path.exists(yol) and not uzerine:
        raise ESHata(f"ön kayıt var: {yol} (--uzerine ile)")
    K = MU.mu_kasa(veri)
    O, S = _es_girdi(c)
    R = {}; Z = []
    for pi, p in enumerate(ES_PAZAR):
        R[p] = es_pazar(p, pi, veri, O, S, olcum=False)
        Z.append(R[p].pop("Z"))
    Zt = pd.concat(Z, ignore_index=True)
    T = es_pay_tablo(Zt, {p: R[p]["taban"] for p in ES_PAZAR})
    sha = es_sha_simdi(veri)
    kod_commit = _es_git(["log", "-1", "--format=%H %cI", "--", "MACD_UYUM_ES.py"]) or "(işlenmemiş)"
    J = {"zaman": _es_simdi(), "sha": sha, "kod_commit": kod_commit, "kasa": K, "dogrulama": {p: {k: R[p][k] for k in ("D1", "D2", "D3", "D4")}
         for p in ES_PAZAR}, "pay": T.to_dict("records"), "taban": {p: R[p]["taban"] for p in ES_PAZAR},
         "ham_u1_bar": {p: R[p]["ham_u1_bar"] for p in ES_PAZAR}}
    _es_jyaz(_es_yol("hazirlik", c), J, "ES hazırlık")
    Lr = [f"# ES_ON_KAYIT — K47 eş kirliliği (Cemal'in itirazı, 25 Kas 2026)", "",
          f"Yazıldı: {J['zaman']} ({ES_SURUM}). Getirisiz: bu dosyada yeni getiri / fark / hüküm YOK (D2 yalnız Ç217'nin yayımlanmış satır "
          "değerlerini yeniden üretir; D4 yalnız eşitlik sayısı).", "",
          "## SHA", ""]
    Lr += [f"- {k}: {v}" for k, v in sha.items()]
    Lr += [f"- kod commit (MACD_UYUM_ES.py): {kod_commit}", f"- eşik sözlüğü (ES_ESIK) sha: {sha['esik']}",
           f"- KASA: açık kesik {K['kesik']}, mühür {K.get('muhur_id')}, açılan {K.get('acilan')}", "",
           "## TANIMLAR (iş tanımı aynen)", "",
           "- HAM U1 DURUMU: MU.mu_hisse kosul['U1'] maskesi (S10 ∧ F68 ∧ DİPTE; aday gün tanımıyla) doğru olan bütün barlar; dip başına ilk gün ve 15 "
           "bar aralığı UYGULANMADAN. HAM S10F68: aynı, DİPTE şartsız (kosul['U1b']).",
           "- K20 (ANA): eşin b-20 .. b-1 barlarından en az birinde ham U1. K1 (bilgi): b-1'de ham U1. KG (bilgi): b-20 .. b-1'de en az bir ham S10F68.",
           "- BARIZ = U1 ∧ F65 <= -0,05 (uyum_satir.csv.gz). Hücreler: ABD / AVR x d1619 / d2022 KARAR; BIST BİLGİ.", "",
           "## UYGULAMA YORUMLARI (ölçümden önce)", "",
           "- b = eşin hazır (geçerli bar) serisinde tarihi d'den küçük bar sayısı. Eş havuzda olduğu için d'de geçerli barı vardır; b onun sırasıdır.",
           "- Olay kümesi Ç217 c2_olc22 ile aynı: uyum_olay U1 -> c2_olay (tekil 15); eş kümesi c2_es (olayların kendisi dışarıda). D2 bunu birebir denetler.",
           "- Kirli eş sayısı = Ç217 eş kümesinde (olay çiftleri dışarıda) bayraklı üye sayısı; pay = kirli / n_es; A tablosu yalnız Ç217'de ölçülen "
           "olaylar (n_es >= 5, R15 sonlu).",
           "- Olay hissesinin kendisi de giriş günü d'de K1 / K20 kirlidir (sinyal günü t = b-1 ham U1); Ç217'de zaten eş dışıydı.",
           "- Temiz eş: Ç217 dışlaması + olay günlerindeki bütün K20 (bilgi: KG) kirli havuz çiftleri; en az 5 temiz eş; az kalan olay düşer (sayısı yazılır).",
           "- Hüküm tohumları: U1 = Ç217 (100000 + pazar sırası x 100 + dönem sırası), BARIZ = Ç219 (300 + 10 x pazar sırası + dönem sırası); eski ve "
           "temiz aynı tohumla.",
           "- C (bilgi): bütün havuz (bütün günler). İkinci satır (bilgi, önceden yazılı): Ç217 U1 olay çiftleri havuzdan çıkarılarak.",
           "- D3: pazar başına 30 çift Ç217 eş üyeliklerinden; yarısı K20 kirli (yeterliyse), yarısı temiz (kirli bayrağı da sınansın diye).",
           "- D: uyarı eşiği |F15 kirli - temiz| > 0,05 ya da |ATRP kirli / temiz - 1| > %10.", "",
           "## DOĞRULAMALAR (D1-D4; hepsi tuttu, tutmasaydı DURURDU)", ""]
    for p in ES_PAZAR:
        d1, d2, d3, d4 = (R[p][k] for k in ("D1", "D2", "D3", "D4"))
        Lr.append(f"- {p}: D1 olay dosyası {d1['olay_dosya']} = ham üretim {d1['ham_uretim']} (ortak {d1['ortak']}) TUTTU; D2 {d2['n']} olay "
                  f"(ölçülen {d2['olculen']}) es_r15 / n_es / fark / sıra göreli 1e-9 TUTTU; D3 {d3['tuttu']} / {d3['n']} çift (kirli {d3['kirli_K20']}) "
                  f"TUTTU; D4 {d4['tuttu']} / {d4['karsilastirma']} karşılaştırma ({d4['olay']} olay x eski / temiz) TUTTU")
    Lr += ["", "## A. KİRLİLİK PAYI (getirisiz)", ""] + es_pay_md(T)
    Lr += ["", "Taban = bütün eş havuzunda (bütün günler, pazar x dönem) bayraklı (d, hisse) payı.", "",
           "## BEKLENTİ (sonuçtan önce)", "",
           "Kirli eşler olayla aynı etkiyi taşıyorsa, kirli pay p iken ölçülen fark ≈ (1 - p) x gerçek fark olur; kirlilik farkı küçültür, p %100'e "
           "yaklaşmadıkça sıfırlamaz. Yukarıdaki A tablosu p'yi verir; Ç217 farkları ±0,4 puan civarında olduğundan p küçükse temiz eşle farkın "
           "anlamlı büyümesi beklenmez.", "",
           "## KARAR KURALI (sonuçtan sonra değişmez)", "", f"- {ES_ESIK['karar']}",
           "- Açık veriye K47 için 4. bakış: TUTAR çıksa bile keşiftir; kesin hüküm yalnız KASA körüyle (Cemal kararı). Bir hücre TUTAR çıkarsa iddiadan "
           "önce plasebo kapısı gerekir; raporda 'plasebo koşulmadı' yazılır.",
           "- Evren yalnız bugün işlem görenler: sonuç yukarı yanlı (K7).", "",
           "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt; HAYIR ya da boş = kos çalışmaz)", "",
           "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    import IZ_KARNE as _IK
    Lr += [f"| {k['kod']} | {k['ad']} | {ES_KONTROL[k['kod']][0]} | {ES_KONTROL[k['kod']][1]} |" for k in _IK.IK_KONTROL]
    metin = "\n".join(Lr) + "\n"
    YH._yh_yaz(yol, metin, "ES ön kayıt")
    return yol


# ================================================================ 9) KAPI ve KOŞU
def es_kapi(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    c = cikti or ES_YOL["cikti"]; yol = _es_yol("onkayit", c)
    if not os.path.exists(yol):
        raise ESHata(f"ön kayıt yok: {yol}")
    if os.path.exists(_es_yol("sonuc", c)):
        raise ESHata("es_sonuc.json var: ikinci koşu DURDU")
    rel = os.path.relpath(yol, KOK_ES)
    if _es_git(["status", "--porcelain", "--", rel, "MACD_UYUM_ES.py"]):
        raise ESHata("ön kayıt ya da MACD_UYUM_ES.py git'te değişmiş / işlenmemiş -> DURDU")
    oc = _es_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not oc:
        raise ESHata("ön kayıt git'e işlenmemiş -> DURDU")
    metin = open(yol, encoding="utf-8").read(); S = es_sha_simdi(veri)
    bozuk = [k for k, v in S.items() if f"- {k}: {v}" not in metin]
    if bozuk:
        raise ESHata(f"sha tutmuyor: {bozuk} -> DURDU")
    import IZ_KARNE as _IK
    kk = _IK.ik_kontrol_kapisi(yol)
    K = MU.mu_kasa(veri)
    return {"onkayit": rel, "onkayit_commit": oc, "sha": S, "kontrol": kk["gecti"], "kasa": K}


def es_kos(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time(); c = cikti or ES_YOL["cikti"]
    G = es_kapi(veri, c); zaman = _es_simdi()
    O, S = _es_girdi(c)
    R, Z = {}, []
    for pi, p in enumerate(ES_PAZAR):
        R[p] = es_pazar(p, pi, veri, O, S, olcum=True)
        Z.append(R[p].pop("Z"))
    Zt = pd.concat(Z, ignore_index=True)
    Zt["n_es_temiz"] = Zt.n_es_temiz.astype(float)
    H: Dict[str, Dict[str, Any]] = {}
    for grup in ("U1", "BARIZ"):
        X = Zt if grup == "U1" else Zt[Zt.bariz]
        for p in ES_PAZAR:
            for h in ES_DONEM:
                t = es_tohum(grup, p, h)
                H[f"{grup}|eski|{p}|{h}"] = es_hucre(X, p, h, t, "es_r15", "sira")
                H[f"{grup}|temiz|{p}|{h}"] = es_hucre(X, p, h, t, "es_r15_temiz", "sira_temiz")
                H[f"{grup}|temizKG|{p}|{h}"] = es_hucre(X, p, h, t, "es_r15_temiz_KG", "sira_temiz_KG")
                x = X[(X.pazar == p) & (X.donem == h) & X.olculen]
                H[f"{grup}|dusen|{p}|{h}"] = {"K20": int((~np.isfinite(x.fark_temiz)).sum()), "KG": int((~np.isfinite(x.fark_temiz_KG)).sum())}
    # eski hücreler Ç217 / Ç219 yayımlı değerleriyle aynı mı (D2 hücre düzeyi)
    J217 = json.load(open(_es_yol("c217_sonuc", c), encoding="utf-8")); J219 = json.load(open(_es_yol("c219_sonuc", c), encoding="utf-8"))
    yay = []
    for p in ES_PAZAR:
        for h in ES_DONEM:
            for grup, ref in (("U1", J217["ana"]["U1"].get(f"{p}|{h}", {})), ("BARIZ", J219["hucre"].get(f"U1b|{p}|{h}", {}))):
                e = H[f"{grup}|eski|{p}|{h}"]
                ok = int(ref.get("n", -1)) == int(e["n"]) and np.isclose(float(ref.get("fark", np.nan)), float(e["fark"]), rtol=1e-9) and \
                    np.isclose(float(ref.get("sira", np.nan)), float(e["sira"]), rtol=1e-9) and ref.get("hukum", e["hukum"]) == e["hukum"]
                yay.append({"grup": grup, "pazar": p, "hucre": h, "tuttu": bool(ok)})
    if not all(y["tuttu"] for y in yay):
        raise ESHata(f"eski hücreler Ç217 / Ç219 yayımlı değerleriyle tutmuyor: {[y for y in yay if not y['tuttu']]} -> DURDU")
    karar = {g: es_karar(H, g, "temiz") for g in ("U1", "BARIZ")}
    karar_kg = {g: es_karar(H, g, "temizKG") for g in ("U1", "BARIZ")}
    # satır dosyası + K11 yeniden üretim
    kol = ["pazar", "sembol", "tarih", "giris", "donem", "F65", "bariz", "r15", "es_r15", "n_es", "fark", "sira", "n_kirli_K20", "n_kirli_K1",
           "n_kirli_KG", "es_r15_temiz", "n_es_temiz", "fark_temiz", "sira_temiz", "es_r15_temiz_KG", "n_es_temiz_KG", "fark_temiz_KG",
           "sira_temiz_KG", "olculen"]
    Zs = Zt[kol].copy(); Zs["tarih"] = pd.to_datetime(Zs.tarih).dt.strftime("%Y-%m-%d"); Zs["giris"] = pd.to_datetime(Zs.giris).dt.strftime("%Y-%m-%d")
    sy = _es_yol("satir", c)
    Zs.to_csv(sy, index=False, float_format="%.12g", compression="gzip")
    Y = pd.read_csv(sy)
    yen = {}
    for p, h in (("ABD", "d1619"), ("AVR", "d2022")):
        y = Y[(Y.pazar == p) & (Y.donem == h)].dropna(subset=["r15", "es_r15_temiz"])
        f = float((y.r15 - y.es_r15_temiz).mean()); e = H[f"U1|temiz|{p}|{h}"]
        yen[f"{p}|{h}"] = {"n": int(len(y)), "fark": f, "tuttu": bool(len(y) == e["n"] and np.isclose(f, e["fark"], rtol=1e-9))}
    if not all(v["tuttu"] for v in yen.values()):
        raise ESHata(f"K11 yeniden üretim tutmadı: {yen} -> DURDU")
    J = {"surum": ES_SURUM, "zaman": zaman, "kapi": {k: v for k, v in G.items()}, "karar": karar, "karar_KG": karar_kg, "hucre": H,
         "yayimli_esitlik": yay, "C": {p: R[p]["C"] for p in ES_PAZAR}, "D": {p: R[p]["D"] for p in ES_PAZAR},
         "dogrulama": {p: {k: R[p][k] for k in ("D1", "D2", "D3", "D4")} for p in ES_PAZAR}, "yeniden": yen,
         "satir_dosya": os.path.relpath(sy, KOK_ES), "satir_sha": _es_sha(sy), "sure_sn": round(time.time() - t0, 1)}
    _es_jyaz(_es_yol("sonuc", c), J, "ES sonuç")
    es_rapor(J, c)
    return J


# ================================================================ 10) RAPOR
def es_rapor(J: Dict[str, Any], cikti: Optional[str] = None) -> str:
    c = cikti or ES_YOL["cikti"]; H = J["hucre"]
    L = ["# ES_RAPOR — K47 eş kirliliği: temiz eşle yeniden ölçüm", "",
         f"Koşu {J['zaman']}; ön kayıt {J['kapi']['onkayit_commit']}; {ES_SURUM}. Açık veri (KASA kesik 2022-12-31). Hüküm plasebo HARİÇ; "
         "plasebo koşulmadı. Evren bugün işlem görenler: sonuç yukarı yanlı.", "",
         f"KARAR U1: {J['karar']['U1']['karar']} {J['karar']['U1']['hukum']}",
         f"KARAR BARIZ: {J['karar']['BARIZ']['karar']} {J['karar']['BARIZ']['hukum']}",
         f"(bilgi, KG dışlama) U1: {J['karar_KG']['U1']['karar']}; BARIZ: {J['karar_KG']['BARIZ']['karar']}", "",
         "## B. Hücreler (K20 temiz eş)", "",
         "| grup | pazar | hücre | n eski / temiz (düşen) | FARK eski [%95] | FARK temiz [%95] | temiz - eski | SIRA eski / temiz [alt] | güç temiz | hüküm eski / temiz |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for g in ("U1", "BARIZ"):
        for p in ES_PAZAR:
            for h in ES_DONEM:
                e, t, du = H[f"{g}|eski|{p}|{h}"], H[f"{g}|temiz|{p}|{h}"], H[f"{g}|dusen|{p}|{h}"]
                L.append(f"| {g} | {p} | {h} | {e['n']} / {t['n']} ({du['K20']}) | {_y(e['fark'])} [{_y(e.get('boot_alt'))}; {_y(e.get('boot_ust'))}] | "
                         f"{_y(t['fark'])} [{_y(t.get('boot_alt'))}; {_y(t.get('boot_ust'))}] | {_y(t['fark'] - e['fark'] if t['fark'] is not None and e['fark'] is not None else np.nan)} | "
                         f"{(e.get('sira') or float('nan')):.3f} / {(t.get('sira') or float('nan')):.3f} [{(t.get('sira_alt') or float('nan')):.3f}] | "
                         f"{(t.get('guc') or float('nan')):.2f} | {e['hukum']} / {t['hukum']} |")
    L += ["", "## B (bilgi). KG temiz eş", "", "| grup | pazar | hücre | n temiz KG (düşen) | FARK temiz KG [%95] | KG - eski | hüküm |", "|---|---|---|---|---|---|---|"]
    for g in ("U1", "BARIZ"):
        for p in ES_PAZAR:
            for h in ES_DONEM:
                e, t, du = H[f"{g}|eski|{p}|{h}"], H[f"{g}|temizKG|{p}|{h}"], H[f"{g}|dusen|{p}|{h}"]
                L.append(f"| {g} | {p} | {h} | {t['n']} ({du['KG']}) | {_y(t['fark'])} [{_y(t.get('boot_alt'))}; {_y(t.get('boot_ust'))}] | "
                         f"{_y(t['fark'] - e['fark'] if t['fark'] is not None and e['fark'] is not None else np.nan)} | {t['hukum']} |")
    L += ["", "## C. Kirli eş - temiz eş (bütün havuz, K20; bilgi)", "",
          "| pazar | hücre | (d, kova) hücre | kirli üye | fark [%95] | olay çiftleri hariç: fark [%95] |", "|---|---|---|---|---|---|"]
    for p in ES_PAZAR:
        for h in ES_DONEM:
            a, b = J["C"][p]["K20"][h], J["C"][p]["K20_olay_haric"][h]
            L.append(f"| {p} | {h} | {a['n_hucre']} | {a['n_kirli']} | {_y(a['fark'])} [{_y(a['alt'])}; {_y(a['ust'])}] | "
                     f"{_y(b['fark'])} [{_y(b['alt'])}; {_y(b['ust'])}] (kirli {b['n_kirli']}) |")
    L += ["", "## D. Denge (Ç217 eş kümelerinde K20 kirli / temiz eş)", "", "| pazar | hücre | n kirli / temiz | F15 kirli / temiz | ATRP kirli / temiz | uyarı |",
          "|---|---|---|---|---|---|"]
    for p in ES_PAZAR:
        for h in ES_DONEM:
            d = J["D"][p][h]
            L.append(f"| {p} | {h} | {d['n_kirli']} / {d['n_temiz']} | {d['F15_kirli']:.3f} / {d['F15_temiz']:.3f} | "
                     f"{_p(d['ATRP_kirli'], 2)} / {_p(d['ATRP_temiz'], 2)} | {'UYARI' if d['uyari'] else '-'} |")
    L += ["", f"Satır dosyası: {J['satir_dosya']} (sha {J['satir_sha'][:16]}); K11 yeniden üretim: {J['yeniden']}", ""]
    metin = "\n".join(L) + "\n"
    YH._yh_yaz(_es_yol("rapor", c), metin, "ES rapor")
    return metin


# ================================================================ 11) ÇAKIŞMA KAPISI
def _cakisma_kontrol_es(_once=_CK_ONCE_ES, _dosya="MACD_UYUM_ES.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_ES", "_CK_KAYIT", "_cakisma_kontrol_es", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "hashlib", "subprocess", "time", "_dt", "annotations", "Any", "Dict", "List",
           "Optional", "Tuple", "_swv", "C2", "MU", "YH", "_y", "_p")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_es()


def _es_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=ES_SURUM)
    alt = ap.add_subparsers(dest="komut", required=True)
    for k in ("hazirlik", "kos", "sha"):
        p = alt.add_parser(k); p.add_argument("--veri", default=None); p.add_argument("--cikti", default=None)
        if k == "hazirlik":
            p.add_argument("--uzerine", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.komut == "hazirlik":
            print("ÖN KAYIT:", es_hazirlik(a.veri, a.cikti, a.uzerine))
        elif a.komut == "kos":
            J = es_kos(a.veri, a.cikti)
            print("KOŞU TAMAM:", {g: J["karar"][g]["karar"] for g in J["karar"]})
        else:
            print(json.dumps(es_sha_simdi(a.veri), ensure_ascii=False, indent=1))
    except (ESHata, MU.MUHata) as ex:
        eslog.error("%s", ex)
        print(f"DURDU: {ex}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__" and "get_ipython" not in globals():
    sys.exit(_es_ana())
