"""K56 sürücüleri: sentetik (M01), faz0 (raporlar), erisim (küçük örneklem). Her koşu: kimlik (commit, kilit sha, kod sha), kaynak kaydı, çıktı yolu denetimi."""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import time
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from .ortak import K56Ayar, KaynakKaydi, cikti_dogrula, gunluk_log, kosu_kimligi, log


def _json_yaz(yol: str, veri: Any) -> None:
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=1, default=str)


def _spek_isci(arg):
    spek, hucreler, A = arg
    from . import mekanizma as M
    kk = KaynakKaydi(); S, _ = M.secim_sentetik(A, kk, hucreler, spekler=(spek,)); return S


def sentetik_kos(A: K56Ayar, isci: int = 4, hucreler: Optional[List[str]] = None) -> Dict[str, Any]:
    from . import mekanizma as M
    gunluk_log(); A.cikti = cikti_dogrula(A.cikti); os.makedirs(A.cikti, exist_ok=True); t0 = time.time()
    kimlik = kosu_kimligi(A, "SENTETIK"); kk = KaynakKaydi()
    from K55.faz1 import hucreleri_kur
    hucreleri_kur(); T = M.k55_hucre_varyantlari(A, kk)
    if hucreler:
        T = T[T.hucre.isin(hucreler)].reset_index(drop=True)
    log.info("M01 sentetik: %d hücre × %d spek; kimlik %s", len(T), len(M.SENTETIK_SPEK), kimlik["kimlik"])
    args = [(s, list(T.hucre), A) for s in M.SENTETIK_SPEK]
    if isci > 1:
        with mp.get_context("fork").Pool(min(isci, len(args))) as hv:
            parca = hv.map(_spek_isci, args, chunksize=1)
    else:
        parca = [_spek_isci(a) for a in args]
    S = pd.concat(parca, ignore_index=True); Z = M.sentetik_ozet(S, T)
    S.to_csv(os.path.join(A.cikti, "K56_SECIM_SENTETIK.csv"), index=False); Z.to_csv(os.path.join(A.cikti, "K56_SECIM_SENTETIK_OZET.csv"), index=False)
    kk.tablo().to_csv(os.path.join(A.cikti, "K56_KAYNAK_KAYDI_SENTETIK.csv"), index=False)
    _json_yaz(os.path.join(A.cikti, "K56_KOSU_SENTETIK.json"), {**kimlik, "sure_dk": round((time.time() - t0) / 60, 1), "hucre": len(T), "spek": M.SENTETIK_SPEK,
                                                                 "karar": Z.karar.value_counts().to_dict() if len(Z) else {}})
    log.info("M01 sentetik bitti: %.1f dk; karar %s", (time.time() - t0) / 60, Z.karar.value_counts().to_dict() if len(Z) else {})
    return {"S": S, "Z": Z, "kimlik": kimlik}


