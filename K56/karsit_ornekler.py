"""K56 karşıt örnekler: grup tasarımı (ONKAYIT_K56 5) ve Faz 0 küçük erişim örneklemi.

Grup tasarımı Faz 1 mekanizma testlerinin zorunlu parçasıdır: bir mekanizma yalnız yükselenlerde (G1) görülüyorsa kabul edilmez; aynı belirtiyi
gösterip yükselmeyenler (G2), batanlar (G3), büyük düşenler (G4), hisse sayısı artanlar (G5), birleşme / satın almayla çıkanlar (G6) ve sektör ×
likidite eşli rastgele (G7) aynı ölçüyle raporlanır. Faz 0 örneklemi yalnız veri ERİŞİMİNİ sınar (hipotez testi değil).
"""
from __future__ import annotations

import os
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from .ortak import K56Ayar, KaynakKaydi

GRUPLAR: List[Dict[str, str]] = [
    {"grup": "G1", "ad": "Olay (büyük yükseliş)", "tanim": "K55 olay tanımı (Y60 +%30 / Y120 +%50 / Y250 +%100; giriş t0+1 açılışı; örtüşmez); M01 sonucu "
     "MEKANİK AÇIKLAR ise olay günü yerine 'ileri getiri tabanlı' tanım (sinyal günü sabit, olay = ileri getiri üst %5) kullanılır", "kaynak": "K55_OLAYLAR (K55 kodu)"},
    {"grup": "G2", "ad": "Aynı belirti, yükseliş yok", "tanim": "aynı gün, aynı oynaklık ondalığı (vd), likidite üçlüsü (lt), sektör ve sınanan belirtinin aynı beşte "
     "biri; ±60 işlem gününde olay yok; olay başına 5 eş", "kaynak": "K55 panel"},
    {"grup": "G3", "ad": "Sonradan iflas / tasfiye", "tanim": "K54 sınıf 2 (SEC 8-K 1.03 / Tiingo); belirtinin iflastan önceki 250 günde görülme sıklığı", "kaynak": "K54_SIRKET_DURUMU"},
    {"grup": "G4", "ad": "Büyük düşüş", "tanim": "ileri 60 günde −%30 ve altı (Y60'ın aynası); aynı tanım kuralı", "kaynak": "K55 panel"},
    {"grup": "G5", "ad": "Hisse sayısı ciddi artan", "tanim": "XBRL dei:EntityCommonStockSharesOutstanding (bildirim tarihine göre) 12 ayda > %20 artış", "kaynak": "SEC companyfacts"},
    {"grup": "G6", "ad": "Birleşme / satın alma", "tanim": "K54 sınıf 3 + SEC DEFM14A / SC TO-T / 8-K 2.01 tarihleri", "kaynak": "K54 + SEC submissions"},
    {"grup": "G7", "ad": "Sektör × likidite eşli rastgele", "tanim": "aynı gün, sektör, likidite üçlüsü; belirtiden bağımsız rastgele 5 eş", "kaynak": "K55 panel"},
]
OLCULER = ("n_olay", "n_hisse", "mekanizma_sikligi", "yanlis_pozitif_orani", "kesinlik", "etki", "etki_alt", "etki_ust")


def grup_tasarimi() -> pd.DataFrame:
    T = pd.DataFrame(GRUPLAR); T["raporlanan"] = ", ".join(OLCULER); return T


