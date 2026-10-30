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

from .mekanizma import ETKI_YOK, YONTEM_DENETIMI, bulgu_hipotezleri
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


def k55_otomatik(A: K56Ayar, kk: KaynakKaydi, Z: Optional[pd.DataFrame], kur: pd.DataFrame) -> pd.DataFrame:
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
                     "m01_d_sentetik_Y60": (float(z.d_sent_Y60) if z is not None else np.nan), "m01_gecikme5": (float(z.d_sent_gecikme5) if z is not None else np.nan), "kaynak": "otomatik + kürasyon (açıklamalar)"})
    return pd.DataFrame(rows)


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
    rows = []; env = {_norm(k): k for k in E.kimlik}
    for nk, v in kod.items():
        hit = next((env[e] for e in env if e == nk or e.startswith(nk)), None)
        if hit is None:
            rows.append({"tur": "envanterde_yok", "kimlik": v["kod"], "kaynak": v["dosya"], "ayrinti": f"kaynak karar: {v['karar']}"})
            continue
        ek = str(E.loc[E.kimlik == hit, "eski_karar"].iloc[0])
        if v["dosya"] in ("cy_hipotez.csv", "cy_b_hipotez.csv") and v["karar"] and _norm(v["karar"])[:12] not in _norm(ek):
            rows.append({"tur": "karar_uyusmuyor", "kimlik": hit, "kaynak": v["dosya"], "ayrinti": f"kaynak '{v['karar']}' / envanter '{ek[:120]}'"})
    n55 = int((E.kaynak_calisma == "K55").sum() - E.kimlik.str.startswith("K55-F0").sum())
    if n55 != 63:
        rows.append({"tur": "k55_hucre_sayisi", "kimlik": "K55", "kaynak": "K55_HUCRE_SONUC.csv", "ayrinti": f"{n55} != 63"})
    for a in ("olasi_aciklamalar", "dogrulayici_veri"):
        bos = E[E[a].map(lambda x: not (isinstance(x, list) and len(x)) and not (isinstance(x, str) and x.strip()))]
        for k in bos.kimlik:
            rows.append({"tur": f"bos_{a}", "kimlik": k, "kaynak": "kürasyon", "ayrinti": "açıklama alanı boş"})
    return pd.DataFrame(rows, columns=["tur", "kimlik", "kaynak", "ayrinti"])


# Faz 0 ön sınıf: varsayılan kurallar + bulguya özel (gerekçeli) atamalar. Kesin sınıf Faz 1'de (ONKAYIT_K56 3).
ON_SINIF_OZEL: Dict[str, Tuple[str, str]] = {}


def on_sinif(r: pd.Series) -> Tuple[str, str]:
    if r.kimlik in ON_SINIF_OZEL:
        return ON_SINIF_OZEL[r.kimlik]
    m01 = r.get("m01_sentetik", "")
    if r.kaynak_calisma == "K55" and r.sinif in ("TERS_YONLU", "BASARILI", "KUCUK_ETKI", "VEKIL") and m01 == "MEKANIK_ACIKLAR":
        return ("YANLIŞ BULGU", f"M01 sentetik sıfır sınaması gerçek etkinin {r.m01_oran_Y60:.0%}'ini dört yapay evrende yeniden üretiyor (ONKAYIT_K56 3-1a); "
                "kesinleşmesi için gerçek veride gecikme sınaması (Faz 1, M01)")
    if r.kaynak_calisma == "K55" and r.sinif in ("TERS_YONLU", "BASARILI", "KUCUK_ETKI", "VEKIL") and m01 == "BELIRSIZ":
        return ("İLİŞKİ VAR, NEDEN BELİRSİZ", "M01 yalnız GARCH'lı yapay evrende mekanik; M03 (oynaklık seçimi) ile ayrıştırılacak")
    if r.sinif in ("BASARISIZ",):
        return (ETKI_YOK, "kaynak kararı başarısız; sonradan başarılı sayılmaz")
    if r.sinif == "VERI_YETERSIZ":
        return ("VERİ YETERSİZ", "kaynakta ölçülemedi / n yetersiz")
    if r.sinif == "VEKIL":
        return ("ALTERNATİF AÇIKLAMA", "bilinen ölçünün vekili (|ρ| > 0,8 ya da kaynakta vekil işareti); bağımsız bilgi iddiası yok")
    if r.sinif == "DONEM_CELISKILI":
        return ("İLİŞKİ VAR, NEDEN BELİRSİZ", "dönemler arası işaret / karar çelişkisi: iz sayılmaz (CLAUDE.md); mekanizma testi yalnız tutarlı alt kümede")
    return ("İLİŞKİ VAR, NEDEN BELİRSİZ", "etki kaynakta var ama mekanizma sınanmadı")


def envanter_kur(A: K56Ayar, kk: KaynakKaydi, Z: Optional[pd.DataFrame], yol: str = KURASYON) -> Tuple[pd.DataFrame, pd.DataFrame]:
    kk.oku(yol, "envanter", "K56 envanter kürasyonu (okuyucu ajanlar + denetim)")
    kur = kurasyon_yukle(yol); k55 = k55_otomatik(A, kk, Z, kur)
    diger = kur[~kur.kimlik.str.match(r"^K55-D\d\d-S\d\d$")].copy(); diger["kaynak"] = "kürasyon"
    E = pd.concat([diger, k55], ignore_index=True, sort=False)
    E["mekanizma_hipotezleri"] = E.kimlik.map(lambda k: "; ".join(bulgu_hipotezleri(k)))
    s = E.apply(on_sinif, axis=1); E["faz0_on_sinif"] = [a for a, _ in s]; E["faz0_gerekce"] = [b for _, b in s]
    for c in ("olasi_aciklamalar", "dogrulayici_veri"):
        E[c] = E[c].map(lambda x: " | ".join(x) if isinstance(x, list) else ("" if (x is None or (isinstance(x, float) and np.isnan(x))) else str(x)))
    E = E.sort_values(["kaynak_calisma", "kimlik"], kind="stable").reset_index(drop=True)
    return E, denetle(E, kaynak_kodlari(A, kk))


def aciklanmamislar(E: pd.DataFrame) -> pd.DataFrame:
    """Etkisi olan (başarısız ya da yöntem denetimi olmayan) bütün bulgular ve Faz 0 açıklama durumu: AÇIKLANMADI (neden belirsiz / veri
    yetersiz) ya da ADAY AÇIKLAMA (M01 mekanik eser adayı ya da vekil; Faz 1 doğrulaması bekliyor). Hiçbiri 'açıklandı' sayılmaz."""
    m = ~E.faz0_on_sinif.isin([ETKI_YOK, YONTEM_DENETIMI])
    T = E.loc[m].copy()
    T["faz0_durum"] = np.where(T.faz0_on_sinif.isin(["YANLIŞ BULGU", "ALTERNATİF AÇIKLAMA"]), "ADAY AÇIKLAMA (Faz 1 doğrulaması bekliyor)", "AÇIKLANMADI")
    kol = ["kimlik", "kaynak_calisma", "ad", "sinif", "yon", "buyukluk", "faz0_durum", "faz0_on_sinif", "faz0_gerekce", "mekanizma_hipotezleri", "olasi_aciklamalar", "dogrulayici_veri"]
    return T[[c for c in kol if c in T]].sort_values(["faz0_durum", "kaynak_calisma", "kimlik"]).reset_index(drop=True)
