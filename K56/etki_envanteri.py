"""K56 etki envanteri: K51-K55'in BÜTÜN bulguları (başarılı, başarısız, ters, vekil, küçük etkili, veri yetersiz) tek tabloda, 10 alanla.

Kaynaklar: (1) K55 hücreleri OTOMATİK (K55_HUCRE_SONUC + K55_VEKIL + K55 dal modüllerindeki yön; sayılar CSV'den, elle aktarım yok);
(2) K51-K54 bulguları K56/envanter_kaynak.json kürasyonundan (okuyucu ajanlarının kaynak dosyalardan çıkardığı, sonra mekanik denetlenen kayıt);
(3) M01 sentetik sınama sonucu (K55 hücreleri). Mekanik denetim: kürasyondaki eski kararlar kaynak CSV'lerdeki kararla karşılaştırılır,
kaynaktaki her hipotez kodunun envanterde olduğu doğrulanır; uyuşmazlık K56_ENVANTER_DENETIMI.csv'ye yazılır (sessiz düzeltme yok).
Faz 0 ön sınıfı kesin değildir; kesin sınıf Faz 1 testleriyle (ONKAYIT_K56 3).
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .mekanizma import BETIMLEYICI, ETKI_SAGLAM_DEGIL, ETKI_YOK, YANLIS_ADAY, YONTEM_DENETIMI, bulgu_hipotezleri
from .ortak import KOK, K56Ayar, KaynakKaydi

KURASYON = os.path.join(KOK, "K56", "envanter_kaynak.json")
ALANLAR = ["kimlik", "ad", "kaynak_calisma", "kaynak_dosya", "veri_donem", "olculen", "yon", "buyukluk", "kontrol_farki", "gecen_testler", "kalan_testler",
           "eski_karar", "sinif", "sinirlamalar", "olasi_aciklamalar", "dogrulayici_veri", "aciklanmis", "aciklanma_gerekcesi"]


def _norm(s: Any) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z0-9]+", "", s)


def kurasyon_yukle(yol: str = KURASYON) -> pd.DataFrame:
    if not os.path.exists(yol):
        raise FileNotFoundError(f"envanter kürasyonu yok: {yol}")
    J = json.load(open(yol, encoding="utf-8")); T = pd.DataFrame(J["bulgular"])
    eksik = [a for a in ALANLAR if a not in T]
    if eksik:
        raise ValueError(f"kürasyonda alan eksik: {eksik}")
    if T.kimlik.duplicated().any():
        raise ValueError(f"kürasyonda yinelenen kimlik: {sorted(T.kimlik[T.kimlik.duplicated()])[:10]}")
    return T


def k55_otomatik(A: K56Ayar, kk: KaynakKaydi, Z: Optional[pd.DataFrame], kur: pd.DataFrame, Zk: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """K55'in 63 hücresi: sayılar ve durum CSV'den; varsayılan yön kayıttan; vekil ve sentetik sonucu eklenir. Açıklama alanları kürasyondan
    (aynı kimlikle varsa) alınır, yoksa boş kalır ve denetimde işaretlenir."""
    from K55.faz1 import hucreleri_kur
    from K55.hucreler import HUCRELER
    hucreleri_kur()
    D = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_HUCRE_SONUC.csv"), "envanter", "K55 hücre durumları"))
    V = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_VEKIL.csv"), "envanter", "K55 vekil kıyası")).set_index("hucre")
    kmap = kur.set_index("kimlik") if len(kur) else pd.DataFrame()
    rows = []
    for r in D.itertuples():
        t = HUCRELER.get(r.hucre, {}); yon = t.get("yon", np.nan); kim = f"K55-{r.hucre}"
        ters = r.durum == "KEŞİF" and np.isfinite(r.A_d) and np.sign(r.A_d) != yon
        sinif = {"KEŞİF": "TERS_YONLU" if ters else ("KUCUK_ETKI" if abs(r.A_d) < 0.2 else "BASARILI"), "REDDEDİLDİ": "BASARISIZ", "VERİ YETERSİZ": "VERI_YETERSIZ"}.get(r.durum, "BASARISIZ")
        if r.hucre in V.index and bool(V.loc[r.hucre, "vekil"]):
            sinif = "VEKIL"
        vk = (f"; vekil kıyası: en yakın {V.loc[r.hucre, 'en_yakin_bilinen']} ρ {V.loc[r.hucre, 'en_yakin_rho']:+.2f}, dd250 katmanlı d {V.loc[r.hucre, 'A_dd250_katmanli_d']:+.3f}"
              if r.hucre in V.index else "")
        z = Z[Z.hucre == r.hucre].iloc[0] if (Z is not None and len(Z) and (Z.hucre == r.hucre).any()) else None
        k = kmap.loc[kim] if kim in getattr(kmap, "index", []) else None
        def kf(a, varsayilan=""):
            return k[a] if (k is not None and a in k and isinstance(k[a], (str, list)) and len(k[a])) else varsayilan
        rows.append({"kimlik": kim, "ad": f"{r.hucre}: {r.soru}", "kaynak_calisma": "K55", "kaynak_dosya": "arastirma_cikti/k55_dallanma/tam_evren/K55_HUCRE_SONUC.csv, K55_VARYANTLAR.csv, K55_VEKIL.csv; K55/dal*.py",
                     "veri_donem": "ABD 3.260 hisse (K55 evren v1.3), KEŞİF 2016-21, likit satırlar; olay Y60 / Y120 / Y250", "olculen": f"{r.soru} (varsayılan yön {'+' if yon == 1 else '−'})",
                     "yon": "ters" if ters else ("sifir" if r.durum != "KEŞİF" else ("pozitif" if r.A_d > 0 else "negatif")),
                     "buyukluk": f"A en iyi {r.A_en_iyi}: d {r.A_d:+.3f}, AUC {r.A_auc:.3f}, q {r.A_q:.3f}; C lift en çok {r.C_lift_max:.2f}" + vk,
                     "kontrol_farki": f"A: aynı gün × oynaklık ondalığı içinde olay olmayan satırlar; B eşleşmiş ileri (5 eş) {r.B_en_iyi}: fark {r.B_fark:+.4f} [alt {r.B_fark_alt:+.4f}], q {r.B_q:.3f}",
                     "gecen_testler": "A (ETKİ + FDR + yıl tekrarı + rejim)" if r.durum == "KEŞİF" else "-", "kalan_testler": "B ileri getiri TUTMAZ (bütün varyantlar)" + ("" if r.durum == "KEŞİF" else "; A etkisi yok ya da eşik altı"),
                     "eski_karar": f"K55 Faz 1: {r.durum}" + (f" (eksik pay {r.eksik_pay_max:.2f})" if r.durum == "VERİ YETERSİZ" else ""), "sinif": sinif,
                     "sinirlamalar": kf("sinirlamalar", "yalnız OHLCV; olay tanımı ileri pencereye bağlı (seçim etkisi); KEŞİF dışı açılmadı; hayatta kalan ağırlıklı evren"),
                     "olasi_aciklamalar": kf("olasi_aciklamalar", []), "dogrulayici_veri": kf("dogrulayici_veri", []), "aciklanmis": kf("aciklanmis", "hayir"), "aciklanma_gerekcesi": kf("aciklanma_gerekcesi", ""),
                     "m01_sentetik": (z.karar if z is not None else ""), "m01_oran_Y60": (float(z.oran_Y60) if z is not None else np.nan),
                     "m01_d_sentetik_Y60": (float(z.d_sent_Y60) if z is not None else np.nan), "m01_gecikme5": (float(z.d_sent_gecikme5) if z is not None else np.nan),
                     "m01_spek": (z.spek_siniflari if z is not None else ""), "m01_kesif_karar": _kesif_karar(Zk, r.hucre), "kaynak": "otomatik + kürasyon (açıklamalar)"})
    n_k = int((D.durum == "KEŞİF").sum()); n_r = int((D.durum == "REDDEDİLDİ").sum()); n_v = int((D.durum == "VERİ YETERSİZ").sum())
    rows.append({"kimlik": "K55-SONUC", "ad": "K55 Faz 1 genel karar (63 OHLCV hücresi, KEŞİF 2016-21)", "kaynak_calisma": "K55", "kaynak_dosya": "arastirma_cikti/k55_dallanma/tam_evren/K55_FAZ1_RAPOR.md",
                 "veri_donem": "ABD 3.260 hisse, KEŞİF 2016-21", "olculen": "63 hücre, A / B / C yöntemleri", "yon": "sifir", "buyukluk": f"KEŞİF {n_k}, REDDEDİLDİ {n_r}, VERİ YETERSİZ {n_v}; B 0 / 164 TUTMAZ",
                 "kontrol_farki": "B eşleşmiş ileri 60 gün: en büyük fark +0,010 (eşik +0,05)", "gecen_testler": "-", "kalan_testler": "B (ileri getiri) hiçbir varyantta", "eski_karar": "Faz 1'de İZ YOK",
                 "sinif": "BASARISIZ", "sinirlamalar": "yalnız KEŞİF; İÇ / BAĞIMSIZ açılmadı", "olasi_aciklamalar": ["OHLCV ölçüleri ileri getiri taşımıyor", "A farkları olay tanımı eseri (M01)"],
                 "dogrulayici_veri": ["v1.1-2 seçimsiz kontrol"], "aciklanmis": "kismen", "aciklanma_gerekcesi": "İZ YOK kararı değişmez", "kaynak": "otomatik"})
    return pd.DataFrame(rows)


def _kesif_karar(Zk: Optional[pd.DataFrame], hucre: str) -> str:
    """v1.1-3: KEŞİF'i sağlayan (varyant, ufuk) satırlarındaki sentetik kararların özeti (ör. 'MEKANIK_ACIKLAR 3/4')."""
    if Zk is None or not len(Zk) or not (Zk.hucre == hucre).any():
        return ""
    v = Zk[Zk.hucre == hucre].karar.value_counts(); return f"{v.index[0]} {int(v.iloc[0])}/{int(v.sum())}"


