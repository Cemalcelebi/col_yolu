"""ornek20_ciz — MACD_UYUM U1 olaylarından 20 rastgele olayın KÖR görsel seti (24 Kasım 2026; iş tanımı: ana model mesajı).

Cemal (24 Kas 2026): "yaptığın örneklemden tamamıyla rastgele 20 tane göster, kodun seçtiği uyumsuzluğu göreyim". Cemal her sayfada DOĞRU /
YANLIŞ işaretler. Bu betik ÖLÇMEZ ve HÜKÜM VERMEZ; yalnız kodun t günündeki görüşünü çizer.

SEÇİM: uyum_ornek20_secim.json (tohum 2574117880; uyum_satir.csv.gz içindeki 5.838 U1 olayından 20; sayfa sırası dosyadaki 'sayfa' alanı).
  Seçim dosyası DEĞİŞTİRİLMEZ, yeni seçim yapılmaz; satır dosyasının sha'sı seçimdeki satir_sha256 ile aynı olmalı (değilse DURUR).
KODUN GÖRÜŞÜ (MACD_UYUM / YAPI_HEDEF fonksiyonları çağrılır; yeniden yazılmaz):
  veri  = MU.C2.c2_veri (= DUSUS_SONRASI.ds_veri; ölçümle aynı yol), hissenin verisi t'de KESİLİR, YH._yh_hazir (geçerli bar: H > L, V > 0)
  olay  = MU.mu_hisse(kesik seri) içindeki U1 olayı (t günü): L1, L2, F65, F66, F68, S10, DİPTE
  MACD  = YH.yh_macd(Close[t-250 .. t]) (12, 26, 9; ewm adjust=False; pencerenin ilk 35 barı ısınma) = yh_s10_bar'ın t'deki MACD'si
  RSI   = MU._mu_rsi (Wilder 14; serinin başından t'ye, nedensel; yalnız bilgi paneli)
SAYFA: A4 dikey; başlıkta sayfa no ve pazar; fiyat paneli max(seri başı, L2 - 125) .. t (t son bar); hisse adı, tarih, t'den sonrası ve sonuç yok.
YENİDEN HESAP (K10 / K11): her sayfanın ÇİZİM verisinden (yalnız çizilen barlar ve çizilen MACD) L1, L2, MACD(L1), MACD(L2), F65, F66, F68,
  DİPTE (ve F66m, F66h, F67, tL2, s65, s66, S10, stop, 120 bar tepesi) yeniden hesaplanır; satır dosyası, yh_s10_bar (birebir), kesik seride
  mu_hisse (birebir) ve olay dosyasıyla (12 anlamlı basamak) aynı olmalı; biri tutmazsa DURUR: anahtar ve PDF yazılmaz.
ANAHTAR: uyum_ornek20_anahtar.json (sayfa başına pazar, sembol, t, L1 / L2 tarihi, giriş, stop, h5, h10, stop_oldu, r15, es_r15, fark;
  satır dosyasından AYNEN). PDF'e girmez; sha256'sı kapakta yazılır (mühür). İçerik belirlenimci (zaman damgası yok); dosya varsa ve
  farklıysa DURUR (--uzerine verilmedikçe). Sonuç değerleri ekrana BASILMAZ.

Komut (repo kökünden):
  python arastirma_cikti/macd_uyum/ornek20_ciz.py ciz [--uzerine]   denetim -> anahtar -> UYUM_ORNEK20.pdf (kapak + 20 sayfa) + tablo
  python arastirma_cikti/macd_uyum/ornek20_ciz.py denetim           yalnız yeniden hesap tablosu (dosya yazmaz)
Veri: /tmp/kasa/acik (V_ABD.pkl, V_AVR.pkl, V_BIST.pkl; KASA açık kesik 2022-12-31; sha'lar UYUM_ON_KAYIT.md ile aynı olmalı). Ortam: O20_VERI.
MACD_UYUM.py, YAPI_HEDEF.py, seçim ve satır dosyaları DEĞİŞTİRİLMEZ; yalnız okunur. Colab: kod değiştiyse çalışma zamanını yeniden başlat.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_O20 = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import textwrap  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

O20_DIR = (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals()
           else os.path.join(os.getcwd(), "arastirma_cikti", "macd_uyum"))
O20_KOK = os.path.dirname(os.path.dirname(O20_DIR))
if O20_KOK not in sys.path:
    sys.path.insert(0, O20_KOK)

import MACD_UYUM as MU  # noqa: E402  (yalnız okunur: mu_kasa, mu_hisse, _mu_rsi, _mu_onkayit_sha, MU_ESIK, MU_PAZAR, C2)
import YAPI_HEDEF as YH  # noqa: E402  (yalnız okunur: _yh_hazir, yh_macd, yh_s10_bar, yh_s10_dipler, YH_ESIK8, _YH_S10_OZ, _yh_yaz)

o20log = logging.getLogger("col.ornek20")
if not o20log.handlers:
    _o20_h = logging.StreamHandler(sys.stderr)
    _o20_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s ornek20: %(message)s", "%H:%M:%S"))
    o20log.addHandler(_o20_h)
    o20log.setLevel(logging.INFO)
    o20log.propagate = False

O20_SURUM = "ornek20_ciz v1 (2026-11-24): MACD_UYUM U1 kör görsel set, 20 rastgele olay (kodun t günündeki görüşü)"
O20_YOL: Dict[str, str] = {
    "secim": os.path.join(O20_DIR, "uyum_ornek20_secim.json"),
    "satir": os.path.join(O20_DIR, "uyum_satir.csv.gz"),
    "olay": os.path.join(O20_DIR, "uyum_olay.csv.gz"),
    "onkayit": os.path.join(O20_DIR, "UYUM_ON_KAYIT.md"),
    "anahtar": os.path.join(O20_DIR, "uyum_ornek20_anahtar.json"),
    "pdf": os.path.join(O20_DIR, "UYUM_ORNEK20.pdf"),
    "veri": os.environ.get("O20_VERI", "/tmp/kasa/acik"),
}
O20_ESIK: Dict[str, Any] = {
    "hipotez": "U1", "sayfa_n": 20, "evren_n": 5838, "tohum": 2574117880,
    "oncesi": 125,                 # fiyat paneli max(seri başı, L2 - 125) .. t
    "rtol_satir": 1e-12,           # satır dosyası %.15g yazıldı
    "rtol_olay": 1e-10,            # olay dosyası %.12g yazıldı
    "pdf_tercih": 3 * 1024 * 1024, "pdf_azami": 8 * 1024 * 1024,
    "sayfa_boyut": (8.27, 11.69),  # A4 dikey (inç)
    "etiket_ara": 16,              # '1. dip' / '2. dip' etiket merkezleri arası en az bar
}
O20_ANAHTAR_ALAN = ["sayfa", "pazar", "sembol", "tarih", "L1_tarih", "L2_tarih", "giris", "E0", "stop", "h5", "h10", "stop_oldu", "r15",
                    "es_r15", "fark"]
O20_RENK = {"yukari": "#1a9850", "asagi": "#d73027", "mavi": "#1f4e9c", "stop": "#d62728", "tepe": "#7f7f7f", "sinyal_gunu": "#444444",
            "macd": "#000000", "sinyal": "#e31a1c", "hist": "#b9b9b9", "rsi": "#6a3d9a", "ipucu": "#666666"}
O20_KESIK = "mu_hisse (t'de kesik)"   # kodun t günündeki görüşü: veri t'de kesilip MU.mu_hisse ile yeniden taranır


class O20Hata(RuntimeError):
    """Durdurucu hata: seçim / satır / veri sha tutmuyor ya da çizimden yeniden hesap koddan farklı (DUR; dosya yazılmaz)."""


# ================================================================ 0) ORTAK
def _o20_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _o20_rel(yol: str) -> str:
    return os.path.relpath(yol, O20_KOK)


def _o20_f(x: Any) -> Optional[float]:
    """JSON için sayı: sonlu değilse None (satır dosyasındaki boş hücre)."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if np.isfinite(v) else None


