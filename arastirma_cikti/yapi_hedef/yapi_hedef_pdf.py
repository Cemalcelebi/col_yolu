"""yapi_hedef_pdf.py — YAPI_HEDEF sonuç PDF'i (Cemal'le birlikte değerlendirme; 17 Kasım 2026).

İş tanımı: arastirma_cikti/yapi_hedef/PDF_IS_TANIMI.md.
Bu betik YENİ ÖLÇÜ HESAPLAMAZ. Bütün oranlar, KAT'lar, etiketler sonuc.json'dan; örnek olaylar ve sayımlar olay_Y1..Y5.csv.gz
satır dosyalarından okunur. Fiyat verisi (ORTAK_CETVEL.oc_veri, OC_VERI=/tmp/veri) yalnız örnek grafiklerin mumlarını çizmek içindir;
grafikteki hat / stop0 / tavan / hedef / çıkış değerleri satır dosyasındaki sütunlardır (giriş fiyatı E0, hat, stop0, tavan, k5, kst,
cikis_bar, cikis_tur, getiri). Örnek seçimi tohum 7 ile sabittir.

Komut:  OC_VERI=/tmp/veri python arastirma_cikti/yapi_hedef/yapi_hedef_pdf.py [--cikti YOL]
Çıktı:  arastirma_cikti/yapi_hedef/YAPI_HEDEF_SONUC_2026-11-17.pdf  (A4 yatay, DejaVu Sans, < 8 MB)
Colab:  exec(open('arastirma_cikti/yapi_hedef/yapi_hedef_pdf.py').read())  (kod değiştiyse çalışma zamanını yeniden başlat)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_YP = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import textwrap  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

KLASOR_YP = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(os.getcwd(), "arastirma_cikti", "yapi_hedef")
KOK_YP = os.path.abspath(os.path.join(KLASOR_YP, "..", ".."))
if KOK_YP not in sys.path:
    sys.path.insert(0, KOK_YP)

yplog = logging.getLogger("col.yapi_hedef_pdf")
if not yplog.handlers:
    _yp_h = logging.StreamHandler(sys.stderr)
    _yp_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s yapi_hedef_pdf: %(message)s", "%H:%M:%S"))
    yplog.addHandler(_yp_h)
    yplog.setLevel(logging.INFO)
    yplog.propagate = False


class YPHata(RuntimeError):
    """PDF üretiminde durduran hata."""


YP_AYAR: Dict[str, Any] = {
    "tohum": 7,
    "once": 60,                 # sinyal öncesi mum
    "sonra": 20,                # giriş dahil sonraki mum (çıkış daha geçse grafik çıkışa kadar uzar, en çok 62)
    "sonra_azami": 62,
    "ornek_hedef": 3, "ornek_stop": 3,
    "pazar_sira_hedef": ["ABD", "BIST", "ABD"],
    "pazar_sira_stop": ["BIST", "ABD", "BIST"],
    "donem": ["2023", "2024-26"],          # örnekler karar / bilgi dönemlerinden
    "sayfa": (11.69, 8.27),                # A4 yatay
    "azami_mb": 8.0,
    "sayfa_aralik": (25, 40),
}
YP_YOL: Dict[str, str] = {
    "sonuc": os.path.join(KLASOR_YP, "sonuc.json"),
    "satir": os.path.join(KLASOR_YP, "olay_{d}.csv.gz"),
    "pdf": os.path.join(KLASOR_YP, "YAPI_HEDEF_SONUC_2026-11-17.pdf"),
}
YP_DENEME = ["Y1", "Y2", "Y3", "Y4", "Y5"]
YP_KARAR = [("ABD", "2023"), ("ABD", "2024-26"), ("AVR", "2023"), ("AVR", "2024-26")]
YP_RENK = {"TUTAR": "#cfe8cf", "DESTEKLENMEDİ": "#f2d6d3", "ÖLÇÜLEMEDİ": "#fbefc9", "": "#ffffff"}
YP_PAZAR_AD = {"ABD": "ABD", "AVR": "Avrupa", "BIST": "BIST"}

# Düz dille tanımlar (RAPOR.md '2. TANIM' ve YAPI_HEDEF.py YH_ESIK'ten; yeni şart yok)
YP_TANIM: Dict[str, List[str]] = {
    "Y1": ["S6 taban kodu: düşüşten sonra dar bantlı, düz taban bölgesi (kutu).",
           "AL mumu: kapanış bölge tavanının üstüne çıkar (kırılım mumu).",
           "Hat = bölge dibi (kutunun alt kenarı); stop0 = hat x 0,98.",
           "Giriş = kırılım mumundan sonraki günün açılışı."],
    "Y2": ["FITIL_V2 'TAM_DIP' günleri (alt fitili az mum + dip savunması;",
           "olaylar fitil_v2 çalışmasının dosyasından alındı).",
           "Hat = sinyal günü dahil son 10 barın en düşük fiyatı; stop0 = hat x 0,98.",
           "Giriş = sinyalden sonraki günün açılışı."],
    "Y3": ["KAZAN: 20-60 barlık pencerede dipler çanak gibi (dip serisine eğri",
           "uyumu yukarı açık); sağ kenarın dibi ortadaki dipten %3 yukarıda;",
           "son kapanış pencerenin orta seviyesinin üstünde (DÖNÜŞ).",
           "Kırılım: kapanış pencere tavanının üstünde. Fiyat 120 günlük zirvenin",
           "en az %15 altında. Hat = pencere dibi; stop0 = hat x 0,98."],
    "Y4": ["Y1 olayı + KAĞIT HAFIZASI: aynı hissede son 250 barda önceki",
           "S6 tabanlarından AL sonrası 15 barda +%5 görenler eksi",
           "kırılıp patlayanlar >= 0 ise olay sayılır (yalnız geçmiş).",
           "Hat / stop / giriş Y1 ile aynı."],
    "Y5": ["DÜZ TAVAN SAT (yön aşağı): en az %20 yükselişten sonra 8-70 barlık",
           "düz tavan bölgesi (bant <= %12, yüksekler düz), fiyat 120 günlük",
           "aralığın üst çeyreğinde. SAT mumu: kapanış bölge dibinin %2 altında.",
           "stop0 = bölge tavanı x 1,02; hedef -%5 / -%10 (aşağı)."],
}


# ================================================================ BİÇİM YARDIMCILARI
def _yz(x: Any, n: int = 1) -> str:
    """Oran -> '%34,5' (Türkçe ondalık)."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    return "%" + f"{v * 100:.{n}f}".replace(".", ",")