def kaynak_kodlari(A: K56Ayar, kk: KaynakKaydi) -> Dict[str, Dict[str, str]]:
    """Kaynak CSV'lerdeki hipotez / test kodları ve kararları: {beklenen envanter kimliği (normalize): {kod, karar, dosya}}."""
    out: Dict[str, Dict[str, str]] = {}
    def ekle(on: str, dosya: str, kodkol: str, kararkol: str, aciklama: str) -> None:
        T = pd.read_csv(kk.oku(os.path.join(A.abd, dosya), "envanter", aciklama))
        for kod, g in T.groupby(kodkol, sort=False):
            out[_norm(on + str(kod))] = {"kod": str(kod), "karar": " / ".join(sorted(set(str(x) for x in g[kararkol].dropna()))), "dosya": dosya}
    ekle("K51-", "cy_hipotez.csv", "kod", "karar", "K51 H hipotez kararları")
    ekle("K51-", "cy_b_hipotez.csv", "kod", "karar", "K51 v1.1 B hipotez kararları")
    ekle("K51v12-", "K51_HIPOTEZ_KARARLARI.csv", "hipotez", "karar_hucre", "K51 v1.2 H-A..H-E")
    ekle("K52-", "K51_ANALIST_EK_KATKI_TESTI.csv", "kod", "karar_hucre", "K52 analist ek katkı")
    ekle("K53-", "K53_HIPOTEZ_TESTI.csv", "kod", "karar_hucre", "K53 hipotez testleri")
    return out


