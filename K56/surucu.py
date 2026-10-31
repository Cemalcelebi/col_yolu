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
        L.append(f"- Açıklayıcı tanı (ön kayıt dışı, karar değiştirmez): olay dizilerinin BÜTÜN günleri bir arada d medyanı {S.tani_dizi_d.median():+.3f}; olay "
                 f"dizisi dışındaki nitelikli günler d medyanı {S.tani_dis_d.median():+.3f}; (iii) d medyanı {S.iii_d.median():+.3f}. (iii) olay başına bir gün "
                 "alır (olay ağırlıklı), dizi günleri ve (ii) gün ağırlıklıdır: aynı dizilerin günleri bir arada fark göstermiyor, olay başına bir gün "
                 "gösteriyor. Olası neden ağırlık: uzun dizilerin günleri havuza çok girer ve dizi ilerledikçe (fiyat yükselirken) değişken ortalamaya yaklaşabilir "
                 "(DOĞRULANMADI; ön kayıt dışı). Bir günün nitelikli "
                 "olup olmayacağı (öngörü) sorusu gün ağırlıklıdır; ön kayıtta karar (ii)'ye göredir.")
        if "tani_dizi_n" in S:
            L.append(f"- Dizi günü / olay oranı medyanı {(S.tani_dizi_n / S.i_n_olay).median():.1f} (bir olayın başlattığı kesintisiz nitelikli dizinin ortalama uzunluğu).")
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
    _json_yaz(os.path.join(out, "K56_BAGIMSIZ_KILIT_TASLAK.json"), {**kil, "not": "İÇ koşusu taslağı; GEÇERLİ KİLİT DEĞİL (v1.3: geçerli kilit yalnız kilit_uret ile)"})
    _json_yaz(os.path.join(out, "K56_KOSU_IC.json"), {**kimlik, "sure_dk": R["sure_dk"], "b1_gecen": int(R["S"].b1_gecti.sum()), "b2": R["S"].sinif_a1.value_counts().to_dict(),
                                                      "b3": R["B3"].karar.value_counts().to_dict() if len(R["B3"]) else {}, "hucre": R["H"].to_dict("records")})
    _son_yaz(A, "ic_dogrulama", kimlik, out)
    return R


# ---------------------------------------------------------------- K56-EVREN2: indirme (1 Kasım 2026'dan itibaren) ve evren v2 + etki
def _evren2_klasor(A: K56Ayar) -> str:
    y = os.path.join(A.onbellek, "evren_v2", "tiingo"); os.makedirs(y, exist_ok=True); return y     # Tiingo fiyatları repoya girmez (lisans)


def evren2_indir_kos(A: K56Ayar) -> Dict[str, Any]:
    """v1.3 iki aşamalı Tiingo indirmesi (1 Kasım'dan önce ValueError; kota / 429'da durur, kaldığı yerden sürer):
    1) bütün adaylar için meta (fiyat yok); 2) fiyatsız doğrulama (meta varlık, adi hisse adı, Ö2 CIK bağlama, SEC geçmişi, kimlik, SEC kapsamı, ön ek; SEC
    e-postası yalnız SEC_EPOSTA) -> K56_EVREN2_META_DOGRULAMA.csv (sha koşu kaydına); 3) yalnız DIŞI kuralına takılmayanların fiyatı."""
    from . import batan_evren as BE, evren_v2 as E2
    from .ortak import Istemci, sha256_dosya
    gunluk_log(); kimlik = kosu_kimligi(A, "EVREN2-INDIR"); out = _alt_cikti(A, "evren_v2"); ADAY = pd.read_csv(os.path.join(out, "K56_EVREN2_ADAY.csv")); kl = _evren2_klasor(A)
    Tl = BE.tiingo_listesi(A); eski = [r.sembol for r in ADAY.itertuples() if BE.indirme_oncesi_suzgec(Tl, r.sembol, r.borsa, r.baslangic, r.bitis)[0] == "DIŞI"]
    if eski:
        raise RuntimeError(f"aday listesi v1.3 indirme öncesi süzgecinden geçmemiş ({len(eski)}: {eski[:8]}); önce python K56.py evren2_aday")
    durum = os.path.join(kl, "K56_EVREN2_TIINGO_DURUM.csv"); asama = "meta"
    try:
        BE.tiingo_indir(list(ADAY.sembol), kl, durum_yolu=durum, meta=set(ADAY.sembol), fiyat=False)
        asama = "doğrulama"
        if not os.environ.get("SEC_EPOSTA"):
            raise RuntimeError("SEC_EPOSTA yok: Ö2 CIK'lerinin SEC geçmişi olmadan doğrulama yapılmaz (sessiz sınıf 6 olurdu)")
        A.ag = True; ist = Istemci(A); Istemci.sec_ua(); N25 = pd.read_csv(os.path.join(out, "K56_EVREN2_25NSE.csv")); N25["nse_tarih"] = pd.to_datetime(N25.nse_tarih)
        M = E2.meta_dogrulama(A, ist, ADAY, kl, N25, BE.tiingo_listesi(A), os.path.join(A.onbellek, "evren_v2", "sec_ozet_v2.json")); A.ag = False
        my = os.path.join(out, "K56_EVREN2_META_DOGRULAMA.csv"); M.to_csv(my, index=False)
        asama = "fiyat"; gec = list(M.sembol[M.fiyat_iste])
        D = BE.tiingo_indir(gec, kl, durum_yolu=durum, fiyat=True); bitti = True
    except BE.KotaDoldu as ex:
        log.warning("Tiingo durdu (%s aşaması; kota / hız): %s; aynı komut kaldığı yerden sürer", asama, ex); bitti = False
    D = pd.read_csv(durum) if os.path.exists(durum) else pd.DataFrame()
    D.to_csv(os.path.join(out, "K56_EVREN2_TIINGO_DURUM.csv"), index=False)                         # yalnız durum (fiyat yok)
    my = os.path.join(out, "K56_EVREN2_META_DOGRULAMA.csv"); n = sum(os.path.exists(os.path.join(kl, f"{s}.csv")) for s in ADAY.sembol)
    _json_yaz(os.path.join(out, "K56_EVREN2_INDIRME.json"), {"kimlik": kimlik["kimlik"], "commit": kimlik["commit"], "asama": asama, "bitti": bitti, "fiyat_dosyasi": n, "aday": len(ADAY),
                                                             "meta_dogrulama_sha": sha256_dosya(my) if os.path.exists(my) else "", "zaman": time.strftime("%Y-%m-%d %H:%M:%S")})
    log.info("Tiingo: %d / %d fiyat dosyası; aşama %s; %s", n, len(ADAY), asama, "bitti" if bitti else "KOTA / HIZ (sürdürülecek)")
    return {"dosya": n, "aday": len(ADAY), "bitti": bitti}


def _etki_kos(A: K56Ayar, kk: KaynakKaydi, VR: Dict[str, Any], donem: str, eski_yol: str, isci: int, etiket: str) -> pd.DataFrame:
    if not os.path.exists(eski_yol):
        raise FileNotFoundError(f"kıyas dosyası yok: {eski_yol}")
    Rv = F1_calistir(A, kk, donem, VR, isci); S = Rv["S"]; S["evren"] = etiket
    E = pd.read_csv(kk.oku(eski_yol, "kiyas", f"K56 {donem} satırları (K55 evreni)"))[["hucre", "varyant", "ufuk", "i_n_olay", "i_d", "ii_d", "sinif_a1"]]
    S = S.merge(E.rename(columns={"i_n_olay": "eski_i_n_olay", "i_d": "eski_i_d", "ii_d": "eski_ii_d", "sinif_a1": "eski_sinif_a1"}), on=["hucre", "varyant", "ufuk"], how="left")
    S["fark_i_d"] = S.i_d - S.eski_i_d; S["fark_ii_d"] = S.ii_d - S.eski_ii_d; S["sinif_degisti"] = S.sinif_a1 != S.eski_sinif_a1
    return S


