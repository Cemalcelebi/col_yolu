"""KISA_UFUK — mevcut, mühürlü beş olay kümesinin sonrası 3 ve 5 MUMLUK ufukta (27 Kasım 2026). YENİ olay aranmaz; olaylar yeniden taranmaz /
süzülmez; yalnız sonuç ufku değişir.

İş tanımı: arastirma_cikti/kisa_ufuk/KU_IS_TANIMI.md (ana model). Kümeler:
  K1 WEB DESENLERİ   /root/.kasa/ham/web_desen/olay_{ABD,AVR}.pkl            17 kol, yönlü (WEB_DESEN.WD_KOL)
  K2 DOJİ ÖBEĞİ      /root/.kasa/ham/doji_obek/olay_ANA_{ABD,AVR}.pkl         k = 2, 3, 4+ (yönsüz)
  K3 UÇLAR           /root/.kasa/ham/mum_izi27/olay27.pkl                    E2 günlük, 12 ölçü + 4 bileşiğin UÇ10'u (yönsüz; beklenen yön yukarı)
  K4 KODUN BÖLGELERİ arastirma_cikti/mum_izi/mum_izi24_olay.csv.gz            günlük ANA, KAPILI / KAPISIZ (yönsüz)
  K5 ESKİ ÇÖL PUANI  /root/.kasa/ham/col_skor6/pencere_{ABD,AVR}.pkl          PUAN_ESIT üst %10 (L 20, 40), F5 üst %2 (L 40) (yönsüz)
Bar deposu: YUKSELIS_ONCESI ham_{ABD,AVR}.npz (COL_SKOR6 depo_*.npz ile bayt değil içerik olarak birebir; K3 / K4 olayları sembol + giriş tarihiyle
eşlenir). Ölçüler (H = 3, 5; bilgi: ilk mum H = 1 ve H = 15): R_H, TOPLAM FARK_H (aynı hissenin aynı dönemdeki BÜTÜN uygun günleri), SEÇİM_H,
ÖNCE HANGİSİ (5 bar, +-1 ATR), İLK MUM. Ay kümeli bootstrap (10.000; tohum 2714), BH q 0,10 (41 kol x 2 ufuk). Hüküm önceden (KU_ESIK['hukum']).
Veri <= 2022-12-31 (assert + KASA kapısı). KASA AÇILMAZ. Mevcut modüller DEĞİŞTİRİLMEZ; içe alınır.

Komut:  python KISA_UFUK.py dogrula   H = 15 sağlaması (kaynak kümelerin kendi T1 tanımıyla; kısa ufuk HESAPLANMAZ) -> ham/ku_dogrulama.json
        python KISA_UFUK.py sayim     GETİRİSİZ SAYIM (küme x kol x hücre; kaynak sha) -> ham/ku_sayim.json
        python KISA_UFUK.py onkayit   KU_ON_KAYIT.md (mühürler + sayım + sağlama + yorum noktaları + kontrol tablosu)
        python KISA_UFUK.py olcum     kapı (kontrol + sha + ön kayıt commit + push + temiz ağaç + KASA) -> ölçüm (BİR KEZ) -> ku_sonuc.json + ku_ozet.csv
        python KISA_UFUK.py rapor     KU_RAPOR.md (sonuç json'undan; yeniden üretim / HATA / SAPMA ham/ku_rapor_ek.json'dan)
        python KISA_UFUK.py sha       kod / eşik sha
Colab:  exec(open('KISA_UFUK.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_KU = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import time  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_KU = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_KU not in sys.path:
    sys.path.insert(0, KOK_KU)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ; yazma + sızıntı taraması, sha, git)
import MUM_IZI_HAVUZ as HV  # noqa: E402  (DEĞİŞTİRİLMEZ; hücre adı, BH, ay özeti, hv25 dizileri)
import YUKSELIS_ONCESI as YO  # noqa: E402  (DEĞİŞTİRİLMEZ; bar deposu, örnek maskesi, P15, bootstrap yüzdeliği)
import WEB_DESEN as WD  # noqa: E402  (DEĞİŞTİRİLMEZ; kol yönleri, ATR dizisi)
import COL_SKOR6 as CS  # noqa: E402  (DEĞİŞTİRİLMEZ; ölçüm popülasyonu, dönemler)
import MUM_IZI_UC as UC  # noqa: E402  (DEĞİŞTİRİLMEZ; 16 satır adı)

kulog = logging.getLogger("col.kisa_ufuk")
if not kulog.handlers:
    _ku_h = logging.StreamHandler(sys.stderr)
    _ku_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s kisa_ufuk: %(message)s", "%H:%M:%S"))
    kulog.addHandler(_ku_h)
    kulog.setLevel(logging.INFO)
    kulog.propagate = False


class KUHata(RuntimeError):
    """Durdurucu hata: kapı / şema / eşleme / kesik / sıra / sağlama uyuşmazlığı."""


KU_SURUM = "KISA_UFUK v1.0 (2026-11-27): mevcut beş olay kümesi 3 ve 5 mumluk ufukta"
KU_YOL = {"cikti": os.path.join(KOK_KU, "arastirma_cikti", "kisa_ufuk"), "kod": os.path.join(KOK_KU, "KISA_UFUK.py"),
          "ham": os.environ.get("KU_HAM", "/root/.kasa/ham/kisa_ufuk"), "yo_ham": YO.YO_YOL["ham"], "acik": YO.YO_YOL["acik"],
          "is_tanimi": os.path.join(KOK_KU, "arastirma_cikti", "kisa_ufuk", "KU_IS_TANIMI.md")}
KU_DOSYA = {"onkayit": "KU_ON_KAYIT.md", "sonuc": "ku_sonuc.json", "ozet": "ku_ozet.csv", "rapor": "KU_RAPOR.md"}
KU_KESIK = pd.Timestamp("2022-12-31")
KU_PAZAR = ("ABD", "AVR")
KU_HUCRE = ("ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022")
KU_ABD = ("ABD|d1619", "ABD|d2022")
KU_AVR = ("AVR|d1619", "AVR|d2022")
KU_UFUK = (3, 5)                 # karar ufukları
KU_HEPSI_UFUK = (1, 3, 5, 15)    # 1 = ilk mum (bilgi), 15 = karşılaştırma (bilgi)
KU_DONEM = {"d1619": ("2016-01-01", "2019-12-31"), "d2022": ("2020-01-01", "2022-12-31")}

# kaynak dosyalar (yalnız okunur; sha ön kayıtta)
KU_KAYNAK: Dict[str, str] = {
    "K1_olay_ABD": "/root/.kasa/ham/web_desen/olay_ABD.pkl", "K1_olay_AVR": "/root/.kasa/ham/web_desen/olay_AVR.pkl",
    "K2_olay_ABD": "/root/.kasa/ham/doji_obek/olay_ANA_ABD.pkl", "K2_olay_AVR": "/root/.kasa/ham/doji_obek/olay_ANA_AVR.pkl",
    "K2_taban_ABD": "/root/.kasa/ham/doji_obek/taban_ABD.pkl", "K2_taban_AVR": "/root/.kasa/ham/doji_obek/taban_AVR.pkl",
    "K3_olay": "/root/.kasa/ham/mum_izi27/olay27.pkl",
    "K4_olay": os.path.join(KOK_KU, "arastirma_cikti", "mum_izi", "mum_izi24_olay.csv.gz"),
    "K5_pencere_ABD": "/root/.kasa/ham/col_skor6/pencere_ABD.pkl", "K5_pencere_AVR": "/root/.kasa/ham/col_skor6/pencere_AVR.pkl",
    "K5_kesim": os.path.join(KOK_KU, "arastirma_cikti", "col_skor6", "cs_kesim.json"),
    "DEPO_ABD": os.path.join(YO.YO_YOL["ham"], "ham_ABD.npz"), "DEPO_AVR": os.path.join(YO.YO_YOL["ham"], "ham_AVR.npz"),
    "YO_ozellik_ABD": os.path.join(YO.YO_YOL["ham"], "ozellik_ABD.pkl"), "YO_ozellik_AVR": os.path.join(YO.YO_YOL["ham"], "ozellik_AVR.pkl"),
    "S1_wd_sonuc": os.path.join(KOK_KU, "arastirma_cikti", "web_desen", "wd_sonuc.json"),
    "S2_dj_sonuc": os.path.join(KOK_KU, "arastirma_cikti", "doji_obek", "dj_sonuc.json"),
    "S3_mum27_sonuc": os.path.join(KOK_KU, "arastirma_cikti", "mum_izi", "mum_izi27_sonuc.json"),
    "S4_mum24_sonuc": os.path.join(KOK_KU, "arastirma_cikti", "mum_izi", "mum_izi24_sonuc.json"),
    "S5_cs_sonuc": os.path.join(KOK_KU, "arastirma_cikti", "col_skor6", "cs_sonuc.json"),
}

# kollar (sıra sabit; BH ailesi = bu 41 kol x 2 ufuk)
KU_K5_KOL = [("PUAN_ESIT_UC10_L20", "PUAN_ESIT", "uc10", 20), ("PUAN_ESIT_UC10_L40", "PUAN_ESIT", "uc10", 40), ("F5_UC2_L40", "F5", "uc2", 40)]


def _ku_kollar() -> List[Dict[str, Any]]:
    L: List[Dict[str, Any]] = []
    for k in WD.WD_KOLLAR:
        L.append({"kume": "K1", "kol": k, "id": f"K1|{k}", "yon": int(WD.WD_KOL[k]["yon"]), "yonlu": True, "ad": WD.WD_KOL[k]["ad"]})
    for k, ad in ((2, "k=2"), (3, "k=3"), (4, "k=4+")):
        L.append({"kume": "K2", "kol": str(k), "id": f"K2|{k}", "yon": 1, "yonlu": False, "ad": f"doji öbeği {ad}"})
    for s in UC.UC_SATIR:
        L.append({"kume": "K3", "kol": s, "id": f"K3|{s}", "yon": 1, "yonlu": False, "ad": f"{s} UÇ10 (E2 günlük)"})
    for g in ("KAPILI", "KAPISIZ"):
        L.append({"kume": "K4", "kol": g, "id": f"K4|{g}", "yon": 1, "yonlu": False, "ad": f"kodun seçtiği bölgeler {g} (günlük ANA)"})
    for ad, kol, uc, Lp in KU_K5_KOL:
        L.append({"kume": "K5", "kol": ad, "id": f"K5|{ad}", "yon": 1, "yonlu": False, "ad": f"{kol} {'üst %10' if uc == 'uc10' else 'üst %2'} L={Lp}"})
    return L


KU_KOLLAR = _ku_kollar()
KU_KOL_ID = [k["id"] for k in KU_KOLLAR]

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
KU_ESIK: Dict[str, Any] = {
    "surum": "KU-1.0",
    "tohum": 2714,
    "tohum_tanim": "np.random.default_rng([2714, crc32('kol_id|hücre')]); kol x hücre başına bir ağırlık matrisi W (bütün ölçü ve ufuklar aynı W ile); "
                   "sıra bağımsız, tekrarlanabilir",
    "ufuk": {"karar": [3, 5], "bilgi": [1, 15],
             "R_H": "R_H = C[e + H - 1] / giriş - 1 (e = giriş barı; giriş barı dahil H'inci geçerli bar kapanışı); yönlü kümede yön x R_H; e + H - 1 "
                    "hissenin verisinde yoksa ya da tarihi > 2022-12-31 ise ölçülmez (sayılır)",
             "giris": "her kümede kendi tanımındaki giriş: K1 olay dosyasının 'giris' sütunu (W3 / W4 bar içi seviye, ötekiler sinyalden sonraki açılış); "
                      "K2 O[t + 1]; K3 E0; K4 E0; K5 O[t + 1] (t = pencere sonu)"},
    "taban": {"en_az": 30,
              "tanim": "BÜTÜN UYGUN GÜNLER: hissenin kendi geçerli barı k (adım 1) <=> YO.yo_ornek_maske kuralları adım 5 yerine 1 ile (k + 15 hissenin "
                       "verisinde; POS(k + 1) - POS(k) <= 10; POS(k + 15) - POS(k + 1) <= 29; giriş satırında P2; giriş tarihi 2016-01-01 .. 2022-12-31; "
                       "15. bar <= 2022-12-31); hücre giriş tarihine göre; giriş O[k + 1]; T1_H = (hisse, hücre) başına C[k + H] / O[k + 1] - 1 "
                       "ortalaması; aynı hissenin aynı hücrede < 30 uygun günü varsa olay T1_YOK (düşer, sayılır); yönlü kümede TOPLAM FARK = yön x (R_H - T1_H)"},
    "secim": "SEÇİM_H = yön x (R_H - P_H(d)); P_H(d) = YO.yo_P15 tanımı ufuk H satırla: d satırında P2 ve açılışı sonlu > 0 hisselerin [d, d + H - 1] "
             "satırlarındaki son geçerli kapanış / açılış(d) - 1 eşit ağırlıklı ortalaması (< 5 hisse ise yok); d = giriş barının satırı (bilgi)",
    "once": {"H": 5, "atr": 1.0,
             "tanim": "barlar e .. e + 4 (giriş barı dahil): yukarı = High >= giriş + 1 ATR, aşağı = Low <= giriş - 1 ATR; ATR = WD.wd_atr_dizi (TR'nin 20 "
                      "bar ortalaması, kendi barları) e - 1 barında; hangisi önce; AYNI BARDA İKİSİ = desen yönünün TERSİ önce (kötümser; yönsüzde "
                      "yön = yukarı, aynı bar = aşağı önce); ONCE = 1(yönde önce) - 1(ters yönde önce) ∈ {-1, 0, 1}; taban = aynı hissenin aynı hücredeki "
                      "bütün uygun günlerinde (giriş O[k + 1], barlar k + 1 .. k + 5, ATR(k)) aynı yön ve aynı bağ kuralıyla ONCE ortalaması; "
                      "ASİMETRİ = ONCE - taban(hisse, hücre, yön); ATR'si olmayan olay / gün bu ölçüye girmez"},
    "ilk_mum": "ILK = yön x (R_1 - T1_1); R_1 = C[e] / giriş - 1 (giriş barının kendi getirisi: açılış girişlerde açılıştan kapanışa, bar içi girişte "
               "seviyeden kapanışa); T1_1 = aynı hissenin aynı hücredeki uygun günlerinde C[k + 1] / O[k + 1] - 1 ortalaması (bilgi)",
    "boot": {"B": 10000, "kume": "giriş ayı (YYYY-AA)",
             "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık); ortalama = ağırlıklı toplam / ağırlıklı sayı; %95 = 2,5 / 97,5 "
                      "yüzdelik (YO._q); T1 / taban sabit",
             "p": "tek yönlü p = (1 + #(boot ort <= 0)) / (B + 1)"},
    "bh": {"q": 0.10, "aile": "41 kol x 2 ufuk (H = 3, 5) = 82 satır; satır p'si = ABD 2016-19 ve ABD 2020-22 TOPLAM FARK_H tek yönlü p'lerinin büyüğü "
                              "(kesişim-birleşim); HV._hv_bh"},
    "maliyet": {"cizgi": 0.002, "tanim": "gidiş-dönüş %0,20 (bilgi; önceden): iki ABD döneminin TOPLAM FARK_H nokta ortalaması > %0,20 -> 'çizgi üstü'; "
                                         "TUTAR satırında 'İŞLENEBİLİR', değilse 'işlenemez'; TERS / EKSİ satırında |ortalama| > %0,20 'ters yönde çizgi üstü' "
                                         "(bilgi) diye yazılır"},
    "hukum": {"n_min": 300, "ay_min": 12, "avr_n": 100,
              "sira": "ÖLÇÜLEMEDİ (ABD hücrelerinden birinde n < 300 ya da farklı ay < 12) > TUTAR > TERS (yönsüzde EKSİ) > TEK DÖNEM > TUTMADI",
              "TUTAR": "ABD 2016-19 ve 2020-22'de TOPLAM FARK_H > 0 ve ay kümeli alt ucu > 0 VE AVR'nin iki döneminde (n >= 100 olan hücrelerde) TOPLAM "
                       "FARK_H nokta değeri > 0 VE BH (q 0,10) geçer",
              "TERS": "ABD iki dönemde de TOPLAM FARK_H üst ucu < 0 (yönsüz kümelerde 'EKSİ' diye okunur)",
              "TEK_DONEM": "ABD şartı (TOPLAM FARK_H > 0 ve alt > 0) yalnız bir dönemde",
              "TUTMADI": "ötekiler (ABD iki dönemde geçip AVR / BH'de kalan dahil; not yazılır)",
              "avr_not": "AVR hücresi n < 100 ise şart aranmaz, 'AVR n < 100' notu"},
    "dogrulama": {"tolerans": 1e-9, "K4_tolerans": 2e-6,
                  "tanim": "ölçümden ÖNCE, aynı kodla H = 15 ve kaynak kümenin KENDİ T1 tanımıyla (K1: YO örnek günleri k % 5; K2: DOJI taban dosyası; K3: "
                           "HV.hv25_uygun m = 16 bütün günler; K5: COL_SKOR6 uygun + evren + dönem pencere sonları; K4: kaynakta T1 yok, R15 olay olay) kaynak "
                           "sonuç json'undaki hücre değerleri birebir (mutlak fark <= 1e-9; K4 R15 csv %.6f yuvarlamalı, <= 2e-6); biri tutmazsa o küme DUR"},
    "esleme": "K3 / K4 olayları depoya (sembol, giriş tarihi) ile eşlenir; giriş barının depodaki açılışı E0 ile aynı olmalı (göreli 1e-9; K4 csv %.6f: "
              "mutlak 6e-7 + göreli 1e-9); eşleşmeyen olay sayılır ve düşer; e = t + 1 (kaynak bar sırası) denetlenir",
    "kesik": "depo tarih en büyüğü <= 2022-12-31 (assert) + KASA.kasa_kapisi(V_ABD.pkl, V_AVR.pkl, '2022-12-31'); her olayın 15. barı <= 2022-12-31 (assert)",
    "sira": "kod + test -> H = 15 sağlaması -> getirisiz sayım -> ön kayıt commit + push -> ik_kontrol_kapisi -> ölçüm (bir kez) -> rapor",
}

KU_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban aynı hissenin aynı hücredeki (pazar x dönem) BÜTÜN uygun günleri (aynı giriş / H bar geometrisi, giriş açılışta); önce hangisi "
                   "tabanı aynı hisse, aynı yön, aynı bağ kuralı (kötümser bağın mekanik etkisi iki tarafta aynı); SEÇİM aynı gün piyasa P_H'si; yönlü "
                   "kümede işaret çevrilir; olaylar kaynaklarında olduğu gibi (yeniden süzülmez)"),
    "K2": ("EVET", "olay kümeleri kaynak modüllerde yalnız sinyal barına kadarki veriyle kuruldu (kaynak testleri); bu modül olayları değiştirmez; R_H giriş "
                   "barından sonra; ATR e - 1 barında; T1 dönem ortalaması (kaynaklarla aynı kalıp; bilgi tarihi dönem içi, karar ölçüsü değil); "
                   "kısa ufuk getirileri yalnız ölçüm kapısından sonra (aşama assert); veri <= 2022-12-31 assert + KASA kapısı"),
    "K3": ("EVET", "depo MI.mi_veri geçerli barları (H > L, V > 0, sonlu > 0); kilitli / boşluk / evren süzgeçleri kaynak kümelerde uygulanmış; taban "
                   "günlerinde giriş boşluğu <= 10 satır, 15 bar <= 30 satır; H bar penceresi olayın kendi geçerli barları"),
    "K4": ("EVET", "olaylar kaynak tekilleştirmesiyle aynen (K1 5 bar, K3 E2 örtüşmeyen 15 bar pencereler, K4 15 bar tekil; K2 / K5 kaynakta örtüşür: "
                   "çıkarım ay kümeli bootstrap ile); n olay ve farklı ay ayrı, en kalabalık 3 ay payı, medyan yazılır"),
    "K5": ("EVET", "giriş her kümenin kendi tanımı (sinyal / pencere sonundan sonraki açılış; W3 / W4 bar içi seviye); taban günlerinde O[k + 1]; K3 / K4'te "
                   "depo açılışı E0 ile birebir denetlenir (DUR)"),
    "K6": ("EVET", "tek depo (YO ham, MI bölünme düzeltmeli açık kopya; COL_SKOR6 depo_*.npz ile içerik birebir, denetlendi); getiriler oransal, yerel "
                   "para; pazar içi karşılaştırma"),
    "K7": ("EVET", "evren bugün yaşayan hisseler: sonuç yukarı yanlı; T1 aynı hisseden olduğu için yanlılık farkta kısmen düşer; aşağı yönlü K1 kollarının "
                   "aleyhine; raporda yazılır; kasa açılmaz"),
    "K8": ("EVET", "n < 300 ya da farklı ay < 12 ABD hücresi -> ÖLÇÜLEMEDİ; ABD iki dönem + AVR iki dönem; BH q 0,10 (82 satır); 82'den fazla deneme "
                   "(kaynaklarda 15 bar) olduğu raporda yazılır"),
    "K9": ("EVET", "KU_ON_KAYIT.md: KU_KOD_SHA, KU_ESIK_SHA, bütün kaynak dosya sha'ları, SAYIM_SHA, DOGRULAMA_SHA, yorum noktaları ve hüküm; ölçüm kapısı: "
                   "kontrol + sha + ön kayıt commit + push + temiz ağaç + KASA; ikinci koşu durur; eşik / tanım sonuçtan sonra değişmez"),
    "K10": ("EVET", "olay dosyası şemaları ve satır sayıları sayımda; K3 / K4 eşlemesi E0 ve e = t + 1 ile (DUR); H = 15 sağlaması kaynak sonuç json'larıyla "
                    "birebir (DUR); K1 depo sembolü olay sembolüyle aynı (DUR)"),
    "K11": ("EVET", "rapordan önce >= 3 satır (kol x hücre x ufuk) olay dosyası + depodan bağımsız kısa kodla yeniden üretilir; H = 15 sağlaması ayrıca"),
    "K12": ("EVET", "'TUTAR / TERS / EKSİ' yalnız hüküm kuralıyla; maliyet çizgisinin altı 'işlenemez'; sayı ile yorum ayrı cümlede; evren notu; çoklu deneme "
                    "notu; K4 15 bar eski sonucu eşli farktır (TOPLAM FARK değil) diye yazılır"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_ku); mevcut modüller ve defter dosyaları değişmez (yalnız import); olay / sonuç dosyaları sha ile "
                    "değişmediği denetlenir; yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez, kasa açılmaz"),
}

KU_YORUM = [
    "Olaylar AYNEN: her kümenin olay dosyası okunur, olay seçimi (filtre, tekilleştirme, kesim) kaynakta nasılsa öyle; yalnız sonuç ufku değişir. K2'de "
    "kaynağın 'tabansız' düşürdüğü olaylar burada BÜTÜN-GÜN tabanıyla yeniden ölçülebilir hale gelebilir (n kaynaktan biraz farklı olabilir; T1_YOK sayısı "
    "yazılır).",
    "T1_H 'bütün günler': YO örnek kuralları adım 1 ile (giriş satırında P2 dahil); kaynakların tabanı farklıydı (K1 / K2 / K5 her 5. bar, K3 / K4 "
    "P2'siz hv25 günleri). Bu yüzden 15 barlık 'eski sonuç' sütunu kaynağın kendi tabanıyla, ayrıca 'KU-15' sütunu bu modülün tabanıyla yazılır "
    "(bilgi; aynı tabanla kısa / uzun ufuk karşılaştırması).",
    "Taban gün kümesi H'den bağımsız tutulur (15 bar pencere kuralı H = 3 / 5 için de aranır): T1_3, T1_5 ve T1_15 aynı günlerden; olayların hepsi "
    "kaynaklarında 15 barı tamamlamış olaylardır.",
    "R_H giriş barı dahil H'inci barın kapanışı (H = 3: giriş barı + 2 bar). Bar içi girişli K1 kollarında (W3, W3T, W4, W4Y) giriş seviyedir; R_1 seviyeden "
    "kapanışa. Taban günlerinde giriş açılışta.",
    "ÖNCE HANGİSİ: 1 ATR = WD.wd_atr_dizi (TR'nin 20 bar ortalaması) giriş barından önceki barda; giriş barı dahil 5 bar; aynı barda ikisi = desen yönünün "
    "tersi önce. Bar içi girişte giriş barının H / L'si girişten önce oluşmuş olabilir (kötümser kural iki yönde ayrı işler; bilgi).",
    "Yönsüz kümelerde (K2-K5) yön = +1 (beklenen yön yukarı); TERS kuralı 'EKSİ' diye okunur (olaydan sonra fiyat aynı hissenin rastgele gününden kötü).",
    "K3: olay27 'E2' evreni, 'gunluk', durum TAMAM, ABD / AVR, satır bayrağı <ad>_UC10 = True (B4 HEPSI_VE'nin 'UC10' bayrağı: altı bileşen kendi uç %30'unda, "
    "kaynak tanımı). Kesimler kaynakta ABD 2016-19'dan; o hücre keşif hücresidir (örneklem içi kesim, sonuç dağılımından değil, getirisiz).",
    "K4: mum_izi24_olay.csv.gz 'gunluk', ana == True, olculdu == True, grup KAPILI / KAPISIZ, ABD / AVR (BIST bilgi bile değil: depoda yok). Kaynağın 15 bar "
    "sonucu EŞLİ FARKTIR (aynı gün aynı kova eşleri), TOPLAM FARK değildir; eski sonuç sütununda bu yazılır. KAPILI ABD hücreleri n 63 / 75 -> ÖLÇÜLEMEDİ "
    "beklenir.",
    "K5: COL_SKOR6 pencere satırları uygun + EVREN + dönem; ölçüm popülasyonu CS.cs_pop(X, L); uç = değer >= cs_kesim.json 'getirisiz' kesimi (pazarın kendi "
    "2016-19 dağılımı). Pencereler k % 5 ve L > 5 olduğu için örtüşür (kaynakta da).",
    "Maliyet çizgisi %0,20 bir İŞLEM maliyetidir; TOPLAM FARK aynı hissenin rastgele gününe göre farktır (mutlak getiri değil). Çizginin altındaki fark "
    "'işlenemez'.",
    "BH ailesi 82 satır (41 kol x H 3 / 5); ilk mum, önce hangisi, SEÇİM ve H = 15 bilgi satırlarıdır, BH'ye ve hükme girmez. Bu kümelerde daha önce 15 "
    "barla 82'den fazla deneme yapıldı; kısa ufuk ayrıca bir deneme turudur.",
    "AVR hücrelerinde n < 100 ise AVR şartı aranmaz ve not yazılır (K4 KAPILI AVR n 11 / 6).",
    "Hiçbir eşik / tanım sonuçtan sonra değişmez; yalnız gösterim değişirse SAPMA'da yazılır.",
]


# ================================================================ 0) YARDIMCI
def _ku_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or KU_YOL["cikti"], KU_DOSYA[ad])


def _ku_ham(ad: str, ham: Optional[str] = None) -> str:
    return os.path.join(ham or KU_YOL["ham"], ad)


def ku_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or KU_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def ku_kod_sha() -> str:
    return MI._mi_sha(KU_YOL["kod"])


def _ku_rng(anahtar: str) -> np.random.Generator:
    return np.random.default_rng([int(KU_ESIK["tohum"]), zlib.crc32(str(anahtar).encode("utf-8"))])


def ku_kaynak_sha(anahtar: Optional[List[str]] = None) -> Dict[str, str]:
    out = {}
    for a in (anahtar or list(KU_KAYNAK)):
        y = KU_KAYNAK[a]
        if not os.path.exists(y):
            raise KUHata(f"DOSYA YOK: {a} -> {y}")
        out[a] = MI._mi_sha(y)
    return out


def ku_hucre_kod(giris: Any) -> np.ndarray:
    """Giriş tarihine göre dönem kodu: 0 = d1619, 1 = d2022, -1 = dışı (HV.hv_hucre_ad ile aynı sınırlar; testte denetlenir)."""
    g = pd.DatetimeIndex(giris)
    out = np.full(len(g), -1, np.int64)
    for i, d in enumerate(("d1619", "d2022")):
        a, b = HV.HV_ESIK["hucre"]["donem"][d]
        out[(g >= pd.Timestamp(a)) & (g <= pd.Timestamp(b))] = i
    return out


# ================================================================ 1) DEPO
def ku_depo(pazar: str, yo_ham: Optional[str] = None) -> Dict[str, Any]:
    """YO bar deposu (kesik assert)."""
    z = np.load(os.path.join(yo_ham or KU_YOL["yo_ham"], f"ham_{pazar}.npz"))
    D = {k: z[k] for k in z.files}
    tarih = pd.DatetimeIndex(D["tarih"])
    if tarih.max() > KU_KESIK:
        raise KUHata(f"KESİK: {pazar} deposunda {tarih.max().date()} > {KU_KESIK.date()} (kasa açılmaz)")
    D["tarih_ix"] = tarih
    D["sembol_ix"] = {str(s): j for j, s in enumerate(D["sembol"])}
    return D


def ku_kesik_olay(D: Dict[str, Any], j: np.ndarray, e: np.ndarray) -> None:
    """Her olayın 15. barı (e + 14) veride ve <= kesik (assert)."""
    off = D["off"]; g = off[j] + e
    if (g + 14 > off[j + 1] - 1).any() or (e < 1).any():
        raise KUHata("K10: olay 15 bar penceresi hissenin verisini aşıyor ya da giriş ilk bar")
    if (D["tarih_ix"][D["POS"][g + 14]] > KU_KESIK).any():
        raise KUHata("KESİK: olay penceresi 2022-12-31'i aşıyor")


def ku_taban_k(m: int, pos: np.ndarray, p2: np.ndarray, tarih: pd.DatetimeIndex) -> np.ndarray:
    """BÜTÜN uygun günler (getirisiz): YO.yo_ornek_maske kuralları adım 1 ile (testte k % 5 alt kümesi yo_ornek_maske ile birebir)."""
    E = YO.YO_ESIK["ornek"]; U = int(YO.YO_ESIK["yukselis"]["ufuk"])
    if m < U + 2:
        return np.array([], np.int64)
    k = np.arange(0, m - U)
    ok = (pos[k + 1] - pos[k] <= int(E["giris_bosluk"])) & (pos[k + U] - pos[k + 1] <= int(E["pencere_satir"]) - 1) & p2[pos[k + 1]]
    gt = tarih[pos[k + 1]]
    ok &= (gt >= pd.Timestamp("2016-01-01")) & (gt <= pd.Timestamp("2022-12-31")) & (tarih[pos[k + U]] <= KU_KESIK)
    return k[ok]


def ku_taban(D: Dict[str, Any]) -> pd.DataFrame:
    """Pazarın bütün uygun günleri: j, k, dönem kodu (getirisiz)."""
    off = D["off"]; P2 = D["P2"]; tarih = D["tarih_ix"]; parca_j, parca_k = [], []
    for j in range(len(off) - 1):
        a, b = int(off[j]), int(off[j + 1])
        kk = ku_taban_k(b - a, D["POS"][a:b], P2[:, j], tarih)
        if len(kk):
            parca_j.append(np.full(len(kk), j, np.int64)); parca_k.append(kk)
    j = np.concatenate(parca_j) if parca_j else np.array([], np.int64); k = np.concatenate(parca_k) if parca_k else np.array([], np.int64)
    dk = ku_hucre_kod(tarih[D["POS"][off[j] + k + 1]])
    if (dk < 0).any():
        raise KUHata("K10: taban gününde dönem dışı giriş")
    return pd.DataFrame({"j": j, "k": k, "dk": dk})


# ================================================================ 2) OLAY KÜMELERİ (getirisiz; yalnız kimlik, giriş, hücre)
_KU_OLAY_KOL = ["kume", "kol", "yon", "pazar", "sembol", "j", "e", "giris", "dk", "hucre", "ay", "giris_tarih"]


def _ku_cerceve(kume: str, kol: Any, yon: Any, pazar: str, D: Dict[str, Any], j: np.ndarray, e: np.ndarray, giris: np.ndarray) -> pd.DataFrame:
    j = np.asarray(j, np.int64); e = np.asarray(e, np.int64)
    gt = D["tarih_ix"][D["POS"][D["off"][j] + e]]; dk = ku_hucre_kod(gt)
    X = pd.DataFrame({"kume": kume, "kol": np.asarray(kol, object) if not isinstance(kol, str) else kol, "yon": np.asarray(yon, np.int64) if np.ndim(yon) else int(yon),
                      "pazar": pazar, "sembol": np.asarray(D["sembol"], object)[j], "j": j, "e": e, "giris": np.asarray(giris, float), "dk": dk})
    X["hucre"] = np.where(dk == 0, f"{pazar}|d1619", np.where(dk == 1, f"{pazar}|d2022", f"{pazar}|dis"))
    X["giris_tarih"] = gt; X["ay"] = gt.strftime("%Y-%m")
    return X[_KU_OLAY_KOL]


def ku_olay_K1(pazar: str, D: Dict[str, Any]) -> pd.DataFrame:
    T = pd.read_pickle(KU_KAYNAK[f"K1_olay_{pazar}"])
    if (np.asarray(D["sembol"], object)[T.j.to_numpy()] != T.sembol.to_numpy()).any():
        raise KUHata("K10: K1 olay sembolü depo sembolüyle uyuşmuyor")
    X = _ku_cerceve("K1", T.kol.to_numpy(), T.yon.to_numpy(), pazar, D, T.j.to_numpy(), T.e.to_numpy(), T.giris.to_numpy())
    if (X.hucre.to_numpy() != T.hucre.to_numpy()).any():
        raise KUHata("K10: K1 hücre ataması kaynaktan farklı")
    bek = np.array([WD.WD_KOL[k]["yon"] for k in T.kol])
    if (bek != T.yon.to_numpy()).any():
        raise KUHata("K10: K1 yön kaynak kol tanımından farklı")
    return X


def ku_olay_K2(pazar: str, D: Dict[str, Any]) -> pd.DataFrame:
    T = pd.read_pickle(KU_KAYNAK[f"K2_olay_{pazar}"]); T = T[T.k.isin([2, 3, 4])]
    if (np.asarray(D["sembol"], object)[T.j.to_numpy()] != T.sembol.to_numpy()).any():
        raise KUHata("K10: K2 olay sembolü depo sembolüyle uyuşmuyor")
    e = T.t.to_numpy(np.int64) + 1; g = D["off"][T.j.to_numpy()] + e
    if (D["POS"][g] != T.d_row.to_numpy()).any():
        raise KUHata("K10: K2 giriş satırı (d_row) depoyla uyuşmuyor")
    X = _ku_cerceve("K2", T.k.astype(str).to_numpy(), 1, pazar, D, T.j.to_numpy(), e, D["O"][g])
    if (X.hucre.to_numpy() != T.hucre.to_numpy()).any():
        raise KUHata("K10: K2 hücre ataması kaynaktan farklı")
    return X


def _ku_esle(D: Dict[str, Any], sembol: np.ndarray, giris: Any, E0: np.ndarray, t: np.ndarray, atol: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(sembol, giriş tarihi) -> (j, e); E0 = depo O[e] ve e = t + 1 denetimi. Döner (j, e, eşleşti)."""
    gt = pd.DatetimeIndex(pd.to_datetime(giris)); tarih = D["tarih_ix"]; N = len(sembol)
    j = np.array([D["sembol_ix"].get(str(s), -1) for s in sembol], np.int64)
    r = tarih.get_indexer(gt); e = np.full(N, -1, np.int64)
    ok = (j >= 0) & (r >= 0)
    for jj in np.unique(j[ok]):
        ii = np.flatnonzero(ok & (j == jj)); a, b = int(D["off"][jj]), int(D["off"][jj + 1]); pos = D["POS"][a:b]
        q = np.searchsorted(pos, r[ii]); q = np.minimum(q, len(pos) - 1); hit = pos[q] == r[ii]
        e[ii[hit]] = q[hit]
    ok &= e >= 0
    if ok.any():
        g = D["off"][j[ok]] + e[ok]; o = D["O"][g]; E = np.asarray(E0, float)[ok]
        if (np.abs(o - E) > atol + 1e-9 * np.abs(E)).any():
            raise KUHata("K10: eşlenen giriş barının açılışı E0 ile uyuşmuyor")
        if (e[ok] != np.asarray(t, np.int64)[ok] + 1).any():
            raise KUHata("K10: eşlenen giriş barı kaynak bar sırasıyla (t + 1) uyuşmuyor")
    return j, e, ok


