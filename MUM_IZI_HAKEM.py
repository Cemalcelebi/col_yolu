"""MUM_IZI_HAKEM — MUM_IZI EK 10 ikinci adım: görsel hakem için aday PDF'leri ve hakemin seçtiklerinden Cemal'e onay PDF'i (26 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI10_IS_TANIMI.md (commit 6b3aba8) + ana modelin ikinci adım görevi. Bu modül YALNIZ çizim ve derleme altyapısıdır:
hakemlik yapmaz, getiri / sonrası hesaplamaz. Adaylar MUM_IZI8 evren taramasının v5M VAR olaylarından (evren içi, tekil) rastgele seçilir.
Eski kodlar değişmez (içe alınır). Veri <= 2022-12-31; KASA açılmaz.

Komut:  python MUM_IZI_HAKEM.py aday [--parti 1|2]                         1: 300 aday (hakem_aday), 2: 600 yeni aday (hakem_aday2); 50'şer sayfa + anahtar
        python MUM_IZI_HAKEM.py onay --hakem <json1> [<json2> ...] [--aday KLASÖR] [--kapak "<metin>"] [--ad <önek>] [--cikti KLASÖR]
                                                                           hakemin EVET'lerinden MUM_IZI10_ONAY.pdf + mum_izi10_onay_anahtar.json
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_HK = {k: id(v) for k, v in globals().items()}

import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_HK = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_HK not in sys.path:
    sys.path.insert(0, KOK_HK)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ)

hklog = logging.getLogger("col.mum_izi_hakem")
if not hklog.handlers:
    _hk_h = logging.StreamHandler(sys.stderr)
    _hk_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_hakem: %(message)s", "%H:%M:%S"))
    hklog.addHandler(_hk_h)
    hklog.setLevel(logging.INFO)
    hklog.propagate = False


class HKHata(RuntimeError):
    """Durdurucu hata: şema / mühür / sayı / kesik."""


HK_SURUM = "MUM_IZI_HAKEM v1.0 (2026-11-26): hakem aday PDF'leri + onay derleme"
HK_YOL = {"cikti": MI.MI_YOL["cikti"], "aday": os.path.join(MI.MI_YOL["cikti"], "hakem_aday"), "kod": os.path.join(KOK_HK, "MUM_IZI_HAKEM.py"),
          "ham8": "/tmp/mum_izi/v5/tarama_ham.json", "tarama8": os.path.join(MI.MI_YOL["cikti"], "mum_izi8_tarama.json"),
          "anahtarlar": [os.path.join(MI.MI_YOL["cikti"], f) for f in ("mum_izi4_onay_anahtar.json", "mum_izi6_anahtar.json", "mum_izi8_onay_anahtar.json",
                                                                       "mum_izi9_onay_anahtar.json")]}
HK_ESIK: Dict[str, Any] = {
    "surum": "HK-1.0", "kural": "R4+M",
    "aday": {"tohum": 25112101, "gunluk": 150, "haftalik": 150, "bist_tavan": 30, "dosya_sayfa": 50,
             "secim": "MUM_IZI8 taramasının v5M ('R4+M') VAR, evren içi, tekil olayları; önceki dört setin (MUM_IZI4 / 6 / 8 / 9) hisseleri hariç; önce haftalık "
                      "sonra günlük, her dilimde olaylar (sembol, tarih) sırasına dizilip tohumla karıştırılır ve sırayla alınır: hisse başına bir (iki dilim "
                      "birlikte), BIST dilim başına <= 30; 300 sayfa tohumla karışık sıraya (günlük / haftalık karışık) dizilir, 1-300 numaralanır, 50'şer sayfalık 6 dosya",
             "sayfa": "MUM_IZI4_ONAY düzeni: solda küçük 'Senin kalıbın', sağda bölge (öncesi 15 mum, Bollinger 20 + SMA20, bölge turuncu kutu, bölge sonunda kesik), "
                      "başlık 'Sayfa N: bulunan bölge (günlük / haftalık mum)'; kodun okuması YOK; ✓ / × kutuları YOK; hisse / tarih / sonrası YOK"},
    "onay": {"tohum": 25112103, "hedef": 24, "gunluk": 12, "haftalik": 12, "en_az": 8,
             "secim": "hakem dosyalarındaki 'karar' == EVET sayfalar; >= 24 ise RASTGELE 24 (günlük 12 + haftalık 12; bir dilim yetmezse öteki dilimden rastgele "
                      "tamamlanır); < 24 ise hepsi; < 8 ise DUR. Sayfa sırası tohumla karışık; yeni sayfa numaraları 2'den",
             "sayfa": "kapak (tek sayfa) + seçilenler MUM_IZI4_ONAY düzeniyle (✓ benziyor / ✗ benzemiyor kutuları VAR); hisse / tarih / sonrası yok",
             "hakem_sema": {"sayfalar": {"<sayfa no>": {"karar": "EVET | HAYIR", "puan": "0-10", "gerekce": "metin"}}}},
}
# 2. parti (EK 12): HK_ESIK'e eklenmedi ki 1. partinin anahtarındaki esik_sha geçerli kalsın
HK_ESIK_P2: Dict[str, Any] = {
    "surum": "HK-P2-1.0", "tohum": 25112121, "gunluk": 300, "haftalik": 300, "bist_oran": 0.20, "dosya_sayfa": 50, "eksik_izin": True,
    "secim": "MUM_IZI8 taramasının v5M ('R4+M') VAR, evren içi, tekil olayları; önceki dört setin (MUM_IZI4 / 6 / 8 / 9) ve 1. partinin (hakem_aday, 300 aday) "
             "hisseleri hariç; önce haftalık sonra günlük, her dilimde (sembol, tarih) sırasına dizilip tohumla karıştırılır ve sırayla alınır: hisse başına bir "
             "(iki dilim birlikte), BIST dilim başına en çok %20 (döngüde hedefin %20'si tavan; sonunda BIST payı alınan sayının %20'sini aşarsa son alınan BIST "
             "adayları çıkarılır); bir dilimde uygun hisse yetmezse olabildiği kadar (sayı yazılır); bütün sayfalar tohumla karışık sıraya, 1'den kesintisiz, 50'şer "
             "sayfalık dosyalar",
    "sayfa": "1. partiyle aynı (kısa sayfa; 'Senin kalıbın' + bölge turuncu kutu; kutusuz; hisse / tarih / sonrası yok)"}
HK_PARTI: Dict[int, Dict[str, Any]] = {
    1: {"esik": HK_ESIK["aday"], "klasor": os.path.join(MI.MI_YOL["cikti"], "hakem_aday"), "onek": "mum_izi10_aday", "baslik": "MUM_IZI10 aday", "onceki": []},
    2: {"esik": HK_ESIK_P2, "klasor": os.path.join(MI.MI_YOL["cikti"], "hakem_aday2"), "onek": "mum_izi12_aday", "baslik": "MUM_IZI12 aday",
        "onceki": [os.path.join(MI.MI_YOL["cikti"], "hakem_aday", "mum_izi10_aday_anahtar.json")]}}
HK_KAPAK = ("Bu kez bölgeleri formül değil, senin işaretlerinden öğrenen bir görsel hakem seçti. Hakemi görmediği 56 sayfanda sınadım: benziyor dediği 5 "
            "sayfanın 3'üne sen de benziyor demiştin. {M} adaya baktı, {N} tanesini seçti; {BUNLAR}. Benziyorsa ✓, benzemiyorsa × kutusuna X koy; yanlış "
            "bulduğun yeri daire içine al.")


def _hk_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or HK_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# ================================================================ 1) ADAY SEÇİMİ
def hk_olaylar() -> List[Dict[str, Any]]:
    """MUM_IZI8 taramasının v5M olayları (ham dosya, sha mum_izi8_tarama.json ile denetlenir)."""
    J = json.load(open(HK_YOL["tarama8"], encoding="utf-8"))
    if not os.path.exists(HK_YOL["ham8"]):
        raise HKHata(f"MUM_IZI8 tarama ham dosyası yok: {HK_YOL['ham8']} (MUM_IZI_V5.py tarama ile yeniden üretilir)")
    if MI._mi_sha(HK_YOL["ham8"]) != J["ham_sha"]:
        raise HKHata("MUM_IZI8 tarama ham dosyası mühürle uyuşmuyor")
    return json.load(open(HK_YOL["ham8"], encoding="utf-8"))["olay"][HK_ESIK["kural"]]


def hk_haric(parti: int = 1) -> set:
    h: set = set()
    for y in HK_YOL["anahtarlar"] + HK_PARTI[parti]["onceki"]:
        if not os.path.exists(y):
            raise HKHata(f"hariç listesi için anahtar yok: {y}")
        h |= {r["sembol"] for r in json.load(open(y, encoding="utf-8"))["sayfalar"]}
    return h


def hk_aday_sec(olay: List[Dict[str, Any]], haric: set, G: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    G = G or HK_ESIK["aday"]; rng = np.random.default_rng(G["tohum"]); sec: List[Dict[str, Any]] = []; gor = set(haric)
    for z in ("haftalik", "gunluk"):
        h = sorted([o for o in olay if o["zaman"] == z and o["evren"]], key=lambda o: (o["sembol"], o["tarih"])); n = 0; bist = 0; dz: List[Dict[str, Any]] = []
        tavan = int(G["bist_tavan"]) if "bist_tavan" in G else int(np.floor(G["bist_oran"] * G[z] + 1e-9))
        for i in rng.permutation(len(h)):
            o = h[int(i)]
            if o["sembol"] in gor or (o["pazar"] == "BIST" and bist >= tavan):
                continue
            dz.append(dict(o)); gor.add(o["sembol"]); n += 1; bist += int(o["pazar"] == "BIST")
            if n >= G[z]:
                break
        if "bist_oran" in G:                                   # BIST payı alınan sayının %20'sini aşmasın (dilim yetmediyse)
            while bist > int(np.floor(G["bist_oran"] * len(dz) + 1e-9)):
                j = max(i for i, o in enumerate(dz) if o["pazar"] == "BIST"); gor.discard(dz[j]["sembol"]); dz.pop(j); bist -= 1
        if len(dz) < G[z] and not G.get("eksik_izin", False):
            raise HKHata(f"{z}: yalnız {len(dz)} aday bulundu (hedef {G[z]})")
        sec += dz
    p = rng.permutation(len(sec))
    return [dict(sec[i], sayfa=j + 1) for j, i in enumerate(p)]


# ================================================================ 2) ÇİZİM
def _hk_sayfa(fig, d: pd.DataFrame, r: Dict[str, Any], a: Dict[str, np.ndarray], sayfa: int, kutular: bool) -> None:
    from matplotlib.patches import Rectangle
    t = d.index.get_loc(pd.Timestamp(r["tarih"])); m = int(r["m"]); once = int(MV.MV_ESIK["onay"]["once"]); i0 = max(0, t - m + 1 - once)
    BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(i0, t + 1)
    # kutulu (onay) sayfa: MUM_IZI4_ONAY yerleşimi aynen (A4); kutusuz (aday) sayfa: aynı öğeler, alt boşluk yok (küçük sayfa)
    yer = ([0.04, 0.6, 0.3, 0.28], [0.38, 0.45, 0.58, 0.45], 0.4) if kutular else ([0.04, 0.42, 0.3, 0.45], [0.38, 0.14, 0.58, 0.76], 0.3)
    MV._mv_ciz(fig.add_axes(yer[0]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
    MV._mv_ciz(fig.add_axes(yer[1]), *(d[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl], BA[sl],
               (t - m + 1 - i0, t - i0), f"Sayfa {sayfa}: bulunan bölge ({'haftalık' if r['zaman'] == 'haftalik' else 'günlük'} mum)")
    fig.text(0.04, yer[2], "Turuncu kutu = bölge; sağ kenar = bölgenin sonu (sonrası gösterilmiyor).\nMor = Bollinger 20 ve SMA20 (kesik).", fontsize=9, va="top")
    if kutular:
        ax = fig.add_axes([0.1, 0.12, 0.8, 0.22]); ax.axis("off")
        for xx, txt in ((0.0, "✓  benziyor"), (0.55, "✗  benzemiyor")):
            ax.add_patch(Rectangle((xx, 0.1), 0.42, 0.8, fill=False, linewidth=3, transform=ax.transAxes))
            ax.text(xx + 0.21, 0.5, txt, ha="center", va="center", fontsize=22, transform=ax.transAxes)


def _hk_bas(d: pd.DataFrame, r: Dict[str, Any]) -> str:
    t = d.index.get_loc(pd.Timestamp(r["tarih"])); return str(d.index[t - int(r["m"]) + 1].date())


def hk_aday(cikti: Optional[str] = None, parti: int = 1) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    if parti not in HK_PARTI:
        raise HKHata(f"bilinmeyen parti {parti}")
    PT = HK_PARTI[parti]; G = PT["esik"]
    kl = cikti or PT["klasor"]; os.makedirs(kl, exist_ok=True); ya = os.path.join(kl, f"{PT['onek']}_anahtar.json")
    if os.path.exists(ya):
        raise HKHata("aday anahtarı zaten var")
    sec = hk_aday_sec(hk_olaylar(), hk_haric(parti), G)
    if max(pd.Timestamp(r["tarih"]) for r in sec) > MI.MI_KESIK:
        raise HKHata("KESİK AŞIMI")
    a = MV.mv_sablon()["tam"]["ohlc"]; Vc: Dict[Any, Any] = {}; dosyalar = []; anah = []; ds = int(G["dosya_sayfa"])
    for f in range(int(np.ceil(len(sec) / ds))):
        y = os.path.join(kl, f"{PT['onek']}_{f + 1}.pdf"); dosyalar.append(y)
        with PdfPages(y, metadata={"Title": f"{PT['baslik']} {f + 1}", "CreationDate": None, "ModDate": None}) as pdf:
            for r in sec[f * ds:(f + 1) * ds]:
                k = (r["zaman"], r["pazar"])
                if k not in Vc:
                    Vc[k] = MV.mv_veri(*k)
                d = Vc[k][r["sembol"]]
                fig = plt.figure(figsize=(8.3, 6.2)); _hk_sayfa(fig, d, r, a, r["sayfa"], kutular=False); pdf.savefig(fig); plt.close(fig)
                anah.append({"sayfa": r["sayfa"], "dosya": os.path.basename(y), "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"],
                             "bolge_bas": _hk_bas(d, r), "bolge_son": r["tarih"], "pencere": int(r["m"]), "k": int(r["k"]), "v1_S": r["S"]})
        hklog.info("%s yazıldı", y)
    X = pd.DataFrame(anah)
    J = {"not": "MÜHÜRLÜ: sayfa -> hisse / bölge tarihleri; PDF'e girmez", "surum": HK_SURUM, "parti": parti, "esik_sha": _hk_sha(G if parti != 1 else None),
         "tohum": G["tohum"], "hedef": {"gunluk": G["gunluk"], "haftalik": G["haftalik"]}, "n": len(anah),
         "kaynak": {"tarama8_ham_sha": MI._mi_sha(HK_YOL["ham8"]), "kural": HK_ESIK["kural"]},
         "sayim": {f"{z}|{p}": int(v) for (z, p), v in X.groupby(["zaman", "pazar"]).size().items()},
         "dosya_sha": {os.path.basename(y): MI._mi_sha(y) for y in dosyalar}, "sayfalar": anah}
    MI._mi_jyaz(ya, J, f"aday anahtar parti {parti}")
    return J


# ================================================================ 3) ONAY DERLEME
def hk_hakem_oku(yollar: List[str]) -> Dict[int, Dict[str, Any]]:
    """Hakem dosyaları: {"sayfalar": {"<no>": {"karar": EVET | HAYIR, "puan": 0-10, "gerekce": metin}}}; birden çok dosya birleşir; çelişki / şema dışı -> DUR."""
    out: Dict[int, Dict[str, Any]] = {}
    for y in yollar:
        J = json.load(open(y, encoding="utf-8"))
        if not isinstance(J, dict) or not isinstance(J.get("sayfalar"), dict):
            raise HKHata(f"hakem şeması: 'sayfalar' yok ({y})")
        for k, v in J["sayfalar"].items():
            if not str(k).strip().isdigit() or not isinstance(v, dict):
                raise HKHata(f"hakem şeması: sayfa {k!r} ({y})")
            kr = str(v.get("karar", "")).strip().replace("İ", "I").upper()
            if kr not in ("EVET", "HAYIR"):
                raise HKHata(f"hakem şeması: sayfa {k} karar {v.get('karar')!r} ({y})")
            try:
                pu = float(v.get("puan"))
            except (TypeError, ValueError) as ex:
                raise HKHata(f"hakem şeması: sayfa {k} puan {v.get('puan')!r}") from ex
            if not 0 <= pu <= 10:
                raise HKHata(f"hakem şeması: sayfa {k} puan {pu} (0-10 dışı)")
            n = int(k); kayit = {"karar": kr, "puan": pu, "gerekce": str(v.get("gerekce", ""))}
            if n in out and out[n]["karar"] != kr:
                raise HKHata(f"hakem dosyaları çelişiyor: sayfa {n}")
            out[n] = kayit
    return out


def hk_onay_sec(evet: List[Dict[str, Any]], G: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """EVET sayfaları (zaman alanlı) -> seçim: >= hedef ise rastgele hedef (günlük / haftalık 12'şer, eksik dilim ötekinden), < hedef ise hepsi; < en_az -> DUR."""
    G = G or HK_ESIK["onay"]; rng = np.random.default_rng(G["tohum"]); ev = sorted(evet, key=lambda r: r["sayfa"])
    if len(ev) < G["en_az"]:
        raise HKHata(f"hakem EVET sayısı {len(ev)} < {G['en_az']}: onay seti kurulmadı")
    if len(ev) <= G["hedef"]:
        sec = list(ev)
    else:
        sec = []; kalan = []
        for z in ("gunluk", "haftalik"):
            h = [r for r in ev if r["zaman"] == z]; p = rng.permutation(len(h)); al = [h[int(i)] for i in p[:G[z]]]; sec += al
            kalan += [h[int(i)] for i in p[G[z]:]]
        if len(sec) < G["hedef"]:
            kalan = sorted(kalan, key=lambda r: r["sayfa"]); p = rng.permutation(len(kalan)); sec += [kalan[int(i)] for i in p[:G["hedef"] - len(sec)]]
    p = rng.permutation(len(sec))
    return [dict(sec[i], yeni_sayfa=j + 2) for j, i in enumerate(p)]


def hk_aday_anahtar_bul(klasor: str) -> str:
    """Klasördeki TEK '*anahtar*.json' dosyası (aday anahtarı)."""
    if not os.path.isdir(klasor):
        raise HKHata(f"aday klasörü yok: {klasor}")
    a = sorted(f for f in os.listdir(klasor) if "anahtar" in f and f.endswith(".json"))
    if len(a) != 1:
        raise HKHata(f"aday klasöründe tek anahtar json'u olmalı, bulunan: {a}")
    return os.path.join(klasor, a[0])


def hk_kapak_metni(kapak: Optional[str], M: int, N: int, K: int) -> str:
    """--kapak verilmişse aynen ({M} bakılan aday, {N} hakem EVET, {K} PDF'e giren sayfa yer tutucuları doldurulur); yoksa eski kapak."""
    if kapak is not None:
        return kapak.replace("{M}", str(M)).replace("{N}", str(N)).replace("{K}", str(K))
    return HK_KAPAK.format(M=M, N=N, BUNLAR="bunlar onlar" if N <= HK_ESIK["onay"]["hedef"] else f"içlerinden rastgele {K}'ü bunlar")


def hk_onay(hakem: List[str], cikti: Optional[str] = None, aday_klasor: Optional[str] = None, kapak: Optional[str] = None,
            ad: Optional[str] = None) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    cikti = cikti or HK_YOL["cikti"]
    y = os.path.join(cikti, f"{ad}_ONAY.pdf" if ad else "MUM_IZI10_ONAY.pdf"); ya = os.path.join(cikti, f"{ad}_onay_anahtar.json" if ad else "mum_izi10_onay_anahtar.json")
    if os.path.exists(y) or os.path.exists(ya):
        raise HKHata(f"onay PDF / anahtar zaten var: {y}")
    ay = hk_aday_anahtar_bul(aday_klasor or HK_YOL["aday"])
    A = json.load(open(ay, encoding="utf-8")); Ad = {int(r["sayfa"]): r for r in A["sayfalar"]}
    H = hk_hakem_oku(hakem); yabanci = sorted(set(H) - set(Ad))
    if yabanci:
        raise HKHata(f"hakem dosyasında aday listesinde olmayan sayfalar: {yabanci[:10]}")
    evet = [dict(Ad[n], hakem_puan=v["puan"], hakem_gerekce=v["gerekce"]) for n, v in H.items() if v["karar"] == "EVET"]
    sec = hk_onay_sec(evet); M = len(H); N = len(evet)
    a = MV.mv_sablon()["tam"]["ohlc"]; Vc: Dict[Any, Any] = {}; os.makedirs(cikti, exist_ok=True)
    with PdfPages(y, metadata={"Title": f"{ad or 'MUM_IZI10'} onay", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.06, 0.95, "GÖRSEL HAKEMİN SEÇTİĞİ BÖLGELER", fontsize=16, weight="bold")
        fig.text(0.06, 0.88, hk_kapak_metni(kapak, M, N, len(sec)), fontsize=13, va="top", wrap=True)
        MV._mv_ciz(fig.add_axes([0.25, 0.2, 0.5, 0.35]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
        pdf.savefig(fig); plt.close(fig)
        for r in sorted(sec, key=lambda r: r["yeni_sayfa"]):
            k = (r["zaman"], r["pazar"])
            if k not in Vc:
                Vc[k] = MV.mv_veri(*k)
            d = Vc[k][r["sembol"]]; rr = {"tarih": r["bolge_son"], "m": r["pencere"], "zaman": r["zaman"]}
            if _hk_bas(d, rr) != r["bolge_bas"]:
                raise HKHata(f"aday sayfa {r['sayfa']}: bölge başı anahtarla uyuşmuyor")
            fig = plt.figure(figsize=(8.3, 11.7)); _hk_sayfa(fig, d, rr, a, r["yeni_sayfa"], kutular=True); pdf.savefig(fig); plt.close(fig)
    K = {"not": "MÜHÜRLÜ: yeni sayfa -> aday sayfası / hakem puanı / hisse / tarihler; PDF'e girmez", "surum": HK_SURUM, "tohum": HK_ESIK["onay"]["tohum"],
         "hakem_dosyalari": {os.path.basename(h): MI._mi_sha(h) for h in hakem}, "aday_anahtari": os.path.basename(ay), "aday_anahtar_sha": MI._mi_sha(ay),
         "kapak": hk_kapak_metni(kapak, M, N, len(sec)), "aday_bakilan": M, "hakem_evet": N, "secilen": len(sec),
         "secilen_zaman": pd.Series([r["zaman"] for r in sec], dtype=object).value_counts().to_dict(), "pdf_sha": MI._mi_sha(y),
         "sayfalar": [{"yeni_sayfa": r["yeni_sayfa"], "aday_sayfa": r["sayfa"], "hakem_puan": r["hakem_puan"], "hakem_gerekce": r["hakem_gerekce"], "zaman": r["zaman"],
                       "pazar": r["pazar"], "sembol": r["sembol"], "bolge_bas": r["bolge_bas"], "bolge_son": r["bolge_son"], "pencere": r["pencere"]}
                      for r in sorted(sec, key=lambda r: r["yeni_sayfa"])]}
    MI._mi_jyaz(ya, K, "onay anahtar 10")
    hklog.info("onay: %d adaya bakıldı, hakem EVET %d, seçilen %d -> %s", M, N, len(sec), y)
    return K


# ================================================================ 4) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_hk(_once=_CK_ONCE_HK, _dosya="MUM_IZI_HAKEM.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_HK",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_hk()


def _hk_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_HAKEM")
    ap.add_argument("komut", choices=["aday", "onay"])
    ap.add_argument("--hakem", nargs="+", default=None, help="hakem json dosyaları (onay)")
    ap.add_argument("--cikti", default=None, help="çıktı klasörü (varsayılan arastirma_cikti/mum_izi; aday için hakem_aday)")
    ap.add_argument("--aday", default=None, help="aday klasörü (onay; içinde tek '*anahtar*.json'; varsayılan arastirma_cikti/mum_izi/hakem_aday)")
    ap.add_argument("--parti", type=int, default=1, help="aday partisi (aday; 1 = hakem_aday, 2 = hakem_aday2)")
    ap.add_argument("--kapak", default=None, help="onay kapak metni ({M} bakılan aday, {N} hakem EVET, {K} PDF'e giren sayfa)")
    ap.add_argument("--ad", default=None, help="onay çıktı öneki: <önek>_ONAY.pdf, <önek>_onay_anahtar.json (varsayılan eski adlar)")
    a = ap.parse_args(argv)
    try:
        if a.komut == "aday":
            J = hk_aday(a.cikti, a.parti); print(json.dumps({"parti": a.parti, "n": J["n"], "sayim": J["sayim"], "tohum": J["tohum"]}, ensure_ascii=False))
        else:
            if not a.hakem:
                raise HKHata("--hakem en az bir dosya ister")
            K = hk_onay(a.hakem, a.cikti, a.aday, a.kapak, a.ad)
            print(json.dumps({k: K[k] for k in ("aday_bakilan", "hakem_evet", "secilen", "secilen_zaman", "tohum")}, ensure_ascii=False))
    except HKHata as ex:
        hklog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_hk_ana())