def _o20_yuzde(x: float, n: int = 2, isaret: bool = True) -> str:
    v = 100.0 * float(x)
    s = f"{v:+.{n}f}" if isaret else f"{v:.{n}f}"
    return "%" + s.replace(".", ",")


def _o20_sayi(x: float, anlamli: int = 4) -> str:
    """MACD gibi fiyat birimli sayı: 4 anlamlı basamak, ondalık virgül, bilimsel gösterim yok."""
    v = float(x)
    if not np.isfinite(v):
        return "-"
    if v == 0.0:
        return "0"
    b = max(0, anlamli - 1 - int(math.floor(math.log10(abs(v)))))
    return f"{v:.{b}f}".replace(".", ",")


def _o20_yakin(a: Any, b: Any, rtol: float) -> bool:
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError):
        return False
    if not (np.isfinite(a) and np.isfinite(b)):
        return False
    return abs(a - b) <= rtol * max(abs(a), abs(b)) or a == b


# ================================================================ 1) GİRDİLER (seçim, satır, olay, veri kapısı)
def o20_secim() -> Dict[str, Any]:
    """Seçim dosyası (DEĞİŞMEZ): 20 sayfa, 1..20, tekil; tohum / evren iş tanımıyla; satır sha'sı seçimdekiyle aynı."""
    J = json.load(open(O20_YOL["secim"], encoding="utf-8"))
    S = list(J.get("secim", []))
    no = sorted(int(s["sayfa"]) for s in S)
    if no != list(range(1, int(O20_ESIK["sayfa_n"]) + 1)):
        raise O20Hata(f"seçim sayfaları 1..{O20_ESIK['sayfa_n']} değil: {no}")
    if int(J["tohum"]) != int(O20_ESIK["tohum"]) or int(J["evren_n"]) != int(O20_ESIK["evren_n"]):
        raise O20Hata(f"seçim tohumu / evren sayısı iş tanımından farklı: {J['tohum']} / {J['evren_n']}")
    if len({(s["pazar"], s["sembol"], s["tarih"]) for s in S}) != len(S):
        raise O20Hata("seçimde tekrar eden olay var")
    sha = _o20_sha(O20_YOL["satir"])
    if sha != J["satir_sha256"]:
        raise O20Hata(f"satır dosyası seçimdeki sha ile aynı değil: {sha} != {J['satir_sha256']}")
    return {**J, "secim": sorted(S, key=lambda s: int(s["sayfa"])), "secim_sha256": _o20_sha(O20_YOL["secim"]), "satir_sha256": sha}


def o20_satir(J: Dict[str, Any]) -> pd.DataFrame:
    """Seçilen 20 olayın satır dosyası satırları (U1), seçim sırasıyla. Seçimdeki giriş / dönem / L1 / L2 / E0 / stop0 satırla aynı olmalı."""
    X = pd.read_csv(O20_YOL["satir"], dtype={"tarih": str, "giris": str, "L1_tarih": str, "L2_tarih": str, "sembol": str})
    U = X[X.hipotez == O20_ESIK["hipotez"]]
    if len(U) != int(J["evren_n"]):
        raise O20Hata(f"satır dosyasında U1 olayı {len(U)} (seçimde {J['evren_n']})")
    sat = []
    for s in J["secim"]:
        m = U[(U.pazar == s["pazar"]) & (U.sembol == s["sembol"]) & (U.tarih == s["tarih"])]
        if len(m) != 1:
            raise O20Hata(f"sayfa {s['sayfa']}: satır dosyasında {len(m)} eşleşme")
        r = m.iloc[0]
        for k in ("giris", "donem", "L1_tarih", "L2_tarih"):
            if str(r[k]) != str(s[k]):
                raise O20Hata(f"sayfa {s['sayfa']}: seçim {k} {s[k]} != satır {r[k]}")
        for k in ("E0", "stop0"):
            if not _o20_yakin(r[k], s[k], O20_ESIK["rtol_satir"]):
                raise O20Hata(f"sayfa {s['sayfa']}: seçim {k} satırdan farklı")
        sat.append(r)
    return pd.DataFrame(sat).reset_index(drop=True)


def o20_olay(J: Dict[str, Any]) -> List[pd.Series]:
    """Ön kayıttaki olay dosyasının (tam seri taraması) aynı U1 satırları (L1 / L2 sırası, tepe120, F66m vb.)."""
    O = pd.read_csv(O20_YOL["olay"], dtype={"tarih": str, "L1_tarih": str, "L2_tarih": str, "sembol": str})
    U = O[O.hipotez == O20_ESIK["hipotez"]]
    out = []
    for s in J["secim"]:
        m = U[(U.pazar == s["pazar"]) & (U.sembol == s["sembol"]) & (U.tarih == s["tarih"])]
        if len(m) != 1:
            raise O20Hata(f"sayfa {s['sayfa']}: olay dosyasında {len(m)} eşleşme")
        out.append(m.iloc[0])
    return out


