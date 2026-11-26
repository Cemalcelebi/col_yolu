"""MUM_IZI_HAKEM — MUM_IZI EK 10 ikinci adım: görsel hakem için aday PDF'leri ve hakemin seçtiklerinden Cemal'e onay PDF'i (26 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI10_IS_TANIMI.md (commit 6b3aba8) + ana modelin ikinci adım görevi. Bu modül YALNIZ çizim ve derleme altyapısıdır:
hakemlik yapmaz, getiri / sonrası hesaplamaz. Adaylar MUM_IZI8 evren taramasının v5M VAR olaylarından (evren içi, tekil) rastgele seçilir.
Eski kodlar değişmez (içe alınır). Veri <= 2022-12-31; KASA açılmaz.

Komut:  python MUM_IZI_HAKEM.py aday [--parti 1|2|3]                       1: 300 aday (hakem_aday), 2: 600 yeni aday (hakem_aday2), 3: 600 yeni aday
                                                                           (hakem_aday3, EK 14); 50'şer sayfa + anahtar
        python MUM_IZI_HAKEM.py onay --hakem <json1> [<json2> ...] [--hakem2 <json>] [--aday KLASÖR] [--kapak "<metin>"] [--ad <önek>] [--cikti KLASÖR]
                                                                           hakemin EVET'lerinden MUM_IZI10_ONAY.pdf + mum_izi10_onay_anahtar.json;
                                                                           --hakem2 ile iki aşamalı seçim (EK 14 A3; HK_ESIK_ONAY2)
        python MUM_IZI_HAKEM.py onay ... --ad <önek> --olcek                    EK 16 İŞ B: aynı set ölçekli (sağda yüzde ekseni, sağlam dikey sınır + kırpma
                                                                           işareti, mum boyu satırı, ✓ / K / × kutuları): <önek>_ONAY_OLCEKLI.pdf +
                                                                           <önek>_onay_olcekli.json; eski PDF / anahtar değişmez
        python MUM_IZI_HAKEM.py ogren [--cikti KLASÖR]                     EK 14 A2: MUM_IZI10 + MUM_IZI12 onay sayfaları Cemal etiket şeridiyle
                                                                           (MUM_IZI14_OGREN.pdf; önce BENZİYOR, sonra KISMEN, sonra BENZEMİYOR)
        python MUM_IZI_HAKEM.py aday --parti 4                            EK 18 A1-A2: mum boyu KAPISI (ORAN <= 0,70) + ölçekli aday sayfaları (hakem_aday4;
                                                                           mum_izi18_aday_*.pdf + anahtar (ORAN, katman) + mum_izi18_havuz_sayim.json)
        python MUM_IZI_HAKEM.py havuz --parti 4                           EK 18 A1: havuz sayımı (yalnız yazdırır)
        python MUM_IZI_HAKEM.py ogren --olcek                              EK 18 A3: MUM_IZI18_OGREN.pdf (MUM_IZI14 ölçekli 17 + MUM_IZI10 / 12 48 bölge,
                                                                           ölçekli yeniden çizim + etiket şeridi)
        python MUM_IZI_HAKEM.py onay --hakem ... --hakem2 <json> --aday arastirma_cikti/mum_izi/hakem_aday4 --ad MUM_IZI18 --olcek
                                                                           EK 18 A4: ölçekli partiden YENİ set (HK-O4; <ad>_ONAY_OLCEKLI.pdf + anahtar + json)
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
HK_SURUM_OLCEK = "EK 16 İŞ B (2026-11-26): onay --olcek"
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
# 3. parti (EK 14 A1): 2. partiyle aynı kural / düzen / katman payları; yalnız tohum ve hariç listesi yeni (HK_ESIK / HK_ESIK_P2 değişmez: eski esik_sha'lar geçerli)
HK_ESIK_P3: Dict[str, Any] = {
    "surum": "HK-P3-1.0", "tohum": 25112131, "gunluk": 300, "haftalik": 300, "bist_oran": 0.20, "dosya_sayfa": 50, "eksik_izin": True,
    "secim": "2. partiyle (HK-P2-1.0) aynı kural: MUM_IZI8 taramasının v5M ('R4+M') VAR, evren içi, tekil olayları; önceki bütün setlerin (MUM_IZI4 / 6 / 8 / 9 / 10 / "
             "12 onay) ve 1. - 2. partinin (hakem_aday 300, hakem_aday2 600) hisseleri hariç; önce haftalık sonra günlük, her dilimde (sembol, tarih) sırasına "
             "dizilip tohumla karıştırılır ve sırayla alınır: hisse başına bir (iki dilim birlikte), BIST dilim başına en çok %20; bir dilimde uygun hisse "
             "yetmezse olabildiği kadar (eksik yazılır, öteki dilimle doldurulmaz); bütün sayfalar tohumla karışık sıraya, 1'den kesintisiz, 50'şer sayfalık dosyalar",
    "sayfa": "1. - 2. partiyle aynı (kısa sayfa; 'Senin kalıbın' + bölge turuncu kutu; kutusuz; hisse / tarih / sonrası yok)"}
HK_PARTI[3] = {"esik": HK_ESIK_P3, "klasor": os.path.join(MI.MI_YOL["cikti"], "hakem_aday3"), "onek": "mum_izi14_aday", "baslik": "MUM_IZI14 aday",
               "onceki": [os.path.join(MI.MI_YOL["cikti"], "hakem_aday", "mum_izi10_aday_anahtar.json"),
                          os.path.join(MI.MI_YOL["cikti"], "hakem_aday2", "mum_izi12_aday_anahtar.json"),
                          os.path.join(MI.MI_YOL["cikti"], "mum_izi10_onay_anahtar.json"), os.path.join(MI.MI_YOL["cikti"], "MUM_IZI12_onay_anahtar.json")]}
# İki aşamalı onay (EK 14 A3; seçim kuralı sonuçtan önce yazıldı, değişmez)
HK_ESIK_ONAY2: Dict[str, Any] = {
    "surum": "HK-O2-1.0", "tohum": 25112141, "hedef": 24, "en_az": 1, "uyari_alti": 12,
    "secim": "aday = 1. aşama EVET; (a) 2. aşama da EVET olanlar, puan1 + puan2 büyükten küçüğe; (b) 2. aşama KISMEN olanlar, aynı sırayla; eşitlikte küçük aday "
             "sayfa numarası; 2. aşama HAYIR olan girmez; set = ilk 24 (varsa); PDF içi sayfa sırası tohumla karışık, yeni sayfa numaraları 2'den; her 1. aşama "
             "EVET sayfası 2. aşama dosyasında olmalı (yoksa DUR); set 0 ise DUR, < 12 ise uyarı (ana model 4. partiyi açar)",
    "sayfa": "eski onay düzeni (kapak + MUM_IZI4_ONAY yerleşimi, ✓ / ✗ kutuları); hakem kararı / puanı / sınıf yalnız mühürlü anahtarda"}
HK_KAPAK2 = ("{M} adaya iki aşamalı görsel hakem baktı: ilk hakem {N} tanesine benziyor dedi, ikinci hakem bunların {N2} tanesine de benziyor dedi; {K} tanesi "
             "burada (günlük ve haftalık). Benziyorsa ✓ kutusuna X koy. Kısmen benziyorsa iki kutunun arasına K yaz. Benzemiyorsa × kutusuna X koy. Yanlış "
             "bulduğun yeri daire içine al.")
# Etiketli öğrenme dosyası (EK 14 A2)
HK_OGREN: Dict[str, Any] = {
    "surum": "HK-OG-1.0", "ad": "MUM_IZI14_OGREN.pdf", "sayfa": [2, 25],
    "kaynak": [{"pdf": os.path.join(MI.MI_YOL["cikti"], "MUM_IZI10_ONAY.pdf"), "etiket": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi10_onay.json"),
                "anahtar": os.path.join(MI.MI_YOL["cikti"], "mum_izi10_onay_anahtar.json")},
               {"pdf": os.path.join(MI.MI_YOL["cikti"], "MUM_IZI12_ONAY.pdf"), "etiket": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi12_onay.json"),
                "anahtar": os.path.join(MI.MI_YOL["cikti"], "MUM_IZI12_onay_anahtar.json")}],
    "sira": ["EVET", "KISMEN", "HAYIR"], "yazi": {"EVET": "CEMAL: BENZİYOR", "KISMEN": "CEMAL: KISMEN", "HAYIR": "CEMAL: BENZEMİYOR"},
    "renk": {"EVET": "#1b7f3a", "KISMEN": "#e07b00", "HAYIR": "#c62828"}, "serit_pt": 78}
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


# ================================================================ 2b) ÖLÇEKLİ ONAY SAYFASI (EK 16 İŞ B; yalnız --olcek; eski sayfa / sha değişmez)
HK_ESIK_OLCEK: Dict[str, Any] = {
    "surum": "HK-OL-1.0", "onceki_bar": 120, "onceki_en_az": 40, "dilim": [2.0, 98.0], "pay": 0.04, "bant_pay": 0.15,
    "adim": [0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 250, 500],
    "cizgi": [4, 8],
    "boy": "BOY_MUTLAK = bölge barlarında (H - L) / C medyanı (%); ÖNCEKİ = bölge başından önceki en çok 120 barın (H - L) / C medyanı (en az 40 bar, yoksa boş); "
           "ORAN = BOY_MUTLAK / ÖNCEKİ (İŞ A BOY_MUTLAK / BOY_OZ tanımı); yalnız bölge sonu t'ye kadarki barlar (t + 1 ve sonrası kullanılmaz: assert)",
    "sinir": "dikey sınır = pencere barlarının O / H / L / C değerlerinin %2 - %98 dilimi ile bölge barlarının en düşük L / en yüksek H'sinin birleşimi; "
             "bölgedeki Bollinger üst / alt bandı görünsün diye her yönde en çok bu açıklığın %15'i kadar genişler (mum ölçeği ezilmesin); ± %4 pay; bunu aşan fitil / bant "
             "çerçevede kesilir, kesilen yere kenarda küçük üçgen (mum: her kesilen mumda koyu kırmızı; bant: her kesik parçada bir mor)",
    "eksen": "sağda yüzde ekseni: 0 = bölgenin son kapanışı; adım listeden 4-8 çizgi verecek en küçük adım; ince yatay kılavuz; fiyat / tarih / hisse yok",
    "kutu": "üç kutu: ✓ benziyor, K kısmen, × benzemiyor",
    "kapak_ek": "Bu sürümde sağda yüzde ekseni var: mumların gerçek boyu görünür. Önceki (ölçeksiz) dosya yerine bunu işaretle. Kısmen için K kutusu eklendi."}


def hk_boy_olcu(H: np.ndarray, L: np.ndarray, C: np.ndarray, t: int, m: int, G: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """B3 ölçüleri yalnız bölge (t - m + 1 .. t) ve öncesi barlarından. t'den sonraki barlar dilimlenip atılır (geleceğe bakma yok; assert)."""
    G = G or HK_ESIK_OLCEK
    t = int(t); m = int(m)
    if not (0 <= t < len(C)) or m < 1 or t - m + 1 < 0:
        raise HKHata(f"boy ölçüsü: geçersiz t={t}, m={m}, n={len(C)}")
    H = np.asarray(H, float)[:t + 1]; L = np.asarray(L, float)[:t + 1]; C = np.asarray(C, float)[:t + 1]
    assert len(C) == t + 1, "geleceğe bakma kapısı: bölge sonundan sonraki bar ölçüye girdi"
    with np.errstate(divide="ignore", invalid="ignore"):
        b = (H - L) / C
    b[~np.isfinite(b) | (C <= 0)] = np.nan
    s = t - m + 1; bolge = b[s:t + 1]; onc = b[max(0, s - int(G["onceki_bar"])):s]; onc = onc[np.isfinite(onc)]
    bm = float(np.nanmedian(bolge) * 100) if np.isfinite(bolge).any() else float("nan")
    if len(onc) >= int(G["onceki_en_az"]):
        om = float(np.median(onc) * 100); oran = bm / om if om > 0 else float("nan")
    else:
        om = float("nan"); oran = float("nan")
    return {"boy_mutlak": bm, "onceki": om, "oran": oran, "onceki_n": int(len(onc)), "bolge_n": int(np.isfinite(bolge).sum()), "son_bar": t}


