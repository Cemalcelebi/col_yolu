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
    ap.add_argument("komut", choices=["sayim", "onkayit", "kos", "rapor", "sha"])
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
    except HVHata as ex:
        hvlog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_hv_ana())
