"""K66 testleri (ağ gerekmez; yalnız SENTETİK veri, gerçek veride getiri ölçmez). Çalıştırma: python test_k66.py

1) çakışma kapısı (_CK_ONCE_K66)  2) ön kayıt mührü (üzerine yazmama, bozuk / farklı mühür reddi, eşik / tanım / karar sırası değişince mühür değişir,
kapsamdaki seçim kuralı mühürle çelişince yazmama; gerçek K66_ON_KAYIT.md varsa bugünkü eşiklerle aynı)  3) FINRA dosya ayrıştırma (tırnaklı / tırnaksız aynı;
ad alanında tek '"'; 403 / XML reddi; yinelenen kod; ödeme günü uyuşmazlığı)  4) indirme (sahte indirici; ağ yok): aday günler, 403 sonraki adaya geçer, var olan
dosyaya istek atılmaz, bozuk gövde yazılmaz  5) BİLGİ TARİHİ kuralı (ödeme + 12 işlem günü; 'bilgi < t'; r0 elle)  6) değişkenler elle (SI_PAY bölünmeli /
bölünmesiz, DTC, SI_DEG bölünme düzeltmesi ve düzeltilemeyen bayrak, SI_DEG1)  7) GELECEĞE BAKMA YOK: bilgi günü >= t olan raporlar ve t'den sonraki pay
bozulunca t ve öncesi değişkenler aynı  8) isim denetimi ve sembol eşleme (eski kodu başka şirkete ait satır düşer, çakışan kod dışarıda)  9) karar sırası seçim
kuralı (toplanma -> İÇ, yoksa EVREN)  10) kapsam modu getiri hesaplamaz  11) uçtan uca sentetik koşu (git'li): ön kayıt yokken / işlenmemişken / değişmişken
`kos` reddeder; çıktılar, K64 fonksiyonlarıyla S1 / karar, rapor  12) e-posta / anahtar yok.
"""
from __future__ import annotations

import copy
import os
import re
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K66 as K  # noqa: E402
import test_k60 as TK  # noqa: E402
import test_k64 as TK64  # noqa: E402

FI, K60, K64 = K.FI, K.K60, K.K64
E0 = K.K66_ESIK
BAS = "|".join(K.K66_FINRA_SUTUN)


def finra_metin(odeme: str, satirlar: list, tirnak: bool = False) -> bytes:
    """Sentetik FINRA dosyası. satır = (kod, ad, sınıf, si, si_once, bolunme, adv, dtc, revizyon, degisim)."""
    g = odeme.replace("-", ""); out = [BAS if not tirnak else "|".join(f'"{c}"' for c in K.K66_FINRA_SUTUN)]
    for kod, ad, sinif, si, so, bol, adv, dtc, rev, deg in satirlar:
        al = [g, kod, ad, "A", sinif, f"{si:.0f}", f"{so:.0f}", "S" if bol else "", f"{adv:.0f}", f"{dtc:.2f}", "R" if rev else "", f"{deg:.2f}", f"{si - so:.0f}", odeme]
        if tirnak:
            al = [f'"{x}"' if x != "" else "" for x in al]
        out.append("|".join(al))
    return ("\n".join(out) + "\n").encode()


def durmali(f, ad: str, hata: list, tur=None) -> None:
    try:
        f(); hata.append(ad)
    except (tur or K.K66Hata):
        pass


