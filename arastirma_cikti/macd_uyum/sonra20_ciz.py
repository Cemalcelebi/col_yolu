"""sonra20_ciz — MACD_UYUM U1b (bariz uyumsuzluk) 20 rastgele olayın SONUÇLU görsel seti: kodun t günündeki görüşü + sinyalden sonraki 20
mum (24 Kasım 2026; iş tanımı: ana model mesajı).

Cemal (24 Kas 2026): "tutmadı dediğin rastgele tam uyumsuzluğu göreyim; bu bölgeyle bırakma, sonrasındaki 20 mumu da göster, ne yapmış".
Bu set KÖR DEĞİL: hisse adı, tarih ve sonuç görünür. Betik ÖLÇMEZ ve HÜKÜM VERMEZ; kodun t'deki görüşünü ve sonrasını çizer, satır dosyasının
sonuç alanlarını yazar.

SEÇİM: uyum_b_sonra20_secim.json (tohum 2936415393): uyum_satir.csv.gz U1 satırlarından F65 <= -0,05 (U1b, Ç219) VE t <= 2022-11-25 olan
  2.337 olaydan 20; sayfa sırası dosyadaki 'sayfa'. Seçim DEĞİŞTİRİLMEZ; satır sha'sı seçimdekiyle aynı olmalı, evren satır dosyasından yeniden
  sayılır (2.337; U1b toplamı 2.348 = uyum_b_sonuc.json) ve 20 olay bu evrende olmalı (değilse DURUR).
KODUN GÖRÜŞÜ (t'ye kadar; ornek20_ciz.py fonksiyonları AYNEN çağrılır): o20_kapi (KASA kapısı + V_*.pkl sha), o20_olay, o20_gorus (veri t'de
  kesilir, mu_hisse U1 olayı, yh_s10_bar, MACD [t-250, t], RSI), o20_cizim (max(seri başı, L2 - 125) .. t), o20_yeniden + o20_karsilastir
  (çizimden L1 / L2 / MACD(L1) / MACD(L2) / F65 / F66 / F68 / DİPTE = satır dosyası / yh_s10_bar / kesik seride mu_hisse / olay dosyası).
SONRASI 20 MUM (K2): aynı hissenin geçerli barları (CETVEL2 panelinin Vd'si = ds_veri, YH._yh_hazir), t'den sonraki ilk 20. Tam serinin t'ye
  kadarki barları kesik seriyle BİREBİR olmalı; 20. mum KASA açık kesiğini (2022-12-31) aşarsa DURUR. MACD aynı pencere başından (t-250) t+20'ye
  aynı hesap (YH.yh_macd); RSI aynı nedensel seri (MU._mu_rsi). İkisinin t'ye kadarki değerleri kodun görüşüyle BİREBİR (değilse DURUR).
SONUÇ (sayfadaki sayılar satır dosyasından AYNEN; iki yoldan yeniden hesap, %.15g yazımıyla birebir; biri tutmazsa DURUR, PDF / tablo yazılmaz):
  çizimden: E0 = t+1 açılışı, r15 = t+15 kapanışı / E0 - 1, h5 / h10 / stop_oldu = YAPI_HEDEF 1. tur 15 bar kuralı (bağımsız döngü s20_sim ve
            YH.yh_sim), mum sıraları (giriş mumu t+1 = 1. mum), 20 mumda en yüksek / en düşük kapanış;
  CETVEL2 panelinden (c2_panel22_al ufuk 15): E0 = P['Op'][d, j], r15 = R15[d, j], es_r15 / n_es / sira / fark = C2.c2_es (dışlama kümesi:
            pazarın satır dosyasındaki bütün U1 olayları; c2_olc ile aynı), h5 / h10 / st5 = YH.yh_sim panel penceresi (30 satır birleşik takvim).
  Ölçümün stopu (YH_ESIK['olcu']['stop']): başta stop0 = Low(L2) x 0,98; her mumun sonunda stop = max(stop, en yüksek kapanış x 0,93, giriş x 1,02
  [+%5 görüldüyse], giriş x 1,07 [+%10 görüldüyse]); kapanış o günkü stopun altındaysa STOP. Sayfada sabit stop (kesik) ve ölçümün o günkü stopu
  (noktalı basamak, karar mumuna kadar) ayrı çizilir.
ÇIKTI: UYUM_B_SONRA20.pdf (kapak + 20 sayfa) ve uyum_b_sonra20_tablo.json (sayfa başına kontrol sayıları; belirlenimci, zaman damgası yok).
  Dosya varsa ve içerik farklıysa DURUR (--uzerine verilmedikçe).

Komut (repo kökünden):
  python arastirma_cikti/macd_uyum/sonra20_ciz.py ciz [--uzerine]   denetim -> UYUM_B_SONRA20.pdf + uyum_b_sonra20_tablo.json + tablo
  python arastirma_cikti/macd_uyum/sonra20_ciz.py denetim           yalnız yeniden hesap tablosu (dosya yazmaz)
Veri: /tmp/kasa/acik (V_ABD.pkl, V_AVR.pkl, V_BIST.pkl; KASA açık kesik 2022-12-31). Ortam: S20_VERI.
MACD_UYUM.py, YAPI_HEDEF.py, CETVEL2.py, ornek20_ciz.py, seçim ve satır dosyaları DEĞİŞTİRİLMEZ; yalnız okunur. Colab: kod değiştiyse çalışma
zamanını yeniden başlat.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_S20 = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import textwrap  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

S20_DIR = (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals()
           else os.path.join(os.getcwd(), "arastirma_cikti", "macd_uyum"))
S20_KOK = os.path.dirname(os.path.dirname(S20_DIR))
if S20_KOK not in sys.path:
    sys.path.insert(0, S20_KOK)
if S20_DIR not in sys.path:
    sys.path.insert(0, S20_DIR)

import ornek20_ciz as O20  # noqa: E402  (yalnız okunur: o20_kapi, o20_olay, o20_gorus, o20_cizim, o20_yeniden, o20_karsilastir, çizim yardımcıları)

MU = O20.MU   # MACD_UYUM (yalnız okunur)
YH = O20.YH   # YAPI_HEDEF (yalnız okunur: YH_ESIK, yh_sim, _yh_pencere, yh_macd, _yh_hazir, _yh_yaz)
C2 = MU.C2    # CETVEL2 (yalnız okunur: c2_panel22_al, c2_es)

s20log = logging.getLogger("col.sonra20")
if not s20log.handlers:
    _s20_h = logging.StreamHandler(sys.stderr)
    _s20_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sonra20: %(message)s", "%H:%M:%S"))
    s20log.addHandler(_s20_h)
    s20log.setLevel(logging.INFO)
    s20log.propagate = False

S20_SURUM = "sonra20_ciz v1 (2026-11-24): MACD_UYUM U1b (F65 <= -%5) sonuçlu görsel set, 20 rastgele olay + sinyalden sonraki 20 mum"
S20_YOL: Dict[str, str] = {
    "secim": os.path.join(S20_DIR, "uyum_b_sonra20_secim.json"),
    "satir": os.path.join(S20_DIR, "uyum_satir.csv.gz"),
    "b_sonuc": os.path.join(S20_DIR, "uyum_b_sonuc.json"),
    "tablo": os.path.join(S20_DIR, "uyum_b_sonra20_tablo.json"),
    "pdf": os.path.join(S20_DIR, "UYUM_B_SONRA20.pdf"),
    "veri": os.environ.get("S20_VERI", "/tmp/kasa/acik"),
}
S20_ESIK: Dict[str, Any] = {
    "hipotez": "U1", "F65_ust": -0.05, "t_son": "2022-11-25", "sayfa_n": 20, "evren_n": 2337, "tohum": 2936415393,
    "olcum_n": 2348, "olcum_karar": "TUTMADI",   # Ç219 U1b ölçümü (uyum_b_sonuc.json; kapaktaki uyarı cümlesi bundan)
    "sonra": 20,                   # sinyalden sonra çizilen mum
    "oncesi": 125,                 # fiyat paneli max(seri başı, L2 - 125) .. t + 20 (ornek20 ile aynı)
    "fark_kimlik_tol": 1e-13,      # satır içi fark = r15 - es_r15 (üç değer ayrı ayrı %.15g yazıldı)
    "pdf_tercih": 3 * 1024 * 1024, "pdf_azami": 8 * 1024 * 1024,
    "sayfa_boyut": (8.27, 11.69),  # A4 dikey (inç)
    "sag_bos": 10.0,               # t+20'den sonra sağ kenar etiket alanı (bar)
    "etiket_ara_pt": 12.0,         # sağ kenar etiketleri arası en az dikey uzaklık (punto)
}
S20_RENK: Dict[str, str] = {**O20.O20_RENK, "golge": "#e4e4e4", "hedef5": "#2ca02c", "hedef10": "#0a5c26", "giris": "#22a03c",
                            "giris_kenar": "#0b4f1c", "takip": "#d62728", "ufuk": "#3a3a3a", "yildiz": "#22a03c", "yildiz_kenar": "#0b4f1c",
                            "carpi": "#d62728", "carpi_kenar": "#6b0000", "kutu": "#f6f6f6", "kutu_kenar": "#b8b8b8", "uyari": "#8b0000"}
S20_GRUP = ["L1", "L2", "MACD(L1)", "MACD(L2)", "F65", "F66", "F68", "DİPTE", "S10", "giriş", "r15", "eş", "fark", "h5", "h10", "stop",
            "uzatma", "KASA"]


class S20Hata(RuntimeError):
    """Durdurucu hata: seçim / satır / veri / KASA tutmuyor ya da çizimden / panelden yeniden hesap satır dosyasından farklı (DUR; dosya yazılmaz)."""


# ================================================================ 0) ORTAK
def _s20_sha(yol: str) -> str:
    return O20._o20_sha(yol)


def _s20_rel(yol: str) -> str:
    return os.path.relpath(yol, S20_KOK)


def _s20_f(x: Any) -> Optional[float]:
    """JSON için sayı: sonlu değilse None (satır dosyasındaki boş hücre)."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if np.isfinite(v) else None


