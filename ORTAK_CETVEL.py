"""ORTAK_CETVEL — dört aşamalı yeniden ölçümün (K24 iki evre çöl; D9 uzun çöl + rüzgâr; düzgün dip vs çöl; INTEM ileri test) TEK ve
MÜHÜRLÜ ölçüm cetveli, tek dosya (14 Kasım 2026; ana oturum iş tanımı, AŞAMA 1).

Cemal (14 Kas 2026): "Her aşamada aynı ölçüm kriterleri kullanılacak. Sonucu beğenmediğimiz için eşikle oynanmaz."
Bu şart MEKANİKTİR: bütün eşikler OC_ESIK sözlüğündedir ve sha256 ile mühürlenir (oc_esik_sha). Dört aşamanın her biri bu modülü İÇE ALIR
ve koşmadan önce oc_kapi(onkayit_yolu) çağırır: IZ_KARNE.ik_kontrol_kapisi + ön kayıttaki CETVEL_SHA / CETVEL_KOD_SHA / GUC_SHA satırları
bu dosyanın o anki değerleriyle aynı + ön kayıt git'e işlenmiş ve değişmemiş. Biri tutmazsa koşu durur (OCHata).
Bu cetvel dört aşamada değiştirilmez; değişirse yeni cetvel sürümü ve bütün aşamalar yeniden koşulur.

ÖLÇÜLER (her aşamada aynı; ayrıntı OC_ESIK):
  (1) r60 = giriş (t'den sonraki ilk geçerli bar AÇILIŞI) -> 60. işlem günü kapanışı; EŞLİ FARK (aynı giriş günü, aynı pazar, aynı 60 gün
      momentum beşliği x 20 gün likidite üçlüsü; FON_IZI FI_OLCUT tanımı burada yeniden yazıldı, sentetik testte birebir eşit); ay kümeli
      bootstrap %95; hücre içi sıra.
  (2) 10 yuvalı slot portföyü (60 gün) vs 200 plasebo portföy (her olay yerine aynı gün aynı hücreden rastgele hisse; %90).
  (3) OLASILIK TABLOSU: 250 işlem gününde +%100'e / -%50'ye dokunma; eşlerin katı (karar) ve aynı gün taban oranın katı (bilgi);
      60 günde önce +%20 (-%10'dan önce) eşlerin katı (eski tek cetvelle kıyas; karar dışı).
  (4) 20 gün P(+%20 önce) / P(-%10 önce) bilgi.
HÜCRE = pazar {ABD, AVR, BIST} x dönem {2016-22 keşif, 2023, 2024-26/08}. KARAR hücreleri ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26.
GÜÇ: oc_guc / oc_guc_tablo (gerçek ABD 2023-26 eş farkı dağılımı; veri yoksa σ = %25 varsayımı) -> guc_tablosu.json (sha ön kayıtta).

Komut:  python ORTAK_CETVEL.py guc        güç tablosu (ABD 2023-26 rastgele hisse-gün; arastirma_cikti/ortak_cetvel/GUC_TABLOSU.md + guc_tablosu.json)
        python ORTAK_CETVEL.py onkayit    CETVEL_ON_KAYIT.md (OC_ESIK tam metni, mühür, kod sha, güç sha, kontrol listesi)
        python ORTAK_CETVEL.py kapi <yol> verilen ön kaydı oc_kapi'dan geçirir
        python ORTAK_CETVEL.py sha        cetvel / kod / güç sha'ları
Kullanım (aşama modülü):  import ORTAK_CETVEL as OC; OC.oc_kapi(onkayit); V = {p: OC.oc_veri(p) for p in OC.OC_ESIK["pazar"]};
        S = OC.oc_olc(olaylar, V); print(OC.oc_rapor(S))
Colab:  exec(open('ORTAK_CETVEL.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_BIST.pkl, V_ABD.pkl, V_AVR.pkl (yoksa islenmis-veri dalından vpac); ABD ek: /tmp/veri2/k34_yahoo.pkl. Tiingo YOK.
Komisyon / kayma YOK. Evren bugün işlem gören hisseler (+ k34 nakdi biten, yine bugün işlem gören): hayatta kalma yanlılığı vardır, yazılır.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_OC = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_OC = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_OC not in sys.path:
    sys.path.insert(0, KOK_OC)

oclog = logging.getLogger("col.ortak_cetvel")
if not oclog.handlers:
    _oc_h = logging.StreamHandler(sys.stderr)
    _oc_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s ortak_cetvel: %(message)s", "%H:%M:%S"))
    oclog.addHandler(_oc_h)
    oclog.setLevel(logging.INFO)
    oclog.propagate = False

OC_SURUM = "ORTAK_CETVEL v1.0 (2026-11-14)"
OC_YOL = {"cikti": os.path.join(KOK_OC, "arastirma_cikti", "ortak_cetvel"), "veri": os.environ.get("OC_VERI", "/tmp/veri"),
          "veri2": os.environ.get("OC_VERI2", "/tmp/veri2"), "kod": os.path.join(KOK_OC, "ORTAK_CETVEL.py"),
          "k34_evren": os.path.join(KOK_OC, "arastirma_cikti", "col_yolu_abd", "k34_evren.csv"),
          "evren_disi": [os.path.join(KOK_OC, "evren_disi_ABD.csv"), os.path.join(KOK_OC, "arastirma_cikti", "k55_dallanma", "K55_EVREN_DISI.csv")],
          "iv_worktree": "/tmp/iv"}
OC_DOSYA = {"onkayit": "CETVEL_ON_KAYIT.md", "guc_json": "guc_tablosu.json", "guc_md": "GUC_TABLOSU.md", "guc_ham": "guc_ham.csv"}

# ================================================================ MÜHÜRLÜ CETVEL (sonuç görüldükten sonra DEĞİŞMEZ)
OC_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "kriz": "2026-08-31",   # fon krizi: fiyatlar bu günde kesilir; ölçü penceresi bu günü aşan olay o ölçüde ölçülmez
    "pazar": ["ABD", "AVR", "BIST"],
    "donem": [["2016-22", "2016-01-01", "2022-12-31"], ["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-08-31"]],
    "donem_tarih": "giriş günü",
    "kesif_donem": "2016-22", "karar_pazar": ["ABD", "AVR"], "karar_donem": ["2023", "2024-26"], "bilgi_pazar": ["BIST"],
    "olay": {
        "girdi": "DataFrame[sembol, tarih (sinyal günü t; yalnız t'ye kadar bilgi), pazar]",
        "giris": "t'den sonraki ilk GEÇERLİ bar (hissenin kendi takvimi) AÇILIŞI; t ile giriş arası en çok 10 birleşik takvim işlem günü",
        "giris_azami_bosluk": 10,
        "sinyal_bar": "t hissenin ham verisinde bir bar ise geçerli olmalı (H>L, V>0); t bar değilse (hafta sonu haber) serbest",
        "tekil_gun": 60,
        "tekil": "aynı hissede, geçmiş bilgili süzgeçlerden (geçerli bar, havuz üyeliği) SONRA, giriş günü sırasıyla ilk olay tutulur; "
                 "sonraki olay birleşik takvimde >= 60 işlem günü sonra olmalı; ölçüm düşmeleri (kriz kesiği, ileri bölünme) tekilleştirmeyi etkilemez",
    },
    "gecerli_bar": "O, H, L, C > 0 ve sonlu, H > L, V > 0 (değilse bar veriden atılır: bayat fiyat sinyal / ölçü üretmez)",
    "likidite": {"gun": 20, "min_gun": 10, "olcu": "C*V (AVR: *Kur, EUR); giriş gününden ÖNCEKİ 20 birleşik takvim gününün medyanı (shift 1)",
                 "alt_kesik": 0.20, "kesit": "giriş günü, geçerli barı ve sonlu likiditesi olan pazar hisseleri; alt %20 havuzdan ve olaydan çıkar"},
    "bolunme": {"aktif": True, "esik": 0.25, "geri_gun": 10, "geri_pay": 0.5,
                "oranlar": [1.5, 2, 3, 4, 5, 6, 8, 10, 15, 20, 25, 30, 40, 50, 100], "oran_tol": 0.04,
                "gecmis_pencere": [-61, -1],
                "ileri": "UYGULANMAZ: ileri ölçü penceresinde şüphe dışlama sonuca göre seçimdir (gerçek ±%33-50 / 2 kat günleri siler; "
                         "ABD 2023-25 havuzunda 250 gün penceresinin %5'i, k34'te %9'u); veri fi_k1_veri düzeltilmiş, FON_IZI r60'ı da dışlamaz",
                "tanim": "SIKISMA_YENIDEN ANA kuralı (sy_bolunme_supheli ile aynı): |günlük basit getiri| > %25, 10 gün sonra sıçramanın en az "
                         "yarısı duruyor, önceki 10 gün düz VE |ln getiri| bir bölünme oranının ln'ine ±0,04 yakın (en küçük oran 1,5 olduğu için "
                         "iş tanımındaki '|ln| > ln 1,25' ile aynı günleri seçer). Geçmiş penceresinde [d-61, d-1] şüpheli günü olan hisse o gün "
                         "havuzdan (olay + eş) çıkar (momentum / likidite bozulmasın). İleri pencerede dışlama YOK (bkz. 'ileri')."},
    "esli": {"mom": 60, "mom_kova": 5, "likit": 20, "likit_kova": 3, "min_havuz": 30, "min_es": 3, "havuz": "gecmis",
             "tanim": "FON_IZI FI_OLCUT ile aynı: giriş günü d; momentum = C(d-1)/C(d-61)-1 (kapanış en çok 5 gün ileri taşınır); likidite = "
                      "önceki 20 gün medyan C*V; o gün havuzdaki hisseler arasında sıra (rank first) -> 5 momentum x 3 likidite kovası (qcut); "
                      "eş = aynı gün, aynı kova, olay hissesi hariç, o ölçüde ölçülebilir hisseler; en az 3 eş. "
                      "HAVUZ 'gecmis': kovalar yalnız d günü bilinenlerle (geçerli bar, momentum, likidite, alt %20 dışı, geçmiş bölünme dışı) "
                      "kurulur; FON_IZI'de havuz ileri r60'ı olan hisselerle kurulur (ileri bilgi). Gelecek tam olduğunda ikisi birebir aynıdır (test)."},
    "olcu": {"ufuk": 60, "cikis": "giriş + 59 birleşik takvim günü kapanışı (yoksa en çok 5 gün önceki son kapanış; FON_IZI ile aynı)",
             "bootstrap": 2000, "tohum": 27, "guven": [0.025, 0.975], "kume": "giriş ayı",
             "slot": 10, "slot_takvim_carpan": 1.45, "port_n": 200, "port_yuzde": 0.90,
             "dokunma_ufuk": 250, "dokunma_yukari": 1.00, "dokunma_asagi": -0.50,
             "once_ufuk": 60, "once_yukari": 0.20, "once_asagi": -0.10, "bilgi_ufuk": 20,
             "dokunma_tanim": "giriş günü dahil ufuk kadar birleşik takvim gününde geçerli barların High / Low'u giriş açılışına göre; aynı gün iki "
                              "eşik = aşağı önce sayılır; ufuk kriz kesiğini ya da hissenin son barını (5 gün pay) aşarsa ölçülmez",
             "kat": "KAT = Σ olay göstergesi / Σ olayın eş oranı (eş: aynı gün aynı hücre); TABAN KAT = Σ olay / Σ aynı gün bütün havuz oranı "
                    "(olay hissesi hariç); %95 aralık ay kümeli bootstrap (2000, tohum 27)"},
    "hucre_karar": {"n_esik": 30, "port_yuzde": 0.90, "sira_esik": 0.50,
                    "tanim": "TUTAR = (1) n >= 30; (2) ortalama eşli fark > 0 VE ay kümeli %95 alt uç > 0; (3) ortalama hücre içi sıra > 0,50; "
                             "(4) slot portföyü > 200 plasebo portföyün %90 yüzdeliği; (5) İKİ ALT DÖNEM AYNI YÖN: hücre olayları giriş "
                             "sırasıyla iki yarıya (ilk floor(n/2) / kalan) bölünür, iki yarının ortalama eşli farkı da > 0. "
                             "(1)-(4) FON_IZI FI_OLCUT dört şartıdır."},
    "etiket": {"n_yeter": 1000, "guc_esik": 0.80, "guc_delta_ref": 0.05,
               "guc_bak": "güç tablosunda hücre n'inden küçük ya da eşit en büyük n satırı (muhafazakâr); n < 30 -> güç 0",
               "hucre": "n < 30 ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, δ=+%5) >= %80) -> TUTMADI; değilse ÖLÇÜLEMEDİ",
               "genel": "İZ = dört karar hücresi TUTAR (BIST 2023 + 2024-26 da TUTAR ise 'İZ + BIST'); EMARE = en az bir karar hücresi TUTAR "
                        "ama dördü değil (tek pazar / tek dönem; AVR'de veri yoksa ve ABD iki dönem TUTAR -> 'EMARE (ABD-ADAY; AVR verisi yok)'); "
                        "İZ DEĞİL = hiçbir karar hücresi TUTMAZ ve verisi olan bütün karar hücreleri TUTMADI (güç yeterli); "
                        "ÖLÇÜLEMEDİ = öteki durumlar (TUTAR yok ama en az bir karar hücresi güçsüz). Keşif 2016-22 ve BIST bilgi.",
               "olasilik": "hücre: n_250 < 30 ÖLÇÜLEMEDİ; +%100 eş katının alt ucu > 1 VE -%50 eş katının üst ucu < 1 -> SEÇİCİ; ikisinin de "
                           "alt ucu > 1 -> PİYANGO; aksi YOK. Genel: dört karar hücresi aynı (SEÇİCİ ya da PİYANGO) ise o; herhangi bir karar "
                           "hücresi ÖLÇÜLEMEDİ ise ÖLÇÜLEMEDİ; aksi YOK."},
    "guc": {"n": [30, 100, 300, 1000, 3000], "delta": [0.0, 0.02, 0.05, 0.10], "tekrar": 200, "tohum": 1477,
            "kaynak": "ABD (V_ABD + k34), giriş 2023-01-01 .. 2026-06-30, havuzda olan, r60'ı ölçülebilir ve en az 3 eşi olan rastgele hisse-gün "
                      "(yerine koymadan); olayın r60'ına δ eklenir, eşler dokunulmaz (K58 k58_delta_ekle ile aynı); güç = hücrenin TUTTUĞU tekrar payı",
            "bas": "2023-01-01", "son": "2026-06-30", "sigma_varsayim": 0.25, "sentetik_es": 20, "sentetik_ay": 42,
            "k58_kontrol": {"delta": 0.02, "n_max": 300, "k58_ust": 0.11, "pay": 0.05,
                            "tanim": "dört şartlı güç (δ +%2, n <= 300) K58'in bulduğu en yüksek değeri (%11) + 5 puan aşmamalı"}},
    "veri": {"abd_ek": "k34_yahoo (nakdi biten, bugün işlem gören 2.246 şirket; V_ABD'de olmayanlar eklenir, evrene k34_evren ilk_giris "
                       "gününden itibaren girer; 'batanlar dahil' SAYILMAZ)", "abd_ek_aktif": True,
             "evren_disi": "ABD: evren_disi_ABD.csv (varsa) + K55_EVREN_DISI.csv 'fon_evren_disi' satırları (ETF / fon) çıkar",
             "min_bar": 80, "tiingo": False},
}

OC_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü, aynı pazar, aynı momentum beşliği x likidite üçlüsü (FI_OLCUT; test_ortak_cetvel FON_IZI ile birebir), "
                   "aynı giriş (açılış) / çıkış (60. gün) geometrisi; plasebo 200 portföy aynı gün aynı hücreden rastgele hisse; güç simülasyonu "
                   "rastgele hisse-gün (δ=0 yanlış pozitif payı tabloda). Mekanik üstünlük: sinyal tanımı her aşamanın ön kaydında ayrıca yazılır"),
    "K2": ("EVET", "havuz 'gecmis': kovalar yalnız d günü bilinenle (FON_IZI'deki ileri r60 şartı kaldırıldı); momentum d-1'e, likidite d-1'e kadar; "
                   "test 'geleceğe bakma': seri d'de kesilince hücre etiketleri aynı (fi kipinde aynı DEĞİL, test gösterir); sınır: bölünme "
                   "şüphesi tespiti 10 gün sonrasını kullanır (veri temizliği, raporda)"),
    "K3": ("EVET", "oc_veri_hazirla: H>L, V>0, O/H/L/C>0 olmayan bar atılır; sinyal günü barı geçersizse olay düşer (sayımda); dokunma ölçüleri yalnız geçerli bar"),
    "K4": ("EVET", "oc_olay_hazirla: aynı hissede 60 birleşik takvim işlem gününde tek olay (geçmiş bilgili süzgeçlerden sonra); n = bağımsız olay; "
                   "hücre tablosunda ortalama yanında medyan"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (hissenin kendi takvimi; en çok 10 gün boşluk); test 'giriş ertesi açılış'"),
    "K6": ("EVET", "tek kip: fi_k1_veri düzeltilmiş fiyat (V_*.pkl); getiri oranı birimden bağımsız; AVR likidite *Kur (EUR); bölünme şüphesi "
                   "(SIKISMA_YENIDEN ANA) geçmiş pencerede [d-61, d-1] dışarıda (sayımda ayrı); ileri pencerede dışlama yok (sonuca göre seçim "
                   "olurdu; şüphelilerin %70'i 1,5 kat oranlı gerçek günlük hareket); 100x pens / sterlin sıçraması oran listesinde (100)"),
    "K7": ("EVET", "evren bugün işlem görenler (V_*) + ABD k34 nakdi biten (yine bugün işlem gören; batanlar YOK, Tiingo YOK); raporda "
                   "'hayatta kalma yanlılığı: getiriler yukarı, -%50 olasılığı aşağı yanlı' notu her oc_rapor'da basılır"),
    "K8": ("EVET", "3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki alt dönem (hücre yarıları) aynı yön şartı; İZ DEĞİL yalnız güç yeterliyken "
                   "(n >= 1.000 ya da güç %80, guc_tablosu.json); çoklu karşılaştırma: aşama ön kaydında yazılır"),
    "K9": ("EVET", "OC_ESIK sha256 + kod sha256 + güç tablosu sha256 CETVEL_ON_KAYIT.md'de; oc_kapi üçünü + git işlenmiş/değişmemiş + "
                   "IZ_KARNE.ik_kontrol_kapisi denetler, tutmazsa durur (test 'kapı'); eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV; aşama modülü olay kaynağını kendi ön kaydında denetler"),
    "K11": ("EVET", "oc_olc olay satırlarını (_esler hariç) döndürür; aşama raporu >= 2 hücreyi satır dosyasından bağımsız yeniden üretir; "
                    "bu işte güç tablosunun 2 satırı ham csv'den yeniden üretildi (GUC_TABLOSU.md)"),
    "K12": ("EVET", "etiketler (İZ / İZ DEĞİL / ÖLÇÜLEMEDİ / EMARE / SEÇİCİ / PİYANGO) yalnız oc_etiket kuralıyla; fiyat değişimi ile işlem "
                    "kârı ayrı (komisyon yok yazılır); sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_oc; yasak dosyalara dokunulmaz (git diff); e-posta / anahtar taraması testte; ücretli veri / Tiingo yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm cetveli"),
}


class OCHata(RuntimeError):
    """Durdurucu hata: mühür / kod / güç sha'sı tutmuyor, ön kayıt git'e işlenmemiş ya da değişmiş, veri yok, girdi bozuk."""


# ================================================================ 0) ORTAK
_OC_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _oc_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _oc_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def oc_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """OC_ESIK'in kanonik JSON'unun sha256'sı (cetvel mührü)."""
    s = json.dumps(OC_ESIK if E is None else E, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def oc_kod_sha(yol: Optional[str] = None) -> str:
    """ORTAK_CETVEL.py dosyasının bayt sha256'sı."""
    return _oc_sha_dosya(yol or OC_YOL["kod"])


def oc_guc_sha(yol: Optional[str] = None) -> str:
    yol = yol or os.path.join(OC_YOL["cikti"], OC_DOSYA["guc_json"])
    if not os.path.exists(yol):
        raise OCHata(f"güç tablosu yok: {yol} (önce `python ORTAK_CETVEL.py guc`)")
    return _oc_sha_dosya(yol)


def _oc_donem(t: pd.Series, E: Dict[str, Any]) -> np.ndarray:
    t = pd.to_datetime(pd.Series(t)).reset_index(drop=True)
    out = np.array([""] * len(t), dtype=object)
    for ad, a, b in E["donem"]:
        out[((t >= pd.Timestamp(a)) & (t <= pd.Timestamp(b))).to_numpy()] = ad
    return out


def _oc_git_islenmis(yol: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve işlendikten sonra değişmemiş olmalı."""
    kl, ad = os.path.dirname(os.path.abspath(yol)), os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H %cI", "--", ad], capture_output=True, text=True, timeout=60)
        d = subprocess.run(["git", "-C", kl, "status", "--porcelain", "--", ad], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as ex:
        raise OCHata(f"git çalıştırılamadı ({ex}); {yol} işlenmiş mi doğrulanamadı")
    if r.returncode != 0 or not r.stdout.strip():
        raise OCHata(f"git'e işlenmemiş: {yol} (önce commit + push)")
    if d.returncode != 0 or d.stdout.strip():
        raise OCHata(f"git'e işlendikten sonra değişmiş: {yol} ({d.stdout.strip() or d.stderr.strip()})")
    h, z = r.stdout.strip().split(" ", 1)
    return {"commit": h, "commit_zamani": z}


# ================================================================ 1) VERİ
def oc_veri_hazirla(d: pd.DataFrame, E: Dict[str, Any] = OC_ESIK) -> Tuple[pd.DataFrame, pd.DatetimeIndex]:
    """Geçerli bar süzgeci (H>L, V>0, O/H/L/C>0 sonlu), kriz kesiği, Kur sütunu (yoksa 1). Döner: (temiz veri, geçersiz bar tarihleri)."""
    d = d.copy()
    if isinstance(d.columns, pd.MultiIndex):
        d.columns = d.columns.get_level_values(0)
    if "Kur" not in d.columns:
        d["Kur"] = 1.0
    d = d[["Open", "High", "Low", "Close", "Volume", "Kur"]].astype(float)
    ix = pd.DatetimeIndex(d.index)
    d.index = (ix.tz_convert(None) if ix.tz is not None else ix).normalize()
    d = d[~d.index.duplicated(keep="last")].sort_index()
    d = d[d.index <= pd.Timestamp(E["kriz"])]
    fin = np.isfinite(d[["Open", "High", "Low", "Close", "Volume"]]).all(axis=1)
    ok = fin & (d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & (d.Low > 0)
    gecersiz = pd.DatetimeIndex(d.index[~ok])
    d = d[ok].copy()
    d["Kur"] = d["Kur"].ffill().bfill().fillna(1.0)
    return d, gecersiz


def _oc_evren_disi() -> set:
    out = set()
    for yol in OC_YOL["evren_disi"]:
        if not os.path.exists(yol):
            continue
        try:
            t = pd.read_csv(yol)
            if "kategori" in t.columns:
                t = t[t.kategori.astype(str) == "fon_evren_disi"]
            out |= set(t["sembol"].astype(str).str.upper())
        except Exception as ex:
            oclog.warning("evren dışı listesi okunamadı (%s): %s", yol, ex)
    return out


def _oc_vpac(klasor: str) -> None:
    """islenmis-veri dalından /tmp/veri paketini açar (git worktree + FON_IZI vpac). Ağ / git yoksa OCHata."""
    wt = OC_YOL["iv_worktree"]
    try:
        if not os.path.isdir(os.path.join(wt, "veri")):
            subprocess.run(["git", "-C", KOK_OC, "fetch", "origin", "islenmis-veri"], capture_output=True, text=True, timeout=600)
            r = subprocess.run(["git", "-C", KOK_OC, "worktree", "add", wt, "origin/islenmis-veri"], capture_output=True, text=True, timeout=600)
            if r.returncode != 0:
                raise OCHata(f"worktree açılamadı: {r.stderr.strip()}")
        r = subprocess.run([sys.executable, os.path.join(KOK_OC, "FON_IZI.py"), "vpac", os.path.join(wt, "veri"), klasor],
                           capture_output=True, text=True, timeout=3600)
        if r.returncode != 0:
            raise OCHata(f"vpac başarısız: {r.stderr.strip()[-500:]}")
    except (OSError, subprocess.SubprocessError) as ex:
        raise OCHata(f"veri paketi açılamadı: {ex}")


def oc_veri(pazar: str, E: Dict[str, Any] = OC_ESIK, klasor: Optional[str] = None, veri2: Optional[str] = None) -> Dict[str, Any]:
    """pazar -> {'pazar', 'V': {sembol: temiz OHLCV+Kur}, 'gecersiz': {sembol: tarihler}, 'evren_bas': {sembol: Timestamp}, 'not': [...]}.
    V_<pazar>.pkl yoksa islenmis-veri dalından açılır. ABD: k34_yahoo eklenir (V_ABD'de olmayanlar; evren_bas = k34_evren ilk_giris), fonlar çıkar."""
    if pazar not in E["pazar"]:
        raise OCHata(f"bilinmeyen pazar {pazar}")
    klasor = klasor or OC_YOL["veri"]
    yol = os.path.join(klasor, f"V_{pazar}.pkl")
    if not os.path.exists(yol):
        oclog.info("%s yok; islenmis-veri dalından açılıyor", yol)
        _oc_vpac(klasor)
        if not os.path.exists(yol):
            raise OCHata(f"veri yok: {yol}")
    ham = pd.read_pickle(yol)
    if isinstance(ham, dict) and "veri" in ham and isinstance(ham["veri"], dict):
        ham = ham["veri"]
    out: Dict[str, Any] = {"pazar": pazar, "V": {}, "gecersiz": {}, "evren_bas": {}, "kaynak": {}, "not": []}

    def ekle(s: str, d: pd.DataFrame, kaynak: str, bas: Optional[pd.Timestamp] = None) -> None:
        try:
            x, g = oc_veri_hazirla(d, E)
        except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer
            oclog.warning("%s %s atlandı: %s", pazar, s, ex); return
        if len(x) < E["veri"]["min_bar"]:
            return
        out["V"][s] = x; out["gecersiz"][s] = g; out["kaynak"][s] = kaynak
        if bas is not None:
            out["evren_bas"][s] = pd.Timestamp(bas)

    for s, d in ham.items():
        ekle(str(s), d, f"V_{pazar}")
    if pazar == "ABD" and E["veri"]["abd_ek_aktif"]:
        yy = os.path.join(veri2 or OC_YOL["veri2"], "k34_yahoo.pkl")
        if os.path.exists(yy) and os.path.exists(OC_YOL["k34_evren"]):
            Y = pd.read_pickle(yy); ev = pd.read_csv(OC_YOL["k34_evren"], parse_dates=["ilk_giris"])
            ev = ev[ev.kaynak.astype(str) == "yahoo"].drop_duplicates("sembol")
            n0 = len(out["V"])
            for r in ev.itertuples():
                if r.sembol in out["V"] or r.sembol not in Y:
                    continue
                ekle(str(r.sembol), Y[r.sembol], "k34_yahoo", r.ilk_giris)
            out["not"].append(f"k34_yahoo eklendi: {len(out['V']) - n0} hisse (evrene ilk_giris gününden itibaren; bugün işlem görenler, batan YOK)")
        else:
            out["not"].append("k34_yahoo ya da k34_evren.csv yok: ABD evreni yalnız V_ABD")
    if pazar == "ABD":
        disi = _oc_evren_disi(); at = sorted(s for s in out["V"] if s.upper() in disi)
        for s in at:
            for k in ("V", "gecersiz", "evren_bas", "kaynak"):
                out[k].pop(s, None)
        out["not"].append(f"evren dışı (fon / ETF) çıkarılan: {len(at)} {at[:10]}")
    out["not"].append("hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı")
    oclog.info("%s: %d hisse (%s)", pazar, len(out["V"]), yol)
    return out


def _oc_veri_sar(V: Any, pazar: str = "?") -> Dict[str, Any]:
    """Düz {sembol: DataFrame} sözlüğünü oc_veri biçimine sarar (sentetik test / dış kullanım)."""
    if isinstance(V, dict) and "V" in V and isinstance(V.get("V"), dict):
        return V
    out = {"pazar": pazar, "V": {}, "gecersiz": {}, "evren_bas": {}, "kaynak": {}, "not": []}
    for s, d in V.items():
        x, g = oc_veri_hazirla(d)
        out["V"][str(s)] = x; out["gecersiz"][str(s)] = g; out["kaynak"][str(s)] = "dis"
    return out


# ================================================================ 2) BÖLÜNME ŞÜPHESİ (SIKISMA_YENIDEN ANA ile aynı)
def oc_bolunme_supheli(C: np.ndarray, E: Dict[str, Any] = OC_ESIK) -> np.ndarray:
    """Bölünme şüphesi günleri (bool; bar i: C[i-1] -> C[i]). SIKISMA_YENIDEN.sy_bolunme_supheli (kati=False) ile aynı."""
    B = E["bolunme"]; n = len(C); s = np.zeros(n, bool)
    if n < 2 or not B.get("aktif", True):
        return s
    with np.errstate(all="ignore"):
        r = np.r_[np.nan, np.log(C[1:] / C[:-1])]
        aday = np.where(np.abs(np.r_[np.nan, C[1:] / C[:-1] - 1]) > B["esik"])[0]
    for i in aday:
        j = min(n - 1, i + B["geri_gun"])
        kalici = abs(math.log(C[j] / C[i - 1])) >= B["geri_pay"] * abs(r[i])
        once = max(0, i - 1 - B["geri_gun"])
        duz_once = abs(math.log(C[i - 1] / C[once])) < B["geri_pay"] * abs(r[i])
        if not (kalici and duz_once):
            continue
        lr = abs(r[i])
        if any(abs(lr - math.log(k)) < B["oran_tol"] for k in B["oranlar"]):
            s[i] = True
    return s


def _oc_pencere_say(cs: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """cs: (n+1, u) kümülatif toplam; satır d için [a_d, b_d] (dahil, kırpılmış) toplamı."""
    n = cs.shape[0] - 1
    lo = np.clip(a, 0, n); hi = np.clip(b + 1, 0, n)
    return cs[hi] - cs[lo]


# ================================================================ 3) PANEL (giriş günü x hisse)
def oc_panel(Vd: Any, E: Dict[str, Any] = OC_ESIK, kip: Optional[str] = None) -> Dict[str, Any]:
    """Birleşik takvimde giriş günü d x hisse: Op/Hi/Lo/Cl, r60 (R), momentum (M), likidite (Lq), havuz (ok), r60 ölçülebilir (okR),
    hücre (H; -1 = havuz dışı). kip 'gecmis' (mühürlü) ya da 'fi' (FON_IZI fi_olcut_panel ile birebir; yalnız test / uyum)."""
    Vd = _oc_veri_sar(Vd)
    kip = kip or E["esli"]["havuz"]
    if kip not in ("gecmis", "fi"):
        raise OCHata(f"havuz kipi {kip} bilinmiyor")
    V = Vd["V"]; S = sorted(V)
    if not S:
        raise OCHata("panel: boş veri")
    idx = pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in S])))
    kriz = idx.searchsorted(pd.Timestamp(E["kriz"]), side="right")
    n, u = len(idx), len(S); h = E["olcu"]["ufuk"]; Es = E["esli"]

    def tablo(kol):
        return pd.DataFrame({s: V[s][kol] for s in S}).reindex(idx).to_numpy(float)
    Op, Hi, Lo, Cl = tablo("Open"), tablo("High"), tablo("Low"), tablo("Close")
    Tl = pd.DataFrame({s: V[s].Close * V[s].Volume * V[s].Kur for s in S}).reindex(idx)
    Cf = pd.DataFrame(Cl).ffill(limit=5).to_numpy()
    R = np.full((n, u), np.nan); son = min(n, kriz)
    if son - h + 1 > 0:
        with np.errstate(all="ignore"):
            R[:son - h + 1] = Cf[h - 1:son] / Op[:son - h + 1] - 1
    M = np.full((n, u), np.nan)
    if n > Es["mom"] + 1:
        with np.errstate(all="ignore"):
            M[Es["mom"] + 1:] = Cf[Es["mom"]:-1] / Cf[:-Es["mom"] - 1] - 1
    Lq = Tl.rolling(Es["likit"], min_periods=E["likidite"]["min_gun"]).median().shift(1).to_numpy()
    gec = np.isfinite(Op) & (Op > 0)
    # bölünme şüphesi (hissenin kendi geçerli kapanışları) -> birleşik takvim konumu
    sup = np.zeros((n, u), bool)
    if E["bolunme"].get("aktif", True):
        for j, s in enumerate(S):
            sj = oc_bolunme_supheli(V[s].Close.to_numpy(float), E)
            if sj.any():
                sup[idx.get_indexer(V[s].index[sj]), j] = True
    cs_sup = np.vstack([np.zeros((1, u), int), np.cumsum(sup, axis=0)])
    dd = np.arange(n)
    ga, gb = E["bolunme"]["gecmis_pencere"]
    sup_gecmis = _oc_pencere_say(cs_sup, dd + ga, dd + gb) > 0
    son_bar = np.array([idx.get_loc(V[s].index[-1]) for s in S])
    lik_alt = np.zeros((n, u), bool)
    evb = np.array([idx.searchsorted(Vd["evren_bas"][s]) if s in Vd.get("evren_bas", {}) else 0 for s in S])
    okR = np.isfinite(R)
    if kip == "fi":
        ok = np.isfinite(R) & np.isfinite(M) & np.isfinite(Lq) & np.isfinite(Op) & (Op > 0)
        okR = ok.copy()
    else:
        ok = gec & np.isfinite(M) & np.isfinite(Lq) & ~sup_gecmis & (dd[:, None] >= evb[None, :])
        ak = E["likidite"]["alt_kesik"]
        if ak > 0:
            taban = gec & np.isfinite(Lq)
            for d in range(n):
                g = taban[d]
                if g.sum() < 2:
                    continue
                q = np.quantile(Lq[d, g], ak)
                lik_alt[d] = Lq[d] < q
                ok[d] &= ~lik_alt[d]
    H = np.full((n, u), -1, int)
    for d in range(n):
        g = ok[d]
        if g.sum() < Es["min_havuz"]:
            continue
        mq = pd.qcut(pd.Series(M[d, g]).rank(method="first"), Es["mom_kova"], labels=False).to_numpy()
        lq = pd.qcut(pd.Series(Lq[d, g]).rank(method="first"), Es["likit_kova"], labels=False).to_numpy()
        H[d, g] = mq * Es["likit_kova"] + lq
    return {"pazar": Vd.get("pazar", "?"), "kip": kip, "tarih": idx, "sembol": S, "kol": {s: i for i, s in enumerate(S)},
            "Op": Op, "Hi": Hi, "Lo": Lo, "R": R, "M": M, "Lq": Lq, "H": H, "ok": ok, "okR": okR, "sup": sup, "cs_sup": cs_sup,
            "sup_gecmis": sup_gecmis, "lik_alt": lik_alt, "evb": evb,
            "son_bar": son_bar, "kriz_i": son - 1, "gecersiz": Vd.get("gecersiz", {}), "Vidx": {s: V[s].index for s in S},
            "not": list(Vd.get("not", []))}