def o20_kapi(veri: str) -> Dict[str, Any]:
    """KASA kapısı (MU.mu_kasa: açık kesik 2022-12-31; DURUR) + V_*.pkl sha'ları UYUM_ON_KAYIT.md'dekiyle aynı (ölçümün verisi; K6)."""
    K = MU.mu_kasa(veri)
    metin = open(O20_YOL["onkayit"], encoding="utf-8").read()
    sha = {}
    for p in MU.MU_PAZAR:
        s = _o20_sha(os.path.join(veri, f"V_{p}.pkl")); b = MU._mu_onkayit_sha(metin, f"V_{p}_SHA")
        if s != b:
            raise O20Hata(f"V_{p}.pkl sha ön kayıttakinden farklı: {s} != {b}")
        sha[p] = s
    return {"kasa": K, "veri_sha": sha}


# ================================================================ 2) KODUN t GÜNÜNDEKİ GÖRÜŞÜ ve ÇİZİM VERİSİ
def o20_gorus(Vd: Dict[str, Any], sembol: str, tarih: str) -> Dict[str, Any]:
    """Veri t'de kesilir (K2) -> geçerli bar (K3) -> MU.mu_hisse U1 olayı (t) + yh_s10_bar + MACD [t-250, t] + RSI (nedensel)."""
    E8 = YH.YH_ESIK8
    if sembol not in Vd["V"]:
        raise O20Hata(f"{sembol}: veride yok")
    ham = Vd["V"][sembol]; t = pd.Timestamp(tarih)
    kes = YH._yh_hazir(ham[ham.index <= t])
    if not len(kes) or kes.index[-1] != t:
        raise O20Hata(f"{sembol} {tarih}: sinyal günü geçerli bar değil")
    ti = len(kes) - 1
    Op, Hi, Lo, Cl, Vo = (kes[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    if not bool(((Hi > Lo) & (Vo > 0) & (Op > 0) & (Cl > 0) & (Lo > 0)).all()):
        raise O20Hata(f"{sembol} {tarih}: geçersiz bar var (K3)")
    Ev, _ = MU.mu_hisse(kes)
    e = Ev[(Ev.hipotez == O20_ESIK["hipotez"]) & (pd.to_datetime(Ev.tarih) == t)]
    if len(e) != 1:
        raise O20Hata(f"{sembol} {tarih}: veri t'de kesilince U1 olayı {len(e)} (1 olmalı; K2)")
    yh = YH.yh_s10_bar(Lo, Cl, ti, E8)
    w0 = max(0, ti - int(E8["macd"]["pencere"]))
    m, s, h = YH.yh_macd(np.asarray(Cl[w0:ti + 1], float), E8)
    rsi = MU._mu_rsi(Cl)
    return {"sembol": sembol, "t": t, "ti": ti, "idx": kes.index, "O": Op, "H": Hi, "L": Lo, "C": Cl, "V": Vo,
            "olay": e.iloc[0], "yh": yh, "w0": w0, "m": m, "s": s, "h": h, "rsi": rsi}


def o20_cizim(g: Dict[str, Any]) -> Dict[str, Any]:
    """Sayfada çizilecek veri: pencere [max(0, L2 - 125), t]; MACD / sinyal / histogram t günündeki pencereden. Daireler kodun L1 / L2'si."""
    ti, w0 = int(g["ti"]), int(g["w0"])
    L1, L2 = int(g["olay"]["L1"]), int(g["olay"]["L2"])
    a = max(0, L2 - int(O20_ESIK["oncesi"]))
    if a < w0:
        raise O20Hata("çizim penceresi MACD penceresinin [t-250, t] dışında")
    sl = slice(a, ti + 1); sm = slice(a - w0, ti + 1 - w0)
    cz = {"a": a, "ti": ti, "tarih": pd.DatetimeIndex(g["idx"][sl]), "O": g["O"][sl].copy(), "H": g["H"][sl].copy(), "L": g["L"][sl].copy(),
          "C": g["C"][sl].copy(), "V": g["V"][sl].copy(), "macd": g["m"][sm].copy(), "sinyal": g["s"][sm].copy(), "hist": g["h"][sm].copy(),
          "rsi": g["rsi"][sl].copy(), "i1": L1 - a, "i2": L2 - a}
    if len(cz["macd"]) != len(cz["L"]) or cz["tarih"][-1] != g["t"] or bool((cz["tarih"] > g["t"]).any()):
        raise O20Hata("çizim penceresi t'de bitmiyor ya da boyları farklı (K2)")
    if not bool(np.all(np.diff(cz["tarih"].asi8) > 0)):
        raise O20Hata("çizim penceresi sıralı / tekil değil (K3)")
    return cz


def o20_yeniden(cz: Dict[str, Any]) -> Dict[str, Any]:
    """YALNIZ çizim verisinden (çizilen barlar ve çizilen MACD): dipler, L1 / L2, MACD(L1), MACD(L2), F65, F66, F66m, F66h, F67, tL2, s65,
    s66, S10, F68, DİPTE, stop, 120 bar tepesi / dibi. Kurallar YH_ESIK8 / MU_ESIK ile aynı işlem sırası (birebir karşılaştırma için)."""
    E8 = YH.YH_ESIK8; T = E8["esik"]; Dp = MU.MU_ESIK["dipte"]
    L, H, C = cz["L"], cz["H"], cz["C"]; n = len(L) - 1
    dip = YH.yh_s10_dipler(L, n, E8)
    if not dip:
        raise O20Hata("çizimde dip bulunamadı")
    i2 = dip[-1]
    onceki = [k for k in dip if k <= i2 - int(E8["dip"]["L1_min_ara"])]
    if not onceki:
        raise O20Hata("çizimde L1 bulunamadı")
    i1 = onceki[-1]
    m1, m2 = float(cz["macd"][i1]), float(cz["macd"][i2]); h1, h2 = float(cz["hist"][i1]), float(cz["hist"][i2])
    l1, l2, c2 = float(L[i1]), float(L[i2]), float(C[i2])
    s65 = l2 <= l1 * (1.0 + float(T["F65_ust"]))
    s66 = (m2 - m1) / c2 > float(T["F66_alt_acik"]) and m2 / c2 < float(T["F66m_ust_acik"])
    mt, st = float(cz["macd"][n]), float(cz["sinyal"][n])
    F68 = (1.0 if mt > st else 0.0) if (np.isfinite(mt) and np.isfinite(st)) else np.nan
    g = int(Dp["geri"])
    if i2 - g < 0:
        raise O20Hata("çizimde 2. dipten geriye 120 bar yok (DİPTE hesaplanamaz)")
    mn = float(np.min(L[i2 - g:i2])); tepe = float(np.max(H[i2 - g:i2 + 1]))
    dipte = bool((l2 <= mn * (1.0 + float(Dp["dip_tol"]))) and (c2 <= float(Dp["tepe_pay"]) * tepe))
    return {"i1": int(i1), "i2": int(i2), "dipler": [int(k) for k in dip],
            "L1_tarih": str(cz["tarih"][i1].date()), "L2_tarih": str(cz["tarih"][i2].date()), "t": str(cz["tarih"][n].date()),
            "m1": m1, "m2": m2, "macd_t": mt, "sinyal_t": st,
            "F65": l2 / l1 - 1.0, "F66": (m2 - m1) / c2, "F66m": m2 / c2, "F66h": (h2 - h1) / c2, "F67": float(i2 - i1), "F68": F68,
            "tL2": float(n - i2), "s65": 1.0 if s65 else 0.0, "s66": 1.0 if s66 else 0.0, "S10": 1.0 if (s65 and s66) else 0.0,
            "dipte": dipte, "tepe120": tepe, "dip120": mn, "dusus120": 1.0 - c2 / tepe, "dip120_oran": l2 / mn - 1.0,
            "stop0": l2 * float(MU.MU_ESIK["stop_carpan"]), "low_L1": l1, "low_L2": l2, "close_L2": c2, "close_t": float(C[n]),
            "rsi_L1": float(cz["rsi"][i1]), "rsi_L2": float(cz["rsi"][i2])}


def o20_karsilastir(Y: Dict[str, Any], cz: Dict[str, Any], g: Dict[str, Any], sat: pd.Series, ol: pd.Series) -> Dict[str, Any]:
    """Çizimden yeniden hesap = satır dosyası / yh_s10_bar (birebir) / kesik seride mu_hisse (birebir) / olay dosyası. Kontrol listesi döner."""
    K: List[Dict[str, Any]] = []
    rs, ro = float(O20_ESIK["rtol_satir"]), float(O20_ESIK["rtol_olay"])

    def ek(grup: str, ad: str, kaynak: str, beklenen: Any, bulunan: Any, tur: str = "esit", rtol: float = 0.0) -> None:
        if tur == "esit":
            ok = bool(beklenen == bulunan)
        else:
            ok = _o20_yakin(beklenen, bulunan, rtol)
        K.append({"grup": grup, "ad": ad, "kaynak": kaynak, "tamam": ok, "beklenen": beklenen, "bulunan": bulunan})

    a = int(cz["a"]); e = g["olay"]; yh = g["yh"]
    # (a) çizimdeki daireler = çizim verisinden bulunan dipler
    ek("L1", "daire L1 = çizimden L1", "çizim", int(cz["i1"]), Y["i1"])
    ek("L2", "daire L2 = çizimden L2", "çizim", int(cz["i2"]), Y["i2"])
    # (b) satır dosyası
    ek("L1", "L1_tarih", "satır", str(sat["L1_tarih"]), Y["L1_tarih"])
    ek("L2", "L2_tarih", "satır", str(sat["L2_tarih"]), Y["L2_tarih"])
    ek("t", "sinyal günü", "satır", str(sat["tarih"]), Y["t"])
    for k in ("F65", "F66", "stop0", "rsi_L1", "rsi_L2", "close_t"):
        ek({"F65": "F65", "F66": "F66"}.get(k, "diğer"), k, "satır", float(sat[k]), Y[k], "yakin", rs)
    for k in ("F68", "S10", "s66"):
        ek({"F68": "F68", "S10": "S10", "s66": "F66"}[k], k, "satır", float(sat[k]), Y[k])
    ek("DİPTE", "dipte", "satır", bool(sat["dipte"]) if not isinstance(sat["dipte"], str) else sat["dipte"] == "True", Y["dipte"])
    # MACD(L1), MACD(L2): satırdaki F66 ile ve yh_s10_bar F66 / F66m'den geri kurulan değerlerle
    c2 = float(cz["C"][cz["i2"]])
    m2k = float(yh["F66m"]) * c2; m1k = m2k - float(yh["F66"]) * c2
    ek("MACD(L2)", "MACD(L2) = F66m x C(L2) (yh_s10_bar)", "yh_s10_bar", m2k, Y["m2"], "yakin", 1e-12)
    ek("MACD(L1)", "MACD(L1) = MACD(L2) - F66 x C(L2) (yh_s10_bar)", "yh_s10_bar", m1k, Y["m1"], "yakin", 1e-9)
    # (c) yh_s10_bar birebir (10 çıktı)
    for k in YH._YH_S10_OZ:
        grp = {"F65": "F65", "F66": "F66", "F66m": "MACD(L2)", "F68": "F68", "S10": "S10"}.get(k, "yh_s10_bar")
        ek(grp, k, "yh_s10_bar", float(yh[k]), float(Y[k]))
    # (d) kesik seride mu_hisse (kodun t günündeki görüşü) birebir
    ek("L1", "L1 sırası", O20_KESIK, int(e["L1"]), a + Y["i1"])
    ek("L2", "L2 sırası", O20_KESIK, int(e["L2"]), a + Y["i2"])
    ek("t", "t sırası", O20_KESIK, int(e["i"]), a + len(cz["L"]) - 1)
    for k in ("F65", "F66", "F66m", "F66h", "F67", "F68", "s65", "s66", "S10", "tL2", "tepe120", "low_L1", "low_L2", "close_L2", "close_t",
              "stop0", "rsi_L1", "rsi_L2"):
        grp = {"F65": "F65", "F66": "F66", "F66m": "MACD(L2)", "F68": "F68", "S10": "S10", "tepe120": "DİPTE"}.get(k, "mu_hisse")
        ek(grp, k, O20_KESIK, float(e[k]), float(Y[k]))
    ek("DİPTE", "dipte", O20_KESIK, bool(e["dipte"]), Y["dipte"])
    # (e) ön kayıttaki olay dosyası (tam seri taraması; %.12g)
    ek("L1", "L1 sırası", "olay dosyası", int(ol["L1"]), a + Y["i1"])
    ek("L2", "L2 sırası", "olay dosyası", int(ol["L2"]), a + Y["i2"])
    ek("t", "t sırası", "olay dosyası", int(ol["i"]), a + len(cz["L"]) - 1)
    ek("L1", "L1_tarih", "olay dosyası", str(ol["L1_tarih"]), Y["L1_tarih"])
    ek("L2", "L2_tarih", "olay dosyası", str(ol["L2_tarih"]), Y["L2_tarih"])
    for k in ("F65", "F66", "F66m", "F66h", "tepe120", "low_L1", "low_L2", "close_L2", "close_t", "stop0"):
        ek({"F65": "F65", "F66": "F66", "F66m": "MACD(L2)", "tepe120": "DİPTE"}.get(k, "olay"), k, "olay dosyası", float(ol[k]), float(Y[k]),
           "yakin", ro)
    for k in ("F67", "F68", "s65", "s66", "S10", "tL2"):
        ek({"F68": "F68", "S10": "S10"}.get(k, "olay"), k, "olay dosyası", float(ol[k]), float(Y[k]))
    dp = ol["dipte"]
    ek("DİPTE", "dipte", "olay dosyası", (dp == "True") if isinstance(dp, str) else bool(dp), Y["dipte"])
    # (f) U1 tanımı çizimde tutuyor (S10 VE F68 VE DİPTE) ve t <= L2 + 20
    ek("S10", "U1 = S10 VE F68 VE DİPTE", "tanım", True, bool(Y["S10"] == 1.0 and Y["F68"] == 1.0 and Y["dipte"]))
    ek("t", "t - L2 <= 20", "tanım", True, bool(Y["tL2"] <= float(MU.MU_ESIK["olay"]["taze_azami"])))
    bozuk = [k for k in K if not k["tamam"]]
    return {"kontrol": K, "n": len(K), "bozuk": bozuk, "tamam": not bozuk}


# ================================================================ 3) ÇİZİM (A4 dikey; telefonda okunur)
def _o20_plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42, "axes.unicode_minus": True})
    return plt