def _s20_15g(bulunan: Any, satir: Any) -> bool:
    """Satır dosyası %.15g ile yazıldı: yeniden hesaplanan değer aynı biçimle yazılınca satırdakiyle AYNI metin mi (ikisi de NaN ise tutar)."""
    try:
        b, s = float(bulunan), float(satir)
    except (TypeError, ValueError):
        return False
    if not np.isfinite(s):
        return not np.isfinite(b)
    if not np.isfinite(b):
        return False
    return f"{b:.15g}" == f"{s:.15g}"


def _s20_bayrak(bulunan: Any, satir: Any) -> bool:
    """0 / 1 bayrak (ya da NaN) birebir."""
    try:
        b, s = float(bulunan), float(satir)
    except (TypeError, ValueError):
        return False
    if not np.isfinite(s):
        return not np.isfinite(b)
    return bool(np.isfinite(b) and b == s)


def _s20_tarih(t: Any) -> str:
    return pd.Timestamp(t).strftime("%d.%m.%Y")


def _s20_yz(x: Any, n: int = 2) -> str:
    v = _s20_f(x)
    return "-" if v is None else O20._o20_yuzde(v, n)


def _s20_puan(x: Any, n: int = 2) -> str:
    v = _s20_f(x)
    return "-" if v is None else (f"{100.0 * v:+.{n}f}".replace(".", ",") + " puan")


def _s20_mum(k: int) -> Optional[int]:
    """Bar sırası (0 = giriş mumu) -> mum numarası (giriş mumu t+1 = 1. mum); yoksa None."""
    return int(k) + 1 if int(k) >= 0 else None


# ================================================================ 1) GİRDİLER (seçim, satır, ölçüm sonucu)
def s20_secim() -> Dict[str, Any]:
    """Seçim dosyası (DEĞİŞMEZ): 20 sayfa, tohum / evren iş tanımıyla; satır sha'sı aynı; evren satır dosyasından yeniden sayılır."""
    try:
        J = json.load(open(S20_YOL["secim"], encoding="utf-8"))
    except (OSError, ValueError) as ex:
        raise S20Hata(f"seçim dosyası okunamadı: {ex}") from ex
    S = sorted(J.get("secim", []), key=lambda s: int(s["sayfa"]))
    n = int(S20_ESIK["sayfa_n"])
    if [int(s["sayfa"]) for s in S] != list(range(1, n + 1)):
        raise S20Hata(f"seçim sayfaları 1..{n} değil")
    if int(J["tohum"]) != int(S20_ESIK["tohum"]) or int(J["evren_n"]) != int(S20_ESIK["evren_n"]):
        raise S20Hata(f"seçim tohumu / evren sayısı iş tanımından farklı: {J['tohum']} / {J['evren_n']}")
    if len({(s["pazar"], s["sembol"], s["tarih"]) for s in S}) != len(S):
        raise S20Hata("seçimde tekrar eden olay var")
    sha = _s20_sha(S20_YOL["satir"])
    if sha != J["satir_sha256"]:
        raise S20Hata(f"satır dosyası seçimdeki sha ile aynı değil: {sha} != {J['satir_sha256']}")
    X = pd.read_csv(S20_YOL["satir"], dtype={"tarih": str, "giris": str, "L1_tarih": str, "L2_tarih": str, "sembol": str, "donem": str},
                    float_precision="round_trip")
    U = X[X.hipotez == S20_ESIK["hipotez"]].copy()
    B = U[U.F65 <= float(S20_ESIK["F65_ust"])]
    E = B[B.tarih <= str(S20_ESIK["t_son"])]
    if len(B) != int(S20_ESIK["olcum_n"]):
        raise S20Hata(f"U1b (F65 <= -0,05) olay sayısı {len(B)} (iş tanımında {S20_ESIK['olcum_n']})")
    if len(E) != int(J["evren_n"]):
        raise S20Hata(f"seçim evreni satır dosyasından {len(E)} sayıldı (seçimde {J['evren_n']})")
    ev = set(zip(E.pazar, E.sembol, E.tarih))
    dis = [s["sayfa"] for s in S if (s["pazar"], s["sembol"], s["tarih"]) not in ev]
    if dis:
        raise S20Hata(f"seçilen olaylar evrende değil (sayfa {dis})")
    return {**J, "secim": S, "secim_sha256": _s20_sha(S20_YOL["secim"]), "satir_sha256": sha, "U": U, "olcum_n_say": int(len(B)),
            "evren_n_say": int(len(E))}


def s20_b_sonuc() -> Dict[str, Any]:
    """Ç219 ölçüm sonucu (kapaktaki uyarı cümlesinin kaynağı): U1b n ve karar iş tanımıyla aynı olmalı."""
    try:
        B = json.load(open(S20_YOL["b_sonuc"], encoding="utf-8"))
    except (OSError, ValueError) as ex:
        raise S20Hata(f"uyum_b_sonuc.json okunamadı: {ex}") from ex
    n = int(B.get("n", {}).get("U1b", -1)); k = str(B.get("karar"))
    if n != int(S20_ESIK["olcum_n"]) or k != str(S20_ESIK["olcum_karar"]):
        raise S20Hata(f"uyum_b_sonuc.json U1b n {n} / karar {k}: iş tanımındaki {S20_ESIK['olcum_n']} / {S20_ESIK['olcum_karar']} değil")
    return {"dosya": _s20_rel(S20_YOL["b_sonuc"]), "sha256": _s20_sha(S20_YOL["b_sonuc"]), "n_U1b": n, "karar": k,
            "on_kayit": B.get("on_kayit")}


def s20_satir(J: Dict[str, Any]) -> List[pd.Series]:
    """Seçilen 20 olayın U1 satırları, sayfa sırasıyla. Seçimdeki giriş / dönem / L1 / L2 / E0 / stop0 satırla birebir olmalı."""
    U = J["U"]; out = []
    for s in J["secim"]:
        m = U[(U.pazar == s["pazar"]) & (U.sembol == s["sembol"]) & (U.tarih == s["tarih"])]
        if len(m) != 1:
            raise S20Hata(f"sayfa {s['sayfa']}: satır dosyasında {len(m)} eşleşme")
        r = m.iloc[0]
        for k in ("giris", "donem", "L1_tarih", "L2_tarih"):
            if str(r[k]) != str(s[k]):
                raise S20Hata(f"sayfa {s['sayfa']}: seçim {k} {s[k]} != satır {r[k]}")
        for k in ("E0", "stop0"):
            if not _s20_15g(s[k], r[k]):
                raise S20Hata(f"sayfa {s['sayfa']}: seçim {k} satırdan farklı")
        if not (float(r["F65"]) <= float(S20_ESIK["F65_ust"]) and str(r["tarih"]) <= str(S20_ESIK["t_son"])):
            raise S20Hata(f"sayfa {s['sayfa']}: satır U1b / t sınırı şartını tutmuyor")
        out.append(r)
    return out


