"""MUM_IZI_HAVUZ — MUM_IZI EK 24: KODUN SEÇTİĞİ BÖLGELER (aday kuralı havuzu + mum boyu kapısı ORAN <= 0,70), göz onayı olmadan, 15 mumluk sonrası (26 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI24_IS_TANIMI.md (commit 5826f37; ana model). Başlık her yerde 'KODUN SEÇTİĞİ BÖLGELER': Cemal'in göz onayı (geçmişli
sayfa, 24 bölge) kodun gösterdiği bölgelerin %42'sine BENZİYOR, %75'ine BENZİYOR ya da KISMEN dedi; bu yüzden sonuç 'kalıbın sonucu' DEĞİLDİR.

OLAYLAR: MUM_IZI8 taramasının v5M ('R4+M') VAR, evren içi olayları (MUM_IZI_HAKEM.hk_olaylar; ham dosya mühürlü). ORAN = MUM_IZI_HAKEM.hk_olay_oran /
hk_boy_olcu (yalnız bölge sonu t'ye kadarki barlar); KAPILI = HK.hk_kapi (ORAN <= 0,70, sınır dahil); KAPISIZ = ORAN sonlu ve > 0,70 (aynı havuz, K1 kontrol).
ANA ÖRNEK = daha önce sonrası ölçülmüş / gösterilmiş bölgeler (mum_izi21_olay.csv 181 + MUM_IZI22 onay 24) HARİÇ; DUYARLILIK = hepsi dahil.
ÖLÇÜ: MUM_IZI_GOZ (MUM_IZI11) tanımları AYNEN: gz_olc_bir (giriş = bölgeden sonraki ilk geçerli bar açılışı, R15, stop = bölge dibi x 0,98, dokunma), haftalık
+%5 MUM_IZI_GOZ2.k17_dokunma; eş = GZ.gz_es_grup (CETVEL2 v2.2 konum eşi; aynı giriş günü, aynı kova, aynı takvim aralığı, >= 5 eş).
HÜCRE: C2.c2_hucre (FARK, ay kümeli bootstrap, SIRA, ay kümeli işaret permütasyonu) + 10 yuvalı slot portföyü (BOFA_IZI.bi_slot) ve 200 eşli rastgele portföy +
güç (C2.c2_guc; günlükte cetvel2_guc_v2.2 H 15 eğrisi, haftalıkta plasebo eğrisi C2.c2_guc_egri). Hüküm iş tanımı 3. bölüm (HV_ESIK['hukum']).
Veri <= 2022-12-31 (assert + KASA kapısı). KASA AÇILMAZ. Mevcut modüller (MUM_IZI*, CETVEL2, BOFA_IZI) DEĞİŞTİRİLMEZ; içe alınır.

Komut:  python MUM_IZI_HAVUZ.py sayim      GETİRİSİZ SAYIM (yalnız yazdırır + /tmp/mum_izi/havuz/sayim.json)
        python MUM_IZI_HAVUZ.py onkayit    MUM_IZI24_ON_KAYIT.md (sayım + mühürler + kontrol tablosu)
        python MUM_IZI_HAVUZ.py kos        kapı (kontrol + ön kayıt sha + commit + temiz ağaç + KASA) -> hesap -> mum_izi24_olay.csv.gz + mum_izi24_sonuc.json
        python MUM_IZI_HAVUZ.py rapor      MUM_IZI24_RAPOR.md tabloları (sonuç json'undan)
        python MUM_IZI_HAVUZ.py sha        kod / eşik sha
EK 25 (MUM_IZI25_IS_TANIMI.md; rastgele gün tabanı, zamanlama / seçim, piyasa tahmini; EK 24 kodu ve çıktıları değişmez):
        python MUM_IZI_HAVUZ.py sayim25 | onkayit25 | kos25 | rapor25 | sha25
Colab:  exec(open('MUM_IZI_HAVUZ.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_HV = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_HV = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_HV not in sys.path:
    sys.path.insert(0, KOK_HV)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAFTALIK as MH  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAKEM as HK  # noqa: E402  (DEĞİŞTİRİLMEZ; ORAN / kapı / havuz)
import MUM_IZI_GOZ as GZ  # noqa: E402  (DEĞİŞTİRİLMEZ; ölçü / eş)
import MUM_IZI_GOZ2 as G2  # noqa: E402  (DEĞİŞTİRİLMEZ; k17_gecit_bir, k17_dokunma)

hvlog = logging.getLogger("col.mum_izi_havuz")
if not hvlog.handlers:
    _hv_h = logging.StreamHandler(sys.stderr)
    _hv_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_havuz: %(message)s", "%H:%M:%S"))
    hvlog.addHandler(_hv_h)
    hvlog.setLevel(logging.INFO)
    hvlog.propagate = False


class HVHata(RuntimeError):
    """Durdurucu hata: kapı / şema / veri / kesik / yeniden üretim uyuşmazlığı."""


HV_SURUM = "MUM_IZI_HAVUZ v1.0 (2026-11-26): EK 24 kodun seçtiği bütün bölgeler (aday kuralı + mum boyu kapısı), 15 mumluk sonrası"
_C = MI.MI_YOL["cikti"]
HV_YOL = {"cikti": _C, "kod": os.path.join(KOK_HV, "MUM_IZI_HAVUZ.py"), "gecici": "/tmp/mum_izi/havuz",
          "haric21": os.path.join(_C, "mum_izi21_olay.csv"), "haric22": os.path.join(_C, "MUM_IZI22_onay_anahtar.json"),
          "is_tanimi": os.path.join(_C, "MUM_IZI24_IS_TANIMI.md")}
HV_DOSYA = {"onkayit": "MUM_IZI24_ON_KAYIT.md", "rapor": "MUM_IZI24_RAPOR.md", "sonuc": "mum_izi24_sonuc.json", "olay": "mum_izi24_olay.csv.gz"}
HV_KESIK = pd.Timestamp("2022-12-31")
HV_ZAMAN = ("gunluk", "haftalik")
HV_PAZAR = ("ABD", "AVR", "BIST")
HV_GRUP = ("KAPILI", "KAPISIZ")

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
HV_ESIK: Dict[str, Any] = {
    "surum": "HV-1.0",
    "havuz": "MUM_IZI8 taramasının v5M ('R4+M') VAR olayları, evren içi (HK.hk_olaylar; ham dosya sha mum_izi8_tarama.json ile); günlük ve haftalık ayrı zaman dilimi",
    "oran": "HK.hk_olay_oran (hk_boy_olcu; ORAN = bölge barlarında (H - L) / C medyanı / bölgeden önceki 120 barın medyanı, en az 40 bar; yalnız bölge sonu t'ye "
            "kadarki barlar); ikinci tanım yok",
    "kapi": {"oran_en_cok": 0.70, "tanim": "KAPILI = HK.hk_kapi(ORAN) (sonlu ve <= 0,70, sınır dahil); KAPISIZ = ORAN sonlu ve > 0,70; ORAN yok (önceki < 40 bar) "
                                          "-> 'ORAN_YOK' (iki gruba da girmez; sayısı yazılır)"},
    "tekil": {"bar": 15, "tanim": "aynı zaman dilimi ve hissede olaylar bölge sonu bar sırasıyla; son TUTULAN olaydan < 15 bar sonraki olay atılır (ilki kalır); "
                                  "havuzun tamamında (KAPILI + KAPISIZ + ORAN_YOK birlikte), kapıdan önce"},
    "haric": {"yakin_bar": 15,
              "tanim": "mum_izi21_olay.csv (181 bölge; zaman, sembol, bolge_son) + MUM_IZI22_onay_anahtar.json (24 bölge; zaman, sembol, bolge_son): aynı zaman "
                       "dilimi + aynı hisse + bölge sonu bar farkı <= 15 (tam eşleşme 0 dahil; sonrası örtüşür) -> HARİÇ (ANA ÖRNEK'e girmez; DUYARLILIK'ta "
                       "dahil); hem KAPILI hem KAPISIZ olaylarda aynı kural; tam / yakın sayıları ayrı yazılır"},
    "olcu": {"tanim": "GZ.gz_olc_bir AYNEN (GZ_ESIK['olcu']; ESIK11_SHA): giriş = bölgeden sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk "
                      "günü), ufuk 15 mum, R15 = 15. mumun kapanışı / giriş - 1, stop = bölge dibi x 0,98, giriş <= stop ölçülmez, 15. mum > 2022-12-31 "
                      "ölçülmez (ufuk_kesik), dokunma = High >= giriş x (1 + x) ilk gün Low <= stop ilk günden ÖNCE (aynı gün stop önce)",
             "hedef": "+%5 ve +%10 her iki dilimde: günlük GZ d5 / d10; haftalık d10 = GZ d10, d5 = G2.k17_dokunma (aynı kural; denetim: k17_dokunma +%10 = GZ "
                      "d10, değilse DUR)",
             "getirisiz_gecit": "G2.k17_gecit_bir (gz_olc_bir kapıları aynen; getiri hesaplamaz); hesapta gz_olc_bir ile birebir aynı olmalı (DUR)"},
    "es": {"tanim": "GZ.gz_es_grup AYNEN (CETVEL2 v2.2 c2_panel22_al ufuk 15 önbelleksiz; aynı giriş günü, aynı kova KV, >= 5 eş, aynı takvim aralığı, eş stop'u "
                    "bölge takvim aralığında eşin dibi x 0,98, giriş > stop); panel GZ.gz_es kuralı (günlük açık kopya; haftalık bölge sonu <= 2015-12-31 -> p1, "
                    "değilse açık kopya; BIST p1 yok -> panel_yok); eş hedefleri +%5 / +%10 için olay satırı gz_es_grup'a zaman 'gunluk' ile verilir (gz_es_grup "
                    "zamanı yalnız hedef listesi için okur)",
           "dislama": "aynı gün KAPILI ya da KAPISIZ (ya da ORAN_YOK) olayı olan hisseler eşten dışlanır: o pazardaki havuzun BÜTÜN olaylarının (iki zaman "
                      "dilimi, hariç dahil) giriş günleri; olayın kendisi gz_es_grup içinde dışlanır",
           "uye": "slot portföyü ve güç plasebosu için eş üyelerinin R'leri hv_es_uye ile (gz_es_grup'un uygunluk adımları aynen); denetim: üye sayısı = n_es ve üye "
                  "ortalaması = es_R15 (1e-9), değilse DUR"},
    "hucre": {"donem": {"o16": ["1990-01-01", "2015-12-31"], "d1619": ["2016-01-01", "2019-12-31"], "d2022": ["2020-01-01", "2022-12-31"]},
              "atama": "giriş tarihine göre (pazar x dönem)", "karar": ["ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022"],
              "bilgi": ["BIST|d1619", "BIST|d2022", "ABD|o16", "AVR|o16", "BIST|o16"]},
    "istat": {"c2_hucre": "C2.c2_hucre(R15, es_R15, sira, giris, '+', tohum_ek, egri=None, perm=True): n (eşli), ort / medyan FARK, ort SIRA, AY KÜMELİ bootstrap "
                          "%95 (YH.yh_d3_boot_l3o; C2_ESIK boot B 2000, tohum 2111), p = DS.ds_perm_p ay kümeli işaret permütasyonu (R 10.000, tohum 2113 + "
                          "tohum_ek, tek yönlü +); L3O yalnız bilgi (hükme girmez)",
              "tohum_ek": "zaman 0 / 1 x 1000 + grup (KAPILI 0, KAPISIZ 1, KAPILI_DUY 2, KAPISIZ_DUY 3) x 100 + hücre sırası (karar 0-3, bilgi 4-8, hepsi 9)",
              "hedef_payi": "+%5 payı (d5) ve +%10 payı (d10) ölçülen olaylarda; EŞLİ HEDEF PAYI = eşli olaylarda d5 payı - es_d5 ortalaması (d10 aynı)",
              "esinden_iyi": "fark > 0 payı (eşli olaylar)"},
    "slot": {"yuva": 10, "rastgele": 200, "tohum": 26112401, "esik": 0.90,
             "tanim": "BOFA_IZI.bi_slot AYNEN: eşli olaylar giriş günü sırasıyla (eşitlikte sembol), yuva serbest ise (önceki çıkış günü <= giriş günü) alınır, "
                      "15. mumun son günü çıkar, getiri R15; rastgele: her olay yerine aynı gün aynı kovadan rastgele bir eş üyesinin R'si (aynı giriş / çıkış "
                      "günleri), 200 portföy; YÜZDELİK = rastgele portföylerin gerçekten küçük olanlarının payı; şart: gerçek > rastgelelerin %90 yüzdeliği "
                      "(np.quantile 0,90)"},
    "guc": {"delta": 0.02, "esik": 0.80, "tohum": 26112402,
            "gunluk": "C2.c2_guc(n, C2._c2_egri22_al(pazar, dönem, 15, None)) (cetvel2_guc_v2.2.json H 15; 'o16' -> 'acik' eğrisi)",
            "haftalik": "cetvel2'de 15 haftalık ufuk yok -> plasebo eğrisi: hücrenin ANA olaylarının (KAPILI + KAPISIZ) >= 6 üyeli her eş kümesinden rastgele bir "
                        "üye (tohum 26112402), fark = üye R - öteki üyelerin ortalaması; C2.c2_guc_egri(fark, tohum_ek) ve C2.c2_guc(n, eğri); olay getirisi "
                        "kullanılmaz",
            "bilgi": "günlükte plasebo eğrisi güçü de bilgi olarak yazılır"},
    "hukum": {"tutar": "n >= 30 VE ort FARK > 0 VE ay kümeli boot alt > 0 VE ort SIRA > 0,50 VE slot portföyü > 200 rastgele portföyün %90 yüzdeliği",
              "tutmadi": "TUTAR değil VE n >= 30 VE güç >= 0,80", "olculemedi": "ötekiler (n < 30 ya da güç < 0,80)",
              "anlamli": "pozitif anlamlı = n >= 30, FARK > 0, boot alt > 0; negatif anlamlı = n >= 30, FARK < 0, boot üst < 0",
              "genel": "zaman dilimi başına dört karar hücresi: (1) en az bir pozitif anlamlı VE en az bir negatif anlamlı -> 'ÇELİŞKİLİ'; (2) dördü TUTAR -> "
                       "'AÇIK VERİDE TUTUYOR (birleşik iz bileşeni adayı; kasa açılmaz)'; (3) en az biri TUTMADI ve hiçbiri TUTAR değil -> 'TUTMADI'; (4) "
                       "ötekiler -> 'ÖLÇÜLEMEDİ' (eksik hücreler yazılır)",
              "ornek": "hüküm ANA ÖRNEK KAPILI ile; DUYARLILIK (hepsi dahil) ayrı satır; KAPISIZ bilgi"},
    "kapi_etkisi": {"perm": 10000, "tohum": 26112403, "boot": 2000, "tohum_boot": 26112404,
                    "tanim": "KAPILI - KAPISIZ ort eşli FARK farkı (ANA örnek; eşli olaylar); p = tabakalı permütasyon: grup etiketleri (pazar x giriş ayı) "
                             "tabakaları içinde karıştırılır, iki yönlü, 10.000; %95 = giriş ayı kümeli bootstrap (aylar yerine koyarak, B 2000); zaman "
                             "dilimine göre (bütün pazar / dönemler) ve dört karar hücresinde ayrı"},
    "bh": {"q": 0.10, "aile": "2 zaman dilimi x 4 karar hücresi (ANA KAPILI); p = c2_hucre p (ay kümeli işaret, tek yönlü +); BİLGİ satırı (hükme girmez)"},
    "kesik": "veri en büyük tarihi <= 2022-12-31 (assert, her blok) + KASA.kasa_kapisi (gz_kos ile aynı dosyalar)",
}

HV_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = GZ.gz_es_grup (aynı giriş günü, aynı kova, aynı takvim aralığı, aynı stop geometrisi, >= 5 eş); eş dışlama havuzun bütün olayları "
                   "(KAPILI + KAPISIZ + ORAN_YOK, iki zaman dilimi); slot tabanı 200 eşli rastgele portföy (aynı gün aynı kova); aynı bağlam kontrolü KAPISIZ = "
                   "aynı aday kuralının ORAN > 0,70 olayları (KAPI ETKİSİ, tabakalı permütasyon)"),
    "K2": ("EVET", "ORAN yalnız bölge sonu t'ye kadarki barlardan (HK.hk_boy_olcu assert); aday kuralı olayları tarama anında o güne kadarki veriyle; giriş "
                   "bölgeden SONRAKİ ilk geçerli bar açılışı; eş kovası giriş günü KV satırı; hariç listesi ve kapı getiriden bağımsız; veri <= 2022-12-31 "
                   "assert + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0); haftalık barlar tamamlanmış ISO haftaları (MH / MV aynen); GZ kapıları aynen"),
    "K4": ("EVET", "aynı hissede < 15 bar arayla ikinci olay atılır (hv_tekil; havuz tekil ise 0 yazılır); bölge kimliği zaman + sembol + bölge sonu tekil (DUR); "
                   "ortalama yanında medyan"),
    "K5": ("EVET", "giriş = bölgeden sonraki ilk geçerli barın açılışı (gz_olc_bir; haftalıkta sonraki haftanın ilk günü açılışı); giriş <= stop ölçülmez "
                   "(sayısı yazılır)"),
    "K6": ("EVET", "MI bölünme düzeltmeli fiyatlar (GZ aynen); getiriler oransal; ABD USD, AVR yerel para, BIST TL; karar eşli farkla (aynı pazar aynı gün)"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı): sonuç 'yukarı yanlı' okunur; eşli fark aynı evrenle kurulduğu için yanlılık kısmen "
                   "düşer, kalkmaz; kasa açılmaz"),
    "K8": ("EVET", "n < 30 hücre ÖLÇÜLEMEDİ (getirisiz sayımda beklenen yazılır); iki alt dönem (2016-19, 2020-22) ve iki pazar ayrı hücre; BH q 0,10 bilgi "
                   "satırı (2 x 4 aile); küçük hücreden 'bulgu' denmez"),
    "K9": ("EVET", "MUM_IZI24_ON_KAYIT.md: KOD24_SHA, ESIK24_SHA, GZ / G2 / HK / MI kod sha, ham havuz sha, hariç dosya sha, SAYIM_SHA + getirisiz sayım + güç; "
                   "getiriler bu commit + push'tan sonra; hv_kapi: kontrol kapısı + sha + commit + temiz ağaç + sayım eşitliği"),
    "K10": ("EVET", "havuz ham dosyası mühürle (HK.hk_olaylar); olay indeksi taramayla (hk_olay_oran DUR); hariç dosyalarının şeması (sütun / anahtar) denetlenir; "
                    "bölge kimliği tekil (DUR); bölge başı / sonu / giriş / 15. mum tarihleri getirisiz ve hesap aşamasında birebir (DUR)"),
    "K11": ("EVET", "getirisiz geçit = gz_olc_bir (DUR); k17_dokunma +%10 = GZ d10 (DUR); eş üyeleri = gz_es_grup n_es / es_R15 (DUR); rapordan önce >= 2 hücre "
                    "olay csv'sinden bağımsız kısa kodla yeniden üretilir"),
    "K12": ("EVET", "başlık 'KODUN SEÇTİĞİ BÖLGELER'; 'kalıbın sonucu' denmez (göz onayı %42 BENZİYOR / %75 BENZİYOR ya da KISMEN); 'iz' sözü yalnız hüküm "
                    "kuralıyla; sayı ile yorum ayrı cümlede"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_hv); MUM_IZI_HAKEM / GOZ / GOZ2 ve defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; "
                    "sızıntı taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez, kasa açılmaz"),
}


# ================================================================ 0) YARDIMCI
def _hv_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or HV_YOL["cikti"], HV_DOSYA[ad])


def hv_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or HV_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def hv_json_sha(J: Any) -> str:
    return hashlib.sha256(json.dumps(MI._mi_json(J), sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def hv_kesik_kapi(V: Dict[str, pd.DataFrame], ad: str = "veri", kesik: pd.Timestamp = HV_KESIK) -> pd.Timestamp:
    """Kasa kapısı (mekanik): verideki en büyük tarih kesiği aşarsa DUR."""
    if not V:
        raise HVHata(f"{ad}: veri boş")
    en = max(pd.Timestamp(d.index.max()) for d in V.values() if len(d))
    if en > kesik:
        raise HVHata(f"KESİK AŞIMI: {ad} en geç {en.date()} > {kesik.date()} (KASA açılmaz)")
    return en


def hv_grup(oran: Any) -> str:
    """KAPILI = HK.hk_kapi (sınır dahil <= 0,70); KAPISIZ = sonlu ve > 0,70; ORAN yok -> ORAN_YOK."""
    if HK.hk_kapi(oran):
        return "KAPILI"
    try:
        x = float(oran)
    except (TypeError, ValueError):
        return "ORAN_YOK"
    return "KAPISIZ" if np.isfinite(x) else "ORAN_YOK"


def hv_tekil(X: pd.DataFrame, bar: Optional[int] = None) -> Tuple[pd.DataFrame, int]:
    """Aynı (zaman, sembol): bölge sonu bar indeksi t sırasıyla; son tutulandan < bar sonraki olay atılır."""
    bar = int(bar if bar is not None else HV_ESIK["tekil"]["bar"])
    if not len(X):
        return X.copy(), 0
    X = X.sort_values(["zaman", "sembol", "t"], kind="stable"); tut = np.ones(len(X), bool); son: Dict[Tuple[str, str], int] = {}
    for i, (z, s, t) in enumerate(zip(X.zaman, X.sembol, X.t.astype(int))):
        k = (z, s)
        if k in son and t - son[k] < bar:
            tut[i] = False; continue
        son[k] = t
    return X[tut].reset_index(drop=True), int((~tut).sum())


def hv_hucre_ad(giris: Any, pazar: str) -> str:
    """Giriş tarihine göre 'pazar|dönem' (HV_ESIK['hucre']['donem']); hiçbiri değilse 'pazar|dis'."""
    g = pd.Timestamp(giris)
    for ad, (a, b) in HV_ESIK["hucre"]["donem"].items():
        if pd.Timestamp(a) <= g <= pd.Timestamp(b):
            return f"{pazar}|{ad}"
    return f"{pazar}|dis"


def hv_haric_liste() -> List[Dict[str, Any]]:
    """Hariç bölgeler: mum_izi21_olay.csv (181) + MUM_IZI22 onay anahtarı (24). Şema denetlenir."""
    A = pd.read_csv(HV_YOL["haric21"])
    for c in ("zaman", "sembol", "bolge_son", "pazar"):
        if c not in A:
            raise HVHata(f"K10: {os.path.basename(HV_YOL['haric21'])} sütun yok: {c}")
    K = json.load(open(HV_YOL["haric22"], encoding="utf-8")).get("sayfalar")
    if not isinstance(K, list) or not all({"zaman", "sembol", "bolge_son", "pazar"} <= set(r) for r in K):
        raise HVHata("K10: MUM_IZI22 anahtar şeması")
    out = [{"kaynak": "mum_izi21", "zaman": r.zaman, "pazar": r.pazar, "sembol": r.sembol, "bolge_son": str(r.bolge_son)} for r in A.itertuples()]
    out += [{"kaynak": "mum_izi22", "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "bolge_son": str(r["bolge_son"])} for r in K]
    if len(out) != 205:
        raise HVHata(f"K10: hariç bölge sayısı {len(out)} (beklenen 181 + 24)")
    return out


def hv_haric_isaretle(X: pd.DataFrame, H: List[Dict[str, Any]], bar_ix: Dict[Tuple[str, str], pd.DatetimeIndex],
                      yakin: Optional[int] = None) -> pd.DataFrame:
    """Olay -> haric ('tam' / 'yakin' / ''). bar_ix[(zaman, sembol)] = o hissenin o zaman dilimindeki bar takvimi (bölge sonu tarihleri burada aranır;
    tarih takvimde yoksa önceki son bar)."""
    yakin = int(yakin if yakin is not None else HV_ESIK["haric"]["yakin_bar"])
    hk: Dict[Tuple[str, str], List[int]] = {}; tam = set()
    for h in H:
        k = (h["zaman"], h["sembol"]); tam.add((h["zaman"], h["sembol"], str(pd.Timestamp(h["bolge_son"]).date())))
        ix = bar_ix.get(k)
        if ix is None or not len(ix):
            continue
        p = int(ix.searchsorted(pd.Timestamp(h["bolge_son"]), side="right")) - 1
        if p >= 0:
            hk.setdefault(k, []).append(p)
    X = X.copy(); hr = []
    for z, s, tr, t in zip(X.zaman, X.sembol, X.tarih, X.t.astype(int)):
        if (z, s, str(pd.Timestamp(tr).date())) in tam:
            hr.append("tam"); continue
        L = hk.get((z, s), [])
        hr.append("yakin" if any(abs(t - p) <= yakin for p in L) else "")
    X["haric"] = hr
    return X


def hv_tarihler(Dg: pd.DataFrame, W: Optional[pd.DataFrame], r: Dict[str, Any]) -> Dict[str, Any]:
    """Getirisiz takvim: gz_olc_bir'in tarih arama adımları (bölge başı, bölge sonu, giriş günü, 15. mum günü); fiyat okunmaz."""
    U = int(GZ.GZ_ESIK["olcu"]["ufuk"]); B = W if r["zaman"] == "haftalik" else Dg
    t = int(B.index.get_loc(pd.Timestamp(r["tarih"]))); s = t - int(r["m"]) + 1
    out: Dict[str, Any] = {"bolge_bas": (W.bas.iloc[s] if r["zaman"] == "haftalik" else Dg.index[s]), "bolge_son": Dg.index[Dg.index.get_loc(B.index[t])],
                           "giris": None, "son15": None}
    if t + 1 < len(B):
        out["giris"] = W.bas.iloc[t + 1] if r["zaman"] == "haftalik" else Dg.index[t + 1]
    if t + U < len(B):
        out["son15"] = B.index[t + U]
    return out