def sentetik_birlestir(A: K56Ayar, ana: str, ekler: List[str]) -> pd.DataFrame:
    """Ana sentetik koşu + yalnız belirli hücreler için yeniden koşulan ekler (ör. v1.0-a D02-S10 düzeltmesi): ekteki hücrelerin satırları
    anadakilerin yerine geçer. Kimlik dosyaları birlikte saklanır. Çıktı A.cikti'ye."""
    A.cikti = cikti_dogrula(A.cikti); os.makedirs(A.cikti, exist_ok=True)
    S = pd.read_csv(os.path.join(ana, "K56_SECIM_SENTETIK.csv")); Z = pd.read_csv(os.path.join(ana, "K56_SECIM_SENTETIK_OZET.csv"))
    kim = [json.load(open(os.path.join(ana, "K56_KOSU_SENTETIK.json"), encoding="utf-8"))]
    for e in ekler:
        Se = pd.read_csv(os.path.join(e, "K56_SECIM_SENTETIK.csv")); Ze = pd.read_csv(os.path.join(e, "K56_SECIM_SENTETIK_OZET.csv")); h = set(Ze.hucre)
        S = pd.concat([S[~S.hucre.isin(h)], Se], ignore_index=True); Z = pd.concat([Z[~Z.hucre.isin(h)], Ze], ignore_index=True)
        kim.append(json.load(open(os.path.join(e, "K56_KOSU_SENTETIK.json"), encoding="utf-8")))
    Z = Z.sort_values("hucre").reset_index(drop=True)
    S.to_csv(os.path.join(A.cikti, "K56_SECIM_SENTETIK.csv"), index=False); Z.to_csv(os.path.join(A.cikti, "K56_SECIM_SENTETIK_OZET.csv"), index=False)
    kay = [pd.read_csv(os.path.join(d, "K56_KAYNAK_KAYDI_SENTETIK.csv")) for d in [ana] + ekler if os.path.exists(os.path.join(d, "K56_KAYNAK_KAYDI_SENTETIK.csv"))]
    if kay:
        pd.concat(kay, ignore_index=True).drop_duplicates().to_csv(os.path.join(A.cikti, "K56_KAYNAK_KAYDI_SENTETIK.csv"), index=False)
    _json_yaz(os.path.join(A.cikti, "K56_KOSU_SENTETIK.json"), {"birlesik": True, "kosular": kim, "karar": Z.karar.value_counts().to_dict()})
    return Z


def _kesif_isci(arg):
    spek, V_, A = arg
    from . import mekanizma as M
    kk = KaynakKaydi(); S, _ = M.secim_sentetik(A, kk, spekler=(spek,), varyantlar=V_); return S


def sentetik_kesif_kos(A: K56Ayar, isci: int = 4) -> Dict[str, Any]:
    """ONKAYIT_K56 v1.1-3: KEŞİF'i sağlayan bütün (varyant, ufuk) satırlarında aynı dört spek ve eşiklerle sentetik sınama."""
    from . import mekanizma as M
    gunluk_log(); A.cikti = cikti_dogrula(A.cikti); os.makedirs(A.cikti, exist_ok=True); t0 = time.time()
    kimlik = kosu_kimligi(A, "SENTETIK-KESIF"); kk = KaynakKaydi(); K = M.kesif_satirlari(A, kk)
    log.info("v1.1-3 sentetik: %d KEŞİF satırı, %d varyant × %d spek", len(K), K.varyant.nunique(), len(M.SENTETIK_SPEK))
    args = [(sp, K[["hucre", "varyant"]].drop_duplicates(), A) for sp in M.SENTETIK_SPEK]
    with mp.get_context("fork").Pool(min(isci, len(args))) as hv:
        S = pd.concat(hv.map(_kesif_isci, args, chunksize=1), ignore_index=True)
    Zk = M.sentetik_kesif_ozet(S, K)
    S.to_csv(os.path.join(A.cikti, "K56_SECIM_SENTETIK_KESIF_SATIR.csv"), index=False); Zk.to_csv(os.path.join(A.cikti, "K56_SECIM_SENTETIK_KESIF.csv"), index=False)
    kk.tablo().to_csv(os.path.join(A.cikti, "K56_KAYNAK_KAYDI_SENTETIK_KESIF.csv"), index=False)
    _json_yaz(os.path.join(A.cikti, "K56_KOSU_SENTETIK_KESIF.json"), {**kimlik, "sure_dk": round((time.time() - t0) / 60, 1), "satir": len(K), "karar": Zk.karar.value_counts().to_dict()})
    log.info("v1.1-3 sentetik bitti: %.1f dk; %s", (time.time() - t0) / 60, Zk.karar.value_counts().to_dict())
    return {"S": S, "Zk": Zk}