def denetle(E: pd.DataFrame, kod: Dict[str, Dict[str, str]]) -> pd.DataFrame:
    """(a) kaynakta olup envanterde olmayan kod, (b) envanter kararının kaynak kararla uyuşmaması (K51 H / B: karar metni içerilmeli),
    (c) K55 hücre sayısı 63, (d) zorunlu alan boşlukları. Uyuşmazlık düzeltilmez, raporlanır."""
    rows = []; env = {_norm(k): k for k in E.kimlik}; alias = {_norm(k): [_norm(x) for x in v] for k, v in KOD_ESLEME.items()}
    for nk, v in kod.items():
        hit = env.get(nk)
        if hit is None and nk in alias:
            hit = next((env[a] for a in alias[nk] if a in env), None)
        if hit is None:
            ad = sorted((e for e in env if e.startswith(nk)), key=len)
            hit = env[ad[0]] if ad else None
        if hit is None:
            ad = sorted((e for e in env if len(e) >= 10 and nk.startswith(e)), key=len, reverse=True)
            hit = env[ad[0]] if ad else None
        if hit is None:
            rows.append({"tur": "envanterde_yok", "kimlik": v["kod"], "kaynak": v["dosya"], "ayrinti": f"kaynak karar: {v['karar']}"})
            continue
        ek = str(E.loc[E.kimlik == hit, "eski_karar"].iloc[0]); nek = _norm(ek)
        if v["dosya"] in ("cy_hipotez.csv", "cy_b_hipotez.csv") and v["karar"] and _norm(v["karar"])[:12] not in nek:
            rows.append({"tur": "karar_uyusmuyor", "kimlik": hit, "kaynak": v["dosya"], "ayrinti": f"kaynak '{v['karar']}' / envanter '{ek[:120]}'"})
        elif v["dosya"] not in ("cy_hipotez.csv", "cy_b_hipotez.csv") and v["karar"]:
            eksik = [t for t in (x.strip() for x in v["karar"].split("/")) if t and t.lower() != "nan" and _norm(t) not in nek]
            if eksik:
                rows.append({"tur": "karar_eksik_sozcuk", "kimlik": hit, "kaynak": v["dosya"], "ayrinti": f"kaynak kararları {v['karar']}; envanterde geçmeyen: {eksik}"})
    n55 = int(E.kimlik.str.match(r"^K55-D\d\d-S\d\d$").sum())
    if n55 != 63:
        rows.append({"tur": "k55_hucre_sayisi", "kimlik": "K55", "kaynak": "K55_HUCRE_SONUC.csv", "ayrinti": f"{n55} != 63"})
    for a in ("olasi_aciklamalar", "dogrulayici_veri"):
        bos = E[E[a].map(lambda x: not (isinstance(x, list) and len(x)) and not (isinstance(x, str) and x.strip()))]
        for k in bos.kimlik:
            rows.append({"tur": f"bos_{a}", "kimlik": k, "kaynak": "kürasyon", "ayrinti": "açıklama alanı boş"})
    return pd.DataFrame(rows, columns=["tur", "kimlik", "kaynak", "ayrinti"])