def _o20_etiket_x(x1: float, x2: float) -> Tuple[float, float]:
    """'1. dip' / '2. dip' etiketleri üst üste binmesin: merkezler arası en az O20_ESIK['etiket_ara'] bar."""
    d = x2 - x1; ara = float(O20_ESIK["etiket_ara"])
    if d >= ara:
        return x1, x2
    k = (ara - d) / 2.0
    return x1 - k, x2 + k


def o20_sayfa_ciz(cz: Dict[str, Any], Y: Dict[str, Any], no: int, toplam: int, pazar: str):
    plt = _o20_plt()
    R = O20_RENK
    W, Hs = O20_ESIK["sayfa_boyut"]
    fig = plt.figure(figsize=(W, Hs))
    axp = fig.add_axes([0.06, 0.515, 0.90, 0.405])
    axm = fig.add_axes([0.06, 0.345, 0.90, 0.160], sharex=axp)
    axr = fig.add_axes([0.06, 0.283, 0.90, 0.054], sharex=axp)
    O, H, L, C = cz["O"], cz["H"], cz["L"], cz["C"]
    n = len(L) - 1; x = np.arange(n + 1) - n                     # t = 0 (son bar); bar sırası ardışık, boşluk yok
    i1, i2 = int(Y["i1"]), int(Y["i2"]); x1, x2 = i1 - n, i2 - n
    l1, l2 = float(L[i1]), float(L[i2]); st = float(Y["stop0"]); tp = float(Y["tepe120"])
    alt = min(float(L.min()), st); ust = float(H.max()); pad = (ust - alt) * 0.05
    sag = 7.5
    # --- fiyat paneli: mumlar
    renk = np.where(C >= O, R["yukari"], R["asagi"])
    axp.vlines(x, L, H, colors=renk, linewidth=1.0, zorder=3)
    govde = np.maximum(np.abs(C - O), (ust - alt) * 0.0015)
    axp.bar(x, govde, bottom=np.minimum(O, C), width=0.66, color=renk, edgecolor=renk, linewidth=0.3, zorder=4)
    # 120 bar tepesi: [L2 - 120, L2]
    g = int(MU.MU_ESIK["dipte"]["geri"]); xa = x2 - g
    axp.plot([xa, x2], [tp, tp], color=R["tepe"], linewidth=1.0, linestyle=(0, (4, 3)), zorder=2)
    axp.text(xa + 0.5, tp + pad * 0.18, "120 bar tepesi", color="#555555", fontsize=11, ha="left", va="bottom", zorder=9,
             bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    # stop: Low(L2) x 0,98, L2'den t'ye
    axp.plot([x2, 0], [st, st], color=R["stop"], linewidth=1.8, linestyle=(0, (6, 3)), zorder=5)
    axp.text(0.9, st, "stop", color=R["stop"], fontsize=12.5, fontweight="bold", ha="left", va="center", zorder=9)
    # iki dip: Low noktasında daire + mavi çizgi
    axp.plot([x1, x2], [l1, l2], color=R["mavi"], linewidth=2.6, zorder=6, solid_capstyle="round")
    axp.plot([x1, x2], [l1, l2], linestyle="none", marker="o", markersize=15, markerfacecolor="none", markeredgecolor=R["mavi"],
             markeredgewidth=2.2, zorder=7)
    tx1, tx2 = _o20_etiket_x(x1, x2); ye = alt - pad * 1.05
    for tx, xx, yy, s in ((tx1, x1, l1, "1. dip"), (tx2, x2, l2, "2. dip")):
        axp.annotate(s, xy=(xx, yy), xytext=(tx, ye), ha="center", va="top", fontsize=13, fontweight="bold", color=R["mavi"], zorder=9,
                     arrowprops=dict(arrowstyle="-", color=R["mavi"], lw=1.0, shrinkA=1, shrinkB=8),
                     bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))
    # sinyal günü (t): ince dikey noktalı çizgi
    for ax in (axp, axm, axr):
        ax.axvline(0, color=R["sinyal_gunu"], linewidth=0.9, linestyle=(0, (1, 2.5)), zorder=1)
    axp.set_ylim(alt - pad * 3.3, ust + pad * 1.9)
    axp.text(-0.7, ust + pad * 1.75, "sinyal günü", ha="right", va="top", fontsize=12, color="#222222", zorder=10,
             bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))
    # --- MACD paneli (t günündeki pencere [t-250, t])
    m, s, h = cz["macd"], cz["sinyal"], cz["hist"]
    ok = np.isfinite(h)
    axm.bar(x[ok], h[ok], width=0.7, color=R["hist"], zorder=2)
    axm.axhline(0.0, color="#333333", linewidth=0.9, zorder=3)
    axm.plot(x, s, color=R["sinyal"], linewidth=1.3, zorder=4)
    axm.plot(x, m, color=R["macd"], linewidth=1.6, zorder=5)
    m1, m2 = float(m[i1]), float(m[i2])
    axm.plot([x1, x2], [m1, m2], color=R["mavi"], linewidth=2.4, zorder=6, solid_capstyle="round")
    axm.plot([x1, x2], [m1, m2], linestyle="none", marker="o", markersize=12, markerfacecolor="none", markeredgecolor=R["mavi"],
             markeredgewidth=2.0, zorder=7)
    yv = np.concatenate([m[np.isfinite(m)], s[np.isfinite(s)], h[ok], [0.0]])
    ma, mu = float(yv.min()), float(yv.max()); mp = (mu - ma) * 0.08 if mu > ma else 1.0
    yme = ma - mp * 1.45    # etiket kutusu dairenin altından başlar (daire yarıçapı ~1 mp); daireyi örtmez
    for tx, xx, yy, s_ in ((tx1, x1, m1, "1. dip"), (tx2, x2, m2, "2. dip")):
        axm.annotate(s_, xy=(xx, yy), xytext=(tx, yme), ha="center", va="top", fontsize=10.5, fontweight="bold", color=R["mavi"], zorder=9,
                     arrowprops=dict(arrowstyle="-", color=R["mavi"], lw=0.9, shrinkA=1, shrinkB=6),
                     bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))
    axm.set_ylim(ma - mp * 3.9, mu + mp * 2.2)
    axm.text(x[0] + 0.5, mu + mp * 2.0, "MACD (12, 26, 9) siyah · sinyal kırmızı · histogram gri", fontsize=9.5, ha="left", va="top",
             color="#333333", zorder=10, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    axm.text(sag - 0.3, 0.0, "0", fontsize=10.5, ha="right", va="center", color="#333333")
    # --- RSI paneli (bilgi)
    axr.plot(x, cz["rsi"], color=R["rsi"], linewidth=1.2, zorder=4)
    for v in (30.0, 70.0):
        axr.axhline(v, color="#8a8a8a", linewidth=0.8, linestyle=(0, (3, 3)), zorder=2)
        axr.text(sag - 0.3, v, f"{int(v)}", fontsize=9, ha="right", va="center", color="#555555")
    axr.set_ylim(0, 100)
    axr.text(x[0] + 0.5, 96, "RSI 14 (bilgi)", fontsize=9, ha="left", va="top", color="#333333", zorder=10,
             bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    for ax in (axp, axm, axr):
        ax.set_xlim(x[0] - 1.0, sag)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_linewidth(0.6); sp.set_color("#999999")
    # --- başlık
    fig.text(0.05, 0.958, f"{int(no)}", fontsize=44, fontweight="bold", ha="left", va="center")
    fig.text(0.50, 0.958, pazar, fontsize=26, fontweight="bold", ha="center", va="center")
    fig.text(0.95, 0.958, f"/ {int(toplam)}", fontsize=16, color="#666666", ha="right", va="center")
    # --- kodun sayıları (hüküm yok)
    satirlar = [
        (f"2. dip / 1. dip: {_o20_yuzde(Y['F65'])}", "kural: en çok %+1"),
        (f"MACD 1. dipte {_o20_sayi(Y['m1'])}  ·  2. dipte {_o20_sayi(Y['m2'])}", "kural: 2. dipte yukarıda ve < 0"),
        (f"120 bar tepesinden düşüş: {_o20_yuzde(Y['dusus120'], 1, False)}", "2. dip kapanışıyla · kural: en az %20"),
        (f"2. dip / önceki 120 barın en düşüğü: {_o20_yuzde(Y['dip120_oran'])}", "kural: en çok %+1"),
        (f"2. dipten sinyal gününe: {int(Y['tL2'])} bar", "kural: en geç 20 bar"),
    ]
    y0, dy = 0.248, 0.0285
    for k, (a_, b_) in enumerate(satirlar):
        fig.text(0.07, y0 - k * dy, a_, fontsize=14, ha="left", va="center", color="#111111")
        fig.text(0.95, y0 - k * dy, b_, fontsize=10, ha="right", va="center", color=R["ipucu"])
    fig.text(0.50, 0.085, "☐ DOĞRU            ☐ YANLIŞ", fontsize=22, ha="center", va="center")
    fig.text(0.50, 0.052, "Yanlışsa okla göster: fiyat dipleri · MACD dipleri · dipte değil · sinyal günü", fontsize=10.5, ha="center",
             va="center", color="#444444")
    fig.text(0.07, 0.022, "Not: " + "_" * 58, fontsize=13, ha="left", va="center", color="#333333")
    return fig


def o20_kapak(anahtar_sha: str, J: Dict[str, Any], toplam: int):
    plt = _o20_plt()
    W, Hs = O20_ESIK["sayfa_boyut"]
    fig = plt.figure(figsize=(W, Hs))
    fig.text(0.5, 0.945, "MACD POZİTİF UYUMSUZLUK —", fontsize=22, fontweight="bold", ha="center", va="center")
    fig.text(0.5, 0.912, f"kodun gözü ({toplam} rastgele olay)", fontsize=22, fontweight="bold", ha="center", va="center")
    tanim = ("Kodun tanımı (düz dille):\n"
             "  1. Fiyatın ikinci dibi birinciyle aynı ya da daha derin\n"
             "      (en çok %1 yukarı).\n"
             "  2. MACD ikinci dipte birinciden yukarıda ve sıfırın altında.\n"
             "  3. İkinci dip 120 barın dibi ve 120 bar tepesinden\n"
             "      en az %20 aşağıda.\n"
             "  4. Sinyal günü: MACD sinyal çizgisinin üstünde; ikinci dipten\n"
             "      en geç 20 bar sonra.")
    fig.text(0.07, 0.875, tanim, fontsize=13.5, ha="left", va="top", linespacing=1.45)
    ayr = ("Kodun dibi: solundaki 5 mumdan alçak, sağındaki 5 mumdan alçak ya da eşit en düşük (Low), son 60 bar içinde; "
           "1. dip 2. dipten en az 8 bar önce. 2. dip sağdaki 5 mumla onaylandığı için sinyal günü en erken 6 bar sonra; "
           "sinyal günü şartların İLK tuttuğu gün. MACD kapanıştan, sinyal gününden geriye 250 barla hesaplanır (o günkü görüş; "
           "sayfadaki MACD çizgisi de bu). 120 bar tepesinden düşüş 2. dibin kapanışıyla ölçülür.")
    fig.text(0.07, 0.645, "\n".join(textwrap.wrap(ayr, 84)), fontsize=11, ha="left", va="top", linespacing=1.4, color="#333333")
    secim = (f"Seçim: {int(J['evren_n']):,}".replace(",", ".") + f" olaydan tohumla tamamen rastgele {toplam}; sayfa sırası rastgele "
             f"(tohum {int(J['tohum'])}; seçim çizimden önce kaydedildi).")
    fig.text(0.07, 0.525, "\n".join(textwrap.wrap(secim, 70)), fontsize=12.5, ha="left", va="top", linespacing=1.4)
    kor = ("Sayfalarda hisse adı, tarih ve sinyalden sonrası yok.\n"
           "Sonuçlar ayrı anahtarda: uyum_ornek20_anahtar.json")
    fig.text(0.07, 0.468, kor, fontsize=12.5, ha="left", va="top", linespacing=1.4)
    fig.text(0.07, 0.421, "anahtar sha256:", fontsize=11, ha="left", va="top", color="#333333")
    fig.text(0.07, 0.401, anahtar_sha, fontsize=9.6, ha="left", va="top", family="DejaVu Sans Mono", color="#111111")
    isaret = ("İşaret: her sayfada  ✓ DOĞRU (bu bir uyumsuzluk)\n"
              "ya da  ✗ YANLIŞ.\n"
              "Yanlışsa okla hangi parça olduğunu göster:\n"
              "fiyat dipleri / MACD dipleri / dipte değil / sinyal günü.")
    fig.text(0.07, 0.36, isaret, fontsize=13.5, ha="left", va="top", linespacing=1.5, fontweight="bold")
    ciz = ("Çizimler: daire = kodun seçtiği dip (fiyatta mumun en düşük noktası, MACD'de çizginin üstü); mavi çizgi iki dibi "
           "birleştirir. Kırmızı kesik = stop (2. dibin en düşüğü x 0,98; 2. dipten sinyal gününe). Gri kesik = 120 bar tepesi "
           "(2. dipten geriye 120 bar). Noktalı dikey = sinyal günü (son mum). Orta panel: MACD siyah, sinyal kırmızı, histogram gri, "
           "yatay çizgi sıfır. Alt panel: RSI 14 (30 / 70 çizgili), yalnız bilgi; kodun tanımında yok. Sayfanın altında kodun "
           "sayıları; sağda gri yazı kodun kuralı. Mumlar yalnız geçerli günler (sıfır hacimli / H = L günler yok), aralıksız.")
    fig.text(0.07, 0.225, "\n".join(textwrap.wrap(ciz, 84)), fontsize=11, ha="left", va="top", linespacing=1.4, color="#333333")
    fig.text(0.5, 0.035, "Sayfada hüküm yok: yalnız kodun gördüğü çizildi ve yazıldı.", fontsize=10.5, ha="center", va="center",
             color="#555555")
    return fig


# ================================================================ 4) ANAHTAR (mühürlü; PDF'e girmez)
def o20_anahtar_metin(J: Dict[str, Any], sat: pd.DataFrame) -> str:
    sayfalar = []
    for s, (_, r) in zip(J["secim"], sat.iterrows()):
        z = {"sayfa": int(s["sayfa"]), "pazar": str(r["pazar"]), "sembol": str(r["sembol"]), "tarih": str(r["tarih"]),
             "L1_tarih": str(r["L1_tarih"]), "L2_tarih": str(r["L2_tarih"]), "giris": str(r["giris"]), "E0": _o20_f(r["E0"]),
             "stop": _o20_f(r["stop0"]), "h5": _o20_f(r["h5"]), "h10": _o20_f(r["h10"]), "stop_oldu": _o20_f(r["stop_oldu"]),
             "r15": _o20_f(r["r15"]), "es_r15": _o20_f(r["es_r15"]), "fark": _o20_f(r["fark"])}
        if list(z) != O20_ANAHTAR_ALAN:
            raise O20Hata("anahtar alanları iş tanımından farklı")
        sayfalar.append(z)
    A = {"surum": O20_SURUM,
         "uyari": "GİZLİ ANAHTAR: Cemal UYUM_ORNEK20.pdf sayfalarını işaretlemeden açılmaz. Sonuç alanları (h5, h10, stop_oldu, r15, es_r15, "
                  "fark) satır dosyasından AYNEN kopyalandı; bu dosya PDF'e girmez, sha256'sı PDF kapağında yazılıdır.",
         "pdf": _o20_rel(O20_YOL["pdf"]),
         "secim": {"dosya": _o20_rel(O20_YOL["secim"]), "sha256": J["secim_sha256"], "tohum": int(J["tohum"]), "evren_n": int(J["evren_n"]),
                   "zaman_utc": J.get("zaman_utc")},
         "satir": {"dosya": _o20_rel(O20_YOL["satir"]), "sha256": J["satir_sha256"], "hipotez": O20_ESIK["hipotez"]},
         "alan": {"tarih": "sinyal günü t", "L1_tarih": "1. dip", "L2_tarih": "2. dip", "giris": "t'den sonraki ilk geçerli bar (giriş günü)",
                  "E0": "giriş açılışı", "stop": "stop0 = Low(L2) x 0,98",
                  "h5": "15 geçerli barda kapanış +%5 stop'tan önce (1 / 0; YAPI_HEDEF 1. tur cetveli)", "h10": "aynı, +%10",
                  "stop_oldu": "stop (giriş stop altıysa 1)", "r15": "t+1 açılış -> 15. geçerli bar kapanışı - 1 (CETVEL2 v2.2 R15, stop'suz)",
                  "es_r15": "aynı gün eşlerinin r15 ortalaması (konum eşi)", "fark": "r15 - es_r15"},
         "sayfalar": sayfalar}
    return json.dumps(A, ensure_ascii=False, indent=1, allow_nan=False) + "\n"


def o20_anahtar_yaz(metin: str, uzerine: bool = False) -> str:
    """Anahtar belirlenimci: varsa ve aynıysa dokunulmaz; farklıysa DURUR (--uzerine verilmedikçe). sha256 döner."""
    yol = O20_YOL["anahtar"]
    yeni = metin.encode("utf-8")
    if os.path.exists(yol):
        eski = open(yol, "rb").read()
        if eski == yeni:
            o20log.info("anahtar zaten var ve aynı (sha %s…)", hashlib.sha256(yeni).hexdigest()[:16])
            return _o20_sha(yol)
        if not uzerine:
            raise O20Hata(f"anahtar var ve içerik farklı: {_o20_rel(yol)} (mühür bozulmasın; --uzerine yalnız bilerek)")
    YH._yh_yaz(yol, metin, "O20 anahtar")
    if _o20_sha(yol) != hashlib.sha256(yeni).hexdigest():
        raise O20Hata("anahtar diske beklenen baytlarla yazılmadı")
    return _o20_sha(yol)


# ================================================================ 5) AKIŞ
def o20_hazirla(veri: Optional[str] = None) -> Dict[str, Any]:
    """Girdiler + kapı + 20 sayfanın görüşü, çizim verisi ve yeniden hesap denetimi. Biri tutmazsa O20Hata (DUR)."""
    v = veri or O20_YOL["veri"]
    J = o20_secim()
    G = o20_kapi(v)
    sat = o20_satir(J)
    olay = o20_olay(J)
    Vd: Dict[str, Dict[str, Any]] = {}
    sayfa = []
    for s, (_, r), ol in zip(J["secim"], sat.iterrows(), olay):
        p = s["pazar"]
        if p not in Vd:
            Vd[p] = MU.C2.c2_veri(p, v)
        g = o20_gorus(Vd[p], s["sembol"], s["tarih"])
        cz = o20_cizim(g)
        Y = o20_yeniden(cz)
        D = o20_karsilastir(Y, cz, g, r, ol)
        sayfa.append({"no": int(s["sayfa"]), "pazar": p, "cz": cz, "Y": Y, "D": D})
        o20log.info("sayfa %d (%s): %d / %d kontrol tuttu", int(s["sayfa"]), p, D["n"] - len(D["bozuk"]), D["n"])
    bozuk = [(x["no"], k["kaynak"], k["ad"]) for x in sayfa for k in x["D"]["bozuk"]]
    if bozuk:
        raise O20Hata(f"çizimden yeniden hesap kodla aynı DEĞİL ({len(bozuk)} kontrol): {bozuk[:8]} -> DURDU (PDF / anahtar yazılmadı)")
    return {"J": J, "G": G, "sat": sat, "sayfa": sayfa}


def o20_tablo(S: List[Dict[str, Any]]) -> str:
    """Denetim tablosu (sonuç değeri yok): grup başına bütün kaynaklarda tuttu mu."""
    gruplar = ["L1", "L2", "MACD(L1)", "MACD(L2)", "F65", "F66", "F68", "DİPTE", "S10"]
    L = ["| sayfa | pazar | " + " | ".join(gruplar) + " | yh_s10_bar 10 çıktı | t'de kesik mu_hisse | olay dosyası | kontrol |",
         "|---|---|" + "---|" * (len(gruplar) + 4)]
    for x in S:
        K = x["D"]["kontrol"]

        def isr(f) -> str:
            k = [c for c in K if f(c)]
            return ("✓" if all(c["tamam"] for c in k) else "✗") if k else "-"
        hucre = [isr(lambda c, g=g: c["grup"] == g) for g in gruplar]
        yh = [c for c in K if c["kaynak"] == "yh_s10_bar" and c["ad"] in YH._YH_S10_OZ]
        L.append(f"| {x['no']} | {x['pazar']} | " + " | ".join(hucre) + f" | {sum(c['tamam'] for c in yh)} / {len(yh)} | "
                 f"{isr(lambda c: c['kaynak'] == O20_KESIK)} | {isr(lambda c: c['kaynak'] == 'olay dosyası')} | "
                 f"{x['D']['n'] - len(x['D']['bozuk'])} / {x['D']['n']} |")
    return "\n".join(L)


def o20_ciz(veri: Optional[str] = None, uzerine: bool = False) -> Dict[str, Any]:
    from matplotlib.backends.backend_pdf import PdfPages
    plt = _o20_plt()
    Hz = o20_hazirla(veri)
    J, S = Hz["J"], Hz["sayfa"]
    toplam = len(S)
    sha = o20_anahtar_yaz(o20_anahtar_metin(J, Hz["sat"]), uzerine)
    yol = O20_YOL["pdf"]; gecici = yol + ".gecici"
    meta = {"Title": "MACD pozitif uyumsuzluk - kodun gozu (20 rastgele olay)", "Author": "ornek20_ciz", "Creator": "ornek20_ciz",
            "Producer": "ornek20_ciz", "CreationDate": None, "ModDate": None}
    with PdfPages(gecici, metadata=meta) as pdf:
        fig = o20_kapak(sha, J, toplam); pdf.savefig(fig); plt.close(fig)
        for x in S:
            fig = o20_sayfa_ciz(x["cz"], x["Y"], x["no"], toplam, x["pazar"]); pdf.savefig(fig); plt.close(fig)
    os.replace(gecici, yol)
    boy = os.path.getsize(yol)
    if boy > int(O20_ESIK["pdf_azami"]):
        raise O20Hata(f"PDF çok büyük: {boy} bayt")
    if boy > int(O20_ESIK["pdf_tercih"]):
        o20log.warning("PDF 3 MB'tan büyük: %d bayt", boy)
    return {"pdf": _o20_rel(yol), "pdf_bayt": boy, "pdf_sha256": _o20_sha(yol), "sayfa": toplam + 1, "anahtar": _o20_rel(O20_YOL["anahtar"]),
            "anahtar_sha256": sha, "tablo": o20_tablo(S), "kasa": Hz["G"]["kasa"]["kesik"]}


# ================================================================ 6) ÇAKIŞMA KAPISI
def _cakisma_kontrol_o20(_once=_CK_ONCE_O20, _dosya="ornek20_ciz.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur (Colab exec)."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_O20", "_CK_KAYIT", "_cakisma_kontrol_o20", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "hashlib", "argparse", "textwrap", "annotations", "Any", "Dict", "List",
           "Optional", "Tuple", "MU", "YH")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_o20()


def _o20_ana(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=O20_SURUM)
    ap.add_argument("komut", nargs="?", default="ciz", choices=["ciz", "denetim"])
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine", action="store_true", help="anahtar farklıysa üzerine yaz (mühürden sonra KULLANMA)")
    a = ap.parse_args(argv)
    try:
        if a.komut == "denetim":
            Hz = o20_hazirla(a.veri)
            print(o20_tablo(Hz["sayfa"]))
            print(f"\nDENETİM: {len(Hz['sayfa'])} / {len(Hz['sayfa'])} sayfa tuttu")
        else:
            R = o20_ciz(a.veri, a.uzerine)
            print(R["tablo"])
            print(f"\nPDF: {R['pdf']} ({R['sayfa']} sayfa, {R['pdf_bayt']} bayt, sha256 {R['pdf_sha256']})")
            print(f"ANAHTAR: {R['anahtar']} (sha256 {R['anahtar_sha256']}; kapakta yazılı)")
    except (O20Hata, MU.MUHata) as ex:
        o20log.error("%s", ex)
        print(f"DURDU: {ex}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__" and "get_ipython" not in globals():
    sys.exit(_o20_ana())