def faz0_kos(A: K56Ayar) -> Dict[str, Any]:
    """Faz 0 raporları (ağ yok): envanter + denetim, açıklanmamışlar, hipotezler, hipotez × veri, veri kaynakları (+ erişim testi sonucu varsa),
    yöntemler (+ M01 sentetik), riskler, uygulama sırası. Sentetik ve erişim çıktıları A.cikti'de olmalı (önce sentetik / erisim)."""
    from . import etki_envanteri as EE
    from . import mekanizma as M
    from . import mekanizma_raporu as MR
    gunluk_log(); A.cikti = cikti_dogrula(A.cikti); os.makedirs(A.cikti, exist_ok=True); A.ag = False
    kimlik = kosu_kimligi(A, "FAZ0"); kk = KaynakKaydi()
    zy = os.path.join(A.cikti, "K56_SECIM_SENTETIK_OZET.csv"); Z = pd.read_csv(zy) if os.path.exists(zy) else None
    zk = os.path.join(A.cikti, "K56_SECIM_SENTETIK_KESIF.csv"); Zk = pd.read_csv(zk) if os.path.exists(zk) else None
    dn = os.path.join(A.cikti, "K56_DENETIM_BULGULARI.csv"); Dn = pd.read_csv(dn) if os.path.exists(dn) else None
    if Z is None:
        log.warning("M01 sentetik özeti yok (%s): K55 bulgularında sentetik sütunu boş kalır", zy)
    E, Den = EE.envanter_kur(A, kk, Z, Zk=Zk); Ac = EE.aciklanmamislar(E); H = M.hipotez_tablosu()
    ey = os.path.join(A.cikti, "K56_VERI_ERISIM_TESTI.csv"); Er = pd.read_csv(ey) if os.path.exists(ey) else pd.DataFrame()
    VK = MR.veri_kaynaklari(Er); HV = MR.hipotez_veri(H, VK); R = MR.riskler(); Sira = MR.uygulama_sirasi()
    E.to_csv(os.path.join(A.cikti, "K56_ETKI_ENVANTERI.csv"), index=False); Den.to_csv(os.path.join(A.cikti, "K56_ENVANTER_DENETIMI.csv"), index=False)
    Ac.to_csv(os.path.join(A.cikti, "K56_ACIKLANMAMIS_BULGULAR.csv"), index=False); H.to_csv(os.path.join(A.cikti, "K56_HIPOTEZLER.csv"), index=False)
    HV.to_csv(os.path.join(A.cikti, "K56_HIPOTEZ_VERI.csv"), index=False); VK.to_csv(os.path.join(A.cikti, "K56_VERI_KAYNAKLARI.csv"), index=False)
    R.to_csv(os.path.join(A.cikti, "K56_RISKLER.csv"), index=False); Sira.to_csv(os.path.join(A.cikti, "K56_UYGULAMA_SIRASI.csv"), index=False)
    MR.suzgec().to_csv(os.path.join(A.cikti, "K56_TALIMAT_SUZGECI.csv"), index=False)
    kk.tablo().to_csv(os.path.join(A.cikti, "K56_KAYNAK_KAYDI.csv"), index=False)
    yol = MR.faz0_yaz(A.cikti, kimlik, E, Den, Ac, H, HV, VK, Er, Z, R, Sira, Zk, Dn)
    _json_yaz(os.path.join(A.cikti, "K56_KOSU_FAZ0.json"), {**kimlik, "hipotez_sha": __import__("hashlib").sha256(H.to_csv(index=False).encode()).hexdigest(), "envanter": len(E), "denetim_uyusmazlik": len(Den), "aciklanmamis": len(Ac), "hipotez": len(H),
                                                           "on_sinif": E.faz0_on_sinif.value_counts().to_dict()})
    log.info("Faz 0 raporu: %s (envanter %d, denetim %d, açıklanmamış %d)", yol, len(E), len(Den), len(Ac))
    return {"E": E, "Den": Den, "Ac": Ac, "H": H, "VK": VK, "rapor": yol}