def _sy(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    return f"{v:.{n}f}".replace(".", ",")


def _bin(x: Any) -> str:
    """Tam sayı -> '37.969' (Türkçe binlik ayırıcı)."""
    try:
        return f"{int(round(float(x))):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "-"


def _fiyat(x: Any) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    n = 2 if v >= 10 else (3 if v >= 1 else 4)
    return _sy(v, n)


def _tarih(t: Any) -> str:
    try:
        return pd.Timestamp(t).strftime("%d.%m.%Y")
    except Exception:
        return str(t)


def _kat(h: Dict[str, Any], k: str) -> str:
    return f"{_sy(h.get(k + '_kat'))} [{_sy(h.get(k + '_alt'))}, {_sy(h.get(k + '_ust'))}]"


def _hucre_ad(h: Dict[str, Any]) -> str:
    return f"{YP_PAZAR_AD.get(h['pazar'], h['pazar'])} {h['donem']}"


def _sart(h: Dict[str, Any]) -> str:
    return "".join("✓" if h.get(k) else "·" for k in ("s_n", "s_kat", "s_stop", "s_plasebo"))


# ================================================================ VERİ OKUMA
def yp_sonuc(yol: Optional[str] = None) -> Dict[str, Any]:
    yol = yol or YP_YOL["sonuc"]
    if not os.path.exists(yol):
        raise YPHata(f"sonuc.json yok: {yol}")
    with open(yol, encoding="utf-8") as f:
        J = json.load(f)
    for d in YP_DENEME:
        if d not in J.get("deneme", {}):
            raise YPHata(f"sonuc.json'da {d} yok")
    return J


def yp_satir(d: str) -> pd.DataFrame:
    yol = YP_YOL["satir"].format(d=d)
    if not os.path.exists(yol):
        raise YPHata(f"satır dosyası yok: {yol}")
    X = pd.read_csv(yol, low_memory=False)
    gerek = {"deneme", "pazar", "sembol", "tarih", "giris", "hat", "stop0", "yon", "n", "tavan", "h5", "h10", "st5", "k5", "kst",
             "es_h5", "es_st5", "n_es", "getiri", "cikis_bar", "cikis_tur", "E0", "dd", "donem"}
    eksik = gerek - set(X.columns)
    if eksik:
        raise YPHata(f"{yol}: eksik sütun {sorted(eksik)}")
    return X


def yp_hucre(J: Dict[str, Any], d: str, pazar: str, donem: str) -> Dict[str, Any]:
    for h in J["deneme"][d]["hucre"]:
        if h["pazar"] == pazar and h["donem"] == donem:
            return h
    raise YPHata(f"{d} {pazar} {donem} hücresi sonuc.json'da yok")


def yp_veri(pazarlar: List[str]) -> Dict[str, Dict[str, pd.DataFrame]]:
    """Grafik mumları için OHLCV (ORTAK_CETVEL.oc_veri; geçerli bar dizisi)."""
    os.environ.setdefault("OC_VERI", "/tmp/veri")
    try:
        import ORTAK_CETVEL as OC
    except Exception as ex:
        raise YPHata(f"ORTAK_CETVEL yüklenemedi: {ex}") from ex
    out: Dict[str, Dict[str, pd.DataFrame]] = {}
    for p in pazarlar:
        try:
            out[p] = OC.oc_veri(p)["V"]
        except Exception as ex:
            raise YPHata(f"{p} verisi yüklenemedi ({os.environ.get('OC_VERI')}): {ex}") from ex
        yplog.info("%s: %d hisse", p, len(out[p]))
    return out


# ================================================================ ÖRNEK SEÇİMİ (tohum 7)
def yp_ornek_sec(X: pd.DataFrame, V: Dict[str, Dict[str, pd.DataFrame]], A: Dict[str, Any] = YP_AYAR) -> List[Tuple[str, pd.Series]]:
    """3 'hedefe ulaşan' (h10 = 1 öncelikli, yoksa h5 = 1) + 3 'stop olan' (st5 = 1); ABD ve BIST karışık; tohum 7."""
    rng = np.random.default_rng(A["tohum"])
    taban = X[X.h5.notna() & X.es_h5.notna() & X.pazar.isin(["ABD", "BIST"]) & X.donem.astype(str).isin(A["donem"])
              & ~X.cikis_tur.astype(str).isin(["giris_stop_otesi", "olculmez", ""])].copy()
    taban = taban[[s in V.get(p, {}) for s, p in zip(taban.sembol, taban.pazar)]]
    secilen: List[Tuple[str, pd.Series]] = []
    kullanilan: set = set()

    def cek(havuz: pd.DataFrame, tur: str) -> Optional[pd.Series]:
        havuz = havuz[~havuz.sembol.isin(kullanilan)]
        if not len(havuz):
            return None
        r = havuz.iloc[int(rng.integers(len(havuz)))]
        kullanilan.add(r.sembol)
        return r

    for tur, sira in (("HEDEF", A["pazar_sira_hedef"]), ("STOP", A["pazar_sira_stop"])):
        for p in sira:
            H = taban[taban.pazar == p]
            if tur == "HEDEF":
                r = cek(H[H.h10 == 1], tur)
                if r is None:
                    r = cek(H[H.h5 == 1], tur)
                if r is None:   # bu pazarda yoksa öteki pazar
                    r = cek(taban[taban.h10 == 1], tur)
            else:
                r = cek(H[H.st5 == 1], tur)
                if r is None:
                    r = cek(taban[taban.st5 == 1], tur)
            if r is None:
                yplog.warning("%s: %s örneği bulunamadı (%s)", X.deneme.iat[0], tur, p)
                continue
            secilen.append((tur, r))
    return secilen


# ================================================================ SAYFA YARDIMCILARI
class Sayfa:
    """PdfPages sarmalayıcı: sayfa numarası, başlık, alt bilgi."""

    def __init__(self, pdf: PdfPages):
        self.pdf = pdf
        self.no = 0

    def yeni(self, baslik: str, alt: str = "") -> plt.Figure:
        fig = plt.figure(figsize=YP_AYAR["sayfa"])
        self.no += 1
        fig.text(0.03, 0.955, baslik, fontsize=15, fontweight="bold", va="top")
        if alt:
            fig.text(0.03, 0.915, alt, fontsize=9.5, color="#444444", va="top")
        fig.text(0.97, 0.015, f"YAPI_HEDEF sonuç · 17.11.2026 · sayfa {self.no}", fontsize=7.5, color="#777777", ha="right")
        return fig

    def kaydet(self, fig: plt.Figure) -> None:
        self.pdf.savefig(fig)
        plt.close(fig)


def _tablo(ax: plt.Axes, satirlar: List[List[str]], basliklar: List[str], genislik: List[float], font: float = 8.0,
           renkler: Optional[List[List[str]]] = None, kalin: Optional[List[bool]] = None, yukseklik: float = 1.0) -> None:
    ax.axis("off")
    t = ax.table(cellText=satirlar, colLabels=basliklar, colWidths=genislik, loc="upper left", cellLoc="center",
                 bbox=[0, 1 - yukseklik, 1, yukseklik])
    t.auto_set_font_size(False)
    t.set_fontsize(font)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#bbbbbb")
        cell.set_linewidth(0.5)
        if r == 0:
            cell.set_facecolor("#e6e6e6")
            cell.set_text_props(fontweight="bold")
        else:
            if renkler is not None:
                cell.set_facecolor(renkler[r - 1][c])
            if kalin is not None and kalin[r - 1]:
                cell.set_text_props(fontweight="bold")


def _metin(fig: plt.Figure, x: float, y: float, satirlar: List[str], font: float = 10.0, aralik: float = 0.032, **kw: Any) -> float:
    for s in satirlar:
        fig.text(x, y, s, fontsize=font, va="top", **kw)
        y -= aralik
    return y


# ================================================================ 1) KAPAK + ÖZET
def yp_kapak(S: Sayfa, J: Dict[str, Any]) -> None:
    fig = S.yeni("YAPI_HEDEF: beş yapı denemesinin sonucu (17 Kasım 2026)",
                 "Cemal'le birlikte değerlendirme için. Sayılar sonuc.json ve olay satır dosyalarından; bu PDF yeni ölçü hesaplamaz.")
    y = _metin(fig, 0.03, 0.87, ["YENİ TEST STANDARDI (Cemal, 17 Kas)"], font=11, fontweight="bold")
    y = _metin(fig, 0.04, y + 0.005, [
        "1. Giriş = kırılım mumu (ölçümde kırılımdan sonraki ilk günün açılışı).",
        "2. Hedef = +%5 ve +%10, stop'tan ÖNCE, 15 işlem günü içinde (kapanışla sayılır; Y5'te aşağı yönde -%5 / -%10).",
        "3. Stop geçicidir: başta hat x 0,98; +%5 görülünce giriş x 1,02, +%10 görülünce giriş x 1,07; en yüksek kapanış x 0,93 ile takip.",
        "4. Eş = aynı gün, aynı kova (60 gün momentum beşliği x likidite üçlüsü) öteki hisseler, aynı stop uzaklığı ve aynı kuralla. KAT = olay / eş.",
    ], font=9.5, aralik=0.03)
    y = _metin(fig, 0.03, y - 0.01, ["BEŞ DENEME"], font=11, fontweight="bold")
    kisa = {"Y1": "S6 düz taban kutusunun yukarı kırılımı (AL mumu).",
            "Y2": "Alt fitili az + dip savunması olan TAM_DIP günleri (FITIL_V2).",
            "Y3": "Çanak (kazan) dibi + sağ kenarda dönüş + pencere tavanının kırılımı.",
            "Y4": "Y1 + kağıt hafızası (aynı hissede önceki tabanlar hedefe gittiyse ya da eşitse).",
            "Y5": "Yükseliş sonrası düz tavanın aşağı kırılımı (SAT mumu; yön aşağı)."}
    y = _metin(fig, 0.04, y + 0.005, [f"{d} {J['deneme'][d]['ad']}: {kisa[d]}" for d in YP_DENEME], font=9.5, aralik=0.029)

    # sonuç tablosu
    ax = fig.add_axes([0.03, 0.155, 0.94, y - 0.165])
    bas = ["Deneme", "ETİKET"] + [f"{YP_PAZAR_AD[p]} {q} (karar)" for p, q in YP_KARAR] + ["BIST 2024-26 (bilgi)"]
    sat, ren = [], []
    for d in YP_DENEME:
        r = [f"{d} {J['deneme'][d]['ad']}", J["deneme"][d]["etiket"]]
        rr = ["#ffffff", YP_RENK.get(J["deneme"][d]["etiket"], "#ffffff")]
        for p, q in YP_KARAR + [("BIST", "2024-26")]:
            h = yp_hucre(J, d, p, q)
            r.append(f"n {h['n']}\nKAT5 {_sy(h.get('h5_kat'))} [{_sy(h.get('h5_alt'))}, {_sy(h.get('h5_ust'))}]\n{h['durum']}")
            rr.append(YP_RENK.get(h["durum"], "#ffffff"))
        sat.append(r)
        ren.append(rr)
    _tablo(ax, sat, bas, [0.17, 0.10, 0.146, 0.146, 0.146, 0.146, 0.146], font=7.6, renkler=ren)

    # okuma cümlesi (sayılar sonuc.json'dan)
    h3 = yp_hucre(J, "Y3", "ABD", "2023")
    h5 = yp_hucre(J, "Y5", "BIST", "2024-26")
    tutan_karar = sum(1 for d in YP_DENEME for p, q in YP_KARAR if yp_hucre(J, d, p, q)["durum"] == "TUTAR")
    okuma = (f"OKUMA: TUTAN karar hücresi {tutan_karar} / 20; beş denemenin etiketi de ÖLÇÜLEMEDİ. Y3 hem hedefi hem stopu eşlerden sık görüyor "
             f"(ABD 2023: +%5 {_yz(h3['h5_p_olay'])} / eş {_yz(h3['h5_p_ref'])}, stop önce {_yz(h3['st5_p_olay'])} / eş {_yz(h3['st5_p_ref'])}): "
             f"bu oynaklıkla uyumlu; 'stop eşten az' şartı tutmuyor. Y5 dört şartı yalnız BIST 2024-26 bilgi hücresinde geçiyor (n {h5['n']}, "
             f"KAT5 {_kat(h5, 'h5')}, güç {_yz(h5.get('guc'), 0)}); bu bir karar hücresi değil.")
    _metin(fig, 0.03, 0.135, textwrap.wrap(okuma, 165), font=9.2, aralik=0.028)
    S.kaydet(fig)


# ================================================================ 2) OLASILIK TABLOSU
def yp_olasilik(S: Sayfa, J: Dict[str, Any]) -> None:
    gruplar = [["Y1", "Y2", "Y3"], ["Y4", "Y5"]]
    for gi, grup in enumerate(gruplar):
        fig = S.yeni(f"Olasılık tablosu ({gi + 1}/2): olay / eş / taban",
                     "P(+5) = +%5'i stop'tan önce 15 gün içinde görme payı; eş = aynı gün aynı kova; taban = aynı gün bütün havuz. "
                     "KAT = olay / eş [%95 aralığı]. Kalın satır = karar hücresi.")
        bas = ["Deneme", "Hücre", "n", "P(+5) olay / eş / taban", "KAT +5", "P(+10) olay / eş / taban", "KAT +10",
               "P(stop önce)\nolay / eş / taban", "KAT stop", "DURUM"]
        sat, ren, kal = [], [], []
        for d in grup:
            for h in J["deneme"][d]["hucre"]:
                sat.append([d, _hucre_ad(h), str(h["n"]),
                            f"{_yz(h.get('h5_p_olay'))} / {_yz(h.get('h5_p_ref'))} / {_yz(h.get('tb_h5_p'))}", _kat(h, "h5"),
                            f"{_yz(h.get('h10_p_olay'))} / {_yz(h.get('h10_p_ref'))} / {_yz(h.get('tb_h10_p'))}", _kat(h, "h10"),
                            f"{_yz(h.get('st5_p_olay'))} / {_yz(h.get('st5_p_ref'))} / {_yz(h.get('tb_st5_p'))}", _kat(h, "st5"),
                            h["durum"]])
                r = ["#ffffff"] * 9 + [YP_RENK.get(h["durum"], "#ffffff")]
                if (h.get("h5_alt") or 0) > 1:
                    r[4] = "#e3f1e3"
                if (h.get("st5_alt") or 0) > 1:
                    r[8] = "#f6e0de"
                ren.append(r)
                kal.append(bool(h.get("karar_hucre")))
        ax = fig.add_axes([0.03, 0.12 if gi == 0 else 0.30, 0.94, 0.77 if gi == 0 else 0.59])
        _tablo(ax, sat, bas, [0.045, 0.095, 0.045, 0.135, 0.10, 0.135, 0.10, 0.135, 0.10, 0.11], font=7.2 if gi == 0 else 7.8,
               renkler=ren, kalin=kal)
        if gi == 1:
            _metin(fig, 0.03, 0.27, [
                "NASIL OKUNUR",
                "· KAT +5 = 1,10: olay +%5'i eşlerden %10 daha sık görüyor. Köşeli parantez %95 aralığı; alt uç 1'in üstündeyse yeşil.",
                "· KAT stop alt ucu 1'in üstündeyse (pembe): olay stopu da eşlerden sık görüyor; bu, hissenin daha oynak olmasıyla uyumlu.",
                "· Y5 yön aşağıdır: P(+5) orada -%5'i (aşağı hedefi) stop'tan önce görme payıdır; stop = bölge tavanı x 1,02 yukarıda.",
                "· Karar kuralı (önceden yazılı): n >= 30 VE KAT5 alt > 1 VE P(stop) olay < eş VE plasebo KAT5 alt > 1 -> TUTAR.",
                "  Tutmazsa: n >= 1.000 ya da güç >= %80 ise DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ.",
                "· Hayatta kalma: evren bugün işlem gören hisseler; hedef payları yukarı, stop payları aşağı yanlı (eşler de aynı evrenden).",
            ], font=9, aralik=0.03)
        S.kaydet(fig)


# ================================================================ 3) DENEME BÖLÜMÜ: şema + hücreler
def _sema_yol(d: str) -> Dict[str, Any]:
    """Şematik çizgi (gerçek veri değil): fiyat yolu, kırılım indisi, hat / tavan / stop / hedef seviyeleri."""
    rng = np.random.default_rng(YP_AYAR["tohum"])
    g = lambda n, s: rng.normal(0, s, n)  # noqa: E731
    if d in ("Y1", "Y4"):
        dus = np.linspace(100, 70, 25) + g(25, 0.8)
        taban = 70 + 3 * np.sin(np.linspace(0, 6 * np.pi, 30)) + g(30, 0.5)
        kir = np.array([76.5])
        son = np.linspace(77, 82, 14) + g(14, 0.8)
        y = np.r_[dus, taban, kir, son]
        return {"y": y, "t": 55, "pen": (25, 54), "hat": 66.8, "tavan": 74.0, "yon": 1, "giris": 77.0}
    if d == "Y2":
        dus = np.linspace(100, 72, 35) + g(35, 0.8)
        dip = 72 + np.array([0, -1.5, -2.5, -1.0, -2.0, -0.5, 0.5, -1.0, 0.0, 1.5]) + g(10, 0.3)
        son = np.linspace(74, 78, 15) + g(15, 0.9)
        y = np.r_[dus, dip, son]
        return {"y": y, "t": 44, "pen": (35, 44), "hat": 69.0, "tavan": np.nan, "yon": 1, "giris": 74.0}
    if d == "Y3":
        x = np.linspace(-1, 1, 40)
        dus = np.linspace(100, 82, 15) + g(15, 0.8)
        kazan = 72 + 10 * x ** 2 + g(40, 0.6)
        kazan[-8:] = np.linspace(76, 80, 8) + g(8, 0.4)
        kir = np.array([84.0])
        son = np.linspace(84, 90, 14) + g(14, 0.9)
        y = np.r_[dus, kazan, kir, son]
        return {"y": y, "t": 55, "pen": (15, 54), "hat": 71.5, "tavan": 83.0, "yon": 1, "giris": 84.5}
    # Y5
    yuk = np.linspace(70, 95, 30) + g(30, 0.8)
    tav = 92 + 2.5 * np.sin(np.linspace(0, 5 * np.pi, 25)) + g(25, 0.4)
    kir = np.array([87.0])
    son = np.linspace(86, 80, 14) + g(14, 0.9)
    y = np.r_[yuk, tav, kir, son]
    return {"y": y, "t": 55, "pen": (30, 54), "hat": 89.0, "tavan": 95.0, "yon": -1, "giris": 86.5}


def yp_sema(ax: plt.Axes, d: str) -> None:
    S_ = _sema_yol(d)
    y, t, s = S_["y"], S_["t"], S_["yon"]
    x = np.arange(len(y))
    ax.plot(x, y, color="#333333", lw=1.4)
    a, b = S_["pen"]
    ax.axvspan(a, b, color="#d9e6f5", alpha=0.6, lw=0)
    ax.text((a + b) / 2, ax.get_ylim()[1] if False else max(y) * 1.01, "kodun gördüğü yapı", ha="center", fontsize=8, color="#2b5d9c")
    ax.plot([t], [y[t]], marker="^" if s > 0 else "v", color="#d97706", ms=11, zorder=5)
    ax.annotate("kırılım mumu" if s > 0 else "SAT mumu", (t, y[t]), xytext=(t - 18, y[t] + (6 if s > 0 else -8)), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="#d97706"), color="#d97706")
    ax.axvline(t + 1, color="#1f4e9c", ls=":", lw=1.2)
    ax.text(t + 1.5, min(y) * 0.985, "giriş (ertesi açılış)", fontsize=7.5, color="#1f4e9c")
    E = S_["giris"]
    hat = S_["hat"]
    st0 = hat * 0.98 if s > 0 else S_["tavan"] * 1.02
    if np.isfinite(hat):
        ax.axhline(hat, color="#c0392b", ls="--", lw=1.0, xmax=0.98)
        ax.text(1, hat, " hat (bölge dibi)" if s > 0 else " bölge dibi", fontsize=7.5, color="#c0392b", va="bottom")
    ax.axhline(st0, color="#7b1d14", ls="--", lw=1.0)
    ax.text(1, st0, " stop0", fontsize=7.5, color="#7b1d14", va="top" if s > 0 else "bottom")
    if np.isfinite(S_["tavan"]):
        ax.axhline(S_["tavan"], color="#888888", ls=":", lw=1.0)
        ax.text(1, S_["tavan"], " bölge tavanı", fontsize=7.5, color="#666666", va="bottom")
    for k, lab in ((0.05, "%5"), (0.10, "%10")):
        lv = E * (1 + s * k)
        ax.hlines(lv, t + 1, len(y) - 1, color="#1e8449", ls="--", lw=1.0)
        ax.text(len(y) - 0.5, lv, (" +" if s > 0 else " -") + lab, fontsize=7.5, color="#1e8449", va="center")
    if d == "Y4":
        ax.text(2, max(y) * 0.97, "+ geçmişte (son 250 bar) aynı hissenin\nönceki tabanları hedefe gittiyse (+1)\nkırıldıysa (-1); toplam >= 0",
                fontsize=7.5, color="#555555", va="top")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-1, len(y) + 4)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("Şema (çizim, gerçek veri değil)", fontsize=9, loc="left")