def ku_olay_K3(pazar: str, D: Dict[str, Any], O27: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, Dict[str, int]]:
    if O27 is None:
        O27 = pd.read_pickle(KU_KAYNAK["K3_olay"])
    T = O27[(O27.evren == "E2") & (O27.zaman == "gunluk") & (O27.pazar == pazar) & (O27.durum == "TAMAM")]
    T = T[T.hucre.isin([h for h in KU_HUCRE if h.startswith(pazar)])]
    bay = [f"{s}_UC10" for s in UC.UC_SATIR]
    T = T[T[bay].to_numpy(bool).any(1)]
    j, e, ok = _ku_esle(D, T.sembol.to_numpy(), T.giris, T.E0.to_numpy(float), T.t.to_numpy(), 0.0)
    info = {"aday": int(len(T)), "eslesmedi": int((~ok).sum())}
    T = T[ok]; j = j[ok]; e = e[ok]; parca = []
    for s in UC.UC_SATIR:
        m = T[f"{s}_UC10"].to_numpy(bool)
        if m.any():
            parca.append(_ku_cerceve("K3", s, 1, pazar, D, j[m], e[m], T.E0.to_numpy(float)[m]))
    X = pd.concat(parca, ignore_index=True)
    return X, info


def ku_olay_K4(pazar: str, D: Dict[str, Any], A: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, Dict[str, int]]:
    if A is None:
        A = pd.read_csv(KU_KAYNAK["K4_olay"])
    T = A[(A.zaman == "gunluk") & (A.pazar == pazar) & A.ana.astype(bool) & A.olculdu.astype(bool) & A.grup.isin(["KAPILI", "KAPISIZ"])]
    j, e, ok = _ku_esle(D, T.sembol.to_numpy(), T.giris, T.E0.to_numpy(float), T.t.to_numpy(), 6e-7)
    info = {"aday": int(len(T)), "eslesmedi": int((~ok).sum())}
    T = T[ok]; j = j[ok]; e = e[ok]
    X = _ku_cerceve("K4", T.grup.to_numpy(), 1, pazar, D, j, e, T.E0.to_numpy(float))
    if (X.hucre.to_numpy() != T.hucre.to_numpy()).any():
        raise KUHata("K10: K4 hücre ataması kaynaktan farklı")
    return X, info