def erisim_kos(A: K56Ayar) -> Dict[str, Any]:
    """Küçük örneklem veri erişim testi (ONKAYIT_K56 7): örneklem (karsit_ornekler), beş veri modülü; istek günlüğü (e-posta yok)."""
    from . import finansal_mekanizma, iceriden_islemler, islem_davranisi, karsit_ornekler, kurumsal_olaylar, kurumsal_sahiplik
    from .ortak import Istemci
    gunluk_log(); A.cikti = cikti_dogrula(A.cikti); os.makedirs(A.cikti, exist_ok=True); A.ag = True
    kimlik = kosu_kimligi(A, "ERISIM"); kk = KaynakKaydi(); ist = Istemci(A); Istemci.sec_ua()
    Orn = karsit_ornekler.ornek_sec(A, kk, A.ornek); EV = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_EVREN.csv"), "veri", "evren CIK / işlem tarihleri (eşleşme payı)"))
    satir: List[Dict[str, Any]] = []; tablolar: Dict[str, Any] = {}
    for ad, f in (("kurumsal_sahiplik", lambda: kurumsal_sahiplik.erisim_testi(A, ist, Orn)), ("iceriden_islemler", lambda: iceriden_islemler.erisim_testi(A, ist, Orn, EV)),
                  ("finansal_mekanizma", lambda: finansal_mekanizma.erisim_testi(A, ist, Orn)), ("kurumsal_olaylar", lambda: kurumsal_olaylar.erisim_testi(A, ist, Orn, EV)),
                  ("islem_davranisi", lambda: islem_davranisi.erisim_testi(A, ist, Orn, EV))):
        t0 = time.time()
        try:
            rr = f()
        except Exception as ex:
            rr = [{"modul": ad, "kaynak": "-", "test": "modül", "durum": "BASARISIZ", "olcu": "", "deger": None, "ayrinti": f"{type(ex).__name__}: {ex}", "url": ""}]
        for r in rr:
            if "tablo" in r:
                tablolar[f"{ad}:{r['kaynak']}"] = r.pop("tablo")
            r["sure_sn"] = round(time.time() - t0, 1)
        satir += rr; log.info("erişim %s: %s", ad, pd.Series([r["durum"] for r in rr]).value_counts().to_dict())
    T = pd.DataFrame(satir); T.to_csv(os.path.join(A.cikti, "K56_VERI_ERISIM_TESTI.csv"), index=False)
    Orn.to_csv(os.path.join(A.cikti, "K56_ERISIM_ORNEKLEM.csv"), index=False)
    for k, v in tablolar.items():
        if v:
            pd.DataFrame(v).to_csv(os.path.join(A.cikti, f"K56_ERISIM_{k.split(':')[1]}.csv"), index=False)
    G = pd.DataFrame(ist.gunluk); G["url"] = G.url.str.replace(r"[\w.+-]+@[\w-]+\.[\w.]+", "<e-posta>", regex=True)
    G.to_csv(os.path.join(A.cikti, "K56_ISTEK_GUNLUGU.csv"), index=False); kk.tablo().to_csv(os.path.join(A.cikti, "K56_KAYNAK_KAYDI_ERISIM.csv"), index=False)
    _json_yaz(os.path.join(A.cikti, "K56_KOSU_ERISIM.json"), {**kimlik, "istek": len(G), "indirilen_mb": round(float(pd.to_numeric(G.loc[G.durum.astype(str) != "onbellek", "bayt"], errors="coerce").fillna(0).sum()) / 2 ** 20, 1),
                                                             "onbellekten_mb": round(float(pd.to_numeric(G.loc[G.durum.astype(str) == "onbellek", "bayt"], errors="coerce").fillna(0).sum()) / 2 ** 20, 1),
                                                             "durum": T.durum.value_counts().to_dict()})
    return {"T": T, "Orn": Orn, "G": G}


def drive_kopyala(kaynak: Optional[str] = None, hedef: Optional[str] = None) -> pd.DataFrame:
    """Colab: repodaki K56 çıktılarını (arastirma_cikti/k56_mekanizma) Drive OUTPUT/K56_MEKANIZMA'ya kopyalar; her dosya kopyadan sonra sha256 ile
    doğrulanır (eşit değilse durur). K51-K55 klasörlerine yazmaz (cikti_dogrula)."""
    import shutil
    from .ortak import CIKTI_ALT, DRIVE_OUTPUT, REPO_CIKTI, sha256_dosya
    kaynak = kaynak or REPO_CIKTI; hedef = cikti_dogrula(hedef or os.path.join(DRIVE_OUTPUT, CIKTI_ALT)); os.makedirs(hedef, exist_ok=True); rows = []
    for f in sorted(os.listdir(kaynak)):
        a = os.path.join(kaynak, f)
        if not os.path.isfile(a):
            continue
        b = os.path.join(hedef, f); shutil.copyfile(a, b); sa, sb = sha256_dosya(a), sha256_dosya(b)
        if sa != sb:
            raise RuntimeError(f"kopya bozuk: {f}")
        rows.append({"dosya": f, "bayt": os.path.getsize(b), "sha256": sa})
    M = pd.DataFrame(rows); M.to_csv(os.path.join(hedef, "K56_DRIVE_MANIFEST.csv"), index=False); log.info("Drive'a %d dosya kopyalandı (sha eşit): %s", len(M), hedef)
    return M


