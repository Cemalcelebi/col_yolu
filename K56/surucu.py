"""K56 sürücüleri: sentetik (M01), faz0 (raporlar), erisim (küçük örneklem). Her koşu: kimlik (commit, kilit sha, kod sha), kaynak kaydı, çıktı yolu denetimi."""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import time
from typing import Any, Dict, List, Optional, Tuple

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
    for kok, _, dosyalar in sorted(os.walk(kaynak)):                     # alt klasörler (faz1_yerel/, ic_dogrulama/, evren_v2/ ve koşu klasörleri) dahil
        for f in sorted(dosyalar):
            a = os.path.join(kok, f); g = os.path.relpath(a, kaynak); b = os.path.join(hedef, g); os.makedirs(os.path.dirname(b), exist_ok=True)
            shutil.copyfile(a, b); sa, sb = sha256_dosya(a), sha256_dosya(b)
            if sa != sb:
                raise RuntimeError(f"kopya bozuk: {g}")
            rows.append({"dosya": g, "bayt": os.path.getsize(b), "sha256": sa})
    M = pd.DataFrame(rows); M.to_csv(os.path.join(hedef, "K56_DRIVE_MANIFEST.csv"), index=False); log.info("Drive'a %d dosya kopyalandı (sha eşit): %s", len(M), hedef)
    return M


# ---------------------------------------------------------------- K56-EVREN2 (ONKAYIT v1.2-C)
def _alt_cikti(A: K56Ayar, alt: str) -> str:
    y = cikti_dogrula(os.path.join(A.cikti, alt)); os.makedirs(y, exist_ok=True); return y


def _kosu_klasoru(A: K56Ayar, alt: str, kimlik: Dict[str, Any]) -> str:
    """Her koşu kendi klasörüne (<alt>/<kimlik>/): yeni koşu eskisinin üzerine yazmaz (ön kayıt Genel)."""
    y = os.path.join(_alt_cikti(A, alt), kimlik["kimlik"]); os.makedirs(y, exist_ok=True); return y


def _son_yaz(A: K56Ayar, alt: str, kimlik: Dict[str, Any], klasor: str) -> None:
    _json_yaz(os.path.join(_alt_cikti(A, alt), "SON.json"), {"kimlik": kimlik["kimlik"], "commit": kimlik["commit"], "klasor": os.path.basename(klasor)})


def _son_oku(A: K56Ayar, alt: str) -> str:
    y = os.path.join(A.cikti, alt, "SON.json")
    if not os.path.exists(y):
        raise FileNotFoundError(f"{alt}/SON.json yok: kıyaslanacak koşu bilinmiyor (önce o çalışmayı koş)")
    return os.path.join(A.cikti, alt, json.load(open(y, encoding="utf-8"))["klasor"])