# Faz 0 ön sınıf: varsayılan kurallar + bulguya özel (gerekçeli) atamalar. Kesin sınıf Faz 1'de (ONKAYIT_K56 3).
_YD = "ölçüm hattı / veri / evren denetimi; etki iddiası değil (M13 / M17 kanıtı olarak kullanılır)"
ON_SINIF_OZEL: Dict[str, Tuple[str, str]] = {
    **{k: (YONTEM_DENETIMI, "K51 B7 olumlu / olumsuz / plasebo kontrolü: ölçüm hattının çalıştığını gösterir") for k in ("K51-B7-negatif", "K51-B7-pozitif", "K51-B7-plasebo")},
    **{k: (YONTEM_DENETIMI, _YD) for k in ("K51-V1", "K51-V5", "K51-V6", "K51-V7", "K51-V8", "K54-S1", "K54-S1-OTC", "K54-S1-BELIRSIZ", "K54-S2", "K54-S2-KRONO", "K54-S3",
                                           "K54-S4A", "K54-S4B", "K54-S5", "K54-S6", "K54-ETF", "K54-K51TAHMIN", "K54-DL-P1", "K54-DL-P2", "K54-DL4A-P1", "K54-DL4A-P2",
                                           "K54-EVREN-ETKI", "K54-ETIKET-ETKI", "K54-ANALIST", "K53-EK-DENGE")},
    **{k: (YONTEM_DENETIMI, "K55 Faz 0 evren / veri kalitesi / sızıntı denetimi; etki iddiası değil") for k in ("K55-F0-EVREN", "K55-F0-KALITE", "K55-F0-SIZINTI")},
    "K51-P2-SUREN": (YONTEM_DENETIMI, "gelecek bilgisiyle ayrılmış gruplar (süren / başarısız kırılım): öngörü iddiası yok, tanım gereği fark"),
    "K51-H9": ("VERİ YETERSİZ", "kaynakta ÖLÇÜLEMEDİ (batanlar eksik); hayatta kalma Faz 1'de M17 ile (Tiingo kotası)"),
    "K54-HAYATTA-KALMA": ("VERİ YETERSİZ", "evrende hiç olmayan batanlar ölçülemiyor (K54)"),
    **{k: (YONTEM_DENETIMI, "sonuca göre seçilmiş alt küme ('en iyi 20 hisse' sonuç değişkenine göre çıkarıldı): fark mekanik olarak eksiye kayar; kırılganlık denetimi")
       for k in ("K54-K51P1-E20", "K54-K51P2-E20", "K54-K51ES-E20", "K54-K51HT-E20", "K54-K51CEK-E20", "K52-KIR-EN20-P1", "K52-KIR-EN20-P2")},
    "K53-T7": (YANLIS_ADAY + " (tanımsal)", "BDS 'fiyat zayıf' ile KGS 'hızlı' aynı pencereyi (d0−1..d0+4) kullanıyor: örüntü tanımdan doğar (ONKAYIT_K56 v1.1-1)"),
    "K52-H4Z-P2": ("ALTERNATİF AÇIKLAMA", "olumlu revizyonların yarısı fiyat yükseldikten sonra (M19 ile uyumlu) ama M04 (haber) ile ayrıştırılmadı; karşıt grup / aracılık yok"),
}
# kaynak kodu -> envanterde farklı adla bölünmüş kimlikler (ör. rejime göre ikiye ayrılan K52 H6)
KOD_ESLEME: Dict[str, List[str]] = {"K52-H6-P1": ["K52-H6AYI-P1", "K52-H6BOGA-P1"], "K52-H6-P2": ["K52-H6AYI-P2", "K52-H6BOGA-P2"]}