def sentetik_finra(klasor: str, S: list, D: dict, V: dict = None, tohum: int = 21, bozuk_isim: int = 9, eksik: int = 11, cakisan: bool = False) -> list:
    """Sentetik FINRA dosyaları (aday listesinin ilk günü = ödeme günü). SI = oran x o günkü pay (bölünmeli hisselerde o günkü birim). V verilirse ADV = V hacminin
    FINRA penceresindeki ortalaması / b (o günkü birim; kimlik denetiminden geçer). bozuk_isim hissesinin 2020 öncesi satırları başka şirketindir (başka ad, 50 kat
    ADV); hisse 3'te ADV = 0; eksik hissesi her 5. dosyada yok. Döner: ödeme günleri."""
    rng = np.random.default_rng(tohum); os.makedirs(klasor, exist_ok=True); od = []; once = {}; onceki = None
    for _y, ad in K.k66_finra_adaylar():
        g = ad[0]; t = pd.Timestamp(g); od.append(t); sat = []; bas = onceki if onceki is not None else t - pd.Timedelta(days=14); onceki = t
        for j, s in enumerate(S):
            if j == eksik and len(od) % 5 == 0:
                continue
            pay_o = 1.0e7                                               # o günkü pay birimi: 1e7 x t'ye kadar olan bölünmeler (demetin pay kayıtlarıyla aynı)
            for bs, (bd, br) in D["bolunme"].items():
                if bs == s:
                    pay_o *= float(np.prod(br[bd <= t.to_datetime64()]))
            si = float(rng.uniform(0.005, 0.25) * pay_o); so = once.get(s, si * rng.uniform(0.8, 1.2)); adv = float(rng.uniform(1e4, 5e5))
            if V is not None:
                vv = V[s].Volume[(V[s].index > bas) & (V[s].index <= t)]; b = 1.0
                for bs, (bd, br) in D["bolunme"].items():
                    if bs == s:
                        b = float(np.prod(br[bd > t.to_datetime64()]))
                adv = float(vv.mean()) / b * rng.uniform(0.9, 1.1) if len(vv) >= 3 else 0.0
            adv = 0.0 if j == 3 else (adv * 50 if (j == bozuk_isim and t.year < 2020) else adv)
            isim = (f"Baska{j} Holding" if (j == bozuk_isim and t.year < 2020) else f"Sirket{j} Inc.")
            sat.append((s, isim, "OTC" if j == 2 else "NNM", si, so, j == 6 and t == pd.Timestamp("2018-09-14"), adv, max(si / adv, 1.0) if adv else 999.99,
                        j % 7 == 0, (si / so - 1) * 100 if so > 0 else 100.0))
            once[s] = si
        if cakisan:
            sat.append(("XYZ", "Xyz Corp", "NYSE", 1000.0, 900.0, False, 500.0, 2.0, False, 11.11))
        with open(os.path.join(klasor, f"shrt{g}.csv"), "wb") as f:
            f.write(finra_metin(t.strftime("%Y-%m-%d"), sat, tirnak=t.year >= 2023))
    return od