# ================================================================ 4) OLAYLAR
def oc_olay_hazirla(olaylar: pd.DataFrame, P: Dict[str, Any], E: Dict[str, Any] = OC_ESIK) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Sinyal (sembol, tarih) -> giriş günü (t'den sonraki ilk geçerli bar), havuz üyeliği, tekilleştirme. Yalnız t / giriş açılışı bilgisi.
    Döner: (olay tablosu: sembol, tarih, giris, d, j, hucre, donem), düşme sayımı."""
    say = {"girdi": int(len(olaylar)), "sembol_yok": 0, "sinyal_bar_gecersiz": 0, "giris_yok": 0, "giris_gec": 0, "likidite_alt20": 0,
           "bolunme_gecmis": 0, "evren_once": 0, "gecmis_eksik": 0, "havuz_az": 0, "havuz_disi": 0, "tekil": 0}
    if not len(olaylar):
        return pd.DataFrame(columns=["sembol", "tarih", "giris", "d", "j", "hucre", "donem"]), say
    idx = P["tarih"]; sat = []
    for r in olaylar.itertuples(index=False):
        s = str(r.sembol); t = pd.Timestamp(r.tarih).normalize(); j = P["kol"].get(s)
        if j is None:
            say["sembol_yok"] += 1; continue
        if t in P["gecersiz"].get(s, pd.DatetimeIndex([])):
            say["sinyal_bar_gecersiz"] += 1; continue
        vi = P["Vidx"][s]; k = vi.searchsorted(t, side="right")
        if k >= len(vi):
            say["giris_yok"] += 1; continue
        g = vi[k]; d = idx.get_loc(g); dt = idx.searchsorted(t, side="right")
        if d - dt + 1 > E["olay"]["giris_azami_bosluk"]:
            say["giris_gec"] += 1; continue
        if not P["ok"][d, j] or P["H"][d, j] < 0:
            say["havuz_disi"] += 1
            if P["kip"] == "gecmis":
                if not (np.isfinite(P["M"][d, j]) and np.isfinite(P["Lq"][d, j])):
                    say["gecmis_eksik"] += 1
                elif P["sup_gecmis"][d, j]:
                    say["bolunme_gecmis"] += 1
                elif P["lik_alt"][d, j]:
                    say["likidite_alt20"] += 1
                elif d < P["evb"][j]:
                    say["evren_once"] += 1
                else:
                    say["havuz_az"] += 1
            continue
        sat.append((s, t, g, d, j, int(P["H"][d, j])))
    X = pd.DataFrame(sat, columns=["sembol", "tarih", "giris", "d", "j", "hucre"])
    if len(X):
        X = X.sort_values(["sembol", "d", "tarih"], kind="mergesort").reset_index(drop=True)
        tut = np.zeros(len(X), bool); son: Dict[str, int] = {}
        for i, (s, d) in enumerate(zip(X.sembol.to_numpy(), X.d.to_numpy())):
            if s not in son or d - son[s] >= E["olay"]["tekil_gun"]:
                tut[i] = True; son[s] = d
        say["tekil"] = int((~tut).sum()); X = X[tut].reset_index(drop=True)
    X["donem"] = _oc_donem(X.giris, E) if len(X) else []
    return X, say


def _oc_es_maske(P: Dict[str, Any], d: int, j: int, olcu: np.ndarray) -> np.ndarray:
    m = (P["H"][d] == P["H"][d, j]) & P["ok"][d] & olcu
    m[j] = False
    return m


def oc_esli(P: Dict[str, Any], X: pd.DataFrame, E: Dict[str, Any] = OC_ESIK) -> pd.DataFrame:
    """r60, eşli ortalama r60 (aynı gün, aynı hücre, hisse hariç, r60'ı ölçülebilir), hücre içi sıra, eşli fark, _esler (FON_IZI fi_olcut_olay ile aynı)."""
    sat = []
    for d, j in zip(X.d.to_numpy(int), X.j.to_numpy(int)):
        if not P["okR"][d, j] or not P["ok"][d, j]:
            sat.append((np.nan, np.nan, np.nan, None, 0)); continue
        m = _oc_es_maske(P, d, j, P["okR"][d])
        if m.sum() < E["esli"]["min_es"]:
            sat.append((P["R"][d, j], np.nan, np.nan, None, int(m.sum()))); continue
        e = P["R"][d, m]; x = P["R"][d, j]
        sat.append((x, float(e.mean()), float(((e < x).sum() + 0.5 * (e == x).sum()) / len(e)), e, int(m.sum())))
    X = X.copy()
    X["r60"] = [a[0] for a in sat]; X["esli_r60"] = [a[1] for a in sat]; X["sira"] = [a[2] for a in sat]
    X["fark"] = X.r60 - X.esli_r60; X["n_es"] = [a[4] for a in sat]; X["_esler"] = [a[3] for a in sat]
    X["giris_fiyat"] = P["Op"][X.d.to_numpy(int), X.j.to_numpy(int)] if len(X) else []
    return X


# ================================================================ 5) HÜCRE (FI_OLCUT dört şart + iki alt dönem)
def oc_hucre(X: pd.DataFrame, E: Dict[str, Any] = OC_ESIK, _plasebo: Optional[List[float]] = None) -> Dict[str, Any]:
    """Bir hücrenin olayları (fark, r60, esli_r60, sira, giris, _esler). FON_IZI fi_olcut_hucre ile aynı algoritma ve aynı rastgele sıra
    (tohum 27: önce ay bootstrap, sonra 200 plasebo portföy); ek: iki yarı ortalama eşli fark ve şart bayrakları."""
    O = E["olcu"]; K = E["hucre_karar"]
    X = X.dropna(subset=["fark"]).sort_values("giris")
    if not len(X):
        return {"n": 0, "tutar": False, "tutar4": False}
    ay = pd.to_datetime(X.giris).dt.to_period("M").astype(str).to_numpy(); aylar = np.unique(ay)
    rng = np.random.default_rng(O["tohum"]); f = X.fark.to_numpy(float)
    grup = {a: f[ay == a] for a in aylar}; ort = []
    for _ in range(O["bootstrap"]):
        sec = rng.choice(aylar, len(aylar), replace=True)
        v = np.concatenate([grup[a] for a in sec]); ort.append(v.mean())
    gun = pd.to_datetime(X.giris).to_numpy().astype("datetime64[D]").astype(np.int64)
    tut_gun = int(O["ufuk"] * O["slot_takvim_carpan"])

    def slot(getiri: np.ndarray) -> float:
        bos = np.zeros(O["slot"]); deger = np.ones(O["slot"]) / O["slot"]
        for gi, ri in zip(gun, getiri):
            k = int(np.argmin(bos))
            if bos[k] <= gi:
                deger[k] *= 1 + ri; bos[k] = gi + tut_gun
        return float(deger.sum() - 1)
    if _plasebo is None:
        esler = list(X["_esler"]) if "_esler" in X else [None] * len(X)
        rast = [slot(np.array([rng.choice(e) if e is not None and len(e) else x for e, x in zip(esler, X.r60.to_numpy(float))]))
                for _ in range(O["port_n"])]
    else:
        rast = list(_plasebo)
    yari = len(f) // 2
    y1 = float(f[:yari].mean()) if yari else np.nan; y2 = float(f[yari:].mean())
    out = {"n": int(len(X)), "ort_fark": float(f.mean()), "medyan_fark": float(np.median(f)), "alt95": float(np.quantile(ort, O["guven"][0])),
           "ust95": float(np.quantile(ort, O["guven"][1])), "ort_r60": float(X.r60.mean()), "ort_esli": float(X.esli_r60.mean()),
           "sira": float(X.sira.mean()), "kazanan": float((f > 0).mean()), "portfoy": slot(X.r60.to_numpy(float)),
           "portfoy_esli_p50": float(np.quantile(rast, 0.5)), "portfoy_esli_p90": float(np.quantile(rast, K["port_yuzde"])),
           "portfoy_esli_p10": float(np.quantile(rast, 1 - K["port_yuzde"])), "ay": int(len(aylar)), "yari1_fark": y1, "yari2_fark": y2}
    out["s_n"] = bool(out["n"] >= K["n_esik"]); out["s_fark"] = bool(out["ort_fark"] > 0 and out["alt95"] > 0)
    out["s_sira"] = bool(out["sira"] > K["sira_esik"]); out["s_port"] = bool(out["portfoy"] > out["portfoy_esli_p90"])
    out["s_yari"] = bool(np.isfinite(y1) and y1 > 0 and y2 > 0)
    out["tutar4"] = bool(out["s_n"] and out["s_fark"] and out["s_sira"] and out["s_port"])
    out["tutar"] = bool(out["tutar4"] and out["s_yari"])
    out["_plasebo"] = rast
    return out


# ================================================================ 6) OLASILIK (dokunma / önce)
def _oc_ileri_maks(A: np.ndarray, w: int, en: str) -> np.ndarray:
    """F[d] = A[d .. d+w-1] üzerinde NaN atlayarak maks / min (sütun başına)."""
    D = pd.DataFrame(A[::-1])
    R = D.rolling(w, min_periods=1).max() if en == "max" else D.rolling(w, min_periods=1).min()
    return R.to_numpy()[::-1]


def _oc_olculebilir(P: Dict[str, Any], d: int, w: int) -> np.ndarray:
    """d günü girişte w günlük ileri pencere: kriz kesiğini / hissenin son barını (5 gün pay) aşmıyor, giriş açılışı var (ileri bölünme dışlaması YOK)."""
    son = d + w - 1
    if son > P["kriz_i"]:
        return np.zeros(len(P["sembol"]), bool)
    return (P["son_bar"] >= son - 5) & np.isfinite(P["Op"][d]) & (P["Op"][d] > 0)


def _oc_once(P: Dict[str, Any], d: int, w: int, yuk: float, asg: float) -> Tuple[np.ndarray, np.ndarray]:
    """d girişli w gün: (yukarı önce, aşağı önce) göstergeleri, bütün hisseler; aynı gün iki eşik -> aşağı önce."""
    E0 = P["Op"][d]; Hw = P["Hi"][d:d + w]; Lw = P["Lo"][d:d + w]
    with np.errstate(invalid="ignore"):
        up = Hw >= E0 * (1 + yuk); dn = Lw <= E0 * (1 + asg)
    big = w + 10
    iu = np.where(up.any(0), up.argmax(0), big); idn = np.where(dn.any(0), dn.argmax(0), big)
    return (iu < idn), (idn <= iu) & (idn < big)


def oc_olasilik_olay(P: Dict[str, Any], X: pd.DataFrame, E: Dict[str, Any] = OC_ESIK) -> pd.DataFrame:
    """Olay başına: up100 / dn50 (250 gün dokunma), once20 (60 gün +%20 önce), u20 / d20 (20 gün); her biri için eş oranı (aynı gün aynı
    hücre, havuzda, o ölçüde ölçülebilir, hisse hariç) ve taban oranı (aynı gün bütün havuz, hisse hariç). Ölçülemeyen -> NaN."""
    O = E["olcu"]; X = X.copy()
    kol = ["up100", "dn50", "once20", "u20", "d20"]
    for k in kol:
        for on in ("", "es_", "tb_"):
            X[on + k] = np.nan
    if not len(X):
        return X
    w = O["dokunma_ufuk"]
    FH = _oc_ileri_maks(P["Hi"], w, "max"); FL = _oc_ileri_maks(P["Lo"], w, "min")
    for d in np.unique(X.d.to_numpy(int)):
        rows = np.where(X.d.to_numpy(int) == d)[0]
        Ed = P["Op"][d]; pool = P["ok"][d]
        gost: Dict[str, Tuple[np.ndarray, np.ndarray]] = {}
        m250 = _oc_olculebilir(P, d, w)
        with np.errstate(invalid="ignore"):
            gost["up100"] = ((FH[d] >= Ed * (1 + O["dokunma_yukari"])).astype(float), m250)
            gost["dn50"] = ((FL[d] <= Ed * (1 + O["dokunma_asagi"])).astype(float), m250)
        m60 = _oc_olculebilir(P, d, O["once_ufuk"])
        u60, _ = _oc_once(P, d, O["once_ufuk"], O["once_yukari"], O["once_asagi"])
        gost["once20"] = (u60.astype(float), m60)
        m20 = _oc_olculebilir(P, d, O["bilgi_ufuk"])
        u20, d20 = _oc_once(P, d, O["bilgi_ufuk"], O["once_yukari"], O["once_asagi"])
        gost["u20"] = (u20.astype(float), m20); gost["d20"] = (d20.astype(float), m20)
        for i in rows:
            j = int(X.j.iat[i])
            for k, (g, m) in gost.items():
                if not m[j]:
                    continue
                X.iat[i, X.columns.get_loc(k)] = g[j]
                es = _oc_es_maske(P, d, j, m)
                if es.sum() >= E["esli"]["min_es"]:
                    X.iat[i, X.columns.get_loc("es_" + k)] = float(g[es].mean())
                tb = pool & m; tb = tb.copy(); tb[j] = False
                if tb.sum() >= E["esli"]["min_es"]:
                    X.iat[i, X.columns.get_loc("tb_" + k)] = float(g[tb].mean())
    return X


def oc_kat(olay: np.ndarray, oran: np.ndarray, ay: np.ndarray, E: Dict[str, Any] = OC_ESIK) -> Dict[str, float]:
    """KAT = Σ olay / Σ oran; ay kümeli bootstrap %95 (2000, tohum 27). Geçerli satırlar: ikisi de sonlu."""
    O = E["olcu"]; g = np.isfinite(olay) & np.isfinite(oran)
    a, b, m = olay[g].astype(float), oran[g].astype(float), ay[g]
    out = {"n": int(g.sum()), "p_olay": float(a.mean()) if len(a) else np.nan, "p_ref": float(b.mean()) if len(b) else np.nan,
           "kat": np.nan, "alt": np.nan, "ust": np.nan}
    if not len(a) or b.sum() <= 0:
        return out
    out["kat"] = float(a.sum() / b.sum())
    aylar = np.unique(m); ga = {x: a[m == x].sum() for x in aylar}; gb = {x: b[m == x].sum() for x in aylar}
    rng = np.random.default_rng(O["tohum"]); v = []
    for _ in range(O["bootstrap"]):
        sec = rng.choice(aylar, len(aylar), replace=True)
        pa = sum(ga[x] for x in sec); pb = sum(gb[x] for x in sec)
        v.append(pa / pb if pb > 0 else np.nan)
    v = np.array(v, float); v = v[np.isfinite(v)]
    if len(v):
        out["alt"] = float(np.quantile(v, O["guven"][0])); out["ust"] = float(np.quantile(v, O["guven"][1]))
    return out


def oc_olasilik_hucre(X: pd.DataFrame, E: Dict[str, Any] = OC_ESIK) -> Dict[str, Any]:
    """Bir hücrenin olasılık tablosu satırı + etiketi."""
    ay = pd.to_datetime(X.giris).dt.to_period("M").astype(str).to_numpy() if len(X) else np.array([], dtype=object)
    out: Dict[str, Any] = {}
    for k in ("up100", "dn50", "once20", "u20", "d20"):
        for ref in ("es", "tb"):
            r = oc_kat(X[k].to_numpy(float), X[f"{ref}_{k}"].to_numpy(float), ay, E) if len(X) else {"n": 0}
            for a_, v in r.items():
                out[f"{k}_{ref}_{a_}"] = v
    out["n250"] = int(out.get("up100_es_n", 0))
    out["etiket"] = oc_olasilik_etiket(out, E)
    return out


def oc_olasilik_etiket(r: Dict[str, Any], E: Dict[str, Any] = OC_ESIK) -> str:
    if r.get("n250", 0) < E["hucre_karar"]["n_esik"]:
        return "ÖLÇÜLEMEDİ"
    ua, da, du = r.get("up100_es_alt", np.nan), r.get("dn50_es_alt", np.nan), r.get("dn50_es_ust", np.nan)
    if np.isfinite(ua) and ua > 1 and np.isfinite(du) and du < 1:
        return "SEÇİCİ"
    if np.isfinite(ua) and ua > 1 and np.isfinite(da) and da > 1:
        return "PİYANGO"
    return "YOK"


# ================================================================ 7) GÜÇ
def oc_guc_aday(P: Dict[str, Any], bas: str, son: str, E: Dict[str, Any] = OC_ESIK) -> Tuple[np.ndarray, np.ndarray]:
    """Güç için uygun hisse-günler: giriş [bas, son], havuzda, r60 ölçülebilir, aynı gün aynı hücrede en az min_es ölçülebilir eş."""
    idx = P["tarih"]; a = idx.searchsorted(pd.Timestamp(bas)); b = idx.searchsorted(pd.Timestamp(son), side="right")
    D, J = [], []
    for d in range(a, b):
        g = P["ok"][d] & P["okR"][d] & (P["H"][d] >= 0)
        if g.sum() < 2:
            continue
        say = np.bincount(P["H"][d, g], minlength=E["esli"]["mom_kova"] * E["esli"]["likit_kova"])
        jj = np.where(g)[0]; jj = jj[say[P["H"][d, jj]] - 1 >= E["esli"]["min_es"]]
        D.append(np.full(len(jj), d)); J.append(jj)
    return (np.concatenate(D) if D else np.array([], int)), (np.concatenate(J) if J else np.array([], int))


def oc_delta_ekle(X: pd.DataFrame, delta: float) -> pd.DataFrame:
    """Olayın r60'ına δ ekler; eşler dokunulmaz: fark ve sıra yeni r60 ile (K58 k58_delta_ekle ile aynı)."""
    Y = X.copy(); Y["r60"] = X.r60.to_numpy(float) + delta; Y["fark"] = Y.r60 - Y.esli_r60
    Y["sira"] = [float(((e < x).sum() + 0.5 * (e == x).sum()) / len(e)) if e is not None and len(e) else np.nan
                 for e, x in zip(X["_esler"], Y.r60.to_numpy(float))]
    return Y


def _oc_sentetik_olay(n: int, rng: np.random.Generator, E: Dict[str, Any]) -> pd.DataFrame:
    """Veri yoksa: σ = %25 normal varsayımı; her olayın sentetik_es eşi; olaylar sentetik_ay aya dağılır."""
    G = E["guc"]; s = G["sigma_varsayim"]; k = G["sentetik_es"]
    ay0 = pd.Timestamp(G["bas"]); gun = ay0 + pd.to_timedelta(rng.integers(0, G["sentetik_ay"] * 30, n), unit="D")
    es = [rng.normal(0, s, k) for _ in range(n)]; x = rng.normal(0, s, n)
    X = pd.DataFrame({"giris": gun, "r60": x, "esli_r60": [e.mean() for e in es]})
    X["_esler"] = es; X["fark"] = X.r60 - X.esli_r60
    X["sira"] = [float(((e < v).sum() + 0.5 * (e == v).sum()) / len(e)) for e, v in zip(es, x)]
    return X


def oc_guc(n: int, delta: Any, P: Optional[Dict[str, Any]] = None, aday: Optional[Tuple[np.ndarray, np.ndarray]] = None,
           E: Dict[str, Any] = OC_ESIK, tekrar: Optional[int] = None, tekrar_bas: int = 0) -> pd.DataFrame:
    """n olaylı hücrede δ (tek ya da liste) için güç: her tekrarda gerçek panelden n rastgele hisse-gün (yerine koymadan; P yoksa σ = %25
    sentetik), r60'a δ eklenir, oc_hucre kuralı. Döner: tekrar x δ satırları (tutar = beş şart, tutar4 = FI dört şart, şart bayrakları)."""
    G = E["guc"]; tekrar = G["tekrar"] if tekrar is None else tekrar
    deltalar = list(delta) if isinstance(delta, (list, tuple, np.ndarray)) else [float(delta)]
    if P is not None and aday is None:
        aday = oc_guc_aday(P, G["bas"], G["son"], E)
    out = []
    for t in range(tekrar_bas, tekrar_bas + tekrar):
        rng = np.random.default_rng([G["tohum"], n, t])
        if P is not None:
            dd, jj = aday
            if len(dd) < n:
                raise OCHata(f"güç: uygun hisse-gün {len(dd)} < n {n}")
            sec = rng.choice(len(dd), n, replace=False)
            X = oc_esli(P, pd.DataFrame({"d": dd[sec], "j": jj[sec], "giris": P["tarih"][dd[sec]]}), E)
            if X.fark.isna().any():
                raise OCHata("güç: seçilen hisse-günde eşli fark yok (aday süzgeci oc_esli ile uyuşmuyor)")
        else:
            X = _oc_sentetik_olay(n, rng, E)
        plas = None
        for dl in deltalar:
            h = oc_hucre(oc_delta_ekle(X, dl), E, _plasebo=plas)
            plas = h.get("_plasebo")
            out.append({"n": n, "tekrar": t, "delta": dl, "kaynak": "gercek" if P is not None else "sigma25", "ay": h.get("ay"),
                        "ort_fark": h.get("ort_fark"), "alt95": h.get("alt95"), "ust95": h.get("ust95"), "sira": h.get("sira"),
                        "portfoy": h.get("portfoy"), "p90": h.get("portfoy_esli_p90"), "s_fark": h.get("s_fark"), "s_sira": h.get("s_sira"),
                        "s_port": h.get("s_port"), "s_yari": h.get("s_yari"), "yari1": h.get("yari1_fark"), "yari2": h.get("yari2_fark"),
                        "tutar4": h.get("tutar4"), "tutar": h.get("tutar")})
    return pd.DataFrame(out)


def oc_guc_ozet(G: pd.DataFrame) -> pd.DataFrame:
    g = G.groupby(["kaynak", "n", "delta"])
    Z = g.agg(tekrar=("tutar", "size"), guc=("tutar", "mean"), guc4=("tutar4", "mean"), s_fark=("s_fark", "mean"), s_sira=("s_sira", "mean"),
              s_port=("s_port", "mean"), s_yari=("s_yari", "mean"), ort_fark=("ort_fark", "mean"), ay=("ay", "mean")).reset_index()
    Z["yari_genislik"] = g.apply(lambda x: float(((x.ust95 - x.alt95) / 2).mean())).to_numpy()
    return Z


_OC_HAVUZ: Dict[str, Any] = {}


def _oc_guc_isci(is_: Tuple[int, int, int, bool]) -> pd.DataFrame:
    n, t0, k, gercek = is_
    if gercek:
        return oc_guc(n, _OC_HAVUZ["E"]["guc"]["delta"], _OC_HAVUZ["P"], _OC_HAVUZ["aday"], _OC_HAVUZ["E"], tekrar=k, tekrar_bas=t0)
    return oc_guc(n, _OC_HAVUZ["E"]["guc"]["delta"], None, None, _OC_HAVUZ["E"], tekrar=k, tekrar_bas=t0)


def oc_guc_tablo(P: Optional[Dict[str, Any]] = None, E: Dict[str, Any] = OC_ESIK, cikti: Optional[str] = None, islem: int = 1,
                 sentetik: bool = True) -> Dict[str, Any]:
    """Güç tablosu (n x δ) gerçek panelle (P) ve σ = %25 sentetik varsayımla; guc_tablosu.json + guc_ham.csv + GUC_TABLOSU.md yazar."""
    cikti = cikti or OC_YOL["cikti"]; os.makedirs(cikti, exist_ok=True); G = E["guc"]; t0 = time.time()
    parcalar = []; meta_aday = 0; adim = 25
    _OC_HAVUZ.update({"P": P, "aday": None, "E": E})
    turler = ([True] if P is not None else []) + ([False] if sentetik or P is None else [])
    if P is not None:
        _OC_HAVUZ["aday"] = oc_guc_aday(P, G["bas"], G["son"], E)
        meta_aday = int(len(_OC_HAVUZ["aday"][0])); oclog.info("güç: uygun hisse-gün %d", meta_aday)
    isler = [(n, t, min(adim, G["tekrar"] - t), gr) for gr in turler for n in sorted(G["n"], reverse=True) for t in range(0, G["tekrar"], adim)]
    if islem > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(islem) as havuz:
            for k, Z in enumerate(havuz.imap_unordered(_oc_guc_isci, isler), 1):
                parcalar.append(Z); oclog.info("güç %d/%d (%.0f sn)", k, len(isler), time.time() - t0)
    else:
        for k, is_ in enumerate(isler, 1):
            parcalar.append(_oc_guc_isci(is_)); oclog.info("güç %d/%d (%.0f sn)", k, len(isler), time.time() - t0)
    Ham = pd.concat(parcalar, ignore_index=True).sort_values(["kaynak", "n", "tekrar", "delta"]).reset_index(drop=True)
    Ham.to_csv(os.path.join(cikti, OC_DOSYA["guc_ham"]), index=False)
    Z = oc_guc_ozet(Ham)
    kaynak = "gercek" if P is not None else "sigma25"
    tab: Dict[str, Dict[str, float]] = {}
    for r in Z[Z.kaynak == kaynak].itertuples():
        tab.setdefault(str(int(r.n)), {})[f"{r.delta:.2f}"] = round(float(r.guc), 4)
    k58 = G["k58_kontrol"]
    z4 = Z[(Z.kaynak == kaynak) & np.isclose(Z.delta, k58["delta"]) & (Z.n <= k58["n_max"])]
    k58_max = float(z4.guc4.max()) if len(z4) else np.nan
    J = {"surum": OC_SURUM, "cetvel_sha": oc_esik_sha(E), "kod_sha": oc_kod_sha(), "uretim_utc": _oc_simdi(), "kaynak": kaynak,
         "aday_hisse_gun": meta_aday, "tablo_guc5": tab,
         "ozet": json.loads(Z.to_json(orient="records", force_ascii=False)),
         "k58_kontrol": {"delta": k58["delta"], "n_max": k58["n_max"], "guc4_max": k58_max, "k58_ust": k58["k58_ust"],
                         "tutarli": bool(np.isfinite(k58_max) and k58_max <= k58["k58_ust"] + k58["pay"])},
         "sure_sn": round(time.time() - t0, 1)}
    with open(os.path.join(cikti, OC_DOSYA["guc_json"]), "w", encoding="utf-8") as f:
        json.dump(J, f, ensure_ascii=False, indent=1, sort_keys=True, default=float)
    md = oc_guc_md(Z, J, Ham, E)
    with open(os.path.join(cikti, OC_DOSYA["guc_md"]), "w", encoding="utf-8") as f:
        f.write(md)
    return {"ham": Ham, "ozet": Z, "json": J, "md": md}


def _yz(x: Any, n: int = 0) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"%{float(x) * 100:.{n}f}".replace(".", ",")
    except (TypeError, ValueError):
        return "-"


def _sy(x: Any, n: int = 2) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"{float(x):.{n}f}".replace(".", ",")
    except (TypeError, ValueError):
        return "-"


def oc_guc_md(Z: pd.DataFrame, J: Dict[str, Any], Ham: pd.DataFrame, E: Dict[str, Any] = OC_ESIK) -> str:
    G = E["guc"]; s = [f"# ORTAK CETVEL — GÜÇ TABLOSU ({OC_SURUM})", "",
                       f"Üretim {J['uretim_utc']}; cetvel sha `{J['cetvel_sha']}`; kod sha `{J['kod_sha']}`.",
                       f"Kaynak: {G['kaynak']}. Uygun hisse-gün: {J['aday_hisse_gun']}. Tekrar {G['tekrar']} (tohum {G['tohum']}).",
                       "GÜÇ = beş şartlı hücre kuralının (FI dört şart + iki alt dönem aynı yön) tuttuğu tekrar payı; 'güç4' = yalnız FI dört şart.", ""]
    for kaynak, baslik in (("gercek", "Gerçek eş farkı dağılımı (ABD 2023-26)"), ("sigma25", "Varsayım: normal, σ = %25 (veri yoksa yedek)")):
        z = Z[Z.kaynak == kaynak]
        if not len(z):
            continue
        s += [f"## {baslik}", "", "| n | " + " | ".join(f"δ {_yz(d, 0)} güç / güç4" for d in G["delta"]) + " | %95 yarı genişlik | ay |",
              "|---|" + "---|" * (len(G["delta"]) + 2)]
        for n in G["n"]:
            zz = z[z.n == n]
            if not len(zz):
                continue
            hucre = []
            for d in G["delta"]:
                r = zz[np.isclose(zz.delta, d)]
                hucre.append(f"{_yz(r.guc.iloc[0], 1)} / {_yz(r.guc4.iloc[0], 1)}" if len(r) else "-")
            s.append(f"| {n} | " + " | ".join(hucre) + f" | {_yz(zz.yari_genislik.iloc[0], 1)} | {_sy(zz.ay.iloc[0], 0)} |")
        s.append("")
        s += ["Şart başına geçme payı (δ = +%5):", "", "| n | fark+alt uç | sıra | portföy | iki yarı | güç |", "|---|---|---|---|---|---|"]
        for r in z[np.isclose(z.delta, 0.05)].itertuples():
            s.append(f"| {r.n} | {_yz(r.s_fark, 1)} | {_yz(r.s_sira, 1)} | {_yz(r.s_port, 1)} | {_yz(r.s_yari, 1)} | {_yz(r.guc, 1)} |")
        s.append("")
    k = J["k58_kontrol"]
    s += ["## K58 tutarlılık", "",
          f"Dört şartlı güç, δ +%{k['delta'] * 100:.0f}, n <= {k['n_max']}: en yüksek {_yz(k['guc4_max'], 1)} (K58: <= {_yz(k['k58_ust'], 0)}; "
          f"pay 5 puan) -> {'TUTARLI' if k['tutarli'] else 'TUTARSIZ'}. Not: K58 plasebo olayları 2016-26'ya yayıyordu (daha çok ay, daha dar "
          "aralık); burada 2023-26 (karar dönemleri), bu yüzden güç K58'den düşük ya da eşit beklenir.", ""]
    # yeniden üretim: ham csv'den iki satır bağımsız
    s += ["## Yeniden üretim (ham csv'den bağımsız; K11)", ""]
    for n, d in ((300, 0.05), (1000, 0.02)):
        h = Ham[(Ham.kaynak == J["kaynak"]) & (Ham.n == n) & np.isclose(Ham.delta, d)]
        if len(h):
            el = float(((h.ort_fark > 0) & (h.alt95 > 0) & (h.sira > 0.5) & (h.portfoy > h.p90) & (h.yari1 > 0) & (h.yari2 > 0)).mean())
            z = Z[(Z.kaynak == J["kaynak"]) & (Z.n == n) & np.isclose(Z.delta, d)]
            s.append(f"- n {n}, δ {_yz(d, 0)}: ham satırların ham istatistiklerinden (ort fark, alt uç, sıra, portföy, p90, yarılar) yeniden {_yz(el, 1)}; özet tablo {_yz(z.guc.iloc[0], 1)} "
                     f"-> {'AYNI' if len(z) and abs(el - float(z.guc.iloc[0])) < 1e-12 else 'FARKLI'}")
    s += ["", "## Okuma", "",
          "- Etiket kuralı (OC_ESIK etiket): hücre 'güç yeterli' = n >= 1.000 YA DA bu tablodaki güç(n, δ = +%5) >= %80 (n'den küçük ya da "
          "eşit en büyük satır). Değilse tutmayan hücre İZ DEĞİL değil ÖLÇÜLEMEDİ yazılır.",
          "- δ = 0 satırı yanlış pozitif payıdır (rastgele olayların hücreyi tutturma oranı).", ""]
    return "\n".join(s)


def oc_guc_bak(n: int, delta: Optional[float] = None, tablo: Optional[Dict[str, Any]] = None, E: Dict[str, Any] = OC_ESIK) -> float:
    """Güç tablosundan n'e küçük-eşit en büyük satırın δ_ref gücü (muhafazakâr). n < 30 ya da tablo yok -> 0."""
    delta = E["etiket"]["guc_delta_ref"] if delta is None else delta
    if tablo is None:
        yol = os.path.join(OC_YOL["cikti"], OC_DOSYA["guc_json"])
        if not os.path.exists(yol):
            return 0.0
        tablo = json.load(open(yol, encoding="utf-8"))["tablo_guc5"]
    ns = sorted(int(k) for k in tablo if int(k) <= n)
    if n < E["hucre_karar"]["n_esik"] or not ns:
        return 0.0
    return float(tablo[str(ns[-1])].get(f"{delta:.2f}", 0.0))


# ================================================================ 8) ETİKET
def oc_hucre_durum(h: Dict[str, Any], E: Dict[str, Any] = OC_ESIK, tablo: Optional[Dict[str, Any]] = None) -> Tuple[str, float]:
    n = int(h.get("n", 0) or 0)
    if n < E["hucre_karar"]["n_esik"]:
        return "ÖLÇÜLEMEDİ", 0.0
    g = oc_guc_bak(n, None, tablo, E)
    if h.get("tutar"):
        return "TUTAR", g
    if n >= E["etiket"]["n_yeter"] or g >= E["etiket"]["guc_esik"]:
        return "TUTMADI", g
    return "ÖLÇÜLEMEDİ", g


def oc_etiket(T: pd.DataFrame, E: Dict[str, Any] = OC_ESIK) -> Dict[str, Any]:
    """T: pazar, donem, durum (oc_hucre_durum), olasilik etiketi (olas). Genel etiket + olasılık etiketi (OC_ESIK etiket)."""
    kp, kd = E["karar_pazar"], E["karar_donem"]
    dur = {(r.pazar, r.donem): r.durum for r in T.itertuples()}
    karar = {(p, d): dur.get((p, d)) for p in kp for d in kd}
    var = {k: v for k, v in karar.items() if v is not None}
    tut = [k for k, v in var.items() if v == "TUTAR"]
    pz_var = {p for (p, _d) in var}
    if len(tut) == len(karar):
        bist = all(dur.get(("BIST", d)) == "TUTAR" for d in kd)
        genel = "İZ + BIST" if bist else "İZ"
    elif tut:
        eksik = [p for p in kp if p not in pz_var]
        tam = [p for p in kp if all(karar.get((p, d)) == "TUTAR" for d in kd)]
        if eksik and tam and set(tam) == pz_var:
            genel = f"EMARE ({'-'.join(tam)}-ADAY; {', '.join(eksik)} verisi yok)"
        else:
            genel = "EMARE (" + ", ".join(f"{p} {d}" for p, d in tut) + ")"
    elif var and all(v == "TUTMADI" for v in var.values()):
        genel = "İZ DEĞİL" + ("" if len(var) == len(karar) else " (" + ", ".join(p for p in kp if p not in pz_var) + " verisi yok)")
    elif not var:
        genel = "VERİ YOK"
    else:
        genel = "ÖLÇÜLEMEDİ"
    ol = {(r.pazar, r.donem): getattr(r, "olas", None) for r in T.itertuples()}
    ok_ = [ol.get(k) for k in karar]
    if all(x == "SEÇİCİ" for x in ok_):
        og = "SEÇİCİ"
    elif all(x == "PİYANGO" for x in ok_):
        og = "PİYANGO"
    elif any(x in (None, "ÖLÇÜLEMEDİ") for x in ok_):
        og = "ÖLÇÜLEMEDİ"
    else:
        og = "YOK"
    return {"genel": genel, "olasilik": og, "karar_hucre": {f"{p} {d}": v for (p, d), v in karar.items()}}


# ================================================================ 9) ANA ARAYÜZ
_OC_PANEL_ONBELLEK: Dict[Any, Dict[str, Any]] = {}


def _oc_panel_al(pazar: str, V: Dict[str, Any], E: Dict[str, Any]) -> Dict[str, Any]:
    v = V[pazar]
    if isinstance(v, dict) and "H" in v and "okR" in v:
        return v
    anahtar = (id(v), oc_esik_sha(E))
    if anahtar not in _OC_PANEL_ONBELLEK:
        _OC_PANEL_ONBELLEK.clear()   # bellek: aynı anda tek panel
        _OC_PANEL_ONBELLEK[anahtar] = oc_panel(_oc_veri_sar(v, pazar), E)
    return _OC_PANEL_ONBELLEK[anahtar]


def oc_olc(olaylar: pd.DataFrame, V: Dict[str, Any], E: Dict[str, Any] = OC_ESIK, tablo: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """olaylar: DataFrame[sembol, tarih, pazar]; V: pazar -> oc_veri(...) çıktısı (ya da oc_panel). Döner: {'hucre': hücre tablosu,
    'olay': olay satırları, 'portfoy': hücre başına portföy / plasebo, 'olasilik': olasılık tablosu, 'etiket': genel + olasılık,
    'sayim': düşme sayımı, 'cetvel_sha', 'kod_sha'}."""
    eks = {"sembol", "tarih", "pazar"} - set(olaylar.columns)
    if eks:
        raise OCHata(f"olaylar sütunu eksik: {eks}")
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    H_, Ol_, Ob_, say_ = [], [], [], {}
    for pz in [p for p in E["pazar"] if p in set(olaylar.pazar)] + sorted(set(olaylar.pazar) - set(E["pazar"])):
        if pz not in E["pazar"]:
            raise OCHata(f"bilinmeyen pazar: {pz}")
        if pz not in V:
            say_[pz] = {"veri_yok": int((olaylar.pazar == pz).sum())}; continue
        P = _oc_panel_al(pz, V, E)
        X, say = oc_olay_hazirla(olaylar[olaylar.pazar == pz], P, E)
        X = oc_esli(P, X, E)
        say["r60_olculemedi"] = int(X.r60.isna().sum()) if len(X) else 0
        say["es_az"] = int((X.r60.notna() & X.fark.isna()).sum()) if len(X) else 0
        X = oc_olasilik_olay(P, X, E)
        X.insert(0, "pazar", pz); say_[pz] = say
        for ad, _a, _b in E["donem"]:
            x = X[X.donem == ad]
            h = oc_hucre(x, E)
            durum, g = oc_hucre_durum(h, E, tablo)
            ol = oc_olasilik_hucre(x, E)
            H_.append({"pazar": pz, "donem": ad, "karar_hucre": pz in E["karar_pazar"] and ad in E["karar_donem"],
                       **{k: v for k, v in h.items() if not k.startswith("_")}, "guc": g, "durum": durum, "olas": ol["etiket"]})
            Ob_.append({"pazar": pz, "donem": ad, **ol})
        Ol_.append(X)
    T = pd.DataFrame(H_)
    Ol = pd.concat(Ol_, ignore_index=True) if Ol_ else pd.DataFrame()
    Ob = pd.DataFrame(Ob_)
    et = oc_etiket(T, E) if len(T) else {"genel": "VERİ YOK", "olasilik": "ÖLÇÜLEMEDİ", "karar_hucre": {}}
    port = T[["pazar", "donem", "n", "portfoy", "portfoy_esli_p10", "portfoy_esli_p50", "portfoy_esli_p90"]].copy() if len(T) and "portfoy" in T else pd.DataFrame()
    return {"hucre": T, "olay": Ol.drop(columns=["_esler"], errors="ignore"), "_olay_esler": Ol, "portfoy": port, "olasilik": Ob,
            "etiket": et, "sayim": say_, "cetvel_sha": oc_esik_sha(E), "kod_sha": oc_kod_sha() if os.path.exists(OC_YOL["kod"]) else "",
            "surum": OC_SURUM, "zaman_utc": _oc_simdi()}


def oc_rapor(S: Dict[str, Any], baslik: str = "Ölçüm") -> str:
    """Her aşama için AYNI biçim: sayım, hücre tablosu (FI dört şart + iki yarı + durum), olasılık tablosu, etiketler, sınırlar."""
    s = [f"## {baslik} — ORTAK CETVEL sonucu", "", f"Cetvel: {S.get('surum')}; CETVEL_SHA `{S.get('cetvel_sha')}`; CETVEL_KOD_SHA `{S.get('kod_sha')}`.", "",
         f"**GENEL ETİKET: {S['etiket']['genel']}** · **OLASILIK ETİKETİ: {S['etiket']['olasilik']}**", "",
         "### Olay sayımı (düşmeler)", "", "| Pazar | girdi | sembol yok | sinyal barı geçersiz | giriş yok | giriş geç | havuz dışı (likidite alt %20 / geçmiş bölünme / geçmiş eksik / evren öncesi / havuz < 30) | tekil | r60 ölçülemedi | eş < 3 |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for p, c in S["sayim"].items():
        hd = f"{c.get('havuz_disi', '-')} ({c.get('likidite_alt20', '-')} / {c.get('bolunme_gecmis', '-')} / {c.get('gecmis_eksik', '-')} / " \
             f"{c.get('evren_once', '-')} / {c.get('havuz_az', '-')})"
        s.append(f"| {p} | " + " | ".join(str(c.get(k, "-")) for k in ("girdi", "sembol_yok", "sinyal_bar_gecersiz", "giris_yok", "giris_gec"))
                 + f" | {hd} | " + " | ".join(str(c.get(k, "-")) for k in ("tekil", "r60_olculemedi", "es_az")) + " |")
    s += ["", "### Hücre tablosu (r60 eşli fark; FI dört şart + iki alt dönem)", "",
          "| Pazar | Dönem | karar | n | ort fark [%95] | medyan | sıra | portföy / plasebo p90 | yarı1 / yarı2 | güç (δ+%5) | durum |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    T = S["hucre"]
    for r in T.itertuples():
        n = int(r.n) if r.n == r.n else 0
        if n == 0:
            s.append(f"| {r.pazar} | {r.donem} | {'K' if r.karar_hucre else 'b'} | 0 | - | - | - | - | - | - | {r.durum} |"); continue
        s.append(f"| {r.pazar} | {r.donem} | {'K' if r.karar_hucre else 'b'} | {n} | {_yz(r.ort_fark, 1)} [{_yz(r.alt95, 1)}, {_yz(r.ust95, 1)}] | "
                 f"{_yz(r.medyan_fark, 1)} | {_sy(r.sira)} | {_yz(r.portfoy, 0)} / {_yz(r.portfoy_esli_p90, 0)} | {_yz(r.yari1_fark, 1)} / "
                 f"{_yz(r.yari2_fark, 1)} | {_yz(r.guc, 0)} | {r.durum} |")
    s += ["", "### Olasılık tablosu (250 gün dokunma; eş katı karar, taban katı bilgi)", "",
          "| Pazar | Dönem | n250 | P(+%100) olay / eş / taban | kat eş [%95] | kat taban | P(-%50) olay / eş / taban | kat eş [%95] | kat taban | "
          "60g önce +%20 kat eş | 20g P(+%20 önce) / P(-%10 önce) olay (eş) | etiket |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in S["olasilik"].to_dict("records"):
        s.append(f"| {r['pazar']} | {r['donem']} | {r.get('n250', 0)} | {_yz(r.get('up100_es_p_olay'), 1)} / {_yz(r.get('up100_es_p_ref'), 1)} / "
                 f"{_yz(r.get('up100_tb_p_ref'), 1)} | {_sy(r.get('up100_es_kat'))} [{_sy(r.get('up100_es_alt'))}, {_sy(r.get('up100_es_ust'))}] | "
                 f"{_sy(r.get('up100_tb_kat'))} | {_yz(r.get('dn50_es_p_olay'), 1)} / {_yz(r.get('dn50_es_p_ref'), 1)} / {_yz(r.get('dn50_tb_p_ref'), 1)} | "
                 f"{_sy(r.get('dn50_es_kat'))} [{_sy(r.get('dn50_es_alt'))}, {_sy(r.get('dn50_es_ust'))}] | {_sy(r.get('dn50_tb_kat'))} | "
                 f"{_sy(r.get('once20_es_kat'))} [{_sy(r.get('once20_es_alt'))}, {_sy(r.get('once20_es_ust'))}] | "
                 f"{_yz(r.get('u20_es_p_olay'), 1)} / {_yz(r.get('d20_es_p_olay'), 1)} ({_yz(r.get('u20_es_p_ref'), 1)} / {_yz(r.get('d20_es_p_ref'), 1)}) | {r.get('etiket')} |")
    s += ["", "### Karar hücreleri", ""] + [f"- {k}: {v}" for k, v in S["etiket"]["karar_hucre"].items()]
    s += ["", "### Sınırlar (her raporda aynı)", "",
          "- Hayatta kalma: evren bugün işlem gören hisseler (+ ABD k34 nakdi biten, yine bugün işlem gören); batanlar yok. Getiriler yukarı, "
          "-%50 olasılığı aşağı yanlı okunmalı.",
          "- Komisyon / kayma yok; slot portföyü 10 yuva, 60 gün tut, sırayla.",
          "- 31.08.2026 (fon krizi) sonrası fiyat yok; 250 gün dokunma ölçüsü en geç ~Ağustos 2025 girişlerini kapsar.",
          "- Etiket kuralı OC_ESIK 'etiket' (İZ DEĞİL yalnız güç yeterliyken). Keşif 2016-22 ve BIST bilgi."]
    return "\n".join(s)


# ================================================================ 10) KAPI ve ÖN KAYIT
_OC_KAPI_DESEN = {"cetvel": r"CETVEL_SHA:\s*`?([0-9a-f]{64})`?", "kod": r"CETVEL_KOD_SHA:\s*`?([0-9a-f]{64})`?",
                  "guc": r"GUC_SHA:\s*`?([0-9a-f]{64})`?"}


def oc_kapi(onkayit_yolu: str, git: bool = True, kontrol: bool = True, kod_yol: Optional[str] = None, guc_yol: Optional[str] = None,
            E: Dict[str, Any] = OC_ESIK, kod_git: bool = True) -> Dict[str, Any]:
    """Aşama koşu kapısı: (1) IZ_KARNE.ik_kontrol_kapisi (KONTROL LİSTESİ dolu); (2) ön kayıttaki CETVEL_SHA == oc_esik_sha(),
    CETVEL_KOD_SHA == bu dosyanın sha'sı, GUC_SHA == guc_tablosu.json sha'sı; (3) ön kayıt git'e işlenmiş ve değişmemiş (kod_git: bu dosya
    ve güç tablosu da). Biri tutmazsa OCHata; ölçüm başlamaz."""
    if not os.path.exists(onkayit_yolu):
        raise OCHata(f"ön kayıt yok: {onkayit_yolu}")
    out: Dict[str, Any] = {"yol": onkayit_yolu}
    if kontrol:
        import IZ_KARNE as IK
        try:
            out["kontrol"] = IK.ik_kontrol_kapisi(onkayit_yolu)["gecti"]
        except RuntimeError as ex:
            raise OCHata(str(ex))
    metin = open(onkayit_yolu, encoding="utf-8").read(); bulunan = {}
    for ad, desen in _OC_KAPI_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise OCHata(f"ön kayıtta '{ad.upper()}' satırı yok ({onkayit_yolu}); CETVEL_SHA / CETVEL_KOD_SHA / GUC_SHA zorunlu")
        bulunan[ad] = m.group(1)
    kod_yol = kod_yol or OC_YOL["kod"]; guc_yol = guc_yol or os.path.join(OC_YOL["cikti"], OC_DOSYA["guc_json"])
    simdi = {"cetvel": oc_esik_sha(E), "kod": oc_kod_sha(kod_yol), "guc": oc_guc_sha(guc_yol)}
    for ad in ("cetvel", "kod", "guc"):
        if bulunan[ad] != simdi[ad]:
            raise OCHata(f"{ad.upper()} sha tutmuyor: ön kayıt {bulunan[ad][:12]}…, şimdi {simdi[ad][:12]}… -> cetvel değişmiş; koşu DURDU "
                         "(değişiklik yeni cetvel sürümü ister ve bütün aşamalar yeniden koşulur)")
    out.update(bulunan)
    if git:
        out["git"] = _oc_git_islenmis(onkayit_yolu)
        if kod_git:
            out["git_kod"] = _oc_git_islenmis(kod_yol); out["git_guc"] = _oc_git_islenmis(guc_yol)
    oclog.info("oc_kapi AÇIK: %s (cetvel %s…)", onkayit_yolu, simdi["cetvel"][:12])
    return out


def oc_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = OC_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def oc_kapi_satirlari(guc_yol: Optional[str] = None) -> str:
    """Aşama ön kayıtlarına AYNEN kopyalanacak üç satır."""
    return "\n".join([f"CETVEL_SHA: `{oc_esik_sha()}`", f"CETVEL_KOD_SHA: `{oc_kod_sha()}`", f"GUC_SHA: `{oc_guc_sha(guc_yol)}`"])


def oc_onkayit_metni(cikti: Optional[str] = None) -> str:
    cikti = cikti or OC_YOL["cikti"]
    J = json.load(open(os.path.join(cikti, OC_DOSYA["guc_json"]), encoding="utf-8"))
    if J["cetvel_sha"] != oc_esik_sha() or J["kod_sha"] != oc_kod_sha():
        raise OCHata("güç tablosu bu cetvel / kodla üretilmemiş: önce `python ORTAK_CETVEL.py guc`")
    tab = J["tablo_guc5"]; G = OC_ESIK["guc"]
    s = [f"# ORTAK CETVEL — ÖN KAYIT ({OC_SURUM})", "",
         f"Yazım: {_oc_simdi()}. Bu dosya ölçümden ÖNCE yazıldı; hiçbir sinyal bu cetvelle henüz ölçülmedi (yalnız sentetik test + güç simülasyonu).", "",
         "**Bu cetvel dört aşamada değiştirilmez; değişirse yeni cetvel sürümü ve bütün aşamalar yeniden koşulur.**", "",
         "Dört aşama (Cemal, 14 Kas 2026): (1) K24 iki evre çöl; (2) D9 uzun çöl + rüzgâr; (3) düzgün dip vs çöl ayrımı; (4) INTEM ileri test. "
         "Her aşama `import ORTAK_CETVEL as OC` ile bu modülü içe alır, kendi ön kaydına aşağıdaki üç satırı AYNEN koyar ve koşmadan önce "
         "`OC.oc_kapi(<aşama ön kaydı>)` çağırır; sha'lardan biri tutmazsa ya da ön kayıt git'e işlenmemişse koşu durur.", "",
         "## Mühür satırları (aşama ön kayıtlarına aynen kopyalanır)", "", oc_kapi_satirlari(), "",
         f"- CETVEL_SHA = sha256(OC_ESIK kanonik JSON, sort_keys); CETVEL_KOD_SHA = sha256(ORTAK_CETVEL.py bayt); GUC_SHA = sha256({OC_DOSYA['guc_json']}).", "",
         "## Güç özeti (gerçek ABD 2023-26 eş farkı dağılımı; beş şartlı hücre kuralı)", "",
         "| n | " + " | ".join(f"δ {_yz(d, 0)}" for d in G["delta"]) + " |", "|---|" + "---|" * len(G["delta"])]
    for n in G["n"]:
        r = tab.get(str(n), {})
        s.append(f"| {n} | " + " | ".join(_yz(r.get(f"{d:.2f}"), 1) for d in G["delta"]) + " |")
    k = J["k58_kontrol"]
    s += ["", f"K58 tutarlılık: dört şartlı güç δ +%2, n <= 300 en yüksek {_yz(k['guc4_max'], 1)} (K58 <= %11) -> {'TUTARLI' if k['tutarli'] else 'TUTARSIZ'}. "
          f"Ayrıntı {OC_DOSYA['guc_md']}.", "",
          "## OC_ESIK (tam metin; mühürlü)", "", "```json", json.dumps(OC_ESIK, ensure_ascii=False, indent=1, sort_keys=True), "```", "",
          oc_kontrol_tablosu(), "",
          "## Test", "", "`python test_ortak_cetvel.py` (sentetik; tekilleştirme, ertesi açılış, FON_IZI ile hücre etiketleri birebir, bootstrap "
          "determinizmi, plasebo, olasılık tablosu, etiket kuralları, kapı, geleceğe bakma kesme testi, e-posta / anahtar taraması).", ""]
    return "\n".join(s)


def oc_onkayit_yaz(cikti: Optional[str] = None, uzerine: bool = False) -> str:
    cikti = cikti or OC_YOL["cikti"]; os.makedirs(cikti, exist_ok=True)
    yol = os.path.join(cikti, OC_DOSYA["onkayit"])
    if os.path.exists(yol) and not uzerine:
        try:
            _oc_git_islenmis(yol)
            raise OCHata(f"ön kayıt zaten git'e işlenmiş ({yol}); üzerine yazılmaz (yeni cetvel sürümü gerekir)")
        except OCHata as ex:
            if "zaten" in str(ex):
                raise
            raise OCHata(f"ön kayıt var ({yol}); git'e işlenmemişse --uzerine-yaz ile yeniden yaz")
    metin = oc_onkayit_metni(cikti)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _cakisma_kontrol_oc(_once=_CK_ONCE_OC, _dosya="ORTAK_CETVEL.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_OC", "_CK_KAYIT", "_cakisma_kontrol_oc", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "subprocess", "warnings", "copy", "_dt",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_oc()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=OC_SURUM)
    ap.add_argument("komut", choices=["guc", "onkayit", "kapi", "sha"])
    ap.add_argument("yol", nargs="?", default=None)
    ap.add_argument("--islem", type=int, default=1)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "guc":
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            P_ = oc_panel(oc_veri("ABD"))
            R_ = oc_guc_tablo(P_, cikti=a.cikti, islem=a.islem)
            print(R_["md"])
        elif a.komut == "onkayit":
            print(oc_onkayit_yaz(a.cikti, uzerine=a.uzerine_yaz))
        elif a.komut == "kapi":
            print(json.dumps(oc_kapi(a.yol or os.path.join(OC_YOL["cikti"], OC_DOSYA["onkayit"])), ensure_ascii=False, indent=1))
        else:
            print(json.dumps({"cetvel_sha": oc_esik_sha(), "kod_sha": oc_kod_sha(),
                              "guc_sha": oc_guc_sha() if os.path.exists(os.path.join(OC_YOL["cikti"], OC_DOSYA["guc_json"])) else None}, indent=1))
    except OCHata as ex:
        oclog.error("%s", ex); sys.exit(1)