_BASARISIZ_SOZ = ("DESTEKLENMIYOR", "TUTMAZ", "IZDEGIL", "TERSYON", "OLCULEMEDI", "GECERSIZ", "IZYOK")


def on_sinif(r: pd.Series) -> Tuple[str, str]:
    """Faz 0 ön sınıfı (ONKAYIT_K56 v1.1-4): bulguya özel gerekçeli atama, yoksa mekanik kural."""
    if r.kimlik in ON_SINIF_OZEL:
        return ON_SINIF_OZEL[r.kimlik]
    etkili = r.get("sinif") in ("TERS_YONLU", "BASARILI", "KUCUK_ETKI", "VEKIL", "DONEM_CELISKILI")
    if r.get("sinif") == "BASARISIZ":
        return (ETKI_YOK, "kaynak kararı başarısız; sonradan başarılı sayılmaz")
    if r.get("sinif") == "VERI_YETERSIZ":
        return ("VERİ YETERSİZ", "kaynakta ölçülemedi / n yetersiz")
    if r.kaynak_calisma == "K55" and str(r.kimlik).startswith("K55-D") and etkili:
        m01 = r.get("m01_sentetik", ""); ku = r.get("m01_kesif_karar", "")
        if m01 == "MEKANIK_ACIKLAR":
            return (YANLIS_ADAY + " (M01)", f"Y60'ta sentetik / gerçek d oranı {r.m01_oran_Y60:.2f}, dört spek {r.get('m01_spek', '')}; KEŞİF ufkunda: {ku or 'koşulmadı'}"
                    + ("; ayrıca r20 vekili (|ρ| > 0,8)" if r.sinif == "VEKIL" else "") + "; kesinleşmesi v1.1-2 seçimsiz kontrolle (Faz 1)")
        if m01 == "BELIRSIZ":
            return ("İLİŞKİ VAR, NEDEN BELİRSİZ", f"M01 sentetik Y60 dört spek: {r.get('m01_spek', '')} (çoğunluk yok); KEŞİF ufkunda: {ku or 'koşulmadı'}; M03 / M01 Faz 1'de")
        if r.sinif == "VEKIL":
            return ("ALTERNATİF AÇIKLAMA", "hesaplanmış vekil (|ρ| > 0,8)")
        return ("İLİŞKİ VAR, NEDEN BELİRSİZ", f"M01 sentetik {m01 or 'yok'}")
    karar = _norm(r.get("eski_karar", ""))
    if "DESTEKLENIYOR" in karar or "KESIF" in karar:
        return ("İLİŞKİ VAR, NEDEN BELİRSİZ", "kaynak kararı destekleniyor; mekanizma sınanmadı")
    if any(t in karar for t in _BASARISIZ_SOZ):
        return (ETKI_SAGLAM_DEGIL, "kaynak kararı başarısız / tutmaz; küçük, ters ya da dönem çelişkili etki iz sayılmaz (CLAUDE.md, ONKAYIT_K56 v1.1-4)")
    return (BETIMLEYICI, "kaynakta karar yok (bilgi / denetçi notu); etki iddiası değil")