def testler() -> list:
    hata = []; nan = np.nan
    # 1) çakışma kapısı
    src = open(os.path.join(KOK, "K66.py"), encoding="utf-8").read().replace("from __future__ import annotations\n", "")
    g = {"__name__": "kapi_test", "k66_kos": object(), "_CK_KAYIT": {"k66_kos": "BASKA.py"}}
    try:
        exec(compile(src, "K66.py", "exec"), g); hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi_test2"}
    try:
        exec(compile(src, "K66.py", "exec"), g2); exec(compile(src, "K66.py", "exec"), g2)
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    if "_CK_ONCE_K66 = " not in src or "_cakisma_kontrol_k66()" not in src:
        hata.append("1) çakışma kapısı adı _CK_ONCE_K66 değil")
    # 2) ön kayıt mührü
    if K.k66_kodlar() != ["SI_PAY", "DTC", "SI_DEG", "SI_DEG1"]:
        hata.append("2) değişken listesi iş tanımındaki gibi değil")
    F = E0["finra"]
    if not (E0["kriz"] == "2026-08-31" and [d[0] for d in E0["donem"]] == ["2018-2021", "2022-2026", "2023-2026"] and E0["bagimsiz"] == ["2018-2021", "2022-2026"]
            and E0["pazar"] == ["ABD"] and E0["olay"] == K64.K64_ESIK["olay"] and E0["maliyet"] == {"ABD": 0.0020} and E0["coklu"]["bh_q"] == 0.10
            and E0["s1"]["n_esik"] == 30 and F["bilgi_gecikme_islem"] == 12 and F["deg_rapor"] == 6 and F["ilk"] == "2017-12-29"
            and E0["sira"]["karar"]["K66"] in ("IC", "EVREN") and E0["sira_secim"] == {"n_min": 30, "oran_min": 0.5}
            and all(E0["s1"][k] == K64.K64_ESIK["s1"][k] for k in ("bootstrap", "guven", "gecerli_pay", "n_esik"))):
        hata.append("2) K66_ESIK sabitleri iş tanımındaki gibi değil")
    if [K64.k64_karar_sirasi(k, E0) for k in K.k66_kodlar()] != [E0["sira"]["karar"]["K66"]] * 4:
        hata.append("2) karar sırası bütün aile için aynı değil")
    Es = [copy.deepcopy(E0) for _ in range(4)]
    Es[0]["finra"]["bilgi_gecikme_islem"] = 11; Es[1]["degisken"][2]["tanim"] += " "; Es[2]["sira"]["karar"]["K66"] = "EVREN" if E0["sira"]["karar"]["K66"] == "IC" else "IC"
    Es[3]["donem"][0][1] = "2017-01-01"
    if len({K.k66_esik_sha()} | {K.k66_esik_sha(e) for e in Es}) != 5 or K.k66_esik_sha() != K.k66_esik_sha(copy.deepcopy(E0)):
        hata.append("2) eşik / tanım / karar sırası / dönem değişince mühür değişmiyor ya da aynı eşikte mühür farklı")
    vs = {"V_ABD.pkl": ("b" * 64, 1), "k66_finra": ("c" * 64, 209)}
    with tempfile.TemporaryDirectory() as td:
        y = K.k66_onkayit(td, veri_sha=vs); ilk = open(y, encoding="utf-8").read()
        if f"ESIK_SHA256: {K.k66_esik_sha()}" not in ilk or not re.search(r"^Yazım zamanı: \d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC", ilk, re.M):
            hata.append("2) ön kayıtta mühür / UTC zaman yok")
        for parca in (("## Veri", "## 0. Soru", "## 1. Olay", "## 2. Evren", "## 3. Değişkenler", "## 4. S1", "## 5. S2", "## 6. Cetvel", "## 7. Hücreler", "## 8. Çoklu test",
                      "## 9. GÜÇ BEYANI", "## 10. Yanlılık beyanı", "## 11. SAPMA / BOŞLUK", "## 12. Kapsam", "## 13. Çıktılar", "## 14. Değişmezlik", "EK KATKI VAR", "ÖLÇÜLEMEZ",
                      "ABD-ADAY", "BIST VERİSİ YOK", "ÖDÜNÇ ÜCRETİ", "IBorrowDesk", "YAŞAYAN YANLILIĞI", "Benjamini-Hochberg", "python -I K66.py kos", "BİLGİ TARİHİ", "KİMLİK DENETİMİ", "SAPMA 5.",
                      "+ **12 işlem günü**", "7. iş gününde", "Kapsam sayımı görüldü, getiri görülmedi", "float", "OTC", "SAPMA 1.", "SAPMA 2.", "K58")
                      + tuple(f"BOŞLUK {i}." for i in range(1, 10)) + tuple(f"| {k} | " for k in K.k66_kodlar())):
            if parca not in ilk:
                hata.append(f"2) ön kayıtta '{parca}' yok")
        if K64._k64_onkayit_oku(y)["veri"] != vs:
            hata.append("2) ön kayıttan veri sha256'ları okunamadı")
        K.k66_onkayit(td)
        if open(y, encoding="utf-8").read() != ilk:
            hata.append("2) ön kayıt üzerine yazıldı")
        durmali(lambda: K.k66_onkayit_dogrula(td, git=True), "2) git'e işlenmemiş ön kayıt kabul edildi", hata)
        open(y, "w", encoding="utf-8").write(ilk.replace(K.k66_esik_sha(), "0" * 64))
        durmali(lambda: K.k66_onkayit_dogrula(td), "2) bozuk mühür kabul edildi", hata)
        durmali(lambda: K.k66_onkayit(td), "2) mührü farklı ön kayıt sessizce kabul edildi", hata)
    with tempfile.TemporaryDirectory() as td:     # kapsamdaki seçim kuralı mühürdeki karar sırasıyla çelişirse ön kayıt yazılmaz
        ters = "EVREN" if E0["sira"]["karar"]["K66"] == "IC" else "IC"; n_u, n_a = (200, 190) if ters == "EVREN" else (5, 400)
        pd.DataFrame([{"tanim": "K24", "pazar": "ABD", "donem": d, "degisken": k, "n_ust": n_u, "n_alt": n_a} for d in E0["bagimsiz"] for k in K.k66_kodlar()]).to_csv(K._k66_yol("kapsam", td), index=False)
        durmali(lambda: K.k66_onkayit(td, veri_sha=vs), "2) seçim kuralıyla çelişen karar sırasıyla ön kayıt yazıldı", hata)
    gercek = K._k66_yol("onkayit")
    if os.path.exists(gercek):
        try:
            oc = K.k66_onkayit_dogrula()
            if not oc["zaman_utc"] or len(oc["veri"]) < 9:
                hata.append(f"2) gerçek ön kayıtta UTC zaman / veri sha256 eksik ({len(oc['veri'])} kaynak)")
        except K.K66Hata as ex:
            hata.append(f"2) gerçek ön kayıt bugünkü eşiklerle tutmuyor: {ex}")
    # 3) FINRA dosya ayrıştırma
    sat = [("AAA", "Alpha Inc.", "NYSE", 1000, 800, False, 400, 2.5, False, 25.0), ("BBB", 'Beta "B" Corp', "OTC", 50, 0, True, 0, 999.99, True, 100.0),
           ("CCC", "Gamma", "NNM", 10, 20, False, 100, 1.0, False, -50.0), ("CCC", "Gamma2", "NNM", 11, 20, False, 100, 1.0, False, -45.0)]
    try:
        A = K.k66_finra_ayristir(finra_metin("2019-03-15", sat[:3]), "20190315"); Bq = K.k66_finra_ayristir(finra_metin("2019-03-15", sat[:3], tirnak=True), "20190315")
        cols = ["kod", "sinif", "si", "si_once", "adv", "dtc_dosya", "deg_yuzde", "bolunme", "revizyon"]
        if not (A[cols].equals(Bq[cols]) and A.ad.iloc[1] == 'Beta "B" Corp' and A.si.tolist() == [1000, 50, 10] and A.bolunme.tolist() == [False, True, False]
                and A.revizyon.tolist() == [False, True, False] and A.attrs["odeme"] == pd.Timestamp("2019-03-15")):
            hata.append("3) tırnaklı / tırnaksız dosya aynı ayrıştırılmadı ya da alanlar yanlış")
        Y = K.k66_finra_ayristir(finra_metin("2019-03-15", sat), "20190315")
        if Y.attrs["yinelenen"] != 2 or "CCC" in set(Y.kod):
            hata.append("3) yinelenen kod atılmadı")
    except K.K66Hata as ex:
        hata.append(f"3) geçerli dosya reddedildi: {ex}")
    durmali(lambda: K.k66_finra_ayristir(b'<?xml version="1.0" encoding="UTF-8"?><Error><Code>AccessDenied</Code></Error>'), "3) 403 / XML gövdesi kabul edildi", hata)
    durmali(lambda: K.k66_finra_ayristir(finra_metin("2019-03-15", sat[:2]), "20190329"), "3) ödeme günü dosya adıyla uyuşmayan dosya kabul edildi", hata)
    # 4) indirme (sahte indirici)
    ad = K.k66_finra_adaylar(); gunler = [g for _y, a in ad for g in a]
    if not (ad[0] == ("2017-12-son", ["20171229"]) and all(pd.Timestamp(g).weekday() < 5 for g in gunler) and min(gunler) == "20171229" and max(gunler) <= "20260831"
            and ad[1][1][0] == "20180115" and len(ad) == 2 * (12 * 8 + 8) + 1):
        hata.append("4) aday ödeme günleri yanlış")
    E4 = copy.deepcopy(E0); E4["finra"].update({"ilk": "2019-03-01", "son": "2019-04-30", "bekle": 0.0}); istek = []

    def sahte(gun):
        istek.append(gun)
        if gun in ("20190315", "20190329", "20190415"):
            return 200, finra_metin(f"{gun[:4]}-{gun[4:6]}-{gun[6:]}", sat[:2])
        if gun == "20190430":
            return 200, b"<?xml version='1.0'?><Error/>"
        return 403, b""
    with tempfile.TemporaryDirectory() as td:
        r = K.k66_finra_indir(td, sahte, E4); dos = sorted(os.listdir(td))
        if not (dos == ["k66_indir.json", "shrt20190315.csv", "shrt20190329.csv", "shrt20190415.csv"] and r["yeni"] == 3 and r["bulunamadi"] == ["2019-04-son"]
                and "20190331" not in istek and istek.index("20190329") > istek.index("20190315")):
            hata.append(f"4) indirme sonucu beklenen gibi değil ({dos}, {r['yeni']}, {r['bulunamadi']})")
        istek.clear(); r2 = K.k66_finra_indir(td, sahte, E4)
        if any(g in istek for g in ("20190315", "20190329", "20190415")) or r2["vardi"] != 3:
            hata.append("4) var olan dosya için yeniden istek atıldı")
    # 5) BİLGİ TARİHİ kuralı
    tak = pd.bdate_range("2019-01-01", "2019-06-28"); od = np.array(["2019-01-15", "2019-01-31", "2019-02-16", "2019-02-28"], "datetime64[D]")
    bi = K.k66_bilgi_indeksi(od, tak)
    el = [tak.get_loc(pd.Timestamp("2019-01-15")) + 12, tak.get_loc(pd.Timestamp("2019-01-31")) + 12, tak.get_loc(pd.Timestamp("2019-02-18")) + 12, tak.get_loc(pd.Timestamp("2019-02-28")) + 12]
    if bi.tolist() != el:
        hata.append(f"5) bilgi günü = ödeme + 12 işlem günü değil ({bi.tolist()} != {el})")
    r0 = K.k66_son_rapor(bi, len(tak))
    for i in range(len(tak)):
        beklenen = max([r for r in range(len(od)) if el[r] < i], default=-1)
        if r0[i] != beklenen:
            hata.append(f"5) r0 elle hesapla aynı değil (gün {i}: {r0[i]} != {beklenen})"); break
    if not (r0[el[0]] == -1 and r0[el[0] + 1] == 0):
        hata.append("5) bilgi günü = t olan rapor t'de kullanıldı ('bilgi < t' kuralı)")
    durmali(lambda: K.k66_son_rapor(np.array([5, 3]), 10), "5) artmayan bilgi günleri kabul edildi", hata)
    # 6) değişkenler elle (sentetik demet: hisse 5 ters bölünme 2019-06-03, hisse 6 4:1 bölünme 2018-09-04)
    D = TK.sentetik_demet(N=40, tohum=4); S = list(D["sembol"]); V = TK64.sentetik_fiyat(S); T = D["temel"]; bol = D["bolunme"]
    M = K64.k64_fiyat_matrisleri(V, K64.K64_ESIK); takv = M["takvim"]
    with tempfile.TemporaryDirectory() as td:
        odl = sentetik_finra(td, S, D, V); Fp = K.k66_finra_panel(S, td)
    hacim = K.k66_hacim_matris(V, takv, S); kim, lo = K.k66_kimlik(Fp, hacim, takv, bol); Fp = {**Fp, "kimlik_ok": kim}
    durmali(lambda: K.k66_degiskenler({k: v for k, v in Fp.items() if k != "kimlik_ok"}, takv, np.full((len(takv), len(S)), 1e7), bol), "6) kimlik denetimsiz panel kabul edildi", hata)
    pay = K.k66_pay_matris(T, takv.to_numpy("datetime64[D]"), S, bol); X, bil = K.k66_degiskenler(Fp, takv, pay, bol)
    tv = takv.to_numpy("datetime64[D]"); bie = np.searchsorted(tv, Fp["odeme"]) + 12

    def elle_pay(j: int, gun: np.datetime64) -> float:
        kd, kn, kb = T["pay"][j]; m = kb < gun; d = kd[m][np.argmax(kd[m])]; c = 1.0
        if S[j] in bol:
            bd, br = bol[S[j]]; c = float(np.prod(br[bd > d.astype("datetime64[ns]")]))
        return float(kn[m][np.argmax(kd[m])]) * c

    def b_(j: int, r: int) -> float:
        if S[j] not in bol:
            return 1.0
        bd, br = bol[S[j]]
        return float(np.prod(br[bd > Fp["odeme"][r].astype("datetime64[ns]")]))
    kontrol = 0
    for gun in ("2018-11-20", "2019-05-21", "2019-06-25", "2021-03-10", "2024-07-16"):
        i = takv.get_loc(pd.Timestamp(gun)); r = max(q for q in range(len(bie)) if bie[q] < i)
        for j in (0, 1, 5, 6, 9, 11):
            ok = Fp["var"][r, j] and Fp["kimlik_ok"][r, j]
            si = Fp["si"][r, j]; adv = Fp["adv"][r, j]
            sp = si * b_(j, r) / elle_pay(j, np.datetime64(gun)) if ok else nan
            dtc = si / adv if ok and adv > 0 else nan
            r6 = r - 6; ok6 = r6 >= 0 and Fp["var"][r6, j] and Fp["kimlik_ok"][r6, j]
            bay = any(Fp["bolunme"][q, j] for q in range(r6 + 1, r + 1)) if ok6 else False
            bil_ = S[j] in bol and any((bol[S[j]][0] > Fp["odeme"][r6].astype("datetime64[ns]")) & (bol[S[j]][0] <= Fp["odeme"][r].astype("datetime64[ns]"))) if ok6 else False
            dg = np.log(si * b_(j, r) / (Fp["si"][r6, j] * b_(j, r6))) if ok and ok6 and not (bay and not bil_) else nan
            bil1 = S[j] in bol and any((bol[S[j]][0] > Fp["odeme"][r - 1].astype("datetime64[ns]")) & (bol[S[j]][0] <= Fp["odeme"][r].astype("datetime64[ns]")))
            dg1 = Fp["deg_yuzde"][r, j] / 100 if ok and Fp["si_once"][r, j] > 0 and not Fp["bolunme"][r, j] and not bil1 else nan
            for k, v in (("SI_PAY", sp), ("DTC", dtc), ("SI_DEG", dg), ("SI_DEG1", dg1)):
                x = float(X[k][i, j])
                if not (np.isclose(x, v, rtol=1e-5) if np.isfinite(v) else np.isnan(x)):
                    hata.append(f"6) {k} elle hesapla aynı değil ({gun}, hisse {j}: {x} != {v})")
                kontrol += int(np.isfinite(v))
    if kontrol < 60:
        hata.append(f"6) elle denetlenen dolu değer az ({kontrol})")
    i5a, i5b = takv.get_loc(pd.Timestamp("2019-05-21")), takv.get_loc(pd.Timestamp("2019-06-25"))
    if not (0.004 < X["SI_PAY"][i5a, 5] < 0.26 and 0.004 < X["SI_PAY"][i5b, 5] < 0.26 and 0.004 < X["SI_PAY"][i5a, 6] < 0.26):
        hata.append(f"6) bölünmeli hissede SI_PAY bugünkü birimde değil ({X['SI_PAY'][i5a, 5]}, {X['SI_PAY'][i5b, 5]}, {X['SI_PAY'][i5a, 6]})")
    if np.isfinite(X["DTC"][:, 3]).any():
        hata.append("6) ADV = 0 olan hissede DTC hesaplandı")
    # bölünme bayrağı: hisse 6'nın 2018-09-14 raporunda bayrak var, K60 kaydında 2018-09-04 bölünmesi var -> düzeltilir (değer var); kayıt silinince yok
    rb = int(np.searchsorted(Fp["odeme"], np.datetime64("2018-09-14")))
    gun_b = [i for i in range(len(takv)) if bil["r0"][i] == rb + 2]
    if gun_b:
        ib = gun_b[0]; X2, _b = K.k66_degiskenler(Fp, takv, pay, {k: v for k, v in bol.items() if k != S[6]})
        if not (np.isfinite(X["SI_DEG"][ib, 6]) and np.isnan(X2["SI_DEG"][ib, 6]) and np.isfinite(X2["SI_DEG"][ib, 1])):
            hata.append("6) düzeltilemeyen bölünme bayrağında SI_DEG yok sayılmadı / düzeltilebilende hesaplanmadı")
    # 7) GELECEĞE BAKMA YOK
    for gun in ("2019-06-25", "2022-03-15"):
        i0 = takv.get_loc(pd.Timestamp(gun)); gelecek = bil["bilgi_idx"] >= i0
        Fb = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in Fp.items()}
        rng = np.random.default_rng(3)
        for k in ("si", "si_once", "adv", "deg_yuzde", "dtc_dosya"):
            Fb[k][gelecek] = Fb[k][gelecek] * rng.uniform(0.1, 9.0, Fb[k][gelecek].shape)
        Fb["bolunme"][gelecek] = ~Fb["bolunme"][gelecek]; Fb["var"][gelecek] = rng.random(Fb["var"][gelecek].shape) < 0.5
        hb = hacim.copy(); hb[i0 + 1:] *= rng.uniform(0.01, 100.0, hb[i0 + 1:].shape); Fb["kimlik_ok"] = K.k66_kimlik(Fb, hb, takv, bol)[0]
        if not np.array_equal(Fb["kimlik_ok"][~gelecek], Fp["kimlik_ok"][~gelecek]):
            hata.append(f"7) t = {gun}'den sonraki hacim / rapor bozulunca önceki raporların kimlik denetimi değişti")
        payb = pay.copy(); payb[i0 + 1:] *= rng.uniform(0.2, 5.0, payb[i0 + 1:].shape)
        Xb, _b = K.k66_degiskenler(Fb, takv, payb, bol)
        for k in K.k66_kodlar():
            if not TK.esit(X[k][:i0 + 1], Xb[k][:i0 + 1]):
                hata.append(f"7) {k}: t = {gun}'den sonra yayımlanan rapor / sonraki pay bozulunca t ve öncesi değişti")
        if all(TK.esit(X[k][i0 + 30:], Xb[k][i0 + 30:]) for k in K.k66_kodlar()):
            hata.append("7) bozma t sonrasını değiştirmedi (test anlamsız)")
    # 8) isim denetimi ve sembol eşleme
    if not (K.k66_isim_anahtari("The Agilent Technologies, Inc.") == "agilent" and K.k66_isim_anahtari("AT&T Inc.") == "att" and K.k66_isim_anahtari("BERKSHIRE HATHAWAY Class B") == "berkshire"
            and K.k66_finra_kodu("BRK-B") == "BRKB" and K.k66_finra_kodu("bf.b") == "BFB"):
        hata.append("8) isim anahtarı / FINRA kodu yanlış")
    r19 = int(np.searchsorted(Fp["odeme"], np.datetime64("2019-06-01"))); r21 = int(np.searchsorted(Fp["odeme"], np.datetime64("2021-06-01")))
    if not (Fp["var"][r19, 9] and not Fp["isim_ok"][r19, 9] and Fp["isim_ok"][r21, 9] and Fp["isim_ok"][r19, 1] and Fp["var"][:, 2].all() and Fp["otc"][:, 2].all()):
        hata.append("8) isim bilgisi (bugünkü adla uyuşma) yanlış")
    if not (not kim[r19, 9] and kim[r21, 9] and kim[r19, 1] and not kim[:, 3].any() and kim[1:, 2].all() and kim[1:, 6].all() and kim[1:, 5].all()):
        hata.append("8) kimlik denetimi: başka şirkete ait (50 kat ADV) satır düşmedi, ADV = 0 kabul edildi ya da geçerli / bölünmeli satır düştü")
    r = 40; j = 1; a_ = Fp["odeme"][r - 1]; b_g = Fp["odeme"][r]; vv = V[S[j]].Volume[(V[S[j]].index > pd.Timestamp(a_)) & (V[S[j]].index <= pd.Timestamp(b_g))]
    if not np.isclose(lo[r, j], np.log10(Fp["adv"][r, j] / vv.mean())):
        hata.append("8) kimlik oranı elle hesapla aynı değil")
    with tempfile.TemporaryDirectory() as td:
        S2 = S[:6] + ["XY-Z", "XYZ"]; sentetik_finra(td, S2, {"bolunme": {}}, cakisan=True); Fc = K.k66_finra_panel(S2, td)
        if not (Fc["ozet"]["cakisan_kod"] == ["XYZ"] and not Fc["var"][:, 6:].any() and Fc["var"][:, 0].all()):
            hata.append("8) aynı FINRA koduna düşen iki sembol dışarıda bırakılmadı")
    # 9) karar sırası seçim kuralı
    def kp(u, a):
        return pd.DataFrame([{"tanim": "K24", "pazar": "ABD", "donem": d, "degisken": k, "n_ust": u, "n_alt": a} for d in E0["bagimsiz"] for k in K.k66_kodlar()]
                            + [{"tanim": "D13", "pazar": "ABD", "donem": "2018-2021", "degisken": "DTC", "n_ust": 1, "n_alt": 900}])
    K9 = kp(300, 280); K9b = K9.copy(); K9b.loc[0, "n_ust"] = 29; K9c = K9.copy(); K9c.loc[3, "n_alt"] = 140
    if not (K.k66_sira_sec(K9)[0] == "EVREN" and K.k66_sira_sec(K9b)[0] == "IC" and K.k66_sira_sec(K9c)[0] == "IC" and K.k66_sira_sec(kp(300, 150))[0] == "EVREN"
            and K.k66_sira_sec(kp(300, 149))[0] == "IC"):
        hata.append("9) karar sırası seçim kuralı (n < 30 ya da oran < 0,5 -> İÇ) tutmuyor")
    # 10) kapsam modu getiri hesaplamaz
    with tempfile.TemporaryDirectory() as tf:
        sentetik_finra(tf, S, D, V); Fg = K.k66_finra_panel(S, tf)
    girdi = {"ABD": {"V": V, "T": T, "pay": {"bolunme": bol, "sembol": S}, "F": Fg, "ozet": {"hisse": len(S), "finra": Fg["ozet"]}}}
    Es = copy.deepcopy(E0); Es["olay"]["d13"]["etkin"] = False
    asil = (FI.fi_olcut_panel, FI.fi_olcut_olay, FI.fi_olcut_hucre)

    def yasak(*a, **k):
        raise AssertionError("kapsam modunda FI_OLCUT çağrıldı")
    with tempfile.TemporaryDirectory() as td:
        try:
            FI.fi_olcut_panel = FI.fi_olcut_olay = FI.fi_olcut_hucre = yasak
            Kp = K.k66_kapsam(td, girdi, Es)
        except AssertionError as ex:
            hata.append(f"10) {ex}"); Kp = pd.DataFrame()
        finally:
            FI.fi_olcut_panel, FI.fi_olcut_olay, FI.fi_olcut_hucre = asil
        if len(Kp):
            if any(c in Kp.columns for c in ("r60", "fark", "ort_fark", "r20")) or not {"n_ham", "n_tekil", "n_pencere", "n_deger", "n_ust", "n_alt", "n_ust_ic"} <= set(Kp.columns):
                hata.append("10) kapsam tablosunda getiri sütunu var ya da sayım sütunu eksik")
            O = K64.k64_olay_k24(V, Es); o = Kp[(Kp.degisken == "(olay)") & (Kp.donem == "2018-2021")].iloc[0]; z = Kp[(Kp.degisken == "SI_PAY") & (Kp.donem == "2018-2021")].iloc[0]
            gm = (O.giris >= "2018-01-01") & (O.giris <= "2021-12-31")
            if not (o.n_ham == gm.sum() and o.n_tekil == (gm & O.tekil).sum() and o.n_pencere <= o.n_tekil and z.n_ust + z.n_orta + z.n_alt <= z.n_deger <= o.n_pencere and z.n_deger > 0):
                hata.append("10) kapsam sayıları olay tablosuyla tutmuyor")
            notu = K.k66_kapsam_notu(td, Es)
            if "Kapsam sayımı" not in notu or "| SI_PAY | EVREN |" not in notu or "FINRA:" not in notu or "seçim kuralı uygulaması" not in notu or "KİMLİK denetiminden geçen satır" not in notu:
                hata.append("10) kapsam notu yazılamadı")
    # 11) uçtan uca sentetik koşu (git'li)
    with tempfile.TemporaryDirectory() as td:
        durmali(lambda: K.k66_kos(td, True, girdi, Es), "11) ön kayıt yokken koşu durmadı", hata)
        TK.git(td, "init", "-q"); y = K.k66_onkayit(td, veri_sha=vs, E=Es)
        durmali(lambda: K.k66_kos(td, True, girdi, Es), "11) git'e işlenmemiş ön kayıtla koşu durmadı", hata)
        TK.git(td, "add", "K66_ON_KAYIT.md"); TK.git(td, "commit", "-q", "-m", "on kayit")
        R = K.k66_kos(td, True, girdi, Es)
        for ad_ in ("olay", "s1", "fark", "s2", "karar", "meta", "rapor"):
            if not os.path.exists(K._k66_yol(ad_, td)):
                hata.append(f"11) çıktı yok: {ad_}")
        S1, Fk, Kr = R["s1"], R["fark"], R["karar"]; st = Es["sira"]["karar"]["K66"]
        tm = S1[(S1.grup == "TEMEL") & (S1.rejim == "HEPSI") & (S1.donem == "2018-2021")].iloc[0]
        Xe = pd.read_csv(K._k66_yol("olay", td), parse_dates=["sinyal", "giris"]); m1 = (Xe.giris >= "2018-01-01") & (Xe.giris <= "2021-12-31") & Xe.fark.notna()
        if not (tm.n == m1.sum() and np.isclose(tm.ort_fark, Xe.fark[m1].mean()) and np.isclose(tm.medyan_r60, Xe.r60[m1].median())):
            hata.append("11) temel model hücresi olay dosyasından yeniden üretilemedi")
        fz = Fk[(Fk.degisken == "DTC") & (Fk.sira_turu == "EVREN") & (Fk.donem == "2018-2021")].iloc[0]; gz = K64.k64_grup(Xe.DTC_sira.to_numpy(float))
        if not (fz.n_ust == (m1 & (gz == "UST")).sum() and fz.n_alt == (m1 & (gz == "ALT")).sum()
                and np.isclose(fz.nokta, Xe.fark[m1 & (gz == "UST")].mean() - Xe.fark[m1 & (gz == "ALT")].mean())
                and bool(fz.ek_UST) == bool(fz.olculebilir and fz.ort_ust > fz.ort_temel and fz.alt > 0)):
            hata.append("11) ÜST - ALT satırı olay dosyasından yeniden üretilemedi / ek katkı kuralı tutmuyor")
        # olay dosyasındaki değişken değeri, sinyal günündeki matris değeriyle aynı (r0 kuralı olay düzeyinde)
        H = K.k66_pazar_hazirla(girdi["ABD"], Es); it = H["takvim"].get_indexer(pd.DatetimeIndex(Xe.sinyal)); jj = np.array([H["kol"][s] for s in Xe.sembol])
        if not TK.esit(Xe.SI_PAY.to_numpy(float), H["X"]["SI_PAY"][it, jj].astype(float), 1e-6):
            hata.append("11) olay dosyasındaki SI_PAY sinyal günü matris değeriyle aynı değil")
        if len(Fk) != 3 * 4 * 2 or len(Kr) != 8 or Kr.aile_m.iloc[0] > 16 or set(S1[(S1.rejim != "HEPSI") & (S1.grup != "TEMEL")].sira_turu.unique()) != {st} \
                or not set(Kr.karar.str.slice(0, 8)) <= {"ABD-ADAY", "İZ DEĞİL", "ÖLÇÜLEME"}:
            hata.append(f"11) ÜST - ALT / karar tablosu boyutu ya da etiketleri beklenen gibi değil ({len(Fk)}, {len(Kr)})")
        if len(R["s2"]) != 12 or not (R["s2"].n_ust.fillna(0) > 0).any():
            hata.append("11) S2 tablosu boş / eksik")
        rap = open(R["rapor"], encoding="utf-8").read()
        for parca in ("## Karar tablosu", "## Temel model", "## SI_PAY", "## DTC", "## SI_DEG", "## SI_DEG1", "ÜST - ALT", "S2 (çöl dışı evren", "## Veri eksikleri"):
            if parca not in rap:
                hata.append(f"11) raporda '{parca}' yok")
        if open(K.k66_rapor(td, Es), encoding="utf-8").read() != rap:
            hata.append("11) rapor çıktılardan yeniden üretilince değişti")
        open(y, "a", encoding="utf-8").write("\nsonradan eklenen satır\n")
        durmali(lambda: K.k66_kos(td, True, girdi, Es), "11) git'e işlendikten sonra değişen ön kayıtla koşu durmadı", hata)
    # 12) e-posta / anahtar yok
    for ad_ in ("K66.py", "test_k66.py"):
        metin = open(os.path.join(KOK, ad_), encoding="utf-8").read()
        if K._K66_EPOSTA.search(metin) or re.search(r"(api[_-]?key|token|password|sifre)\s*=\s*['\"][A-Za-z0-9]{8,}", metin, re.I):
            hata.append(f"12) {ad_} içinde e-posta / anahtar biçimli parça var")
    return hata


if __name__ == "__main__":
    h = testler()
    for x in h:
        print("HATA:", x)
    print("test_k66:", "TAMAM (12/12)" if not h else f"{len(h)} HATA")
    sys.exit(1 if h else 0)