def evren2_aday_kos(A: K56Ayar) -> Dict[str, Any]:
    """Aday listesi (Ö1 + Ö2), SEC başvuru geçmişi, ön sınıflandırma (Tiingo bitişine göre). Tiingo FİYAT isteği yok."""
    from . import batan_evren as BE
    from .ortak import Istemci
    gunluk_log(); A.ag = True; out = _alt_cikti(A, "evren_v2"); kimlik = kosu_kimligi(A, "EVREN2-ADAY"); kk = KaynakKaydi(); ist = Istemci(A); Istemci.sec_ua()
    EV = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_EVREN.csv"), "veri", "K55 evreni (aday dışlama)")); T = BE.tiingo_listesi(A)
    O1, O1d = BE.aday_o1(A, kk, EV, T); n2 = max(0, BE.KOTA_UST - len(O1)); O2, havuz, N25 = BE.aday_o2(A, ist, EV, T, n2, set(O1.sembol) | set(O1d.sembol))
    if O1.cik.duplicated().any() or O1.sembol.duplicated().any() or O2.sembol.isin(O1.sembol).any():
        raise RuntimeError("Ö1 / Ö2 adaylarında yinelenen CIK ya da sembol")
    ADAY = pd.concat([O1, O2], ignore_index=True, sort=False)
    onb = os.path.join(A.onbellek, "evren_v2"); os.makedirs(onb, exist_ok=True)
    sec = BE.sec_gecmis(ist, sorted(O1.cik.astype(int).unique()), os.path.join(onb, "sec_ozet_v2.json"))
    ct = json.load(open("/tmp/k55/company_tickers.json", encoding="utf-8")); bugun = {v["ticker"].upper().replace(".", "-"): int(v["cik_str"]) for v in ct.values()}
    S = BE.siniflandir(O1, sec, T, bugun)                              # Ö2'nin CIK'i indirmeden sonra (Tiingo meta adı + 25-NSE; v1.2-a)
    ADAY.to_csv(os.path.join(out, "K56_EVREN2_ADAY.csv"), index=False); havuz.to_csv(os.path.join(out, "K56_EVREN2_O2_HAVUZ.csv"), index=False)
    N25.to_csv(os.path.join(out, "K56_EVREN2_25NSE.csv"), index=False); O1d.to_csv(os.path.join(out, "K56_EVREN2_O1_DISLANAN.csv"), index=False)
    S.to_csv(os.path.join(out, "K56_EVREN2_SINIF_ON.csv"), index=False); kk.tablo().to_csv(os.path.join(out, "K56_KAYNAK_KAYDI_EVREN2.csv"), index=False)
    G = pd.DataFrame(ist.gunluk); G["url"] = G.url.str.replace(r"[\w.+-]+@[\w-]+\.[\w.]+", "<e-posta>", regex=True); G.to_csv(os.path.join(out, "K56_EVREN2_ISTEK_GUNLUGU.csv"), index=False)
    _json_yaz(os.path.join(out, "K56_KOSU_EVREN2_ADAY.json"), {**kimlik, "o1": len(O1), "o1_dislanan": O1d.dislama.value_counts().to_dict(), "o2": len(O2), "o2_havuz": len(havuz), "o2_uygun": int((~havuz.sonraki_kullanim & ~havuz.haric).sum()), "n25": len(N25), "aday": len(ADAY), "sec_var": int(S.sec_var.sum()),
                                                              "sinif_on": S.sinif_k56.value_counts().to_dict()})
    log.info("evren v2 adaylar: Ö1 %d, Ö2 %d (havuz %d); sınıf %s", len(O1), len(O2), len(havuz), S.sinif_k56.value_counts().to_dict())
    return {"ADAY": ADAY, "S": S, "havuz": havuz}


# ---------------------------------------------------------------- K56-F1A (KEŞİF) ve K56-IC (İÇ) (ONKAYIT v1.2-A / B)
def _panel_yollari(A: K56Ayar) -> Tuple[str, str]:
    p = os.environ.get("K56_K55_PANEL", os.path.join(A.k55, "panel", "k55_panel_tam.pkl")); o = os.path.join(A.k55, "K55_OLAYLAR.csv.gz")
    if not os.path.exists(p):
        raise FileNotFoundError(f"K55 paneli yok: {p} (K56_K55_PANEL ile verin)")
    return p, o