def _ku_k5_kesim() -> Dict[str, Any]:
    return json.load(open(KU_KAYNAK["K5_kesim"], encoding="utf-8"))


def ku_k5_pencere(pazar: str) -> pd.DataFrame:
    """COL_SKOR6 ölçüm satırları: uygun + EVREN + dönem (cs_olcum ile aynı süzgeç)."""
    X = pd.read_pickle(KU_KAYNAK[f"K5_pencere_{pazar}"]); don = X.hucre.str.split("|").str[1]
    return X[X.uygun.to_numpy(bool) & X.EVREN.to_numpy(bool) & don.isin(CS.CS_DONEM).to_numpy(bool)]


def ku_olay_K5(pazar: str, D: Dict[str, Any], X: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    if X is None:
        X = ku_k5_pencere(pazar)
    if (np.asarray(D["sembol"], object)[X.j.to_numpy()] != X.sembol.to_numpy()).any():
        raise KUHata("K10: K5 pencere sembolü depo sembolüyle uyuşmuyor")
    K = _ku_k5_kesim(); parca = []
    for ad, kol, uc, L in KU_K5_KOL:
        kk = CS.cs_kesim_al(K, pazar, L, kol)
        m = CS.cs_pop(X, L) & (X[f"{kol}_{L}"].to_numpy(float) >= kk[uc])
        g = X[m]; e = g.t.to_numpy(np.int64) + 1; gg = D["off"][g.j.to_numpy()] + e
        if (D["POS"][gg] != g.d_row.to_numpy()).any():
            raise KUHata("K10: K5 giriş satırı depoyla uyuşmuyor")
        Y = _ku_cerceve("K5", ad, 1, pazar, D, g.j.to_numpy(), e, D["O"][gg])
        if (Y.hucre.to_numpy() != g.hucre.to_numpy()).any():
            raise KUHata("K10: K5 hücre ataması kaynaktan farklı")
        parca.append(Y)
    return pd.concat(parca, ignore_index=True)


def ku_olaylar(pazar: str, D: Dict[str, Any], O27: Optional[pd.DataFrame] = None, A24: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Pazarın bütün kümeleri (getirisiz)."""
    info: Dict[str, Any] = {}
    X1 = ku_olay_K1(pazar, D); X2 = ku_olay_K2(pazar, D)
    X3, info["K3"] = ku_olay_K3(pazar, D, O27); X4, info["K4"] = ku_olay_K4(pazar, D, A24); X5 = ku_olay_K5(pazar, D)
    X = pd.concat([X1, X2, X3, X4, X5], ignore_index=True)
    X["kol_id"] = X.kume + "|" + X.kol.astype(str)
    if not set(X.kol_id.unique()) <= set(KU_KOL_ID):
        raise KUHata(f"K10: tanımsız kol: {sorted(set(X.kol_id.unique()) - set(KU_KOL_ID))}")
    if (X.dk < 0).any():
        raise KUHata("K10: dönem dışı olay (kaynak kümeler dönem içi olmalı)")
    ku_kesik_olay(D, X.j.to_numpy(), X.e.to_numpy())
    return X, info


# ================================================================ 3) SONUÇ ÇEKİRDEĞİ (aşama kapılı)
_KU_DURUM = {"kapi_gecti": False}
_KU_ASAMA = {"dogrulama": {15}, "olcum": set(KU_HEPSI_UFUK), "test": set(range(1, 31))}


def _ku_asama(asama: str, H: int, dep: Dict[str, Any]) -> None:
    if asama not in _KU_ASAMA or int(H) not in _KU_ASAMA[asama]:
        raise KUHata(f"SIRA: {asama} aşamasında H = {H} izinli değil (kısa ufuk yalnız ölçüm kapısından sonra)")
    if asama == "olcum" and not _KU_DURUM["kapi_gecti"]:
        raise KUHata("SIRA: ölçüm kapısı geçilmeden kısa ufuk getirisi istendi")
    if asama == "test" and not dep.get("_sentetik", False):
        raise KUHata("SIRA: 'test' aşaması yalnız sentetik depoyla")


def ku_R_olay(dep: Dict[str, Any], j: Any, e: Any, giris: Any, H: int, asama: str) -> np.ndarray:
    """R_H = C[e + H - 1] / giriş - 1 (giriş barı dahil H'inci geçerli bar); veri yoksa ya da tarih > kesik ise NaN."""
    _ku_asama(asama, H, dep)
    j = np.asarray(j, np.int64); e = np.asarray(e, np.int64); giris = np.asarray(giris, float); off = dep["off"]
    g = off[j] + e + int(H) - 1; ok = g <= off[j + 1] - 1; out = np.full(len(j), np.nan)
    if ok.any():
        gg = g[ok]; tar = pd.DatetimeIndex(dep["tarih"])[dep["POS"][gg]]
        v = dep["C"][gg] / giris[ok] - 1; v[np.asarray(tar > KU_KESIK)] = np.nan; out[ok] = v
    return out


def ku_R_taban(dep: Dict[str, Any], j: Any, k: Any, H: int, asama: str) -> np.ndarray:
    """Taban günü (karar barı k): C[k + H] / O[k + 1] - 1."""
    _ku_asama(asama, H, dep)
    j = np.asarray(j, np.int64); k = np.asarray(k, np.int64); off = dep["off"]; g = off[j] + k
    if len(g) and (g + int(H) > off[j + 1] - 1).any():
        raise KUHata("K10: taban penceresi hissenin verisini aşıyor")
    return dep["C"][g + int(H)] / dep["O"][g + 1] - 1


def ku_once_dizi(Hs: np.ndarray, Ls: np.ndarray, giris: np.ndarray, A: np.ndarray, yon: np.ndarray) -> np.ndarray:
    """ONCE ∈ {-1, 0, 1}: +1 ATR / -1 ATR hangisi önce (yön düzeltmeli); aynı bar = desen yönünün tersi önce; A sonlu değilse NaN."""
    giris = np.asarray(giris, float)[:, None]; A_ = np.asarray(A, float)[:, None]; yon = np.asarray(yon, np.int64)
    with np.errstate(invalid="ignore"):
        up = Hs >= giris + A_; dn = Ls <= giris - A_
    BIG = 10 ** 9
    ku = np.where(up.any(1), up.argmax(1), BIG); kd = np.where(dn.any(1), dn.argmax(1), BIG)
    fav = np.where(yon == 1, ku < kd, kd < ku)                        # bağda (ku == kd < BIG) ters önce
    adv = np.where(yon == 1, (kd <= ku) & (kd < BIG), (ku <= kd) & (ku < BIG))
    out = fav.astype(float) - adv.astype(float)
    out[~np.isfinite(np.asarray(A, float))] = np.nan
    return out


def ku_once_olay(dep: Dict[str, Any], ATR: np.ndarray, j: Any, e: Any, giris: Any, yon: Any, asama: str, H: int = 5) -> np.ndarray:
    _ku_asama(asama, H, dep)
    j = np.asarray(j, np.int64); e = np.asarray(e, np.int64); g = dep["off"][j] + e
    if len(g) and (g + H - 1 > dep["off"][j + 1] - 1).any():
        raise KUHata("K10: önce hangisi penceresi hissenin verisini aşıyor")
    W = g[:, None] + np.arange(H)[None, :]
    A = np.where(e >= 1, ATR[np.maximum(g - 1, 0)], np.nan)
    return ku_once_dizi(dep["H"][W], dep["L"][W], giris, A, yon)


def ku_once_taban(dep: Dict[str, Any], ATR: np.ndarray, j: Any, k: Any, yon: int, asama: str, H: int = 5) -> np.ndarray:
    _ku_asama(asama, H, dep)
    j = np.asarray(j, np.int64); k = np.asarray(k, np.int64); g = dep["off"][j] + k
    W = g[:, None] + 1 + np.arange(H)[None, :]
    return ku_once_dizi(dep["H"][W], dep["L"][W], dep["O"][g + 1], ATR[g], np.full(len(g), int(yon)))


def ku_PH(Op: np.ndarray, Cl: np.ndarray, P2: np.ndarray, H: int) -> np.ndarray:
    """P_H(d): YO.yo_P15 tanımı H satırla (H = 15'te yo_P15 ile birebir; testte)."""
    n, _ = Op.shape; U = int(H); out = np.full(n, np.nan); mn = int(YO.YO_ESIK["piyasa"]["en_az_hisse"])
    for d in range(n - U + 1):
        with np.errstate(invalid="ignore"):
            jj = np.flatnonzero(P2[d] & np.isfinite(Op[d]) & (Op[d] > 0))
        if not len(jj):
            continue
        c = Cl[d:d + U, jj]; okc = np.isfinite(c)
        sonk = np.where(okc.any(0), U - 1 - np.argmax(okc[::-1], axis=0), -1)
        R = np.where(sonk >= 0, c[np.maximum(sonk, 0), np.arange(len(jj))] / Op[d, jj] - 1, np.nan); R = R[np.isfinite(R)]
        if len(R) >= mn:
            out[d] = float(R.mean())
    return out


# ================================================================ 4) İSTATİSTİK
def ku_ay_W(ay: np.ndarray, anahtar: str, B: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    B = int(B or KU_ESIK["boot"]["B"]); u, k = np.unique(np.asarray(ay, str), return_inverse=True); K = len(u)
    W = _ku_rng(anahtar).multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    return k, W


def ku_boot(x: np.ndarray, k: np.ndarray, W: np.ndarray) -> Dict[str, Any]:
    """Ay kümeli bootstrap ortalama (sonlu değerler); ort, medyan, alt, üst, tek yönlü p, n."""
    x = np.asarray(x, float); f = np.isfinite(x); n = int(f.sum())
    if n < 2:
        return {"n": n, "ort": float(x[f].mean()) if n else None, "medyan": float(np.median(x[f])) if n else None, "alt": None, "ust": None, "p": None}
    K = W.shape[1]; s = np.bincount(k[f], weights=x[f], minlength=K); c = np.bincount(k[f], minlength=K).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (W @ s) / (W @ c)
    a, b = YO._q(d); dd = d[np.isfinite(d)]
    return {"n": n, "ort": float(x[f].mean()), "medyan": float(np.median(x[f])), "alt": a, "ust": b,
            "p": float((1 + (dd <= 0).sum()) / (len(dd) + 1)) if len(dd) else None}


def ku_hucre_olc(g: pd.DataFrame, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    """Bir kol x hücre: n, ay, üst3; her H için TF / SEÇİM; ILK, ONCE (H 5) ve asimetri; R medyanı."""
    ao = HV.hv25_ay_ozet(pd.DatetimeIndex(g.giris_tarih).strftime("%Y-%m-%d").tolist()) if len(g) else {"n": 0, "ay": 0, "ust3_pay": None}
    o: Dict[str, Any] = {"n": ao["n"], "ay": ao["ay"], "ust3_pay": ao["ust3_pay"]}
    if len(g) < 2:
        return o
    k, W = ku_ay_W(g.ay.to_numpy(), anahtar, B)
    for H in KU_HEPSI_UFUK:
        o[f"TF{H}"] = ku_boot(g[f"TF{H}"].to_numpy(float), k, W)
        o[f"SEC{H}"] = ku_boot(g[f"SEC{H}"].to_numpy(float), k, W)
        o[f"R{H}_medyan_yonlu"] = float(np.nanmedian(g.yon.to_numpy() * g[f"R{H}"].to_numpy(float)))
    o["ONCE_ASM"] = ku_boot(g.ONCE_ASM.to_numpy(float), k, W)
    f = np.isfinite(g.ONCE.to_numpy(float))
    o["ONCE"] = {"n": int(f.sum()), "yonde": float((g.ONCE[f] == 1).mean()) if f.any() else None,
                 "ters": float((g.ONCE[f] == -1).mean()) if f.any() else None, "taban_fark": float(g.ONCE_TB[f].mean()) if f.any() else None,
                 "olay_fark": float(g.ONCE[f].mean()) if f.any() else None}
    return o


def ku_hukum(o: Dict[str, Dict[str, Any]], H: int, bh_gecti: bool, yonlu: bool) -> Tuple[str, List[str]]:
    Hk = KU_ESIK["hukum"]; notlar: List[str] = []
    for h in KU_ABD:
        c = o.get(h, {})
        if c.get("n", 0) < int(Hk["n_min"]) or c.get("ay", 0) < int(Hk["ay_min"]):
            return "ÖLÇÜLEMEDİ", [f"{h} n {c.get('n', 0)} / ay {c.get('ay', 0)}"]
    tf = {h: o[h].get(f"TF{H}", {}) for h in KU_ABD}
    gec = {h: (tf[h].get("ort") or 0) > 0 and tf[h].get("alt") is not None and tf[h]["alt"] > 0 for h in KU_ABD}
    avr_ok = True
    for h in KU_AVR:
        c = o.get(h, {})
        if c.get("n", 0) < int(Hk["avr_n"]):
            notlar.append(f"{h.split('|')[0]} {h.split('|')[1]} n < 100 (şart aranmadı)"); continue
        v = c.get(f"TF{H}", {}).get("ort")
        if v is None or not v > 0:
            avr_ok = False
    if all(gec.values()):
        if avr_ok and bh_gecti:
            return "TUTAR", notlar
        notlar.append("ABD iki dönemde geçti, " + ("AVR işareti uymadı" if not avr_ok else "BH geçmedi"))
        return "TUTMADI", notlar
    if all(tf[h].get("ust") is not None and tf[h]["ust"] < 0 for h in KU_ABD):
        return ("TERS" if yonlu else "EKSİ"), notlar
    if sum(gec.values()) == 1:
        return "TEK DÖNEM", notlar
    return "TUTMADI", notlar


def ku_maliyet(o: Dict[str, Dict[str, Any]], H: int, hukum: str) -> Dict[str, Any]:
    v = [o.get(h, {}).get(f"TF{H}", {}).get("ort") for h in KU_ABD]
    if any(x is None for x in v):
        return {"ort": None, "etiket": "-"}
    m = float(np.mean(v)); c = float(KU_ESIK["maliyet"]["cizgi"])
    if hukum == "TUTAR":
        et = "İŞLENEBİLİR" if m > c else "işlenemez (TUTAR ama çizgi altı)"
    elif hukum in ("TERS", "EKSİ"):
        et = "ters yönde çizgi üstü (bilgi)" if abs(m) > c else "işlenemez"
    else:
        et = "çizgi üstü (hüküm yok)" if m > c else "işlenemez"
    return {"ort": m, "etiket": et}


# ================================================================ 5) H = 15 SAĞLAMASI (kaynak T1 tanımlarıyla; kısa ufuk YOK)
def _ku_fark(ad: str, mine: Optional[float], kaynak: Optional[float], tol: float, satir: List[Dict[str, Any]]) -> None:
    ok = mine is not None and kaynak is not None and np.isfinite(mine) and np.isfinite(kaynak) and abs(mine - kaynak) <= tol
    satir.append({"ad": ad, "bu_kod": mine, "kaynak": kaynak, "fark": None if not ok and (mine is None or kaynak is None) else
                  (None if mine is None or kaynak is None else float(mine - kaynak)), "tuttu": bool(ok)})


def ku_dogrula_K1(DS: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    J = json.load(open(KU_KAYNAK["S1_wd_sonuc"], encoding="utf-8")); tol = float(KU_ESIK["dogrulama"]["tolerans"]); S: List[Dict[str, Any]] = []
    for p in KU_PAZAR:
        D = DS[p]; X = ku_olay_K1(p, D); Xs, _ = YO.yo_yukle(p, KU_YOL["yo_ham"])
        t15 = ku_R_taban(D, Xs.j.to_numpy(), Xs.k.to_numpy(), 15, "dogrulama")
        T1 = pd.Series(t15).groupby([Xs.j.to_numpy(), Xs.hucre.to_numpy()]).mean()
        R = ku_R_olay(D, X.j, X.e, X.giris, 15, "dogrulama")
        t1 = T1.reindex(pd.MultiIndex.from_arrays([X.j.to_numpy(), X.hucre.to_numpy()])).to_numpy(float)
        TF = X.yon.to_numpy() * (R - t1); kol = X.kol.to_numpy(); hc = X.hucre.to_numpy()
        Ts = pd.read_pickle(KU_KAYNAK[f"K1_olay_{p}"].replace("olay_", "satir_")) if os.path.exists(KU_KAYNAK[f"K1_olay_{p}"].replace("olay_", "satir_")) else None
        if Ts is not None:
            _ku_fark(f"K1 {p} olay R15 en büyük mutlak fark", float(np.nanmax(np.abs(R - Ts.R15.to_numpy()))), 0.0, tol, S)
        for k in WD.WD_KOLLAR:
            for h in [x for x in KU_HUCRE if x.startswith(p)]:
                m = (kol == k) & (hc == h)
                _ku_fark(f"K1 {k} {h} TF15", float(np.mean(TF[m])) if m.any() else None, J["kol"][k]["hucre"][h].get("TF", {}).get("ort"), tol, S)
    return S


def ku_dogrula_K2(DS: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    J = json.load(open(KU_KAYNAK["S2_dj_sonuc"], encoding="utf-8")); tol = float(KU_ESIK["dogrulama"]["tolerans"]); S: List[Dict[str, Any]] = []
    for p in KU_PAZAR:
        D = DS[p]; X = ku_olay_K2(p, D); T = pd.read_pickle(KU_KAYNAK[f"K2_taban_{p}"])
        t15 = ku_R_taban(D, T.j.to_numpy(), T.t.to_numpy(), 15, "dogrulama")
        T1 = pd.Series(t15).groupby([T.j.to_numpy(), T.hucre.to_numpy()]).mean()
        R = ku_R_olay(D, X.j, X.e, X.giris, 15, "dogrulama")
        t1 = T1.reindex(pd.MultiIndex.from_arrays([X.j.to_numpy(), X.hucre.to_numpy()])).to_numpy(float)
        TF = R - t1; ok = np.isfinite(t1)
        for k in ("2", "3", "4"):
            for h in [x for x in KU_HUCRE if x.startswith(p)]:
                m = ok & (X.kol.to_numpy() == k) & (X.hucre.to_numpy() == h); src = J["ANA"]["hucre"][h][k]
                _ku_fark(f"K2 k={k} {h} TF15", float(np.mean(TF[m])) if m.any() else None, src["TOPLAM_FARK"].get("ort"), tol, S)
                _ku_fark(f"K2 k={k} {h} n", float(m.sum()), float(src["n"]), 0.0, S)
    return S


def _ku_hv25_A(D: Dict[str, Any], j: int) -> Dict[str, Any]:
    a, b = int(D["off"][j]), int(D["off"][j + 1])
    Dg = pd.DataFrame({"Open": D["O"][a:b], "High": D["H"][a:b], "Low": D["L"][a:b], "Close": D["C"][a:b]}, index=D["tarih_ix"][D["POS"][a:b]])
    return HV.hv25_dizi(Dg, None)


def ku_dogrula_K3(DS: Dict[str, Dict[str, Any]], O27: pd.DataFrame) -> List[Dict[str, Any]]:
    tol = float(KU_ESIK["dogrulama"]["tolerans"]); S: List[Dict[str, Any]] = []
    sat = json.load(open(KU_KAYNAK["S3_mum27_sonuc"], encoding="utf-8"))["tablo"]["satir"]
    ref = {(r["satir"], r["hucre"]): r for r in sat if r.get("evren") == "E2" and r.get("zaman") == "gunluk" and r.get("uc") == "UC10"}
    for p in KU_PAZAR:
        D = DS[p]; T = O27[(O27.evren == "E2") & (O27.zaman == "gunluk") & (O27.pazar == p) & (O27.durum == "TAMAM")]
        T = T[T.hucre.isin([h for h in KU_HUCRE if h.startswith(p)])]
        bay = [f"{s}_UC10" for s in UC.UC_SATIR]; T = T[T[bay].to_numpy(bool).any(1)]
        j, e, ok = _ku_esle(D, T.sembol.to_numpy(), T.giris, T.E0.to_numpy(float), T.t.to_numpy(), 0.0)
        if (~ok).any():
            raise KUHata(f"K3 {p}: {int((~ok).sum())} olay depoyla eşleşmedi (sağlama DUR)")
        R = ku_R_olay(D, j, e, T.E0.to_numpy(float), 15, "dogrulama")
        dn = T.hucre.str.split("|").str[1].to_numpy(); T1 = np.full(len(T), np.nan)
        for jj in np.unique(j):
            A = _ku_hv25_A(D, int(jj)); ii = np.flatnonzero(j == jj)
            for d in np.unique(dn[ii]):
                a, b = HV.HV_ESIK["hucre"]["donem"][d]; tu = HV.hv25_uygun(A, 16, [], a, b, UC.UC_KESIK)
                if len(tu):
                    g = int(D["off"][jj]) + tu
                    T1[ii[dn[ii] == d]] = float(np.mean(D["C"][g + 15] / D["O"][g + 1] - 1))
        _ku_fark(f"K3 {p} olay R15 en büyük mutlak fark", float(np.nanmax(np.abs(R - T.R15.to_numpy(float)))), 0.0, tol, S)
        _ku_fark(f"K3 {p} olay T1 en büyük mutlak fark", float(np.nanmax(np.abs(T1 - T.T1.to_numpy(float)))), 0.0, tol, S)
        TF = R - T1; hc = T.hucre.to_numpy()
        for s in UC.UC_SATIR:
            for h in [x for x in KU_HUCRE if x.startswith(p)]:
                m = T[f"{s}_UC10"].to_numpy(bool) & (hc == h); r = ref.get((s, h), {})
                _ku_fark(f"K3 {s} {h} TF15", float(np.mean(TF[m])) if m.any() else None, (r.get("TF") or {}).get("ort"), tol, S)
    return S


def ku_dogrula_K4(DS: Dict[str, Dict[str, Any]], A24: pd.DataFrame) -> List[Dict[str, Any]]:
    tol = float(KU_ESIK["dogrulama"]["K4_tolerans"]); S: List[Dict[str, Any]] = []
    Tj = json.load(open(KU_KAYNAK["S4_mum24_sonuc"], encoding="utf-8"))["tablo"]["hucre"]
    for p in KU_PAZAR:
        D = DS[p]; T = A24[(A24.zaman == "gunluk") & (A24.pazar == p) & A24.ana.astype(bool) & A24.olculdu.astype(bool) & A24.grup.isin(["KAPILI", "KAPISIZ"])]
        j, e, ok = _ku_esle(D, T.sembol.to_numpy(), T.giris, T.E0.to_numpy(float), T.t.to_numpy(), 6e-7)
        if (~ok).any():
            raise KUHata(f"K4 {p}: {int((~ok).sum())} olay depoyla eşleşmedi (sağlama DUR)")
        R = ku_R_olay(D, j, e, T.E0.to_numpy(float), 15, "dogrulama")
        _ku_fark(f"K4 {p} olay R15 en büyük mutlak fark (csv %.6f)", float(np.nanmax(np.abs(R - T.R15.to_numpy(float)))), 0.0, tol, S)
        for g in ("KAPILI", "KAPISIZ"):
            for h in [x for x in KU_HUCRE if x.startswith(p)]:
                m = (T.grup.to_numpy() == g) & (T.hucre.to_numpy() == h); src = Tj.get(f"gunluk|{g}|{h}", {})
                _ku_fark(f"K4 {g} {h} R15 ort (ölçülen)", float(np.mean(R[m])) if m.any() else None, src.get("R15_ort_olculen"), tol, S)
                _ku_fark(f"K4 {g} {h} n ölçülen", float(m.sum()), float(src.get("n_olculen", -1)), 0.0, S)
    return S


def ku_dogrula_K5(DS: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    tol = float(KU_ESIK["dogrulama"]["tolerans"]); S: List[Dict[str, Any]] = []
    J = json.load(open(KU_KAYNAK["S5_cs_sonuc"], encoding="utf-8"))["satir"]; K = _ku_k5_kesim()
    for p in KU_PAZAR:
        D = DS[p]; X = ku_k5_pencere(p)
        R = ku_R_taban(D, X.j.to_numpy(), X.t.to_numpy(), 15, "dogrulama")
        T1 = pd.Series(R, index=X.index).groupby([X.hucre, X.sembol]).transform("mean").to_numpy(float); TF = R - T1
        for ad, kol, uc, L in KU_K5_KOL:
            kk = CS.cs_kesim_al(K, p, L, kol); m0 = CS.cs_pop(X, L) & (X[f"{kol}_{L}"].to_numpy(float) >= kk[uc])
            for h in [x for x in KU_HUCRE if x.startswith(p)]:
                m = m0 & (X.hucre.to_numpy() == h); src = J[f"{kol}|{uc}|{L}"][h]
                _ku_fark(f"K5 {ad} {h} TF15", float(np.mean(TF[m])) if m.any() else None, src.get("TOPLAM_FARK"), tol, S)
                _ku_fark(f"K5 {ad} {h} n", float(m.sum()), float(src.get("n")), 0.0, S)
    return S


def ku_dogrula(ham: Optional[str] = None) -> Dict[str, Any]:
    """H = 15 sağlaması: beş küme; biri tutmazsa DUR. Kısa ufuk hesaplanmaz (aşama 'dogrulama' yalnız H = 15)."""
    t0 = time.time(); ham = ham or KU_YOL["ham"]; os.makedirs(ham, exist_ok=True)
    DS = {p: ku_depo(p) for p in KU_PAZAR}
    O27 = pd.read_pickle(KU_KAYNAK["K3_olay"]); A24 = pd.read_csv(KU_KAYNAK["K4_olay"])
    out: Dict[str, Any] = {"surum": KU_SURUM, "zaman": MI._mi_simdi(), "kume": {}}
    for ad, f in (("K1", lambda: ku_dogrula_K1(DS)), ("K2", lambda: ku_dogrula_K2(DS)), ("K3", lambda: ku_dogrula_K3(DS, O27)),
                  ("K4", lambda: ku_dogrula_K4(DS, A24)), ("K5", lambda: ku_dogrula_K5(DS))):
        S = f(); out["kume"][ad] = {"satir": S, "tuttu": all(s["tuttu"] for s in S), "n_satir": len(S)}
        kulog.info("sağlama %s: %d satır, %s", ad, len(S), "TUTTU" if out["kume"][ad]["tuttu"] else "TUTMADI")
    out["hepsi_tuttu"] = all(v["tuttu"] for v in out["kume"].values()); out["sure_sn"] = round(time.time() - t0, 1)
    MI._mi_jyaz(_ku_ham("ku_dogrulama.json", ham), out, "ku sağlama")
    if not out["hepsi_tuttu"]:
        bad = [s["ad"] for v in out["kume"].values() for s in v["satir"] if not s["tuttu"]][:10]
        raise KUHata(f"H = 15 SAĞLAMASI TUTMADI (DUR): {bad}")
    return out


# ================================================================ 6) GETİRİSİZ SAYIM
def ku_sayim(ham: Optional[str] = None) -> Dict[str, Any]:
    """Küme x kol x hücre olay sayıları (T1 tabanı >= 30 gün olanlar), T1_YOK, eşleşmeyen; taban gün sayıları; kaynak sha. Getiri hesaplanmaz."""
    ham = ham or KU_YOL["ham"]; os.makedirs(ham, exist_ok=True)
    O27 = pd.read_pickle(KU_KAYNAK["K3_olay"]); A24 = pd.read_csv(KU_KAYNAK["K4_olay"])
    S: Dict[str, Any] = {"surum": KU_SURUM, "hucre": {}, "taban": {}, "t1_yok": {}, "esleme": {}, "ham_n": {}}
    for p in KU_PAZAR:
        D = ku_depo(p); X, info = ku_olaylar(p, D, O27, A24); S["esleme"][p] = info
        T = ku_taban(D); key_t = T.j.to_numpy() * 2 + T.dk.to_numpy(); cnt = np.bincount(key_t, minlength=2 * (len(D["off"]) - 1))
        key = X.j.to_numpy() * 2 + X.dk.to_numpy(); X["t1_n"] = cnt[key]
        for h in [x for x in KU_HUCRE if x.startswith(p)]:
            S["taban"][h] = {"gun": int((T.dk == (0 if h.endswith("d1619") else 1)).sum()),
                             "hisse": int(T[T.dk == (0 if h.endswith("d1619") else 1)].j.nunique())}
        for kid, g in X.groupby("kol_id"):
            S["ham_n"][f"{kid}|{p}"] = int(len(g)); S["t1_yok"][f"{kid}|{p}"] = int((g.t1_n < int(KU_ESIK["taban"]["en_az"])).sum())
            gg = g[g.t1_n >= int(KU_ESIK["taban"]["en_az"])]
            for h, gh in gg.groupby("hucre"):
                ao = HV.hv25_ay_ozet(pd.DatetimeIndex(gh.giris_tarih).strftime("%Y-%m-%d").tolist())
                S["hucre"][f"{kid}|{h}"] = {"n": ao["n"], "ay": ao["ay"], "ust3_pay": ao["ust3_pay"]}
        del D, X, T; gc.collect()
    S["kaynak_sha"] = ku_kaynak_sha()
    MI._mi_jyaz(_ku_ham("ku_sayim.json", ham), S, "ku sayım")
    return S


def ku_sayim_sha(S: Dict[str, Any]) -> str:
    return HV.hv_json_sha({k: v for k, v in S.items() if k != "kaynak_sha"})


# ================================================================ 7) ÖN KAYIT + KAPI
def _f(x: Any, n: int = 2, yuzde: bool = False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    v = float(x) * (100 if yuzde else 1)
    return f"{v:.{n}f}".replace(".", ",")


def ku_onkayit_yaz(cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    import IZ_KARNE as IK  # noqa: F401  (kontrol tablosu maddeleri)
    cikti = cikti or KU_YOL["cikti"]
    S = json.load(open(_ku_ham("ku_sayim.json", ham), encoding="utf-8")); V = json.load(open(_ku_ham("ku_dogrulama.json", ham), encoding="utf-8"))
    if not V.get("hepsi_tuttu"):
        raise KUHata("ön kayıt yazılmaz: H = 15 sağlaması tutmadı")
    sha = ku_kaynak_sha()
    if sha != S["kaynak_sha"]:
        raise KUHata("K9: kaynak dosyalar sayımdan sonra değişti")
    L = [f"# KU_ON_KAYIT — mevcut beş olay kümesi 3 ve 5 mumluk ufukta: kısa ufuk getirileri hesaplanmadan ÖNCE ({MI._mi_simdi()})", "",
         f"Sürüm: {KU_SURUM}. İş tanımı: KU_IS_TANIMI.md. Sonuç dosyası (ku_sonuc.json) bu ön kayıt commit + push edilmeden üretilmez (kapı). "
         "Evren bugün yaşayan hisseler (yukarı yanlı). KASA açılmaz (veri <= 2022-12-31). Olaylar kaynak dosyalarından AYNEN alınır; yalnız ufuk değişir.", "",
         "## Mühürler", "", f"KU_KOD_SHA: {ku_kod_sha()}", f"KU_ESIK_SHA: {ku_esik_sha()}"]
    L += [f"DOSYA_{a}: {v}" for a, v in sha.items()]
    L += [f"SAYIM_SHA: {ku_sayim_sha(S)}", f"DOGRULAMA_SHA: {HV.hv_json_sha({k: v for k, v in V.items() if k not in ('zaman', 'sure_sn')})}", "",
          "Kaynak yolları:", ""] + [f"- {a}: {y}" for a, y in KU_KAYNAK.items()]
    L += ["", "## Eşik / tanım sözlüğü (KU_ESIK, sabit)", "", "```json", json.dumps(KU_ESIK, ensure_ascii=False, indent=1), "```", ""]
    # sağlama
    L += ["## H = 15 SAĞLAMASI (kaynak kümelerin kendi T1 tanımıyla; bu sonuçlar zaten yayımlandı; kısa ufuk hesaplanmadı)", "",
          "| küme | satır | tuttu | örnekler (bu kod / kaynak) |", "|---|---|---|---|"]
    orn = {"K1": "K1 W7T ABD|d1619 TF15", "K2": "K2 k=2 ABD|d1619 TF15", "K3": "K3 BOY_YUZDE_ORAN ABD|d1619 TF15", "K4": "K4 KAPILI ABD|d1619 R15 ort (ölçülen)",
           "K5": "K5 PUAN_ESIT_UC10_L20 ABD|d1619 TF15"}
    for ad, v in V["kume"].items():
        ex = [s for s in v["satir"] if s["ad"] == orn[ad]] + [s for s in v["satir"] if "en büyük mutlak fark" in s["ad"]]
        L.append(f"| {ad} | {v['n_satir']} | {'EVET' if v['tuttu'] else 'HAYIR'} | " +
                 "; ".join(f"{s['ad']}: {_f(s['bu_kod'], 6, True) if 'fark' not in s['ad'] else _f(s['bu_kod'], 9)} / "
                           f"{_f(s['kaynak'], 6, True) if 'fark' not in s['ad'] else _f(s['kaynak'], 9)}" for s in ex) + " |")
    # sayım
    L += ["", "## GETİRİSİZ SAYIM (T1 tabanı >= 30 gün olan olaylar; n / farklı ay / en kalabalık 3 ay payı)", "",
          "| kol | yön | ABD 2016-19 | ABD 2020-22 | AVR 2016-19 | AVR 2020-22 | T1_YOK (ABD / AVR) |", "|---|---|---|---|---|---|---|"]
    for k in KU_KOLLAR:
        c = [S["hucre"].get(f"{k['id']}|{h}") for h in KU_HUCRE]
        L.append(f"| {k['id']} | {'+' if k['yon'] > 0 else '-'}{'' if k['yonlu'] else ' (yönsüz)'} | " +
                 " | ".join(f"{x['n']} / {x['ay']} / {_f(x['ust3_pay'], 2)}" if x else "0" for x in c) +
                 f" | {S['t1_yok'].get(k['id'] + '|ABD', 0)} / {S['t1_yok'].get(k['id'] + '|AVR', 0)} |")
    L += ["", "Taban (bütün uygun günler): " + "; ".join(f"{h}: {v['gun']} gün, {v['hisse']} hisse" for h, v in S["taban"].items()),
          "", "Eşleme (K3 / K4; depoya sembol + giriş tarihiyle): " + json.dumps(S["esleme"], ensure_ascii=False), ""]
    L += ["## Yorum noktaları (ölçümden ÖNCE sabit)", ""] + [f"{i + 1}. {x}" for i, x in enumerate(KU_YORUM)]
    Hk = KU_ESIK["hukum"]
    L += ["", "## Hüküm (önceden; kol x ufuk, H = 3 ve H = 5 ayrı)", "", f"- TUTAR: {Hk['TUTAR']}", f"- TERS / EKSİ: {Hk['TERS']}",
          f"- TEK DÖNEM: {Hk['TEK_DONEM']}", f"- TUTMADI: {Hk['TUTMADI']}", f"- sıra: {Hk['sira']}", f"- maliyet: {KU_ESIK['maliyet']['tanim']}",
          f"- BH: {KU_ESIK['bh']['aile']}", "", "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "",
          "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    ad = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
          "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
          "K13": "süreç", "K14": "boyut (gerçek para)"}
    for k, (y, kn) in KU_KONTROL.items():
        L.append(f"| {k} | {ad[k]} | {y} | {kn} |")
    return MI._mi_yaz(_ku_yol("onkayit", cikti), "\n".join(L) + "\n", "KU_ON_KAYIT")


def ku_kapi(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    """Ölçüm kapısı: sonuç yoksa; kontrol listesi; mühürler; ön kayıt commit'li ve uzakta; kod / ön kayıt temiz; KASA."""
    import IZ_KARNE as IK
    import KASA as KS
    cikti = cikti or KU_YOL["cikti"]; yol = _ku_yol("onkayit", cikti)
    if os.path.exists(_ku_yol("sonuc", cikti)):
        raise KUHata("sonuç zaten var (ikinci koşu DURUR)")
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise KUHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read()
    S = json.load(open(_ku_ham("ku_sayim.json", ham), encoding="utf-8"))
    bek = {"KU_KOD_SHA": ku_kod_sha(), "KU_ESIK_SHA": ku_esik_sha(), **{f"DOSYA_{a}": v for a, v in ku_kaynak_sha().items()}, "SAYIM_SHA": ku_sayim_sha(S)}
    for a, v in bek.items():
        if f"{a}: {v}" not in metin:
            raise KUHata(f"ön kayıt kapısı: {a} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_KU); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise KUHata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "KISA_UFUK.py"]):
        raise KUHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    uzak = MI._mi_git(["branch", "-r", "--contains", c.split()[0]])
    if not uzak:
        raise KUHata("ön kayıt commit'i uzakta (push) değil -> DURDU")
    try:
        kasa = KS.kasa_kapisi([os.path.join(KU_YOL["acik"], f"V_{p}.pkl") for p in KU_PAZAR], "2022-12-31")
    except KS.KasaHata as ex:
        raise KUHata(f"KASA kapısı KAPALI: {ex}") from ex
    _KU_DURUM["kapi_gecti"] = True
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, "uzak": uzak.split()[0] if uzak else "", "kasa": kasa, **bek}


# ================================================================ 8) ÖLÇÜM (BİR KEZ)
def ku_pazar_hesap(p: str, D: Dict[str, Any], X: pd.DataFrame, asama: str = "olcum") -> pd.DataFrame:
    """Olay satırlarına R_H, T1_H, TF_H, SEC_H (H 1, 3, 5, 15), ONCE / ONCE_TB / ONCE_ASM (getiri; aşama kapılı)."""
    T = ku_taban(D); nkey = 2 * (len(D["off"]) - 1); key_t = T.j.to_numpy() * 2 + T.dk.to_numpy()
    cnt = np.bincount(key_t, minlength=nkey).astype(float)
    X = X.copy(); key = X.j.to_numpy() * 2 + X.dk.to_numpy()
    X = X[cnt[key] >= int(KU_ESIK["taban"]["en_az"])].copy(); key = X.j.to_numpy() * 2 + X.dk.to_numpy()
    yon = X.yon.to_numpy(np.int64); drow = D["POS"][D["off"][X.j.to_numpy()] + X.e.to_numpy()]
    for H in KU_HEPSI_UFUK:
        rt = ku_R_taban(D, T.j.to_numpy(), T.k.to_numpy(), H, asama)
        T1 = np.bincount(key_t, weights=rt, minlength=nkey) / np.maximum(cnt, 1)
        R = ku_R_olay(D, X.j, X.e, X.giris, H, asama); PH = ku_PH(D["Op"], D["Cl"], D["P2"], H)
        X[f"R{H}"] = R; X[f"T1_{H}"] = T1[key]; X[f"TF{H}"] = yon * (R - T1[key]); X[f"SEC{H}"] = yon * (R - PH[drow])
    dep = {k: D[k] for k in ("O", "H", "L", "C", "POS", "off")}; ATR = WD.wd_atr_dizi(dep)
    tb = {}
    for y in (1, -1):
        v = ku_once_taban(D, ATR, T.j.to_numpy(), T.k.to_numpy(), y, asama)
        f = np.isfinite(v); s = np.bincount(key_t[f], weights=v[f], minlength=nkey); c = np.bincount(key_t[f], minlength=nkey).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            tb[y] = np.where(c > 0, s / c, np.nan)
    X["ONCE"] = ku_once_olay(D, ATR, X.j, X.e, X.giris, yon, asama)
    X["ONCE_TB"] = np.where(yon == 1, tb[1][key], tb[-1][key]); X["ONCE_ASM"] = X.ONCE - X.ONCE_TB
    X["ILK"] = X["TF1"]
    return X


def ku_olcum_hesap(SS: Dict[str, pd.DataFrame], B: Optional[int] = None) -> Dict[str, Any]:
    A = pd.concat(list(SS.values()), ignore_index=True)
    J: Dict[str, Any] = {"surum": KU_SURUM, "kol": {}}
    for k in KU_KOLLAR:
        J["kol"][k["id"]] = {**k, "hucre": {}}
        for h in KU_HUCRE:
            g = A[(A.kol_id == k["id"]) & (A.hucre == h)]
            J["kol"][k["id"]]["hucre"][h] = ku_hucre_olc(g, f"{k['id']}|{h}", B)
    ad, pp = [], []
    for k in KU_KOLLAR:
        for H in KU_UFUK:
            ps = [J["kol"][k["id"]]["hucre"][h].get(f"TF{H}", {}).get("p") for h in KU_ABD]
            ad.append((k["id"], H)); pp.append(max(ps) if all(x is not None for x in ps) else None)
    q = HV._hv_bh(pp, float(KU_ESIK["bh"]["q"]))
    for (kid, H), p_, q_ in zip(ad, pp, q):
        K = J["kol"][kid]; bh = q_ is not None and q_ <= float(KU_ESIK["bh"]["q"])
        hk, nt = ku_hukum(K["hucre"], H, bh, bool(K["yonlu"]))
        K[f"H{H}"] = {"p": p_, "bh_q": q_, "bh_gecti": bool(bh), "hukum": hk, "not": nt, "maliyet": ku_maliyet(K["hucre"], H, hk)}
    say: Dict[str, int] = {}
    for k in KU_KOLLAR:
        for H in KU_UFUK:
            v = J["kol"][k["id"]][f"H{H}"]["hukum"]; say[f"H{H}|{v}"] = say.get(f"H{H}|{v}", 0) + 1
    J["hukum_say"] = say
    tut = [f"{k['id']} H{H}" for k in KU_KOLLAR for H in KU_UFUK if J["kol"][k["id"]][f"H{H}"]["hukum"] == "TUTAR"]
    J["genel"] = ("KISA UFUKTA TUTAN KOL VAR: " + ", ".join(tut) + " (açık veride aday; KASA KURALI: tek iz kasa açmaz; ileri test)" if tut
                  else "KISA UFUKTA (3 / 5 MUM) TUTAN KOL YOK (bu kümelerde)")
    return J


def _ku_eski(J: Dict[str, Any]) -> None:
    """15 barlık eski sonuçlar (kaynak json'lar; karşılaştırma için)."""
    W = json.load(open(KU_KAYNAK["S1_wd_sonuc"], encoding="utf-8")); Dj = json.load(open(KU_KAYNAK["S2_dj_sonuc"], encoding="utf-8"))
    M = json.load(open(KU_KAYNAK["S3_mum27_sonuc"], encoding="utf-8"))["tablo"]
    M4 = json.load(open(KU_KAYNAK["S4_mum24_sonuc"], encoding="utf-8"))["tablo"]["hucre"]; C = json.load(open(KU_KAYNAK["S5_cs_sonuc"], encoding="utf-8"))
    ref = {(r["satir"], r["hucre"]): r for r in M["satir"] if r.get("evren") == "E2" and r.get("zaman") == "gunluk" and r.get("uc") == "UC10"}
    hk27 = {s: (M.get("hukum") or {}).get(f"E2|gunluk|{s}|UC10", {}).get("hukum") for s in UC.UC_SATIR}
    for k in KU_KOLLAR:
        e: Dict[str, Any] = {"olcu": "TOPLAM FARK (kaynak tabanı)", "hucre": {}, "hukum": None}
        for h in KU_HUCRE:
            v = None
            if k["kume"] == "K1":
                v = W["kol"][k["kol"]]["hucre"][h].get("TF", {}).get("ort"); e["hukum"] = W["kol"][k["kol"]].get("hukum")
            elif k["kume"] == "K2":
                v = Dj["ANA"]["hucre"][h][k["kol"]]["TOPLAM_FARK"].get("ort"); e["hukum"] = Dj["hukum"]["satir"].get(f"{k['kol']}|TOPLAM_FARK")
            elif k["kume"] == "K3":
                v = (ref.get((k["kol"], h), {}).get("TF") or {}).get("ort"); e["hukum"] = hk27.get(k["kol"])
            elif k["kume"] == "K4":
                v = M4.get(f"gunluk|{k['kol']}|{h}", {}).get("fark"); e["olcu"] = "EŞLİ FARK (kaynak; TOPLAM FARK değil)"
                e.setdefault("hukum_hucre", {})[h] = M4.get(f"gunluk|{k['kol']}|{h}", {}).get("hukum")
                e["hukum"] = "hücre: " + " / ".join(str(e["hukum_hucre"].get(x)) for x in KU_ABD if x in e["hukum_hucre"])
            else:
                _, kol, uc, Lp = [x for x in KU_K5_KOL if x[0] == k["kol"]][0]
                v = C["satir"][f"{kol}|{uc}|{Lp}"][h].get("TOPLAM_FARK"); e["hukum"] = C.get("hukum", {}).get(f"{kol}|{uc}|{Lp}")
            e["hucre"][h] = v
        J["kol"][k["id"]]["eski15"] = e


def ku_olcum(cikti: Optional[str] = None, ham: Optional[str] = None, B: Optional[int] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or KU_YOL["cikti"]; ham = ham or KU_YOL["ham"]
    kapi = ku_kapi(cikti, ham)
    O27 = pd.read_pickle(KU_KAYNAK["K3_olay"]); A24 = pd.read_csv(KU_KAYNAK["K4_olay"]); SS = {}
    for p in KU_PAZAR:
        D = ku_depo(p); X, _ = ku_olaylar(p, D, O27, A24)
        SS[p] = ku_pazar_hesap(p, D, X, "olcum")
        SS[p].to_pickle(_ku_ham(f"ku_satir_{p}.pkl", ham), protocol=4)
        del D, X; gc.collect()
    J = ku_olcum_hesap(SS, B); _ku_eski(J)
    J.update({"kapi": kapi, "esik_sha": ku_esik_sha(), "kod_sha": ku_kod_sha(), "zaman": MI._mi_simdi(), "sure_sn": round(time.time() - t0, 1),
              "satir_sha": {p: MI._mi_sha(_ku_ham(f"ku_satir_{p}.pkl", ham)) for p in KU_PAZAR}})
    simdi = ku_kaynak_sha()
    if any(simdi[a] != kapi[f"DOSYA_{a}"] for a in simdi):
        raise KUHata("K13: kaynak dosyalar ölçüm sırasında değişti")
    MI._mi_jyaz(_ku_yol("sonuc", cikti), J, "ku sonuç")
    ku_ozet_csv(J, _ku_yol("ozet", cikti))
    kulog.info("ölçüm bitti (%.0f sn): %s", time.time() - t0, J["genel"])
    return J


def ku_ozet_csv(J: Dict[str, Any], yol: str) -> str:
    R = []
    for kid, K in J["kol"].items():
        for h in KU_HUCRE:
            c = K["hucre"][h]
            r = {"kol": kid, "kume": K["kume"], "yon": K["yon"], "hucre": h, "n": c.get("n"), "ay": c.get("ay"), "ust3_pay": c.get("ust3_pay")}
            for H in KU_HEPSI_UFUK:
                for a in ("ort", "alt", "ust", "p", "medyan"):
                    r[f"TF{H}_{a}"] = (c.get(f"TF{H}") or {}).get(a)
                r[f"SEC{H}_ort"] = (c.get(f"SEC{H}") or {}).get("ort")
            for a in ("ort", "alt", "ust"):
                r[f"ONCE_ASM_{a}"] = (c.get("ONCE_ASM") or {}).get(a)
            r["ONCE_yonde"] = (c.get("ONCE") or {}).get("yonde"); r["ONCE_ters"] = (c.get("ONCE") or {}).get("ters")
            r["eski15"] = (K.get("eski15") or {}).get("hucre", {}).get(h)
            for H in KU_UFUK:
                r[f"H{H}_hukum"] = K[f"H{H}"]["hukum"]; r[f"H{H}_bh_q"] = K[f"H{H}"]["bh_q"]; r[f"H{H}_maliyet"] = K[f"H{H}"]["maliyet"]["etiket"]
            R.append(r)
    df = pd.DataFrame(R); txt = df.to_csv(index=False)
    return MI._mi_yaz(yol, txt, "ku özet")


# ================================================================ 9) RAPOR
def _ar(b: Optional[Dict[str, Any]], n: int = 2) -> str:
    if not b or b.get("ort") is None:
        return "-"
    return f"{_f(b['ort'], n, True)} [{_f(b.get('alt'), n, True)}; {_f(b.get('ust'), n, True)}]"


def ku_rapor_yaz(cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    cikti = cikti or KU_YOL["cikti"]; J = json.load(open(_ku_yol("sonuc", cikti), encoding="utf-8"))
    ek_yol = _ku_ham("ku_rapor_ek.json", ham); EK = json.load(open(ek_yol, encoding="utf-8")) if os.path.exists(ek_yol) else {}
    L = ["# KU_RAPOR — mevcut beş olay kümesi 3 ve 5 mumluk ufukta (ABD + AVR 2016-2022)", "",
         "Birimler: TOPLAM FARK yüzde puan (yön düzeltmeli; aşağı desende işaret çevrildi; yönsüz kümelerde yön = yukarı), [ay kümeli bootstrap %95]. "
         "TOPLAM FARK_H = R_H - aynı hissenin aynı dönemdeki bütün uygun günlerinin R_H ortalaması. ÖNCE = 5 barda +1 ATR / -1 ATR hangisi önce "
         "(yönde - ters), ASİMETRİ = olay - aynı hissenin rastgele günleri (puan, x 100). İLK = giriş barının kendi getirisi - rastgele gün. 15 bar eski = "
         "kaynak raporun kendi tabanıyla (K4: EŞLİ FARK); KU-15 = bu modülün tabanıyla 15 bar (bilgi). Evren bugün yaşayan hisseler (yukarı yanlı). "
         f"Maliyet çizgisi %0,20 (gidiş-dönüş). BH ailesi 82 satır (41 kol x 2 ufuk); bu kümelerde 15 barla daha önce 82'den fazla deneme yapıldı.", "",
         "## SONUÇ", "", f"- GENEL: {J['genel']}",
         "- Hüküm sayıları: " + ", ".join(f"{a} {v}" for a, v in sorted(J["hukum_say"].items())), ""]
    for kume, baslik in (("K1", "K1 WEB DESENLERİ (yönlü)"), ("K2", "K2 DOJİ ÖBEĞİ (yönsüz)"), ("K3", "K3 UÇLAR, E2 günlük UÇ10 (yönsüz)"),
                         ("K4", "K4 KODUN SEÇTİĞİ BÖLGELER, günlük ANA (yönsüz)"), ("K5", "K5 ESKİ ÇÖL PUANI (yönsüz)")):
        L += [f"### {baslik}", "", "| kol | yön | H=3 TF ABD 16-19 | H=3 TF ABD 20-22 | H=5 TF ABD 16-19 | H=5 TF ABD 20-22 | ÖNCE asimetri 16-19 / 20-22 | "
              "İLK mum 16-19 / 20-22 | KU-15 16-19 / 20-22 | 15 bar eski 16-19 / 20-22 | AVR H3 / H5 (16-19; 20-22) | n ABD | hüküm H=3 / H=5 | maliyet H3 / H5 | BH q H3 / H5 |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for kid, K in J["kol"].items():
            if K["kume"] != kume:
                continue
            c = K["hucre"]; e = K.get("eski15", {}).get("hucre", {})
            avr = "; ".join("/".join(_f((c[h].get(f"TF{H}") or {}).get("ort"), 2, True) for H in KU_UFUK) + f" (n {c[h].get('n')})" for h in KU_AVR)
            L.append(f"| {K['kol']} | {'+' if K['yon'] > 0 else '-'} | {_ar(c['ABD|d1619'].get('TF3'))} | {_ar(c['ABD|d2022'].get('TF3'))} | "
                     f"{_ar(c['ABD|d1619'].get('TF5'))} | {_ar(c['ABD|d2022'].get('TF5'))} | "
                     f"{_ar(c['ABD|d1619'].get('ONCE_ASM'), 1)} / {_ar(c['ABD|d2022'].get('ONCE_ASM'), 1)} | "
                     f"{_ar(c['ABD|d1619'].get('TF1'))} / {_ar(c['ABD|d2022'].get('TF1'))} | "
                     f"{_f((c['ABD|d1619'].get('TF15') or {}).get('ort'), 2, True)} / {_f((c['ABD|d2022'].get('TF15') or {}).get('ort'), 2, True)} | "
                     f"{_f(e.get('ABD|d1619'), 2, True)} / {_f(e.get('ABD|d2022'), 2, True)} ({K.get('eski15', {}).get('hukum') or '-'}) | {avr} | {c['ABD|d1619'].get('n')} / {c['ABD|d2022'].get('n')} | "
                     f"**{K['H3']['hukum']}** / **{K['H5']['hukum']}** | {K['H3']['maliyet']['etiket']} / {K['H5']['maliyet']['etiket']} | "
                     f"{_f(K['H3']['bh_q'], 3)} / {_f(K['H5']['bh_q'], 3)} |")
        L.append("")
    L += ["### Hücre ayrıntısı (n / ay / üst3; SEÇİM_H; ÖNCE yönde / ters payı)", "",
          "| kol | hücre | n | ay | üst3 | SEÇİM3 | SEÇİM5 | ÖNCE yönde / ters (%) | R3 medyan | R5 medyan |", "|---|---|---|---|---|---|---|---|---|---|"]
    for kid, K in J["kol"].items():
        for h in KU_HUCRE:
            c = K["hucre"][h]; o = c.get("ONCE") or {}
            L.append(f"| {kid} | {h} | {c.get('n')} | {c.get('ay')} | {_f(c.get('ust3_pay'), 2)} | {_ar(c.get('SEC3'))} | {_ar(c.get('SEC5'))} | "
                     f"{_f(o.get('yonde'), 1, True)} / {_f(o.get('ters'), 1, True)} | {_f(c.get('R3_medyan_yonlu'), 2, True)} | {_f(c.get('R5_medyan_yonlu'), 2, True)} |")
    L += ["", "## KONTROL LİSTESİ", "", "Ön kayıttaki tablo (KU_ON_KAYIT.md) aynen geçerli; ölçüm kapısı geçti: "
          f"{J.get('kapi', {}).get('onkayit_commit', '-')} (uzak {J.get('kapi', {}).get('uzak', '-')}).", "", "## YENİDEN ÜRETİM", ""]
    L += [f"- {x}" for x in (EK.get("yeniden") or ["-"])]
    L += ["", "## HATA", ""] + [f"- {x}" for x in (EK.get("hata") or ["-"])] + ["", "## SAPMA", ""] + [f"- {x}" for x in (EK.get("sapma") or ["-"])]
    L += ["", "## ÖNERİLEN DEFTER SATIRLARI", "", "(ana model işler; alt ajan deftere yazmaz)", ""] + [f"- {x}" for x in (EK.get("defter") or ["-"])]
    return MI._mi_yaz(_ku_yol("rapor", cikti), "\n".join(L) + "\n", "KU_RAPOR")


# ================================================================ 10) ÇAKIŞMA KAPISI + KOMUT
def _cakisma_kontrol_ku(_once=_CK_ONCE_KU, _dosya="KISA_UFUK.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_KU",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_ku()


def _ku_ana(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(__doc__); return 0
    k = argv[0]
    try:
        if k == "dogrula":
            V = ku_dogrula(); print(json.dumps({a: v["tuttu"] for a, v in V["kume"].items()}, ensure_ascii=False))
        elif k == "sayim":
            S = ku_sayim(); print("SAYIM_SHA:", ku_sayim_sha(S))
        elif k == "onkayit":
            print(ku_onkayit_yaz())
        elif k == "olcum":
            J = ku_olcum(); print(J["genel"]); print(json.dumps(J["hukum_say"], ensure_ascii=False))
        elif k == "rapor":
            print(ku_rapor_yaz())
        elif k == "sha":
            print(json.dumps({"kod": ku_kod_sha(), "esik": ku_esik_sha()}))
        else:
            print(__doc__); return 2
    except (KUHata, YO.YOHata, MI.MIHata) as ex:
        kulog.error("DURDU: %s", ex); return 1
    return 0


if __name__ == "__main__":
    sys.exit(_ku_ana())