def yp_deneme_sayfa(S: Sayfa, J: Dict[str, Any], d: str, X: pd.DataFrame) -> None:
    Jd = J["deneme"][d]
    fig = S.yeni(f"{d} {Jd['ad']} (yön {'yukarı' if Jd['yon'] > 0 else 'aşağı'}): etiket {Jd['etiket']}",
                 f"Satır dosyası: {len(X)} olay (ABD {int((X.pazar == 'ABD').sum())}, Avrupa {int((X.pazar == 'AVR').sum())}, "
                 f"BIST {int((X.pazar == 'BIST').sum())}; 2016-22 / 2023 / 2024-26). Hücre satırları sonuc.json'dan.")
    ax = fig.add_axes([0.03, 0.53, 0.45, 0.31])
    yp_sema(ax, d)
    y = _metin(fig, 0.52, 0.87, ["KODUN TANIMI (düz dille)"], font=10.5, fontweight="bold")
    y = _metin(fig, 0.52, y + 0.004, YP_TANIM[d], font=9.2, aralik=0.031)
    y = _metin(fig, 0.52, y - 0.012, ["Ölçü: giriş ertesi açılış; +%5 / +%10 stop'tan önce 15 gün;",
                                      "eşler aynı gün aynı kova, aynı stop uzaklığı (d) ile."], font=8.6, aralik=0.028, color="#444444")
    bas = ["Hücre", "n", "P(+5) olay / eş", "KAT5 [%95]", "P(stop önce) olay / eş", "plasebo KAT5 [%95]", "şartlar\nn·kat·stop·pls", "güç", "DURUM"]
    sat, ren, kal = [], [], []
    for h in Jd["hucre"]:
        sat.append([_hucre_ad(h) + (" (karar)" if h.get("karar_hucre") else ""), str(h["n"]),
                    f"{_yz(h.get('h5_p_olay'))} / {_yz(h.get('h5_p_ref'))}", _kat(h, "h5"),
                    f"{_yz(h.get('st5_p_olay'))} / {_yz(h.get('st5_p_ref'))}", _kat(h, "pl_h5"), _sart(h), _yz(h.get("guc"), 0), h["durum"]])
        ren.append(["#ffffff"] * 8 + [YP_RENK.get(h["durum"], "#ffffff")])
        kal.append(bool(h.get("karar_hucre")))
    ax2 = fig.add_axes([0.03, 0.06, 0.94, 0.42])
    _tablo(ax2, sat, bas, [0.15, 0.06, 0.12, 0.13, 0.13, 0.14, 0.10, 0.06, 0.11], font=8.2, renkler=ren, kalin=kal)
    S.kaydet(fig)