def envanter_kur(A: K56Ayar, kk: KaynakKaydi, Z: Optional[pd.DataFrame], yol: str = KURASYON, Zk: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    kk.oku(yol, "envanter", "K56 envanter kürasyonu (okuyucu ajanlar + denetim)")
    kur = kurasyon_yukle(yol); k55 = k55_otomatik(A, kk, Z, kur, Zk)
    diger = kur[~kur.kimlik.str.match(r"^K55-D\d\d-S\d\d$")].copy(); diger["kaynak"] = "kürasyon"
    E = pd.concat([diger, k55], ignore_index=True, sort=False)
    E["mekanizma_hipotezleri"] = E.kimlik.map(lambda k: "; ".join(bulgu_hipotezleri(k)))
    s = E.apply(on_sinif, axis=1); E["faz0_on_sinif"] = [a for a, _ in s]; E["faz0_gerekce"] = [b for _, b in s]
    for c in ("olasi_aciklamalar", "dogrulayici_veri"):
        E[c] = E[c].map(lambda x: " | ".join(x) if isinstance(x, list) else ("" if (x is None or (isinstance(x, float) and np.isnan(x))) else str(x)))
    E = E.sort_values(["kaynak_calisma", "kimlik"], kind="stable").reset_index(drop=True)
    Den = denetle(E, kaynak_kodlari(A, kk))
    # K55: okuyucu ajanın sınıfı otomatik kuraldan farklıysa kural geçerli (REDDEDİLDİ hücre BAŞARISIZ kalır; vekil yalnız |ρ| > 0,8), fark kayda geçer
    ka = kur.set_index("kimlik").sinif if len(kur) else pd.Series(dtype=str); ko = k55.set_index("kimlik").sinif
    fark = [{"tur": "k55_sinif_kurali", "kimlik": k, "kaynak": "K55_HUCRE_SONUC + K55_VEKIL", "ayrinti": f"okuyucu {ka[k]} -> kural {ko[k]}"} for k in ko.index if k in ka.index and ka[k] != ko[k]]
    for d in json.load(open(yol, encoding="utf-8")).get("duzeltmeler", []):
        fark.append({"tur": "kurasyon_duzeltmesi", "kimlik": d["kimlik"], "kaynak": d.get("kaynak", ""), "ayrinti": f"{d['alan']}: {d['gerekce']}"})
    return E, pd.concat([Den, pd.DataFrame(fark, columns=Den.columns)], ignore_index=True)


def aciklanmamislar(E: pd.DataFrame) -> pd.DataFrame:
    """Faz 0 açıklama durumu (hiçbiri 'açıklandı' sayılmaz): AÇIKLANMADI (İLİŞKİ VAR, NEDEN BELİRSİZ: gerçek, mekanizması bilinmeyen etki),
    ADAY AÇIKLAMA (YANLIŞ BULGU ADAYI / ALTERNATİF AÇIKLAMA: Faz 1 doğrulaması bekliyor), VERİ YETERSİZ (ölçülemedi), BETİMLEYİCİ (karar yok).
    ETKİ YOK, ETKİ SAĞLAM DEĞİL ve YÖNTEM DENETİMİ listede yok (mekanizma aranmaz)."""
    dur = {"İLİŞKİ VAR, NEDEN BELİRSİZ": "AÇIKLANMADI", "ALTERNATİF AÇIKLAMA": "ADAY AÇIKLAMA (Faz 1 doğrulaması bekliyor)", "VERİ YETERSİZ": "VERİ YETERSİZ (ölçülemedi)", BETIMLEYICI: "BETİMLEYİCİ (karar yok)"}
    T = E.copy(); T["faz0_durum"] = T.faz0_on_sinif.map(lambda x: "ADAY AÇIKLAMA (Faz 1 doğrulaması bekliyor)" if str(x).startswith(YANLIS_ADAY) else dur.get(x))
    T = T[T.faz0_durum.notna()]
    kol = ["kimlik", "kaynak_calisma", "ad", "sinif", "yon", "buyukluk", "faz0_durum", "faz0_on_sinif", "faz0_gerekce", "mekanizma_hipotezleri", "olasi_aciklamalar", "dogrulayici_veri"]
    return T[[c for c in kol if c in T]].sort_values(["faz0_durum", "kaynak_calisma", "kimlik"]).reset_index(drop=True)
