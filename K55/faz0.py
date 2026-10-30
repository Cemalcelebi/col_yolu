"""K55 Faz 0 sürücüsü (Cemal'in 30 Ekim onayı): 1 veri kalitesi, 2 fonsuz evren, 3 ortak panel, 4 sembol / şirket eşleştirme kontrolü,
5 sızıntı testleri, 6 birim / sentetik testler (test_k55.py ayrı), 7 deneme koşusu (ornek = 50), 8 rapor. İz arama sonucu optimize edilmez.
"""
from __future__ import annotations

import os
import time
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd

from .eslestirme import eslestir
from .evren import evren_daralt, evren_kur, ornek_sec
from .hucre import degisken_ekle, hucre_kos, yontem_A
from .hucreler import HUCRELER
from .olay_tanimlari import olay_tekillik_denetimi, olaylar
from .istatistik import coklu_test_ozeti
from .ortak import DONEM, FDR_Q, K55Ayar, cikti_dogrula, cy, gunluk_log, kosu_kimligi, log, veri_sha
from .panel import panel_kaydet, panel_kur
from .raporlama import faz0_yaz, sizinti_yaz, veri_kapsami_yaz
from .sizinti import eslesme_testi, gelecek_degisken, kesme_testi, olay_etiketi_testi, rastgele_degisken_uret
from .veri_kalitesi import evren_kalite

KESIF_IC = ("KESIF", "IC_DOGRULAMA")          # Faz 0 denetimleri yalnız bu dönemlerde; BAĞIMSIZ kilitli