# ================================================================ 1) VERİ BLOKLARI
def hv_blok(zaman: str, pazar: str) -> Tuple[Dict[str, pd.DataFrame], Optional[Dict[str, pd.DataFrame]], Dict[str, pd.DataFrame]]:
    """(Vd günlük, W haftalık ya da None, Vb ORAN serisi) — GZ / MV yükleyicileri aynen; kesik assert."""
    if zaman == "gunluk":
        Vd = MI.mi_veri(pazar, MV.MV_YOL["gunluk"])["V"]; hv_kesik_kapi(Vd, f"{zaman} {pazar}")
        return Vd, None, {s: d for s, d in Vd.items() if len(d) >= 40}
    Vd = MI.mi_veri(pazar, MH.MH_YOL["tam"])["V"]; hv_kesik_kapi(Vd, f"{zaman} {pazar}")
    W = MV.mv_haftalik_panel(Vd)
    return Vd, W, W


# ================================================================ 2) HAVUZ (GETİRİSİZ)
def hv_havuz() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Havuz + ORAN + grup + tekil + hariç + getirisiz geçit + takvim. Getiri hesaplanmaz."""
    ham = [o for o in HK.hk_olaylar() if o["evren"]]
    X0 = pd.DataFrame(ham)
    if X0.duplicated(["zaman", "sembol", "tarih"]).any():
        raise HVHata("K4: havuzda aynı bölge iki kez")
    X, atilan = hv_tekil(X0); H = hv_haric_liste(); parca = []; huni: Dict[str, Any] = {"ham_evren": int(len(X0)), "tekil_atilan": atilan}
    for z in HV_ZAMAN:
        for p in HV_PAZAR:
            B = X[(X.zaman == z) & (X.pazar == p)]
            if not len(B):
                continue
            Vd, W, Vb = hv_blok(z, p)
            olo, _ = HK.hk_olay_oran(B.to_dict("records"), veri=lambda zz, pp, _V=Vb: _V)
            Y = pd.DataFrame(olo)
            Y["grup"] = [hv_grup(o) for o in Y.oran]
            bix = {(z, s): Vb[s].index for s in {h["sembol"] for h in H if h["zaman"] == z} if s in Vb}
            Y = hv_haric_isaretle(Y, H, bix)
            gc_, tr = [], []
            for r in Y.to_dict("records"):
                Dg = Vd[r["sembol"]]; Wr = W[r["sembol"]] if W is not None else None
                g = G2.k17_gecit_bir(Dg, Wr, r, MI.MI_KESIK); T = hv_tarihler(Dg, Wr, r)
                if str(pd.Timestamp(g["bolge_bas_bar"]).date()) != str(pd.Timestamp((Wr if z == "haftalik" else Dg).index[int(r["t"]) - int(r["m"]) + 1]).date()):
                    raise HVHata("K10: bölge başı uyuşmuyor")
                gc_.append(g); tr.append(T)
            Y["olculebilir"] = [bool(g["olculebilir"]) for g in gc_]; Y["neden"] = [g["neden"] for g in gc_]
            for c in ("bolge_bas", "bolge_son", "giris", "son15"):
                Y[c] = [t_[c] for t_ in tr]
            Y["hucre"] = [hv_hucre_ad(g_, p) if g_ is not None else f"{p}|yok" for g_ in Y.giris]
            parca.append(Y); del Vd, W, Vb; gc.collect()
            hvlog.info("havuz: %s %s %d olay (KAPILI %d)", z, p, len(Y), int((Y.grup == "KAPILI").sum()))
    X = pd.concat(parca, ignore_index=True)
    X["ana"] = X.haric == ""
    return X, huni


def _hv_panel_ad(zaman: str, bolge_son: Any) -> str:
    return "acik" if zaman == "gunluk" or pd.Timestamp(bolge_son) > pd.Timestamp("2015-12-31") else "p1"


_HV_PANEL_KLASOR = {"acik": MV.MV_YOL["gunluk"], "p1": MH.MH_YOL["p1"]}


def hv_gun_olay(Pn: Dict[str, Any], X: pd.DataFrame, pazar: str) -> Dict[int, set]:
    """Eş dışlama: o pazardaki havuzun BÜTÜN olaylarının giriş günleri (iki zaman dilimi, bütün gruplar, hariç dahil)."""
    idx = Pn["P"]["tarih"]; kol = Pn["P"]["kol"]; gun: Dict[int, set] = {}
    for s, g in zip(X.sembol[X.pazar == pazar], X.giris[X.pazar == pazar]):
        if g is None or (isinstance(g, float) and not np.isfinite(g)) or pd.isna(g) or s not in kol:
            continue
        try:
            d = idx.get_loc(pd.Timestamp(g))
        except KeyError:
            continue
        gun.setdefault(int(d), set()).add(kol[s])
    return gun


def hv_es_uye(Pn: Dict[str, Any], X: pd.DataFrame, gun_olay: Dict[int, set]) -> List[Dict[str, Any]]:
    """gz_es_grup'un uygunluk adımları AYNEN (olay getirisi okunmaz): kova, dışlama, >= 5 üye, üye R (aynı takvim aralığı) ve stop uygunluğu.
    Döner her olay için {es_neden_u, kova_u, uye_R (np.ndarray)}."""
    P = Pn["P"]; idx = P["tarih"]; kol = P["kol"]; KV = Pn["KV"]; Op, Lo, Cl = P["Op"], P["Lo"], Pn["Cl"]
    sc = float(GZ.GZ_ESIK["olcu"]["stop_carpan"]); mn = int(GZ.GZ_ESIK["es"]["min"]); out = []
    for r in X.itertuples():
        rec: Dict[str, Any] = {"es_neden_u": "", "kova_u": np.nan, "uye_R": np.array([])}
        j = kol.get(r.sembol)
        try:
            d = idx.get_loc(pd.Timestamp(r.giris)); e = idx.get_loc(pd.Timestamp(r.son15)); a = idx.get_loc(pd.Timestamp(r.bolge_bas)); tt = idx.get_loc(pd.Timestamp(r.bolge_son))
        except KeyError:
            rec["es_neden_u"] = "panel_tarih_yok"; out.append(rec); continue
        if j is None or KV[d, j] < 0:
            rec["es_neden_u"] = "kova_yok"; out.append(rec); continue
        kv = int(KV[d, j]); rec["kova_u"] = kv
        uye = np.flatnonzero((KV[d] == kv) & np.isfinite(Op[d]) & (Op[d] > 0)); dis = gun_olay.get(d, set())
        uye = np.array([u for u in uye if u != j and u not in dis], np.int64)
        if len(uye) < mn:
            rec["es_neden_u"] = "es_az"; out.append(rec); continue
        E = Op[d, uye]; c = Cl[d:e + 1, uye]; okc = np.isfinite(c)
        sonk = np.where(okc.any(0), c.shape[0] - 1 - np.argmax(okc[::-1], axis=0), -1)
        Rr = np.where(sonk >= 0, c[np.maximum(sonk, 0), np.arange(len(uye))] / E - 1, np.nan)
        with np.errstate(all="ignore"):
            st = np.nanmin(Lo[a:tt + 1, uye], axis=0) * sc
        ok = np.isfinite(Rr) & np.isfinite(st) & (E > st)
        if ok.sum() < mn:
            rec["es_neden_u"] = "es_az"; out.append(rec); continue
        rec["uye_R"] = Rr[ok].astype(float); out.append(rec)
    return out


def hv_es_hazirla(X: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[Tuple[str, str], Dict[int, set]]]:
    """Getirisiz eş uygunluğu (ölçülebilir olaylar): panel, kova, üye R'leri. X'e es_neden_u, kova_u, n_uye, panel ekler; üye R'leri '_uye' sütununda."""
    import CETVEL2 as C2
    X = X.copy(); X["panel"] = None; X["es_neden_u"] = None; X["kova_u"] = np.nan; X["n_uye"] = 0; X["_uye"] = None
    m = X.olculebilir.astype(bool)
    X.loc[m, "panel"] = [_hv_panel_ad(z, b) for z, b in zip(X.zaman[m], X.bolge_son[m])]
    X.loc[~m, "es_neden_u"] = "olculemedi"; gunler: Dict[Tuple[str, str], Dict[int, set]] = {}
    for (pz, pn), g in X[m].groupby(["pazar", "panel"]):
        if not os.path.exists(os.path.join(_HV_PANEL_KLASOR[pn], f"V_{pz}.pkl")):
            X.loc[g.index, "es_neden_u"] = "panel_yok"; continue
        Pn = C2.c2_panel22_al(pz, _HV_PANEL_KLASOR[pn], 15, onbellek=False)
        gun = hv_gun_olay(Pn, X, pz); gunler[(pz, pn)] = gun
        U = hv_es_uye(Pn, g, gun)
        X.loc[g.index, "es_neden_u"] = [u["es_neden_u"] for u in U]; X.loc[g.index, "kova_u"] = [u["kova_u"] for u in U]
        X.loc[g.index, "n_uye"] = [len(u["uye_R"]) for u in U]
        for i, u in zip(g.index, U):
            X.at[i, "_uye"] = u["uye_R"]
        del Pn; gc.collect(); hvlog.info("eş üyeleri: %s %s %d olay", pz, pn, len(g))
    X["esli_u"] = X.es_neden_u.fillna("") == ""
    return X, gunler


# ================================================================ 3) GÜÇ
def hv_plasebo_fark(uyeler: List[np.ndarray], tohum: int) -> np.ndarray:
    """Her >= 6 üyeli eş kümesinden rastgele bir üye: üye R - öteki üyelerin ortalaması (olay getirisi kullanılmaz)."""
    rng = np.random.default_rng(int(tohum)); out = []
    for u in uyeler:
        u = np.asarray(u, float)
        if len(u) < 6:
            continue
        k = int(rng.integers(len(u))); out.append(float(u[k] - np.delete(u, k).mean()))
    return np.asarray(out, float)


def _hv_hucre_sira(hc: str) -> int:
    L = HV_ESIK["hucre"]["karar"] + HV_ESIK["hucre"]["bilgi"]
    return L.index(hc) if hc in L else 9


def hv_egri(X: pd.DataFrame, zaman: str, hc: str) -> Dict[str, Any]:
    """Güç eğrileri: günlük cetvel2 (H 15), haftalık + günlük bilgi plasebo eğrisi (hücrenin ANA KAPILI + KAPISIZ eş kümeleri)."""
    import CETVEL2 as C2
    pz, dn = hc.split("|"); out: Dict[str, Any] = {"cetvel2": None, "plasebo": None}
    if zaman == "gunluk":
        out["cetvel2"] = C2._c2_egri22_al(pz, "acik" if dn == "o16" else dn, 15, None)
    g = X[(X.zaman == zaman) & (X.hucre == hc) & X.ana & X.grup.isin(HV_GRUP) & X.esli_u]
    f = hv_plasebo_fark(list(g._uye), int(HV_ESIK["guc"]["tohum"]) + 7 * HV_ZAMAN.index(zaman) + _hv_hucre_sira(hc))
    if len(f) >= 3:
        out["plasebo"] = C2.c2_guc_egri(f, tohum_ek=100 * HV_ZAMAN.index(zaman) + _hv_hucre_sira(hc)); out["plasebo"]["n_kume"] = int(len(f))
    return out


def hv_guc(n: int, zaman: str, eg: Dict[str, Any]) -> Dict[str, float]:
    import CETVEL2 as C2
    gc2 = C2.c2_guc(int(n), eg.get("cetvel2")) if (n > 0 and eg.get("cetvel2")) else float("nan")
    gpl = C2.c2_guc(int(n), eg.get("plasebo")) if (n > 0 and eg.get("plasebo")) else float("nan")
    return {"guc": (gc2 if zaman == "gunluk" else gpl), "guc_cetvel2": gc2, "guc_plasebo": gpl}


# ================================================================ 4) GETİRİSİZ SAYIM
def hv_sayim(X: pd.DataFrame) -> Dict[str, Any]:
    """Zaman dilimi x grup x örnek (ANA / HEPSİ) x hücre: toplam, ölçülebilen, eşli; güç ve beklenen hüküm (ANA KAPILI)."""
    out: Dict[str, Any] = {"zaman": {}, "hucre": {}}
    hucreler = HV_ESIK["hucre"]["karar"] + HV_ESIK["hucre"]["bilgi"]
    for z in HV_ZAMAN:
        Z = X[X.zaman == z]; r: Dict[str, Any] = {"havuz": int(len(Z)), "ORAN_YOK": int((Z.grup == "ORAN_YOK").sum()),
                                                  "oran_olan": int(Z.grup.isin(HV_GRUP).sum())}
        r["kapili_pay"] = float((Z.grup == "KAPILI").sum()) / r["oran_olan"] if r["oran_olan"] else None
        for gp in HV_GRUP:
            G = Z[Z.grup == gp]
            r[gp] = {"toplam": int(len(G)), "haric_tam": int((G.haric == "tam").sum()), "haric_yakin": int((G.haric == "yakin").sum()),
                     "ANA": int(G.ana.sum()), "ANA_olculebilen": int((G.ana & G.olculebilir).sum()), "ANA_esli": int((G.ana & G.esli_u).sum()),
                     "HEPSI_olculebilen": int(G.olculebilir.sum()), "HEPSI_esli": int(G.esli_u.sum()),
                     "olculemedi": G[~G.olculebilir.astype(bool)].neden.value_counts().to_dict(),
                     "es_yok": G[G.olculebilir.astype(bool) & ~G.esli_u].es_neden_u.value_counts().to_dict(),
                     "pazar_ANA_esli": G[G.ana & G.esli_u].pazar.value_counts().to_dict(),
                     "en_gec_15_mum": str(pd.Timestamp(G[G.olculebilir.astype(bool)].son15.max()).date()) if G.olculebilir.any() else None}
        out["zaman"][z] = r
        for hc in hucreler + ["hepsi"]:
            eg = hv_egri(X, z, hc) if hc != "hepsi" else {}
            q: Dict[str, Any] = {}
            for gp in HV_GRUP:
                G = Z[(Z.grup == gp) & ((Z.hucre == hc) if hc != "hepsi" else True)]
                n_ana = int((G.ana & G.esli_u).sum()); n_hep = int(G.esli_u.sum())
                q[gp] = {"ANA_olculebilen": int((G.ana & G.olculebilir).sum()), "ANA_esli": n_ana, "HEPSI_esli": n_hep}
                if hc != "hepsi":
                    q[gp].update({f"ANA_{k}": v for k, v in hv_guc(n_ana, z, eg).items()})
                    q[gp].update({f"HEPSI_{k}": v for k, v in hv_guc(n_hep, z, eg).items()})
            if hc != "hepsi":
                gk = q["KAPILI"]["ANA_guc"]; nk = q["KAPILI"]["ANA_esli"]
                q["beklenen_ANA_KAPILI"] = ("hükme açık (n >= 30, güç >= 0,80)" if (nk >= 30 and np.isfinite(gk) and gk >= 0.80)
                                            else ("beklenen ÖLÇÜLEMEDİ (n < 30)" if nk < 30 else "beklenen ÖLÇÜLEMEDİ ya da TUTAR (güç < 0,80: TUTMADI yazılamaz)"))
                q["egri"] = {k: ({kk: v[kk] for kk in ("N", "a", "b") if kk in v} if v else None) for k, v in eg.items()}
            out["hucre"][f"{z}|{hc}"] = q
    return out