def faz1_ozet(R: Dict[str, Any]) -> List[str]:
    """Sayılardan üretilen özet (yorum yok; ön kayıtlı karar adları)."""
    S, H, Bl = R["S"], R["H"], R["Bl"]; L = ["## Özet (sayılardan)", ""]
    L.append(f"- A1 / B2 seçimsiz kontrol, satır: {S.sinif_a1.value_counts().to_dict()}; hücre: {H.a1.value_counts().to_dict()}.")
    L.append(f"- GERÇEK ETKİ KALIYOR satırı: {int((S.sinif_a1 == 'GERÇEK ETKİ KALIYOR').sum())} / {len(S)}. d(ii) / d(i) medyanı {S.r_ii.median():.3f} "
             f"(d(i) medyanı {S.i_d.median():+.3f}, d(ii) medyanı {S.ii_d.median():+.3f}).")
    L.append(f"- (iii) duyarlılık (olay dizisinden rastgele gün): {S.sinif_iii.value_counts().to_dict()}; (ii) ile sınıfı farklı satır {int(S.iii_farkli.sum())}.")
    if "tani_dizi_d" in S:
        L.append(f"- Açıklayıcı tanı (ön kayıt dışı, karar değiştirmez): olay dizisinin bütün günleri d medyanı {S.tani_dizi_d.median():+.3f}; olay dizisi DIŞINDAKİ "
                 f"nitelikli günler d medyanı {S.tani_dis_d.median():+.3f} (işareti d(i)'ye ters satır {int((np.sign(S.tani_dis_d) == -np.sign(S.i_d)).sum())} / {len(S)}). "
                 "(iii) yalnız ilk günün seçimini kaldırır; olayın başlattığı dizinin (yükseliş epizodunun ilk dizisi) seçimini kaldırmaz. Bir günün nitelikli "
                 "olup olmayacağı sorusunun karşılığı (ii)'dir.")
    a2 = [c for c in S.columns if c.startswith("a2_") and c.endswith("_kuculme")]
    if a2:
        K = S[S[a2].notna().any(axis=1)]
        if len(K):
            L.append(f"- A2 kalan etki: {len(K)} satır; en az bir denetimin AÇIKLADIĞI (küçülme >= 0,50) satır {int((K[a2] >= 0.5).any(axis=1).sum())}; denetim başına "
                     f"AÇIKLAR sayısı {{{', '.join(f'{c[3:-8]}: {int((K[c] >= 0.5).sum())}' for c in a2)}}}. (Küçük d(ii)'de küçülme oranı oynaktır.)")
    if len(Bl) and "karar" in Bl:
        z = Bl[Bl.karar.isin(["G1 > G7", "G1 < G7"])]
        L.append("- A3 bileşim, aralığı 0'ı dışlayan: " + ("; ".join(f"{r.ufuk} {r.olcu} {r.karar} ({r.fark:+.3f})" for r in z.itertuples()) or "yok") + ".")
    if "b1_gecti" in S:
        L.append(f"- B1 (K55 A, ilk geçiş) İÇ'te geçen satır {int(S.b1_gecti.sum())} / {len(S)}; hücre {H.b1_durum.value_counts().to_dict()}. B1 geçişi seçim etkisi "
                 "tekrarlandığında da olur; gerçek etki için belirleyici B2'dir (ön kayıt v1.2-B).")
    if len(R.get("B3", [])):
        L.append(f"- B3 (K55 B, eşleşmiş ileri getiri) İÇ: {R['B3'].karar.value_counts().to_dict()}.")
    return L + [""]


def faz1_yaz(alt: str, baslik: str, kimlik: Dict[str, Any], R: Dict[str, Any], ek: List[str]) -> str:
    from .mekanizma_raporu import _md
    S, H, Bl = R["S"], R["H"], R["Bl"]; L = [f"# {baslik} ({kimlik['kimlik']})", "", f"- commit {kimlik['commit']}; kilit sha {kimlik['onkayit_sha'][:12]}; evren sürümü {R['evren_surum'][:12]}; süre {R['sure_dk']} dk.",
                                            f"- Olay oranı (olay / likit satır): {json.dumps({k: round(v, 5) for k, v in R['olay_orani'].items()})}."] + ek + [""] + faz1_ozet(R)
    L += ["## A1 seçimsiz kontrol: satır sınıfları", ""] + _md(S.sinif_a1.value_counts().rename("n").reset_index(), ["sinif_a1", "n"])
    L += ["", "Ufuk × sınıf:", ""] + _md(pd.crosstab(S.ufuk, S.sinif_a1).reset_index(), list(pd.crosstab(S.ufuk, S.sinif_a1).reset_index().columns))
    L += ["", "## Hücre sınıfları (KEŞİF satırlarının çoğunluğu)", ""] + _md(H, list(H.columns))
    L += ["", "## Satırlar (d: (i) ilk geçiş, (ii) bütün nitelikli günler, (iii) rastgele gün)", ""]
    L += _md(S.sort_values(["hucre", "varyant", "ufuk"]), ["hucre", "varyant", "ufuk", "i_n_olay", "i_d", "ii_n_olay", "ii_d", "ii_d_alt", "ii_d_ust", "iii_d", "r_ii", "sent_oran_faz0", "sinif_a1", "sinif_iii", "ayr_d",
                                                         "tani_dizi_d", "tani_dis_d"])
    a2 = [c for c in S.columns if c.startswith("a2_") and c.endswith("_kuculme")]
    if a2:
        K = S[S[a2].notna().any(axis=1)]
        L += ["", "## A2 kalan etki denetimi (küçülme = 1 − |d_denetim| / |d(ii)|; >= 0,50 açıklar, 0,25-0,50 kısmen, < 0,25 açıklamaz)", ""] + _md(K, ["hucre", "varyant", "ufuk", "ii_d"] + a2)
    L += ["", "## A3 haber ve birleşme bileşimi (G1 olay − G7 eş; ÖNCESİ sızıntısız, SONRASI açıklayıcı)", ""] + _md(Bl, ["ufuk", "olcu", "tur", "n_olay", "pay_g1", "pay_g7", "fark", "fark_alt", "fark_ust", "karar"])
    if "b1_gecti" in S:
        L += ["", "## B1 İÇ (A, ilk geçiş; KEŞİF satırlarıyla)", "", f"- geçen satır {int(S.b1_gecti.sum())} / {len(S)}", ""] + _md(S[S.b1_gecti], ["hucre", "varyant", "ufuk", "kesif_d", "i_d", "i_d_alt", "i_d_ust", "i_auc", "q_bh"])
    if len(R.get("B3", [])):
        L += ["", "## B3 İÇ (K55 B, eşleşmiş ileri)", ""] + _md(R["B3"], ["hucre", "varyant", "n", "fark", "fark_alt", "net_fark", "slot_rastgele_yuzdelik", "karar"])
    yol = os.path.join(alt, "RAPOR.md"); open(yol, "w", encoding="utf-8").write("\n".join(L) + "\n"); return yol