def hk_y_sinir(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, kutu: Tuple[int, int], G: Optional[Dict[str, Any]] = None,
               BU: Optional[np.ndarray] = None, BA: Optional[np.ndarray] = None) -> Tuple[float, float]:
    """Sağlam dikey sınır (pencere dizileri; kutu = bölgenin pencere içi indeksleri). Bölge barları her zaman çerçevede kalır; bölgedeki bantlar için çerçeve
    her yönde en çok açıklığın bant_pay'ı kadar genişler; bunu aşan fitil / bant kesilir (işaretlenir)."""
    G = G or HK_ESIK_OLCEK; a, b = kutu
    hav = np.concatenate([np.asarray(x, float) for x in (O, H, L, C)]); hav = hav[np.isfinite(hav)]
    if not len(hav):
        raise HKHata("dikey sınır: pencerede geçerli fiyat yok")
    p0, p1 = (float(x) for x in G["dilim"])
    lo = min(float(np.percentile(hav, p0)), float(np.nanmin(np.asarray(L, float)[a:b + 1])))
    hi = max(float(np.percentile(hav, p1)), float(np.nanmax(np.asarray(H, float)[a:b + 1])))
    if not hi > lo:
        hi = lo * 1.01 + 1e-9
    gen = float(G["bant_pay"]) * (hi - lo); lo0, hi0 = lo, hi
    if BU is not None:                                      # bölgedeki üst bant: çerçeve en çok açıklığın bant_pay'ı kadar genişler
        v = np.asarray(BU, float)[a:b + 1]; v = v[np.isfinite(v)]
        if len(v):
            hi = min(max(hi0, float(v.max())), hi0 + gen)
    if BA is not None:
        v = np.asarray(BA, float)[a:b + 1]; v = v[np.isfinite(v)]
        if len(v):
            lo = max(min(lo0, float(v.min())), lo0 - gen)
    pad = float(G["pay"]) * (hi - lo)
    return lo - pad, hi + pad


def hk_yuzde_adim(alt: float, ust: float, ref: float, G: Optional[Dict[str, Any]] = None) -> Tuple[float, List[float]]:
    """Yüzde ekseni: ref'e göre [alt, ust] aralığında 4-8 çizgi veren en küçük adım (yoksa 8'i aşmayan ilk adım). Dönüş: (adım, yüzde listesi)."""
    G = G or HK_ESIK_OLCEK; n0, n1 = (int(x) for x in G["cizgi"])
    if not (ref > 0 and ust > alt):
        raise HKHata(f"yüzde ekseni: geçersiz aralık / referans ({alt}, {ust}, {ref})")
    qa = (alt / ref - 1) * 100; qu = (ust / ref - 1) * 100; sec: Optional[Tuple[float, List[float]]] = None
    for s in G["adim"]:
        s = float(s); k = np.arange(np.ceil(qa / s - 1e-9), np.floor(qu / s + 1e-9) + 1) * s; k = [float(round(x, 6)) + 0.0 for x in k]
        if len(k) <= n1:
            if len(k) >= n0:
                return s, k
            sec = sec or (s, k)
    if sec is None:
        raise HKHata("yüzde ekseni: uygun adım yok")
    return sec


def _hk_yuzde_yazi(p: float) -> str:
    if abs(p) < 1e-9:
        return "0"
    v = f"{abs(p):.1f}".rstrip("0").rstrip(".").replace(".", ",")
    return f"{'+' if p > 0 else '−'}%{v}"