def sizinti_testleri(P: pd.DataFrame, V: Dict[str, pd.DataFrame], O: pd.DataFrame, likit_map: Dict[str, np.ndarray], rng: np.random.Generator, tohum: int) -> Dict[str, Any]:
    S: Dict[str, Any] = {}
    # (a) kesme testi: her kayıtlı hücre, 3 sembol × 4 nokta
    semboller = sorted(V)[:: max(1, len(V) // 3)][:3]; kes_ok = True; ayrinti = {}
    for kimlik, t in HUCRELER.items():
        hs = 0
        for s in semboller:
            d = V[s]; n = len(d); r = kesme_testi(t["fonk"], d, [n // 2, int(n * 0.7), int(n * 0.9), n - 1]); hs += r["hata_sayi"]
        ayrinti[kimlik] = hs; kes_ok &= hs == 0
    S["a_kesme_testi"] = {"gecti": kes_ok, "hucre_hata": ayrinti, "sembol": semboller}
    # (a2) dedektör: geleceğe bakan değişken kesme testinde KALMALI
    hs = sum(kesme_testi(gelecek_degisken, V[s], [len(V[s]) // 2, len(V[s]) - 70])["hata_sayi"] for s in semboller)
    S["a2_kesme_dedektor"] = {"gecti": hs > 0, "gelecek_degisken_hata": hs, "not": "hata > 0 beklenir (dedektör çalışıyor)"}
    # (d) olay etiketi: olaylı 3 sembol
    oy = O[O.ufuk == "Y60"]; ok = True; say = 0
    for s in oy.sembol.unique()[:3]:
        t0 = int(oy[oy.sembol == s].i.iloc[0]); d = V[s]
        if t0 + 61 < len(d):
            r = olay_etiketi_testi(d, likit_map[s], t0); ok &= r["gecti"]; say += 1
    S["d_olay_etiketi"] = {"gecti": ok and say > 0, "sinanan_olay": say}
    # (b) olumlu kontrol: t+60 getirisi (gelecek) -> A yönteminde büyük etki; (c) olumsuz: rastgele -> etki yok (KESIF + IC)
    P["_gelecek"] = degisken_ekle(P, V, gelecek_degisken, "_gelecek"); P["_rastgele"] = degisken_ekle(P, V, rastgele_degisken_uret(tohum), "_rastgele")
    ra = yontem_A(P, O, "_gelecek", "Y60", rng, KESIF_IC); rb = yontem_A(P, O, "_rastgele", "Y60", rng, KESIF_IC)
    S["b_olumlu_kontrol"] = {"gecti": bool(ra.get("n_olay", 0) >= 10 and ra.get("d", 0) > 1.0 and ra.get("auc", 0) > 0.8), "n_olay": ra.get("n_olay"), "d": ra.get("d"), "auc": ra.get("auc")}
    # olumsuz kontrol: rastgele değişkenin etkisi sıfırdan ayrılmamalı (ay kümeli aralık sıfırı kapsar, |d| < 0,30, AUC 0,5 ± 0,08)
    S["c_olumsuz_kontrol"] = {"gecti": bool(rb.get("n_olay", 0) >= 10 and abs(rb.get("d", 9)) < 0.30 and rb.get("d_alt", 1) < 0 < rb.get("d_ust", -1) and 0.42 < rb.get("auc", 0) < 0.58),
                              "n_olay": rb.get("n_olay"), "d": rb.get("d"), "d_alt": rb.get("d_alt"), "d_ust": rb.get("d_ust"), "auc": rb.get("auc")}
    # (e) eşleşmiş kontrol: sinyal örneği -> kontroller tarih toleransı içinde, sembol farklı
    D = P[P.likit & P.r60_tanimli & (P.vd >= 0) & P.donem60.isin(KESIF_IC)]
    if len(D) > 100:
        sin = D.sample(min(300, len(D)), random_state=tohum); M = eslestir(D, sin, D, rng=rng); X = pd.concat([sin, M], axis=1)
        S["e_eslesme"] = {**eslesme_testi(X[X.kontrol_n > 0], D), "eslesmeyen_pay": float((X.kontrol_n == 0).mean())}
    else:
        S["e_eslesme"] = {"gecti": False, "not": "likit tanımlı satır yetersiz"}
    P.drop(columns=["_gelecek", "_rastgele"], inplace=True)
    return S


def faz0(A: Optional[K55Ayar] = None, paketler: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    A = A or K55Ayar(); gunluk_log(); A.cikti = cikti_dogrula(A.cikti); os.makedirs(A.cikti, exist_ok=True)    # v1.2 madde 8: çıkış yolu denetimi
    sure: Dict[str, float] = {}; durum: Dict[str, str] = {}; rng = np.random.default_rng(A.tohum)
    t = time.time(); vsha = veri_sha(A); sure["veri_sha"] = round(time.time() - t, 1)                      # v1.2 madde 4: veri sha zorunlu (eksik -> durur)
    if not os.path.exists(os.path.join(A.veri, "endeks.pkl")):
        raise FileNotFoundError("endeks.pkl yok; Faz 0'da endeks indirilmez (network=False)")
    t = time.time(); E = evren_kur(A, vsha, network=False); V, EV, surum = E["V"], E["EV"], E["surum"]
    tam_n = len(EV); E["disi"].to_csv(os.path.join(A.cikti, "K55_EVREN_DISI.csv"), index=False); E["kesim"].to_csv(os.path.join(A.cikti, "K55_KESIM.csv"), index=False)
    E["k54_sorun"].to_csv(os.path.join(A.cikti, "K55_K54_TUTARLILIK.csv"), index=False)
    disi_say = E["disi"].kategori.value_counts().to_dict() if len(E["disi"]) else {}
    if A.ornek:
        EVo, dag = ornek_sec(EV, A.ornek, A.tohum); V, EV = evren_daralt(V, EV, EVo); dag.to_csv(os.path.join(A.cikti, "K55_ORNEKLEM.csv"), index=False)
        log.info("deneme örneklemi: %d sembol %s; eksik tabaka %s", len(EV), EV.sinif.value_counts().sort_index().to_dict(), dag[dag.eksik > 0].tabaka.tolist())
    else:
        dag = pd.DataFrame()
    sure["evren"] = round(time.time() - t, 1); durum["evren"] = f"{len(EV)} sembol; dışlama {disi_say}; 4b kesim {len(E['kesim'])}; V/EV tutarlılık {'geçti' if E['tutarlilik']['gecti'] else 'KALDI'}"
    kimlik = kosu_kimligi(A, surum, paketler, vsha); kimlik["evren_dosya_sha"] = E["dosya_sha"]
    t = time.time(); Q, ozet = evren_kalite(V, EV); Q.to_csv(os.path.join(A.cikti, "K55_VERI_KALITESI.csv"), index=False)
    ozet["dislama_kategorileri"] = disi_say; ozet["kisa_seri_yukleyici_disi"] = int(disi_say.get("kisa_seri_yukleyici", 0)); ozet["kesim_4b"] = E["kesim"][["sembol", "once", "sonra", "atilan"]].to_dict("records")
    ozet["v_ev_tutarlilik"] = E["tutarlilik"]; ozet["orneklem_eksik_tabaka"] = dag[dag.eksik > 0][["tabaka", "kota", "aday", "secilen", "eksik"]].to_dict("records") if len(dag) else []
    EV.to_csv(os.path.join(A.cikti, "K55_EVREN.csv"), index=False); sure["kalite"] = round(time.time() - t, 1); durum["veri_kalitesi"] = f"eksiksiz {ozet['eksiksiz']} / {ozet['sembol']}"
    C = cy(); Ac = C.CYAyar(veri=A.veri, cikti=A.cikti, pazarlar=("ABD",)); endeks = C.cy_endeks(Ac, C.CY)
    t = time.time(); P, likit_map, bilgi = panel_kur(V, EV, A, endeks); sure["panel"] = bilgi["sure_sn"]
    os.makedirs(os.path.join(A.cikti, "panel"), exist_ok=True); pyol = panel_kaydet(P, os.path.join(A.cikti, "panel", f"k55_panel_{A.ornek or 'tam'}.pkl"))
    durum["panel"] = f"{bilgi['satir']} satır, {bilgi['likit_satir']} likit"
    t = time.time(); O, say = olaylar(V, likit_map); tek = olay_tekillik_denetimi(O); sure["olaylar"] = round(time.time() - t, 1)
    O.to_csv(os.path.join(A.cikti, "K55_OLAYLAR.csv.gz"), index=False, compression="gzip"); durum["olaylar"] = f"{len(O)} olay, tekillik {'geçti' if tek.get('gecti') else 'KALDI'}"
    t = time.time(); S = sizinti_testleri(P, V, O, likit_map, rng, A.tohum); sure["sizinti"] = round(time.time() - t, 1); durum["sizinti"] = "hepsi geçti" if all(r.get("gecti") for r in S.values()) else "KALAN VAR"
    # hücre iskelesi: kayıtlı hücreler, yalnız KESIF (İÇ DOĞRULAMA adaylar için saklanır; BAĞIMSIZ hiç açılmaz)
    t = time.time(); rows = []
    for kimlik_h, tanim in HUCRELER.items():
        rows += hucre_kos(kimlik_h, tanim, P, V, O, rng, donemler=("KESIF",), ufuklar=("Y60",))
    H = pd.DataFrame(rows); H.to_csv(os.path.join(A.cikti, "K55_HUCRE_ISKELE.csv"), index=False); sure["hucre_iskele"] = round(time.time() - t, 1)
    durum["hucre_motoru"] = f"{len(H)} satır (A / B / C), hata yok"
    Hc, yuk = coklu_test_ozeti(H[H.p.notna()] if "p" in H else H, FDR_Q); yuk.to_csv(os.path.join(A.cikti, "K55_COKLU_TEST.csv"), index=False)   # v1.2 madde 7: test yükü
    # tam evren tahmini
    n = max(1, len(EV)); olcek = tam_n / n
    tam = {"sembol": tam_n, "panel_satir_tahmini": int(bilgi["satir"] * olcek), "bellek_GB_tahmini": round(bilgi["satir"] * olcek * 30 * 4 / 1e9, 2),
           "panel_sn": round(sure["panel"] * olcek, 0), "olaylar_sn": round(sure["olaylar"] * olcek, 0), "sizinti_sn": round(sure["sizinti"] * olcek, 0),
           "hucre_basina_sn_tahmini": round(sure["hucre_iskele"] * olcek / max(1, len(HUCRELER)), 0), "isci": A.isci, "not": "Faz 1 = 80 OHLCV hücresi × (5 pencere) × 3 yöntem; bootstrap 2.000"}
    R = {"kimlik": kimlik, "kalite_ozet": ozet, "panel_bilgi": bilgi, "sizinti": S, "hucre": H, "coklu_test": yuk, "sure": sure, "tekillik": tek, "modul_durum": durum, "olay_donem": O.groupby(["ufuk", "donem"]).size().to_dict() if len(O) else {}, "evren_disi": E["disi"], "kesim": E["kesim"], "orneklem": dag,
         "moduller_ok": bool(tek.get("gecti") and all(r.get("gecti") for r in S.values()) and len(H)), "tam_tahmin": tam, "panel_yol": pyol, "EV": EV, "O": O, "Q": Q}
    veri_kapsami_yaz(Q, ozet, bilgi, O, say, A.cikti, kimlik); sizinti_yaz(S, A.cikti); faz0_yaz(R, A.cikti); durum["rapor"] = "yazıldı"
    log.info("FAZ 0 bitti: %s; süreler %s", durum, sure)
    return R