def faz1a_kos(A: K56Ayar, isci: int = 3) -> Dict[str, Any]:
    """K56-F1A: A1 + A2 + A3 KEŞİF'te; ayrıca kalibre sentetik spekler (125 satır). İndirme yok."""
    from . import faz1_yerel as F1
    from . import mekanizma as M
    gunluk_log(); A.ag = False; kimlik = kosu_kimligi(A, "F1A"); out = _kosu_klasoru(A, "faz1_yerel", kimlik); kk = KaynakKaydi(); p, o = _panel_yollari(A)
    R = F1.calistir(A, kk, "KESIF", p, o, isci=isci, b3=False)
    K = M.kesif_satirlari(A, kk); Sk, _ = M.secim_sentetik(A, kk, spekler=(("kalibre_gjr", 565), ("kalibre_sicrama", 566)), varyantlar=K)
    Kc = []
    for sp in ("kalibre_gjr", "kalibre_sicrama"):
        z = M.sentetik_kesif_ozet(Sk[Sk.spek == sp], K); z["spek"] = sp; Kc.append(z)
    Kc = pd.concat(Kc, ignore_index=True); oran = {}
    Kc["sinif_tek_spek"] = Kc.spek_siniflari                              # tek spek: 4 spek uyum kuralı (karar sütunu) burada uygulanamaz -> BELIRSIZ yazar
    Kc = Kc.rename(columns={"karar": "karar_4spek_kurali_uygulanamaz"})
    for sp, th in (("kalibre_gjr", 565), ("kalibre_sicrama", 566)):
        Vs, EVs, Es = M.sentetik_veri(M.SENTETIK_HISSE, M.SENTETIK_GUN, th, sp); Ps, Os = M.sentetik_panel(Vs, EVs, Es); oran[sp] = (Os.ufuk.value_counts() / Ps.likit.sum()).round(5).to_dict()
    R["S"].to_csv(os.path.join(out, "K56F1_A1_SATIR.csv"), index=False); R["H"].to_csv(os.path.join(out, "K56F1_A1_HUCRE.csv"), index=False); R["Bl"].to_csv(os.path.join(out, "K56F1_A3_BILESIM.csv"), index=False)
    Kc.to_csv(os.path.join(out, "K56F1_SENTETIK_KALIBRE.csv"), index=False); kk.tablo().to_csv(os.path.join(out, "K56F1_KAYNAK_KAYDI.csv"), index=False)
    ek = [f"- Kalibre sentetik (duyarlılık, bilgisiz yapay veri): tek spek sınıfları {Kc.groupby('spek').sinif_tek_spek.value_counts().to_dict()}; sentetik / gerçek d oranı "
          f"medyanı {Kc.groupby('spek').oran.median().round(2).to_dict()}; yapay olay oranı {oran} (gerçeğin altında: kalibrasyon kuyrukları tam üretmiyor).",
          "- A3 SONRASI sütunları AÇIKLAYICIDIR (olaydan sonraki bilgi); hiçbir sinyalde kullanılmaz. ÖNCESİ yalnız t0−1'e kadar başvurular (sızıntı kapısı)."]
    faz1_yaz(out, "K56-F1A FAZ 1 YEREL ANALİZLER (KEŞİF 2016-21; keşif verisi yeniden kullanımı)", kimlik, R, ek)
    _json_yaz(os.path.join(out, "K56_KOSU_F1A.json"), {**kimlik, "sure_dk": R["sure_dk"], "a1": R["S"].sinif_a1.value_counts().to_dict(), "hucre": R["H"].a1.value_counts().to_dict(), "sentetik_olay_orani": oran})
    _son_yaz(A, "faz1_yerel", kimlik, out)
    return R