# ================================================================ 4) ÖRNEK GRAFİK
def _mumlar(ax: plt.Axes, D: pd.DataFrame) -> None:
    x = np.arange(len(D))
    O, H, L, C = (D[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    for i in x:
        r = "#1e8449" if C[i] >= O[i] else "#c0392b"
        ax.vlines(i, L[i], H[i], color=r, lw=0.8)
        alt, boy = min(O[i], C[i]), abs(C[i] - O[i])
        ax.add_patch(Rectangle((i - 0.32, alt), 0.64, max(boy, (H[i] - L[i]) * 0.02 + 1e-12), facecolor=r, edgecolor=r, lw=0.5))


def yp_ornek_sayfa(S: Sayfa, d: str, no: int, tur: str, r: pd.Series, V: Dict[str, Dict[str, pd.DataFrame]], A: Dict[str, Any] = YP_AYAR) -> Dict[str, Any]:
    df = V[r.pazar][r.sembol]
    t_ts, g_ts = pd.Timestamp(r.tarih), pd.Timestamp(r.giris)
    if g_ts not in df.index or t_ts not in df.index:
        raise YPHata(f"{d} {r.sembol} {r.tarih}: sinyal / giriş günü fiyat verisinde yok")
    ti, gi = int(df.index.get_loc(t_ts)), int(df.index.get_loc(g_ts))
    s = int(r.yon)
    E0 = float(r.E0)
    if abs(float(df.Open.iat[gi]) / E0 - 1) > 1e-5:
        yplog.warning("%s %s: veri açılışı %.4f != satır E0 %.4f", d, r.sembol, df.Open.iat[gi], E0)
    cb = int(r.cikis_bar) if np.isfinite(float(r.cikis_bar)) else -1
    sonra = max(A["sonra"], min(cb + 3, A["sonra_azami"])) if cb >= 0 else A["sonra"]
    a = max(0, ti - A["once"])
    b = min(len(df), gi + sonra)
    D = df.iloc[a:b]
    x_t, x_g = ti - a, gi - a

    fig = S.yeni(f"{d} örnek {no}/6 · {'HEDEFE ULAŞAN' if tur == 'HEDEF' else 'STOP OLAN'} · {r.sembol} · {YP_PAZAR_AD[r.pazar]} · "
                 f"sinyal {_tarih(t_ts)}",
                 f"Sinyal öncesi {ti - a} mum + giriş + sonraki mumlar (sonrası gösterilir, kör set değil). Fiyat ekseni gerçek fiyat"
                 f"{' (yerel para)' if r.pazar != 'BIST' else ' (TL)'}; hisse verisi fi_k1_veri düzeltilmiş fiyat.")
    axp = fig.add_axes([0.06, 0.36, 0.86, 0.52])
    axv = fig.add_axes([0.06, 0.24, 0.86, 0.11], sharex=axp)
    _mumlar(axp, D)
    # yapı penceresi
    n = float(r.n) if np.isfinite(float(r.n)) else np.nan
    if np.isfinite(n) and n > 0:
        if d == "Y2":
            p0, p1 = x_t - int(n) + 1, x_t
        else:
            p0, p1 = x_t - int(n), x_t - 1
        axp.axvspan(max(p0, 0) - 0.5, p1 + 0.5, color="#d9e6f5", alpha=0.55, lw=0, zorder=0)
    axp.axvspan(x_t - 0.5, x_t + 0.5, color="#fde2b8", alpha=0.8, lw=0, zorder=0)
    axp.axvline(x_g - 0.5, color="#1f4e9c", ls=":", lw=1.3)
    xs = np.array([max(p0, 0) if np.isfinite(n) and n > 0 else max(x_t - 20, 0), len(D) - 1], float)
    if np.isfinite(float(r.hat)):
        axp.hlines(float(r.hat), xs[0] - 0.5, x_t + 0.5, color="#c0392b", ls="--", lw=1.1)
    axp.hlines(float(r.stop0), x_g - 0.5, len(D) - 0.5, color="#7b1d14", ls="--", lw=1.1)
    if pd.notna(r.tavan) and np.isfinite(float(r.tavan)):
        axp.hlines(float(r.tavan), xs[0] - 0.5, x_t + 0.5, color="#777777", ls=":", lw=1.1)
    T5, T10 = E0 * (1 + s * 0.05), E0 * (1 + s * 0.10)
    axp.hlines([T5, T10], x_g - 0.5, len(D) - 0.5, color="#1e8449", ls="--", lw=1.0)
    axp.plot([x_g], [E0], marker="o", color="#1f4e9c", ms=6, zorder=6)
    axp.annotate("giriş", (x_g, E0), xytext=(-30, 8 if s > 0 else -14), textcoords="offset points", fontsize=8, color="#1f4e9c")
    # ufuk 15 bar sonu
    u_son = x_g + 14
    if u_son < len(D):
        axp.axvline(u_son + 0.5, color="#999999", ls="-.", lw=0.8)
    k5, kst = int(r.k5) if pd.notna(r.k5) else -1, int(r.kst) if pd.notna(r.kst) else -1
    if k5 >= 0 and x_g + k5 < len(D):
        axp.plot([x_g + k5], [float(D.Close.iat[x_g + k5])], marker="*", color="#0b5d1e", ms=15, mec="white", mew=0.8, zorder=9)
    if kst >= 0 and x_g + kst < len(D):
        axp.plot([x_g + kst], [float(D.Close.iat[x_g + kst])], marker="X", color="#c0392b", ms=11, mec="white", mew=0.8, zorder=9)
    # gerçekleşen çıkış (takip stoplu, satır dosyası)
    cikis_fiyat = np.nan
    if cb >= 0 and x_g + cb < len(D):
        ct = str(r.cikis_tur)
        cikis_fiyat = float(D.Open.iat[x_g + cb]) if ct in ("stop", "ters") else float(D.Close.iat[x_g + cb])
        axp.plot([x_g + cb], [cikis_fiyat], marker="D", color="#6c3483", ms=8, zorder=8)
        axp.annotate(f"çıkış ({ct})", (x_g + cb, cikis_fiyat), xytext=(8 if x_g + cb < len(D) - 8 else -70, -14 if s > 0 else 10),
                     textcoords="offset points",
                     fontsize=8, color="#6c3483")
        g_kontrol = s * (cikis_fiyat / E0 - 1)
        if np.isfinite(float(r.getiri)) and abs(g_kontrol - float(r.getiri)) > 1e-4:
            yplog.warning("%s %s: grafikteki çıkış getirisi %.5f != satır getiri %.5f", d, r.sembol, g_kontrol, float(r.getiri))
    # etiketler sağda
    sag = len(D) - 0.3
    for lv, lab, c in ((float(r.stop0), "stop0", "#7b1d14"), (T5, ("+" if s > 0 else "-") + "%5", "#1e8449"),
                       (T10, ("+" if s > 0 else "-") + "%10", "#1e8449")):
        axp.text(sag, lv, " " + lab, fontsize=8, color=c, va="center")
    if np.isfinite(float(r.hat)):
        axp.text(xs[0], float(r.hat), ("hat" if s > 0 else "bölge dibi"), fontsize=8, color="#c0392b", va="top", ha="left")
    if pd.notna(r.tavan) and np.isfinite(float(r.tavan)):
        axp.text(xs[0], float(r.tavan), "tavan", fontsize=8, color="#666666", va="bottom", ha="left")
    lo = min(float(D.Low.min()), float(r.stop0), T10 if s < 0 else E0) * 0.98
    hi = max(float(D.High.max()), float(r.stop0), T10 if s > 0 else E0) * 1.02
    axp.set_ylim(lo, hi)
    axp.set_xlim(-1, len(D) + 5)
    axp.grid(alpha=0.25, lw=0.5)
    axp.tick_params(labelbottom=False, labelsize=8)
    # hacim
    renk = np.where(D.Close.to_numpy(float) >= D.Open.to_numpy(float), "#7fbf8f", "#e39a90")
    axv.bar(np.arange(len(D)), D.Volume.to_numpy(float), color=renk, width=0.7)
    axv.axvline(x_g - 0.5, color="#1f4e9c", ls=":", lw=1.3)
    axv.set_ylabel("hacim", fontsize=8)
    axv.tick_params(labelsize=7.5)
    axv.yaxis.get_offset_text().set_fontsize(7)
    tik = list(range(0, len(D), 10))
    axv.set_xticks(tik)
    axv.set_xticklabels([D.index[i].strftime("%d.%m.%y") for i in tik], fontsize=7.5)
    axv.grid(alpha=0.2, lw=0.5)

    # alt yazı (satır dosyası sütunları)
    yon_s = "+" if s > 0 else "-"
    if d in ("Y1", "Y4"):
        durum = str(r.ek).split(";")[0] if pd.notna(r.ek) else ""
        gor = f"S6 taban bölgesi {int(n) if np.isfinite(n) else '-'} bar ({durum}), hat {_fiyat(r.hat)}, kırılım kapanışı > tavan {_fiyat(r.tavan)}"
        if d == "Y4" and "hafiza" in r.index:
            gor += f"; hafıza {int(r.hafiza)}"
    elif d == "Y2":
        gor = f"TAM_DIP günü; hat = son 10 barın dibi {_fiyat(r.hat)}"
    elif d == "Y3":
        gor = f"kazan penceresi {int(n) if np.isfinite(n) else '-'} bar, dip {_fiyat(r.hat)}, kırılım kapanışı > tavan {_fiyat(r.tavan)} ({r.ek})"
    else:
        gor = f"düz tavan {int(n) if np.isfinite(n) else '-'} bar, bölge {_fiyat(r.hat)} - {_fiyat(r.tavan)}, SAT kapanışı < dip x 0,98 ({r.ek})"
    sonuc_p = []
    sonuc_p.append(f"{yon_s}%5 gün {k5}" if k5 >= 0 else f"{yon_s}%5 yok")
    sonuc_p.append(f"{yon_s}%10 görüldü" if float(r.h10) == 1 else f"{yon_s}%10 yok")
    sonuc_p.append(f"stop gün {kst}" + (" (hedeften önce)" if float(r.st5) == 1 else "") if kst >= 0 else "15 günde stop yok")
    es_s = f"eşler ({int(r.n_es)} hisse): {yon_s}%5 {_yz(r.es_h5, 0)}, stop önce {_yz(r.es_st5, 0)}"
    cik_s = f"takip stoplu çıkış gün {cb} ({r.cikis_tur}), fiyat değişimi {_yz(r.getiri)}" if cb >= 0 else "çıkış ölçülmedi"
    satirlar = [
        f"Kodun gördüğü: {gor}.",
        f"Giriş {_tarih(g_ts)} açılış {_fiyat(E0)}; stop0 {_fiyat(r.stop0)} (uzaklık {_yz(r.dd)}). "
        f"Sonuç (15 gün, giriş günü = 0): {'; '.join(sonuc_p)}. {es_s}.",
        f"{cik_s}. İşaretler: mavi alan = kodun yapı penceresi, turuncu = sinyal mumu, mavi nokta = giriş, yıldız = {yon_s}%5, X = stop, mor = çıkış. Kesikli stop0 yalnız başlangıç stopudur; X takip stopuyla da (çizilmedi) gelebilir.",
    ]
    sar = [w for s_ in satirlar for w in textwrap.wrap(s_, 165)]
    _metin(fig, 0.06, 0.21, sar, font=8.6, aralik=0.026)
    fig.text(0.06, 0.06, "Cemal: ______________________________________________________________________________________________",
             fontsize=11, va="top", color="#333333")
    S.kaydet(fig)
    return {"deneme": d, "tur": tur, "sembol": r.sembol, "pazar": r.pazar, "tarih": str(r.tarih), "giris": str(r.giris),
            "h5": float(r.h5), "h10": float(r.h10), "st5": float(r.st5), "k5": k5, "kst": kst, "cikis_bar": cb,
            "cikis_tur": str(r.cikis_tur), "getiri": float(r.getiri)}


# ================================================================ 5) BİRLİKTE DEĞERLENDİRME
def yp_sayimlar(J: Dict[str, Any], Xs: Dict[str, pd.DataFrame], V: Dict[str, Dict[str, pd.DataFrame]]) -> Dict[str, Any]:
    """Şüphe maddeleri için sayımlar (yalnız satır sayımı / sonuc.json; yeni getiri / hedef ölçüsü yok)."""
    out: Dict[str, Any] = {}
    X1 = Xs["Y1"]
    yil: Dict[str, float] = {}
    for p in ("ABD", "BIST"):
        yil[p] = float(sum(len(df) for df in V[p].values()) / 252.0)
    out["hisse_yil"] = yil
    out["y1_ham"] = {p: J["sayim"]["Y1"][p]["girdi"] for p in ("ABD", "AVR", "BIST")}
    out["y1_tekil"] = {p: int((X1.pazar == p).sum()) for p in ("ABD", "AVR", "BIST")}
    X1y = X1.assign(yil=pd.to_datetime(X1.tarih).dt.year)
    g = X1y.groupby(["pazar", "sembol", "yil"]).size()
    out["y1_hy_med"] = {p: float(g.loc[p].median()) for p in ("ABD", "BIST")}
    out["y1_hy_max"] = {p: int(g.loc[p].max()) for p in ("ABD", "BIST")}
    out["y1_n_q"] = X1.n.quantile([0.1, 0.5, 0.9]).tolist()
    durum = X1.ek.astype(str).str.split(";").str[0]
    out["y1_bolgesiz"] = float((durum == "AL_BOLGESIZ").mean())
    X3 = Xs["Y3"]
    out["y3_n_q"] = X3.n.quantile([0.1, 0.5, 0.9]).tolist()
    out["y3_n20"] = float((X3.n == 20).mean()); out["y3_n60"] = float((X3.n == 60).mean())
    out["y3_dd"] = {(p, q): yp_hucre(J, "Y3", p, q).get("dd_med") for p, q in YP_KARAR}
    out["y1_dd"] = yp_hucre(J, "Y1", "ABD", "2023").get("dd_med")
    out["y3_st"] = {(p, q): yp_hucre(J, "Y3", p, q) for p, q in YP_KARAR}
    X4 = Xs["Y4"]
    out["y4_pay"] = len(X4) / len(X1)
    out["y4_haf0"] = float((X4.hafiza == 0).mean())
    out["y4_haf1"] = float((X4.hafiza >= 1).mean())
    X5 = Xs["Y5"]
    out["y5_n_q"] = X5.n.quantile([0.1, 0.5, 0.9]).tolist()
    out["y5_n30"] = float((X5.n <= 30).mean())
    out["y5_bant_med"] = float((X5.tavan / X5.hat - 1).median())
    out["y5_bant6"] = float(((X5.tavan / X5.hat - 1) <= 0.06).mean())
    return out


def yp_degerlendirme(S: Sayfa, J: Dict[str, Any], C: Dict[str, Any]) -> None:
    fig = S.yeni("Birlikte değerlendirme: kodun olası yanlışları ve Cemal'e 5 soru",
                 "Sayılar satır dosyalarının sayımı ve sonuc.json; şüpheler iş tanımında yazılı olanlar.")
    st = C["y3_st"]
    a23, a24 = st[("ABD", "2023")], st[("ABD", "2024-26")]
    h1 = yp_hucre(J, "Y1", "ABD", "2024-26")
    sol = [
        ("1. Eşler oynaklıkla eşlenmedi.",
         [f"Eş = aynı gün, aynı momentum x likidite kovası, aynı stop uzaklığı. Oynak hisse hem hedefe hem stopa sık değer.",
          f"Y3 ABD 2023: stop önce {_yz(a23['st5_p_olay'])} / eş {_yz(a23['st5_p_ref'])} (KAT {_sy(a23['st5_kat'])}); "
          f"ABD 2024-26: {_yz(a24['st5_p_olay'])} / {_yz(a24['st5_p_ref'])} (KAT {_sy(a24['st5_kat'])}).",
          f"Y3 stop uzaklığı medyanı {_yz(C['y3_dd'][('ABD', '2023')])} (Y1: {_yz(C['y1_dd'])}): daha geniş, daha oynak yapılar."]),
        ("2. Y1 bölgeleri çok sık.",
         [f"Ham S6 AL günü (tekilleştirme öncesi): ABD {_bin(C['y1_ham']['ABD'])} / {_bin(C['hisse_yil']['ABD'])} hisse-yıl = "
          f"{_sy(C['y1_ham']['ABD'] / C['hisse_yil']['ABD'], 1)} / yıl; BIST {_bin(C['y1_ham']['BIST'])} / {_bin(C['hisse_yil']['BIST'])} = "
          f"{_sy(C['y1_ham']['BIST'] / C['hisse_yil']['BIST'], 1)} / yıl.",
          f"60 günde tekil olaylar: hisse-yıl başına medyan {_sy(C['y1_hy_med']['ABD'], 0)} (ABD), en çok {C['y1_hy_max']['ABD']}. "
          f"Bölge boyu medyan {_sy(C['y1_n_q'][1], 0)} bar, %10'u <= {_sy(C['y1_n_q'][0], 0)} bar.",
          f"Y1 KAT5 ABD 2024-26 {_sy(h1['h5_kat'])}: eşlerden farksız; kutu her küçük dalgada oluşuyor olabilir."]),
        ("3. Y3 kazan tanımı yalnız sayısal uyum.",
         [f"Eğri katsayısı a > 0 (yalnız işaret), en büyük tutan pencere seçilir. Pencere medyanı {_sy(C['y3_n_q'][1], 0)} bar; "
          f"alt sınırdaki (20 bar) pay {_yz(C['y3_n20'], 0)}, üst sınırdaki (60 bar) pay {_yz(C['y3_n60'], 0)}.",
          "Görsel 'kazan' (simetrik çanak, yeterli derinlik) şartı yok; V dibi ya da tek iğne de geçebilir."]),
        ("4. Y4 hafıza tanımı zayıf.",
         [f"Y4 olay sayısı / Y1 olay sayısı = {_yz(C['y4_pay'], 0)}; Y4 içinde hafıza = 0 olan pay {_yz(C['y4_haf0'], 0)} "
          f"(geçmişte sonucu bilinen taban yok ya da artı / eksi eşit).",
          f"Hafıza >= +1 ('güvenilir', D8 sözü) olan pay yalnız {_yz(C['y4_haf1'], 0)}; Y4 büyük ölçüde Y1'in kendisi."]),
        ("5. Y5 tavan tanımı Cemal'in düz tavanından geniş.",
         [f"Kod: 8-70 bar, bant <= %12. Ders D2: 10-30 mum düz tepe; ters oluşum çıkışı bant <= %6.",
          f"Y5 bölge boyu medyanı {_sy(C['y5_n_q'][1], 0)} bar (30 bar ve altı pay {_yz(C['y5_n30'], 0)}); bant (tavan / dip - 1) medyanı "
          f"{_yz(C['y5_bant_med'])}; bandı %6 ve altı olan pay {_yz(C['y5_bant6'], 0)}.",
          "D9 'büyük kırmızı SAT mumu' (mum boyu >= 1,5 x bölge medyanı) şartı kodda yok; her %2'lik kopuş SAT sayılıyor."]),
    ]
    y = 0.875
    for bas, govde in sol:
        fig.text(0.03, y, bas, fontsize=9.6, fontweight="bold", va="top")
        y -= 0.026
        for g in govde:
            fig.text(0.045, y, g, fontsize=8.2, va="top")
            y -= 0.024
        y -= 0.008
    y -= 0.004
    fig.text(0.03, y, "CEMAL'E 5 SORU (cevap grafik sayfalarındaki 'Cemal: ____' satırına ya da buraya)", fontsize=10, fontweight="bold", va="top",
             color="#1f4e9c")
    y -= 0.03
    sorular = [
        "S1. Y1 örneklerinde kodun çizdiği taban (mavi alan, hat çizgisi) senin tabanın mı? Değilse fark nerede: boy mu, bant mı, düşüş sonrası mı?",
        "S2. Y3'ün kazanı senin kazanın mı? Çanak yeterince derin / simetrik mi, sağ kenar dönüşü doğru yerde mi?",
        "S3. Takip stopu kuralı böyle mi kalsın (+%5'te giriş x 1,02, +%10'da giriş x 1,07, en yüksek kapanış x 0,93)?",
        "S4. Hedef +%5 kapanışla mı sayılsın, gün içi High ile mi? (Şimdi karar kapanışla; High bilgi sütununda.)",
        "S5. Y5 SAT mumu doğru mu: düz tavandan %2 aşağı kapanış yeter mi, yoksa büyük kırmızı mum (D9) şart mı?",
    ]
    for s_ in sorular:
        fig.text(0.045, y, s_, fontsize=8.6, va="top")
        y -= 0.026
    S.kaydet(fig)


# ================================================================ 6) SON SAYFA
def yp_son(S: Sayfa, J: Dict[str, Any]) -> None:
    fig = S.yeni("Veri sınırları, kayıt ve sıradaki 3 deneme")
    k = J["kos"][0]
    vn = J.get("veri_not", {})
    y = _metin(fig, 0.03, 0.89, ["VERİ SINIRLARI"], font=11, fontweight="bold")
    y = _metin(fig, 0.04, y + 0.004, [
        f"· Hayatta kalma: evren bugün işlem gören hisseler (ABD {vn.get('ABD', ['', '', '', ''])[-1]}, Avrupa {vn.get('AVR', ['', ''])[-1]}, "
        f"BIST {vn.get('BIST', ['', ''])[-1]}).",
        "  Batan / kottan çıkan yok: hedef payı yukarı, stop payı aşağı yanlı okunur (eşler ve plasebo da aynı evrenden).",
        "· Komisyon ve kayma yok; stop çıkışı ertesi açılış. Getiri = komisyonsuz fiyat değişimi (bilgi).",
        "· Fon krizi kesiği 31.08.2026: 15 günlük pencere bu tarihi aşan olay ölçülmedi.",
        "· ABD ek evreni (k34) yok: ABD yalnız V_ABD. Avrupa'da olay verisi yok; yalnız fiyat-hacim.",
        "· Takip stopu geçici kural (Cemal: 'son kural değil').",
    ], font=9.2, aralik=0.03)
    y = _metin(fig, 0.03, y - 0.01, ["KAYIT (ön kayıt ölçümden önce)"], font=11, fontweight="bold")
    y = _metin(fig, 0.04, y + 0.004, [
        f"· Ön kayıt: ON_KAYIT.md {k['kapi']['onkayit_zaman']}; commit {k['kapi']['git_onkayit']['commit'][:10]} ({k['kapi']['git_onkayit']['commit_zamani']}).",
        f"· Koşu: {k['zaman_utc']}; ölçüm commit'i 8adc0b7 (RAPOR.md, sonuc.json, olay_Y1..Y5.csv.gz).",
        "· Geleceğe bakma denetimi: her deneme x pazar 5 rastgele olay kesik veriyle yeniden üretildi; 75 / 75 tuttu (sonuc.json).",
    ], font=9.2, aralik=0.03)
    y = _metin(fig, 0.03, y - 0.01, ["GÜÇ NOTU"], font=11, fontweight="bold")
    guc_sat = []
    for d in YP_DENEME:
        for p, q in YP_KARAR:
            h = yp_hucre(J, d, p, q)
            if 300 <= h["n"] < 1000:
                guc_sat.append(f"{d} {YP_PAZAR_AD[p]} {q} (n {h['n']}, güç {_yz(h.get('guc'), 0)})")
    y = _metin(fig, 0.04, y + 0.004, [
        "· n 300-999 olan karar hücreleri gerçek bir KAT 1,25'i %80 olasılıkla yakalayamıyor (güç tablosu); bu hücreler ÖLÇÜLEMEDİ kalıyor:",
        "  " + "; ".join(guc_sat[:3]),
        "  " + "; ".join(guc_sat[3:]),
        "· n < 300 hücrelerde (Y2 tamamı, Y5 Avrupa) güç %2-%11: sonuç her iki yönde de söylenemez.",
    ], font=9.0, aralik=0.029)
    y = _metin(fig, 0.03, y - 0.01, ["SIRADAKİ 3 DENEME (sonuç görülmeden, sabit eşikle ön kayda yazılacak)"], font=11, fontweight="bold")
    _metin(fig, 0.04, y + 0.004, [
        "1. OYNAKLIK KOVASI: eşler ayrıca aynı oynaklık üçlüsünden (ör. 20 gün ortalama mum boyu / fiyat) seçilir; Y3 ve Y5 bu eşle yeniden ölçülür.",
        "   Amaç: Y3'ün hedef fazlası oynaklıktan mı geliyor, yapıdan mı, ayrılsın.",
        "2. Y5 n BÜYÜTME: Y5 karar hücrelerinde n 86-934; ABD ek evreni / daha uzun Avrupa verisi ile n >= 1.000'e ya da güç %80'e çıkarılır.",
        "   BIST 2024-26'daki TUTAR (bilgi hücresi, n 257) ancak karar hücrelerinde tekrar ederse anlam taşır.",
        "3. Y1 + D4 DÖNÜŞ: Y1 olaylarına Cemal'in 'dönüşü görmeden giriş yok' şartı eklenir (son 5 bar dibi > önceki 10 bar dibi VE",
        "   son kapanış > son 10 barın orta seviyesi). Y1 tek başına eşlerden farksız; dönüş şartı ayrım yapıyor mu, ölçülür.",
    ], font=9.0, aralik=0.029)
    S.kaydet(fig)


# ================================================================ ANA AKIŞ
def yp_uret(cikti: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or YP_YOL["pdf"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42, "axes.unicode_minus": False})
    J = yp_sonuc()
    Xs = {d: yp_satir(d) for d in YP_DENEME}
    V = yp_veri(["ABD", "BIST"])
    ornekler: List[Dict[str, Any]] = []
    gecici = cikti + ".gecici"
    try:
        with PdfPages(gecici) as pdf:
            S = Sayfa(pdf)
            yp_kapak(S, J)
            yp_olasilik(S, J)
            for d in YP_DENEME:
                yp_deneme_sayfa(S, J, d, Xs[d])
                sec = yp_ornek_sec(Xs[d], V)
                if len(sec) != YP_AYAR["ornek_hedef"] + YP_AYAR["ornek_stop"]:
                    yplog.warning("%s: %d örnek seçildi (beklenen 6)", d, len(sec))
                for i, (tur, r) in enumerate(sec, 1):
                    ornekler.append(yp_ornek_sayfa(S, d, i, tur, r, V))
            C = yp_sayimlar(J, Xs, V)
            yp_degerlendirme(S, J, C)
            yp_son(S, J)
            md = pdf.infodict()
            md["Title"] = "YAPI_HEDEF sonuç (17.11.2026)"
            md["Subject"] = "Y1-Y5 yapı denemeleri: hedef +%5 / +%10 stop'tan önce 15 gün"
            sayfa = S.no
        os.replace(gecici, cikti)
    except Exception:
        if os.path.exists(gecici):
            os.remove(gecici)
        raise
    mb = os.path.getsize(cikti) / 1e6
    if mb >= YP_AYAR["azami_mb"]:
        raise YPHata(f"PDF {mb:.1f} MB >= {YP_AYAR['azami_mb']} MB")
    lo, hi = YP_AYAR["sayfa_aralik"]
    if not lo <= sayfa <= hi:
        yplog.warning("sayfa sayısı %d, beklenen %d-%d", sayfa, lo, hi)
    yplog.info("PDF yazıldı: %s (%d sayfa, %.2f MB)", cikti, sayfa, mb)
    return {"pdf": cikti, "sayfa": sayfa, "mb": mb, "ornek": ornekler}


# ================================================================ ÇAKIŞMA KAPISI ve KOMUT
def _cakisma_kontrol_yp(_once=_CK_ONCE_YP, _dosya="yapi_hedef_pdf.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_YP", "_CK_KAYIT", "_cakisma_kontrol_yp", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "argparse", "matplotlib", "plt", "PdfPages", "Rectangle", "annotations",
           "Any", "Dict", "List", "Optional", "Tuple", "_yz", "_sy")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_yp()

if __name__ == "__main__" and "get_ipython" not in globals():
    ap = argparse.ArgumentParser(description="YAPI_HEDEF sonuç PDF'i")
    ap.add_argument("--cikti", default=None)
    a_ = ap.parse_args()
    try:
        R_ = yp_uret(a_.cikti)
        print(f"PDF {R_['pdf']} · {R_['sayfa']} sayfa · {R_['mb']:.2f} MB")
        for o in R_["ornek"]:
            print(f"{o['deneme']} {o['tur']:5s} {o['pazar']:4s} {o['sembol']:10s} sinyal {o['tarih']} giriş {o['giris']} "
                  f"h5 {o['h5']:.0f} h10 {o['h10']:.0f} st5 {o['st5']:.0f} k5 {o['k5']} kst {o['kst']} çıkış {o['cikis_bar']} {o['cikis_tur']} "
                  f"getiri {o['getiri']:+.4f}")
    except YPHata as ex:
        yplog.error("%s", ex)
        sys.exit(1)