# ================================================================ 5) HESAP
def hv_olc(X: pd.DataFrame) -> pd.DataFrame:
    """Ölçülebilir olaylar: GZ.gz_olc_bir AYNEN + d5 (haftalık k17_dokunma); getirisiz geçit / takvim ile birebir (DUR)."""
    X = X.copy(); kol = ["E0", "stop", "R15", "max15", "min15", "stop15", "d5", "d10", "R30"]
    for c in kol:
        X[c] = np.nan
    X["olculdu"] = False
    for z in HV_ZAMAN:
        for p in HV_PAZAR:
            B = X[(X.zaman == z) & (X.pazar == p)]
            if not len(B):
                continue
            Vd, W, _ = hv_blok(z, p)
            for i, r in zip(B.index, B.to_dict("records")):
                Dg = Vd[r["sembol"]]; Wr = W[r["sembol"]] if W is not None else None
                rec = GZ.gz_olc_bir(Dg, Wr, r, MI.MI_KESIK)
                if bool(rec["olculdu"]) != bool(r["olculebilir"]) or (not rec["olculdu"] and rec["neden"] != r["neden"]):
                    raise HVHata(f"K11: gz_olc_bir getirisiz geçitle uyuşmuyor ({z} {p} {r['neden']} / {rec['neden']})")
                for c in ("bolge_bas", "bolge_son"):
                    if pd.Timestamp(rec[c]) != pd.Timestamp(r[c]):
                        raise HVHata(f"K10: {c} takvimi uyuşmuyor")
                if not rec["olculdu"]:
                    continue
                if pd.Timestamp(rec["giris"]) != pd.Timestamp(r["giris"]) or pd.Timestamp(rec["son15"]) != pd.Timestamp(r["son15"]):
                    raise HVHata("K10: giriş / 15. mum takvimi uyuşmuyor")
                X.loc[i, "olculdu"] = True
                for c in ("E0", "stop", "R15", "max15", "min15", "stop15", "R30"):
                    X.loc[i, c] = rec.get(c, np.nan)
                if z == "gunluk":
                    X.loc[i, "d5"] = rec["d5"]; X.loc[i, "d10"] = rec["d10"]
                else:
                    gi = Dg.index.get_loc(pd.Timestamp(rec["giris"])); ei = Dg.index.get_loc(pd.Timestamp(rec["son15"]))
                    Hs = Dg.High.to_numpy(float)[gi:ei + 1]; Ls = Dg.Low.to_numpy(float)[gi:ei + 1]
                    if G2.k17_dokunma(Hs, Ls, float(rec["E0"]), float(rec["stop"]), 0.10) != float(rec["d10"]):
                        raise HVHata("K11: haftalık +%10 k17_dokunma GZ d10 ile uyuşmuyor")
                    X.loc[i, "d10"] = rec["d10"]; X.loc[i, "d5"] = G2.k17_dokunma(Hs, Ls, float(rec["E0"]), float(rec["stop"]), 0.05)
            del Vd, W; gc.collect(); hvlog.info("ölçü: %s %s %d olay", z, p, len(B))
    return X


def hv_es(X: pd.DataFrame) -> pd.DataFrame:
    """GZ.gz_es_grup AYNEN (zaman 'gunluk' verilerek +%5 / +%10 eş hedefleri) + üye R'leri (hv_es_uye) ve birebir denetim."""
    import CETVEL2 as C2
    X = X.copy()
    for c in ("kova", "n_es", "es_R15", "es_med", "fark", "sira", "es_max15", "es_min15", "es_d5", "es_d10", "es_stop15"):
        X[c] = np.nan
    X["es_neden"] = None; X["_uye"] = None
    m = X.olculdu.astype(bool)
    for (pz, pn), g in X[m].groupby(["pazar", "panel"]):
        if not os.path.exists(os.path.join(_HV_PANEL_KLASOR[pn], f"V_{pz}.pkl")):
            X.loc[g.index, "es_neden"] = "panel_yok"; continue
        Pn = C2.c2_panel22_al(pz, _HV_PANEL_KLASOR[pn], 15, onbellek=False); gun = hv_gun_olay(Pn, X, pz)
        gg = g.copy(); gg["zaman"] = "gunluk"
        E = GZ.gz_es_grup(Pn, gg, gun); U = hv_es_uye(Pn, g, gun)
        for i, u in zip(g.index, U):
            e = E.loc[i]; ok = isinstance(e.get("es_neden"), str) and e["es_neden"] == "" and np.isfinite(float(e.get("fark", np.nan)))
            if ok != (u["es_neden_u"] == ""):
                raise HVHata(f"K11: eş uygunluğu gz_es_grup ile uyuşmuyor ({pz} {pn})")
            if ok and (int(e["n_es"]) != len(u["uye_R"]) or abs(float(e["es_R15"]) - float(np.mean(u["uye_R"]))) > 1e-9):
                raise HVHata(f"K11: eş üyeleri gz_es_grup n_es / es_R15 ile uyuşmuyor ({pz} {pn})")
            for c in ("kova", "n_es", "es_R15", "es_med", "fark", "sira", "es_max15", "es_min15", "es_d5", "es_d10", "es_stop15"):
                if c in e.index:
                    X.loc[i, c] = e[c]
            X.loc[i, "es_neden"] = e.get("es_neden") if not ok else ""
            X.at[i, "_uye"] = u["uye_R"] if ok else None
        del Pn; gc.collect(); hvlog.info("eş: %s %s %d olay", pz, pn, len(g))
    X.loc[~m, "es_neden"] = "olculemedi"
    X["esli"] = np.isfinite(X.fark.astype(float))
    if not (X.esli == X.esli_u).all():
        raise HVHata("K11: eşli olay kümesi getirisiz sayımdaki ile aynı değil")
    return X


def hv_slot(g: pd.DataFrame, tohum: int) -> Dict[str, Any]:
    """bi_slot gerçek + 200 eşli rastgele portföy (aynı gün aynı kova üyeleri)."""
    import BOFA_IZI as BI
    S = HV_ESIK["slot"]; g = g[g.esli].copy()
    if not len(g):
        return {"slot": np.nan, "slot_p90": np.nan, "slot_yuzdelik": np.nan, "slot_gecti": False}
    g["_g"] = pd.to_datetime(g.giris); g = g.sort_values(["_g", "sembol"], kind="stable")
    gi = g._g.to_numpy().astype("datetime64[D]").astype(np.int64); ci = pd.to_datetime(g.son15).to_numpy().astype("datetime64[D]").astype(np.int64)
    gercek = BI.bi_slot(gi, ci, g.R15.to_numpy(float), int(S["yuva"])); rng = np.random.default_rng(int(tohum)); U = list(g._uye)
    rast = np.array([BI.bi_slot(gi, ci, np.array([float(u[rng.integers(len(u))]) for u in U]), int(S["yuva"])) for _ in range(int(S["rastgele"]))])
    p90 = float(np.quantile(rast, float(S["esik"])))
    return {"slot": float(gercek), "slot_p50": float(np.quantile(rast, 0.5)), "slot_p90": p90, "slot_yuzdelik": float((rast < gercek).mean()),
            "slot_gecti": bool(gercek > p90)}


def hv_hukum(c: Dict[str, Any]) -> Dict[str, Any]:
    f = lambda k: c.get(k) is not None and np.isfinite(float(c.get(k)))  # noqa: E731
    n = int(c.get("n", 0) or 0); neden = []
    if n < 30:
        neden.append("n < 30")
    if not (f("fark") and c["fark"] > 0):
        neden.append("FARK <= 0")
    if not (f("boot_alt") and c["boot_alt"] > 0):
        neden.append("boot alt <= 0")
    if not (f("sira") and c["sira"] > 0.50):
        neden.append("SIRA <= 0,50")
    if not c.get("slot_gecti", False):
        neden.append("slot <= %90")
    gk = c.get("guc"); gucok = gk is not None and np.isfinite(float(gk)) and float(gk) >= float(HV_ESIK["guc"]["esik"])
    h = "TUTAR" if not neden else ("TUTMADI" if (n >= 30 and gucok) else "ÖLÇÜLEMEDİ")
    poz = bool(n >= 30 and f("fark") and c["fark"] > 0 and f("boot_alt") and c["boot_alt"] > 0)
    neg = bool(n >= 30 and f("fark") and c["fark"] < 0 and f("boot_ust") and c["boot_ust"] < 0)
    return {"hukum": h, "neden": "; ".join(neden) if neden else "bütün şartlar", "poz_anlamli": poz, "neg_anlamli": neg}