def ic_kos(A: K56Ayar, isci: int = 3) -> Dict[str, Any]:
    """K56-IC: İÇ 2022-23 (B1 ilk geçiş A, B2 seçimsiz, B3 K55 B, B4 bileşim + A2). BAĞIMSIZ kapalı; sonunda BAĞIMSIZ kilit dosyası üretilir (açmaz)."""
    from . import faz1_yerel as F1
    from .ortak import BAGIMSIZ_KILIT, kilit_icerigi, veri_tanimi_hesapla
    gunluk_log(); A.ag = False; kimlik = kosu_kimligi(A, "IC"); out = _kosu_klasoru(A, "ic_dogrulama", kimlik); kk = KaynakKaydi(); p, o = _panel_yollari(A)
    R = F1.calistir(A, kk, "IC_DOGRULAMA", p, o, isci=isci, b3=True)
    R["S"].to_csv(os.path.join(out, "K56IC_SATIR.csv"), index=False); R["H"].to_csv(os.path.join(out, "K56IC_HUCRE.csv"), index=False)
    R["B3"].to_csv(os.path.join(out, "K56IC_B3.csv"), index=False); R["Bl"].to_csv(os.path.join(out, "K56IC_BILESIM.csv"), index=False); kk.tablo().to_csv(os.path.join(out, "K56IC_KAYNAK_KAYDI.csv"), index=False)
    ek = ["- Yalnız önceden belirlenmiş 125 satır ve 64 varyant; İÇ sonucuna göre eşik / değişken türetilmez. BAĞIMSIZ (2024-26) kapalı (kod kapısı).",
          "- B1 = K55 A (ilk geçiş) ölçütleri; B2 = seçimsiz kontrol (gerçek etki için belirleyici); B3 = K55 B; B4 = bileşim + A2."]
    faz1_yaz(out, "K56-IC İÇ DOĞRULAMA 2022-23", kimlik, R, ek)
    vt = {**veri_tanimi_hesapla(p, o, evren=False), "evren_surum": R["evren_surum"]}
    kil = {**kilit_icerigi(vt), "uretim": time.strftime("%Y-%m-%d %H:%M:%S"), "commit": kimlik["commit"], "kimlik": kimlik["kimlik"],
           "not": "BAĞIMSIZ açılmadı; açılış için Cemal kararı + K56_BAGIMSIZ_AC=1 + bu dosyanın birebir doğrulanması (kod, ön kayıt, eşik, veri tanımı yeniden hesaplanır)"}
    _json_yaz(os.path.join(out, BAGIMSIZ_KILIT), kil); _json_yaz(os.path.join(A.cikti, BAGIMSIZ_KILIT), kil)       # kökteki = geçerli kilit; koşu klasöründe kopyası
    _json_yaz(os.path.join(out, "K56_KOSU_IC.json"), {**kimlik, "sure_dk": R["sure_dk"], "b1_gecen": int(R["S"].b1_gecti.sum()), "b2": R["S"].sinif_a1.value_counts().to_dict(),
                                                      "b3": R["B3"].karar.value_counts().to_dict() if len(R["B3"]) else {}, "hucre": R["H"].to_dict("records")})
    _son_yaz(A, "ic_dogrulama", kimlik, out)
    return R