# ================================================================ 2) SONRASI 20 MUM ve UZATMA (K2, K3, KASA)
def s20_sonrasi(Vd: Dict[str, Any], g: Dict[str, Any], kesik: pd.Timestamp) -> Dict[str, Any]:
    """Tam geçerli seri: t'ye kadarki barlar kesik seriyle BİREBİR (K2); t'den sonraki ilk 20 geçerli bar (K3); 20. mum <= KASA kesiği."""
    sembol = g["sembol"]; t = pd.Timestamp(g["t"]); ti = int(g["ti"]); n = int(S20_ESIK["sonra"])
    ham = Vd["V"][sembol]
    tam = YH._yh_hazir(ham)
    if len(tam) <= ti or tam.index[ti] != t or not tam.index[:ti + 1].equals(pd.DatetimeIndex(g["idx"])):
        raise S20Hata(f"{sembol} {t.date()}: tam serinin t'ye kadarki barları kesik seriyle aynı değil (K2)")
    for c, k in (("Open", "O"), ("High", "H"), ("Low", "L"), ("Close", "C"), ("Volume", "V")):
        if not np.array_equal(tam[c].to_numpy(float)[:ti + 1], np.asarray(g[k], float)):
            raise S20Hata(f"{sembol} {t.date()}: tam seri {c} t'ye kadar kesik seriden farklı (K2)")
    so = tam.iloc[ti + 1: ti + 1 + n]
    if len(so) != n:
        raise S20Hata(f"{sembol} {t.date()}: t'den sonra {len(so)} geçerli bar var ({n} gerekir)")
    if so.index[-1] > kesik:
        raise S20Hata(f"{sembol} {t.date()}: {n}. mum {so.index[-1].date()} KASA açık kesiğini ({kesik.date()}) aşıyor -> DUR")
    Op, Hi, Lo, Cl, Vo = (so[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    if not bool((np.isfinite(np.c_[Op, Hi, Lo, Cl, Vo]).all()) and ((Hi > Lo) & (Vo > 0) & (Op > 0) & (Cl > 0) & (Lo > 0)).all()):
        raise S20Hata(f"{sembol} {t.date()}: sonraki {n} mumda geçersiz bar var (K3)")
    if not bool(np.all(np.diff(so.index.asi8) > 0)) or so.index[0] <= t:
        raise S20Hata(f"{sembol} {t.date()}: sonraki mumlar sıralı / tekil değil (K3)")
    ara = ham[(ham.index > t) & (ham.index <= so.index[-1])]
    return {"tarih": pd.DatetimeIndex(so.index), "O": Op, "H": Hi, "L": Lo, "C": Cl, "V": Vo,
            "atlanan_gecersiz": int(len(ara) - n)}


def s20_uzat(cz: Dict[str, Any], g: Dict[str, Any], so: Dict[str, Any]) -> Dict[str, Any]:
    """Çizim verisi [a, t + 20]: t'ye kadar o20_cizim AYNEN; MACD aynı pencere başından (t-250) t+20'ye yh_macd, RSI nedensel seri.
    t'ye kadarki MACD / sinyal / histogram / RSI kodun görüşüyle BİREBİR olmalı (değilse DURUR)."""
    a, ti, w0 = int(cz["a"]), int(g["ti"]), int(g["w0"])
    Ct = np.r_[np.asarray(g["C"], float), so["C"]]
    m2, s2, h2 = YH.yh_macd(Ct[w0:], YH.YH_ESIK8)
    k = ti + 1 - w0
    if not (np.array_equal(m2[:k], g["m"], equal_nan=True) and np.array_equal(s2[:k], g["s"], equal_nan=True)
            and np.array_equal(h2[:k], g["h"], equal_nan=True)):
        raise S20Hata(f"{g['sembol']}: MACD uzatması t'ye kadar kodun görüşüyle aynı değil (K2)")
    rsi2 = MU._mu_rsi(Ct)
    if not np.array_equal(rsi2[:ti + 1], np.asarray(g["rsi"], float), equal_nan=True):
        raise S20Hata(f"{g['sembol']}: RSI uzatması t'ye kadar kodun görüşüyle aynı değil (K2)")
    nt = len(cz["L"]) - 1
    ez = {"a": a, "nt": nt, "tarih": cz["tarih"].append(so["tarih"]),
          "O": np.r_[cz["O"], so["O"]], "H": np.r_[cz["H"], so["H"]], "L": np.r_[cz["L"], so["L"]], "C": np.r_[cz["C"], so["C"]],
          "V": np.r_[cz["V"], so["V"]], "macd": m2[a - w0:].copy(), "sinyal": s2[a - w0:].copy(), "hist": h2[a - w0:].copy(),
          "rsi": rsi2[a:].copy(), "i1": int(cz["i1"]), "i2": int(cz["i2"])}
    n = int(S20_ESIK["sonra"])
    for kk in ("O", "H", "L", "C", "V", "macd", "sinyal", "hist", "rsi"):
        if len(ez[kk]) != nt + 1 + n or not np.array_equal(ez[kk][:nt + 1], np.asarray(cz[kk], float), equal_nan=True):
            raise S20Hata(f"{g['sembol']}: çizimin t'ye kadarki kısmı ({kk}) kodun görüşünden farklı (K2)")
    if ez["tarih"][nt] != pd.Timestamp(g["t"]) or not bool(np.all(np.diff(ez["tarih"].asi8) > 0)):
        raise S20Hata(f"{g['sembol']}: çizim tarihleri t'de bölünmüyor ya da sıralı değil (K2 / K3)")
    return ez


# ================================================================ 3) SONUÇ: ÇİZİMDEN ve PANELDEN YENİDEN HESAP
def s20_sim(C: np.ndarray, E0: float, stop0: float) -> Dict[str, Any]:
    """YAPI_HEDEF 1. tur 15 bar kuralı (YH_ESIK['olcu']), yh_sim ile aynı işlem sırası, BAĞIMSIZ döngü. Bar k = 0 giriş mumu:
    (1) kapanış < stop (k-1 sonundaki) -> STOP; (2) değilse +%5 / +%10 kapanışla görüldü mü; (3) stop = max(stop, giriş x 1,02 [+%5],
    giriş x 1,07 [+%10], en yüksek kapanış x 0,93). Döner k5, k10, kst (-1 yok), her barda kontrol edilen stop (yol) ve stopun türü."""
    O_ = YH.YH_ESIK["olcu"]; St = O_["stop"]; u = int(O_["ufuk"]); h5, h10 = O_["hedef"]
    C = np.asarray(C, float)
    if len(C) < u:
        raise S20Hata(f"15 bar kuralı için {u} kapanış gerekir ({len(C)})")
    E0 = float(E0); st0 = float(stop0)
    if not (np.isfinite(E0) and E0 > 0 and np.isfinite(st0) and E0 - st0 > 0):
        raise S20Hata("giriş stopun altında ya da tanımsız (bu sette beklenmiyor)")
    T5 = E0 * (1 + h5); T10 = E0 * (1 + h10); K5 = E0 * (1 + St["kilit5"]); K10 = E0 * (1 + St["kilit10"])
    stop = st0; ext = -np.inf; k5 = k10 = kst = -1; yol: List[float] = []
    for k in range(u):
        c = float(C[k]); yol.append(stop)
        if c - stop < 0:
            kst = k
            break
        if k5 < 0 and c - T5 >= 0:
            k5 = k
        if k10 < 0 and c - T10 >= 0:
            k10 = k
        lvl = stop
        if k5 >= 0:
            lvl = max(lvl, K5)
        if k10 >= 0:
            lvl = max(lvl, K10)
        ext = max(ext, c)
        stop = max(lvl, ext * (1 - St["takip"]))
    st5 = kst >= 0 and k5 < 0
    karar = kst if st5 else (k5 if k5 >= 0 else u - 1)
    tur = None
    if kst >= 0:
        tur = "sabit" if yol[kst] == st0 else "takip"
    return {"k5": int(k5), "k10": int(k10), "kst": int(kst), "h5": 1.0 if k5 >= 0 else 0.0, "h10": 1.0 if k10 >= 0 else 0.0,
            "st5": 1.0 if st5 else 0.0, "yol": [float(v) for v in yol], "karar_bar": int(karar), "stop_turu": tur,
            "stop_seviye": float(yol[kst]) if kst >= 0 else None}


def s20_cizimden(so: Dict[str, Any], stop0: float) -> Dict[str, Any]:
    """Yalnız çizilen sonraki 20 mumdan: E0, r15 (c2_rh ile aynı işlem), 15 bar kuralı (s20_sim ve YH.yh_sim), 20 mum kapanış uçları."""
    u = int(YH.YH_ESIK["olcu"]["ufuk"])
    O, H, L, C = so["O"], so["H"], so["L"], so["C"]
    E0 = float(O[0])
    r15 = float(C[u - 1] / O[0] - 1)
    s = s20_sim(C, E0, stop0)
    Sm = YH.yh_sim(C[:, None], H[:, None], L[:, None], np.array([E0]), np.array([float(stop0)]), 1, YH.YH_ESIK)
    rel = C / E0 - 1.0
    imx, imn = int(np.argmax(rel)), int(np.argmin(rel))
    return {**s, "E0": E0, "r15": r15, "yh_olc": bool(Sm["olc"][0]), "yh_h5": float(Sm["h5"][0]), "yh_h10": float(Sm["h10"][0]),
            "yh_st5": float(Sm["st5"][0]), "yh_k5": int(Sm["k5"][0]), "yh_kst": int(Sm["kst"][0]),
            "en_yuksek": float(rel[imx]), "en_yuksek_k": imx, "en_dusuk": float(rel[imn]), "en_dusuk_k": imn, "giris_tarih": so["tarih"][0],
            "t20_tarih": so["tarih"][-1]}


def s20_panel_anahtar(Pn: Dict[str, Any], U: pd.DataFrame, pazar: str) -> Dict[str, Any]:
    """Pazarın satır dosyasındaki bütün U1 olayları -> panel (d, j): c2_olc'un eş dışı kümesi (aynı hipotezin bütün olayları)."""
    P = Pn["P"]; idx = P["tarih"]; jx = {str(s): i for i, s in enumerate(P["sembol"])}
    Up = U[U.pazar == pazar]
    if not len(Up):
        raise S20Hata(f"{pazar}: satır dosyasında U1 olayı yok")
    d = idx.get_indexer(pd.DatetimeIndex(pd.to_datetime(Up.giris)))
    eks = sorted(set(Up.sembol) - set(jx))
    if (d < 0).any() or eks:
        raise S20Hata(f"{pazar}: U1 olaylarının giriş günü / hissesi panelde yok ({int((d < 0).sum())} gün, hisse {eks[:5]})")
    return {"d": d.astype(np.int64), "j": np.array([jx[s] for s in Up.sembol], np.int64), "jx": jx, "n": int(len(Up))}


def s20_panelden(Pn: Dict[str, Any], A: Dict[str, Any], r: pd.Series, stop0: float) -> Dict[str, Any]:
    """CETVEL2 paneli: E0 = Op[d, j], r15 = R15[d, j], c2_es (aynı dışlama kümesi), yh_sim panel penceresi (30 satır birleşik takvim)."""
    P = Pn["P"]
    try:
        d = int(P["tarih"].get_loc(pd.Timestamp(r["giris"])))
    except KeyError as ex:
        raise S20Hata(f"{r['sembol']}: giriş günü {r['giris']} panel takviminde yok") from ex
    j = int(A["jx"][str(r["sembol"])])
    E0 = float(P["Op"][d, j]); x = float(Pn["R15"][d, j])
    e = C2.c2_es(Pn, np.array([d]), np.array([j]), np.array([x]), A["d"], A["j"])
    Rz = int(YH.YH_ESIK["olcu"]["pencere_azami"]); jj = np.array([j])
    Sm = YH.yh_sim(YH._yh_pencere(Pn["Cl"], d, Rz, jj), YH._yh_pencere(P["Hi"], d, Rz, jj), YH._yh_pencere(P["Lo"], d, Rz, jj),
                   np.array([E0]), np.array([float(stop0)]), 1, YH.YH_ESIK)
    return {"d": d, "j": j, "E0": E0, "r15": x, "es_r15": float(e["es_r15"][0]), "n_es": float(e["n_es"][0]), "sira": float(e["sira"][0]),
            "fark": float(e["fark"][0]), "olc": bool(Sm["olc"][0]), "h5": float(Sm["h5"][0]), "h10": float(Sm["h10"][0]),
            "st5": float(Sm["st5"][0]), "k5": int(Sm["k5"][0]), "kst": int(Sm["kst"][0])}


def s20_karsilastir(D: Dict[str, Any], Rc: Dict[str, Any], Rp: Dict[str, Any], r: pd.Series, Y: Dict[str, Any], so: Dict[str, Any],
                    kesik: pd.Timestamp) -> Dict[str, Any]:
    """Kodun görüşü denetimi (o20_karsilastir, AYNEN) + sonuç sayıları: çizimden / panelden = satır dosyası (%.15g birebir, bayraklar eşit)."""
    K: List[Dict[str, Any]] = list(D["kontrol"])

    def ek(grup: str, ad: str, kaynak: str, beklenen: Any, bulunan: Any, ok: bool) -> None:
        K.append({"grup": grup, "ad": ad, "kaynak": kaynak, "tamam": bool(ok), "beklenen": beklenen, "bulunan": bulunan})

    def j(x: Any) -> Any:
        return _s20_f(x) if isinstance(x, (float, np.floating)) else x

    # giriş
    gt = str(Rc["giris_tarih"].date())
    ek("giriş", "giriş günü (t'den sonraki ilk geçerli bar)", "çizim", str(r["giris"]), gt, gt == str(r["giris"]))
    ek("giriş", "E0 = t+1 açılış", "çizim", j(r["E0"]), j(Rc["E0"]), _s20_15g(Rc["E0"], r["E0"]))
    ek("giriş", "E0 = P['Op'][d, j]", "panel", j(r["E0"]), j(Rp["E0"]), _s20_15g(Rp["E0"], r["E0"]))
    ek("giriş", "E0 çizim = panel (bit)", "çizim / panel", j(Rp["E0"]), j(Rc["E0"]), Rc["E0"] == Rp["E0"])
    ek("giriş", "stop0 = Low(L2) x 0,98", "çizim", j(r["stop0"]), j(Y["stop0"]), _s20_15g(Y["stop0"], r["stop0"]))
    ek("giriş", "giriş stopun üstünde (giris_stop_alti = 0)", "satır", 0, int(r["giris_stop_alti"]),
       int(r["giris_stop_alti"]) == 0 and Rc["E0"] > float(Y["stop0"]))
    # r15
    ek("r15", "r15 = t+15 kapanış / E0 - 1", "çizim", j(r["r15"]), j(Rc["r15"]), _s20_15g(Rc["r15"], r["r15"]))
    ek("r15", "r15 = R15[d, j] (c2_rh)", "panel", j(r["r15"]), j(Rp["r15"]), _s20_15g(Rp["r15"], r["r15"]))
    ek("r15", "r15 çizim = panel (bit)", "çizim / panel", j(Rp["r15"]), j(Rc["r15"]), Rc["r15"] == Rp["r15"])
    # eş (yalnız panelden: aynı gün aynı kova, dışlama = pazarın bütün U1 olayları)
    ek("eş", "es_r15 (c2_es)", "panel", j(r["es_r15"]), j(Rp["es_r15"]), _s20_15g(Rp["es_r15"], r["es_r15"]))
    ek("eş", "n_es (c2_es)", "panel", int(r["n_es"]), int(Rp["n_es"]), int(Rp["n_es"]) == int(r["n_es"]))
    ek("eş", "sira (c2_es)", "panel", j(r["sira"]), j(Rp["sira"]), _s20_15g(Rp["sira"], r["sira"]))
    # fark
    ek("fark", "fark = r15 - es_r15 (c2_es)", "panel", j(r["fark"]), j(Rp["fark"]), _s20_15g(Rp["fark"], r["fark"]))
    fs = float(r["fark"]); kim = float(r["r15"]) - float(r["es_r15"])
    kok = (not np.isfinite(fs) and not np.isfinite(kim)) or (np.isfinite(fs) and np.isfinite(kim)
                                                          and abs(fs - kim) <= float(S20_ESIK["fark_kimlik_tol"]))
    ek("fark", "satır içi fark = r15 - es_r15", "satır", j(fs), j(kim), kok)
    # h5 / h10 / stop (1. tur 15 bar kuralı)
    for grp, alan, cz_, yh_, pn_ in (("h5", "h5", "h5", "yh_h5", "h5"), ("h10", "h10", "h10", "yh_h10", "h10"),
                                     ("stop", "stop_oldu", "st5", "yh_st5", "st5")):
        ek(grp, f"{alan} (bağımsız döngü s20_sim)", "çizim", j(r[alan]), j(Rc[cz_]), _s20_bayrak(Rc[cz_], r[alan]))
        ek(grp, f"{alan} (YH.yh_sim, çizilen mumlar)", "çizim", j(r[alan]), j(Rc[yh_]), _s20_bayrak(Rc[yh_], r[alan]))
        ek(grp, f"{alan} (YH.yh_sim, panel penceresi)", "panel", j(r[alan]), j(Rp[pn_]), _s20_bayrak(Rp[pn_], r[alan]))
    ek("stop", "stop_oldu = st5 (giriş stop altı değil)", "satır", j(r["st5"]), j(r["stop_oldu"]), _s20_bayrak(r["stop_oldu"], r["st5"]))
    ek("h5", "mum sırası k5: s20_sim = yh_sim (çizim) = yh_sim (panel)", "çizim / panel", Rc["k5"], [Rc["yh_k5"], Rp["k5"]],
       Rc["k5"] == Rc["yh_k5"] == Rp["k5"])
    ek("stop", "mum sırası kst: s20_sim = yh_sim (çizim) = yh_sim (panel)", "çizim / panel", Rc["kst"], [Rc["yh_kst"], Rp["kst"]],
       Rc["kst"] == Rc["yh_kst"] == Rp["kst"])
    ek("stop", "15 bar ölçülebilir (çizim ve panel)", "çizim / panel", True, [Rc["yh_olc"], Rp["olc"]], bool(Rc["yh_olc"] and Rp["olc"]))
    # uzatma (K2) ve KASA: s20_sonrasi / s20_uzat tutmasaydı buraya gelinmezdi; kayıt için
    ek("uzatma", "tam seri t'ye kadar = kesik seri; MACD / RSI uzatması t'ye kadar birebir", "çizim", True, True, True)
    ek("KASA", f"{S20_ESIK['sonra']}. mum <= KASA açık kesik", "veri", str(kesik.date()), str(Rc["t20_tarih"].date()),
       pd.Timestamp(Rc["t20_tarih"]) <= kesik)
    ek("KASA", "sonraki 20 mum geçerli (H > L, V > 0) ve ardışık", "veri", int(S20_ESIK["sonra"]), int(len(so["C"])),
       len(so["C"]) == int(S20_ESIK["sonra"]))
    bozuk = [k for k in K if not k["tamam"]]
    return {"kontrol": K, "n": len(K), "bozuk": bozuk, "tamam": not bozuk}


# ================================================================ 4) AKIŞ (hazırlık + denetim)
def s20_hazirla(veri: Optional[str] = None) -> Dict[str, Any]:
    """Girdiler + kapı + 20 sayfanın görüşü, sonrası, uzatma, iki yoldan yeniden hesap ve denetim. Biri tutmazsa S20Hata (DUR)."""
    v = veri or S20_YOL["veri"]
    J = s20_secim()
    Bs = s20_b_sonuc()
    G = O20.o20_kapi(v)
    kesik = pd.Timestamp(G["kasa"]["kesik"])
    sat = s20_satir(J)
    olay = O20.o20_olay(J)
    sayfa: List[Optional[Dict[str, Any]]] = [None] * len(J["secim"])
    pazarlar = list(dict.fromkeys(s["pazar"] for s in J["secim"]))
    for p in pazarlar:
        Pn = C2.c2_panel22_al(p, v, 15, onbellek=False)
        A = s20_panel_anahtar(Pn, J["U"], p)
        Vd = Pn["Vd"]
        for i, (s, r, ol) in enumerate(zip(J["secim"], sat, olay)):
            if s["pazar"] != p:
                continue
            g = O20.o20_gorus(Vd, s["sembol"], s["tarih"])
            cz = O20.o20_cizim(g)
            Y = O20.o20_yeniden(cz)
            D = O20.o20_karsilastir(Y, cz, g, r, ol)
            so = s20_sonrasi(Vd, g, kesik)
            ez = s20_uzat(cz, g, so)
            Rc = s20_cizimden(so, float(Y["stop0"]))
            Rp = s20_panelden(Pn, A, r, float(Y["stop0"]))
            Kd = s20_karsilastir(D, Rc, Rp, r, Y, so, kesik)
            sayfa[i] = {"no": int(s["sayfa"]), "pazar": p, "sembol": s["sembol"], "tarih": s["tarih"], "satir": r, "g": g, "cz": cz, "Y": Y,
                        "so": so, "ez": ez, "Rc": Rc, "Rp": Rp, "D": Kd}
            s20log.info("sayfa %d (%s %s): %d / %d kontrol tuttu", int(s["sayfa"]), p, s["sembol"], Kd["n"] - len(Kd["bozuk"]), Kd["n"])
        del Pn, A, Vd
    if any(x is None for x in sayfa):
        raise S20Hata("bazı sayfalar hazırlanamadı")
    S: List[Dict[str, Any]] = [x for x in sayfa if x is not None]
    bozuk = [(x["no"], k["kaynak"], k["ad"]) for x in S for k in x["D"]["bozuk"]]
    if bozuk:
        raise S20Hata(f"yeniden hesap satır dosyasıyla / kodla aynı DEĞİL ({len(bozuk)} kontrol): {bozuk[:8]} -> DURDU (PDF / tablo yazılmadı)")
    return {"J": J, "B": Bs, "G": G, "kesik": kesik, "sayfa": S, "ozet": s20_ozet(S)}


def s20_ozet(S: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Kapak özeti (20 olay): sayılar satır dosyasından; mum / stop türü çizimden (satırla birebir denetlendi)."""
    r = [x["satir"] for x in S]
    f = lambda k: np.array([float(q[k]) for q in r])  # noqa: E731
    h5, h10, st, r15, es, fk = f("h5"), f("h10"), f("stop_oldu"), f("r15"), f("es_r15"), f("fark")
    esh5, esh10, esst = f("es_h5"), f("es_h10"), f("es_st5")
    ok = np.isfinite(es) & np.isfinite(fk)
    tur = [x["Rc"]["stop_turu"] for x in S if float(x["satir"]["stop_oldu"]) == 1.0]
    eksiz = [f"{x['sembol']} ({x['tarih'][:4]})" for x, o in zip(S, ok) if not o]
    return {"n": len(S), "h5": int((h5 == 1).sum()), "h10": int((h10 == 1).sum()), "stop": int((st == 1).sum()),
            "hicbiri": int(((h5 != 1) & (st != 1)).sum()), "stop_takip": int(sum(t == "takip" for t in tur)),
            "stop_sabit": int(sum(t == "sabit" for t in tur)),
            "r15_ort": float(np.mean(r15)), "r15_med": float(np.median(r15)),
            "es_n": int(ok.sum()), "es_r15_ort": float(np.mean(es[ok])), "es_r15_med": float(np.median(es[ok])),
            "fark_ort": float(np.mean(fk[ok])), "fark_med": float(np.median(fk[ok])),
            "es_h5_ort": float(np.nanmean(esh5)), "es_h10_ort": float(np.nanmean(esh10)), "es_st5_ort": float(np.nanmean(esst)),
            "es_h_n": int(np.isfinite(esh5).sum()), "essiz": eksiz}


def s20_tablo_md(S: List[Dict[str, Any]]) -> str:
    """Denetim tablosu: grup başına bütün kaynaklarda tuttu mu (✓ / ✗) + kontrol sayısı."""
    L = ["| sayfa | pazar | sembol | " + " | ".join(S20_GRUP) + " | kontrol |", "|---|---|---|" + "---|" * (len(S20_GRUP) + 1)]
    for x in S:
        K = x["D"]["kontrol"]
        hucre = []
        for g in S20_GRUP:
            k = [c for c in K if c["grup"] == g]
            hucre.append(("✓" if all(c["tamam"] for c in k) else "✗") if k else "-")
        L.append(f"| {x['no']} | {x['pazar']} | {x['sembol']} | " + " | ".join(hucre) + f" | {x['D']['n'] - len(x['D']['bozuk'])} / {x['D']['n']} |")
    return "\n".join(L)


# ================================================================ 5) ÇİZİM (A4 dikey; telefonda okunur)
def _s20_ayir(ax: Any, fig: Any, ylist: List[float], ara_pt: float) -> List[float]:
    """Sağ kenar etiketleri üst üste binmesin: ekran biriminde en az ara_pt; önce yukarı it, eksen tepesini aşarsa aşağıdan geri it."""
    if not ylist:
        return []
    tr = ax.transData; inv = tr.inverted(); ara = float(ara_pt) * fig.dpi / 72.0
    sira = sorted(range(len(ylist)), key=lambda i: ylist[i])
    ek = [float(tr.transform((0.0, ylist[i]))[1]) for i in sira]
    for k in range(1, len(ek)):
        ek[k] = max(ek[k], ek[k - 1] + ara)
    tepe = float(ax.transAxes.transform((0.0, 1.0))[1]) - ara * 0.5
    if ek[-1] > tepe:
        ek[-1] = tepe
        for k in range(len(ek) - 2, -1, -1):
            ek[k] = min(ek[k], ek[k + 1] - ara)
    out = [0.0] * len(ylist)
    for k, i in enumerate(sira):
        out[i] = float(inv.transform((0.0, ek[k]))[1])
    return out


def s20_sayfa_ciz(x: Dict[str, Any], toplam: int):
    plt = O20._o20_plt()
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch, FancyBboxPatch
    R = S20_RENK
    ez, Y, Rc, r = x["ez"], x["Y"], x["Rc"], x["satir"]
    W, Hs = S20_ESIK["sayfa_boyut"]
    fig = plt.figure(figsize=(W, Hs))
    axp = fig.add_axes([0.06, 0.505, 0.90, 0.397])
    axm = fig.add_axes([0.06, 0.350, 0.90, 0.147], sharex=axp)
    axr = fig.add_axes([0.06, 0.292, 0.90, 0.050], sharex=axp)
    O, H, L, C = ez["O"], ez["H"], ez["L"], ez["C"]
    nt = int(ez["nt"]); N = len(L); ns = N - 1 - nt
    xx = np.arange(N) - nt                                       # t = 0; sonrası 1..20 (geçerli bar sırası, aralıksız)
    i1, i2 = int(Y["i1"]), int(Y["i2"]); x1, x2 = i1 - nt, i2 - nt
    l1, l2 = float(L[i1]), float(L[i2]); st = float(Y["stop0"]); tp = float(Y["tepe120"])
    E0 = float(Rc["E0"]); hd = YH.YH_ESIK["olcu"]["hedef"]; T5, T10 = E0 * (1 + hd[0]), E0 * (1 + hd[1])
    kb = int(Rc["karar_bar"]); yol = np.asarray(Rc["yol"][:kb + 1], float)
    alt = min(float(L.min()), st, float(yol.min())); ust = max(float(H.max()), T10); pad = (ust - alt) * 0.05
    sag = ns + 0.5 + float(S20_ESIK["sag_bos"]); xs0, xs1 = 0.5, ns + 0.5
    # --- sonrası gölgesi (t'den sonra başlar), sinyal günü ve 15. mum çizgileri
    for ax in (axp, axm, axr):
        ax.axvspan(xs0, xs1, color=R["golge"], lw=0, zorder=0)
        ax.axvline(0, color=R["sinyal_gunu"], linewidth=0.9, linestyle=(0, (1, 2.5)), zorder=1)
        ax.axvline(int(YH.YH_ESIK["olcu"]["ufuk"]), color=R["ufuk"], linewidth=1.0, linestyle=(0, (5, 2, 1, 2)), zorder=1)
    # --- mumlar
    renk = np.where(C >= O, R["yukari"], R["asagi"])
    axp.vlines(xx, L, H, colors=renk, linewidth=1.0, zorder=3)
    govde = np.maximum(np.abs(C - O), (ust - alt) * 0.0015)
    axp.bar(xx, govde, bottom=np.minimum(O, C), width=0.66, color=renk, edgecolor=renk, linewidth=0.3, zorder=4)
    # --- 120 bar tepesi: [L2 - 120, L2]
    g120 = int(MU.MU_ESIK["dipte"]["geri"]); xa = x2 - g120
    axp.plot([xa, x2], [tp, tp], color=R["tepe"], linewidth=1.0, linestyle=(0, (4, 3)), zorder=2)
    axp.text(xa + 0.5, tp + pad * 0.18, "120 bar tepesi", color="#555555", fontsize=11, ha="left", va="bottom", zorder=9,
             bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    # --- sabit stop: Low(L2) x 0,98, L2'den t+20'ye
    axp.plot([x2, xs1], [st, st], color=R["stop"], linewidth=1.8, linestyle=(0, (6, 3)), zorder=5)
    # --- ölçümün o günkü stopu (takip), giriş mumundan karar mumuna kadar; sabit stoptan yukarıdaysa
    if bool((yol > st).any()):
        axp.stairs(yol, np.arange(len(yol) + 1) + 0.5, baseline=None, color=R["takip"], linewidth=1.5, linestyle=(0, (1, 1.2)), zorder=6)
    # --- hedefler ve giriş seviyesi (t+1'den t+20'ye)
    axp.plot([xs0, xs1], [T5, T5], color=R["hedef5"], linewidth=1.6, linestyle=(0, (5, 3)), zorder=5)
    axp.plot([xs0, xs1], [T10, T10], color=R["hedef10"], linewidth=1.6, linestyle=(0, (5, 3)), zorder=5)
    axp.plot([xs0, xs1], [E0, E0], color=R["giris"], linewidth=0.9, linestyle=(0, (1, 2)), zorder=5)
    # --- iki dip: Low noktasında daire + mavi çizgi (ornek20 ile aynı)
    axp.plot([x1, x2], [l1, l2], color=R["mavi"], linewidth=2.6, zorder=6, solid_capstyle="round")
    axp.plot([x1, x2], [l1, l2], linestyle="none", marker="o", markersize=15, markerfacecolor="none", markeredgecolor=R["mavi"],
             markeredgewidth=2.2, zorder=7)
    tx1, tx2 = O20._o20_etiket_x(x1, x2); ye = alt - pad * 1.05
    for tx, xq, yq, s_ in ((tx1, x1, l1, "1. dip"), (tx2, x2, l2, "2. dip")):
        axp.annotate(s_, xy=(xq, yq), xytext=(tx, ye), ha="center", va="top", fontsize=13, fontweight="bold", color=R["mavi"], zorder=9,
                     arrowprops=dict(arrowstyle="-", color=R["mavi"], lw=1.0, shrinkA=1, shrinkB=8),
                     bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))
    # --- giriş üçgeni (t+1 açılışı), +%5 yıldızı / stop çarpısı (karar mumunda)
    axp.plot([1], [E0], marker="^", markersize=10, markerfacecolor="none", markeredgecolor=R["giris_kenar"], markeredgewidth=1.8,
             linestyle="none", zorder=11)                         # içi boş: t+1 mumu üçgenin içinden görünür
    if Rc["k5"] >= 0:
        q = nt + 1 + int(Rc["k5"])
        axp.plot([Rc["k5"] + 1], [H[q] + pad * 0.55], marker="*", markersize=14, markerfacecolor=R["yildiz"], markeredgecolor=R["yildiz_kenar"],
                 markeredgewidth=0.8, linestyle="none", zorder=12)
    if Rc["st5"] == 1.0:
        q = nt + 1 + int(Rc["kst"])
        axp.plot([Rc["kst"] + 1], [L[q] - pad * 0.55], marker="X", markersize=10.5, markerfacecolor=R["carpi"],
                 markeredgecolor=R["carpi_kenar"], markeredgewidth=0.8, linestyle="none", zorder=12)
    axp.set_ylim(alt - pad * 3.3, ust + pad * 1.9)
    axp.text(-0.7, ust + pad * 1.75, "sinyal günü", ha="right", va="top", fontsize=12, color="#222222", zorder=10,
             bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))
    axp.text((xs0 + xs1) / 2.0, ust + pad * 1.75, "sonrası\n20 mum", ha="center", va="top", fontsize=10, color="#333333", zorder=10,
             linespacing=1.05, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    axp.text(int(YH.YH_ESIK["olcu"]["ufuk"]), alt - pad * 3.15, "15. mum", ha="center", va="bottom", fontsize=10, color=R["ufuk"], zorder=10,
             bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))
    # --- MACD paneli: t'ye kadar kodun penceresi [t-250, t]; sonrası aynı hesabın devamı
    for ax in (axp, axm, axr):
        ax.set_xlim(xx[0] - 1.0, sag)
    m, s, h = ez["macd"], ez["sinyal"], ez["hist"]
    ok = np.isfinite(h)
    axm.bar(xx[ok], h[ok], width=0.7, color=R["hist"], zorder=2)
    axm.axhline(0.0, color="#333333", linewidth=0.9, zorder=3)
    axm.plot(xx, s, color=R["sinyal"], linewidth=1.3, zorder=4)
    axm.plot(xx, m, color=R["macd"], linewidth=1.6, zorder=5)
    m1, m2 = float(m[i1]), float(m[i2])
    axm.plot([x1, x2], [m1, m2], color=R["mavi"], linewidth=2.4, zorder=6, solid_capstyle="round")
    axm.plot([x1, x2], [m1, m2], linestyle="none", marker="o", markersize=12, markerfacecolor="none", markeredgecolor=R["mavi"],
             markeredgewidth=2.0, zorder=7)
    yv = np.concatenate([m[np.isfinite(m)], s[np.isfinite(s)], h[ok], [0.0]])
    ma, mu = float(yv.min()), float(yv.max()); mp = (mu - ma) * 0.08 if mu > ma else 1.0
    yme = ma - mp * 1.45
    for tx, xq, yq, s_ in ((tx1, x1, m1, "1. dip"), (tx2, x2, m2, "2. dip")):
        axm.annotate(s_, xy=(xq, yq), xytext=(tx, yme), ha="center", va="top", fontsize=10.5, fontweight="bold", color=R["mavi"], zorder=9,
                     arrowprops=dict(arrowstyle="-", color=R["mavi"], lw=0.9, shrinkA=1, shrinkB=6),
                     bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))
    axm.set_ylim(ma - mp * 3.9, mu + mp * 2.2)
    axm.text(xx[0] + 0.5, mu + mp * 2.0, "MACD (12, 26, 9) siyah · sinyal kırmızı · histogram gri", fontsize=9.5, ha="left", va="top",
             color="#333333", zorder=10, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
    axm.text(sag - 0.3, 0.0, "0", fontsize=10.5, ha="right", va="center", color="#333333")
    # --- RSI paneli (bilgi)
    axr.plot(xx, ez["rsi"], color=R["rsi"], linewidth=1.2, zorder=4)
    for v in (30.0, 70.0):
        axr.axhline(v, color="#8a8a8a", linewidth=0.8, linestyle=(0, (3, 3)), zorder=2)
        axr.text(sag - 0.3, v, f"{int(v)}", fontsize=9, ha="right", va="center", color="#555555")
    axr.set_ylim(0, 100)
    axr.text(xx[0] + 0.5, 96, "RSI 14 (bilgi)", fontsize=9, ha="left", va="top", color="#333333", zorder=10,
             bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    for ax in (axp, axm, axr):
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_linewidth(0.6); sp.set_color("#999999")
    # --- sağ kenar etiketleri (çizgilerin sonu; üst üste binmez)
    et = [("stop", st, R["stop"], 12.0, "bold"), ("giriş", E0, R["giris_kenar"], 11.0, "bold"), ("+%5", T5, R["hedef5"], 11.0, "bold"),
          ("+%10", T10, R["hedef10"], 11.0, "bold")]
    yy = _s20_ayir(axp, fig, [e[1] for e in et], float(S20_ESIK["etiket_ara_pt"]))
    for (s_, y0_, c_, fs_, fw_), y_ in zip(et, yy):
        if abs(y_ - y0_) > 1e-12 * max(1.0, abs(y0_)):          # kaydırılan etikete çizginin ucundan ince bağlantı
            axp.plot([xs1, xs1 + 1.3], [y0_, y_], color=c_, linewidth=0.8, zorder=10, clip_on=False)
        axp.text(xs1 + 1.5, y_, s_, color=c_, fontsize=fs_, fontweight=fw_, ha="left", va="center", zorder=10, clip_on=False)
    # --- başlık (+ kodun sayıları, küçük; hüküm yok)
    fig.text(0.05, 0.962, f"{int(x['no'])}", fontsize=40, fontweight="bold", ha="left", va="center")
    fig.text(0.50, 0.968, f"{x['pazar']} · {x['sembol']}", fontsize=24, fontweight="bold", ha="center", va="center")
    fig.text(0.50, 0.937, f"sinyal günü {_s20_tarih(x['tarih'])}", fontsize=12, color="#444444", ha="center", va="center")
    fig.text(0.95, 0.962, f"/ {int(toplam)}", fontsize=16, color="#666666", ha="right", va="center")
    fig.text(0.50, 0.914, s20_kod_satiri(Y), fontsize=10, color="#444444", ha="center", va="center")
    # --- işaret anahtarı (her sayfada aynı; sütun sütun: giriş / hedefler, stoplar / gölge, işaretler / ufuk)
    axl = fig.add_axes([0.06, 0.236, 0.90, 0.050]); axl.set_axis_off()
    tut = [Line2D([], [], marker="^", markersize=9, markerfacecolor="none", markeredgecolor=R["giris_kenar"], markeredgewidth=1.6,
                  linestyle="none"),
           Line2D([], [], color=R["hedef5"], linewidth=1.6, linestyle=(0, (5, 3))),
           Line2D([], [], color=R["hedef10"], linewidth=1.6, linestyle=(0, (5, 3))),
           Line2D([], [], color=R["stop"], linewidth=1.8, linestyle=(0, (6, 3))),
           Line2D([], [], color=R["takip"], linewidth=1.5, linestyle=(0, (1, 1.2))),
           Patch(facecolor=R["golge"], edgecolor="#bdbdbd", linewidth=0.5),
           Line2D([], [], marker="*", markersize=11, markerfacecolor=R["yildiz"], markeredgecolor=R["yildiz_kenar"], linestyle="none"),
           Line2D([], [], marker="X", markersize=8.5, markerfacecolor=R["carpi"], markeredgecolor=R["carpi_kenar"], linestyle="none"),
           Line2D([], [], color=R["ufuk"], linewidth=1.0, linestyle=(0, (5, 2, 1, 2)))]
    ad = ["giriş (t+1 açılışı)", "+%5 hedef (girişe göre)", "+%10 hedef", "sabit stop (2. dip x 0,98)", "ölçümün o günkü stopu (takip)",
          "sonrası 20 mum", "+%5'e stoptan önce ulaştığı mum", "stopun +%5'ten önce olduğu mum", "15. mum (ölçüm ufku)"]
    axl.legend(tut, ad, loc="center", ncol=3, fontsize=9.0, frameon=False, handlelength=2.2, columnspacing=1.6, handletextpad=0.5,
               borderaxespad=0.0, labelspacing=0.25)
    # --- sonuç kutusu (satır dosyasından; mum sıraları çizimden, satırla birebir denetlendi)
    fig.add_artist(FancyBboxPatch((0.045, 0.012), 0.91, 0.214, boxstyle="round,pad=0.004,rounding_size=0.01", transform=fig.transFigure,
                                  facecolor=R["kutu"], edgecolor=R["kutu_kenar"], linewidth=0.8, zorder=0))
    fig.text(0.07, 0.210, "SONUÇ (satır dosyası)", fontsize=12.5, fontweight="bold", ha="left", va="center", color="#222222")
    for i_, s_ in enumerate(s20_sonuc_satirlari(x)):
        fig.text(0.07, 0.183 - i_ * 0.0258, s_, fontsize=13.0, ha="left", va="center", color="#111111")
    return fig


def s20_kod_satiri(Y: Dict[str, Any]) -> str:
    """Başlık altı küçük satır: kodun t günündeki sayıları (çizimden yeniden hesap; satırla denetlendi)."""
    return (f"2. dip / 1. dip {_s20_yz(Y['F65'])}  ·  MACD 1. dipte {O20._o20_sayi(Y['m1'])}, 2. dipte {O20._o20_sayi(Y['m2'])}  ·  "
            f"2. dipten sinyal gününe {int(Y['tL2'])} bar")


def s20_sonuc_satirlari(x: Dict[str, Any]) -> List[str]:
    """Sonuç kutusu satırları: değerler satır dosyasından (r15, es_r15, fark, h5, h10, stop_oldu); mum sıraları ve 20 mum uçları çizimden."""
    r, Rc = x["satir"], x["Rc"]
    es = _s20_f(r["es_r15"])
    L = [f"15 mum getirisi (t+1 açılış → t+15 kapanış): {_s20_yz(r['r15'])}",
         (f"Aynı gün eşlerin ortalaması: {_s20_yz(es)}   ·   fark: {_s20_puan(r['fark'])}" if es is not None else
          f"Aynı gün eşlerin ortalaması: yok (eş sayısı {int(r['n_es'])})   ·   fark: yok")]
    L.append("+%5 hedef (kapanışla, stoptan önce): " + (f"geldi ({_s20_mum(Rc['k5'])}. mum)" if float(r["h5"]) == 1.0 else "gelmedi"))
    L.append("+%10 hedef (kapanışla, stoptan önce): " + (f"geldi ({_s20_mum(Rc['k10'])}. mum)" if float(r["h10"]) == 1.0 else "gelmedi"))
    if float(r["stop_oldu"]) == 1.0:
        tur = "takip stopu" if Rc["stop_turu"] == "takip" else "sabit stop"
        L.append(f"Stop (+%5'ten önce): oldu ({_s20_mum(Rc['kst'])}. mum, {tur})")
    else:
        L.append("Stop (+%5'ten önce): olmadı")
    L.append(f"20 mumda en yüksek kapanış (girişe göre): {_s20_yz(Rc['en_yuksek'], 1)} ({_s20_mum(Rc['en_yuksek_k'])}. mum)")
    L.append(f"20 mumda en düşük kapanış (girişe göre): {_s20_yz(Rc['en_dusuk'], 1)} ({_s20_mum(Rc['en_dusuk_k'])}. mum)")
    return L


def s20_kapak(J: Dict[str, Any], B: Dict[str, Any], Oz: Dict[str, Any], toplam: int):
    plt = O20._o20_plt()
    R = S20_RENK
    W, Hs = S20_ESIK["sayfa_boyut"]
    fig = plt.figure(figsize=(W, Hs))
    nok = lambda v: f"{int(v):,}".replace(",", ".")  # noqa: E731
    fig.text(0.5, 0.955, "BARİZ MACD UYUMSUZLUĞU —", fontsize=22, fontweight="bold", ha="center", va="center")
    fig.text(0.5, 0.925, f"sinyalden sonra ne oldu ({toplam} rastgele olay)", fontsize=22, fontweight="bold", ha="center", va="center")
    tanim = ("Tanım: ikinci dip birinciden en az %5 aşağı, MACD ikinci dipte daha yukarıda ve sıfırın altında, ikinci dip 120 barın dibi "
             "(ve 120 bar tepesinden en az %20 aşağıda), sinyal günü MACD sinyalin üstünde (ikinci dipten en geç 20 bar sonra).")
    fig.text(0.07, 0.893, "\n".join(textwrap.wrap(tanim, 76)), fontsize=12.5, ha="left", va="top", linespacing=1.38)
    secim = (f"Seçim: {nok(J['evren_n'])} olaydan tohumla rastgele {toplam} (tohum {int(J['tohum'])}; liste çizimden önce kaydedildi). "
             f"{nok(J['evren_n'])} = Ç219'un {nok(B['n_U1b'])} olayından sinyal günü {_s20_tarih(S20_ESIK['t_son'])} ve öncesi olanlar "
             "(sonraki 20 mum açık veride kalsın diye).")
    fig.text(0.07, 0.812, "\n".join(textwrap.wrap(secim, 80)), fontsize=12, ha="left", va="top", linespacing=1.38)
    fig.text(0.07, 0.742, "Bu set kör değil: hisse adı, tarih ve sonuç görünür.", fontsize=12.5, fontweight="bold", ha="left", va="top")
    # --- özet tablo
    fig.text(0.07, 0.700, f"ÖZET ({Oz['n']} olay; 15 mum = giriş mumu t+1 ile t+15 arası)", fontsize=13.5, fontweight="bold", ha="left",
             va="center")
    xo, xe = 0.665, 0.935
    fig.text(xo, 0.674, "olay", fontsize=11.5, fontweight="bold", ha="right", va="center", color="#333333")
    fig.text(xe, 0.674, "aynı gün eşler", fontsize=11.5, fontweight="bold", ha="right", va="center", color="#333333")
    es_n = Oz["es_n"]; n = Oz["n"]
    pay = lambda v: "ort. pay " + O20._o20_yuzde(v, 1, isaret=False)  # noqa: E731
    satir = [("+%5'e stoptan önce ulaşan (kapanışla)", f"{Oz['h5']} / {n}", pay(Oz["es_h5_ort"])),
             ("+%10'a stoptan önce ulaşan", f"{Oz['h10']} / {n}", pay(Oz["es_h10_ort"])),
             ("Stop (+%5'ten önce)", f"{Oz['stop']} / {n}", pay(Oz["es_st5_ort"])),
             ("İkisi de olmadı (15 mumda)", f"{Oz['hicbiri']} / {n}", ""),
             ("15 mum getirisi, ortalama", _s20_yz(Oz["r15_ort"]), f"{_s20_yz(Oz['es_r15_ort'])} ({es_n} olay)"),
             ("15 mum getirisi, medyan", _s20_yz(Oz["r15_med"]), f"{_s20_yz(Oz['es_r15_med'])} ({es_n} olay)")]
    y0, dy = 0.647, 0.0268
    for k, (a_, b_, c_) in enumerate(satir):
        y = y0 - k * dy
        fig.text(0.07, y, a_, fontsize=12.5, ha="left", va="center")
        fig.text(xo, y, b_, fontsize=12.5, ha="right", va="center", fontweight="bold")
        fig.text(xe, y, c_, fontsize=11.5, ha="right", va="center", color="#333333")
    ys = y0 - (len(satir) - 1) * dy - 0.0145
    for yl in (0.688, 0.661, ys):
        fig.add_artist(plt.Line2D([0.07, 0.935], [yl, yl], transform=fig.transFigure, color="#9a9a9a", linewidth=0.7))
    fig.text(0.07, ys - 0.019, f"Fark (olay − eş, {es_n} olay): ortalama {_s20_puan(Oz['fark_ort'])}, medyan {_s20_puan(Oz['fark_med'])}",
             fontsize=12.5, fontweight="bold", ha="left", va="center")
    dip = (f"Stop olan {Oz['stop']} olayın dağılımı: takip stopu (girişten beri en yüksek kapanışın %7 altı) {Oz['stop_takip']}, sabit stop "
           f"(2. dibin en düşüğü x 0,98) {Oz['stop_sabit']}. Eş = aynı giriş günü, aynı kovadaki öteki hisseler (oynaklık, likidite, konum), "
           "aynı kuralla ölçüldü. "
           + (f"Eşi olmayan olay: {', '.join(Oz['essiz'])}. " if Oz["essiz"] else "")
           + "Sonuç sayıları satır dosyasından (uyum_satir.csv.gz); çizimden ve CETVEL2 panelinden yeniden hesaplandı, 20 / 20 birebir.")
    fig.text(0.07, ys - 0.037, "\n".join(textwrap.wrap(dip, 90)), fontsize=10.2, ha="left", va="top", linespacing=1.35, color="#333333")
    uy = (f"Uyarı: {toplam} olay bulgu değildir; {nok(B['n_U1b'])} olayın ölçüm sonucu 'eşlerden ayrışmadı'dır "
          f"(Ç219, karar {B['karar']}).")
    fig.text(0.07, 0.378, "\n".join(textwrap.wrap(uy, 66)), fontsize=13.5, fontweight="bold", ha="left", va="top", linespacing=1.35,
             color=R["uyari"])
    ciz = ("Sayfalar: daire = kodun seçtiği dip (fiyatta mumun en düşüğü, MACD'de çizgi); mavi çizgi iki dibi birleştirir. Gri kesik = 120 "
           "bar tepesi. Noktalı dikey = sinyal günü (t). Açık gri gölge = sinyalden sonraki 20 mum (kodun t günü görmediği kısım). İçi boş yeşil üçgen = "
           "giriş (t+1 açılışı); ince yeşil noktalı = giriş seviyesi. Yeşil kesik = +%5, koyu yeşil kesik = +%10 (girişe göre). Kırmızı kesik = "
           "sabit stop (2. dibin en düşüğü x 0,98). Kırmızı noktalı basamak = ölçümün o günkü stopu: girişten beri en yüksek kapanışın %7 altı "
           "(+%5 görülünce en az giriş +%2), sabit stoptan aşağı inmez; kapanış bu stopun altına inerse stop. Yıldız = +%5'e stoptan önce "
           "kapanışla ulaşılan mum; çarpı = stopun +%5'ten önce olduğu mum. Kesik-noktalı dikey '15. mum' = ölçüm ufku (15 mum getirisi t+15 "
           "kapanışında). Mum sırası: giriş mumu (t+1) = 1. mum; yalnız geçerli günler (sıfır hacimli / H = L günler yok), aralıksız. MACD ve RSI "
           "t'den sonra aynı hesabın devamı (aynı başlangıç); t'ye kadarki değerler kodun gördüğüyle birebir aynı, fark yok. RSI yalnız bilgi.")
    fig.text(0.07, 0.318, "\n".join(textwrap.wrap(ciz, 92)), fontsize=10.2, ha="left", va="top", linespacing=1.36, color="#333333")
    fig.text(0.5, 0.030, "Sayfada hüküm yok: yalnız ne olduğu çizildi ve yazıldı.", fontsize=10.5, ha="center", va="center", color="#555555")
    fig.text(0.5, 0.014, f"satır sha256 {J['satir_sha256'][:16]}… · seçim sha256 {J['secim_sha256'][:16]}…", fontsize=8.5, ha="center",
             va="center", color="#777777", family="DejaVu Sans Mono")
    return fig


# ================================================================ 6) TABLO (belirlenimci) ve YAZIM
def s20_tablo_metin(Hz: Dict[str, Any], pdf: Dict[str, Any]) -> str:
    J, S, Oz = Hz["J"], Hz["sayfa"], Hz["ozet"]
    sayfalar = []
    for x in S:
        r, Y, Rc, Rp, D = x["satir"], x["Y"], x["Rc"], x["Rp"], x["D"]
        gr = {}
        for g in S20_GRUP:
            k = [c for c in D["kontrol"] if c["grup"] == g]
            gr[g] = bool(all(c["tamam"] for c in k)) if k else None
        sayfalar.append({
            "sayfa": int(x["no"]), "pazar": x["pazar"], "sembol": x["sembol"], "tarih": str(r["tarih"]), "giris": str(r["giris"]),
            "t20": str(Rc["t20_tarih"].date()), "donem": str(r["donem"]), "L1_tarih": str(r["L1_tarih"]), "L2_tarih": str(r["L2_tarih"]),
            "kod": {"L1_cizim_sira": int(Y["i1"]), "L2_cizim_sira": int(Y["i2"]), "MACD_L1": _s20_f(Y["m1"]), "MACD_L2": _s20_f(Y["m2"]),
                    "F65": _s20_f(Y["F65"]), "F66": _s20_f(Y["F66"]), "F66m": _s20_f(Y["F66m"]), "F68": _s20_f(Y["F68"]), "S10": _s20_f(Y["S10"]),
                    "dipte": bool(Y["dipte"]), "tL2": _s20_f(Y["tL2"]), "tepe120": _s20_f(Y["tepe120"]), "stop0": _s20_f(Y["stop0"])},
            "satir": {k: _s20_f(r[k]) for k in ("E0", "stop0", "giris_stop_alti", "h5", "h10", "st5", "stop_oldu", "r15", "es_r15", "n_es", "fark",
                                                "sira", "es_h5", "es_h10", "es_st5")},
            "cizimden": {"E0": _s20_f(Rc["E0"]), "r15": _s20_f(Rc["r15"]), "h5": Rc["h5"], "h10": Rc["h10"], "stop_oldu": Rc["st5"],
                         "yh_sim": {"h5": Rc["yh_h5"], "h10": Rc["yh_h10"], "st5": Rc["yh_st5"]},
                         "mum_h5": _s20_mum(Rc["k5"]), "mum_h10": _s20_mum(Rc["k10"]), "mum_stop": _s20_mum(Rc["kst"]),
                         "stop_turu": Rc["stop_turu"], "stop_seviye": Rc["stop_seviye"],
                         "kapanis20_en_yuksek": _s20_f(Rc["en_yuksek"]), "en_yuksek_mum": _s20_mum(Rc["en_yuksek_k"]),
                         "kapanis20_en_dusuk": _s20_f(Rc["en_dusuk"]), "en_dusuk_mum": _s20_mum(Rc["en_dusuk_k"]),
                         "atlanan_gecersiz_bar": int(x["so"]["atlanan_gecersiz"])},
            "panelden": {k: (_s20_f(Rp[k]) if k not in ("d", "j", "olc", "k5", "kst") else Rp[k])
                         for k in ("E0", "r15", "es_r15", "n_es", "sira", "fark", "h5", "h10", "st5", "olc")},
            "kontrol": {"n": int(D["n"]), "tutan": int(D["n"] - len(D["bozuk"])), "gruplar": gr}})
    T = {"surum": S20_SURUM,
         "aciklama": ("MACD_UYUM U1b sonuçlu örnek 20: sayfa başına kodun sayıları (çizimden yeniden hesap; ornek20_ciz denetimi), satır "
                      "dosyasının sonuç alanları ve iki yoldan yeniden hesap (çizilen mumlar; CETVEL2 paneli). Satır = çizim = panel, %.15g "
                      "yazımıyla birebir. Mum sırası: giriş mumu (t+1) = 1. mum. Belirlenimci: zaman damgası yok."),
         "pdf": pdf,
         "secim": {"dosya": _s20_rel(S20_YOL["secim"]), "sha256": J["secim_sha256"], "tohum": int(J["tohum"]), "evren_n": int(J["evren_n"]),
                   "zaman_utc": J.get("zaman_utc"), "kural": J.get("kural")},
         "satir": {"dosya": _s20_rel(S20_YOL["satir"]), "sha256": J["satir_sha256"], "hipotez": S20_ESIK["hipotez"],
                   "U1b_n": int(J["olcum_n_say"]), "evren_n": int(J["evren_n_say"])},
         "olcum": Hz["B"],
         "veri": {"kasa_kesik": str(Hz["kesik"].date()), "sha256": Hz["G"]["veri_sha"]},
         "alan": {"kod": "kodun t günündeki görüşü, çizimden yeniden hesap (ornek20_ciz.o20_yeniden); MACD_L1 / MACD_L2 dipteki MACD değerleri",
                  "satir": "uyum_satir.csv.gz U1 satırı AYNEN (sayfadaki sonuç sayıları bunlardan)",
                  "cizimden": "çizilen sonraki 20 mumdan: E0 = t+1 açılış; r15 = t+15 kapanış / E0 - 1; h5 / h10 / stop_oldu = 1. tur 15 bar kuralı "
                              "(s20_sim ve YH.yh_sim); mum_* = mum numarası (giriş mumu 1); stop_turu = 'sabit' (Low(L2) x 0,98) ya da 'takip' "
                              "(en yüksek kapanış x 0,93 / kilit); kapanis20_* = 20 mumda kapanış / E0 - 1",
                  "panelden": "CETVEL2 c2_panel22_al(ufuk 15): E0 = P['Op'], r15 = R15, es_r15 / n_es / sira / fark = c2_es (dışlama: pazarın bütün U1 "
                              "olayları), h5 / h10 / st5 = YH.yh_sim panel penceresi"},
         "ozet": Oz,
         "kontrol": {"sayfa": len(S), "tutan_sayfa": int(sum(1 for x in S if x["D"]["tamam"])),
                     "kontrol_n": int(sum(x["D"]["n"] for x in S)), "bozuk": int(sum(len(x["D"]["bozuk"]) for x in S))},
         "sayfalar": sayfalar}
    return json.dumps(T, ensure_ascii=False, indent=1, allow_nan=False) + "\n"


def _s20_yaz_bayt(yol: str, veri: bytes, uzerine: bool, ad: str) -> None:
    """Belirlenimci çıktı: dosya varsa ve aynıysa dokunulmaz; farklıysa DURUR (--uzerine verilmedikçe). Geçici dosya + os.replace."""
    if os.path.exists(yol):
        if open(yol, "rb").read() == veri:
            s20log.info("%s zaten var ve aynı (sha %s…)", _s20_rel(yol), hashlib.sha256(veri).hexdigest()[:16])
            return
        if not uzerine:
            raise S20Hata(f"{ad} var ve içerik farklı: {_s20_rel(yol)} (--uzerine yalnız bilerek)")
    gecici = yol + ".gecici"
    with open(gecici, "wb") as f:
        f.write(veri)
    os.replace(gecici, yol)
    if _s20_sha(yol) != hashlib.sha256(veri).hexdigest():
        raise S20Hata(f"{ad} diske beklenen baytlarla yazılmadı")


def s20_ciz(veri: Optional[str] = None, uzerine: bool = False) -> Dict[str, Any]:
    from matplotlib.backends.backend_pdf import PdfPages
    plt = O20._o20_plt()
    Hz = s20_hazirla(veri)
    S = Hz["sayfa"]; toplam = len(S)
    gecici = S20_YOL["pdf"] + ".uretim"
    meta = {"Title": "Bariz MACD uyumsuzlugu - sinyalden sonra ne oldu (20 rastgele olay)", "Author": "sonra20_ciz", "Creator": "sonra20_ciz",
            "Producer": "sonra20_ciz", "CreationDate": None, "ModDate": None}
    try:
        with PdfPages(gecici, metadata=meta) as pdf:
            fig = s20_kapak(Hz["J"], Hz["B"], Hz["ozet"], toplam); pdf.savefig(fig); plt.close(fig)
            for x in S:
                fig = s20_sayfa_ciz(x, toplam); pdf.savefig(fig); plt.close(fig)
        bayt = open(gecici, "rb").read()
    finally:
        if os.path.exists(gecici):
            os.remove(gecici)
    if len(bayt) > int(S20_ESIK["pdf_azami"]):
        raise S20Hata(f"PDF çok büyük: {len(bayt)} bayt")
    if len(bayt) > int(S20_ESIK["pdf_tercih"]):
        s20log.warning("PDF 3 MB'tan büyük: %d bayt", len(bayt))
    pdf_bilgi = {"dosya": _s20_rel(S20_YOL["pdf"]), "sha256": hashlib.sha256(bayt).hexdigest(), "bayt": len(bayt), "sayfa": toplam + 1}
    metin = s20_tablo_metin(Hz, pdf_bilgi)
    try:
        YH._yh_sizinti(metin, "S20 tablo")
    except YH.YHHata as ex:
        raise S20Hata(str(ex)) from ex
    _s20_yaz_bayt(S20_YOL["pdf"], bayt, uzerine, "PDF")
    _s20_yaz_bayt(S20_YOL["tablo"], metin.encode("utf-8"), uzerine, "tablo")
    return {**pdf_bilgi, "tablo": _s20_rel(S20_YOL["tablo"]), "tablo_sha256": _s20_sha(S20_YOL["tablo"]), "md": s20_tablo_md(S),
            "ozet": Hz["ozet"], "kasa": str(Hz["kesik"].date())}


# ================================================================ 7) ÇAKIŞMA KAPISI
def _cakisma_kontrol_s20(_once=_CK_ONCE_S20, _dosya="sonra20_ciz.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur (Colab exec)."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_S20", "_CK_KAYIT", "_cakisma_kontrol_s20", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "hashlib", "argparse", "textwrap", "annotations", "Any", "Dict", "List", "Optional",
           "Tuple", "O20", "MU", "YH", "C2")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_s20()


def _s20_ana(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=S20_SURUM)
    ap.add_argument("komut", nargs="?", default="ciz", choices=["ciz", "denetim"])
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine", action="store_true", help="PDF / tablo farklıysa üzerine yaz (yalnız bilerek)")
    a = ap.parse_args(argv)
    try:
        if a.komut == "denetim":
            Hz = s20_hazirla(a.veri)
            print(s20_tablo_md(Hz["sayfa"]))
            print(f"\nDENETİM: {len(Hz['sayfa'])} / {len(Hz['sayfa'])} sayfa tuttu; özet {json.dumps(Hz['ozet'], ensure_ascii=False)}")
        else:
            R = s20_ciz(a.veri, a.uzerine)
            print(R["md"])
            print(f"\nÖZET: {json.dumps(R['ozet'], ensure_ascii=False)}")
            print(f"PDF: {R['dosya']} ({R['sayfa']} sayfa, {R['bayt']} bayt, sha256 {R['sha256']})")
            print(f"TABLO: {R['tablo']} (sha256 {R['tablo_sha256']})")
    except (S20Hata, O20.O20Hata, MU.MUHata) as ex:
        s20log.error("%s", ex)
        print(f"DURDU: {ex}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__" and "get_ipython" not in globals():
    sys.exit(_s20_ana())