def _hk_sayi(x: float, n: int) -> str:
    return "—" if not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def hk_boy_satiri(B: Dict[str, Any], G: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
    G = G or HK_ESIK_OLCEK
    if not np.isfinite(B["onceki"]):
        return (f"Bölgede ortalama mum boyu: %{_hk_sayi(B['boy_mutlak'], 1)}", f"bu hissenin önceki mumları yetersiz ({B['onceki_n']} < {G['onceki_en_az']}): oran yok")
    n = B["onceki_n"]; ne = f"önceki {n} mumunda" if n < int(G["onceki_bar"]) else f"önceki {int(G['onceki_bar'])} mumunda"
    return (f"Bölgede ortalama mum boyu: %{_hk_sayi(B['boy_mutlak'], 1)}  ·  bu hissenin {ne}: %{_hk_sayi(B['onceki'], 1)}",
            f"oran {_hk_sayi(B['oran'], 2)}   (1'den küçük = bölgede mumlar bu hissenin olağanından küçük)")


def _hk_sayfa_olcek(fig, d: pd.DataFrame, r: Dict[str, Any], a: Dict[str, np.ndarray], sayfa: int, G: Optional[Dict[str, Any]] = None,
                    kutular: bool = True, baslik: Optional[str] = None) -> Dict[str, Any]:
    """EK 16 B1-B4 onay sayfası: büyük bölge grafiği (sağda yüzde ekseni, sağlam sınır + kırpma işareti), altında mum boyu satırı, üç kutu.
    Yalnız bölge sonu t'ye kadarki barlar kullanılır. Dönüş: sayfanın ölçü kaydı (anahtara / json'a).
    EK 18: kutular=False -> aynı çizim, işaret kutusu yok (aday / öğrenme sayfası); baslik verilirse grafik başlığı o (varsayılan 'Sayfa N: ...')."""
    from matplotlib.patches import Rectangle
    G = G or HK_ESIK_OLCEK
    t = d.index.get_loc(pd.Timestamp(r["tarih"])); m = int(r["m"]); once = int(MV.MV_ESIK["onay"]["once"]); i0 = max(0, t - m + 1 - once)
    dg = d.iloc[:t + 1]                                     # geleceğe bakma kapısı: bölgeden sonraki bar çizime / ölçüye girmez
    O_, H_, L_, C_ = (dg[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    BU, BO, BA = MI.mi_bant(C_); sl = slice(i0, t + 1); kutu = (t - m + 1 - i0, t - i0)
    Ow, Hw, Lw, Cw = O_[sl], H_[sl], L_[sl], C_[sl]
    B = hk_boy_olcu(H_, L_, C_, t, m, G)
    MV._mv_ciz(fig.add_axes([0.05, 0.665, 0.34, 0.25]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
    fig.text(0.44, 0.895, "Turuncu kutu = bölge; sağ kenar = bölgenin sonu\n(sonrası gösterilmiyor).\nMor = Bollinger 20 ve SMA20 (kesik).\n"
             "Sağdaki eksen: bölgenin son kapanışına göre\nyüzde (0 = son kapanış).\n▲ / ▼ = çerçeveden taşan fitil kesildi\n(mor işaret: bant kesildi).",
             fontsize=11.5, va="top", linespacing=1.35)
    ax = fig.add_axes([0.05, 0.285, 0.80, 0.34])
    MV._mv_ciz(ax, Ow, Hw, Lw, Cw, BU[sl], BO[sl], BA[sl], kutu, "")
    ax.set_title(baslik if baslik is not None else f"Sayfa {sayfa}: bulunan bölge ({'haftalık' if r['zaman'] == 'haftalik' else 'günlük'} mum)",
                 fontsize=15, weight="bold")
    y0, y1 = hk_y_sinir(Ow, Hw, Lw, Cw, kutu, G, BU[sl], BA[sl]); ax.set_ylim(y0, y1); ax.set_xlim(-0.8, len(Cw) - 0.2)
    ref = float(C_[t]); adim, yz = hk_yuzde_adim(y0, y1, ref, G)
    for p in yz:
        ax.axhline(ref * (1 + p / 100), color="#000000" if abs(p) < 1e-9 else "#9a9a9a", linewidth=1.1 if abs(p) < 1e-9 else 0.5,
                   linestyle="-" if abs(p) < 1e-9 else ":", zorder=1)
    ax.yaxis.tick_right(); ax.set_yticks([ref * (1 + p / 100) for p in yz]); ax.set_yticklabels([_hk_yuzde_yazi(p) for p in yz], fontsize=14)
    ax.tick_params(axis="y", length=4, pad=3)
    x = np.arange(len(Cw)); kes = {"mum_ust": 0, "mum_alt": 0, "bant_ust": 0, "bant_alt": 0}; dy = 0.0
    for i in x:
        if np.isfinite(Hw[i]) and Hw[i] > y1:
            ax.plot(i, y1 - dy, marker="^", color="#8b0000", markersize=8, clip_on=False, zorder=6); kes["mum_ust"] += 1
        if np.isfinite(Lw[i]) and Lw[i] < y0:
            ax.plot(i, y0 + dy, marker="v", color="#8b0000", markersize=8, clip_on=False, zorder=6); kes["mum_alt"] += 1
    for ad_, bb, yk, mk in (("bant_ust", BU[sl], y1, "^"), ("bant_alt", BA[sl], y0, "v")):
        ta = np.isfinite(bb) & ((bb > yk) if mk == "^" else (bb < yk)); kes[ad_] = int(ta.sum())
        bas = np.flatnonzero(ta & ~np.r_[False, ta[:-1]]); son = np.flatnonzero(ta & ~np.r_[ta[1:], False])
        for p0, p1 in zip(bas, son):                    # her kesik bant parçasına bir işaret (parçanın ortası)
            ax.plot((p0 + p1) / 2.0, yk, marker=mk, color="#7b3294", markersize=7, clip_on=False, zorder=5)
    s1, s2 = hk_boy_satiri(B, G)
    fig.text(0.5, 0.245, s1, fontsize=14, ha="center", va="top"); fig.text(0.5, 0.21, s2, fontsize=14, ha="center", va="top", weight="bold")
    if kutular:
        axk = fig.add_axes([0.04, 0.03, 0.92, 0.15]); axk.axis("off")
        for xx, txt in ((0.0, "✓  benziyor"), (0.345, "K  kısmen"), (0.69, "×  benzemiyor")):
            axk.add_patch(Rectangle((xx, 0.05), 0.31, 0.9, fill=False, linewidth=3, transform=axk.transAxes))
            axk.text(xx + 0.155, 0.5, txt, ha="center", va="center", fontsize=21, transform=axk.transAxes)
    return {"boy_mutlak": B["boy_mutlak"], "onceki": B["onceki"], "oran": B["oran"], "onceki_n": B["onceki_n"], "bolge_n": B["bolge_n"],
            "y_sinir_yuzde": [round((y0 / ref - 1) * 100, 3), round((y1 / ref - 1) * 100, 3)], "adim": adim, "cizgi": len(yz), "kesilen": kes,
            "son_bar_index": int(t), "seri_uzunluk_kullanilan": int(len(dg))}


def hk_aday(cikti: Optional[str] = None, parti: int = 1) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    if parti not in HK_PARTI:
        raise HKHata(f"bilinmeyen parti {parti}")
    PT = HK_PARTI[parti]; G = PT["esik"]
    if PT.get("olcek"):                                    # EK 18: mum boyu kapılı, ölçekli aday sayfaları (eski partilerin yolu aşağıda aynen)
        return hk_aday_olcek(cikti, parti)
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
    """Hakem dosyaları: {"sayfalar": {"<no>": {"karar": EVET | KISMEN | HAYIR, "puan": 0-10, "gerekce": metin}}}; birden çok dosya birleşir; çelişki / şema
    dışı -> DUR. KISMEN (EK 14) kabul edilir; tek aşamalı onayda yalnız EVET seçilir (eski davranış)."""
    out: Dict[int, Dict[str, Any]] = {}
    for y in yollar:
        J = json.load(open(y, encoding="utf-8"))
        if not isinstance(J, dict) or not isinstance(J.get("sayfalar"), dict):
            raise HKHata(f"hakem şeması: 'sayfalar' yok ({y})")
        for k, v in J["sayfalar"].items():
            if not str(k).strip().isdigit() or not isinstance(v, dict):
                raise HKHata(f"hakem şeması: sayfa {k!r} ({y})")
            kr = str(v.get("karar", "")).strip().replace("İ", "I").upper()
            if kr not in ("EVET", "KISMEN", "HAYIR"):
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


def hk_onay_sec2(aday: List[Dict[str, Any]], H2: Dict[int, Dict[str, Any]], G: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """İki aşamalı seçim (HK_ESIK_ONAY2): aday = 1. aşama EVET satırları ('sayfa', 'hakem_puan' alanlı); H2 = 2. aşama kararları.
    (a) 2. aşama EVET, (b) 2. aşama KISMEN; her sınıfta puan1 + puan2 büyükten küçüğe, eşitlikte küçük sayfa; HAYIR girmez; ilk hedef; sayfa sırası tohumlu."""
    G = G or HK_ESIK_ONAY2; eksik = sorted(int(r["sayfa"]) for r in aday if int(r["sayfa"]) not in H2)
    if eksik:
        raise HKHata(f"2. aşama hakem dosyasında olmayan 1. aşama EVET sayfaları: {eksik[:10]}")
    sinif: Dict[str, List[Dict[str, Any]]] = {"a": [], "b": []}
    for r in aday:
        h2 = H2[int(r["sayfa"])]; s = {"EVET": "a", "KISMEN": "b"}.get(h2["karar"])
        if s is not None:
            sinif[s].append(dict(r, hakem2_karar=h2["karar"], hakem2_puan=h2["puan"], hakem2_gerekce=h2["gerekce"], sinif=s))
    sira: List[Dict[str, Any]] = []
    for s in ("a", "b"):
        sira += sorted(sinif[s], key=lambda r: (-(float(r["hakem_puan"]) + float(r["hakem2_puan"])), int(r["sayfa"])))
    sec = sira[:int(G["hedef"])]
    if len(sec) < int(G["en_az"]):
        raise HKHata(f"iki aşamalı seçim {len(sec)} sayfa < {G['en_az']}: onay seti kurulmadı")
    if len(sec) < int(G["uyari_alti"]):
        hklog.warning("iki aşamalı set %d sayfa < %d: iş tanımı gereği yeni parti gerekir", len(sec), G["uyari_alti"])
    p = np.random.default_rng(G["tohum"]).permutation(len(sec))
    return [dict(sec[i], yeni_sayfa=j + 2) for j, i in enumerate(p)]


def hk_kapak_metni(kapak: Optional[str], M: int, N: int, K: int, N2: Optional[int] = None) -> str:
    """--kapak verilmişse aynen ({M} bakılan aday, {N} hakem EVET, {K} PDF'e giren sayfa, {N2} iki hakemin de EVET dediği yer tutucuları doldurulur); yoksa
    eski kapak (iki aşamalıda HK_KAPAK2)."""
    if kapak is not None:
        t = kapak.replace("{M}", str(M)).replace("{N}", str(N)).replace("{K}", str(K))
        return t.replace("{N2}", str(N2)) if N2 is not None else t
    if N2 is not None:
        return HK_KAPAK2.format(M=M, N=N, N2=N2, K=K)
    return HK_KAPAK.format(M=M, N=N, BUNLAR="bunlar onlar" if N <= HK_ESIK["onay"]["hedef"] else f"içlerinden rastgele {K}'ü bunlar")


def hk_onay(hakem: List[str], cikti: Optional[str] = None, aday_klasor: Optional[str] = None, kapak: Optional[str] = None,
            ad: Optional[str] = None, hakem2: Optional[str] = None, olcek: bool = False) -> Dict[str, Any]:
    """Onay derleme. hakem2 None: eski tek aşamalı davranış (aynen). hakem2 verilirse iki aşamalı seçim (hk_onay_sec2, HK_ESIK_ONAY2).
    olcek=True (EK 16 İŞ B): mühürlü eski set aynı girdilerle yeniden kurulur, sayfa -> bölge eski anahtarla birebir denetlenir (değilse DUR) ve ölçekli
    sayfalarla <ad>_ONAY_OLCEKLI.pdf + <ad>_onay_olcekli.json (hisse adı yok) yazılır; eski PDF / anahtar okunur, yazılmaz."""
    if olcek:
        if _hk_olcek_parti_mi(aday_klasor or HK_YOL["aday"]):   # EK 18 A4: ölçekli partiden YENİ set (eski set yok); öteki durum eski yeniden basım
            return hk_onay_olcek_yeni(hakem, cikti, aday_klasor, kapak, ad, hakem2)
        return hk_onay_olcek(hakem, cikti, aday_klasor, kapak, ad, hakem2)
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
    H2: Optional[Dict[int, Dict[str, Any]]] = None; N2: Optional[int] = None
    if hakem2 is None:
        sec = hk_onay_sec(evet)
    else:
        H2 = hk_hakem_oku([hakem2]); yabanci2 = sorted(set(H2) - set(Ad))
        if yabanci2:
            raise HKHata(f"2. aşama hakem dosyasında aday listesinde olmayan sayfalar: {yabanci2[:10]}")
        sec = hk_onay_sec2(evet, H2); N2 = sum(1 for r in evet if H2.get(int(r["sayfa"]), {}).get("karar") == "EVET")
    M = len(H); N = len(evet); kapak_t = hk_kapak_metni(kapak, M, N, len(sec), N2)
    a = MV.mv_sablon()["tam"]["ohlc"]; Vc: Dict[Any, Any] = {}; os.makedirs(cikti, exist_ok=True)
    with PdfPages(y, metadata={"Title": f"{ad or 'MUM_IZI10'} onay", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.06, 0.95, "GÖRSEL HAKEMİN SEÇTİĞİ BÖLGELER", fontsize=16, weight="bold")
        fig.text(0.06, 0.88, kapak_t, fontsize=13, va="top", wrap=True)
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
         "kapak": kapak_t, "aday_bakilan": M, "hakem_evet": N, "secilen": len(sec),
         "secilen_zaman": pd.Series([r["zaman"] for r in sec], dtype=object).value_counts().to_dict(), "pdf_sha": MI._mi_sha(y),
         "sayfalar": [{"yeni_sayfa": r["yeni_sayfa"], "aday_sayfa": r["sayfa"], "hakem_puan": r["hakem_puan"], "hakem_gerekce": r["hakem_gerekce"], "zaman": r["zaman"],
                       "pazar": r["pazar"], "sembol": r["sembol"], "bolge_bas": r["bolge_bas"], "bolge_son": r["bolge_son"], "pencere": r["pencere"]}
                      for r in sorted(sec, key=lambda r: r["yeni_sayfa"])]}
    if H2 is not None:                                     # iki aşamalı: ek mühür alanları (eski anahtar şeması bu alanlar dışında aynen)
        K.update({"surum_onay2": HK_ESIK_ONAY2["surum"], "esik_onay2_sha": _hk_sha(HK_ESIK_ONAY2), "tohum": HK_ESIK_ONAY2["tohum"],
                  "hakem2_dosyasi": {os.path.basename(hakem2): MI._mi_sha(hakem2)}, "hakem2_bakilan": len(H2), "iki_hakem_evet": N2,
                  "secilen_sinif": {s: sum(r["sinif"] == s for r in sec) for s in ("a", "b")}})
        ek = {r["yeni_sayfa"]: r for r in sec}
        for x in K["sayfalar"]:
            r = ek[x["yeni_sayfa"]]
            x.update({"hakem_karar": "EVET", "hakem2_karar": r["hakem2_karar"], "hakem2_puan": r["hakem2_puan"], "hakem2_gerekce": r["hakem2_gerekce"],
                      "sinif": r["sinif"]})
    MI._mi_jyaz(ya, K, "onay anahtar 10")
    hklog.info("onay: %d adaya bakıldı, hakem EVET %d, seçilen %d -> %s", M, N, len(sec), y)
    return K


HK_OLCEK_KIMLIK = ("yeni_sayfa", "aday_sayfa", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "pencere")


def hk_onay_olcek(hakem: List[str], cikti: Optional[str] = None, aday_klasor: Optional[str] = None, kapak: Optional[str] = None,
                  ad: Optional[str] = None, hakem2: Optional[str] = None, G: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """EK 16 B5: ölçekli yeniden basım. Kapılar (DUR): eski anahtar var; hakem / 2. hakem / aday anahtarı sha'ları eski anahtardakiyle aynı; kapak eski
    kapakla aynı; seçim yeniden kurulunca her sayfanın bölge kimliği (HK_OLCEK_KIMLIK) eski anahtarla aynı; çıktılar yoksa yazılır."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    G = G or HK_ESIK_OLCEK; cikti = cikti or HK_YOL["cikti"]; on = ad or "MUM_IZI10"
    ea = os.path.join(cikti, f"{ad}_onay_anahtar.json" if ad else "mum_izi10_onay_anahtar.json")
    y = os.path.join(cikti, f"{on}_ONAY_OLCEKLI.pdf"); yj = os.path.join(cikti, f"{on}_onay_olcekli.json")
    if not os.path.exists(ea):
        raise HKHata(f"ölçekli basım için eski onay anahtarı yok: {ea}")
    if os.path.exists(y) or os.path.exists(yj):
        raise HKHata(f"ölçekli onay PDF / json zaten var: {y}")
    E = json.load(open(ea, encoding="utf-8")); ea_sha = MI._mi_sha(ea)
    ey = os.path.join(cikti, f"{ad}_ONAY.pdf" if ad else "MUM_IZI10_ONAY.pdf"); ep_sha = MI._mi_sha(ey) if os.path.exists(ey) else None
    if ep_sha is not None and ep_sha != E.get("pdf_sha"):
        raise HKHata("eski onay PDF'i anahtardaki pdf_sha ile uyuşmuyor (işaretli / değişmiş kopya)")
    hs = {os.path.basename(h): MI._mi_sha(h) for h in hakem}
    if hs != E.get("hakem_dosyalari"):
        raise HKHata("hakem dosyaları eski anahtardaki sha'larla uyuşmuyor")
    if (hakem2 is None) != ("hakem2_dosyasi" not in E) or (hakem2 is not None and {os.path.basename(hakem2): MI._mi_sha(hakem2)} != E["hakem2_dosyasi"]):
        raise HKHata("2. aşama hakem dosyası eski anahtarla uyuşmuyor")
    ay = hk_aday_anahtar_bul(aday_klasor or HK_YOL["aday"])
    if MI._mi_sha(ay) != E.get("aday_anahtar_sha"):
        raise HKHata("aday anahtarı eski onay anahtarındaki sha ile uyuşmuyor")
    A = json.load(open(ay, encoding="utf-8")); Ad = {int(r["sayfa"]): r for r in A["sayfalar"]}
    H = hk_hakem_oku(hakem); yabanci = sorted(set(H) - set(Ad))
    if yabanci:
        raise HKHata(f"hakem dosyasında aday listesinde olmayan sayfalar: {yabanci[:10]}")
    evet = [dict(Ad[n], hakem_puan=v["puan"], hakem_gerekce=v["gerekce"]) for n, v in H.items() if v["karar"] == "EVET"]
    N2: Optional[int] = None
    if hakem2 is None:
        sec = hk_onay_sec(evet)
    else:
        H2 = hk_hakem_oku([hakem2]); sec = hk_onay_sec2(evet, H2); N2 = sum(1 for r in evet if H2.get(int(r["sayfa"]), {}).get("karar") == "EVET")
    kapak0 = hk_kapak_metni(kapak, len(H), len(evet), len(sec), N2)
    if kapak0 != E.get("kapak"):
        raise HKHata("kapak metni eski anahtardaki kapakla aynı değil (eski kapak aynen verilmeli)")
    yeni = [{"yeni_sayfa": r["yeni_sayfa"], "aday_sayfa": r["sayfa"], "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "bolge_bas": r["bolge_bas"],
             "bolge_son": r["bolge_son"], "pencere": r["pencere"]} for r in sorted(sec, key=lambda r: r["yeni_sayfa"])]
    eski = [{k: x[k] for k in HK_OLCEK_KIMLIK} for x in E["sayfalar"]]
    if yeni != eski:
        fark = [i + 2 for i, (p, q) in enumerate(zip(yeni, eski)) if p != q]
        raise HKHata(f"yeniden kurulan seçim eski anahtarla aynı değil (sayı {len(yeni)} / {len(eski)}; farklı sayfa sayısı {len(fark)})")
    kapak_t = f"{kapak0} {G['kapak_ek']}"
    a = MV.mv_sablon()["tam"]["ohlc"]; Vc: Dict[Any, Any] = {}; os.makedirs(cikti, exist_ok=True); olc: List[Dict[str, Any]] = []
    with PdfPages(y, metadata={"Title": f"{on} onay (ölçekli)", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.06, 0.95, "GÖRSEL HAKEMİN SEÇTİĞİ BÖLGELER", fontsize=16, weight="bold")
        fig.text(0.06, 0.88, kapak_t, fontsize=13, va="top", wrap=True)
        MV._mv_ciz(fig.add_axes([0.25, 0.2, 0.5, 0.35]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
        pdf.savefig(fig); plt.close(fig)
        for r in sorted(sec, key=lambda r: r["yeni_sayfa"]):
            k = (r["zaman"], r["pazar"])
            if k not in Vc:
                Vc[k] = MV.mv_veri(*k)
            d = Vc[k][r["sembol"]]; rr = {"tarih": r["bolge_son"], "m": r["pencere"], "zaman": r["zaman"]}
            if _hk_bas(d, rr) != r["bolge_bas"]:
                raise HKHata(f"aday sayfa {r['sayfa']}: bölge başı anahtarla uyuşmuyor")
            fig = plt.figure(figsize=(8.3, 11.7)); o = _hk_sayfa_olcek(fig, d, rr, a, r["yeni_sayfa"], G); pdf.savefig(fig); plt.close(fig)
            olc.append(dict(o, yeni_sayfa=r["yeni_sayfa"], zaman=r["zaman"]))
    J = {"not": "EK 16 İŞ B: ölçekli onay seti; hisse adı / tarih YOK; bölge kimliği eski mühürlü anahtarla denetlendi", "surum": HK_SURUM_OLCEK,
         "esik_olcek": G["surum"], "esik_olcek_sha": _hk_sha(G), "pdf": os.path.basename(y), "pdf_sha": MI._mi_sha(y), "sayfa_sayisi": len(sec) + 1,
         "eski_anahtar": os.path.basename(ea), "eski_anahtar_sha": ea_sha, "eski_pdf": os.path.basename(ey), "eski_pdf_sha": ep_sha,
         "eski_pdf_sha_anahtarda": E.get("pdf_sha"), "kapak": kapak_t,
         "bolge_kimligi": {"esit": True, "alanlar": list(HK_OLCEK_KIMLIK), "sayfa": len(yeni), "yontem": "seçim aynı hakem / aday girdilerinden yeniden kuruldu; "
                           "her sayfanın alanları eski anahtardakiyle birebir karşılaştırıldı (eşit değilse DUR)"},
         "olcu": {k: G[k] for k in ("boy", "sinir", "eksen")}, "sayfalar": olc}
    MI._mi_jyaz(yj, J, "ölçekli onay")
    hklog.info("ölçekli onay: %d sayfa (bölge kimliği eski anahtarla aynı) -> %s", len(sec), y)
    return J


# ================================================================ 3b) ETİKETLİ ÖĞRENME DOSYASI (EK 14 A2)
def hk_ogren_liste(kaynak: Optional[List[Dict[str, Any]]] = None, G: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Kaynak onay PDF'leri + Cemal etiket json'ları -> sıralı örnek listesi. Denetimler (DUR): PDF sha = onay anahtarındaki pdf_sha (işaretsiz özgün), etiket
    sayfaları tam olarak G['sayfa'] aralığı, etiket sınıfı EVET / KISMEN / HAYIR, etiket 'zaman' alanı onay anahtarındaki sayfanın zamanıyla aynı (yanlış dosya
    kapısı). Sıra: sınıf (EVET, KISMEN, HAYIR), sonra kaynak sırası, sonra sayfa."""
    import pypdf
    G = G or HK_OGREN; kaynak = kaynak if kaynak is not None else G["kaynak"]; a0, a1 = (int(x) for x in G["sayfa"]); out: List[Dict[str, Any]] = []
    for ki, k in enumerate(kaynak):
        for y in (k["pdf"], k["etiket"]):
            if not os.path.exists(y):
                raise HKHata(f"öğrenme kaynağı yok: {y}")
        n_sayfa = len(pypdf.PdfReader(k["pdf"]).pages)
        if n_sayfa < a1:
            raise HKHata(f"{os.path.basename(k['pdf'])}: {n_sayfa} sayfa < {a1}")
        zam: Dict[int, str] = {}
        if k.get("anahtar"):
            A = json.load(open(k["anahtar"], encoding="utf-8"))
            if MI._mi_sha(k["pdf"]) != A.get("pdf_sha"):
                raise HKHata(f"{os.path.basename(k['pdf'])}: sha onay anahtarıyla uyuşmuyor (işaretli kopya ya da yanlış dosya)")
            zam = {int(r["yeni_sayfa"]): r["zaman"] for r in A["sayfalar"]}
        E = json.load(open(k["etiket"], encoding="utf-8")).get("sayfalar")
        if not isinstance(E, dict) or sorted(int(x) for x in E) != list(range(a0, a1 + 1)):
            raise HKHata(f"{os.path.basename(k['etiket'])}: etiket sayfaları {a0}-{a1} değil")
        for sn, v in E.items():
            s = str(v.get("isaret", "")).strip().replace("İ", "I").upper()
            if s not in G["sira"]:
                raise HKHata(f"{os.path.basename(k['etiket'])}: sayfa {sn} etiket {v.get('isaret')!r}")
            if zam and v.get("zaman") is not None and zam.get(int(sn)) != v["zaman"]:
                raise HKHata(f"{os.path.basename(k['etiket'])}: sayfa {sn} zamanı onay anahtarıyla uyuşmuyor")
            out.append({"kaynak_i": ki, "pdf": k["pdf"], "sayfa": int(sn), "sinif": s})
    out.sort(key=lambda r: (G["sira"].index(r["sinif"]), r["kaynak_i"], r["sayfa"]))
    return [dict(r, ornek=i + 1) for i, r in enumerate(out)]


def _hk_serit(w: float, bant: float, yazi: str, renk: str, sag: str, fs: float = 30, sag_fs: float = 18):
    """Tek şerit sayfası (matplotlib -> PDF bellekte -> pypdf sayfası); metin aranabilir (TrueType gömülü). fs / sag_fs: yazı boyları (EK 18 uzun şerit)."""
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pypdf
    with matplotlib.rc_context({"pdf.fonttype": 42, "font.family": "DejaVu Sans"}):
        fig = plt.figure(figsize=(w / 72.0, bant / 72.0)); fig.patch.set_facecolor(renk)
        fig.text(0.03, 0.5, yazi, color="white", fontsize=fs, weight="bold", va="center", ha="left")
        fig.text(0.97, 0.5, sag, color="white", fontsize=sag_fs, weight="bold", va="center", ha="right")
        b = io.BytesIO(); fig.savefig(b, format="pdf", facecolor=renk, metadata={"CreationDate": None, "ModDate": None}); plt.close(fig)
    b.seek(0)
    return pypdf.PdfReader(b).pages[0]


def hk_ogren(cikti: Optional[str] = None, kaynak: Optional[List[Dict[str, Any]]] = None, ad: Optional[str] = None,
             G: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """EK 14 A2: kaynak sayfalar bozulmadan alınır, sayfa üstten şerit yüksekliği kadar genişletilir, şeride 'CEMAL: <sınıf>' + 'Örnek n / N' basılır.
    Hisse / tarih eklenmez; grafik örtülmez (şerit sayfanın eski sınırının üstünde)."""
    import pypdf
    from pypdf import PageObject, Transformation
    G = G or HK_OGREN; cikti = cikti or HK_YOL["cikti"]; y = os.path.join(cikti, ad or G["ad"])
    if os.path.exists(y):
        raise HKHata(f"öğrenme dosyası zaten var: {y}")
    L = hk_ogren_liste(kaynak, G); N = len(L); bant = float(G["serit_pt"]); R: Dict[str, Any] = {}; W = pypdf.PdfWriter()
    for r in L:
        if r["pdf"] not in R:
            R[r["pdf"]] = pypdf.PdfReader(r["pdf"])
        src = R[r["pdf"]].pages[r["sayfa"] - 1]; mb = src.mediabox; w = float(mb.width); h = float(mb.height); x0 = float(mb.left); y0 = float(mb.bottom)
        yeni = PageObject.create_blank_page(width=w, height=h + bant)
        yeni.merge_transformed_page(src, Transformation().translate(-x0, -y0))
        yeni.merge_transformed_page(_hk_serit(w, bant, G["yazi"][r["sinif"]], G["renk"][r["sinif"]], f"Örnek {r['ornek']} / {N}"), Transformation().translate(0, h))
        W.add_page(yeni)
    W.add_metadata({"/Title": "MUM_IZI14 öğrenme dosyası (Cemal etiketli)"})
    os.makedirs(cikti, exist_ok=True)
    with open(y, "wb") as f:
        W.write(f)
    sinif = {s: sum(r["sinif"] == s for r in L) for s in G["sira"]}
    hklog.info("öğrenme dosyası: %d örnek %s -> %s", N, sinif, y)
    return {"n": N, "sinif": sinif, "cikti": y, "sha": MI._mi_sha(y), "kaynak_sha": {os.path.basename(p): MI._mi_sha(p) for p in R}}


# ================================================================ 3c) EK 18: MUM BOYU KAPISI, ölçekli aday partisi (4), yeni ölçekli onay, ölçekli öğrenme
# İş tanımı: arastirma_cikti/mum_izi/MUM_IZI18_IS_TANIMI.md (21ff575). Eski sabitler / fonksiyon yolları değişmez; ORAN yalnız hk_boy_olcu ile (tek tanım).
HK_SURUM_P4 = "EK 18 İŞ A (2026-11-26): mum boyu kapısı + ölçekli aday / onay / öğrenme"
HK_ESIK_P4: Dict[str, Any] = {
    "surum": "HK-P4-1.0", "tohum": 25112181, "gunluk": 300, "haftalik": 300, "dosya_sayfa": 50, "eksik_izin": True,
    "kapi": {"oran_en_cok": 0.70, "cok_kucuk": 0.50, "pay_esikleri": [0.85, 0.70, 0.50],
             "tanim": "ORAN = bölge barlarında (H - L) / C medyanı / bölgeden önceki 120 barın (H - L) / C medyanı (en az 40 bar; yoksa aday DEĞİL); hesap "
                      "hk_boy_olcu ile (ölçekli sayfanın mum boyu satırıyla aynı fonksiyon); KAPI: ORAN <= 0,70 (sınır dahil); katman ÇOK KÜÇÜK ORAN <= 0,50, "
                      "KÜÇÜK 0,50 < ORAN <= 0,70"},
    "secim": "MUM_IZI8 taramasının v5M ('R4+M') VAR, evren içi olaylarından KAPI'yı geçenler; önceki bütün setlerin (MUM_IZI4 / 6 / 8 / 9 / 10 / 12 / 14 onay) ve "
             "1. - 3. partinin hisseleri hariç; önce haftalık sonra günlük, her dilimde (sembol, tarih) sırasına dizilip tohumla karıştırılır ve sırayla alınır: "
             "hisse başına bir (iki dilim birlikte); BIST tavanı YOK (iş tanımı: kapıdan geçen 600'den azsa hepsi alınır); dilim hedefi 300, yetmezse olabildiği "
             "kadar (eksik yazılır, öteki dilimle doldurulmaz); bütün sayfalar tohumla karışık sıraya, 1'den kesintisiz, 50'şer sayfalık dosyalar",
    "sayfa": "ÖLÇEKLİ: EK 16 onay --olcek sayfasıyla aynı çizim (_hk_sayfa_olcek: sağda yüzde ekseni, uç fitil kesimi, mum boyu satırı); işaret kutusu YOK; "
             "hisse / tarih / fiyat / sonrası YOK"}
HK_PARTI[4] = {"esik": HK_ESIK_P4, "klasor": os.path.join(MI.MI_YOL["cikti"], "hakem_aday4"), "onek": "mum_izi18_aday", "baslik": "MUM_IZI18 aday", "olcek": True,
               "onceki": [os.path.join(MI.MI_YOL["cikti"], "hakem_aday", "mum_izi10_aday_anahtar.json"),
                          os.path.join(MI.MI_YOL["cikti"], "hakem_aday2", "mum_izi12_aday_anahtar.json"),
                          os.path.join(MI.MI_YOL["cikti"], "hakem_aday3", "mum_izi14_aday_anahtar.json"),
                          os.path.join(MI.MI_YOL["cikti"], "mum_izi10_onay_anahtar.json"), os.path.join(MI.MI_YOL["cikti"], "MUM_IZI12_onay_anahtar.json"),
                          os.path.join(MI.MI_YOL["cikti"], "MUM_IZI14_onay_anahtar.json")]}
HK_KATMAN = {"COK_KUCUK": "ÇOK KÜÇÜK", "KUCUK": "KÜÇÜK"}
# Yeni ölçekli onay seti (A4): seçim EK 14 kuralı (HK_ESIK_ONAY2) aynen; yalnız iş tanımı 3. bölümün 12'ye tamamlama kuralı eklendi
HK_ESIK_ONAY4: Dict[str, Any] = {
    "surum": "HK-O4-1.0", "temel": "HK-O2-1.0", "tohum": 25112141, "hedef": 24, "en_az": 1, "doldur_alt": 12, "doldur_puan_en_az": 6.0,
    "secim": "EK 14 iki aşamalı kural aynen (HK-O2-1.0: aday = 1. aşama EVET; (a) 2. aşama EVET, (b) 2. aşama KISMEN; her sınıfta puan1 + puan2 büyükten küçüğe, "
             "eşitlikte küçük sayfa; HAYIR girmez; ilk 24); set 12'den azsa (c) 1. aşama KISMEN ve puan1 >= 6 olanlar (puan1 büyükten küçüğe, eşitlikte küçük "
             "sayfa; 2. aşama kararına bakılmaz) ile 12'ye tamamlanır ve kapakta söylenir; PDF sırası tohumlu (25112141), yeni sayfa numaraları 2'den; set 0 -> DUR",
    "sayfa": "ölçekli onay sayfası (EK 16: yüzde ekseni, mum boyu satırı ve ORAN, ✓ / K / × kutuları); hakem kararı / puanı / sınıf yalnız mühürlü anahtarda"}
HK_KAPAK4 = ("{M} adaya iki aşamalı görsel hakem baktı. Adayların hepsinde bölgedeki mumlar o hissenin önceki mumlarından en az %30 küçük (oran 0,70 ve altı; "
             "her sayfanın altında yazılı). İlk hakem {N} tanesine benziyor dedi, ikinci hakem bunların {N2} tanesine de benziyor dedi; {K} tanesi burada "
             "(günlük ve haftalık). Sağda yüzde ekseni var: mumların gerçek boyu görünür. Benziyorsa ✓, kısmen benziyorsa K, benzemiyorsa × kutusuna X koy. "
             "Yanlış bulduğun yeri daire içine al.")
HK_KAPAK4_DOLDUR = "Set 12 sayfadan az kaldığı için ilk hakemin kısmen dediği {C} sayfayla 12'ye tamamlandı."
# Ölçekli öğrenme dosyası (A3)
HK_OGREN2: Dict[str, Any] = {
    "surum": "HK-OG-2.0", "ad": "MUM_IZI18_OGREN.pdf",
    "gruplar": [{"ad": "olcekli", "yazi_on": "CEMAL (ölçekli sayfada)",
                 "kaynak": [{"etiket": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi14_onay.json"), "sayfa": [2, 18],
                             "anahtar": os.path.join(MI.MI_YOL["cikti"], "MUM_IZI14_onay_anahtar.json"),
                             "olcekli_json": os.path.join(MI.MI_YOL["cikti"], "MUM_IZI14_onay_olcekli.json")}]},
                {"ad": "eski", "yazi_on": "CEMAL (eski, ölçeksiz sayfada)",
                 "kaynak": [{"etiket": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi10_onay.json"), "sayfa": [2, 25],
                             "anahtar": os.path.join(MI.MI_YOL["cikti"], "mum_izi10_onay_anahtar.json"), "pdf": os.path.join(MI.MI_YOL["cikti"], "MUM_IZI10_ONAY.pdf")},
                            {"etiket": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi12_onay.json"), "sayfa": [2, 25],
                             "anahtar": os.path.join(MI.MI_YOL["cikti"], "MUM_IZI12_onay_anahtar.json"), "pdf": os.path.join(MI.MI_YOL["cikti"], "MUM_IZI12_ONAY.pdf")}]}],
    "sira": ["EVET", "KISMEN", "HAYIR"], "yazi": {"EVET": "BENZİYOR", "KISMEN": "KISMEN", "HAYIR": "BENZEMİYOR"},
    "renk": {"EVET": "#1b7f3a", "KISMEN": "#e07b00", "HAYIR": "#c62828"}, "serit_pt": 78, "fs": 17, "sag_fs": 12,
    "sayfa": "bölgeler mühürlü onay anahtarlarından yeniden çizilir (_hk_sayfa_olcek, kutusuz, başlık 'Örnek n'); üstte etiket şeridi; hisse / tarih / sonrası yok"}


def hk_kapi(oran: Any, G: Optional[Dict[str, Any]] = None) -> bool:
    """KAPI: ORAN sonlu ve <= 0,70 (sınır dahil). ORAN yok (önceki < 40 bar) -> aday DEĞİL."""
    G = G or HK_ESIK_P4
    try:
        x = float(oran)
    except (TypeError, ValueError):
        return False
    return bool(np.isfinite(x) and x <= float(G["kapi"]["oran_en_cok"]))


def hk_katman(oran: Any, G: Optional[Dict[str, Any]] = None) -> Optional[str]:
    G = G or HK_ESIK_P4
    if not hk_kapi(oran, G):
        return None
    return HK_KATMAN["COK_KUCUK"] if float(oran) <= float(G["kapi"]["cok_kucuk"]) else HK_KATMAN["KUCUK"]


def hk_olay_oran(olay: List[Dict[str, Any]], veri=None, sakla: bool = False) -> Tuple[List[Dict[str, Any]], Dict[Tuple[str, str, str], pd.DataFrame]]:
    """Her olaya ORAN (hk_boy_olcu; yalnız bölge sonu t'ye kadarki barlar) + katman ekler. veri(zaman, pazar) -> {sembol: DataFrame} (varsayılan MV.mv_veri).
    Veri dilim dilim yüklenir (bellek); sakla=True ise KAPI'yı geçen olayların serileri döner (çizim için). Bölge sonu KESİK'i aşarsa / tarih seride yoksa DUR."""
    veri = veri or MV.mv_veri; out: List[Dict[str, Any]] = []; sak: Dict[Tuple[str, str, str], pd.DataFrame] = {}
    for k in sorted({(o["zaman"], o["pazar"]) for o in olay}):
        V = veri(*k)
        for o in olay:
            if (o["zaman"], o["pazar"]) != k:
                continue
            if pd.Timestamp(o["tarih"]) > MI.MI_KESIK:
                raise HKHata(f"KESİK AŞIMI: {o['zaman']} {o['pazar']} olay {o['tarih']}")
            d = V.get(o["sembol"])
            if d is None:
                raise HKHata(f"olay serisi yok ({o['zaman']} {o['pazar']})")
            try:
                t = int(d.index.get_loc(pd.Timestamp(o["tarih"])))
            except KeyError as ex:
                raise HKHata(f"olay tarihi seride yok ({o['zaman']} {o['pazar']})") from ex
            if "t" in o and int(o["t"]) != t:
                raise HKHata(f"olay indeksi taramayla uyuşmuyor ({o['zaman']} {o['pazar']})")
            B = hk_boy_olcu(d.High.to_numpy(float), d.Low.to_numpy(float), d.Close.to_numpy(float), t, int(o["m"]))
            r = dict(o, oran=B["oran"], boy_mutlak=B["boy_mutlak"], onceki=B["onceki"], onceki_n=B["onceki_n"], katman=hk_katman(B["oran"]))
            out.append(r)
            if sakla and r["katman"] is not None:
                sak[(o["zaman"], o["pazar"], o["sembol"])] = d
        del V
        hklog.info("ORAN: %s %s bitti (%d olay)", *k, sum(1 for o in olay if (o["zaman"], o["pazar"]) == k))
    return out, sak


def hk_parti_bolgeleri(partiler: Tuple[int, ...] = (1, 2, 3)) -> set:
    """Önceki aday partilerinde (hakeme) gösterilmiş bölgeler: (zaman, sembol, bölge sonu)."""
    s: set = set()
    for p in partiler:
        y = os.path.join(HK_PARTI[p]["klasor"], f"{HK_PARTI[p]['onek']}_anahtar.json")
        if not os.path.exists(y):
            raise HKHata(f"parti {p} anahtarı yok: {y}")
        s |= {(r["zaman"], r["sembol"], r["bolge_son"]) for r in json.load(open(y, encoding="utf-8"))["sayfalar"]}
    return s


def hk_havuz_say(olay_o: List[Dict[str, Any]], haric: set, parti_bolge: set, G: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """A1 havuz sayımı (getirisiz): evren içi olaylar; gruplar 'tum', 'parti_1_3' (1. - 3. partide gösterilmiş bölge), 'hic_gosterilmemis' (hissesi önceki
    hiçbir set / partide yok). Paylar ORAN hesaplanabilen olaylar üzerinden. Hisse adı yok."""
    G = G or HK_ESIK_P4; es = [float(x) for x in G["kapi"]["pay_esikleri"]]
    grp = {"tum": lambda o: True, "parti_1_3": lambda o: (o["zaman"], o["sembol"], o["tarih"]) in parti_bolge,
           "hic_gosterilmemis": lambda o: o["sembol"] not in haric}
    out: Dict[str, Any] = {"payda": "ORAN hesaplanabilen olay (önceki >= 40 bar)", "esikler": es, "grup": {}}
    for g, f in grp.items():
        out["grup"][g] = {}
        for z in ("gunluk", "haftalik"):
            X = [o for o in olay_o if o["zaman"] == z and o.get("evren", True) and f(o)]; ora = np.array([o["oran"] for o in X], float); ok = ora[np.isfinite(ora)]
            r = {"n": len(X), "n_oran": int(len(ok)), "hisse": len({o["sembol"] for o in X})}
            for e in es:
                r[f"pay_le_{e:.2f}"] = (float(np.mean(ok <= e)) if len(ok) else None); r[f"n_le_{e:.2f}"] = int(np.sum(ok <= e))
            kg = [o for o in X if hk_kapi(o["oran"], G)]
            r["kapi_gecen_olay"] = len(kg); r["kapi_gecen_hisse"] = len({o["sembol"] for o in kg})
            r["katman_olay"] = {v: sum(o["katman"] == v for o in kg) for v in HK_KATMAN.values()}
            r["pazar_kapi_gecen_hisse"] = {p: len({o["sembol"] for o in kg if o["pazar"] == p}) for p in ("ABD", "AVR", "BIST")}
            out["grup"][g][z] = r
    return out


def hk_aday_sec4(olay_o: List[Dict[str, Any]], haric: set, G: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Parti 4 seçimi: evren içi + KAPI + hariç dışı; önce haftalık sonra günlük, (sembol, tarih) sırası tohumla karışık; hisse başına bir; dilim hedefine kadar
    (yetmezse hepsi; öteki dilimle doldurulmaz); BIST tavanı yok; bütün sayfalar tohumla karışık, 1'den."""
    G = G or HK_ESIK_P4; rng = np.random.default_rng(G["tohum"]); sec: List[Dict[str, Any]] = []; gor = set(haric)
    for z in ("haftalik", "gunluk"):
        h = sorted([o for o in olay_o if o["zaman"] == z and o["evren"] and hk_kapi(o["oran"], G)], key=lambda o: (o["sembol"], o["tarih"])); n = 0
        for i in rng.permutation(len(h)):
            o = h[int(i)]
            if o["sembol"] in gor:
                continue
            sec.append(dict(o)); gor.add(o["sembol"]); n += 1
            if n >= int(G[z]):
                break
        if n < int(G[z]):
            if not G.get("eksik_izin", False):
                raise HKHata(f"{z}: yalnız {n} aday (hedef {G[z]})")
            hklog.warning("parti 4 %s: kapıdan geçen yeni aday %d < hedef %d (eksik %d; öteki dilimle doldurulmadı)", z, n, G[z], int(G[z]) - n)
    p = rng.permutation(len(sec))
    return [dict(sec[i], sayfa=j + 1) for j, i in enumerate(p)]


def hk_aday_olcek(cikti: Optional[str] = None, parti: int = 4) -> Dict[str, Any]:
    """A1 + A2: havuz sayımı ve mum boyu kapılı ölçekli aday partisi. Çıktı: <önek>_N.pdf (50'şer), <önek>_anahtar.json (mühürlü; ORAN + katman),
    mum_izi18_havuz_sayim.json (hisse adı yok)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    PT = HK_PARTI[parti]; G = PT["esik"]
    if not PT.get("olcek"):
        raise HKHata(f"parti {parti} ölçekli parti değil")
    kl = cikti or PT["klasor"]; ya = os.path.join(kl, f"{PT['onek']}_anahtar.json"); yh = os.path.join(kl, "mum_izi18_havuz_sayim.json")
    if os.path.exists(ya) or os.path.exists(yh):
        raise HKHata("aday anahtarı / havuz sayımı zaten var")
    olay = [o for o in hk_olaylar() if o["evren"]]; haric = hk_haric(parti); pb = hk_parti_bolgeleri()
    olo, sak = hk_olay_oran(olay, sakla=True)
    HV = hk_havuz_say(olo, haric, pb, G)
    sec = hk_aday_sec4(olo, haric, G)
    if not sec:
        raise HKHata("kapıdan geçen yeni aday yok")
    if max(pd.Timestamp(r["tarih"]) for r in sec) > MI.MI_KESIK:
        raise HKHata("KESİK AŞIMI")
    os.makedirs(kl, exist_ok=True)
    a = MV.mv_sablon()["tam"]["ohlc"]; dosyalar = []; anah: List[Dict[str, Any]] = []; ds = int(G["dosya_sayfa"]); aralik = {}
    for f in range(int(np.ceil(len(sec) / ds))):
        y = os.path.join(kl, f"{PT['onek']}_{f + 1}.pdf"); dosyalar.append(y); parca = sec[f * ds:(f + 1) * ds]
        aralik[os.path.basename(y)] = [parca[0]["sayfa"], parca[-1]["sayfa"]]
        with PdfPages(y, metadata={"Title": f"{PT['baslik']} {f + 1}", "CreationDate": None, "ModDate": None}) as pdf:
            for r in parca:
                d = sak[(r["zaman"], r["pazar"], r["sembol"])]
                fig = plt.figure(figsize=(8.3, 11.7)); o = _hk_sayfa_olcek(fig, d, r, a, r["sayfa"], kutular=False); pdf.savefig(fig); plt.close(fig)
                if not (o["oran"] == r["oran"]):           # aynı fonksiyon, aynı barlar: sayfadaki oran seçimdeki oranla birebir
                    raise HKHata(f"sayfa {r['sayfa']}: sayfa ORAN'ı seçim ORAN'ıyla aynı değil")
                anah.append({"sayfa": r["sayfa"], "dosya": os.path.basename(y), "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"],
                             "bolge_bas": _hk_bas(d, r), "bolge_son": r["tarih"], "pencere": int(r["m"]), "k": int(r["k"]), "v1_S": r["S"],
                             "oran": r["oran"], "katman": r["katman"], "boy_mutlak": r["boy_mutlak"], "onceki": r["onceki"], "onceki_n": r["onceki_n"]})
        hklog.info("%s yazıldı", y)
    X = pd.DataFrame(anah); nz = {z: int((X.zaman == z).sum()) for z in ("gunluk", "haftalik")}
    HJ = {"not": "EK 18 A1 havuz sayımı (getirisiz; hisse adı yok)", "surum": HK_SURUM_P4, "esik_sha": _hk_sha(G), "olcek_sha": _hk_sha(HK_ESIK_OLCEK),
          "kaynak": {"tarama8_ham_sha": MI._mi_sha(HK_YOL["ham8"]), "kural": HK_ESIK["kural"]}, "haric_hisse": len(haric), "parti_bolge": len(pb), "havuz": HV}
    MI._mi_jyaz(yh, HJ, "havuz sayımı 18")
    J = {"not": "MÜHÜRLÜ: sayfa -> hisse / bölge tarihleri / ORAN; PDF'e girmez", "surum": HK_SURUM_P4, "parti": parti, "esik_sha": _hk_sha(G),
         "olcek_sha": _hk_sha(HK_ESIK_OLCEK), "tohum": G["tohum"], "hedef": {"gunluk": G["gunluk"], "haftalik": G["haftalik"]}, "n": len(anah), "n_zaman": nz,
         "eksik": {z: max(0, int(G[z]) - nz[z]) for z in nz}, "kaynak": HJ["kaynak"], "haric_hisse": len(haric), "havuz_sayim_sha": MI._mi_sha(yh),
         "sayim": {f"{z}|{p}": int(v) for (z, p), v in X.groupby(["zaman", "pazar"]).size().items()},
         "katman": {f"{z}|{k}": int(v) for (z, k), v in X.groupby(["zaman", "katman"]).size().items()},
         "dosya_sha": {os.path.basename(y): MI._mi_sha(y) for y in dosyalar}, "dosya_sayfa": aralik, "sayfalar": anah}
    MI._mi_jyaz(ya, J, f"aday anahtar parti {parti}")
    return J


def _hk_olcek_parti_mi(klasor: str) -> bool:
    """Aday klasöründeki anahtar ölçekli bir partiye (EK 18: 4) mi ait? Bulunamazsa / okunamazsa False (eski yol aynen çalışır)."""
    try:
        ay = hk_aday_anahtar_bul(klasor); p = json.load(open(ay, encoding="utf-8")).get("parti")
    except (HKHata, OSError, ValueError, AttributeError):
        return False
    return bool(HK_PARTI.get(p, {}).get("olcek")) if isinstance(p, int) else False


def hk_onay_sec4(evet: List[Dict[str, Any]], kismen1: List[Dict[str, Any]], H2: Dict[int, Dict[str, Any]],
                 G: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """HK-O4: a / b sınıfı hk_onay_sec2 ile aynen (HK_ESIK_ONAY2); set doldur_alt'tan azsa (c) 1. aşama KISMEN, puan1 >= doldur_puan_en_az ile tamamlanır;
    sıra a, b, c; PDF sırası tohumlu. Doldurma yoksa sonuç hk_onay_sec2 ile birebir."""
    G = G or HK_ESIK_ONAY4
    ab = hk_onay_sec2(evet, H2, dict(HK_ESIK_ONAY2, en_az=0, hedef=int(G["hedef"])))
    ab = sorted([{k: v for k, v in r.items() if k != "yeni_sayfa"} for r in ab],
                key=lambda r: ({"a": 0, "b": 1}[r["sinif"]], -(float(r["hakem_puan"]) + float(r["hakem2_puan"])), int(r["sayfa"])))
    c: List[Dict[str, Any]] = []
    if len(ab) < int(G["doldur_alt"]):
        var = {int(r["sayfa"]) for r in ab}
        aday = sorted([r for r in kismen1 if float(r["hakem_puan"]) >= float(G["doldur_puan_en_az"]) and int(r["sayfa"]) not in var],
                      key=lambda r: (-float(r["hakem_puan"]), int(r["sayfa"])))
        for r in aday[:int(G["doldur_alt"]) - len(ab)]:
            h2 = H2.get(int(r["sayfa"]))
            c.append(dict(r, hakem2_karar=(h2 or {}).get("karar"), hakem2_puan=(h2 or {}).get("puan"), hakem2_gerekce=(h2 or {}).get("gerekce"), sinif="c"))
        if c:
            hklog.warning("set %d < %d: 1. aşama KISMEN (puan >= %s) %d sayfayla tamamlandı", len(ab), G["doldur_alt"], G["doldur_puan_en_az"], len(c))
    sec = ab + c
    if len(sec) < int(G["en_az"]):
        raise HKHata(f"ölçekli onay seti {len(sec)} sayfa: kurulmadı")
    p = np.random.default_rng(G["tohum"]).permutation(len(sec))
    return [dict(sec[i], yeni_sayfa=j + 2) for j, i in enumerate(p)]


def hk_onay_olcek_yeni(hakem: List[str], cikti: Optional[str] = None, aday_klasor: Optional[str] = None, kapak: Optional[str] = None,
                       ad: Optional[str] = None, hakem2: Optional[str] = None, G: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """A4: ölçekli partiden (4) YENİ onay seti (eski ölçeksiz set yok). İki aşamalı seçim (HK-O4). Çıktı: <ad>_ONAY_OLCEKLI.pdf, <ad>_onay_anahtar.json
    (mühürlü; hisse / tarih / hakem), <ad>_onay_olcekli.json (hisse adı / tarih yok). Kapılar (DUR): --ad ve --hakem2 zorunlu; çıktılar yok; hakem dosyaları
    bütün aday sayfalarını kapsar ve yabancı sayfa yok; sayfa ORAN'ı aday anahtarındaki ORAN'la aynı."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    G = G or HK_ESIK_OLCEK; cikti = cikti or HK_YOL["cikti"]
    if not ad or not hakem2:
        raise HKHata("ölçekli partiden yeni onay: --ad ve --hakem2 zorunlu")
    y = os.path.join(cikti, f"{ad}_ONAY_OLCEKLI.pdf"); ya = os.path.join(cikti, f"{ad}_onay_anahtar.json"); yj = os.path.join(cikti, f"{ad}_onay_olcekli.json")
    if any(os.path.exists(x) for x in (y, ya, yj)):
        raise HKHata(f"ölçekli onay PDF / anahtar / json zaten var: {y}")
    ay = hk_aday_anahtar_bul(aday_klasor or HK_YOL["aday"]); A = json.load(open(ay, encoding="utf-8")); Ad = {int(r["sayfa"]): r for r in A["sayfalar"]}
    H = hk_hakem_oku(hakem); H2 = hk_hakem_oku([hakem2])
    for ad_, HH in (("1. aşama", H), ("2. aşama", H2)):
        yab = sorted(set(HH) - set(Ad))
        if yab:
            raise HKHata(f"{ad_} hakem dosyasında aday listesinde olmayan sayfalar: {yab[:10]}")
    eks = sorted(set(Ad) - set(H))
    if eks:
        raise HKHata(f"1. aşama hakem dosyaları {len(eks)} aday sayfasını kapsamıyor: {eks[:10]}")
    evet = [dict(Ad[n], hakem_puan=v["puan"], hakem_gerekce=v["gerekce"]) for n, v in sorted(H.items()) if v["karar"] == "EVET"]
    kis = [dict(Ad[n], hakem_puan=v["puan"], hakem_gerekce=v["gerekce"]) for n, v in sorted(H.items()) if v["karar"] == "KISMEN"]
    sec = hk_onay_sec4(evet, kis, H2); N2 = sum(1 for r in evet if H2.get(int(r["sayfa"]), {}).get("karar") == "EVET"); C = sum(r["sinif"] == "c" for r in sec)
    M = len(H); N = len(evet)
    kapak_t = hk_kapak_metni(kapak, M, N, len(sec), N2) if kapak is not None else HK_KAPAK4.format(M=M, N=N, N2=N2, K=len(sec))
    if C:
        kapak_t = f"{kapak_t} {HK_KAPAK4_DOLDUR.format(C=C)}"
    a = MV.mv_sablon()["tam"]["ohlc"]; Vc: Dict[Any, Any] = {}; os.makedirs(cikti, exist_ok=True); olc: List[Dict[str, Any]] = []
    with PdfPages(y, metadata={"Title": f"{ad} onay (ölçekli)", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.06, 0.95, "GÖRSEL HAKEMİN SEÇTİĞİ BÖLGELER", fontsize=16, weight="bold")
        fig.text(0.06, 0.88, kapak_t, fontsize=13, va="top", wrap=True)
        MV._mv_ciz(fig.add_axes([0.25, 0.2, 0.5, 0.35]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
        pdf.savefig(fig); plt.close(fig)
        for r in sorted(sec, key=lambda r: r["yeni_sayfa"]):
            k = (r["zaman"], r["pazar"])
            if k not in Vc:
                Vc[k] = MV.mv_veri(*k)
            d = Vc[k][r["sembol"]]; rr = {"tarih": r["bolge_son"], "m": r["pencere"], "zaman": r["zaman"]}
            if _hk_bas(d, rr) != r["bolge_bas"]:
                raise HKHata(f"aday sayfa {r['sayfa']}: bölge başı anahtarla uyuşmuyor")
            fig = plt.figure(figsize=(8.3, 11.7)); o = _hk_sayfa_olcek(fig, d, rr, a, r["yeni_sayfa"], G); pdf.savefig(fig); plt.close(fig)
            if "oran" in r and not (o["oran"] == r["oran"]):
                raise HKHata(f"aday sayfa {r['sayfa']}: ORAN aday anahtarıyla aynı değil")
            olc.append(dict(o, yeni_sayfa=r["yeni_sayfa"], zaman=r["zaman"], katman=r.get("katman")))
    pdf_sha = MI._mi_sha(y); szam = pd.Series([r["zaman"] for r in sec], dtype=object).value_counts().to_dict()
    ss = {s: sum(r["sinif"] == s for r in sec) for s in ("a", "b", "c")}
    K = {"not": "MÜHÜRLÜ: yeni sayfa -> aday sayfası / hakem kararları / hisse / tarihler; PDF'e girmez", "surum": HK_SURUM_P4,
         "surum_onay": HK_ESIK_ONAY4["surum"], "esik_onay4_sha": _hk_sha(HK_ESIK_ONAY4), "esik_onay2_sha": _hk_sha(HK_ESIK_ONAY2), "esik_olcek_sha": _hk_sha(G),
         "tohum": HK_ESIK_ONAY4["tohum"], "hakem_dosyalari": {os.path.basename(h): MI._mi_sha(h) for h in hakem},
         "hakem2_dosyasi": {os.path.basename(hakem2): MI._mi_sha(hakem2)}, "aday_anahtari": os.path.basename(ay), "aday_anahtar_sha": MI._mi_sha(ay),
         "kapak": kapak_t, "aday_bakilan": M, "hakem_evet": N, "hakem2_bakilan": len(H2), "iki_hakem_evet": N2, "secilen": len(sec), "secilen_zaman": szam,
         "secilen_sinif": ss, "doldurulan": C, "pdf": os.path.basename(y), "pdf_sha": pdf_sha,
         "sayfalar": [{"yeni_sayfa": r["yeni_sayfa"], "aday_sayfa": r["sayfa"], "hakem_karar": H[int(r["sayfa"])]["karar"], "hakem_puan": r["hakem_puan"],
                       "hakem_gerekce": r["hakem_gerekce"], "hakem2_karar": r["hakem2_karar"], "hakem2_puan": r["hakem2_puan"], "hakem2_gerekce": r["hakem2_gerekce"],
                       "sinif": r["sinif"], "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "bolge_bas": r["bolge_bas"], "bolge_son": r["bolge_son"],
                       "pencere": r["pencere"], "oran": r.get("oran"), "katman": r.get("katman")} for r in sorted(sec, key=lambda r: r["yeni_sayfa"])]}
    MI._mi_jyaz(ya, K, "onay anahtar 18 (ölçekli)")
    J = {"not": "EK 18 A4: ölçekli partiden yeni onay seti; hisse adı / tarih YOK", "surum": HK_SURUM_P4, "esik_olcek": G["surum"], "esik_olcek_sha": _hk_sha(G),
         "esik_onay4_sha": _hk_sha(HK_ESIK_ONAY4), "pdf": os.path.basename(y), "pdf_sha": pdf_sha, "sayfa_sayisi": len(sec) + 1, "anahtar": os.path.basename(ya),
         "anahtar_sha": MI._mi_sha(ya), "aday_anahtar_sha": MI._mi_sha(ay), "kapak": kapak_t, "secilen_zaman": szam, "secilen_sinif": ss, "doldurulan": C,
         "olcu": {k: G[k] for k in ("boy", "sinir", "eksen")}, "sayfalar": olc}
    MI._mi_jyaz(yj, J, "ölçekli onay 18")
    hklog.info("ölçekli onay (yeni): %d adaya bakıldı, 1. aşama EVET %d, iki hakem EVET %d, seçilen %d (doldurulan %d) -> %s", M, N, N2, len(sec), C, y)
    return dict(J, aday_bakilan=M, hakem_evet=N, iki_hakem_evet=N2, secilen=len(sec))


def hk_ogren_liste2(G: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """A3 örnek listesi. Denetimler (DUR): etiket sayfaları tam olarak aralık; etiket sınıfı EVET / KISMEN / HAYIR; etiket zamanı anahtardakiyle aynı; anahtarın
    pdf_sha'sı özgün PDF'le (varsa) ya da ölçekli json'daki eski_anahtar_sha anahtarla (varsa) aynı. Sıra: grup, sınıf, kaynak, sayfa."""
    G = G or HK_OGREN2; out: List[Dict[str, Any]] = []
    for gi, g in enumerate(G["gruplar"]):
        for ki, k in enumerate(g["kaynak"]):
            for y in [k["etiket"], k["anahtar"]] + [k[x] for x in ("pdf", "olcekli_json") if k.get(x)]:
                if not os.path.exists(y):
                    raise HKHata(f"öğrenme kaynağı yok: {y}")
            A = json.load(open(k["anahtar"], encoding="utf-8"))
            if k.get("pdf") and MI._mi_sha(k["pdf"]) != A.get("pdf_sha"):
                raise HKHata(f"{os.path.basename(k['anahtar'])}: özgün PDF sha'sı anahtarla uyuşmuyor")
            if k.get("olcekli_json") and json.load(open(k["olcekli_json"], encoding="utf-8")).get("eski_anahtar_sha") != MI._mi_sha(k["anahtar"]):
                raise HKHata(f"{os.path.basename(k['anahtar'])}: ölçekli json'daki anahtar sha'sı uyuşmuyor")
            a0, a1 = (int(x) for x in k["sayfa"]); As = {int(r["yeni_sayfa"]): r for r in A["sayfalar"]}
            if sorted(As) != list(range(a0, a1 + 1)):
                raise HKHata(f"{os.path.basename(k['anahtar'])}: anahtar sayfaları {a0}-{a1} değil")
            E = json.load(open(k["etiket"], encoding="utf-8")).get("sayfalar")
            if not isinstance(E, dict) or sorted(int(x) for x in E) != list(range(a0, a1 + 1)):
                raise HKHata(f"{os.path.basename(k['etiket'])}: etiket sayfaları {a0}-{a1} değil")
            for sn, v in E.items():
                s = str(v.get("isaret", "")).strip().replace("İ", "I").upper(); r = As[int(sn)]
                if s not in G["sira"]:
                    raise HKHata(f"{os.path.basename(k['etiket'])}: sayfa {sn} etiket {v.get('isaret')!r}")
                if v.get("zaman") is not None and r["zaman"] != v["zaman"]:
                    raise HKHata(f"{os.path.basename(k['etiket'])}: sayfa {sn} zamanı onay anahtarıyla uyuşmuyor")
                out.append({"grup_i": gi, "grup": g["ad"], "yazi_on": g["yazi_on"], "kaynak_i": ki, "kaynak": os.path.basename(k["etiket"]), "sayfa": int(sn),
                            "sinif": s, **{x: r[x] for x in ("zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "pencere")}})
    out.sort(key=lambda r: (r["grup_i"], G["sira"].index(r["sinif"]), r["kaynak_i"], r["sayfa"]))
    return [dict(r, ornek=i + 1) for i, r in enumerate(out)]


def hk_ogren_olcek(cikti: Optional[str] = None, ad: Optional[str] = None, G: Optional[Dict[str, Any]] = None, liste: Optional[List[Dict[str, Any]]] = None,
                   veri=None) -> Dict[str, Any]:
    """A3: her bölge ölçekli çizimle (kutusuz, başlık 'Örnek n') yeniden çizilir; sayfa üstten şerit kadar genişletilir; şeritte '<grup yazısı>: <sınıf>' ve
    'Örnek n / N'. Hisse / tarih eklenmez; grafik örtülmez."""
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pypdf
    from pypdf import PageObject, Transformation
    G = G or HK_OGREN2; cikti = cikti or HK_YOL["cikti"]; y = os.path.join(cikti, ad or G["ad"]); veri = veri or MV.mv_veri
    if os.path.exists(y):
        raise HKHata(f"öğrenme dosyası zaten var: {y}")
    L = liste if liste is not None else hk_ogren_liste2(G); N = len(L); bant = float(G["serit_pt"]); W = pypdf.PdfWriter(); Vc: Dict[Any, Any] = {}
    a = MV.mv_sablon()["tam"]["ohlc"]; olc: List[Dict[str, Any]] = []
    for r in L:
        k = (r["zaman"], r["pazar"])
        if k not in Vc:
            Vc[k] = veri(*k)
        d = Vc[k].get(r["sembol"])
        if d is None:
            raise HKHata(f"örnek {r['ornek']}: seri yok")
        rr = {"tarih": r["bolge_son"], "m": r["pencere"], "zaman": r["zaman"]}
        if _hk_bas(d, rr) != r["bolge_bas"]:
            raise HKHata(f"örnek {r['ornek']}: bölge başı anahtarla uyuşmuyor")
        b = io.BytesIO(); fig = plt.figure(figsize=(8.3, 11.7))
        o = _hk_sayfa_olcek(fig, d, rr, a, r["ornek"], kutular=False,
                            baslik=f"Örnek {r['ornek']}: bulunan bölge ({'haftalık' if r['zaman'] == 'haftalik' else 'günlük'} mum)")
        fig.savefig(b, format="pdf", metadata={"CreationDate": None, "ModDate": None}); plt.close(fig)
        b.seek(0); src = pypdf.PdfReader(b).pages[0]; mb = src.mediabox; w = float(mb.width); h = float(mb.height)
        yeni = PageObject.create_blank_page(width=w, height=h + bant)
        yeni.merge_transformed_page(src, Transformation().translate(-float(mb.left), -float(mb.bottom)))
        yeni.merge_transformed_page(_hk_serit(w, bant, f"{r['yazi_on']}: {G['yazi'][r['sinif']]}", G["renk"][r["sinif"]], f"Örnek {r['ornek']} / {N}",
                                              fs=float(G["fs"]), sag_fs=float(G["sag_fs"])), Transformation().translate(0, h))
        W.add_page(yeni); olc.append({"ornek": r["ornek"], "grup": r["grup"], "sinif": r["sinif"], "oran": o["oran"]})
    W.add_metadata({"/Title": "MUM_IZI18 öğrenme dosyası (ölçekli, Cemal etiketli)"})
    os.makedirs(cikti, exist_ok=True)
    with open(y, "wb") as f:
        W.write(f)
    sinif = {g["ad"]: {s: sum(1 for r in L if r["grup"] == g["ad"] and r["sinif"] == s) for s in G["sira"]} for g in G["gruplar"]}
    hklog.info("ölçekli öğrenme dosyası: %d örnek %s -> %s", N, sinif, y)
    return {"n": N, "sinif": sinif, "cikti": y, "sha": MI._mi_sha(y), "olcu": olc}


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
    ap.add_argument("komut", choices=["aday", "onay", "ogren", "havuz"])
    ap.add_argument("--hakem", nargs="+", default=None, help="hakem json dosyaları (onay)")
    ap.add_argument("--cikti", default=None, help="çıktı klasörü (varsayılan arastirma_cikti/mum_izi; aday için hakem_aday)")
    ap.add_argument("--aday", default=None, help="aday klasörü (onay; içinde tek '*anahtar*.json'; varsayılan arastirma_cikti/mum_izi/hakem_aday)")
    ap.add_argument("--hakem2", default=None, help="2. aşama hakem json'u (onay; verilirse iki aşamalı seçim)")
    ap.add_argument("--parti", type=int, default=1, help="aday partisi (aday; 1 = hakem_aday, 2 = hakem_aday2, 3 = hakem_aday3, 4 = hakem_aday4: EK 18 mum boyu kapılı, ölçekli)")
    ap.add_argument("--kapak", default=None, help="onay kapak metni ({M} bakılan aday, {N} hakem EVET, {K} PDF'e giren sayfa, {N2} iki hakemin de EVET dediği)")
    ap.add_argument("--ad", default=None, help="onay çıktı öneki: <önek>_ONAY.pdf, <önek>_onay_anahtar.json (varsayılan eski adlar)")
    ap.add_argument("--olcek", action="store_true", help="onay: EK 16 ölçekli yeniden basım (yüzde ekseni, mum boyu satırı, üç kutu); eski anahtar gerekir; "
                                                          "<önek>_ONAY_OLCEKLI.pdf + <önek>_onay_olcekli.json. Aday klasörü ölçekli partiyse (4) YENİ set "
                                                          "(+ <önek>_onay_anahtar.json). ogren: EK 18 ölçekli öğrenme dosyası (MUM_IZI18_OGREN.pdf)")
    a = ap.parse_args(argv)
    try:
        if a.komut == "aday":
            J = hk_aday(a.cikti, a.parti)
            print(json.dumps({k: J[k] for k in ("parti", "n", "n_zaman", "eksik", "sayim", "katman", "dosya_sayfa", "tohum") if k in J}, ensure_ascii=False))
        elif a.komut == "ogren":
            J = hk_ogren_olcek(cikti=a.cikti) if a.olcek else hk_ogren(cikti=a.cikti)
            print(json.dumps({k: J[k] for k in ("n", "sinif", "cikti")}, ensure_ascii=False))
        elif a.komut == "havuz":                            # EK 18 A1: yalnız sayım (yazmaz, hisse adı yok)
            if not HK_PARTI.get(a.parti, {}).get("olcek"):
                raise HKHata("havuz: --parti ölçekli parti olmalı (4)")
            olo, _ = hk_olay_oran([o for o in hk_olaylar() if o["evren"]])
            print(json.dumps(hk_havuz_say(olo, hk_haric(a.parti), hk_parti_bolgeleri(), HK_PARTI[a.parti]["esik"]), ensure_ascii=False, indent=1))
        else:
            if not a.hakem:
                raise HKHata("--hakem en az bir dosya ister")
            if a.olcek:
                J = hk_onay(a.hakem, a.cikti, a.aday, a.kapak, a.ad, a.hakem2, olcek=True)
                print(json.dumps({k: J[k] for k in ("pdf", "pdf_sha", "sayfa_sayisi", "eski_anahtar_sha", "bolge_kimligi", "aday_bakilan", "hakem_evet",
                                                    "iki_hakem_evet", "secilen", "secilen_sinif", "doldurulan") if k in J}, ensure_ascii=False)); return 0
            K = hk_onay(a.hakem, a.cikti, a.aday, a.kapak, a.ad, a.hakem2)
            print(json.dumps({k: K[k] for k in ("aday_bakilan", "hakem_evet", "secilen", "secilen_zaman", "tohum") + (("iki_hakem_evet", "secilen_sinif")
                                                                                                                    if a.hakem2 else ())}, ensure_ascii=False))
    except HKHata as ex:
        hklog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_hk_ana())