# ---------------------------------------------------------------- K56-EVREN2: indirme (1 Kasım 2026'dan itibaren) ve evren v2 + etki
def _evren2_klasor(A: K56Ayar) -> str:
    y = os.path.join(A.onbellek, "evren_v2", "tiingo"); os.makedirs(y, exist_ok=True); return y     # Tiingo fiyatları repoya girmez (lisans)


def evren2_indir_kos(A: K56Ayar) -> Dict[str, Any]:
    """Aday listesindeki 490 sembolün Tiingo fiyatı (+ Ö2 için meta adı). 1 Kasım'dan önce ValueError; kota / 429'da durur, kaldığı yerden sürer."""
    from . import batan_evren as BE
    gunluk_log(); out = _alt_cikti(A, "evren_v2"); ADAY = pd.read_csv(os.path.join(out, "K56_EVREN2_ADAY.csv")); kl = _evren2_klasor(A)
    durum = os.path.join(kl, "K56_EVREN2_TIINGO_DURUM.csv"); meta = set(ADAY.sembol[ADAY.kaynak.str.startswith("Ö2")])
    try:
        D = BE.tiingo_indir(list(ADAY.sembol), kl, durum_yolu=durum, meta=meta); bitti = True
    except BE.KotaDoldu as ex:
        log.warning("Tiingo durdu (kota / hız): %s; aynı komut kaldığı yerden sürer", ex); D = pd.read_csv(durum); bitti = False
    D.to_csv(os.path.join(out, "K56_EVREN2_TIINGO_DURUM.csv"), index=False)                         # yalnız durum (fiyat yok)
    n = sum(os.path.exists(os.path.join(kl, f"{s}.csv")) for s in ADAY.sembol)
    log.info("Tiingo: %d / %d fiyat dosyası; %s", n, len(ADAY), "bitti" if bitti else "KOTA / HIZ (sürdürülecek)")
    return {"dosya": n, "aday": len(ADAY), "bitti": bitti}