def F1_calistir(A: K56Ayar, kk: KaynakKaydi, donem: str, VR: Dict[str, Any], isci: int) -> Dict[str, Any]:
    from . import faz1_yerel as F1
    return F1.calistir(A, kk, donem, None, None, isci=isci, veri=VR, yalniz_a1=True)


def evren2_kur_kos(A: K56Ayar, isci: int = 3) -> Dict[str, Any]:
    """v1.3: meta doğrulamasını geçen adaylar -> indirme sonrası denetim + sınıflandırma -> fiyat / son işlem / sınıf denetimi -> aday doğrulama tablosu ->
    evren v2 (K55 kodu aynen) -> panel / olay -> etki (125 KEŞİF satırı, yalnız A1) KEŞİF ve İÇ; duyarlılık evreni (işaretli alt kümeler hariç); BAĞIMSIZ etkisi
    yalnız ana BAĞIMSIZ koşusu tamamlanmışsa ve kilit tutuyorsa, bir kez (açılış kaydı EVREN2_BAGIMSIZ)."""
    from . import batan_evren as BE, evren_v2 as E2
    from .mekanizma_raporu import _md
    from .ortak import Istemci, sha256_dosya
    gunluk_log(); kok = _alt_cikti(A, "evren_v2"); kimlik = kosu_kimligi(A, "EVREN2"); out = _kosu_klasoru(A, "evren_v2", kimlik); kk = KaynakKaydi(); kl = _evren2_klasor(A); t0 = time.time()
    ADAY = pd.read_csv(kk.oku(os.path.join(kok, "K56_EVREN2_ADAY.csv"), "veri", "K56 evren v2 aday listesi (Ö1 + Ö2)"))
    my = os.path.join(kok, "K56_EVREN2_META_DOGRULAMA.csv")
    if not os.path.exists(my):
        raise FileNotFoundError(f"meta doğrulama tablosu yok: {my} (önce python K56.py evren2_indir)")
    M = pd.read_csv(kk.oku(my, "veri", "v1.3 meta aşaması doğrulama (fiyat görülmeden)")); gec = M[M.fiyat_iste]
    evren2_on_denetim(A, gec.rename(columns={"aday_baslangic": "baslangic", "aday_bitis": "bitis", "aday_borsa": "borsa"}), kl)
    eski_f1, eski_ic = _son_oku(A, "faz1_yerel"), _son_oku(A, "ic_dogrulama")
    N25 = pd.read_csv(kk.oku(os.path.join(kok, "K56_EVREN2_25NSE.csv"), "veri", "SEC EFTS 25-NSE (2015-11..2022-02)")); N25["nse_tarih"] = pd.to_datetime(N25.nse_tarih)
    T = BE.tiingo_listesi(A); A.ag = bool(os.environ.get("SEC_EPOSTA")); ist = Istemci(A) if A.ag else None
    if ist is not None:
        Istemci.sec_ua()
    G = ADAY[ADAY.sembol.isin(set(gec.sembol))].drop(columns=["cik"]).merge(gec[["sembol", "cik", "baglama"]], on="sembol", how="left")     # Ö2 CIK'i ve bağlama yöntemi meta aşamasından
    sec_yol = os.path.join(A.onbellek, "evren_v2", "sec_ozet_v2.json")
    Y = E2.indirme_sonrasi(A, ist, G, kl, N25, T, sec_yol); A.ag = False
    yok = Y[Y.cik.notna() & ~Y.sec_var]
    if len(yok):
        raise RuntimeError(f"{len(yok)} adayın CIK'i var ama SEC geçmişi yok (SEC_EPOSTA verilmedi ya da indirme başarısız): {yok.sembol.tolist()[:10]}; sınıf 6'ya düşüp sessizce evren dışı kalırdı")
    Y.to_csv(os.path.join(out, "K56_EVREN2_YENI_SIRKET.csv"), index=False)
    from K55.ortak import cy
    sec = json.load(open(sec_yol, encoding="utf-8")); F = E2.fiyat_son_islem_denetimi(Y, M, kl, sec, pd.Timestamp(cy().CY["kriz"]))
    fy = os.path.join(out, "K56_EVREN2_FIYAT_DENETIMI.csv"); F.to_csv(fy, index=False)
    R = E2.evren2_kur(A, Y, kl, ek_sha={"K56_EVREN2_META_DOGRULAMA": sha256_dosya(my), "K56_EVREN2_FIYAT_DENETIMI": sha256_dosya(fy)}); R["yeni"].to_csv(os.path.join(out, "K56_EVREN2_EKLEME.csv"), index=False)
    DG = E2.dogrulama_tablosu(M, F, R["yeni"]); dy = os.path.join(out, "K56_EVREN2_DOGRULAMA.csv"); DG.to_csv(dy, index=False)
    VR = E2.panel_olay(R, isci=isci); EVk = pd.read_csv(os.path.join(A.k55, "K55_EVREN.csv"))
    Ok = pd.read_csv(os.path.join(A.k55, "K55_OLAYLAR.csv.gz")); OK = E2.olay_karsilastir(Ok, VR["O"], VR["EV"]); OK.to_csv(os.path.join(out, "K56_EVREN2_OLAY_SAYILARI.csv"), index=False)
    KP = E2.kapsam_tablosu(Y, R, VR["V"]); KP.to_csv(os.path.join(out, "K56_EVREN2_KAPSAM.csv"), index=False)
    GD = E2.getiri_duyarlilik(VR["P"], VR["EV"], Y); GD.to_csv(os.path.join(out, "K56_EVREN2_GETIRI_DUYARLILIK.csv"), index=False)
    ET = [_etki_kos(A, kk, VR, d, y, isci, "v2") for d, y in (("KESIF", os.path.join(eski_f1, "K56F1_A1_SATIR.csv")), ("IC_DOGRULAMA", os.path.join(eski_ic, "K56IC_SATIR.csv")))]
    bag_not = "koşulmaz (v1.2-C ve v1.3-I: EVREN2 etkisi yalnız KEŞİF ve İÇ; BAĞIMSIZ bir kez açılır)"
    ET = pd.concat(ET, ignore_index=True); ET.to_csv(os.path.join(out, "K56_EVREN2_ETKI.csv"), index=False)
    # duyarlılık: işaretli alt kümeler (SPAC, OTC, ADR, YAKIN kimlik, OTC kuyruğu) hariç evren; yalnız KEŞİF ve İÇ
    hariç = set(DG.sembol[DG.duyarlilik_disi]); Rs = E2.evren2_kur(A, Y[~Y.sembol.isin(hariç)], kl, ek_sha={"duyarlilik": "isaretli_haric"}); VRs = E2.panel_olay(Rs, isci=isci)
    ETs = pd.concat([_etki_kos(A, kk, VRs, d, y, isci, "v2_isaretli_haric") for d, y in (("KESIF", os.path.join(eski_f1, "K56F1_A1_SATIR.csv")), ("IC_DOGRULAMA", os.path.join(eski_ic, "K56IC_SATIR.csv")))], ignore_index=True)
    ETs.to_csv(os.path.join(out, "K56_EVREN2_ETKI_DUYARLILIK.csv"), index=False); kk.tablo().to_csv(os.path.join(out, "K56_EVREN2_KAYNAK_KAYDI.csv"), index=False)
    ozet = {"aday": len(ADAY), "kaynak": ADAY.kaynak.value_counts().to_dict(), "meta_disi": M.evren_disi_on.fillna("").str.split("; ").str[0].replace("", np.nan).dropna().value_counts().to_dict(),
            "fiyat_istenen": int(M.fiyat_iste.sum()), "seri_durum": Y.seri_durum.value_counts().to_dict(), "baglama": M.baglama.value_counts().to_dict(),
            "kimlik_ad": M.kimlik_ad.value_counts().to_dict(), "son_islem": F.get("son_islem", pd.Series(dtype=object)).value_counts().to_dict(),
            "sinif_son_k56": Y.sinif_k56.value_counts().to_dict(), "evren_disi_neden": DG.evren_disi_neden.replace("", np.nan).dropna().value_counts().to_dict(),
            "evrene_giren": int(VR["EV"].kaynak.str.startswith("K56_").sum()), "duyarlilik_haric": len(hariç), "evren_v2_sembol": len(VR["EV"]), "evren_k55_sembol": len(EVk),
            "evren_v2_surum": R["surum"], "dogrulama_sha": sha256_dosya(dy), "bagimsiz": bag_not, "sure_dk": round((time.time() - t0) / 60, 1)}
    L = [f"# K56-EVREN2 BATAN ŞİRKETLERLE EVREN v2 ({kimlik['kimlik']})", "", f"- commit {kimlik['commit']}; evren v2 sürümü {R['surum'][:12]} (K55: 0d00d2c97608, DEĞİŞMEDİ); doğrulama tablosu sha {ozet['dogrulama_sha'][:12]}; süre {ozet['sure_dk']} dk.",
         "- K51-K55 evreni ve sonuçları değişmedi; v2 ayrı sürüm. Getiri (asıl): yeni şirkette pencere seri sonunu aşarsa TANIMSIZ; son işlem fiyatı tasfiye ödemesi sayılmadı; eksik delist getirisi uydurulmadı.",
         f"- Aday {ozet['aday']} ({ozet['kaynak']}); meta aşamasında DIŞI (ilk neden) {ozet['meta_disi']}; fiyatı istenen {ozet['fiyat_istenen']}; seri durumu {ozet['seri_durum']}.",
         f"- Kimlik (Tiingo adı ~ SEC adı): {ozet['kimlik_ad']}; Ö2 CIK bağlama {ozet['baglama']}; son işlem tutarlılığı {ozet['son_islem']}.",
         f"- Son sınıf (K54 kuralı + K56 ayrımı): {ozet['sinif_son_k56']}.", f"- Evren dışı (ilk neden): {ozet['evren_disi_neden']}.",
         f"- Evrene giren yeni şirket {ozet['evrene_giren']}; evren v2 {ozet['evren_v2_sembol']} sembol (K55 {ozet['evren_k55_sembol']}); duyarlılıkta hariç tutulan işaretli {ozet['duyarlilik_haric']}.",
         f"- BAĞIMSIZ etkisi: {bag_not}.", "", "## Olay sayıları (dönem × ufuk)", ""] + _md(OK, list(OK.columns))
    L += ["", "## Aday doğrulama (denetim × sonuç)", ""] + _md(DG.groupby(["kaynak", "evrende"]).size().rename("n").reset_index(), ["kaynak", "evrende", "n"])
    L += ["", "Ön / son sınıf:", ""] + _md(pd.crosstab(F.sinif_on_k56.fillna("-"), F.sinif_son_k56.fillna("-")).reset_index(), list(pd.crosstab(F.sinif_on_k56.fillna("-"), F.sinif_son_k56.fillna("-")).reset_index().columns)) if len(F) else []
    L += ["", "## Yeni şirketlerin tarihsel kapsamı", "", f"- KEŞİF günü olan şirket {int((KP.get('gun_kesif', pd.Series(dtype=float)) > 0).sum())}; İÇ {int((KP.get('gun_ic', pd.Series(dtype=float)) > 0).sum())}; 2024 sonrası verisi olan {int(KP.get('gun_2024_sonrasi_var', pd.Series(dtype=bool)).fillna(False).astype(bool).sum())} (BAĞIMSIZ dönemi kapı dışında sayılmaz).", ""]
    L += _md(KP.groupby(["kaynak", "sinif_k56"]).agg(n=("sembol", "size"), evrende=("evrende", "sum")).reset_index(), ["kaynak", "sinif_k56", "n", "evrende"])
    L += ["", "## Veri eksikleri", ""] + _md(R["yeni"].durum.value_counts().rename("n").reset_index(), ["durum", "n"])
    L += ["", "## Getiri duyarlılığı (A1'i etkilemez: olay ve nitelikli gün tam pencere ister)", ""] + _md(GD, list(GD.columns))
    for ad_, X in (("Etki: 125 KEŞİF satırı (v2 − K55)", ET), ("Duyarlılık: işaretli alt kümeler hariç (v2 − K55)", ETs)):
        L += ["", f"## {ad_}", "", f"- sınıfı değişen satır: {X.groupby('donem').sinif_degisti.sum().to_dict()}; d(i) farkı medyanı {X.groupby('donem').fark_i_d.median().round(4).to_dict()}; "
              f"d(ii) farkı medyanı {X.groupby('donem').fark_ii_d.median().round(4).to_dict()}", ""]
        L += _md(X.sort_values(["donem", "hucre", "varyant", "ufuk"]), ["donem", "hucre", "varyant", "ufuk", "eski_i_n_olay", "i_n_olay", "eski_i_d", "i_d", "eski_ii_d", "ii_d", "eski_sinif_a1", "sinif_a1"])
    open(os.path.join(out, "RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    _json_yaz(os.path.join(out, "K56_KOSU_EVREN2.json"), {**kimlik, **ozet, "kiyas": {"faz1_yerel": os.path.basename(eski_f1), "ic_dogrulama": os.path.basename(eski_ic)}})
    _son_yaz(A, "evren_v2", kimlik, out)
    return {"Y": Y, "R": R, "OK": OK, "ET": ET, "DG": DG, "ozet": ozet}


def evren2_on_denetim(A: K56Ayar, ADAY: pd.DataFrame, kl: str) -> None:
    """EVREN2 kurulmadan önce: (1) Tiingo durum tablosunda her aday fiyat için denenmiş ve son durumu kota değil; (2) SEC özeti var ve bütün Ö1 CIK'lerini
    içeriyor; (3) önbellek yolu kayıtlı. Eksikte durur (sessizce eksik / boş evren kurulmaz)."""
    d = os.path.join(kl, "K56_EVREN2_TIINGO_DURUM.csv")
    if not os.path.exists(d):
        raise FileNotFoundError(f"Tiingo durum tablosu yok: {d} (önbellek {A.onbellek}; K56_ONBELLEK doğru mu, indirme yapıldı mı?)")
    D = pd.read_csv(d); D["tur"] = D.get("tur", pd.Series("fiyat", index=D.index)).fillna("fiyat")
    son = D[D.tur == "fiyat"].groupby("sembol").durum.last()
    eksik = sorted(set(ADAY.sembol) - set(son.index)); kota = sorted(son.index[son == "kota"])
    gecici = sorted(son.index[son.astype(str).str.match(r"hata|HTTP 5")])
    if eksik or kota or gecici:
        raise RuntimeError(f"indirme bitmemiş: denenmemiş {len(eksik)} {eksik[:8]}, kota {len(kota)}, geçici hata {len(gecici)} {gecici[:8]}; önce python K56.py evren2_indir")
    sy = os.path.join(A.onbellek, "evren_v2", "sec_ozet_v2.json")
    if not os.path.exists(sy):
        raise FileNotFoundError(f"SEC özeti yok: {sy} (önbellek yolu {A.onbellek})")
    sec = json.load(open(sy, encoding="utf-8")); o1 = ADAY.cik.dropna().astype(int).astype(str)
    if (~o1.isin(sec)).any():
        raise RuntimeError(f"SEC özetinde {int((~o1.isin(sec)).sum())} Ö1 CIK'i yok: {o1[~o1.isin(sec)].tolist()[:8]}")
    log.info("EVREN2 ön denetim tamam: %d aday, durum %s, önbellek %s", len(ADAY), son.value_counts().to_dict(), A.onbellek)


# ---------------------------------------------------------------- v1.3: kilit, BAĞIMSIZ (bir kez), ayrışma, PBO / DSR, sızıntı sınaması
ATIF = "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01STYdL1uBgkMCqCpF48Chvo"


def _git(*arg, kontrol: bool = True, zaman: int = 120) -> str:
    import subprocess
    from .ortak import KOK
    r = subprocess.run(["git", "-C", KOK, *arg], capture_output=True, text=True, timeout=zaman)
    if kontrol and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(arg[:3])} hata: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def _git_kaydet(dosyalar: List[str], mesaj: str, push: bool = True) -> str:
    """Dosyaları zorla ekler, commit'ler ve dalı push eder (4 deneme, üstel bekleme). Push olmazsa RuntimeError (hesap başlamaz / kayıt eksik sayılır)."""
    import subprocess
    from .ortak import KOK
    _git("add", "-f", *dosyalar)
    if subprocess.run(["git", "-C", KOK, "diff", "--cached", "--quiet"], capture_output=True, timeout=60).returncode != 0:      # değişiklik varsa commit zorunlu
        _git("commit", "-q", "-m", mesaj + ATIF)
    c = _git("rev-parse", "HEAD")
    if push:
        dal = _git("rev-parse", "--abbrev-ref", "HEAD")
        for i in range(4):
            if subprocess_ok(["git", "push", "-u", "origin", dal]) and _git("ls-remote", "origin", f"refs/heads/{dal}", kontrol=False).split("\t")[0] == c:
                return c
            time.sleep(2 ** (i + 1))
        raise RuntimeError("git push başarısız ya da uzak dal yeni commit'i göstermiyor (4 deneme)")
    return c


def subprocess_ok(cmd: List[str]) -> bool:
    import subprocess
    from .ortak import KOK
    return subprocess.run(cmd, cwd=KOK, capture_output=True, timeout=180).returncode == 0


def _kiyas_tabani(A: K56Ayar) -> Dict[str, Any]:
    from .ortak import sha256_dosya
    out = {}
    for alt in ("faz1_yerel", "ic_dogrulama"):
        k = _son_oku(A, alt); out[alt] = {"klasor": os.path.basename(k), "sha": {f: sha256_dosya(os.path.join(k, f)) for f in sorted(os.listdir(k)) if f.endswith((".csv", ".json"))}}
    return out


def kilit_uret_kos(A: K56Ayar) -> Dict[str, Any]:
    """v1.3-D: temiz ağaçta etiket + kilit (kod, ön kayıt, hipotez, eşikler, veri tanımı, kıyas tabanı, ortam). Açılış kaydında K55_125_B varsa reddeder."""
    from .ortak import BAGIMSIZ_KILIT, KILIT_ETIKET_ON, acilis_kaydi, git_kirli, kilit_icerigi, veri_tanimi_hesapla
    gunluk_log()
    Kk = acilis_kaydi(A.cikti); Kk = Kk[Kk.calisma == "K55_125_B"]
    if (Kk.durum.isin(["TAMAMLANDI", "BAŞLADI"])).any() or Kk["not"].astype(str).str.contains("SONUÇ DOSYASI OLUŞTU").any():
        raise RuntimeError("BAĞIMSIZ açılmış ya da sonuç dosyası oluşmuş: kilit yeniden üretilemez")
    if git_kirli():
        raise RuntimeError(f"kod yolları kirli: {git_kirli()[:10]}; önce commit")
    sz = _son_oku(A, "sizinti"); szj = json.load(open(os.path.join(sz, "K56_KOSU_SIZ.json"), encoding="utf-8"))
    from .ortak import KOD_YOLLARI
    kod_farki = subprocess_ok(["git", "diff", "--quiet", str(szj.get("commit")), "HEAD", "--", *KOD_YOLLARI]) is False
    if not str(szj.get("karar", "")).startswith("İÇ hesaplarında 2023-12-31 sonrası bilgiye dolaylı erişim YOK") or kod_farki:
        raise RuntimeError(f"sızıntı sınaması bu commit'te PASS değil: {szj.get('karar')} ({szj.get('commit')})")
    p, o = _panel_yollari(A); vt = veri_tanimi_hesapla(p, o, evren=True, A=A); ic = kilit_icerigi(vt)
    svt = szj.get("veri_tanimi", {})
    bag = {k: (svt.get(k) == vt.get(k)) for k in ("panel_sha", "panel_icerik_sha", "olay_sha", "veri_sha", "ek_veri_sha", "evren_surum")}
    if not all(bag.values()) or szj.get("git_kirli") or szj.get("referans") != os.path.basename(_son_oku(A, "ic_dogrulama")):
        raise RuntimeError(f"sızıntı PASS bu veri / İÇ referansıyla alınmamış: {bag}, kirli {szj.get('git_kirli')}, referans {szj.get('referans')}")
    eksik = [k for k, v in vt.get("ek_veri_dosyalari", {}).items() if v == "YOK"] + [k for k, v in ic["esikler"].items() if isinstance(v, str) and v.startswith("okunamadı")]
    if eksik or not vt.get("panel_icerik_sha"):
        raise RuntimeError(f"kilit üretilemez: eksik / okunamayan girdi {eksik}")
    etiket = KILIT_ETIKET_ON + time.strftime("%Y%m%d-%H%M%S"); c = _git("rev-parse", "HEAD"); _git("tag", etiket, c)
    kil = {**ic, "etiket": etiket, "commit_tam": c, "uretim": time.strftime("%Y-%m-%d %H:%M:%S"), "kiyas_tabani": _kiyas_tabani(A),
           "sizinti": {"kosu": szj.get("kimlik"), "karar": szj.get("karar"), "T2a": szj.get("T2a"), "T2b": szj.get("T2b")},
           "kosu_tanimi": {"K55_125_B": {"donem": "BAGIMSIZ", "b3": True, "yalniz_a1": False, "sinir": None, "duyarlilik": "BAGIMSIZ_B (pencere sonu <= 2026-08-31)"}},
           "not": "BAĞIMSIZ açılmadı; açılış: Cemal kararı (31 Eki) + K56_BAGIMSIZ_AC=1 + python K56.py bagimsiz (bir kez)"}
    kil["kosu_tanimi"]["ayar"] = {"veri": os.path.realpath(A.veri), "k55": os.path.realpath(A.k55), "abd": os.path.realpath(A.abd), "cikti": os.path.realpath(A.cikti),
                                  "panel": os.path.realpath(p), "olay": os.path.realpath(o)}
    y = os.path.join(A.cikti, BAGIMSIZ_KILIT); _json_yaz(y, kil)
    for i in range(5):
        if subprocess_ok(["git", "push", "origin", etiket]):
            break
        if i == 4:
            raise RuntimeError(f"kilit etiketi push edilemedi: {etiket}")
        time.sleep(2 ** (i + 1))
    _git_kaydet([y], f"K56 v1.3 BAĞIMSIZ kilidi ({etiket}; açılmadı)")
    log.info("kilit üretildi: %s %s", etiket, c[:12]); return kil


def bagimsiz_kos(A: K56Ayar, isci: int = 3) -> Dict[str, Any]:
    """v1.3-D: BAĞIMSIZ tek açılış (K55_125_B). Kilit + temiz ağaç -> BAŞLADI kaydı commit + push -> asıl (K55 etiketleri) + duyarlılık (BAGIMSIZ_B)
    -> sonuç dosyaları -> TAMAMLANDI (sonuç sha'ları) commit + push. Çökmede ÇÖKTÜ."""
    from . import faz1_yerel as F1
    from .ortak import BAGIMSIZ_ACILIS, acilis_baslat, acilis_bitir, bagimsiz_kilit_dogrula, sha256_dosya
    gunluk_log()
    if os.environ.get("K56_BAGIMSIZ_AC") != "1":
        raise RuntimeError("K56_BAGIMSIZ_AC=1 yok (Cemal kararı)")
    from .ortak import REPO_CIKTI
    if os.path.realpath(A.cikti) != os.path.realpath(REPO_CIKTI):
        raise RuntimeError(f"BAĞIMSIZ yalnız repo çıktı klasöründen açılır ({REPO_CIKTI}); A.cikti {A.cikti}")
    bagimsiz_kilit_dogrula(A.cikti); A.ag = False
    kil = json.load(open(os.path.join(A.cikti, "K56_BAGIMSIZ_KILIT.json"), encoding="utf-8")); ay = kil.get("kosu_tanimi", {}).get("ayar", {})
    p, o = ay.get("panel", ""), ay.get("olay", "")                       # panel / olay yolu kilitten (ortam değişkeninden değil)
    simdi = {"veri": os.path.realpath(A.veri), "k55": os.path.realpath(A.k55), "abd": os.path.realpath(A.abd), "cikti": os.path.realpath(A.cikti), "panel": os.path.realpath(p), "olay": os.path.realpath(o)}
    if simdi != ay or os.path.realpath(_panel_yollari(A)[0]) != os.path.realpath(p):
        raise RuntimeError(f"koşu ayarları / panel yolu kilitle aynı değil: {simdi} != {ay}")
    if _kiyas_tabani(A) != kil.get("kiyas_tabani"):
        raise RuntimeError("kıyas tabanı (F1A / IC SON koşuları) kilitten sonra değişmiş")
    kimlik = kosu_kimligi(A, "BAG"); out = _kosu_klasoru(A, "bagimsiz", kimlik); kk = KaynakKaydi()
    acilis_baslat("K55_125_B", kimlik, A.cikti); kayit = os.path.join(A.cikti, BAGIMSIZ_ACILIS)
    try:
        _git_kaydet([kayit], f"K56 BAĞIMSIZ açılış kaydı: BAŞLADI ({kimlik['kimlik']})")
    except Exception as ex:
        acilis_bitir("K55_125_B", kimlik, "ÇÖKTÜ", A.cikti, notu=f"push yok, hesap başlamadı: {ex}"); raise
    os.environ["K56_BAGIMSIZ_KIMLIK"] = kimlik["kimlik"]; os.environ["K56_BAGIMSIZ_KLASOR"] = A.cikti; dosyalar = []; b_not = ""
    try:
        R = F1.calistir(A, kk, "BAGIMSIZ", p, o, isci=isci, b3=True, veri_dondur=True)
        for ad, X in (("K56BAG_SATIR.csv", R["S"]), ("K56BAG_HUCRE.csv", R["H"]), ("K56BAG_B3.csv", R["B3"]), ("K56BAG_BILESIM.csv", R["Bl"])):
            X.to_csv(os.path.join(out, ad), index=False); dosyalar.append(ad)
        VERI = R.pop("VERI")
        ek = ["- Tek açılış (K55_125_B); testler v1.2-B / v1.3-D, ölçütler İÇ ile aynı; yeni eşik / değişken yok. Asıl: K55 kod etiketleri; duyarlılık: BAGIMSIZ_B "
              "(K55 ön kaydı v1.2-2: pencere sonu <= 2026-08-31), ayrı tablolar (K56BAG_B_*)."]
        faz1_yaz(out, "K56-BAG BAĞIMSIZ DOĞRULAMA 2024-26 (asıl: K55 etiketleri)", kimlik, R, ek); os.rename(os.path.join(out, "RAPOR.md"), os.path.join(out, "RAPOR_ASIL.md"))
        NK = k55_nihai_karar(R["S"], R["H"], R["B3"]); _json_yaz(os.path.join(out, "K56BAG_K55_NIHAI_KARAR.json"), NK)
        open(os.path.join(out, "K56BAG_K55_NIHAI_KARAR.md"), "w", encoding="utf-8").write(f"# {NK['karar']}\n\n" + "\n".join(f"- {x}" for x in NK["notlar"]) + "\n")
        _git_kaydet([os.path.join(out, f) for f in os.listdir(out)], f"K56 BAĞIMSIZ asıl sonuçlar ve K55 nihai karar ({kimlik['kimlik']})")   # asıl sonuç, B'den önce kalıcı
        try:                                                              # duyarlılık: K55 ön kaydı v1.2-2 pencere tanımı (aynı açılış; çökmesi asıl sonucu düşürmez)
            bagimsiz_b_etiketle(VERI); Rb = F1.calistir(A, kk, "BAGIMSIZ_B", None, None, isci=isci, b3=True, veri=VERI)
            for ad, X in (("K56BAG_B_SATIR.csv", Rb["S"]), ("K56BAG_B_HUCRE.csv", Rb["H"]), ("K56BAG_B_B3.csv", Rb["B3"]), ("K56BAG_B_BILESIM.csv", Rb["Bl"])):
                X.to_csv(os.path.join(out, ad), index=False); dosyalar.append(ad)
            faz1_yaz(out, "K56-BAG BAĞIMSIZ DUYARLILIK (BAGIMSIZ_B pencere tanımı)", kimlik, Rb, ek); os.rename(os.path.join(out, "RAPOR.md"), os.path.join(out, "RAPOR_DUYARLILIK_B.md"))
        except Exception as exb:
            Rb = {"S": pd.DataFrame(columns=["sinif_a1"]), "H": pd.DataFrame()}; b_not = f"DUYARLILIK-B çöktü: {type(exb).__name__}: {str(exb)[:150]}"; log.error(b_not)
        kk.tablo().to_csv(os.path.join(out, "K56BAG_KAYNAK_KAYDI.csv"), index=False)
        sha = {f: sha256_dosya(os.path.join(out, f)) for f in dosyalar}
        _json_yaz(os.path.join(out, "K56_KOSU_BAG.json"), {**kimlik, "k55_nihai": NK["karar"], "sonuc_sha": sha, "sure_dk": R["sure_dk"], "b1_gecen": int(R["S"].b1_gecti.sum()), "b2": R["S"].sinif_a1.value_counts().to_dict(),
                                                           "b3": R["B3"].karar.value_counts().to_dict() if len(R["B3"]) else {}, "b_b2": Rb["S"].sinif_a1.value_counts().to_dict()})
        _son_yaz(A, "bagimsiz", kimlik, out); acilis_bitir("K55_125_B", kimlik, "TAMAMLANDI", A.cikti, notu="sonuç sha: " + ",".join(f"{k}:{v[:10]}" for k, v in sha.items()) + (f"; {b_not}" if b_not else ""))
    except Exception as ex:
        if dosyalar:
            acilis_bitir("K55_125_B", kimlik, "ÇÖKTÜ", A.cikti, notu=f"SONUÇ DOSYASI OLUŞTU ({len(dosyalar)}); yeniden koşu yok: {type(ex).__name__}: {str(ex)[:150]}")
        else:
            acilis_bitir("K55_125_B", kimlik, "ÇÖKTÜ", A.cikti, notu=f"sonuç dosyası yok: {type(ex).__name__}: {str(ex)[:150]}")
        _git_kaydet([kayit] + [os.path.join(out, f) for f in os.listdir(out)], f"K56 BAĞIMSIZ açılış kaydı: ÇÖKTÜ ({kimlik['kimlik']})"); raise
    finally:
        os.environ.pop("K56_BAGIMSIZ_KIMLIK", None); os.environ.pop("K56_BAGIMSIZ_KLASOR", None)
    _git_kaydet([kayit] + [os.path.join(out, f) for f in os.listdir(out)] + [os.path.join(A.cikti, "bagimsiz", "SON.json")], f"K56 BAĞIMSIZ sonuçları ve açılış kaydı: TAMAMLANDI ({kimlik['kimlik']})")
    return {"S": R["S"], "H": R["H"], "B3": R["B3"], "Sb": Rb["S"], "Hb": Rb["H"]}


def bagimsiz_b_etiketle(VERI: Dict[str, Any]) -> None:
    """v1.3-D duyarlılık: BAGIMSIZ_B etiketi (t0 2024-01-15..2026-06-05, pencere sonu <= 2026-08-31) panel donem{h} ve olay tablosu donem sütunlarında,
    yerinde (öteki etiketler değişmez)."""
    from K55.ortak import EMBARGO_TAKVIM_GUN, OLAY
    a = pd.Timestamp("2024-01-01") + pd.Timedelta(days=EMBARGO_TAKVIM_GUN); t0s = pd.Timestamp("2026-06-05"); bs = pd.Timestamp("2026-08-31"); P = VERI["P"]; O = VERI["O"]
    for _, (h, _e) in OLAY.items():
        m = (P.tarih >= a) & (P.tarih <= t0s) & pd.to_datetime(P[f"bitis{h}"]).notna() & (pd.to_datetime(P[f"bitis{h}"]) <= bs)
        P.loc[m.to_numpy(), f"donem{h}"] = "BAGIMSIZ_B"
    ob = (O.tarih >= a) & (O.tarih <= t0s) & (pd.to_datetime(O.bitis) <= bs); O.loc[ob.to_numpy(), "donem"] = "BAGIMSIZ_B"


def ayrisma_kos(A: K56Ayar, isci: int = 3) -> Dict[str, Any]:
    """v1.3-E: ayrışma KEŞİF + İÇ (gerçek) ve dört Faz 0 + iki kalibre yapay spek; satır / hücre kararları; BAĞIMSIZ yok."""
    from . import ayrisma as AY, faz1_yerel as F1, mekanizma as M
    from .mekanizma_raporu import _md
    gunluk_log(); A.ag = False; kimlik = kosu_kimligi(A, "AYR"); out = _kosu_klasoru(A, "ayrisma", kimlik); kk = KaynakKaydi(); p, o = _panel_yollari(A); t0 = time.time()
    K = M.kesif_satirlari(A, kk); VR = F1.k55_veri(A, kk, p, o)
    S, Dz = AY.calistir("gercek", VR["P"], VR["V"], VR["O"], K, ("KESIF", "IC_DOGRULAMA"), isci=isci); del VR
    Ss, Dzs = [], []
    for tur, toh in tuple(M.SENTETIK_SPEK) + (("kalibre_gjr", 565), ("kalibre_sicrama", 566)):
        R = AY.sentetik_motor_verisi(tur, toh, M.SENTETIK_HISSE, M.SENTETIK_GUN); s_, d_ = AY.calistir(f"sent:{tur}:{toh}", R["P"], R["V"], R["O"], K, ("KESIF",), isci=isci)
        s_["spek"] = tur; s_["tohum"] = toh; d_["spek"] = tur; Ss.append(s_); Dzs.append(d_); del R
    SS = pd.concat(Ss, ignore_index=True); karar = []
    faz0 = {(t, h) for t, h in M.SENTETIK_SPEK}
    for r in S.itertuples():
        g = SS[(SS.hucre == r.hucre) & (SS.varyant == r.varyant) & (SS.ufuk == r.ufuk)]
        sinif = {f"{x.spek}:{x.tohum}": M.sentetik_sinif(x.G, x.G_ay_alt, x.G_ay_ust, r.G) for x in g.itertuples()}
        sk = AY.spek_cogunluk([v for k, v in sinif.items() if (k.split(":")[0], int(k.split(":")[1])) in faz0])
        karar.append({"hucre": r.hucre, "varyant": r.varyant, "ufuk": r.ufuk, "donem": r.donem, "sent_siniflar": json.dumps(sinif, ensure_ascii=False), "sent_cogunluk": sk,
                      "G_sent_ort": float(g[g.spek.isin(["gauss", "garch_t"])].G.mean()) if len(g) else np.nan, "karar": AY.satir_karari(r._asdict(), sk)})
    KR = pd.DataFrame(karar); S2 = S.merge(KR, on=["hucre", "varyant", "ufuk", "donem"], how="left")
    from .faz1_yerel import hucre_karari
    H = S2.groupby(["donem", "hucre"]).agg(satir=("ufuk", "size"), karar=("karar", lambda s: hucre_karari(list(s)))).reset_index()
    S2.to_csv(os.path.join(out, "K56AYR_SATIR.csv"), index=False); H.to_csv(os.path.join(out, "K56AYR_HUCRE.csv"), index=False); SS.to_csv(os.path.join(out, "K56AYR_SENTETIK.csv"), index=False)
    Dz.to_csv(os.path.join(out, "K56AYR_DIZI.csv.gz"), index=False); pd.concat(Dzs, ignore_index=True).groupby(["spek", "ufuk"]).L.describe().to_csv(os.path.join(out, "K56AYR_DIZI_SENTETIK_OZET.csv"))
    kk.tablo().to_csv(os.path.join(out, "K56AYR_KAYNAK_KAYDI.csv"), index=False)
    L = [f"# K56-AYR (iii) / BÜTÜN GÜNLER AYRIŞMASI ({kimlik['kimlik']})", "", f"- commit {kimlik['commit']}; süre {round((time.time() - t0) / 60, 1)} dk. Ön kayıt v1.3-E; BAĞIMSIZ koşulmadı.", "",
         "## Özet (sayılardan)", ""]
    for d, g in S2.groupby("donem"):
        L.append(f"- {d}: satır kararları {g.karar.value_counts().to_dict()}; hücre {H[H.donem == d].karar.value_counts().to_dict()}; E1 medyanı {g.E1.median():+.3f}, E2 medyanı "
                 f"{g.E2.median():+.3f}, G medyanı {g.G.median():+.3f}; kimlik farkı en çok {np.nanmax(np.abs(g.kimlik_fark)):.1e}; (iii) 200 çekiliş ortalaması − E1 en çok "
                 f"{np.nanmax(np.abs(g.iii_cekilis_ort - g.E1)):.3f}; L ortalaması medyanı {g.L_ort.median():.1f}, P(L=1) medyanı {g.L_P1.median():.2f}.")
    L.append(f"- Yapay (Faz 0 spekleri): G medyanı {SS[SS.spek.isin(['gauss', 'garch_t'])].G.median():+.3f}, E1 {SS[SS.spek.isin(['gauss', 'garch_t'])].E1.median():+.3f}, "
             f"E2 {SS[SS.spek.isin(['gauss', 'garch_t'])].E2.median():+.3f}; kalibre: G medyanı {SS[SS.spek.str.startswith('kalibre')].G.median():+.3f}.")
    L += ["", "Konum bantları (olay ağırlıklı, medyan):", ""] + _md(S2.groupby("donem")[[c for c in S2.columns if c.startswith("bant") and not c.endswith(("_alt", "_ust", "_n"))]].median().round(3).reset_index(),
                                                                     ["donem"] + [c for c in S2.columns if c.startswith("bant") and not c.endswith(("_alt", "_ust", "_n"))])
    L += ["", "## Hücreler", ""] + _md(H, list(H.columns)) + ["", "## Satırlar", ""]
    L += _md(S2.sort_values(["donem", "hucre", "varyant", "ufuk"]), ["donem", "hucre", "varyant", "ufuk", "n_gecerli", "E1", "E2", "G", "G_ay_alt", "G_ay_ust", "G_sembol_yil_alt", "G_sent_ort", "sent_cogunluk", "karar"])
    open(os.path.join(out, "RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    _json_yaz(os.path.join(out, "K56_KOSU_AYR.json"), {**kimlik, "karar": {d: g.karar.value_counts().to_dict() for d, g in S2.groupby("donem")}, "sure_dk": round((time.time() - t0) / 60, 1)})
    _son_yaz(A, "ayrisma", kimlik, out); return {"S": S2, "H": H, "SS": SS}


def pbo_kos(A: K56Ayar, isci: int = 3) -> Dict[str, Any]:
    """v1.3-F: PBO / DSR (KEŞİF + İÇ), bir kez, BAĞIMSIZ açılmadan önce."""
    from . import faz1_yerel as F1, mekanizma as M, pbo_dsr as PB
    from .mekanizma_raporu import _md
    from K55.faz1 import DALLAR, hucreleri_kur
    from K55.hucreler import HUCRELER
    gunluk_log(); A.ag = False; kimlik = kosu_kimligi(A, "PBO"); out = _kosu_klasoru(A, "pbo_dsr", kimlik); kk = KaynakKaydi(); p, o = _panel_yollari(A)
    K = M.kesif_satirlari(A, kk); VR = F1.k55_veri(A, kk, p, o); hucreleri_kur(DALLAR); yk = {h: int(HUCRELER[h].get("yon", 1)) for h in K.hucre.unique()}
    Y, T, mats = PB.calistir(VR["P"], VR["V"], K, yk, isci=isci)
    Y.to_csv(os.path.join(out, "K56PBO_YAPI.csv"), index=False); T.to_csv(os.path.join(out, "K56PBO_SONUC.csv"), index=False)
    for ad, Mx in mats.items():
        Mx.to_csv(os.path.join(out, f"K56PBO_AYLIK_{ad}.csv"))
    L = [f"# K56-PBO PBO / DEFLATED SHARPE (KEŞİF + İÇ) ({kimlik['kimlik']})", "", f"- commit {kimlik['commit']}; ön kayıt v1.3-F; K55 ön kaydı §7. BAĞIMSIZ kullanılmadı.", ""] + _md(T, list(T.columns))
    open(os.path.join(out, "RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n"); _json_yaz(os.path.join(out, "K56_KOSU_PBO.json"), {**kimlik, "sonuc": T.to_dict("records")})
    _son_yaz(A, "pbo_dsr", kimlik, out); return {"Y": Y, "T": T}


def sizinti_kos(A: K56Ayar, isci: int = 3, mod: str = "hepsi") -> Dict[str, Any]:
    """v1.3-G: T0 (yeniden üretim), T1 (aynı evren, kesik fiyat; T1b kesik / T1a tam başvuru özeti), T2a / T2b (kesik evren). Karşılaştırma tolerans 0."""
    from . import faz1_yerel as F1, sizinti_denetimi as SZ
    from .mekanizma_raporu import _md
    gunluk_log(); A.ag = False; kimlik = kosu_kimligi(A, "SIZ"); out = _kosu_klasoru(A, "sizinti", kimlik); kk = KaynakKaydi(); p, o = _panel_yollari(A); t0 = time.time()
    ref_kl = _son_oku(A, "ic_dogrulama"); ref = {"S": pd.read_csv(os.path.join(ref_kl, "K56IC_SATIR.csv")), "H": pd.read_csv(os.path.join(ref_kl, "K56IC_HUCRE.csv")),
                                                  "B3": pd.read_csv(os.path.join(ref_kl, "K56IC_B3.csv")), "Bl": pd.read_csv(os.path.join(ref_kl, "K56IC_BILESIM.csv"))}
    oz: Dict[str, Any] = {"referans": os.path.basename(ref_kl)}; L = [f"# K56-SIZ İÇ → BAĞIMSIZ DOLAYLI ERİŞİM SINAMASI ({kimlik['kimlik']})", "", f"- commit {kimlik['commit']}; referans İÇ koşusu {oz['referans']}.", ""]
    if mod in ("hepsi", "T0"):
        oz["T0"] = SZ.t0_yeniden_uretim(A, p, o, isci); L += [f"- T0 yeniden üretim: {oz['T0']}"]
    def kos(ad, VR, ref_t):
        R = F1.calistir(A, kk, "IC_DOGRULAMA", None, None, isci=isci, b3=True, veri=VR)
        yeni = {"S": _csv_yuvarla(R["S"]), "H": _csv_yuvarla(R["H"]), "B3": _csv_yuvarla(R["B3"]), "Bl": _csv_yuvarla(R["Bl"])}
        for k_, X in yeni.items():
            X.to_csv(os.path.join(out, f"K56SIZ_{ad}_{k_}.csv"), index=False)
        F, z = SZ.karsilastir(ref_t, yeni); F.to_csv(os.path.join(out, f"K56SIZ_{ad}_FARK.csv"), index=False); return R, yeni, F, z
    if mod in ("hepsi", "T1"):
        VR = SZ.kesik_veri(A, "IC_DOGRULAMA", "", isci); R1, y1, F1_, z1 = kos("T1b", VR, ref); oz["T1b"] = z1
        Bl_a = F1.bilesim(VR["P"], VR["V"], VR["O"], VR["J_tam"], _cikmap(A), "IC_DOGRULAMA"); Bl_a = _csv_yuvarla(Bl_a); Bl_a.to_csv(os.path.join(out, "K56SIZ_T1a_Bl.csv"), index=False)
        Fa, za = SZ.karsilastir({"Bl": ref["Bl"]}, {"Bl": Bl_a}); Fa.to_csv(os.path.join(out, "K56SIZ_T1a_FARK.csv"), index=False); oz["T1a_bilesim"] = za
        L += [f"- T1b (kesik fiyat + kesik başvuru özeti) vs İÇ: {z1}", f"- T1a bileşim (tam başvuru özeti) vs İÇ: {za}"]; del VR
        for ev in ("a", "b"):
            if mod != "hepsi":
                break
            VR = SZ.kesik_veri(A, "IC_DOGRULAMA", ev, isci); R2, y2, F2_, z2 = kos(f"T2{ev}", VR, y1); oz[f"T2{ev}"] = z2
            dF = F2_[F2_.sutun.isin(["i_d", "ii_d", "iii_d"])].copy(); dF["f"] = [abs(_fark(a_, b_)) for a_, b_ in zip(dF.ref, dF.yeni)]
            dmax = float(dF.f.max()) if len(dF) else 0.0; sinif = int(F2_.sutun.isin(["sinif_a1", "sinif_iii", "b1_gecti", "karar", "a1", "b1_durum", "(satır)"]).sum())
            Sr = y1["S"].set_index(["hucre", "varyant", "ufuk"]); yari = {}
            for c_ in ("i_d", "ii_d", "iii_d"):
                for k_, v_ in ((Sr[f"{c_}_ust"] - Sr[f"{c_}_alt"]) / 2).items():
                    yari[(c_, "|".join(map(str, k_)))] = v_
            asan = int(sum(1 for r in dF.itertuples() if np.isfinite(r.f) and r.f > 0.25 * yari.get((r.sutun, r.anahtar), np.inf)))
            oz[f"T2{ev}"].update({"en_buyuk_d_farki": dmax, "sinif_degisimi": sinif, "yari_genislik_25_asan": asan, "ihmal_edilebilir": bool(sinif == 0 and dmax <= 0.05 and asan == 0)})
            L += [f"- T2{ev} (kesik evren{' + kesim sonrası giren K34 dışarıda' if ev == 'b' else ''}) vs T1b: {oz[f'T2{ev}']}"]; del VR
    oz["sure_dk"] = round((time.time() - t0) / 60, 1)
    from .ortak import veri_tanimi_hesapla
    oz["veri_tanimi"] = {k: v for k, v in veri_tanimi_hesapla(p, o, evren=True, A=A).items() if k not in ("veri_dosyalari", "ek_veri_dosyalari")}; oz["git_kirli"] = kimlik.get("git_kirli", [])
    t1 = oz.get("T1b", {}).get("birebir", {}); t1a = oz.get("T1a_bilesim", {}).get("birebir", {}); t0_ = oz.get("T0", {})
    gecti = (mod == "hepsi" and t0_.get("panel_esit") and t0_.get("olay_esit") and all(t1.get(k) for k in ("S", "H", "B3")) and t1a.get("Bl"))
    oz["karar"] = ("İÇ hesaplarında 2023-12-31 sonrası bilgiye dolaylı erişim YOK (T0 yeniden üretim + T1b S / H / B3 + T1a bileşim birebir)" if gecti
                   else f"GEÇMEDİ: mod {mod}, T0 {t0_.get('panel_esit')} / {t0_.get('olay_esit')}, T1b {t1}, T1a {t1a} — İÇ geçersiz sayılır, BAĞIMSIZ açılmaz (açıklanana kadar)")
    L += ["", f"## Karar: {oz['karar']}", "", "Görünmeyen sınırlamalar (T1 / T2 ölçemez; beyan): hayatta kalma (evren 2026'da işlem görenler + K34), 2026 sürümü bölünme / temettü düzeltmesi, "
          "güncel sektör / CIK etiketleri; BAĞIMSIZ dönem K51-K54 programında test dönemi olarak kullanıldı."]
    open(os.path.join(out, "RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n"); _json_yaz(os.path.join(out, "K56_KOSU_SIZ.json"), {**kimlik, **oz})
    _son_yaz(A, "sizinti", kimlik, out); return oz


def _csv_yuvarla(X: pd.DataFrame) -> pd.DataFrame:
    """Referans CSV'den okunmuş gibi karşılaştırmak için yazıp okur (dtype / NaN biçimi aynı)."""
    import io
    b = io.StringIO(); X.to_csv(b, index=False); b.seek(0); return pd.read_csv(b)


def _fark(a: Any, b: Any) -> float:
    try:
        return float(b) - float(a)
    except Exception:
        return float("inf")


def _cikmap(A: K56Ayar) -> Dict[str, int]:
    k = pd.read_csv(os.path.join(A.k55, "K55_EVREN.csv")); return {r.sembol: int(r.cik) for r in k.dropna(subset=["cik"]).itertuples()}


def k55_nihai_karar(S: pd.DataFrame, H: pd.DataFrame, B3: pd.DataFrame) -> Dict[str, Any]:
    """v1.3-H eşlemesi (sonuç görülmeden yazıldı; mekanik). Girdi: BAĞIMSIZ asıl koşusunun satır / hücre / B3 tabloları. DUYARLILIK-B, ayrışma, PBO / DSR ve
    EVREN2 kararı değiştirmez. Dönüş: karar metni, notlar, sayılar."""
    sat = S.sinif_a1.value_counts().to_dict() if len(S) else {}; huc = H.a1.value_counts().to_dict() if len(H) else {}
    b1 = int(S.b1_gecti.sum()) if "b1_gecti" in S else 0; b3 = B3.karar.value_counts().to_dict() if len(B3) and "karar" in B3 else {}
    notlar = ["KEŞİF ve İÇ'te seçimsiz kontrolle gerçek etki 0 / 125 (K56-F1A, K56-IC); K55 B KEŞİF 0 TUTAR, İÇ 0 / 64."]
    olculemedi = (not len(S)) or S.sinif_a1.astype(str).str.startswith("TANIMSIZ").all()
    if olculemedi:
        karar = "K55 NİHAİ: İZ YOK (BAĞIMSIZ ölçülemedi; KEŞİF + İÇ'e göre)"
    elif (H.a1 == "GERÇEK ETKİ KALIYOR").any():
        karar = "K55 NİHAİ: İZ YOK korunur + TEK DÖNEM SAPMASI notu"
        notlar.append(f"BAĞIMSIZ'da çoğunluğu GERÇEK ETKİ KALIYOR olan hücre: {H[H.a1 == 'GERÇEK ETKİ KALIYOR'].hucre.tolist()}; KEŞİF ve İÇ'te seçimsiz etki yok, tek dönem tekrar "
                      "sayılmaz; yeni hipotez ancak ayrı ön kayıtla ve K55 dışı veride (Avrupa).")
    elif (H.a1 == "MEKANİK").sum() > len(H) / 2:
        karar = "K55 NİHAİ: İZ YOK — ters yönlü farklar olay tanımının seçim eseri (KEŞİF, İÇ, BAĞIMSIZ)"
    else:
        karar = "K55 NİHAİ: İZ YOK (BAĞIMSIZ kısmen ölçüldü / belirsiz: hücrelerin çoğu MEKANİK değil, GERÇEK ETKİ de değil)"
        tb = {k: v for k, v in sat.items() if str(k).startswith(("TANIMSIZ", "BELİRSİZ"))}; notlar.append(f"BAĞIMSIZ hücre sınıfları: {huc}; TANIMSIZ / BELİRSİZ satırlar: {tb}.")
    dag = {k: v for k, v in sat.items() if k in ("GERÇEK ETKİ KALIYOR", "KISMEN MEKANİK", "TERS KALINTI")}
    if dag:
        notlar.append(f"Dağınık satırlar (iz sayılmaz): {dag}.")
    notlar.append(f"B1 (K55 A, ilk geçiş) BAĞIMSIZ'da geçen satır {b1} / {len(S)}: destek sayılmaz (seçim etkisi tekrarı; İÇ'te B1 119 / 125, B2 0).")
    if b3.get("TUTAR", 0):
        notlar.append(f"B3 TUTAR {b3['TUTAR']} varyant ({B3[B3.karar == 'TUTAR'].varyant.tolist()}): tek dönemde tuttu, İZ DEĞİL; yeni eşik aranmaz.")
    notlar.append("Üst sınır: Avrupa olmadan en fazla ABD-ADAY (CLAUDE.md); DOĞRULANDI için K55 ön kaydına göre AVR şart. Karar yeni eşikle kurtarılmaz (Cemal madde 9).")
    return {"karar": karar, "notlar": notlar, "satir_b2": sat, "hucre_b2": huc, "b1_gecen": b1, "b3": b3}