# ---------------------------------------------------------------- K56-EVREN2 (ONKAYIT v1.2-C)
def _alt_cikti(A: K56Ayar, alt: str) -> str:
    y = cikti_dogrula(os.path.join(A.cikti, alt)); os.makedirs(y, exist_ok=True); return y


def evren2_aday_kos(A: K56Ayar) -> Dict[str, Any]:
    """Aday listesi (Ö1 + Ö2), SEC başvuru geçmişi, ön sınıflandırma (Tiingo bitişine göre). Tiingo FİYAT isteği yok."""
    from . import batan_evren as BE
    from .ortak import Istemci
    gunluk_log(); A.ag = True; out = _alt_cikti(A, "evren_v2"); kimlik = kosu_kimligi(A, "EVREN2-ADAY"); kk = KaynakKaydi(); ist = Istemci(A); Istemci.sec_ua()
    EV = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_EVREN.csv"), "veri", "K55 evreni (aday dışlama)")); T = BE.tiingo_listesi(A)
    O1 = BE.aday_o1(A, kk, EV, T); n2 = max(0, BE.KOTA_UST - len(O1)); O2, havuz = BE.aday_o2(A, ist, EV, T, n2)
    ADAY = pd.concat([O1, O2], ignore_index=True, sort=False)
    if ADAY.cik.duplicated().any():
        ADAY = ADAY.drop_duplicates("cik")
    onb = os.path.join(A.onbellek, "evren_v2"); os.makedirs(onb, exist_ok=True)
    sec = BE.sec_gecmis(ist, sorted(ADAY.cik.astype(int).unique()), os.path.join(onb, "sec_ozet_v2.json"))
    ct = json.load(open("/tmp/k55/company_tickers.json", encoding="utf-8")); bugun = {v["ticker"].upper().replace(".", "-"): int(v["cik_str"]) for v in ct.values()}
    S = BE.siniflandir(ADAY, sec, T, bugun)
    ADAY.to_csv(os.path.join(out, "K56_EVREN2_ADAY.csv"), index=False); havuz.to_csv(os.path.join(out, "K56_EVREN2_O2_HAVUZ.csv"), index=False)
    S.to_csv(os.path.join(out, "K56_EVREN2_SINIF_ON.csv"), index=False); kk.tablo().to_csv(os.path.join(out, "K56_KAYNAK_KAYDI_EVREN2.csv"), index=False)
    G = pd.DataFrame(ist.gunluk); G["url"] = G.url.str.replace(r"[\w.+-]+@[\w-]+\.[\w.]+", "<e-posta>", regex=True); G.to_csv(os.path.join(out, "K56_EVREN2_ISTEK_GUNLUGU.csv"), index=False)
    _json_yaz(os.path.join(out, "K56_KOSU_EVREN2_ADAY.json"), {**kimlik, "o1": len(O1), "o2": len(O2), "o2_havuz": len(havuz), "aday": len(ADAY), "sec_var": int(S.sec_var.sum()),
                                                              "sinif_on": S.sinif_k56.value_counts().to_dict()})
    log.info("evren v2 adaylar: Ö1 %d, Ö2 %d (havuz %d); sınıf %s", len(O1), len(O2), len(havuz), S.sinif_k56.value_counts().to_dict())
    return {"ADAY": ADAY, "S": S, "havuz": havuz}