def evren2_kur_kos(A: K56Ayar, isci: int = 3) -> Dict[str, Any]:
    """İndirme sonrası denetim + sınıflandırma, evren v2 (K55 kodu aynen), panel / olay, etki (125 KEŞİF satırı d(i) / d(ii), KEŞİF ve İÇ), rapor."""
    from . import batan_evren as BE, evren_v2 as E2, faz1_yerel as F1
    from .mekanizma_raporu import _md
    from .ortak import Istemci
    gunluk_log(); kok = _alt_cikti(A, "evren_v2"); kimlik = kosu_kimligi(A, "EVREN2"); out = _kosu_klasoru(A, "evren_v2", kimlik); kk = KaynakKaydi(); kl = _evren2_klasor(A); t0 = time.time()
    ADAY = pd.read_csv(kk.oku(os.path.join(kok, "K56_EVREN2_ADAY.csv"), "veri", "K56 evren v2 aday listesi (Ö1 + Ö2)"))
    evren2_on_denetim(A, ADAY, kl)                                          # eksik indirme / SEC özeti / önbellek yolu: sessiz boş evren yerine dur
    eski_f1, eski_ic = _son_oku(A, "faz1_yerel"), _son_oku(A, "ic_dogrulama")
    N25 = pd.read_csv(kk.oku(os.path.join(kok, "K56_EVREN2_25NSE.csv"), "veri", "SEC EFTS 25-NSE (2015-11..2022-02)")); N25["nse_tarih"] = pd.to_datetime(N25.nse_tarih)
    T = BE.tiingo_listesi(A); A.ag = bool(os.environ.get("SEC_EPOSTA")); ist = Istemci(A) if A.ag else None
    if ist is not None:
        Istemci.sec_ua()
    Y = E2.indirme_sonrasi(A, ist, ADAY, kl, N25, T, os.path.join(A.onbellek, "evren_v2", "sec_ozet_v2.json")); A.ag = False
    yok = Y[Y.cik.notna() & ~Y.sec_var]
    if len(yok):
        raise RuntimeError(f"{len(yok)} adayın CIK'i var ama SEC geçmişi yok (SEC_EPOSTA verilmedi ya da indirme başarısız): {yok.sembol.tolist()[:10]}; sınıf 6'ya düşüp sessizce evren dışı kalırdı")
    Y.to_csv(os.path.join(out, "K56_EVREN2_YENI_SIRKET.csv"), index=False)
    R = E2.evren2_kur(A, Y, kl); R["yeni"].to_csv(os.path.join(out, "K56_EVREN2_EKLEME.csv"), index=False)
    VR = E2.panel_olay(R, isci=isci); EVk = pd.read_csv(os.path.join(A.k55, "K55_EVREN.csv"))
    Ok = pd.read_csv(os.path.join(A.k55, "K55_OLAYLAR.csv.gz")); OK = E2.olay_karsilastir(Ok, VR["O"], VR["EV"]); OK.to_csv(os.path.join(out, "K56_EVREN2_OLAY_SAYILARI.csv"), index=False)
    KP = E2.kapsam_tablosu(Y, R, VR["V"]); KP.to_csv(os.path.join(out, "K56_EVREN2_KAPSAM.csv"), index=False)
    GD = E2.getiri_duyarlilik(VR["P"], VR["EV"], Y); GD.to_csv(os.path.join(out, "K56_EVREN2_GETIRI_DUYARLILIK.csv"), index=False)
    ET = []
    for donem, eski_yol in (("KESIF", os.path.join(eski_f1, "K56F1_A1_SATIR.csv")), ("IC_DOGRULAMA", os.path.join(eski_ic, "K56IC_SATIR.csv"))):
        if not os.path.exists(eski_yol):
            raise FileNotFoundError(f"kıyas dosyası yok: {eski_yol}")
        Rv = F1.calistir(A, kk, donem, None, None, isci=isci, veri=VR, yalniz_a1=True); S = Rv["S"]; S["evren"] = "v2"
        E = pd.read_csv(kk.oku(eski_yol, "kiyas", f"K56 {donem} satırları (K55 evreni)"))[["hucre", "varyant", "ufuk", "i_n_olay", "i_d", "ii_d", "sinif_a1"]]
        S = S.merge(E.rename(columns={"i_n_olay": "eski_i_n_olay", "i_d": "eski_i_d", "ii_d": "eski_ii_d", "sinif_a1": "eski_sinif_a1"}), on=["hucre", "varyant", "ufuk"], how="left")
        S["fark_i_d"] = S.i_d - S.eski_i_d; S["fark_ii_d"] = S.ii_d - S.eski_ii_d; S["sinif_degisti"] = S.sinif_a1 != S.eski_sinif_a1
        ET.append(S)
    ET = pd.concat(ET, ignore_index=True); ET.to_csv(os.path.join(out, "K56_EVREN2_ETKI.csv"), index=False); kk.tablo().to_csv(os.path.join(out, "K56_EVREN2_KAYNAK_KAYDI.csv"), index=False)
    ozet = {"aday": len(ADAY), "kaynak": ADAY.kaynak.value_counts().to_dict(), "seri_durum": Y.seri_durum.value_counts().to_dict(), "baglama": Y.baglama.value_counts().to_dict(),
            "sinif_k56": Y.sinif_k56.value_counts().to_dict(), "evrene_giren": int(VR["EV"].kaynak.str.startswith("K56_").sum()), "evren_v2_sembol": len(VR["EV"]),
            "evren_k55_sembol": len(EVk), "evren_v2_surum": R["surum"], "sure_dk": round((time.time() - t0) / 60, 1)}
    L = [f"# K56-EVREN2 BATAN ŞİRKETLERLE EVREN v2 ({kimlik['kimlik']})", "", f"- commit {kimlik['commit']}; evren v2 sürümü {R['surum'][:12]} (K55: 0d00d2c97608, DEĞİŞMEDİ); süre {ozet['sure_dk']} dk.",
         "- K51-K55 evreni ve sonuçları değişmedi; v2 ayrı sürüm. Getiri (asıl): yeni şirkette pencere seri sonunu aşarsa TANIMSIZ; son işlem fiyatı tasfiye ödemesi sayılmadı; eksik delist getirisi uydurulmadı.",
         f"- Aday {ozet['aday']} ({ozet['kaynak']}); seri durumu {ozet['seri_durum']}; Ö2 CIK bağlama {ozet['baglama']}.",
         f"- Sınıf (K54 kuralı + K56 ayrımı): {ozet['sinif_k56']}.", f"- Evrene giren yeni şirket {ozet['evrene_giren']}; evren v2 {ozet['evren_v2_sembol']} sembol (K55 {ozet['evren_k55_sembol']}).", "",
         "## Olay sayıları (dönem × ufuk)", ""] + _md(OK, list(OK.columns))
    L += ["", "## Yeni şirketlerin tarihsel kapsamı", "", f"- KEŞİF günü olan şirket {int((KP.get('gun_kesif', pd.Series(dtype=float)) > 0).sum())}; İÇ {int((KP.get('gun_ic', pd.Series(dtype=float)) > 0).sum())}; BAĞIMSIZ {int((KP.get('gun_bagimsiz', pd.Series(dtype=float)) > 0).sum())}.", ""]
    L += _md(KP.groupby(["kaynak", "sinif_k56"]).agg(n=("sembol", "size"), evrende=("evrende", "sum")).reset_index(), ["kaynak", "sinif_k56", "n", "evrende"])
    L += ["", "## Veri eksikleri", ""] + _md(R["yeni"].durum.value_counts().rename("n").reset_index(), ["durum", "n"])
    L += ["", "## Getiri duyarlılığı (A1'i etkilemez: olay ve nitelikli gün tam pencere ister)", ""] + _md(GD, list(GD.columns))
    L += ["", "## Etki: 125 KEŞİF satırı (v2 − K55)", "", f"- sınıfı değişen satır: {ET.groupby('donem').sinif_degisti.sum().to_dict() if 'sinif_degisti' in ET else 'eski sonuç yok'}", ""]
    L += _md(ET.sort_values(["donem", "hucre", "varyant", "ufuk"]), ["donem", "hucre", "varyant", "ufuk", "eski_i_n_olay", "i_n_olay", "eski_i_d", "i_d", "eski_ii_d", "ii_d", "eski_sinif_a1", "sinif_a1"])
    open(os.path.join(out, "RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    _json_yaz(os.path.join(out, "K56_KOSU_EVREN2.json"), {**kimlik, **ozet, "kiyas": {"faz1_yerel": os.path.basename(eski_f1), "ic_dogrulama": os.path.basename(eski_ic)}})
    _son_yaz(A, "evren_v2", kimlik, out)
    return {"Y": Y, "R": R, "OK": OK, "ET": ET, "ozet": ozet}


def evren2_on_denetim(A: K56Ayar, ADAY: pd.DataFrame, kl: str) -> None:
    """EVREN2 kurulmadan önce: (1) Tiingo durum tablosunda her aday fiyat için denenmiş ve son durumu kota değil; (2) SEC özeti var ve bütün Ö1 CIK'lerini
    içeriyor; (3) önbellek yolu kayıtlı. Eksikte durur (sessizce eksik / boş evren kurulmaz)."""
    d = os.path.join(kl, "K56_EVREN2_TIINGO_DURUM.csv")
    if not os.path.exists(d):
        raise FileNotFoundError(f"Tiingo durum tablosu yok: {d} (önbellek {A.onbellek}; K56_ONBELLEK doğru mu, indirme yapıldı mı?)")
    D = pd.read_csv(d); D["tur"] = D.get("tur", pd.Series("fiyat", index=D.index)).fillna("fiyat")
    son = D[D.tur == "fiyat"].groupby("sembol").durum.last()
    eksik = sorted(set(ADAY.sembol) - set(son.index)); kota = sorted(son.index[son == "kota"])
    if eksik or kota:
        raise RuntimeError(f"indirme bitmemiş: denenmemiş {len(eksik)} {eksik[:8]}, kota durumunda {len(kota)}; önce python K56.py evren2_indir")
    sy = os.path.join(A.onbellek, "evren_v2", "sec_ozet_v2.json")
    if not os.path.exists(sy):
        raise FileNotFoundError(f"SEC özeti yok: {sy} (önbellek yolu {A.onbellek})")
    sec = json.load(open(sy, encoding="utf-8")); o1 = ADAY.cik.dropna().astype(int).astype(str)
    if (~o1.isin(sec)).any():
        raise RuntimeError(f"SEC özetinde {int((~o1.isin(sec)).sum())} Ö1 CIK'i yok: {o1[~o1.isin(sec)].tolist()[:8]}")
    log.info("EVREN2 ön denetim tamam: %d aday, durum %s, önbellek %s", len(ADAY), son.value_counts().to_dict(), A.onbellek)