def hv_hucre(g: pd.DataFrame, zaman: str, tohum_ek: int, eg: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    import CETVEL2 as C2
    o = g[g.olculdu.astype(bool)]; e = o[o.esli]
    c = C2.c2_hucre(e.R15.to_numpy(float), e.es_R15.to_numpy(float), e.sira.to_numpy(float), pd.to_datetime(e.giris).to_numpy(), "+", tohum_ek=tohum_ek,
                    egri=None, perm=True)
    out = {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in c.items() if k in ("n", "fark", "med", "sira", "boot_alt", "boot_ust", "l3o", "p",
                                                                                                     "r15_ort", "r15_med", "es_ort", "ay")}
    out.update({"n_olculen": int(len(o)), "n_eşsiz": int(len(o) - len(e)), "R15_ort_olculen": float(o.R15.mean()) if len(o) else None,
                "R15_med_olculen": float(o.R15.median()) if len(o) else None,
                "d5": float(o.d5.mean()) if len(o) else None, "d10": float(o.d10.mean()) if len(o) else None, "stop": float(o.stop15.mean()) if len(o) else None,
                "esinden_iyi": float((e.fark > 0).mean()) if len(e) else None})
    if len(e):
        out.update({"d5_esli": float(e.d5.mean()), "es_d5": float(e.es_d5.mean()), "esli_hedef5": float(e.d5.mean() - e.es_d5.mean()),
                    "d10_esli": float(e.d10.mean()), "es_d10": float(e.es_d10.mean()), "esli_hedef10": float(e.d10.mean() - e.es_d10.mean())})
    out.update(hv_slot(g[g.olculdu.astype(bool)], int(HV_ESIK["slot"]["tohum"]) + int(tohum_ek)))
    out.update(hv_guc(int(out["n"]), zaman, eg) if eg else {"guc": float("nan"), "guc_cetvel2": float("nan"), "guc_plasebo": float("nan")})
    out.update(hv_hukum(out))
    return out


def hv_tabaka_perm(a: np.ndarray, b: np.ndarray, ta: np.ndarray, tb: np.ndarray, R: int, tohum: int) -> Optional[float]:
    """İki yönlü tabakalı permütasyon p: etiketler tabaka içinde karıştırılır (tabaka bileşimi korunur)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return None
    z = np.r_[a, b]; lab = np.r_[np.ones(len(a), bool), np.zeros(len(b), bool)]; t = np.r_[np.asarray(ta, object), np.asarray(tb, object)]
    _, tk = np.unique(t.astype(str), return_inverse=True); o0 = np.argsort(tk, kind="stable"); ls = lab[o0]
    obs = abs(a.mean() - b.mean()); rng = np.random.default_rng(int(tohum)); say = 0; na = len(a)
    for _ in range(int(R)):
        perm = np.lexsort((rng.random(len(z)), tk)); L = np.empty(len(z), bool); L[perm] = ls
        say += int(abs(z[L].sum() / na - z[~L].sum() / (len(z) - na)) >= obs - 1e-15)
    return float((1 + say) / (1 + int(R)))


def hv_ay_boot_fark(a: np.ndarray, b: np.ndarray, aa: np.ndarray, ab: np.ndarray, B: int, tohum: int) -> Optional[List[float]]:
    """Giriş ayı kümeli bootstrap: aylar yerine koyarak; her örnekte ort(a) - ort(b)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return None
    ay = np.unique(np.r_[np.asarray(aa, str), np.asarray(ab, str)]); ia = {k: i for i, k in enumerate(ay)}
    ka = np.array([ia[x] for x in np.asarray(aa, str)]); kb = np.array([ia[x] for x in np.asarray(ab, str)]); K = len(ay)
    sa = np.bincount(ka, weights=a, minlength=K); na = np.bincount(ka, minlength=K).astype(float)
    sb = np.bincount(kb, weights=b, minlength=K); nb = np.bincount(kb, minlength=K).astype(float)
    rng = np.random.default_rng(int(tohum)); W = rng.multinomial(K, np.full(K, 1.0 / K), size=int(B)).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (W @ sa) / (W @ na) - (W @ sb) / (W @ nb)
    d = d[np.isfinite(d)]
    return np.quantile(d, [0.025, 0.975]).tolist() if len(d) else None


def hv_kapi_etkisi(A: pd.DataFrame, B: pd.DataFrame, tohum_ek: int) -> Dict[str, Any]:
    K = HV_ESIK["kapi_etkisi"]; a = A[A.esli]; b = B[B.esli]
    if len(a) < 2 or len(b) < 2:
        return {"n_kapili": int(len(a)), "n_kapisiz": int(len(b)), "fark_fark": None, "p": None, "boot95": None}
    ay = lambda D: pd.to_datetime(D.giris).dt.strftime("%Y-%m").to_numpy()  # noqa: E731
    return {"n_kapili": int(len(a)), "n_kapisiz": int(len(b)), "fark_kapili": float(a.fark.mean()), "fark_kapisiz": float(b.fark.mean()),
            "fark_fark": float(a.fark.mean() - b.fark.mean()),
            "p": hv_tabaka_perm(a.fark.to_numpy(float), b.fark.to_numpy(float), (a.pazar + "|" + ay(a)).to_numpy(), (b.pazar + "|" + ay(b)).to_numpy(), int(K["perm"]),
                                int(K["tohum"]) + int(tohum_ek)),
            "boot95": hv_ay_boot_fark(a.fark.to_numpy(float), b.fark.to_numpy(float), ay(a), ay(b), int(K["boot"]), int(K["tohum_boot"]) + int(tohum_ek)),
            "esinden_iyi_kapili": float((a.fark > 0).mean()), "esinden_iyi_kapisiz": float((b.fark > 0).mean()),
            "d5_fark": float(a.d5.mean() - b.d5.mean()), "esli_hedef5_fark": float((a.d5 - a.es_d5).mean() - (b.d5 - b.es_d5).mean())}


def hv_genel(H: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    k = HV_ESIK["hucre"]["karar"]; h = {x: H.get(x, {"hukum": "ÖLÇÜLEMEDİ", "poz_anlamli": False, "neg_anlamli": False}) for x in k}
    eksik = [x for x in k if h[x]["hukum"] == "ÖLÇÜLEMEDİ"]
    if any(h[x]["poz_anlamli"] for x in k) and any(h[x]["neg_anlamli"] for x in k):
        g = "ÇELİŞKİLİ"
    elif all(h[x]["hukum"] == "TUTAR" for x in k):
        g = "AÇIK VERİDE TUTUYOR (birleşik iz bileşeni adayı; kasa açılmaz)"
    elif any(h[x]["hukum"] == "TUTMADI" for x in k) and not any(h[x]["hukum"] == "TUTAR" for x in k):
        g = "TUTMADI"
    else:
        g = "ÖLÇÜLEMEDİ"
    return {"genel": g, "hucre_hukum": {x: h[x]["hukum"] for x in k}, "olculemedi_hucre": eksik}


def _hv_bh(p: List[Optional[float]], q: float) -> List[Optional[float]]:
    ix = [i for i, x in enumerate(p) if x is not None and np.isfinite(x)]; out: List[Optional[float]] = [None] * len(p)
    if not ix:
        return out
    v = np.array([p[i] for i in ix]); o = np.argsort(v); m = len(v); adj = np.empty(m); run = 1.0
    for r in range(m - 1, -1, -1):
        run = min(run, v[o[r]] * m / (r + 1)); adj[o[r]] = run
    for k, i in enumerate(ix):
        out[i] = float(adj[k])
    return out


def hv_tablolar(X: pd.DataFrame, S: Dict[str, Any]) -> Dict[str, Any]:
    hucreler = HV_ESIK["hucre"]["karar"] + HV_ESIK["hucre"]["bilgi"]
    T: Dict[str, Any] = {"hucre": {}, "hepsi": {}, "genel": {}, "kapi_etkisi": {}, "bh": {}}
    grp = {"KAPILI": lambda D: D[(D.grup == "KAPILI") & D.ana], "KAPISIZ": lambda D: D[(D.grup == "KAPISIZ") & D.ana],
           "KAPILI_DUY": lambda D: D[D.grup == "KAPILI"], "KAPISIZ_DUY": lambda D: D[D.grup == "KAPISIZ"]}
    for zi, z in enumerate(HV_ZAMAN):
        Z = X[X.zaman == z]
        for gi, (gad, f) in enumerate(grp.items()):
            G = f(Z)
            for hc in hucreler:
                eg = hv_egri(X, z, hc)
                T["hucre"][f"{z}|{gad}|{hc}"] = hv_hucre(G[G.hucre == hc], z, 1000 * zi + 100 * gi + _hv_hucre_sira(hc), eg)
            T["hepsi"][f"{z}|{gad}"] = hv_hucre(G, z, 1000 * zi + 100 * gi + 9, None)
            T["hepsi"][f"{z}|{gad}"]["pazar_n"] = G[G.olculdu.astype(bool) & G.esli].pazar.value_counts().to_dict()
        for gad in ("KAPILI", "KAPILI_DUY"):
            T["genel"][f"{z}|{gad}"] = hv_genel({hc: T["hucre"][f"{z}|{gad}|{hc}"] for hc in HV_ESIK["hucre"]["karar"]})
        A = grp["KAPILI"](Z); Bk = grp["KAPISIZ"](Z); A = A[A.olculdu.astype(bool)]; Bk = Bk[Bk.olculdu.astype(bool)]
        T["kapi_etkisi"][f"{z}|tum"] = hv_kapi_etkisi(A, Bk, 1000 * zi + 9)
        for hc in HV_ESIK["hucre"]["karar"]:
            T["kapi_etkisi"][f"{z}|{hc}"] = hv_kapi_etkisi(A[A.hucre == hc], Bk[Bk.hucre == hc], 1000 * zi + _hv_hucre_sira(hc))
        T["kapi_etkisi"][f"{z}|karar_birlikte"] = hv_kapi_etkisi(A[A.hucre.isin(HV_ESIK["hucre"]["karar"])], Bk[Bk.hucre.isin(HV_ESIK["hucre"]["karar"])],
                                                                1000 * zi + 8)
    keys = [f"{z}|KAPILI|{hc}" for z in HV_ZAMAN for hc in HV_ESIK["hucre"]["karar"]]
    adj = _hv_bh([T["hucre"][k].get("p") for k in keys], float(HV_ESIK["bh"]["q"]))
    T["bh"] = {k: {"p": T["hucre"][k].get("p"), "p_bh": a, "bh_gecti": bool(a is not None and a <= float(HV_ESIK["bh"]["q"]))} for k, a in zip(keys, adj)}
    return T


# ================================================================ 6) KAPI, ÖN KAYIT, KOŞU
def hv_sha_simdi() -> Dict[str, str]:
    return {"KOD24_SHA": MI._mi_sha(HV_YOL["kod"]), "ESIK24_SHA": hv_esik_sha(), "HK_KOD_SHA": MI._mi_sha(HK.HK_YOL["kod"]), "GZ_KOD_SHA": MI._mi_sha(GZ.GZ_YOL["kod"]),
            "ESIK11_SHA": GZ.gz_esik_sha(), "MI_KOD_SHA": MI._mi_sha(MI.MI_YOL["kod"]), "MV_KOD_SHA": MI._mi_sha(MV.MV_YOL["kod"]),
            "MH_KOD_SHA": MI._mi_sha(MH.MH_YOL["kod"]), "HAVUZ_HAM_SHA": MI._mi_sha(HK.HK_YOL["ham8"]), "HARIC21_SHA": MI._mi_sha(HV_YOL["haric21"]),
            "HARIC22_SHA": MI._mi_sha(HV_YOL["haric22"]), "IS_TANIMI_SHA": MI._mi_sha(HV_YOL["is_tanimi"])}


def hv_sayim_kos() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    X, huni = hv_havuz(); X, _ = hv_es_hazirla(X); S = hv_sayim(X); S["huni"] = huni
    return X, S


def hv_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or HV_YOL["cikti"]; yol = _hv_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise HVHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = hv_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise HVHata(f"ön kayıt kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_HV); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise HVHata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_HAVUZ.py"]):
        raise HVHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def _hv_f(x: Any, n: int = 2, yuzde: bool = False) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    return (f"{v * 100:+.{n}f}" if yuzde else f"{v:.{n}f}").replace(".", ",")


def hv_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or HV_YOL["cikti"]; y = _hv_yol("onkayit", cikti)
    if os.path.exists(y):
        raise HVHata("ön kayıt zaten var")
    X, S = hv_sayim_kos(); sh = hv_sha_simdi(); sh["SAYIM_SHA"] = hv_json_sha(S)
    os.makedirs(HV_YOL["gecici"], exist_ok=True); MI._mi_jyaz(os.path.join(HV_YOL["gecici"], "sayim.json"), S, "sayım 24")
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in HV_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_HAVUZ.py"])
    sat = []
    for z in HV_ZAMAN:
        r = S["zaman"][z]
        sat.append(f"- {z}: havuz {r['havuz']} (ORAN olan {r['oran_olan']}, ORAN_YOK {r['ORAN_YOK']}; KAPILI payı {_hv_f(r['kapili_pay'], 3)})")
        for gp in HV_GRUP:
            q = r[gp]
            sat.append(f"  - {gp}: toplam {q['toplam']}, hariç tam {q['haric_tam']} / yakın {q['haric_yakin']}, ANA {q['ANA']}, ANA ölçülebilen {q['ANA_olculebilen']}, "
                       f"ANA eşli {q['ANA_esli']}; hepsi ölçülebilen {q['HEPSI_olculebilen']}, hepsi eşli {q['HEPSI_esli']}; ölçülemedi "
                       f"{json.dumps(q['olculemedi'], ensure_ascii=False)}; eşsiz {json.dumps(q['es_yok'], ensure_ascii=False)}; ANA eşli pazar "
                       f"{json.dumps(q['pazar_ANA_esli'], ensure_ascii=False)}; en geç 15. mum {q['en_gec_15_mum']}")
    tb = ["| zaman | hücre | rol | KAPILI ANA ölçülebilen | KAPILI ANA eşli | güç (karar eğrisi) | güç cetvel2 / plasebo | KAPILI hepsi eşli | KAPISIZ ANA eşli | beklenen |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for z in HV_ZAMAN:
        for hc in HV_ESIK["hucre"]["karar"] + HV_ESIK["hucre"]["bilgi"]:
            q = S["hucre"][f"{z}|{hc}"]; k_ = q["KAPILI"]
            tb.append(f"| {z} | {hc} | {'KARAR' if hc in HV_ESIK['hucre']['karar'] else 'BİLGİ'} | {k_['ANA_olculebilen']} | {k_['ANA_esli']} | {_hv_f(k_['ANA_guc'])} | "
                      f"{_hv_f(k_['ANA_guc_cetvel2'])} / {_hv_f(k_['ANA_guc_plasebo'])} | {k_['HEPSI_esli']} | {q['KAPISIZ']['ANA_esli']} | {q['beklenen_ANA_KAPILI']} |")
    bek = {z: [hc for hc in HV_ESIK["hucre"]["karar"] if S["hucre"][f"{z}|{hc}"]["beklenen_ANA_KAPILI"].startswith("beklenen")] for z in HV_ZAMAN}
    s = [f"# MUM_IZI24 ÖN KAYIT — KODUN SEÇTİĞİ BÖLGELER ({MI._mi_simdi()})", "",
         "Aday kuralı havuzu (MUM_IZI8 v5M, evren içi) + mum boyu kapısı (ORAN <= 0,70) = 'kodun seçtiği bölgeler'; göz onayı YOK. Cemal'in göz onayı (geçmişli sayfa, "
         "24 bölge): kodun gösterdiği bölgelerin %42'si BENZİYOR, %75'i BENZİYOR ya da KISMEN; bu yüzden sonuç 'kalıbın sonucu' diye okunmaz. Bu dosya bütün "
         "getiriler (olay ve KAPISIZ kontrol) hesaplanmadan ÖNCE commit + push edilir; tanımlar, eşikler, hücreler ve hüküm kuralı sonra değişmez (değişirse SAPMA). "
         "Evren bugün yaşayan hisseler: sonuç yukarı yanlı. KASA açılmaz (veri <= 2022-12-31).", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_HAVUZ.py commit'i: {kc or 'yok'}", "",
         "## GETİRİSİZ SAYIM (olay ve eş getirisi hesaplanmadı; yalnız ORAN, kapı, hariç, veri kapıları, takvim, eş uygunluğu)", "",
         f"- Huni: {json.dumps(S['huni'], ensure_ascii=False)} (havuz tekilse 15 bar tekilleştirme 0 atar)", *sat, "", *tb, "",
         "- Güç: günlük karar eğrisi cetvel2_guc_v2.2 (H 15); haftalık karar eğrisi plasebo (eş üyelerinin farkı; olay getirisi kullanılmaz); delta +0,02, eşik 0,80.",
         "- Güç eğrisi bilgisi ve hücre başı ayrıntı: sayım json'u (SAYIM_SHA; /tmp/mum_izi/havuz/sayim.json, sonuç json'una da yazılır).",
         f"- BEKLENEN ÖLÇÜLEMEDİ (n < 30 ya da güç < 0,80; ölçüm yine koşulur): günlük {bek['gunluk'] or 'yok'}; haftalık {bek['haftalik'] or 'yok'}.", "",
         "## Ölçü, eş, hücre, hüküm (HV_ESIK; sha yukarıda; sonuçtan sonra değişmez)", "", "```", json.dumps(HV_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 24")


HV_OLAY_KOL = ["zaman", "pazar", "sembol", "grup", "ana", "haric", "oran", "boy_mutlak", "onceki", "onceki_n", "m", "t", "tarih", "bolge_bas", "bolge_son", "hucre",
               "olculebilir", "neden", "olculdu", "giris", "E0", "stop", "son15", "R15", "max15", "min15", "stop15", "d5", "d10", "R30", "panel", "kova", "n_es", "es_R15",
               "es_med", "fark", "sira", "es_d5", "es_d10", "es_stop15", "es_neden", "esli"]


def hv_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    t0 = time.time(); cikti = cikti or HV_YOL["cikti"]
    if os.path.exists(_hv_yol("sonuc", cikti)):
        raise HVHata("sonuç zaten var (ikinci koşu DURUR)")
    G0 = hv_kapi(cikti)
    try:
        kasa = KS.kasa_kapisi([os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in HV_PAZAR] + [os.path.join(MH.MH_YOL["tam"], f"V_{p}.pkl") for p in HV_PAZAR]
                              + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")], "2022-12-31")
    except KS.KasaHata as ex:
        raise HVHata(f"KASA kapısı KAPALI: {ex}") from ex
    X, S = hv_sayim_kos(); S_sha = hv_json_sha(S)
    if f"SAYIM_SHA: {S_sha}" not in open(_hv_yol("onkayit", cikti), encoding="utf-8").read():
        raise HVHata("getirisiz sayım ön kayıttakiyle aynı değil -> DURDU")
    X = X.drop(columns=["_uye"]); X = hv_es(hv_olc(X)); T = hv_tablolar(X, S)
    O = X.copy()
    for c in HV_OLAY_KOL:
        if c not in O:
            O[c] = np.nan
    O = O[HV_OLAY_KOL].copy()
    for c in ("tarih", "bolge_bas", "bolge_son", "giris", "son15"):
        O[c] = pd.to_datetime(O[c]).dt.strftime("%Y-%m-%d")
    O = O.sort_values(["zaman", "pazar", "sembol", "tarih"]).reset_index(drop=True)
    O.to_csv(_hv_yol("olay", cikti), index=False, float_format="%.6f", compression={"method": "gzip", "mtime": 0})
    J = {"surum": HV_SURUM, "baslik": "KODUN SEÇTİĞİ BÖLGELER", "kapi": G0, "kasa": kasa, "sayim": S, "tablo": T, "olay_sha": MI._mi_sha(_hv_yol("olay", cikti)),
         "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_hv_yol("sonuc", cikti), J, "sonuç 24")
    return J


# ================================================================ 7) RAPOR TABLOLARI
def hv_rapor_tablo(J: Dict[str, Any]) -> str:
    T = J["tablo"]; s: List[str] = []
    for z in HV_ZAMAN:
        s += [f"### {z.upper()} — KODUN SEÇTİĞİ BÖLGELER (ANA ÖRNEK, KAPILI)", "",
              "| hücre | rol | n eşli | eşli fark ort [ay kümeli %95] | medyan | ort sıra | +%5 payı / eşli hedef payı | +%10 payı / eşli | slot yüzdeliği | güç | hüküm (neden) |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for hc in HV_ESIK["hucre"]["karar"] + HV_ESIK["hucre"]["bilgi"]:
            c = T["hucre"][f"{z}|KAPILI|{hc}"]
            s.append(f"| {hc} | {'KARAR' if hc in HV_ESIK['hucre']['karar'] else 'BİLGİ'} | {c['n']} | {_hv_f(c.get('fark'), 2, True)} [{_hv_f(c.get('boot_alt'), 2, True)}; "
                     f"{_hv_f(c.get('boot_ust'), 2, True)}] | {_hv_f(c.get('med'), 2, True)} | {_hv_f(c.get('sira'), 3)} | {_hv_f(c.get('d5'), 1, True)} / "
                     f"{_hv_f(c.get('esli_hedef5'), 1, True)} | {_hv_f(c.get('d10'), 1, True)} / {_hv_f(c.get('esli_hedef10'), 1, True)} | "
                     f"{_hv_f(c.get('slot_yuzdelik'), 2)} | {_hv_f(c.get('guc'), 2)} | {c['hukum']} ({c['neden']}) |")
        g = T["genel"][f"{z}|KAPILI"]; gd = T["genel"][f"{z}|KAPILI_DUY"]
        s += ["", f"GENEL ({z}, ANA): **{g['genel']}**; ölçülemeyen karar hücreleri: {', '.join(g['olculemedi_hucre']) or 'yok'}. DUYARLILIK (hepsi dahil): {gd['genel']}.", ""]
        s += ["| hepsi birlikte | n eşli | n ölçülen | R15 ort / medyan | eşli fark ort [ay kümeli %95] | eşinden iyi payı | +%5 / eşli hedef | slot yüzdeliği | pazar |",
              "|---|---|---|---|---|---|---|---|---|"]
        for gad in ("KAPILI", "KAPISIZ", "KAPILI_DUY", "KAPISIZ_DUY"):
            c = T["hepsi"][f"{z}|{gad}"]
            s.append(f"| {gad} | {c['n']} | {c['n_olculen']} | {_hv_f(c.get('R15_ort_olculen'), 2, True)} / {_hv_f(c.get('R15_med_olculen'), 2, True)} | "
                     f"{_hv_f(c.get('fark'), 2, True)} [{_hv_f(c.get('boot_alt'), 2, True)}; {_hv_f(c.get('boot_ust'), 2, True)}] | {_hv_f(c.get('esinden_iyi'), 3)} | "
                     f"{_hv_f(c.get('d5'), 1, True)} / {_hv_f(c.get('esli_hedef5'), 1, True)} | {_hv_f(c.get('slot_yuzdelik'), 2)} | "
                     f"{json.dumps(c.get('pazar_n', {}), ensure_ascii=False)} |")
        s += ["", "| KAPI ETKİSİ (KAPILI - KAPISIZ, ANA) | n KAPILI / KAPISIZ | eşli fark KAPILI / KAPISIZ | fark farkı [ay kümeli %95] | p (tabakalı perm, iki yönlü) | "
                  "eşinden iyi KAPILI / KAPISIZ |", "|---|---|---|---|---|---|"]
        for k in ["tum", "karar_birlikte"] + HV_ESIK["hucre"]["karar"]:
            c = T["kapi_etkisi"][f"{z}|{k}"]; b = c.get("boot95") or [None, None]
            s.append(f"| {k} | {c['n_kapili']} / {c['n_kapisiz']} | {_hv_f(c.get('fark_kapili'), 2, True)} / {_hv_f(c.get('fark_kapisiz'), 2, True)} | "
                     f"{_hv_f(c.get('fark_fark'), 2, True)} [{_hv_f(b[0], 2, True)}; {_hv_f(b[1], 2, True)}] | {_hv_f(c.get('p'), 4)} | "
                     f"{_hv_f(c.get('esinden_iyi_kapili'), 3)} / {_hv_f(c.get('esinden_iyi_kapisiz'), 3)} |")
        s += ["", "| KAPISIZ (bilgi) / DUYARLILIK KAPILI hücreleri | KAPISIZ n / fark / hüküm | KAPILI hepsi dahil n / fark [%95] / hüküm |", "|---|---|---|"]
        for hc in HV_ESIK["hucre"]["karar"]:
            a = T["hucre"][f"{z}|KAPISIZ|{hc}"]; d = T["hucre"][f"{z}|KAPILI_DUY|{hc}"]
            s.append(f"| {hc} | {a['n']} / {_hv_f(a.get('fark'), 2, True)} / {a['hukum']} | {d['n']} / {_hv_f(d.get('fark'), 2, True)} [{_hv_f(d.get('boot_alt'), 2, True)}; "
                     f"{_hv_f(d.get('boot_ust'), 2, True)}] / {d['hukum']} |")
        s.append("")
    s += ["BH (q 0,10; bilgi): " + "; ".join(f"{k}: p {_hv_f(v['p'], 4)}, p_BH {_hv_f(v['p_bh'], 4)}" for k, v in T["bh"].items()), ""]
    return "\n".join(s)


def hv_rapor_yaz(cikti: Optional[str] = None) -> str:
    J = json.load(open(_hv_yol("sonuc", cikti), encoding="utf-8"))
    y = os.path.join(HV_YOL["gecici"], "rapor_tablo.md"); os.makedirs(HV_YOL["gecici"], exist_ok=True)
    return MI._mi_yaz(y, hv_rapor_tablo(J), "rapor tablo 24")


# ================================================================ 7b) EK 25 — RASTGELE GÜN TABANI (mutlak kârlılık), ZAMANLAMA / SEÇİM, PİYASA TAHMİNİ
# İş tanımı: arastirma_cikti/mum_izi/MUM_IZI25_IS_TANIMI.md (ana model; 1, 2, 2b, 3. bölüm). EK 24 kodu ve çıktıları DEĞİŞMEZ (yalnız okunur).
# Girdi: mum_izi24_olay.csv.gz (EK 24 olay satırları) + mum_izi23_olay.csv (göz ölçümü 205 bölge). Veri: hv_blok (EK 24 ile aynı yükleyici + kesik assert).
HV25_SURUM = "MUM_IZI_HAVUZ EK 25 v1.0 (2026-11-26): rastgele gün tabanı (T1 / T2 / PİYASA(t)), zamanlama / seçim ayrımı, piyasa tahmini (takvim)"
HV25_YOL = {"olay24": os.path.join(_C, "mum_izi24_olay.csv.gz"), "sonuc24": os.path.join(_C, "mum_izi24_sonuc.json"), "olay23": os.path.join(_C, "mum_izi23_olay.csv"),
            "onkayit24": os.path.join(_C, "MUM_IZI24_ON_KAYIT.md"), "is_tanimi": os.path.join(_C, "MUM_IZI25_IS_TANIMI.md"),
            "ek_kural": os.path.join(_C, "MUM_IZI23_EK_KURAL.md"), "gecici": "/tmp/mum_izi/havuz25"}
HV25_DOSYA = {"onkayit": "MUM_IZI25_ON_KAYIT.md", "rapor": "MUM_IZI25_RAPOR.md", "sonuc": "mum_izi25_sonuc.json", "olay": "mum_izi25_olay.csv.gz"}
HV25_GOZ_SINIF = {"EVET": "BENZİYOR", "KISMEN": "KISMEN", "HAYIR": "BENZEMİYOR"}

HV25_ESIK: Dict[str, Any] = {
    "surum": "HV25-1.0",
    "tohum": 2511,
    "tohum_tanim": "np.random.default_rng([2511, tür, crc32(anahtar)]); tür 1 = T1 (anahtar 'zaman|pazar|sembol|tarih|kaynak'), 2 = T2 (anahtar 'zaman|pazar|dönem'), "
                   "3 = olay bootstrap'ı (anahtar tablo adı), 4 = T2 bootstrap'ı (anahtar 'zaman|pazar|dönem'), 5 = takvim bootstrap'ı (anahtar tablo adı); sıra "
                   "bağımsız, tekrarlanabilir",
    "olcu": {"tanim": "olay ölçüsü GZ.gz_olc_bir AYNEN (EK 24 satırları; R15 / d5 / d10 olay csv'sinden; hv25_olc_dizi aynı tanımı vektörle yeniden üretir, olay "
                      "satırlarıyla R15 / E0 / stop / d5 / d10 birebir, değilse DUR); rastgele gün aynı tanım: karar barı t (bölge sonunun yerine), giriş = t + 1 barının "
                      "açılışı (haftalıkta haftanın ilk günü), R15 = t + 15 barının kapanışı / giriş - 1, stop = t - m + 1 .. t barlarının dibi x 0,98, hedef +%5 / +%10 "
                      "günlük High >= giriş x (1 + x) ilk gün, Low <= stop ilk günden ÖNCE (aynı gün stop önce; GZ / G2.k17_dokunma aynen)",
             "ufuk": 15, "stop_carpan": 0.98},
    "uygun": {"tanim": "rastgele karar barı t uygun <=> t - m + 1 >= 0; t + 15 veri içinde ve t + 15 barının tarihi <= 2022-12-31 (pencere kesiği); giriş tarihi (t + 1 "
                       "barının ilk günü) olayın DÖNEMİ içinde (giriş tarihine göre; 15. mum dönem dışına taşabilir, olaylarla aynı); giriş açılışı sonlu, > 0 ve > stop "
                       "(olaylarla aynı ölçülebilirlik); |(t + 1) - k| >= 15 her k için, k = aynı hisse aynı zaman diliminde BİLİNEN BÖLGELERİN giriş barları (EK 24 "
                       "havuzunun bütün olayları: KAPILI + KAPISIZ + ORAN_YOK, hariç dahil, ölçülemeyenler dahil; k = bölge sonu barı + 1) + göz ölçümü 205 bölge; "
                       "'15 bardan yakın' = |fark| <= 14 (15 mumluk pencereler örtüşür)",
              "yakin_bar": 15},
    "T1": {"cekim": 200, "en_az": 30, "yerine_koyma": False,
           "tanim": "olay başına aynı hisse, aynı zaman dilimi, aynı dönem, aynı m: uygun barlardan yerine koymadan 200 (uygun < 200 ise hepsi); uygun < 30 ise T1 yok "
                    "(olay T1 tablolarına girmez; sayısı yazılır); T1_R15 = çekimlerin R15 ortalaması, T1_d5 / T1_d10 = hedef payları; çekim sayısı KAPISIZ dahil "
                    "her olayda 200 (hesap vektörle; 50'ye inilmedi)"},
    "T2": {"cekim": 5000, "m": 20, "yerine_koyma": False,
           "tanim": "hücre (zaman dilimi x pazar x dönem) başına evrenin bütün (hisse, karar barı) uygun çiftlerinden (m = 20, aynı uygunluk ve dışlama kuralı) "
                    "yerine koymadan 5.000 (az ise hepsi); R15 ortalaması / medyanı, +%5 / +%10 payı; hücre başına tek sayı; belirsizliği ay kümeli bootstrap ile "
                    "(çekimlerin giriş ayları) farka katılır"},
    "piyasa": {"en_az_hisse": 5,
               "tanim": "PİYASA(t) = aynı pazarın (aynı veri: günlükte günlük açık veri, haftalıkta haftalık blok günlük verisi) olayın giriş günü açılışında işlem "
                        "gören (açılış sonlu > 0) bütün hisselerinin, olayın giriş gününden olayın 15. mum gününe kadar R'si (son geçerli kapanış / giriş açılışı - 1; "
                        "gz_es_grup'un R tanımı, kovasız) eşit ağırlıklı ortalaması; hariç: olayın hissesi ve o pazarda AYNI GÜN girişli bilinen bölgesi olan hisseler "
                        "(EK 24 havuzunun bütün olayları, iki zaman dilimi + göz 205); stop / kova şartı yok; < 5 hisse ise yok"},
    "fark": {"TOPLAM_T1": "R15 - T1_R15 (olay başına)", "TOPLAM_T2": "R15 - T2(hücre)", "ZAMANLAMA": "PİYASA(t) - T2(hücre)", "SECIM": "R15 - PİYASA(t)",
             "ozdeslik": "TOPLAM_T2 = ZAMANLAMA + SECIM (olay başına; denetim 1e-12, değilse DUR)",
             "tam_kume": "tablolar R15, T1, PİYASA(t) ve T2 hepsi olan olaylarla (TAM küme); dışarıda kalanlar sayılır; EK 24 eşli farkı (fark) aynı kümenin eşli "
                         "olaylarında yanında yazılır"},
    "boot": {"B": 10000, "kume": "giriş ayı (YYYY-AA)", "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık), ortalama = ağırlıklı toplam / "
                                                                "ağırlıklı sayı; T2 içeren farklarda her tekrarda T2 de kendi çekimlerinin giriş ayları üzerinden "
                                                                "bağımsız yeniden örneklenir; %95 = 2,5 / 97,5 yüzdelik"},
    "ornek": {"KAPILI": "EK 24 KAPILI ANA (ana örnek)", "KAPILI_DUY": "EK 24 KAPILI hepsi (hariç dahil; duyarlılık)", "KAPISIZ": "EK 24 KAPISIZ ANA (kontrol)",
              "GOZ_6_9": "mum_izi23_olay.csv set6-set9 (gerçek ölçekle işaretlenen), sınıf = 'sinif' sütunu (EVET = BENZİYOR, KISMEN, HAYIR = BENZEMİYOR), zaman "
                         "dilimleri birlikte (ayrıca zaman dilimine göre bilgi)",
              "GOZ_7_9": "set7-set9 (kapı havuzu), aynı sınıflar"},
    "hucre": {"karar": ["ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022"], "bilgi": ["BIST|d1619", "BIST|d2022", "ABD|o16", "AVR|o16", "BIST|o16"],
              "atama": "giriş tarihine göre (HV_ESIK['hucre']['donem']); ayrıca zaman dilimine göre 'hepsi birlikte'"},
    "okuma": {"MUTLAK_KARLI": "n >= 30 VE farklı ay >= 12 VE TOPLAM FARK (T1) ort > 0 ve ay kümeli alt ucu > 0; aralık sıfırı içeriyorsa AYRIŞMIYOR; üst ucu < 0 ise "
                              "RASTGELE GÜNDEN KÖTÜ; n ya da ay yetmezse ÖLÇÜLEMEDİ",
              "ZAMANLAMA": "aynı n / ay şartıyla ZAMANLAMA ort > 0 ve alt ucu > 0 -> ZAMANLAMA VAR; üst ucu < 0 -> ZAMANLAMA TERS (bilgi); aralık sıfırı içeriyorsa "
                           "AYRIŞMIYOR",
              "SECIM": "bilgi: aynı kural, etiket SEÇİM + / SEÇİM - / AYRIŞMIYOR",
              "az_donem": "en kalabalık 3 ayın olay payı > 0,30 -> 'az sayıda döneme dayanıyor' notu",
              "n_min": 30, "ay_min": 12, "az_donem_pay": 0.30},
    "goz": {"kismen_kabul": "KISMEN sınıfı (set 6-9, zaman dilimleri birlikte) TOPLAM FARK (T1) ay kümeli %95 aralık kuralıyla 'MUTLAK KÂRLI' (alt ucu > 0; n ve ay "
                            "şartı aranmaz; n < 30 -> 'ÖRNEKLEM YETERSİZ' notu) <=> KISMEN KABUL; set 7-9 aynı kuralla BİLGİ (ayrışırsa ikisi de yazılır)",
            "esli": "MUM_IZI23_EK_KURAL eşli okuma (bilgi): sınıfın EK 23 eşli farkı (csv 'fark') ortalaması, basit bootstrap %95 (10.000, tohum 2311): alt > 0 SONRASI "
                    "İYİ, üst < 0 SONRASI KÖTÜ, aksi GÖSTERİLEMEDİ",
            "tohum_esli": 2311},
    "takvim": {"pazar": ["ABD", "AVR", "BIST"], "karar_pazar": ["ABD", "AVR"], "zaman": "gunluk",
               "takvim": "pazarın günlük verisindeki bütün işlem günlerinin birleşimi (sıralı)",
               "SAYI": "SAYI(g) = bölge sonu tarihi takvimde g - 4 .. g aralığında (son 5 işlem günü, g dahil; bölge sonu <= g) olan olay sayısı; ana: KAPILI ANA "
                       "günlük olaylar (ölçülebilirlikten bağımsız); duyarlılık: KAPILI hepsi; kontrol: KAPISIZ ANA",
               "PIYASA15": "PİYASA15(g) = g + 1 (takvimde sonraki gün) açılışında işlem gören bütün hisselerin (olay dışlaması YOK) g + 1 .. g + 15 takvim günlerinde son "
                           "geçerli kapanış / g + 1 açılışı - 1, eşit ağırlıklı ortalama; < 5 hisse ise gün yok",
               "gun": "g + 1 giriş tarihi 2016-01-01 .. 2022-12-31 ve g + 15 takvim günü tarihi <= 2022-12-31; g >= 20; dönem g + 1 tarihine göre (2016-19, 2020-22); "
                      "bootstrap kümesi g'nin ayı",
               "durum": ["SAYI = 0", "SAYI = 1-2", "SAYI >= 3"],
               "farklar": ["(SAYI >= 1) - (SAYI = 0)", "(SAYI >= 3) - (SAYI = 0)"],
               "dusus": "DUS20(g) = bütün hisselerin (kapanış 5 güne kadar ileri taşınmış) Kapanış(g) / Kapanış(g - 20) - 1 eşit ağırlıklı ortalaması; DÜŞÜŞ günü <=> "
                        "DUS20 < -0,05; satır: DÜŞÜŞ günlerinde PİYASA15 (gün, ort, medyan, artı payı) ve DÜŞÜŞ - öteki günler farkı [ay kümeli %95]; bilgi: DÜŞÜŞ "
                        "günleri içinde ve dışında ayrı (SAYI >= 1) - (SAYI = 0)",
               "okuma": "ABD'de iki dönemde de (SAYI >= 1) - (SAYI = 0) > 0 ve alt ucu > 0 -> 'PİYASA YÜKSELİŞİNİ ÖNCELİYOR' (AVR'de de iki dönemde alt ucu > 0 ise "
                        "'iki pazarda'); yalnız bir dönemde -> 'TEK DÖNEM'; aksi -> 'GÖSTERİLEMEDİ' (iki dönemde de üst ucu < 0 ise 'GÖSTERİLEMEDİ (ters yönde)'); "
                        "AVR ve BIST kendi satırında aynı kuralla (bilgi); KAPISIZ sayısıyla aynı tablo (kontrol)"},
    "kesik": "veri en büyük tarihi <= 2022-12-31 (hv_kesik_kapi her blok) + KASA.kasa_kapisi (EK 24 ile aynı dosyalar); rastgele gün ve takvim günü 15. barı "
             "<= 2022-12-31",
}

HV25_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "üç taban önceden sabit: T1 aynı hisse rastgele gün (aynı dönem, aynı m, aynı stop / giriş / ufuk geometrisi), T2 aynı pazar / dönem / zaman "
                   "dilimi rastgele (hisse, gün), PİYASA(t) aynı giriş günü bütün pazar (olaylı hisseler hariç); EK 24 eşli farkı (aynı gün aynı kova) yanında yazılır; "
                   "KAPISIZ aynı aday kuralının kontrolü; DÜŞÜŞ günü satırı mekanik üstünlük (düşüş sonrası toparlanma) kontrolü"),
    "K2": ("EVET", "olay girişi bölge sonundan sonraki bar açılışı (EK 24); rastgele günde stop t'ye kadarki m bar; takvimde SAYI(g) yalnız bölge sonu <= g (test); "
                   "PİYASA15 g + 1 açılışından; DUS20 g'ye kadar; veri <= 2022-12-31 assert + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0) aynen; haftalık tamamlanmış ISO haftaları (MV.mv_haftalik_panel); rastgele gün girişinde açılış sonlu > 0"),
    "K4": ("EVET", "olaylar EK 24'te tekil (15 bar); rastgele günler bilinen bölgelerin girişine <= 14 bar yakınsa dışlanır; T1 çekimi yerine koymadan; ortalama "
                   "yanında medyan; çıkarım ay kümeli (günler / olaylar bağımsız sayılmaz)"),
    "K5": ("EVET", "giriş = sonraki ilk bar açılışı (olay, rastgele gün, takvim g + 1); giriş <= stop ölçülmez (olay ve rastgele gün aynı)"),
    "K6": ("EVET", "MI bölünme düzeltmeli fiyatlar (EK 24 aynen); getiriler oransal, yerel para; pazar içi karşılaştırma"),
    "K7": ("EVET", "evren bugün yaşayan hisseler: olay da taban da yukarı yanlı; rastgele gün tabanı aynı evrenden olduğu için yanlılık farkta kısmen düşer, kalkmaz; "
                   "raporda yazılır; kasa açılmaz"),
    "K8": ("EVET", "n >= 30 VE farklı ay >= 12 şartı (okuma); en kalabalık 3 ay payı her tabloda; iki dönem ve iki pazar ayrı; göz sınıfları n < 30 -> "
                   "ÖRNEKLEM YETERSİZ; küçük hücreden 'bulgu' denmez"),
    "K9": ("EVET", "MUM_IZI25_ON_KAYIT.md: KOD25_SHA, ESIK25_SHA, girdi sha'ları, SAYIM25_SHA + getirisiz sayım + yorum noktaları; hesap ön kayıt commit + push'tan "
                   "sonra; hv25_kapi: ik_kontrol_kapisi + sha + commit + temiz ağaç + sayım eşitliği"),
    "K10": ("EVET", "girdi şeması (sütunlar) denetlenir; EK 24 satırında t = takvimde bölge sonu (DUR); göz satırlarında bölge sonu takvimde (DUR); getirisiz "
                    "aşamada giriş / 15. mum tarihi, E0 ve stop olay satırlarıyla birebir (DUR); hesapta R15 / d5 / d10 birebir (DUR)"),
    "K11": ("EVET", "hv25_olc_dizi = gz_olc_bir (sentetik test + bütün olay satırları); TOPLAM_T2 = ZAMANLAMA + SECIM (DUR); rapordan önce >= 2 hücre olay csv'sinden "
                    "bağımsız kısa kodla yeniden üretilir"),
    "K12": ("EVET", "başlık 'KODUN SEÇTİĞİ BÖLGELER'; 'kalıbın sonucu' denmez; 'mutlak kârlı / zamanlama var' yalnız okuma kuralıyla; sayı ile yorum ayrı cümlede; "
                    "dönem içi piyasa yönü tabanda da var"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_hv) korunur; EK 24 fonksiyonları ve çıktıları değişmez (test); MUM_IZI_HAKEM / GOZ / GOZ2 ve defter dosyaları "
                    "değişmez; yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez, kasa açılmaz"),
}


def _hv25_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or HV_YOL["cikti"], HV25_DOSYA[ad])


def hv25_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or HV25_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _hv25_rng(tur: int, anahtar: str) -> np.random.Generator:
    import zlib
    return np.random.default_rng([int(HV25_ESIK["tohum"]), int(tur), zlib.crc32(str(anahtar).encode("utf-8"))])


def hv25_donem(giris: Any) -> Optional[str]:
    """Giriş tarihine göre dönem adı (o16 / d1619 / d2022) ya da None."""
    h = hv_hucre_ad(giris, "X").split("|")[1]
    return None if h == "dis" else h


# ---------------------------------------------------------------- ölçü dizileri (rastgele gün ve olay için tek tanım)
def hv25_dizi(Dg: pd.DataFrame, W: Optional[pd.DataFrame]) -> Dict[str, Any]:
    """Bir hissenin ölçü dizileri. Bar takvimi B = W (haftalık) ya da Dg (günlük). gi[k] / ei[k] = k barının ilk / son günlük indeksi."""
    DO = Dg.Open.to_numpy(float); DH = Dg.High.to_numpy(float); DL = Dg.Low.to_numpy(float); DC = Dg.Close.to_numpy(float)
    if W is None:
        n = len(Dg); gi = np.arange(n); ei = np.arange(n); tar = Dg.index; ent = Dg.index; BL = DL
    else:
        gi = Dg.index.get_indexer(pd.DatetimeIndex(W.bas)); ei = Dg.index.get_indexer(W.index)
        if (gi < 0).any() or (ei < 0).any():
            raise HVHata("K10: haftalık bar günleri günlük takvimde yok")
        tar = W.index; ent = pd.DatetimeIndex(W.bas); BL = W.Low.to_numpy(float)
    return {"DO": DO, "DH": DH, "DL": DL, "DC": DC, "gi": gi, "ei": ei, "tarih": pd.DatetimeIndex(tar), "giris_tarih": pd.DatetimeIndex(ent), "BL": BL,
            "n": len(BL), "_rmin": {}}


def _hv25_rmin(A: Dict[str, Any], m: int) -> np.ndarray:
    """rmin[i] = BL[i .. i + m - 1] dibi (i = t - m + 1)."""
    if m not in A["_rmin"]:
        BL = A["BL"]
        A["_rmin"][m] = (np.lib.stride_tricks.sliding_window_view(BL, m).min(axis=1) if len(BL) >= m else np.array([]))
    return A["_rmin"][m]


def hv25_uygun(A: Dict[str, Any], m: int, haric_k: Any, bas: Any, son: Any, kesik: pd.Timestamp = HV_KESIK) -> np.ndarray:
    """Rastgele karar barı t'lerin uygun olanları (getirisiz; HV25_ESIK['uygun'])."""
    U = int(HV25_ESIK["olcu"]["ufuk"]); yk = int(HV25_ESIK["uygun"]["yakin_bar"]); sc = float(HV25_ESIK["olcu"]["stop_carpan"]); n = int(A["n"]); m = int(m)
    if n < m + U + 1:
        return np.array([], np.int64)
    t = np.arange(m - 1, n - U)
    ok = A["tarih"][t + U] <= pd.Timestamp(kesik)
    gt = A["giris_tarih"][t + 1]; ok &= (gt >= pd.Timestamp(bas)) & (gt <= pd.Timestamp(son))
    E0 = A["DO"][A["gi"][t + 1]]; st = _hv25_rmin(A, m)[t - m + 1] * sc
    with np.errstate(invalid="ignore"):
        ok &= np.isfinite(E0) & (E0 > 0) & np.isfinite(st) & (E0 > st)
    for k in np.asarray(list(haric_k), np.int64):
        ok &= np.abs(t + 1 - int(k)) >= yk
    return t[ok]


def hv25_olc_dizi(A: Dict[str, Any], t: Any, m: int) -> Dict[str, np.ndarray]:
    """gz_olc_bir tanımı vektörle (karar barları t, aynı m): E0, stop, R15, d5, d10, stop15, giris / son15 indeksleri. Uygunluk çağıranda (hv25_uygun)."""
    U = int(HV25_ESIK["olcu"]["ufuk"]); sc = float(HV25_ESIK["olcu"]["stop_carpan"]); t = np.asarray(t, np.int64)
    out = {k: np.full(len(t), np.nan) for k in ("E0", "stop", "R15", "d5", "d10", "stop15")}
    out["g0"] = np.full(len(t), -1, np.int64); out["e15"] = np.full(len(t), -1, np.int64)
    if not len(t):
        return out
    g0 = A["gi"][t + 1]; e15 = A["ei"][t + U]; E0 = A["DO"][g0]; st = _hv25_rmin(A, int(m))[t - int(m) + 1] * sc
    R = A["DC"][e15] / E0 - 1
    L = int((e15 - g0).max()) + 1; ix = g0[:, None] + np.arange(L)[None, :]; val = ix <= e15[:, None]; ix = np.minimum(ix, len(A["DH"]) - 1)
    Hs = np.where(val, A["DH"][ix], -np.inf); Ls = np.where(val, A["DL"][ix], np.inf)
    stp = Ls <= st[:, None]; ks = np.where(stp.any(1), stp.argmax(1), 10 ** 9)
    for x, ad in ((0.05, "d5"), (0.10, "d10")):
        hit = Hs >= (E0 * (1 + x))[:, None]; hk = np.where(hit.any(1), hit.argmax(1), 10 ** 9)
        out[ad] = (hit.any(1) & (hk < ks)).astype(float)
    out.update({"E0": E0, "stop": st, "R15": R, "stop15": stp.any(1).astype(float), "g0": g0, "e15": e15})
    return out


# ---------------------------------------------------------------- girdiler
_HV25_K24 = ["zaman", "pazar", "sembol", "grup", "ana", "haric", "m", "t", "tarih", "bolge_bas", "bolge_son", "hucre", "olculdu", "giris", "E0", "stop", "son15",
             "R15", "d5", "d10", "fark", "esli"]
_HV25_K23 = ["set", "sayfa", "sinif", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m", "olculdu", "giris", "E0", "stop", "son15", "R15", "d10", "d5_tum", "fark"]


def hv25_girdi() -> pd.DataFrame:
    """EK 24 olay satırları + göz 205 bölge -> tek tablo (kaynak 'EK24' / 'GOZ23'). Şema denetlenir; getiri hesaplanmaz."""
    A = pd.read_csv(HV25_YOL["olay24"]); G = pd.read_csv(HV25_YOL["olay23"])
    for ad, D, K in (("mum_izi24_olay", A, _HV25_K24), ("mum_izi23_olay", G, _HV25_K23)):
        yok = [c for c in K if c not in D]
        if yok:
            raise HVHata(f"K10: {ad} sütun yok: {yok}")
    if len(A) != 6011 or len(G) != 205:
        raise HVHata(f"K10: girdi satır sayısı ({len(A)} / {len(G)}; beklenen 6011 / 205)")
    A = A.copy(); A["kaynak"] = "EK24"; A["set"] = ""; A["sinif"] = ""; A["haric"] = A.haric.fillna("")
    G = G.copy(); G["kaynak"] = "GOZ23"; G["grup"] = "GOZ"; G["ana"] = False; G["haric"] = ""; G["tarih"] = G.bolge_son; G["t"] = -1
    G["hucre"] = [hv_hucre_ad(g, p) if isinstance(g, str) else f"{p}|yok" for g, p in zip(G.giris, G.pazar)]
    G["d5"] = G.d5_tum; G["esli"] = np.isfinite(G.fark.astype(float))
    G["sinif"] = G.sinif.map(HV25_GOZ_SINIF).fillna("")
    kol = _HV25_K24 + ["kaynak", "set", "sinif"]
    X = pd.concat([A[kol], G[kol]], ignore_index=True)
    X["ana"] = X.ana.astype(bool); X["olculdu"] = X.olculdu.astype(bool)
    return X


def _hv25_ay(s: Any) -> np.ndarray:
    return pd.to_datetime(pd.Series(s)).dt.strftime("%Y-%m").to_numpy()


def hv25_ay_ozet(giris: Any) -> Dict[str, Any]:
    """Olay sayısı, farklı ay, en kalabalık 3 ayın payı (giriş ayı)."""
    a = _hv25_ay(giris) if len(giris) else np.array([], str)
    if not len(a):
        return {"n": 0, "ay": 0, "ust3_pay": None, "ust3": []}
    v = pd.Series(a).value_counts()
    return {"n": int(len(a)), "ay": int(len(v)), "ust3_pay": float(v.iloc[:3].sum() / len(a)), "ust3": [[k, int(c)] for k, c in v.iloc[:3].items()]}


# ---------------------------------------------------------------- blok hazırlığı (getirisiz)
def hv25_blok_hazir(X: pd.DataFrame, z: str, p: str, Vd: Dict[str, pd.DataFrame], W: Optional[Dict[str, pd.DataFrame]]) -> Tuple[pd.DataFrame, Dict[str, Dict[str, Any]], Dict[str, set]]:
    """Blok (zaman, pazar): olay t'leri (EK 24 t denetimi; göz için bölge sonundan), bilinen bölge giriş barları (dışlama), ölçü dizileri; getirisiz denetim
    (giriş / 15. mum tarihi, E0, stop olay satırlarıyla birebir)."""
    B = X[(X.zaman == z) & (X.pazar == p)].copy(); D: Dict[str, Dict[str, Any]] = {}; tt = []
    for r in B.itertuples():
        s = r.sembol
        if s not in D:
            Dg = Vd.get(s); Wr = (W.get(s) if W is not None else None)
            if Dg is None or (W is not None and Wr is None):
                raise HVHata(f"K10: {z} {p} {s}: veri yok")
            D[s] = hv25_dizi(Dg, Wr)
        try:
            k = int(D[s]["tarih"].get_loc(pd.Timestamp(r.tarih)))
        except KeyError as ex:
            raise HVHata(f"K10: {z} {p} {s} {r.tarih}: bölge sonu takvimde yok") from ex
        if r.kaynak == "EK24" and k != int(r.t):
            raise HVHata(f"K10: {z} {p} {s} {r.tarih}: t {r.t} != takvim {k}")
        tt.append(k)
    B["tk"] = tt
    haric: Dict[str, set] = {}
    for s, k in zip(B.sembol, B.tk):
        haric.setdefault(s, set()).add(int(k) + 1)
    for i, r in zip(B.index, B.itertuples()):              # getirisiz denetim: takvim + E0 + stop
        if not r.olculdu:
            continue
        o = hv25_olc_dizi(D[r.sembol], [r.tk], int(r.m)); A = D[r.sembol]
        if A["giris_tarih"][r.tk + 1] != pd.Timestamp(r.giris) or A["tarih"][r.tk + 15] != pd.Timestamp(r.son15):
            raise HVHata(f"K10: {z} {p} {r.sembol} {r.tarih}: giriş / 15. mum tarihi uyuşmuyor")
        if abs(o["E0"][0] - float(r.E0)) > 6e-7 + 1e-9 * abs(float(r.E0)) or abs(o["stop"][0] - float(r.stop)) > 6e-7 + 1e-9 * abs(float(r.stop)):   # csv %.6f
            raise HVHata(f"K10: {z} {p} {r.sembol} {r.tarih}: E0 / stop uyuşmuyor")
    return B, D, haric


def hv25_piyasa_matris(Vd: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Pazar takvimi (bütün işlem günlerinin birleşimi) x hisse: Op, Cl matrisleri."""
    S = sorted(Vd); cal = pd.DatetimeIndex(np.unique(np.concatenate([Vd[s].index.values.astype("datetime64[ns]") for s in S])))
    Op = np.full((len(cal), len(S)), np.nan); Cl = np.full((len(cal), len(S)), np.nan)
    for j, s in enumerate(S):
        pos = cal.get_indexer(Vd[s].index); Op[pos, j] = Vd[s].Open.to_numpy(float); Cl[pos, j] = Vd[s].Close.to_numpy(float)
    return {"cal": cal, "S": S, "kol": {s: j for j, s in enumerate(S)}, "Op": Op, "Cl": Cl}


def hv25_piyasa_R(M: Dict[str, Any], d: int, e: int, haric_j: Any) -> Tuple[float, int]:
    """d günü açılışında işlem gören hisselerin [d, e] son geçerli kapanış / açılış - 1 ortalaması (haric_j sütunları hariç)."""
    E = M["Op"][d].copy(); hj = np.asarray(list(haric_j), np.int64)
    if len(hj):
        E[hj] = np.nan
    j = np.flatnonzero(np.isfinite(E) & (E > 0))
    if not len(j):
        return float("nan"), 0
    c = M["Cl"][d:e + 1, j]; okc = np.isfinite(c)
    sonk = np.where(okc.any(0), c.shape[0] - 1 - np.argmax(okc[::-1], axis=0), -1)
    R = np.where(sonk >= 0, c[np.maximum(sonk, 0), np.arange(len(j))] / E[j] - 1, np.nan); R = R[np.isfinite(R)]
    if len(R) < int(HV25_ESIK["piyasa"]["en_az_hisse"]):
        return float("nan"), int(len(R))
    return float(R.mean()), int(len(R))


def hv25_gun_haric(X: pd.DataFrame, p: str, M: Dict[str, Any]) -> Dict[int, set]:
    """PİYASA(t) dışlaması: pazarda aynı gün girişli bilinen bölgeler (iki zaman dilimi, EK 24 havuzu + göz 205). Giriş yoksa bölge sonundan sonraki takvim günü."""
    out: Dict[int, set] = {}; cal = M["cal"]
    for s, g, tr in zip(X.sembol[X.pazar == p], X.giris[X.pazar == p], X.tarih[X.pazar == p]):
        j = M["kol"].get(s)
        if j is None:
            continue
        if isinstance(g, str):
            d = cal.searchsorted(pd.Timestamp(g))
        else:
            d = cal.searchsorted(pd.Timestamp(tr), side="right")
        if d < len(cal):
            out.setdefault(int(d), set()).add(j)
    return out


# ---------------------------------------------------------------- takvim serisi (2b; getirisiz kısım ayrı)
def hv25_sayi(cal: pd.DatetimeIndex, bolge_son: Any, pencere: int = 5) -> np.ndarray:
    """SAYI(g) = bölge sonu takvimde [g - pencere + 1, g] olan olay sayısı (bölge sonu <= g; geleceğe bakma yok)."""
    p = cal.searchsorted(pd.DatetimeIndex(pd.to_datetime(pd.Series(bolge_son))), side="left")
    bs = pd.DatetimeIndex(pd.to_datetime(pd.Series(bolge_son)))
    if len(p) and ((p >= len(cal)) | (cal[np.minimum(p, len(cal) - 1)] != bs)).any():
        raise HVHata("K10: bölge sonu pazar takviminde yok")
    c = np.bincount(p, minlength=len(cal)).astype(np.int64); cs = np.r_[0, np.cumsum(c)]
    g = np.arange(len(cal)); return cs[g + 1] - cs[np.maximum(g + 1 - int(pencere), 0)]


def hv25_takvim_gunler(cal: pd.DatetimeIndex, kesik: pd.Timestamp = HV_KESIK) -> np.ndarray:
    """2b günleri g: g >= 20, g + 1 tarihi 2016-01-01 .. 2022-12-31, g + 15 tarihi <= kesik."""
    U = int(HV25_ESIK["olcu"]["ufuk"]); n = len(cal); g = np.arange(20, n - U)
    ok = (cal[g + 1] >= pd.Timestamp("2016-01-01")) & (cal[g + 1] <= pd.Timestamp("2022-12-31")) & (cal[g + U] <= pd.Timestamp(kesik))
    return g[ok]


def hv25_durum(sayi: np.ndarray) -> np.ndarray:
    return np.where(sayi <= 0, "SAYI = 0", np.where(sayi <= 2, "SAYI = 1-2", "SAYI >= 3"))


def hv25_dus20(M: Dict[str, Any]) -> np.ndarray:
    C = pd.DataFrame(M["Cl"]).ffill(limit=5).to_numpy(float); out = np.full(len(C), np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        r = C[20:] / C[:-20] - 1
    ok = np.isfinite(r); s = np.where(ok, r, 0).sum(1); k = ok.sum(1)
    out[20:] = np.where(k > 0, s / np.maximum(k, 1), np.nan)
    return out


# ---------------------------------------------------------------- bootstrap
def hv25_boot(x: Any, ay: Any, anahtar: str, t2c: Optional[Any] = None, t2: Optional[Dict[str, Dict[str, Any]]] = None,
              B: Optional[int] = None) -> Dict[str, Any]:
    """Ay kümeli bootstrap ortalama (x - T2(hücre) seçeneğiyle; T2 tekrarları t2[c]['rep'])."""
    x = np.asarray(x, float); ay = np.asarray(ay, str); B = int(B or HV25_ESIK["boot"]["B"])
    if not len(x):
        return {"ort": None, "alt": None, "ust": None, "medyan": None}
    u, k = np.unique(ay, return_inverse=True); K = len(u)
    s = np.bincount(k, weights=x, minlength=K); n = np.bincount(k, minlength=K).astype(float)
    rng = _hv25_rng(3, anahtar); Wm = rng.multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    num = Wm @ s; den = Wm @ n; nok = x.copy()
    if t2c is not None:
        t2c = np.asarray(t2c, str)
        for c in np.unique(t2c):
            msk = t2c == c; cnt = np.bincount(k[msk], minlength=K).astype(float)
            num = num - (Wm @ cnt) * np.asarray(t2[c]["rep"], float); nok[msk] = x[msk] - float(t2[c]["ort"])
    with np.errstate(invalid="ignore", divide="ignore"):
        d = num / den
    d = d[np.isfinite(d)]
    return {"ort": float(nok.mean()), "medyan": float(np.median(nok)), "alt": float(np.quantile(d, 0.025)), "ust": float(np.quantile(d, 0.975))}


def hv25_boot_fark(xa: Any, aya: Any, xb: Any, ayb: Any, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    """İki grup ortalama farkı, ortak ay kümeleriyle (aylar yerine koyarak; her tekrarda ort(a) - ort(b))."""
    xa = np.asarray(xa, float); xb = np.asarray(xb, float); B = int(B or HV25_ESIK["boot"]["B"])
    if len(xa) < 2 or len(xb) < 2:
        return {"fark": None, "alt": None, "ust": None}
    u = np.unique(np.r_[np.asarray(aya, str), np.asarray(ayb, str)]); ix = {a: i for i, a in enumerate(u)}; K = len(u)
    ka = np.array([ix[a] for a in np.asarray(aya, str)]); kb = np.array([ix[a] for a in np.asarray(ayb, str)])
    sa = np.bincount(ka, weights=xa, minlength=K); na = np.bincount(ka, minlength=K).astype(float)
    sb = np.bincount(kb, weights=xb, minlength=K); nb = np.bincount(kb, minlength=K).astype(float)
    rng = _hv25_rng(5, anahtar); Wm = rng.multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (Wm @ sa) / (Wm @ na) - (Wm @ sb) / (Wm @ nb)
    d = d[np.isfinite(d)]
    return {"fark": float(xa.mean() - xb.mean()), "alt": float(np.quantile(d, 0.025)) if len(d) else None, "ust": float(np.quantile(d, 0.975)) if len(d) else None}


def hv25_t2_rep(R: Any, ay: Any, anahtar: str, B: Optional[int] = None) -> np.ndarray:
    R = np.asarray(R, float); ay = np.asarray(ay, str); B = int(B or HV25_ESIK["boot"]["B"])
    u, k = np.unique(ay, return_inverse=True); K = len(u)
    s = np.bincount(k, weights=R, minlength=K); n = np.bincount(k, minlength=K).astype(float)
    Wm = _hv25_rng(4, anahtar).multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    return (Wm @ s) / (Wm @ n)


# ---------------------------------------------------------------- okuma
def hv25_okuma(n: int, ay: int, ort: Any, alt: Any, ust: Any, tur: str = "MUTLAK", sart: bool = True) -> str:
    O = HV25_ESIK["okuma"]
    if sart and (n < int(O["n_min"]) or ay < int(O["ay_min"])):
        return "ÖLÇÜLEMEDİ"
    if alt is None or ust is None or ort is None:
        return "ÖLÇÜLEMEDİ"
    poz = {"MUTLAK": "MUTLAK KÂRLI", "ZAMANLAMA": "ZAMANLAMA VAR", "SECIM": "SEÇİM +"}[tur]
    neg = {"MUTLAK": "RASTGELE GÜNDEN KÖTÜ", "ZAMANLAMA": "ZAMANLAMA TERS", "SECIM": "SEÇİM -"}[tur]
    if ort > 0 and alt > 0:
        return poz
    if ust < 0:
        return neg
    return "AYRIŞMIYOR"


def hv25_takvim_okuma(F: Dict[str, Dict[str, Any]]) -> str:
    """F[dönem] = (SAYI >= 1) - (SAYI = 0) farkı {fark, alt, ust} (d1619, d2022)."""
    ok = [bool(F.get(d) and F[d].get("alt") is not None and F[d].get("fark") is not None and F[d]["fark"] > 0 and F[d]["alt"] > 0) for d in ("d1619", "d2022")]
    if all(ok):
        return "PİYASA YÜKSELİŞİNİ ÖNCELİYOR"
    if any(ok):
        return "TEK DÖNEM"
    ters = all(bool(F.get(d) and F[d].get("ust") is not None and F[d]["ust"] < 0) for d in ("d1619", "d2022"))
    return "GÖSTERİLEMEDİ (ters yönde)" if ters else "GÖSTERİLEMEDİ"


# ---------------------------------------------------------------- ana akış
def hv25_isle(hesap: bool) -> Tuple[pd.DataFrame, Dict[str, Any], Dict[str, Any]]:
    """Getirisiz (hesap False): uygunluk sayıları, T2 havuz sayıları, takvim durum sayıları. Hesap (True): ek olarak R15 / T1 / T2 / PİYASA(t) / PİYASA15."""
    X = hv25_girdi(); X["tk"] = -1; X["T1_uygun"] = 0
    for c in ("T1_n", "T1_R15", "T1_med", "T1_d5", "T1_d10", "PIY_R15", "PIY_n", "R15_y", "d5_y", "d10_y"):
        X[c] = np.nan
    S: Dict[str, Any] = {"T2": {}, "takvim": {}, "blok": {}}; T2D: Dict[str, Any] = {}; TK: Dict[str, Any] = {}
    Dn = HV_ESIK["hucre"]["donem"]; T1 = HV25_ESIK["T1"]
    for z in HV_ZAMAN:
        for p in HV_PAZAR:
            if not ((X.zaman == z) & (X.pazar == p)).any():
                continue
            Vd, W, _ = hv_blok(z, p); hv_kesik_kapi(Vd, f"{z} {p} (EK 25)")
            B, D, haric = hv25_blok_hazir(X, z, p, Vd, W); X.loc[B.index, "tk"] = B.tk
            # T1
            cache: Dict[Tuple[str, int, str], np.ndarray] = {}
            for i, r in zip(B.index, B.itertuples()):
                if not r.olculdu or r.grup == "ORAN_YOK":
                    continue
                if hesap:
                    o = hv25_olc_dizi(D[r.sembol], [r.tk], int(r.m))
                    X.loc[i, "R15_y"] = o["R15"][0]; X.loc[i, "d5_y"] = o["d5"][0]; X.loc[i, "d10_y"] = o["d10"][0]
                dn = hv25_donem(r.giris)
                if dn is None:
                    continue
                kk = (r.sembol, int(r.m), dn)
                if kk not in cache:
                    cache[kk] = hv25_uygun(D[r.sembol], int(r.m), haric.get(r.sembol, set()), Dn[dn][0], Dn[dn][1])
                el = cache[kk]; X.loc[i, "T1_uygun"] = len(el)
                if not hesap:
                    continue
                if len(el) < int(T1["en_az"]):
                    continue
                rng = _hv25_rng(1, f"{z}|{p}|{r.sembol}|{r.tarih}|{r.kaynak}")
                ch = rng.choice(el, size=min(int(T1["cekim"]), len(el)), replace=False); q = hv25_olc_dizi(D[r.sembol], ch, int(r.m))
                X.loc[i, "T1_n"] = len(ch); X.loc[i, "T1_R15"] = float(q["R15"].mean()); X.loc[i, "T1_med"] = float(np.median(q["R15"]))
                X.loc[i, "T1_d5"] = float(q["d5"].mean()); X.loc[i, "T1_d10"] = float(q["d10"].mean())
            # T2 (bütün evren; m 20)
            Ev = W if W is not None else {s: d for s, d in Vd.items() if len(d) >= 40}
            hucre_dn = sorted({hv25_donem(g) for g in B.giris[B.olculdu & B.giris.notna()]} - {None})
            for dn in hucre_dn:
                ad = f"{z}|{p}|{dn}"; havuz = []
                for s in sorted(Ev):
                    if s not in D:
                        D[s] = hv25_dizi(Vd[s], W[s] if W is not None else None)
                    el = hv25_uygun(D[s], int(HV25_ESIK["T2"]["m"]), haric.get(s, set()), Dn[dn][0], Dn[dn][1])
                    if len(el):
                        havuz.append((s, el))
                N = int(sum(len(e) for _, e in havuz)); S["T2"][ad] = {"uygun_cift": N, "hisse": len(havuz)}
                if not hesap or not N:
                    continue
                rng = _hv25_rng(2, ad); sec = np.sort(rng.choice(N, size=min(int(HV25_ESIK["T2"]["cekim"]), N), replace=False))
                sinir = np.cumsum([0] + [len(e) for _, e in havuz]); R = []; d5 = []; d10 = []; ay = []; sm = []; gtar = []
                hi = np.searchsorted(sinir, sec, side="right") - 1
                for h in np.unique(hi):
                    s, el = havuz[h]; tt_ = el[sec[hi == h] - sinir[h]]; q = hv25_olc_dizi(D[s], tt_, int(HV25_ESIK["T2"]["m"]))
                    R += q["R15"].tolist(); d5 += q["d5"].tolist(); d10 += q["d10"].tolist(); gt = D[s]["giris_tarih"][tt_ + 1]
                    ay += list(gt.strftime("%Y-%m")); sm += [s] * len(tt_); gtar += list(gt.strftime("%Y-%m-%d"))
                R = np.asarray(R); rep = hv25_t2_rep(R, ay, ad)
                T2D[ad] = {"ort": float(R.mean()), "medyan": float(np.median(R)), "d5": float(np.mean(d5)), "d10": float(np.mean(d10)), "n": int(len(R)),
                           "ay": int(len(set(ay))), "rep": rep, "_cekim": pd.DataFrame({"sembol": sm, "giris": gtar, "R15": R, "d5": d5, "d10": d10})}
            # PİYASA(t) ve takvim
            M = hv25_piyasa_matris(Vd); gh = hv25_gun_haric(X, p, M); S["blok"][f"{z}|{p}"] = {"hisse": len(M["S"]), "takvim_gun": int(len(M["cal"]))}
            if hesap:
                for i, r in zip(B.index, B.itertuples()):
                    if not r.olculdu:
                        continue
                    d = M["cal"].get_loc(pd.Timestamp(r.giris)); e = M["cal"].get_loc(pd.Timestamp(r.son15))
                    hj = set(gh.get(int(d), set())) | ({M["kol"][r.sembol]} if r.sembol in M["kol"] else set())
                    v, k = hv25_piyasa_R(M, int(d), int(e), hj); X.loc[i, "PIY_R15"] = v; X.loc[i, "PIY_n"] = k
            if z == "gunluk":
                TK[p] = hv25_takvim_blok(X, p, M, hesap); S["takvim"][p] = TK[p]["sayim"]
            del Vd, W, D, M; gc.collect(); hvlog.info("EK 25 blok: %s %s", z, p)
    return X, {"T2": T2D, "takvim": TK}, S


def hv25_takvim_blok(X: pd.DataFrame, p: str, M: Dict[str, Any], hesap: bool) -> Dict[str, Any]:
    cal = M["cal"]; g = hv25_takvim_gunler(cal); E = X[(X.kaynak == "EK24") & (X.zaman == "gunluk") & (X.pazar == p)]
    sec = {"KAPILI": E[(E.grup == "KAPILI") & E.ana], "KAPILI_DUY": E[E.grup == "KAPILI"], "KAPISIZ": E[(E.grup == "KAPISIZ") & E.ana]}
    out: Dict[str, Any] = {"g": g, "sayi": {k: hv25_sayi(cal, v.bolge_son)[g] for k, v in sec.items()}, "tarih": cal[g], "donem": [hv25_donem(x) for x in cal[g + 1]],
                           "sayim": {}}
    for k in sec:
        dm = hv25_durum(out["sayi"][k])
        out["sayim"][k] = {dn: {du: int(((dm == du) & (np.asarray(out["donem"]) == dn)).sum()) for du in HV25_ESIK["takvim"]["durum"]} for dn in ("d1619", "d2022")}
        out["sayim"][k]["olay"] = int(len(sec[k]))
    if hesap:
        U = int(HV25_ESIK["olcu"]["ufuk"]); P = np.full(len(g), np.nan); Pn = np.zeros(len(g), int)
        for i, gg in enumerate(g):
            P[i], Pn[i] = hv25_piyasa_R(M, int(gg) + 1, int(gg) + U, [])
        out["PIY15"] = P; out["PIY_n"] = Pn; out["DUS20"] = hv25_dus20(M)[g]
    return out


# ---------------------------------------------------------------- getirisiz sayım
def _hv25_ornek(X: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    E = X[X.kaynak == "EK24"]; G = X[X.kaynak == "GOZ23"]
    return {"KAPILI": E[(E.grup == "KAPILI") & E.ana], "KAPILI_DUY": E[E.grup == "KAPILI"], "KAPISIZ": E[(E.grup == "KAPISIZ") & E.ana],
            "GOZ_6_9": G[G.set.isin(["set6", "set7", "set8", "set9"])], "GOZ_7_9": G[G.set.isin(["set7", "set8", "set9"])]}


def hv25_sayim(X: pd.DataFrame, S: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"ornek": {}, "T1_uygun": {}, "T2": S["T2"], "takvim": S["takvim"], "blok": S["blok"]}
    hucreler = HV25_ESIK["hucre"]["karar"] + HV25_ESIK["hucre"]["bilgi"]
    for ad, O in _hv25_ornek(X).items():
        O = O[O.olculdu]; q: Dict[str, Any] = {}
        zlist = HV_ZAMAN + ("birlikte",) if ad.startswith("GOZ") else HV_ZAMAN
        for z in zlist:
            Z = O if z == "birlikte" else O[O.zaman == z]
            if ad.startswith("GOZ"):
                for sn in ("BENZİYOR", "KISMEN", "BENZEMİYOR"):
                    Q = Z[Z.sinif == sn]; q[f"{z}|{sn}"] = {**hv25_ay_ozet(list(Q.giris)), "T1_uygun_az30": int((Q.T1_uygun < 30).sum())}
                continue
            q[f"{z}|hepsi"] = {**hv25_ay_ozet(list(Z.giris)), "T1_uygun_az30": int((Z.T1_uygun < 30).sum())}
            for hc in hucreler:
                Q = Z[Z.hucre == hc]; q[f"{z}|{hc}"] = {**hv25_ay_ozet(list(Q.giris)), "T1_uygun_az30": int((Q.T1_uygun < 30).sum())}
            u = Z.T1_uygun.to_numpy(float)
            out["T1_uygun"][f"{ad}|{z}"] = ({"n": int(len(u)), "min": float(u.min()), "p10": float(np.quantile(u, 0.1)), "medyan": float(np.median(u)),
                                             "p90": float(np.quantile(u, 0.9)), "max": float(u.max()), "az30": int((u < 30).sum()), "az200": int((u < 200).sum())}
                                            if len(u) else {"n": 0})
        out["ornek"][ad] = q
    return out


def hv25_sayim_kos() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    X, _, S = hv25_isle(False)
    return X, hv25_sayim(X, S)


def hv25_sha_simdi() -> Dict[str, str]:
    return {"KOD25_SHA": MI._mi_sha(HV_YOL["kod"]), "ESIK25_SHA": hv25_esik_sha(), "ESIK24_SHA": hv_esik_sha(), "GZ_KOD_SHA": MI._mi_sha(GZ.GZ_YOL["kod"]),
            "ESIK11_SHA": GZ.gz_esik_sha(), "OLAY24_SHA": MI._mi_sha(HV25_YOL["olay24"]), "SONUC24_SHA": MI._mi_sha(HV25_YOL["sonuc24"]),
            "OLAY23_SHA": MI._mi_sha(HV25_YOL["olay23"]), "IS_TANIMI25_SHA": MI._mi_sha(HV25_YOL["is_tanimi"]), "EK_KURAL23_SHA": MI._mi_sha(HV25_YOL["ek_kural"])}


# ---------------------------------------------------------------- tablolar (hesap)
def hv25_tablo_ornek(O: pd.DataFrame, T2: Dict[str, Any], anahtar: str, sart: bool = True) -> Dict[str, Any]:
    """Bir olay kümesi: TAM küme (R15, T1, PİYASA, T2) üzerinde bütün farklar."""
    O = O[O.olculdu]
    t2k = (O.zaman + "|" + O.pazar + "|" + [str(hv25_donem(g)) for g in O.giris]).to_numpy()
    tam = np.isfinite(O.R15.astype(float)) & np.isfinite(O.T1_R15.astype(float)) & np.isfinite(O.PIY_R15.astype(float)) & np.array([k in T2 for k in t2k], bool)
    Q = O[tam]; k2 = t2k[tam.to_numpy()]; ay = _hv25_ay(Q.giris) if len(Q) else np.array([], str)
    r: Dict[str, Any] = {"n_olculen": int(len(O)), "n_tam": int(len(Q)), "T1_yok": int((~np.isfinite(O.T1_R15.astype(float))).sum()),
                         "PIY_yok": int((~np.isfinite(O.PIY_R15.astype(float))).sum()), **{f"ay_{k}": v for k, v in hv25_ay_ozet(list(Q.giris)).items()}}
    if not len(Q):
        return r
    R = Q.R15.to_numpy(float); T1v = Q.T1_R15.to_numpy(float); P = Q.PIY_R15.to_numpy(float); t2o = np.array([T2[k]["ort"] for k in k2])
    if np.abs((R - t2o) - ((P - t2o) + (R - P))).max() > 1e-12:
        raise HVHata("K11: TOPLAM_T2 = ZAMANLAMA + SECIM değil")
    r.update({"R15_ort": float(R.mean()), "R15_med": float(np.median(R)), "T1_ort": float(T1v.mean()), "PIY_ort": float(P.mean()), "T2_ort": float(t2o.mean()),
              "d5": float(Q.d5.astype(float).mean()), "T1_d5": float(Q.T1_d5.mean()), "T2_d5": float(np.mean([T2[k]["d5"] for k in k2])),
              "d10": float(Q.d10.astype(float).mean()), "T1_d10": float(Q.T1_d10.mean()), "T2_d10": float(np.mean([T2[k]["d10"] for k in k2])),
              "TOPLAM_T1": hv25_boot(R - T1v, ay, anahtar + "|T1"), "TOPLAM_T2": hv25_boot(R, ay, anahtar + "|T2", k2, T2),
              "ZAMANLAMA": hv25_boot(P, ay, anahtar + "|Z", k2, T2), "SECIM": hv25_boot(R - P, ay, anahtar + "|S"),
              "HEDEF5_T1": hv25_boot(Q.d5.to_numpy(float) - Q.T1_d5.to_numpy(float), ay, anahtar + "|H5")})
    e = Q[Q.esli.astype(bool) & np.isfinite(Q.fark.astype(float))]
    r["esli_n"] = int(len(e)); r["esli_fark"] = float(e.fark.astype(float).mean()) if len(e) else None
    n, a = r["ay_n"], r["ay_ay"]
    r["okuma"] = {"MUTLAK": hv25_okuma(n, a, r["TOPLAM_T1"]["ort"], r["TOPLAM_T1"]["alt"], r["TOPLAM_T1"]["ust"], "MUTLAK", sart),
                  "MUTLAK_T2": hv25_okuma(n, a, r["TOPLAM_T2"]["ort"], r["TOPLAM_T2"]["alt"], r["TOPLAM_T2"]["ust"], "MUTLAK", sart),
                  "ZAMANLAMA": hv25_okuma(n, a, r["ZAMANLAMA"]["ort"], r["ZAMANLAMA"]["alt"], r["ZAMANLAMA"]["ust"], "ZAMANLAMA", sart),
                  "SECIM": hv25_okuma(n, a, r["SECIM"]["ort"], r["SECIM"]["alt"], r["SECIM"]["ust"], "SECIM", sart),
                  "az_donem": bool(r["ay_ust3_pay"] is not None and r["ay_ust3_pay"] > float(HV25_ESIK["okuma"]["az_donem_pay"])),
                  "orneklem_yetersiz": bool(n < int(HV25_ESIK["okuma"]["n_min"]))}
    return r


def hv25_esli_boot(f: Any) -> Dict[str, Any]:
    """EK 23 eşli okuma: basit bootstrap (10.000, tohum 2311)."""
    f = np.asarray(f, float); f = f[np.isfinite(f)]
    if len(f) < 2:
        return {"n": int(len(f)), "ort": float(f.mean()) if len(f) else None, "alt": None, "ust": None, "okuma": "GÖSTERİLEMEDİ"}
    rng = np.random.default_rng(int(HV25_ESIK["goz"]["tohum_esli"])); b = f[rng.integers(0, len(f), size=(10000, len(f)))].mean(1)
    lo, hi = float(np.quantile(b, 0.025)), float(np.quantile(b, 0.975))
    ok = "SONRASI İYİ" if (f.mean() > 0 and lo > 0) else ("SONRASI KÖTÜ" if hi < 0 else "GÖSTERİLEMEDİ")
    return {"n": int(len(f)), "ort": float(f.mean()), "alt": lo, "ust": hi, "okuma": ok}


def hv25_takvim_tablo(TK: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for p, K in TK.items():
        P = K["PIY15"]; ok = np.isfinite(P); dn = np.asarray(K["donem"], object); ay = pd.DatetimeIndex(K["tarih"]).strftime("%Y-%m").to_numpy()
        q: Dict[str, Any] = {}
        for sk in ("KAPILI", "KAPILI_DUY", "KAPISIZ"):
            dm = hv25_durum(K["sayi"][sk]); Fd: Dict[str, Any] = {}
            for dd in ("d1619", "d2022", "birlikte"):
                m0 = ok & ((dn == dd) if dd != "birlikte" else np.isin(dn, ["d1619", "d2022"]))
                sat = {}
                for du in HV25_ESIK["takvim"]["durum"]:
                    m = m0 & (dm == du); v = P[m]
                    sat[du] = {"gun": int(m.sum()), "ort": float(v.mean()) if len(v) else None, "medyan": float(np.median(v)) if len(v) else None,
                               "arti_pay": float((v > 0).mean()) if len(v) else None, "ay": int(len(set(ay[m])))}
                a1 = m0 & (dm != "SAYI = 0"); a3 = m0 & (dm == "SAYI >= 3"); a0 = m0 & (dm == "SAYI = 0")
                sat["fark_1"] = hv25_boot_fark(P[a1], ay[a1], P[a0], ay[a0], f"{p}|{sk}|{dd}|1")
                sat["fark_3"] = hv25_boot_fark(P[a3], ay[a3], P[a0], ay[a0], f"{p}|{sk}|{dd}|3")
                sat["fark_1"]["n"] = [int(a1.sum()), int(a0.sum())]; sat["fark_3"]["n"] = [int(a3.sum()), int(a0.sum())]
                Fd[dd] = sat
            Fd["okuma"] = hv25_takvim_okuma({d: Fd[d]["fark_1"] for d in ("d1619", "d2022")})
            q[sk] = Fd
        D = K["DUS20"]; dus = ok & np.isfinite(D) & (D < -0.05); dg: Dict[str, Any] = {}
        for dd in ("d1619", "d2022", "birlikte"):
            m0 = ok & np.isfinite(D) & ((dn == dd) if dd != "birlikte" else np.isin(dn, ["d1619", "d2022"])); a = m0 & dus; b = m0 & ~dus; v = P[a]
            dm = hv25_durum(K["sayi"]["KAPILI"])
            dg[dd] = {"gun": int(a.sum()), "ort": float(v.mean()) if len(v) else None, "medyan": float(np.median(v)) if len(v) else None,
                      "arti_pay": float((v > 0).mean()) if len(v) else None, "oteki_ort": float(P[b].mean()) if b.any() else None,
                      "fark": hv25_boot_fark(P[a], ay[a], P[b], ay[b], f"{p}|dus|{dd}"),
                      "dus_icinde_fark_1": hv25_boot_fark(P[a & (dm != "SAYI = 0")], ay[a & (dm != "SAYI = 0")], P[a & (dm == "SAYI = 0")],
                                                          ay[a & (dm == "SAYI = 0")], f"{p}|dusic|{dd}"),
                      "dus_disinda_fark_1": hv25_boot_fark(P[b & (dm != "SAYI = 0")], ay[b & (dm != "SAYI = 0")], P[b & (dm == "SAYI = 0")],
                                                           ay[b & (dm == "SAYI = 0")], f"{p}|dusdis|{dd}"),
                      "dus_gun_SAYI_1": int((a & (dm != "SAYI = 0")).sum()), "olay_gun_dus_pay": float(dus[ok & (dm != "SAYI = 0")].mean()) if (ok & (dm != "SAYI = 0")).any() else None}
        q["DUSUS"] = dg; q["gun_n"] = int(ok.sum())
        out[p] = q
    ab = out.get("ABD", {}).get("KAPILI", {}); av = out.get("AVR", {}).get("KAPILI", {})
    if ab:
        g = ab["okuma"]
        if g == "PİYASA YÜKSELİŞİNİ ÖNCELİYOR" and av and av.get("okuma") == "PİYASA YÜKSELİŞİNİ ÖNCELİYOR":
            g += " (iki pazarda)"
        out["genel"] = g
    return out


def hv25_tablolar(X: pd.DataFrame, EK: Dict[str, Any]) -> Dict[str, Any]:
    T2 = EK["T2"]; T: Dict[str, Any] = {"ornek": {}, "goz": {}, "T2": {k: {kk: v[kk] for kk in ("ort", "medyan", "d5", "d10", "n", "ay")} for k, v in T2.items()}}
    hucreler = HV25_ESIK["hucre"]["karar"] + HV25_ESIK["hucre"]["bilgi"]; Ob = _hv25_ornek(X)
    for ad in ("KAPILI", "KAPILI_DUY", "KAPISIZ"):
        O = Ob[ad]; q: Dict[str, Any] = {}
        for z in HV_ZAMAN:
            Z = O[O.zaman == z]; q[f"{z}|hepsi"] = hv25_tablo_ornek(Z, T2, f"{ad}|{z}|hepsi")
            for hc in hucreler:
                q[f"{z}|{hc}"] = hv25_tablo_ornek(Z[Z.hucre == hc], T2, f"{ad}|{z}|{hc}")
        q["birlikte|hepsi"] = hv25_tablo_ornek(O, T2, f"{ad}|birlikte|hepsi")
        T["ornek"][ad] = q
    for ad in ("GOZ_6_9", "GOZ_7_9"):
        O = Ob[ad]; q = {}
        for z in ("birlikte",) + HV_ZAMAN:
            Z = O if z == "birlikte" else O[O.zaman == z]
            for sn in ("BENZİYOR", "KISMEN", "BENZEMİYOR"):
                Q = Z[Z.sinif == sn]; r = hv25_tablo_ornek(Q, T2, f"{ad}|{z}|{sn}", sart=False)
                r["esli_okuma"] = hv25_esli_boot(Q[Q.olculdu].fark.astype(float)); q[f"{z}|{sn}"] = r
        T["goz"][ad] = q
    k = T["goz"]["GOZ_6_9"].get("birlikte|KISMEN", {}); k7 = T["goz"]["GOZ_7_9"].get("birlikte|KISMEN", {})
    T["kismen_kabul"] = {"set_6_9": bool(k.get("okuma", {}).get("MUTLAK") == "MUTLAK KÂRLI"), "set_7_9_bilgi": bool(k7.get("okuma", {}).get("MUTLAK") == "MUTLAK KÂRLI"),
                         "n_6_9": k.get("n_tam"), "orneklem_yetersiz_6_9": bool((k.get("n_tam") or 0) < 30)}
    T["takvim"] = hv25_takvim_tablo(EK["takvim"])
    return T


# ---------------------------------------------------------------- kapı, ön kayıt, koşu
def hv25_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or HV_YOL["cikti"]; yol = _hv25_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise HVHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = hv25_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise HVHata(f"ön kayıt kapısı (EK 25): {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_HV); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise HVHata("ön kayıt (EK 25) commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_HAVUZ.py"]):
        raise HVHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def hv25_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or HV_YOL["cikti"]; y = _hv25_yol("onkayit", cikti)
    if os.path.exists(y):
        raise HVHata("ön kayıt (EK 25) zaten var")
    X, S = hv25_sayim_kos(); sh = hv25_sha_simdi(); sh["SAYIM25_SHA"] = hv_json_sha(S)
    os.makedirs(HV25_YOL["gecici"], exist_ok=True); MI._mi_jyaz(os.path.join(HV25_YOL["gecici"], "sayim25.json"), S, "sayım 25")
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in HV25_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_HAVUZ.py"])
    sat = ["| örneklem | zaman | hücre | n (ölçülen) | farklı ay | en kalabalık 3 ay payı (aylar) | T1 uygun < 30 |", "|---|---|---|---|---|---|---|"]
    for o, q in S["ornek"].items():
        for k, v in q.items():
            z, h = k.split("|", 1)
            sat.append(f"| {o} | {z} | {h} | {v['n']} | {v['ay']} | {_hv_f(v['ust3_pay'], 3)} ({', '.join(f'{a} {c}' for a, c in v['ust3'])}) | {v['T1_uygun_az30']} |")
    t1 = ["| örneklem / zaman | n | en az | %10 | medyan | %90 | en çok | < 30 | < 200 |", "|---|---|---|---|---|---|---|---|---|"]
    for k, v in S["T1_uygun"].items():
        if v.get("n"):
            t1.append(f"| {k} | {v['n']} | {v['min']:.0f} | {v['p10']:.0f} | {v['medyan']:.0f} | {v['p90']:.0f} | {v['max']:.0f} | {v['az30']} | {v['az200']} |")
    t2 = ["| T2 hücresi | uygun (hisse, gün) çifti | hisse |", "|---|---|---|"] + [f"| {k} | {v['uygun_cift']} | {v['hisse']} |" for k, v in S["T2"].items()]
    tk = ["| pazar | SAYI kaynağı | olay | dönem | SAYI = 0 gün | SAYI = 1-2 gün | SAYI >= 3 gün |", "|---|---|---|---|---|---|---|"]
    for p, q in S["takvim"].items():
        for sk, v in q.items():
            for dn in ("d1619", "d2022"):
                tk.append(f"| {p} | {sk} | {v['olay']} | {dn} | {v[dn]['SAYI = 0']} | {v[dn]['SAYI = 1-2']} | {v[dn]['SAYI >= 3']} |")
    yorum = [
        "1. '15 bardan yakın' = rastgele giriş barı ile bilinen bir bölgenin giriş barı arasında |fark| <= 14 bar (15 mumluk pencereler örtüşür); bilinen bölgeler = "
        "EK 24 havuzunun BÜTÜN olayları (KAPILI + KAPISIZ + ORAN_YOK, hariç dahil, ölçülemeyenler dahil) + göz ölçümü 205 bölge, aynı hisse ve aynı zaman dilimi.",
        "2. T1 'aynı dönem' = olayın giriş tarihine göre dönemi (2016 öncesi / 2016-19 / 2020-22); rastgele girişin tarihi dönem içinde, 15. mumu dönem dışına "
        "taşabilir (olaylarla aynı kural), ama 2022-12-31'i aşamaz.",
        "3. Rastgele gün 'geçerli' = giriş açılışı sonlu, > 0 ve > stop (olayın ölçülebilirlik kuralı aynen; giriş <= stop olan gün çekilmez). Yerine koymadan "
        "çekim; T1 için olay başına 200 (KAPISIZ dahil; vektörle hesaplandığı için 50'ye inilmedi); uygun < 30 ise olay T1'siz kalır ve sayılır.",
        "4. T2 stop m = 20 (iş tanımı); T2 rastgele çiftleri de aynı dışlama ve ölçülebilirlik kuralıyla; T2 hücresi = zaman dilimi x pazar x dönem; T2 belirsizliği "
        "ay kümeli bootstrap'a katılır (T2 çekimleri kendi giriş aylarıyla, olaylardan bağımsız).",
        "5. PİYASA(t): olayla aynı veri bloğu (günlükte günlük açık veri, haftalıkta haftalık bloğun günlük verisi), olayın giriş günü açılışında işlem gören bütün "
        "hisseler, olayın 15. mum gününe kadar son geçerli kapanış (gz_es_grup R tanımı, kova / stop yok), olayın hissesi ve AYNI GÜN girişli bilinen bölgesi olan "
        "hisseler hariç (iki zaman dilimi birlikte); günlükte 15. mum günü ile haftalıkta 15. haftanın son günü olayınki.",
        "6. Tablolar TAM kümeyle (R15, T1, PİYASA(t), T2 hepsi olan olaylar); TOPLAM_T2 = ZAMANLAMA + SEÇİM özdeşliği olay başına denetlenir. 'Hepsi birlikte' her "
        "olayı kendi hücresinin T2'siyle karşılaştırır.",
        "7. Göz ölçümü sınıfı 'sinif' sütunu (EVET = BENZİYOR, KISMEN, HAYIR = BENZEMİYOR); set 8 s11 duyarlılığı (sinif_duy) kullanılmaz. KISMEN KABUL kararı set 6-9 "
        "(zaman dilimleri birlikte) ile; set 7-9 bilgi. Göz satırlarının d5'i 'd5_tum' (haftalıkta günlük veriyle aynı kural).",
        "8. 2b SAYI ana = KAPILI ANA günlük olaylar (EK 24 ana örnekle tutarlı; ölçülebilirlikten bağımsız sayılır); KAPILI hepsi duyarlılık, KAPISIZ ANA kontrol. "
        "Takvim = pazarın günlük verisindeki işlem günlerinin birleşimi; 'son 5 işlem günü' = takvimde g - 4 .. g; PİYASA15'te olay dışlaması YOK (iş tanımı 'bütün "
        "hisseler'); bootstrap kümesi g'nin ayı; dönem g + 1 tarihine göre.",
        "9. 'Pazar son 20 günde %5'ten fazla düşmüş' = DUS20(g) < -0,05 (eşit ağırlıklı, kapanış en çok 5 gün ileri taşınır); bilgi satırı olarak DÜŞÜŞ günleri "
        "içinde / dışında (SAYI >= 1) - (SAYI = 0) da yazılır (hükme girmez).",
        "10. Okuma etiketleri iş tanımı 3. bölüm ve 2b aynen; 'iki pazarda' için AVR'de de iki dönemde alt ucu > 0 aranır; iki dönemde de üst ucu < 0 ise "
        "'GÖSTERİLEMEDİ (ters yönde)'. Ortalama yanında medyan; okuma ortalama ve ay kümeli aralıkla.",
    ]
    s = [f"# MUM_IZI25 ÖN KAYIT — KODUN SEÇTİĞİ BÖLGELER: rastgele gün tabanı, zamanlama / seçim, piyasa tahmini ({MI._mi_simdi()})", "",
         "İş tanımı MUM_IZI25_IS_TANIMI.md (1, 2, 2b, 3. bölüm) ve MUM_IZI23_EK_KURAL.md GÜNCELLEME. Bu dosya rastgele gün, T2, PİYASA(t) ve PİYASA15 getirileri "
         "hesaplanmadan ÖNCE commit + push edilir; tanımlar, eşikler ve okuma kuralları sonra değişmez (değişirse SAPMA). Olay R15'leri EK 24 / EK 23 çıktılarından "
         "(daha önce yayımlandı); bu dosyadaki sayım getirisizdir. Evren bugün yaşayan hisseler (olay da taban da yukarı yanlı). Dönem içi piyasa yönü tabanda da "
         "var. KASA açılmaz (veri <= 2022-12-31).", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_HAVUZ.py commit'i: {kc or 'yok'}", "",
         "## GETİRİSİZ SAYIM (yalnız olay / gün sayıları, uygun gün sayıları, takvim durumları; getiri hesaplanmadı)", "",
         "### Örneklem x hücre (ölçülen olaylar; giriş ayına göre)", "", *sat, "",
         "### T1: olay başına çekilebilen (uygun) gün sayısı", "", *t1, "", "### T2: uygun (hisse, gün) çiftleri", "", *t2, "",
         "### Takvim (2b, günlük): SAYI durumlarına göre gün sayısı", "", *tk, "",
         f"- Blok: {json.dumps(S['blok'], ensure_ascii=False)}", "",
         "## Yorum gerektiren noktalar (ölçümden ÖNCE sabit)", "", *yorum, "",
         "## Tanımlar (HV25_ESIK; sha yukarıda)", "", "```", json.dumps(HV25_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 25")


HV25_OLAY_KOL = ["kaynak", "zaman", "pazar", "sembol", "grup", "ana", "haric", "set", "sinif", "m", "tk", "tarih", "bolge_son", "hucre", "olculdu", "giris", "son15",
                 "R15", "d5", "d10", "T1_uygun", "T1_n", "T1_R15", "T1_med", "T1_d5", "T1_d10", "PIY_R15", "PIY_n", "T2_hucre", "T2_R15", "T2_d5", "fark", "esli"]


def hv25_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    t0 = time.time(); cikti = cikti or HV_YOL["cikti"]
    if os.path.exists(_hv25_yol("sonuc", cikti)):
        raise HVHata("sonuç (EK 25) zaten var (ikinci koşu DURUR)")
    G0 = hv25_kapi(cikti)
    try:
        kasa = KS.kasa_kapisi([os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in HV_PAZAR] + [os.path.join(MH.MH_YOL["tam"], f"V_{p}.pkl") for p in HV_PAZAR],
                              "2022-12-31")
    except KS.KasaHata as ex:
        raise HVHata(f"KASA kapısı KAPALI: {ex}") from ex
    X, EK, S0 = hv25_isle(True); S = hv25_sayim(X, S0)
    if f"SAYIM25_SHA: {hv_json_sha(S)}" not in open(_hv25_yol("onkayit", cikti), encoding="utf-8").read():
        raise HVHata("getirisiz sayım (EK 25) ön kayıttakiyle aynı değil -> DURDU")
    m = X.olculdu & X.grup.isin(["KAPILI", "KAPISIZ", "GOZ"])
    for a, b, tol in (("R15", "R15_y", 2e-6), ("d10", "d10_y", 0), ("d5", "d5_y", 0)):
        v = X.loc[m, [a, b]].astype(float); v = v[np.isfinite(v[a])]
        kot = ~np.isfinite(v[b]) | (np.abs(v[a] - v[b]) > tol + 1e-6 * np.abs(v[a]))
        if kot.any():
            raise HVHata(f"K11: hv25_olc_dizi {a} olay satırlarıyla uyuşmuyor ({int(kot.sum())} satır)")
    T = hv25_tablolar(X, EK)
    O = X.copy(); O["T2_hucre"] = [f"{z}|{p}|{hv25_donem(g)}" if isinstance(g, str) else "" for z, p, g in zip(O.zaman, O.pazar, O.giris)]
    O["T2_R15"] = [EK["T2"][k]["ort"] if k in EK["T2"] else np.nan for k in O.T2_hucre]; O["T2_d5"] = [EK["T2"][k]["d5"] if k in EK["T2"] else np.nan for k in O.T2_hucre]
    O = O[HV25_OLAY_KOL]
    C2r = [v["_cekim"].assign(kaynak="T2_CEKIM", T2_hucre=k) for k, v in EK["T2"].items()]
    TKr = []
    for p, K in EK["takvim"].items():
        TKr.append(pd.DataFrame({"kaynak": "TAKVIM", "pazar": p, "tarih": pd.DatetimeIndex(K["tarih"]).strftime("%Y-%m-%d"), "hucre": K["donem"],
                                 "SAYI_KAPILI": K["sayi"]["KAPILI"], "SAYI_KAPILI_DUY": K["sayi"]["KAPILI_DUY"], "SAYI_KAPISIZ": K["sayi"]["KAPISIZ"],
                                 "PIY15": K["PIY15"], "PIY_n": K["PIY_n"], "DUS20": K["DUS20"]}))
    Y = pd.concat([O] + C2r + TKr, ignore_index=True)
    Y.to_csv(_hv25_yol("olay", cikti), index=False, float_format="%.6f", compression={"method": "gzip", "mtime": 0})
    J = {"surum": HV25_SURUM, "baslik": "KODUN SEÇTİĞİ BÖLGELER", "kapi": G0, "kasa": kasa, "sayim": S, "tablo": T, "olay_sha": MI._mi_sha(_hv25_yol("olay", cikti)),
         "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_hv25_yol("sonuc", cikti), J, "sonuç 25")
    return J


def _hv25_b(b: Optional[Dict[str, Any]]) -> str:
    if not b or b.get("ort", b.get("fark")) is None:
        return "-"
    v = b.get("ort", b.get("fark"))
    return f"{_hv_f(v, 2, True)} [{_hv_f(b.get('alt'), 2, True)}; {_hv_f(b.get('ust'), 2, True)}]"


def hv25_rapor_tablo(J: Dict[str, Any]) -> str:
    T = J["tablo"]; s: List[str] = []
    bas = ("| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | "
           "ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |")
    for ad in ("KAPILI", "KAPISIZ", "KAPILI_DUY"):
        for z in HV_ZAMAN + ("birlikte",):
            keys = [f"{z}|hepsi"] + ([f"{z}|{hc}" for hc in HV25_ESIK["hucre"]["karar"] + HV25_ESIK["hucre"]["bilgi"]] if z != "birlikte" else [])
            s += [f"### {ad} — {z.upper()} (KODUN SEÇTİĞİ BÖLGELER)", "", bas, "|" + "---|" * 15]
            for k in keys:
                c = T["ornek"][ad].get(k)
                if not c or not c.get("n_tam"):
                    s.append(f"| {k.split('|', 1)[1]} | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |"); continue
                o = c["okuma"]
                s.append(f"| {k.split('|', 1)[1]} | {c['n_tam']} | {c['ay_ay']} | {_hv_f(c['ay_ust3_pay'], 2)} | {_hv_f(c['R15_ort'], 2, True)} / {_hv_f(c['R15_med'], 2, True)} | "
                         f"{_hv_f(c['T1_ort'], 2, True)} | {_hv_f(c['T2_ort'], 2, True)} | {_hv_f(c['PIY_ort'], 2, True)} | {_hv25_b(c['TOPLAM_T1'])} | {_hv25_b(c['TOPLAM_T2'])} | "
                         f"{_hv25_b(c['ZAMANLAMA'])} | {_hv25_b(c['SECIM'])} | {_hv_f(c['esli_fark'], 2, True)} ({c['esli_n']}) | {_hv_f(c['d5'], 1, True)} / "
                         f"{_hv_f(c['T1_d5'], 1, True)} / {_hv_f(c['T2_d5'], 1, True)} | {o['MUTLAK']}; {o['ZAMANLAMA']}; {o['SECIM']}"
                         f"{'; az sayıda döneme dayanıyor' if o['az_donem'] else ''} |")
            s.append("")
    for ad in ("GOZ_6_9", "GOZ_7_9"):
        s += [f"### GÖZ ÖLÇÜMÜ {ad} (sınıf = Cemal'in işareti)", "", "| zaman | sınıf | n | farklı ay | R15 ort / medyan | T1 ort | TOPLAM FARK (T1) [%95] | ZAMANLAMA [%95] | "
              "SEÇİM [%95] | +%5 olay / T1 | okuma (aralık kuralı) | eşli fark (EK 23 kuralı) [%95] |", "|" + "---|" * 12]
        for k, c in T["goz"][ad].items():
            z, sn = k.split("|")
            if not c.get("n_tam"):
                s.append(f"| {z} | {sn} | 0 | - | - | - | - | - | - | - | - | - |"); continue
            e = c["esli_okuma"]
            s.append(f"| {z} | {sn} | {c['n_tam']} | {c['ay_ay']} | {_hv_f(c['R15_ort'], 2, True)} / {_hv_f(c['R15_med'], 2, True)} | {_hv_f(c['T1_ort'], 2, True)} | "
                     f"{_hv25_b(c['TOPLAM_T1'])} | {_hv25_b(c['ZAMANLAMA'])} | {_hv25_b(c['SECIM'])} | {_hv_f(c['d5'], 1, True)} / {_hv_f(c['T1_d5'], 1, True)} | "
                     f"{c['okuma']['MUTLAK']}{' (ÖRNEKLEM YETERSİZ)' if c['okuma']['orneklem_yetersiz'] else ''} | {_hv_f(e['ort'], 2, True)} [{_hv_f(e['alt'], 2, True)}; "
                     f"{_hv_f(e['ust'], 2, True)}] {e['okuma']} (n {e['n']}) |")
        s.append("")
    s += [f"KISMEN KABUL: {json.dumps(T['kismen_kabul'], ensure_ascii=False)}", ""]
    TK = T["takvim"]
    for p in ("ABD", "AVR", "BIST"):
        if p not in TK:
            continue
        for sk in ("KAPILI", "KAPISIZ", "KAPILI_DUY"):
            q = TK[p][sk]
            s += [f"### PİYASA TAHMİNİ {p} — SAYI kaynağı {sk} (okuma: {q['okuma']})", "",
                  "| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |", "|---|---|---|---|---|---|"]
            for dd in ("d1619", "d2022", "birlikte"):
                r = q[dd]; f = lambda du: f"{r[du]['gun']} / {_hv_f(r[du]['ort'], 2, True)} / {_hv_f(r[du]['medyan'], 2, True)} / {_hv_f(r[du]['arti_pay'], 2)}"  # noqa: E731
                s.append(f"| {dd} | {f('SAYI = 0')} | {f('SAYI = 1-2')} | {f('SAYI >= 3')} | {_hv25_b(r['fark_1'])} | {_hv25_b(r['fark_3'])} |")
            s.append("")
        d = TK[p]["DUSUS"]
        s += [f"#### {p} — pazar son 20 günde %5'ten fazla düşmüş günler (DUS20 < -0,05)", "",
              "| dönem | gün | PİYASA15 ort / medyan / artı payı | öteki günler ort | DÜŞÜŞ - öteki [%95] | DÜŞÜŞ içinde (>= 1) - (= 0) [%95] | DÜŞÜŞ dışında (>= 1) - (= 0) [%95] | "
              "SAYI >= 1 günlerinin DÜŞÜŞ payı |", "|---|---|---|---|---|---|---|---|"]
        for dd in ("d1619", "d2022", "birlikte"):
            r = d[dd]
            s.append(f"| {dd} | {r['gun']} | {_hv_f(r['ort'], 2, True)} / {_hv_f(r['medyan'], 2, True)} / {_hv_f(r['arti_pay'], 2)} | {_hv_f(r['oteki_ort'], 2, True)} | "
                     f"{_hv25_b(r['fark'])} | {_hv25_b(r['dus_icinde_fark_1'])} | {_hv25_b(r['dus_disinda_fark_1'])} | {_hv_f(r['olay_gun_dus_pay'], 2)} |")
        s.append("")
    s += [f"PİYASA TAHMİNİ GENEL (ABD KAPILI; AVR ile): {TK.get('genel')}", ""]
    s += ["T2 hücreleri: " + "; ".join(f"{k}: n {v['n']}, ort {_hv_f(v['ort'], 2, True)}, medyan {_hv_f(v['medyan'], 2, True)}, +%5 {_hv_f(v['d5'], 1, True)}"
                                       for k, v in T["T2"].items()), ""]
    return "\n".join(s)


def hv25_rapor_yaz(cikti: Optional[str] = None) -> str:
    J = json.load(open(_hv25_yol("sonuc", cikti), encoding="utf-8"))
    y = os.path.join(HV25_YOL["gecici"], "rapor_tablo25.md"); os.makedirs(HV25_YOL["gecici"], exist_ok=True)
    return MI._mi_yaz(y, hv25_rapor_tablo(J), "rapor tablo 25")


# ================================================================ 8) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_hv(_once=_CK_ONCE_HV, _dosya="MUM_IZI_HAVUZ.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_HV",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_hv()


def _hv_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_HAVUZ")
    ap.add_argument("komut", choices=["sayim", "onkayit", "kos", "rapor", "sha", "sayim25", "onkayit25", "kos25", "rapor25", "sha25"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "sayim":
            _, S = hv_sayim_kos(); os.makedirs(HV_YOL["gecici"], exist_ok=True)
            MI._mi_jyaz(os.path.join(HV_YOL["gecici"], "sayim.json"), S, "sayım 24")
            print(json.dumps(MI._mi_json({"huni": S["huni"], "zaman": S["zaman"], "SAYIM_SHA": hv_json_sha(S)}), ensure_ascii=False, indent=1))
        elif a.komut == "onkayit":
            print(hv_onkayit_yaz())
        elif a.komut == "kos":
            J = hv_kos(); print(json.dumps(MI._mi_json({k: J["tablo"]["genel"][k] for k in J["tablo"]["genel"]}), ensure_ascii=False, indent=1))
        elif a.komut == "rapor":
            print(hv_rapor_yaz())
        elif a.komut == "sha":
            print(json.dumps(hv_sha_simdi(), indent=1))
        elif a.komut == "sayim25":
            _, S = hv25_sayim_kos(); os.makedirs(HV25_YOL["gecici"], exist_ok=True)
            MI._mi_jyaz(os.path.join(HV25_YOL["gecici"], "sayim25.json"), S, "sayım 25")
            print(json.dumps(MI._mi_json({"T1_uygun": S["T1_uygun"], "takvim": S["takvim"], "SAYIM25_SHA": hv_json_sha(S)}), ensure_ascii=False, indent=1))
        elif a.komut == "onkayit25":
            print(hv25_onkayit_yaz())
        elif a.komut == "kos25":
            J = hv25_kos(); print(json.dumps(MI._mi_json({"kismen_kabul": J["tablo"]["kismen_kabul"], "takvim": J["tablo"]["takvim"].get("genel"),
                                                          "sure_sn": J["sure_sn"]}), ensure_ascii=False, indent=1))
        elif a.komut == "rapor25":
            print(hv25_rapor_yaz())
        elif a.komut == "sha25":
            print(json.dumps(hv25_sha_simdi(), indent=1))
    except HVHata as ex:
        hvlog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_hv_ana())