def ornek_sec(A: K56Ayar, kk: KaynakKaydi, n: int = 12) -> pd.DataFrame:
    """Faz 0 erişim örneklemi (tohumlu, tekrarsız): G1 4 (K55 Y60 KEŞİF olayı, sınıf 1, CIK'li), G2 4 (G1 olay gününde aynı sektör ve likidite
    üçlüsü, olay gününden en az 1 yıl önce ve 90 gün sonra işlemde, ±90 takvim gününde Y60 olayı yok), G3 2 (sınıf 2), G6 2 (sınıf 3). n < 12 verilirse oranlar korunarak kısaltılır."""
    rng = np.random.default_rng(A.tohum)
    EV = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_EVREN.csv"), "orneklem_secimi", "erişim örneklemi: sınıf, CIK, sektör, likidite"))
    O = pd.read_csv(kk.oku(os.path.join(A.k55, "K55_OLAYLAR.csv.gz"), "orneklem_secimi", "erişim örneklemi: G1 olay günleri"), parse_dates=["tarih"])
    EV = EV[EV.cik.notna() & (EV.cik > 0)].copy(); EV["cik"] = EV.cik.astype(int)
    kota = {"G1": 4, "G2": 4, "G3": 2, "G6": 2}
    if n < 12:
        kota = {"G1": max(1, n // 3), "G2": max(1, n // 3), "G3": max(1, n // 6), "G6": max(1, n - 2 * max(1, n // 3) - max(1, n // 6))}
    y60 = O[(O.ufuk == "Y60") & (O.donem == "KESIF")]
    s1 = EV[(EV.sinif == 1) & (EV.kaynak == "V_ABD") & EV.sektor.notna() & (EV.sektor.astype(str).str.lower() != "bilinmiyor")]
    aday = y60[y60.sembol.isin(s1.sembol)].drop_duplicates("sembol")
    sec: List[Dict[str, Any]] = []; kullanilan = set()
    for i in rng.permutation(len(aday)):
        if sum(1 for r in sec if r["grup"] == "G1") >= kota["G1"]:
            break
        r = aday.iloc[i]; e = s1[s1.sembol == r.sembol].iloc[0]
        if e.sektor in {x["sektor"] for x in sec}:
            continue
        sec.append({"grup": "G1", "sembol": r.sembol, "cik": int(e.cik), "tarih": r.tarih, "sektor": e.sektor, "lik_uclu": int(e.lik_uclu), "not": f"Y60 olayı, getiri {r.getiri:+.2f}"})
        kullanilan.add(r.sembol)
    for g1 in [r for r in sec if r["grup"] == "G1"][: kota["G2"]]:
        yakin = y60[(y60.tarih - g1["tarih"]).abs() <= pd.Timedelta(days=90)].sembol
        islemde = (pd.to_datetime(s1.ilk_islem) <= g1["tarih"] - pd.Timedelta(days=365)) & (pd.to_datetime(s1.son_islem) >= g1["tarih"] + pd.Timedelta(days=90))
        es = s1[islemde & (s1.sektor == g1["sektor"]) & (s1.lik_uclu == g1["lik_uclu"]) & ~s1.sembol.isin(yakin) & ~s1.sembol.isin(kullanilan)]
        if not len(es):
            es = s1[islemde & (s1.sektor == g1["sektor"]) & ~s1.sembol.isin(yakin) & ~s1.sembol.isin(kullanilan)]
        if len(es):
            e = es.iloc[int(rng.integers(len(es)))]; kullanilan.add(e.sembol)
            sec.append({"grup": "G2", "sembol": e.sembol, "cik": int(e.cik), "tarih": g1["tarih"], "sektor": e.sektor, "lik_uclu": int(e.lik_uclu), "not": f"{g1['sembol']} eşi, ±90 günde olay yok"})
    for g, sinif in (("G3", 2), ("G6", 3)):
        a = EV[(EV.sinif == sinif) & ~EV.sembol.isin(kullanilan)]
        for i in rng.permutation(len(a))[: kota[g]]:
            e = a.iloc[i]; kullanilan.add(e.sembol)
            sec.append({"grup": g, "sembol": e.sembol, "cik": int(e.cik), "tarih": pd.to_datetime(e.son_islem), "sektor": e.sektor, "lik_uclu": int(e.lik_uclu) if pd.notna(e.lik_uclu) else -1,
                        "not": f"sınıf {sinif} ({e.cikis_islemi}), son işlem {e.son_islem}"})
    T = pd.DataFrame(sec)
    if T.sembol.duplicated().any():
        raise RuntimeError("erişim örnekleminde yinelenen sembol")
    return T
