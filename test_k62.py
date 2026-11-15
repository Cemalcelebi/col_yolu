"""K62 testleri (ağ gerekmez; yalnız SENTETİK veri, gerçek veride getiri ölçmez). Çalıştırma: python test_k62.py

1) çakışma kapısı  2) mühür ve ön kayıt (eşik değişince mühür değişir; yaz / oku / doğrula; üzerine yazmama; bozuk ön kayıt reddi; gerçek
K62_ON_KAYIT.md varsa bugünkü eşiklerle aynı mühür)  3) 'ön kayıt commit'li ve değişmemiş değilse `kos` reddeder' (ön kayıt yok / git'e işlenmemiş
/ işlendikten sonra değişmiş / mühür farklı; işlenmişse koşar)  4) üç sürpriz ölçüsü elle hesapla aynı: SUETF (çeyreklik kâr farkı / çeyrek sonu
piyasa değeri), EAR (2x3 portföye göre [t-1, t+1]), SUEAF = VERİ YOK (sütun üretilmez)  5) portföy kesimleri (2 büyüklük x 3 DD/PD, Haziran
oluşumu, Temmuz-Haziran geçerlilik, özkaynağı <= 0 dışarıda) ve makale tertili (eşit üçte birler, eşitlik kuralı, az olaylı çeyrek ölçülmez)
6) CAR penceresi ([t+2, t+61] = 60 getiri; elle hesap; kotasyondan çıkan hisse portföy getirisini alır; 2/3 kuralı)  7) GELECEĞE BAKMA YOK:
karar gününden (t+1) sonraki fiyat, piyasa değeri, mali tablo ve açıklamalar bozulunca SUETF, EAR, onsel bayrağı ve geleceğe bakmayan tertil
aynı (CAR değişir)  8) 60 gün tekilleştirme  9) sayım modu getiri / sürpriz değeri üretmez  10) istatistik (Student t, kümeli EKK elle,
BH, kırpma, PEAD: ekili etki bulunur, etkisiz veri bulunmaz)  11) ayrıştırıcılar ve önbellekten demet (KAP ilk rapor, çok kodlu şirket, pencere
bölme, fiyat / mali JSON)  12) uçtan uca sentetik `kos` + `rapor` (A, B, C; çıktılardan yeniden üretim; e-posta yok)  13) e-posta / anahtar yok.
"""
from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K62 as K  # noqa: E402


def sentetik(n: int = 90, bas: str = "2008-01-01", bit: str = "2012-12-31", tohum: int = 7, etki: float = 1.0) -> dict:
    """Sentetik BIST benzeri demet + OHLCV paneli. Her hisse-çeyrek için sürpriz s ~ N(0,1): kâr farkı s ile orantılı; açıklama günü ve ertesi
    gün getirisine 0,02 x s, [t+2, t+61] günlerine günde 0,0006 x s x etki eklenir (ekili PEAD). Bütün hisseler > 100 mn USD."""
    rng = np.random.default_rng(tohum); tak = pd.bdate_range(bas, bit); T = len(tak); kod = [f"S{i:03d}" for i in range(n)]
    r = rng.normal(0.0002, 0.015, (T, n)); pay = rng.uniform(2e8, 2e9, n); kur = 1.5; duy, mali = [], []
    yillar = range(tak[0].year, tak[-1].year + 1)
    for j, k in enumerate(kod):
        temel = rng.uniform(2e7, 8e7); oz = rng.uniform(3e8, 3e9); gecmis = {}
        for y in yillar:
            bir = 0.0
            for c in (1, 2, 3, 4):
                s = rng.normal(); e = gecmis.get((y - 1, c), temel) + s * 2e7; gecmis[(y, c)] = e; bir += e; oz += 0.2 * e
                mali.append({"kod": k, "yil": y, "ceyrek": c, "kar_bir": bir, "ozkaynak": oz, "grup": "XI_29"})
                qs = pd.Timestamp(year=y, month=3 * c, day=1) + pd.offsets.MonthEnd(0)
                yayin = qs + pd.Timedelta(days=int(rng.integers(32, 58)), hours=int(rng.integers(9, 23)))
                t = int(tak.searchsorted(yayin.normalize()))
                if t + 1 < T:
                    r[t:t + 2, j] += 0.02 * s; r[t + 2:t + 62, j] += 0.0006 * s * etki
                duy.append({"kod": k, "yil": y, "ceyrek": c, "yayin": yayin, "bildirim": 1})
    C = 10.0 * np.exp(np.cumsum(r, axis=0)) * rng.uniform(0.5, 3.0, n)[None, :]
    PD = C * pay[None, :]; X = 100.0 * np.exp(np.cumsum(r.mean(axis=1)))
    HU = np.abs(rng.normal(5e6, 1e6, (T, n))) + 1e5
    D = {"takvim": tak, "kod": kod, "C": C, "PD": PD, "PDU": PD / kur, "HU": HU, "X": X, "mali": pd.DataFrame(mali),
         "duyuru": pd.DataFrame(duy).sort_values(["yayin", "kod"]).reset_index(drop=True), "sektor": {k: f"SEK{j % 5}" for j, k in enumerate(kod)}, "kap_kayit": len(duy)}
    V = {}
    for j, k in enumerate(kod):
        o = np.concatenate([[C[0, j]], C[:-1, j]]) * np.exp(rng.normal(0, 0.003, T))
        V[k] = pd.DataFrame({"Open": o, "High": np.maximum(o, C[:, j]) * 1.005, "Low": np.minimum(o, C[:, j]) * 0.995, "Close": C[:, j], "Volume": HU[:, j] * kur / C[:, j]}, index=tak)
    return {"D": D, "V": V}


def _git(kl: str, *a: str) -> None:
    subprocess.run(["git", "-C", kl, "-c", "user.name=test", "-c", "user.email=test@invalid", "-c", "commit.gpgsign=false", *a], check=True, capture_output=True, timeout=60)


def _elle_portfoy(D: dict, Y: int) -> dict:
    """Bağımsız (pandas) portföy ataması: Y Haziran sonu büyüklük medyanı x (Y-1) DD/PD üçte birleri."""
    tak = D["takvim"]; iJ = int(tak.searchsorted(pd.Timestamp(f"{Y}-06-30"), side="right")) - 1; iD = int(tak.searchsorted(pd.Timestamp(f"{Y - 1}-12-31"), side="right")) - 1
    M = D["mali"]; oz = M[(M.yil == Y - 1) & (M.ceyrek == 4)].set_index("kod").ozkaynak.reindex(D["kod"]).to_numpy(float)
    S = pd.DataFrame({"boyut": D["PD"][iJ], "dd": oz / D["PD"][iD], "oz": oz}, index=D["kod"]); S = S[S.oz > 0].copy()
    S["b"] = (S.boyut.rank(method="first") - 1) * 2 // len(S); S["d"] = (S["dd"].rank(method="first") - 1) * 3 // len(S)
    return (S.b * 3 + S.d).astype(int).to_dict()


def testler() -> list:
    hata: list = []
    E = K.K62_ESIK
    # 1) çakışma kapısı
    src = open(os.path.join(KOK, "K62.py"), encoding="utf-8").read()
    g = {"__name__": "kapi_test", "k62_kos": lambda: None}
    try:
        exec(compile(src, "K62.py", "exec"), g); hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi_test2"}
    try:
        exec(compile(src, "K62.py", "exec"), g2); exec(compile(src, "K62.py", "exec"), g2)
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    if "_CK_ONCE_K62" not in src or "_cakisma_kontrol_k62()" not in src:
        hata.append("1) çakışma kapısı adı _CK_ONCE_K62 değil")

    # 2) mühür ve ön kayıt
    E2 = copy.deepcopy(E); E2["bolum_a"]["basari_puan"] = 0.02
    if K.k62_esik_sha(E2) == K.k62_esik_sha() or K.k62_esik_sha(bagimli={"FI_OLCUT": {"ufuk": 61}}) == K.k62_esik_sha() or len(K.k62_esik_sha()) != 64:
        hata.append("2) eşik / FI_OLCUT değişince mühür değişmedi")
    if K.k62_esik_sha() != K.k62_esik_sha(copy.deepcopy(E)):
        hata.append("2) mühür kararlı değil")
    with tempfile.TemporaryDirectory() as td:
        vs = {"sha256": "a" * 64, "v_bist_sha256": "b" * 64}
        y = K.k62_onkayit_yaz(td, kapsam={}, veri_sha=vs); ilk = open(y, encoding="utf-8").read(); oc = K._k62_onkayit_oku(y)
        if oc["sha"] != K.k62_esik_sha() or oc["veri_sha256"] != "a" * 64 or oc["v_bist_sha256"] != "b" * 64 or not re.match(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC", oc["zaman_utc"]):
            hata.append(f"2) ön kayıttan mühür / veri sha256 / zaman okunamadı: {oc}")
        for parca in ("## 0. Kaynak makale", "## A. BİREBİR TEKRAR", "## B. DÖNEM", "## C. PROJE CETVELİ", "## D. PROTOKOL", "## E. K28 KARŞILAŞTIRMA", "## F. MÜHÜR", "## G. VERİ VE KAPSAM",
                      "## H. BOŞLUK", "## I. FAZ 2", "SAPMA 1", "SAPMA 3", "SAPMA 9", "BIMAS", "2022Ç4", "TEMİZ", "VERİ YOK", "0.0294", "0.0290", "0.0218", "10.1016/j.bir.2020.09.001", "YENİDEN ÜRETİLDİ", "Benjamini-Hochberg",
                      "30 bp", "2017-2021", "2022-2026", "2023-2026", "2026-08-31", "python -I K62.py kos", "İZ ya da ADAY denmez", "6471"):
            if parca not in ilk:
                hata.append(f"2) ön kayıtta '{parca}' yok")
        try:
            K.k62_onkayit_yaz(td, kapsam={}, veri_sha=vs); hata.append("2) ön kayıt üzerine yazıldı")
        except K.K62Hata:
            pass
        if K.k62_onkayit_dogrula(y, git=False)["sha"] != K.k62_esik_sha():
            hata.append("2) doğrulama mührü yanlış")
        try:
            K.k62_onkayit_dogrula(y, E2, git=False); hata.append("2) eşiği değişmiş koşu durmadı (mühür)")
        except K.K62Hata:
            pass
        open(y, "w", encoding="utf-8").write(ilk.replace("MÜHÜR (K62_ESIK", "MUHUR (K62_ESIK"))
        try:
            K.k62_onkayit_dogrula(y, git=False); hata.append("2) bozuk ön kayıt kabul edildi")
        except K.K62Hata:
            pass
    gercek = K._k62_yol("onkayit")
    if os.path.exists(gercek):
        try:
            if K._k62_onkayit_oku(gercek)["sha"] != K.k62_esik_sha():
                hata.append("2) gerçek K62_ON_KAYIT.md mührü bugünkü K62_ESIK + FI_OLCUT ile aynı değil")
        except K.K62Hata as ex:
            hata.append(f"2) gerçek ön kayıt okunamadı: {ex}")

    S = sentetik(); D, V = S["D"], S["V"]; tak = D["takvim"]; kol = {k: j for j, k in enumerate(D["kod"])}
    H = K.k62_hazirla(D, E, True); Ev = K.k62_olay_tablosu(D, E, True, H)
    # 3) ön kayıt commit'li ve değişmemiş değilse kos reddeder
    with tempfile.TemporaryDirectory() as td:
        try:
            _git(td, "init", "-q"); cik = os.path.join(td, "cikti"); os.makedirs(cik)
            for ad, kw in (("ön kayıt yokken", {}),):
                try:
                    K.k62_kos(cik, demet=D, V=V, **kw); hata.append(f"3) {ad} koşu durmadı")
                except K.K62Hata:
                    pass
            y = K.k62_onkayit_yaz(cik, kapsam={}, veri_sha={"sha256": "a" * 64, "v_bist_sha256": "b" * 64})
            try:
                K.k62_kos(cik, demet=D, V=V); hata.append("3) git'e işlenmemiş ön kayıtla koşu durmadı")
            except K.K62Hata as ex:
                if "işlenmemiş" not in str(ex):
                    hata.append(f"3) beklenmeyen ret nedeni: {ex}")
            _git(td, "add", "-f", y); _git(td, "commit", "-q", "-m", "on kayit")
            if "commit" not in K.k62_onkayit_dogrula(y, git=True).get("git", {}):
                hata.append("3) işlenmiş ön kayıt doğrulanmadı")
            try:
                K.k62_kos(cik, demet=D, V=V, E=E2); hata.append("3) mührü farklı (eşiği değişmiş) koşu durmadı")
            except K.K62Hata:
                pass
            open(y, "a", encoding="utf-8").write("\nsonradan eklenen kural\n")
            try:
                K.k62_kos(cik, demet=D, V=V); hata.append("3) işlendikten sonra değişmiş ön kayıtla koşu durmadı")
            except K.K62Hata as ex:
                if "değişmiş" not in str(ex):
                    hata.append(f"3) beklenmeyen ret nedeni: {ex}")
            if os.path.exists(K._k62_yol("tablo", cik)):
                hata.append("3) reddedilen koşu çıktı yazdı")
            try:
                K.k62_onkayit_yaz(cik, kapsam={}, veri_sha={"sha256": "a" * 64, "v_bist_sha256": "b" * 64}, uzerine=True); hata.append("3) git'e işlenmiş ön kaydın üzerine yazıldı")
            except K.K62Hata:
                pass
        except (subprocess.SubprocessError, OSError) as ex:
            hata.append(f"3) git testi kurulamadı: {ex}")

    # 4) üç sürpriz ölçüsü elle
    Q = K.k62_ceyreklik(D["mali"]); M = D["mali"].set_index(["kod", "yil", "ceyrek"])
    if abs(Q[("S003", 2010, 3)][0] - (M.loc[("S003", 2010, 3)].kar_bir - M.loc[("S003", 2010, 2)].kar_bir)) > 1e-6 or abs(Q[("S003", 2010, 1)][0] - M.loc[("S003", 2010, 1)].kar_bir) > 1e-6:
        hata.append("4) çeyreklik kâr = birikimli fark değil")
    Mx = D["mali"].copy(); Mx = Mx[~((Mx.kod == "S004") & (Mx.yil == 2010) & (Mx.ceyrek == 2))]
    if np.isfinite(K.k62_ceyreklik(Mx)[("S004", 2010, 3)][0]):
        hata.append("4) önceki birikimli değer yokken çeyreklik kâr üretildi")
    ev = Ev[(Ev.kod == "S010") & (Ev.yil == 2011) & (Ev.ceyrek == 2)].iloc[0]; j = kol["S010"]; t = int(ev.t_i)
    iq = int(tak.searchsorted(pd.Timestamp("2011-06-30"), side="right")) - 1
    elle = ((M.loc[("S010", 2011, 2)].kar_bir - M.loc[("S010", 2011, 1)].kar_bir) - (M.loc[("S010", 2010, 2)].kar_bir - M.loc[("S010", 2010, 1)].kar_bir)) / D["PD"][iq, j]
    if not ev.f_mali or abs(ev.SUETF - elle) > 1e-12:
        hata.append(f"4) SUETF elle hesapla aynı değil: {ev.SUETF} != {elle}")
    if t != int(tak.searchsorted(pd.Timestamp(ev.yayin).normalize())) or ev.karar_i != t + 1 or pd.Timestamp(ev.giris) != tak[t + 2]:
        hata.append("4) t / karar / giriş günü yanlış")
    pf = _elle_portfoy(D, 2011 if tak[t] > pd.Timestamp("2011-06-30") else 2010); uye = [kol[k] for k, p in pf.items() if p == pf["S010"]]
    Rg = D["C"][1:] / D["C"][:-1] - 1; rp = Rg[t - 2:t + 1][:, uye].mean(axis=1); ri = Rg[t - 2:t + 1, j]     # Rg[k-1] = k. günün getirisi
    elle_ear = float(np.prod(1 + ri) - np.prod(1 + rp))
    if not ev.f_ear or abs(ev.EAR - elle_ear) > 1e-12:
        hata.append(f"4) EAR elle hesapla aynı değil: {ev.EAR} != {elle_ear}")
    if "SUEAF" in Ev.columns or E["bolum_a"]["veri_yok"] != ["SUEAF"] or "SUEAF" in E["bolum_a"]["olculen"]:
        hata.append("4) SUEAF için sütun / ölçüm üretildi (VERİ YOK olmalı)")

    # 5) portföy kesimleri ve tertil
    Pid = H["Pid"]; i0 = int(tak.searchsorted(pd.Timestamp("2010-06-30"), side="right")); i1 = int(tak.searchsorted(pd.Timestamp("2011-06-30"), side="right")) - 1
    pf10 = _elle_portfoy(D, 2010)
    if any(int(Pid[i0, kol[k]]) != p or int(Pid[i1, kol[k]]) != p for k, p in pf10.items()):
        hata.append("5) 2x3 portföy ataması elle hesapla aynı değil")
    if tak[i0] <= pd.Timestamp("2010-06-30") or (Pid[i0 - 1] == Pid[i0]).all() and _elle_portfoy(D, 2009) != pf10:
        hata.append("5) portföy Haziran sonundan önce değişti")
    ilk = int(tak.searchsorted(pd.Timestamp("2009-06-30"), side="right"))
    if (Pid[:ilk] >= 0).any() or not (Pid[ilk] >= 0).any():
        hata.append("5) ilk oluşumdan (Haziran 2009) önce portföy atandı ya da Temmuz 2009'da atanmadı")
    say = np.bincount(Pid[i0][Pid[i0] >= 0], minlength=6)
    if say.sum() != len(pf10) or len(set(np.bincount(Pid[i0][Pid[i0] >= 0] // 3))) > 2 or abs(np.bincount(Pid[i0][Pid[i0] >= 0] % 3).max() - np.bincount(Pid[i0][Pid[i0] >= 0] % 3).min()) > 1:
        hata.append(f"5) kova büyüklükleri eşit değil: {say}")
    Dn = dict(D); Mn = D["mali"].copy(); Mn.loc[(Mn.kod == "S020") & (Mn.yil == 2009) & (Mn.ceyrek == 4), "ozkaynak"] = -5.0; Dn["mali"] = Mn
    Pn = K.k62_portfoy_ata(Dn, E)
    if Pn[i0, kol["S020"]] != -1 or Pid[i0, kol["S020"]] == -1:
        hata.append("5) özkaynağı <= 0 olan hisse portföye girdi")
    if not Ev[(Ev.kod == "S020") & (Ev.yil == 2010)].f_defter.all() or K.k62_olay_tablosu(Dn, E, False).query("kod == 'S020' and yil == 2010").f_defter.any():
        hata.append("5) önceki yıl sonu özkaynağı negatif olay örnekleme girdi")
    v = np.array([5.0, 1.0, 3.0, 3.0, 9.0, 7.0] * 6 + [np.nan]); q = np.array(["a"] * 37); kd = np.array([f"K{i:02d}" for i in range(37)])
    s = K.k62_tertil(v, q, kd, E)
    if s[-1] != -1 or list(np.bincount(s[:-1])) != [12, 12, 12] or v[:-1][s[:-1] == 0].max() > v[:-1][s[:-1] == 1].min() or v[:-1][s[:-1] == 1].max() > v[:-1][s[:-1] == 2].min():
        hata.append(f"5) tertil eşit üçte bir / sıralı değil: {np.bincount(s[:-1])}")
    if (K.k62_tertil(v[:29], q[:29], kd[:29], E) != -1).any():
        hata.append("5) az olaylı çeyrek (< 30) tertile bölündü")
    s2 = K.k62_tertil(np.concatenate([v[:36], v[:36] + 100]), np.array(["a"] * 36 + ["b"] * 36), np.concatenate([kd[:36], kd[:36]]), E)
    if list(s2[:36]) != list(s2[36:]):
        hata.append("5) tertil çeyrek İÇİNDE hesaplanmıyor")

    # 6) CAR penceresi
    pid = int(Pid[t, j]); uy = np.flatnonzero(Pid[t] == pid); Ri = H["R"]
    if abs(Ri[t + 5, j] - (D["C"][t + 5, j] / D["C"][t + 4, j] - 1)) > 1e-12:
        hata.append("6) günlük getiri tanımı yanlış")
    for n in (21, 41, 61):
        rp = np.array([Ri[k, np.flatnonzero(Pid[k] == pid)].mean() for k in range(t + 2, t + n + 1)]); ri = Ri[t + 2:t + n + 1, j]
        elle_car = float(np.prod(1 + ri) - np.prod(1 + rp))
        if len(ri) != n - 1 or abs(ev[f"CAR{n}"] - elle_car) > 1e-10:
            hata.append(f"6) CAR[2,{n}] elle hesapla aynı değil: {ev[f'CAR{n}']} != {elle_car}")
    if abs(H["Rp"][t + 3, pid] - Ri[t + 3, uy].mean()) > 1e-12:
        hata.append("6) portföy getirisi eşit ağırlıklı ortalama değil")
    Dc = dict(D); Cc = D["C"].copy(); Cc[t + 31:, j] = np.nan; Dc["C"] = Cc; Hc = K.k62_hazirla(Dc, E, True); Ec = K.k62_olay_tablosu(Dc, E, True, Hc)
    ec = Ec[(Ec.kod == "S010") & (Ec.yil == 2011) & (Ec.ceyrek == 2)].iloc[0]
    if ec.f_car or ec.tam or not ec.onsel or np.isfinite(ec.CAR61):
        hata.append("6) getirilerinin 2/3'ü olmayan olay tam örnekleme girdi / CAR üretti")
    Cc = D["C"].copy(); Cc[t + 50:, j] = np.nan; Dc["C"] = Cc; Hc = K.k62_hazirla(Dc, E, True); Ec = K.k62_olay_tablosu(Dc, E, True, Hc)
    ec = Ec[(Ec.kod == "S010") & (Ec.yil == 2011) & (Ec.ceyrek == 2)].iloc[0]
    rp = np.array([Hc["R"][k, [u for u in np.flatnonzero(Hc["Pid"][k] == pid) if Hc["A"][k, u]]].mean() for k in range(t + 2, t + 62)])
    ri = np.where(np.arange(t + 2, t + 62) < t + 50, Hc["R"][t + 2:t + 62, j], rp)
    if not ec.tam or abs(ec.CAR61 - float(np.prod(1 + ri) - np.prod(1 + rp))) > 1e-10:
        hata.append("6) kotasyondan çıkan hisse kalan günlerde portföy getirisini almıyor")
    son = Ev[Ev.t_i + 61 >= len(tak)]
    if len(son) and (son.f_car.any() or son.tam.any()):
        hata.append("6) penceresi takvimi (kesik) aşan olay ölçüldü")

    # 7) geleceğe bakma yok
    kes = t + 1; Df = dict(D); rng = np.random.default_rng(3)
    for ad in ("C", "PD", "PDU", "HU"):
        Z = D[ad].copy(); Z[kes + 1:] *= rng.uniform(0.3, 3.0, Z[kes + 1:].shape); Df[ad] = Z
    Xf = D["X"].copy(); Xf[kes + 1:] *= 1.7; Df["X"] = Xf
    Mf = D["mali"].copy(); gelecek = (Mf.yil * 10 + Mf.ceyrek) > 2011 * 10 + 2; Mf.loc[gelecek, ["kar_bir", "ozkaynak"]] *= -3.0; Df["mali"] = Mf
    Uf = D["duyuru"].copy(); sonra = pd.to_datetime(Uf.yayin) > tak[kes] + pd.Timedelta(days=1); Uf.loc[sonra, "yayin"] = pd.to_datetime(Uf.loc[sonra, "yayin"]) + pd.Timedelta(days=9); Df["duyuru"] = Uf
    Ef = K.k62_olay_tablosu(Df, E, True)
    a = Ev[Ev.karar_i <= kes].set_index(["kod", "yil", "ceyrek"]); b = Ef.set_index(["kod", "yil", "ceyrek"]).reindex(a.index)
    for kolon in ("SUETF", "EAR", "IVOL", "BETA", "PRERET", "ILLIQUIDITY", "SIZE", "BM"):
        if not np.allclose(a[kolon].to_numpy(float), b[kolon].to_numpy(float), rtol=0, atol=1e-12, equal_nan=True):
            hata.append(f"7) gelecek bozulunca {kolon} değişti (geleceğe bakıyor)")
    if not (a.onsel.to_numpy() == b.onsel.to_numpy()).all() or not (a.t_i.to_numpy() == b.t_i.to_numpy()).all():
        hata.append("7) gelecek bozulunca onsel bayrağı / olay günü değişti")
    for o in ("SUETF", "EAR"):
        s0 = pd.Series(K.k62_tertil_onsel(Ev[Ev.onsel].reset_index(drop=True), o, E), index=pd.MultiIndex.from_frame(Ev[Ev.onsel][["kod", "yil", "ceyrek"]]))
        s1 = pd.Series(K.k62_tertil_onsel(Ef[Ef.onsel].reset_index(drop=True), o, E), index=pd.MultiIndex.from_frame(Ef[Ef.onsel][["kod", "yil", "ceyrek"]]))
        ix = a[a.onsel].index
        if not (s0.reindex(ix).to_numpy() == s1.reindex(ix).to_numpy()).all() or (s0.reindex(ix) >= 0).sum() < 100:
            hata.append(f"7) gelecek bozulunca geleceğe bakmayan {o} tertili değişti (ya da hiç atanmadı)")
    yakin = Ev[(Ev.karar_i <= kes) & (Ev.karar_i > kes - 30) & Ev.tam].set_index(["kod", "yil", "ceyrek"])
    if len(yakin) and np.allclose(yakin.CAR61.to_numpy(float), Ef.set_index(["kod", "yil", "ceyrek"]).reindex(yakin.index).CAR61.to_numpy(float), equal_nan=True):
        hata.append("7) sağlama: gelecek bozulunca CAR değişmedi (bozma çalışmıyor)")
    Eo = Ev[Ev.onsel].reset_index(drop=True); so = K.k62_tertil_onsel(Eo, "SUETF", E); g = Eo[(Eo.yil == 2011) & (Eo.ceyrek == 2)].index[5]
    onc = Eo[(Eo.yil == 2011) & (Eo.ceyrek == 1) & (Eo.karar_i <= Eo.karar_i[g])].SUETF.to_numpy(float); alt, ust = np.quantile(onc, [1 / 3, 2 / 3])
    if so[g] != (2 if Eo.SUETF[g] >= ust else (0 if Eo.SUETF[g] <= alt else 1)) or (so[(Eo.yil == Eo.yil.min()) & (Eo.ceyrek == Eo[Eo.yil == Eo.yil.min()].ceyrek.min())] != -1).any():
        hata.append("7) geleceğe bakmayan tertil önceki çeyreğin kesimleriyle elle hesapla aynı değil / ilk çeyrekte sınıf atandı")

    # 8) 60 gün tekilleştirme
    Tk = pd.DataFrame({"kod": ["A", "A", "A", "A", "B", "B"], "t_i": [100, 145, 160, 221, 100, 159]})
    if sorted(K.k62_tekil(Tk, 60).index) != [0, 2, 3, 4] or sorted(K.k62_tekil(Tk, 1).index) != [0, 1, 2, 3, 4, 5] or sorted(K.k62_tekil(Tk, 500).index) != [0, 4]:
        hata.append(f"8) 60 gün tekilleştirme yanlış: {list(K.k62_tekil(Tk, 60).index)}")
    tek = K.k62_tekil(Ev[Ev.tam], 60)
    if (tek.sort_values(["kod", "t_i"]).groupby("kod").t_i.diff().dropna() < 60).any() or len(tek) >= int(Ev.tam.sum()):
        hata.append("8) tekilleştirilmiş olaylarda 60 günden yakın çift var / hiç olay düşmedi")

    # 9) sayım modu
    H0 = K.k62_hazirla(D, E, False); E0 = K.k62_olay_tablosu(D, E, False, H0)
    if any(k in H0 for k in ("R", "Rp", "Rm")) or any(k in E0.columns for k in ("SUETF", "EAR", "CAR61", "CAR21", "PRERET", "IVOL")):
        hata.append("9) sayım modu getiri / sürpriz değeri üretti")
    if not (E0[["onsel", "tam", "f_mali", "f_ear", "f_car"]].to_numpy() == Ev[["onsel", "tam", "f_mali", "f_ear", "f_car"]].to_numpy()).all():
        hata.append("9) sayım modu bayrakları ölçüm moduyla aynı değil")
    Kp = K.k62_kapsam(demet=D, v_semboller=sorted(V)[:50])
    if Kp["olay"]["hepsi"]["tam"] != int(Ev.tam.sum()) or Kp["olay"]["A"]["SUEAF_hesaplanabilir"] != 0 or Kp["olay"]["hepsi"]["onsel_vbist"] >= Kp["olay"]["hepsi"]["onsel"]:
        hata.append("9) kapsam sayımı olay tablosuyla aynı değil")
    def anahtarlar(x):
        return [k for k, v in x.items() for k in [k] + (anahtarlar(v) if isinstance(v, dict) else [])] if isinstance(x, dict) else []
    if [k for k in anahtarlar(Kp) if k.startswith(("ort", "med", "pead", "CAR", "r60", "fark")) or k in ("SUETF", "EAR", "t", "p")]:
        hata.append("9) kapsam çıktısında getiri alanı var")

    # 10) istatistik
    for tt, sd, p in ((2.0, 10, 0.073388), (1.96, 1e6, 0.049996), (0.0, 5, 1.0), (4.26, 47, 0.0000983), (-2.5, 20, 0.021234)):
        if abs(K.k62_t_p(tt, sd) - p) > 2e-5:
            hata.append(f"10) Student t p değeri yanlış: t={tt} sd={sd} -> {K.k62_t_p(tt, sd)} (beklenen {p})")
    rng = np.random.default_rng(5); n = 240; km = np.repeat(np.arange(12), 20); x = rng.normal(size=n); yv = 0.5 + 0.3 * x + rng.normal(size=n) + np.repeat(rng.normal(size=12), 20)
    r = K.k62_ols_kume(yv, np.column_stack([np.ones(n), x]), km); Xm = np.column_stack([np.ones(n), x]); XtXi = np.linalg.inv(Xm.T @ Xm); bb = XtXi @ Xm.T @ yv; u = yv - Xm @ bb
    et = sum(np.outer(Xm[km == g_].T @ u[km == g_], Xm[km == g_].T @ u[km == g_]) for g_ in range(12)); Vv = XtXi @ et @ XtXi * (12 / 11) * ((n - 1) / (n - 2))
    if not np.allclose(r["katsayi"], bb) or not np.allclose(r["se"], np.sqrt(np.diag(Vv))) or r["G"] != 12 or abs(r["p"][1] - K.k62_t_p(r["t"][1], 11)) > 1e-12:
        hata.append("10) kümeli EKK elle hesapla aynı değil")
    if list(K.k62_bh(np.array([0.001, 0.04, 0.03, 0.5, np.nan, 0.012]), 0.10)) != [True, True, True, False, False, True] or K.k62_bh(np.array([0.2, 0.9]), 0.10).any():
        hata.append("10) Benjamini-Hochberg yanlış")
    w = K.k62_winsor(np.arange(200.0), np.array(["a"] * 100 + ["b"] * 100), (0.01, 0.99))
    if abs(w[0] - 0.99) > 1e-9 or abs(w[99] - 98.01) > 1e-9 or abs(w[100] - 100.99) > 1e-9 or w[50] != 50:
        hata.append(f"10) çeyrek içi kırpma yanlış: {w[0]}, {w[99]}, {w[100]}")
    T, Rgt, Xs = K.k62_olc_ab(Ev, E)
    a61 = T[(T.bolum == "A") & (T.olcu == "SUETF") & (T.ufuk == 61) & ~T.tekil].iloc[0]; e61 = T[(T.bolum == "A") & (T.olcu == "EAR") & (T.ufuk == 61) & ~T.tekil].iloc[0]
    if not (a61.pead > 0.01 and a61.t > 3 and a61.alt > 0 and e61.pead > 0.01 and e61.t > 3):
        hata.append(f"10) ekili PEAD bulunamadı: SUETF {a61.pead:.4f} (t {a61.t:.1f}), EAR {e61.pead:.4f} (t {e61.t:.1f})")
    Xa = Xs[K._k62_a_maske(Xs, E)]; cw = K.k62_winsor(Xs.CAR61.to_numpy(float), Xs.mali_ceyrek.to_numpy(), E["olay"]["winsor"])[K._k62_a_maske(Xs, E)]
    elle_p = cw[Xa.SUETF_tertil.to_numpy() == 2].mean() - cw[Xa.SUETF_tertil.to_numpy() == 0].mean()
    if abs(a61.pead - elle_p) > 1e-12 or abs(a61.pead_net - (elle_p - 4 * 0.003)) > 1e-12 or a61.n_q1 != int((Xa.SUETF_tertil == 0).sum()) or abs(a61.fark_puan - (elle_p - 0.0294)) > 1e-12:
        hata.append("10) PEAD / net / makale farkı elle hesapla aynı değil")
    T21 = T[(T.bolum == "A") & (T.olcu == "SUETF") & ~T.tekil].set_index("ufuk").pead
    if not (T21[21] < T21[41] < T21[61]):
        hata.append("10) ekili sürüklenme ufukla büyümüyor")
    if a61.basari not in ("YENİDEN ÜRETİLDİ", "YÖN AYNI, BÜYÜKLÜK FARKLI") or (abs(a61.fark_puan) <= 0.015) != (a61.basari == "YENİDEN ÜRETİLDİ"):
        hata.append(f"10) başarı etiketi ±1,5 puan kuralıyla aynı değil: {a61.basari} (fark {a61.fark_puan:.4f})")
    S0 = sentetik(etki=0.0, tohum=11); Ev0 = K.k62_olay_tablosu(S0["D"], E, True); T0, _, _ = K.k62_olc_ab(Ev0, E)
    z61 = T0[(T0.bolum == "A") & (T0.olcu == "SUETF") & (T0.ufuk == 61) & ~T0.tekil].iloc[0]
    if abs(z61.pead) > 0.012 or abs(z61.t) > 3.0:
        hata.append(f"10) etkisiz veride PEAD bulundu: {z61.pead:.4f} (t {z61.t:.1f})")
    rr = Rgt[(Rgt.bolum == "A") & (Rgt.olcu == "SUETF")].iloc[0]
    if not (rr.a1 > 0.01 and rr.t > 3 and rr.n > 500) or "IO" in rr.katsayi or "PUANxSIZE" not in rr.katsayi:
        hata.append(f"10) kontrollü regresyon ekili etkiyi bulamadı / kontrol listesi yanlış: a1 {rr.a1}, t {rr.t}")

    # 11) ayrıştırıcılar, KAP listesi, önbellekten demet
    ham = json.dumps({"value": [{"HGDG_TARIH": "05-01-2010", "HGDG_KAPANIS": 2.0, "HG_KAPANIS": 20.0, "PD": 5e8, "PD_USD": 3e8, "HGDG_HACIM": 1e6, "DOLAR_HACIM": 7e5, "END_DEGER": 520.0, "SERMAYE": 2.5e7},
                               {"HGDG_TARIH": "04-01-2010", "HGDG_KAPANIS": 1.9, "HG_KAPANIS": 19.0, "PD": 4.75e8, "PD_USD": 2.9e8, "HGDG_HACIM": 2e6, "DOLAR_HACIM": 1.3e6, "END_DEGER": 515.0, "SERMAYE": 2.5e7}]}).encode()
    Fx = K.k62_fiyat_ayristir(ham)
    if list(Fx.tarih.dt.strftime("%Y-%m-%d")) != ["2010-01-04", "2010-01-05"] or list(Fx.kapanis) != [1.9, 2.0] or list(Fx.pd_usd) != [2.9e8, 3e8] or len(K.k62_fiyat_ayristir(b'{"value": []}')):
        hata.append("11) fiyat ayrıştırıcısı (sıra / alanlar / boş yanıt) yanlış")
    hm = json.dumps({"value": [{"itemCode": "3Z", "itemDescTr": "Ana Ortaklık Payları", "value1": "10", "value2": "25", "value3": "", "value4": None},
                               {"itemCode": "2O", "itemDescTr": "Ana Ortaklığa Ait Özkaynaklar", "value1": "100", "value2": "110", "value3": "120", "value4": "130"},
                               {"itemCode": "3L", "itemDescTr": "DÖNEM KARI (ZARARI)", "value1": "11", "value2": "26", "value3": "1", "value4": "2"}]}).encode()
    mx = K.k62_mali_ayristir(hm)
    if mx["kar"] != [10.0, 25.0, None, None] or mx["ozkaynak"] != [100.0, 110.0, 120.0, 130.0] or K.k62_mali_ayristir(b'{"value": []}') is not None:
        hata.append(f"11) mali tablo ayrıştırıcısı yanlış: {mx}")
    if K.k62_mali_ayristir(json.dumps({"value": [{"itemCode": "3Z", "itemDescTr": "Başka Bir Kalem", "value1": "1", "value2": "2", "value3": "3", "value4": "4"}]}).encode())["kar"] != [None] * 4:
        hata.append("11) açıklaması tutmayan kalem kâr olarak alındı")
    L = pd.DataFrame([{"publishDate": "12.08.2010 18:45:00", "stockCodes": "AAAA, AAAB", "year": 2010, "period": 2, "subject": "Finansal Rapor", "disclosureIndex": 1},
                      {"publishDate": "10.08.2010 09:15:00", "stockCodes": "AAAA, AAAB", "year": 2010, "period": 2, "subject": "Finansal Rapor", "disclosureIndex": 2},
                      {"publishDate": "11.08.2010 09:15:00", "stockCodes": "ZZZZ", "year": 2010, "period": 2, "subject": "Finansal Rapor", "disclosureIndex": 3},
                      {"publishDate": "09.03.2011 20:00:00", "stockCodes": "AAAA, AAAB", "year": 2010, "period": 4, "subject": "Finansal Rapor", "disclosureIndex": 4},
                      {"publishDate": "09.03.2011 20:00:00", "stockCodes": None, "year": 2010, "period": 4, "subject": "Finansal Rapor", "disclosureIndex": 5}])
    U = K.k62_duyurular(L, ["AAAA", "AAAB"], {"AAAA": 1.0, "AAAB": 9.0})
    if len(U) != 2 or set(U.kod) != {"AAAB"} or str(U.yayin.iloc[0]) != "2010-08-10 09:15:00" or int(U.bildirim.iloc[0]) != 2:
        hata.append(f"11) KAP ilk Finansal Rapor / en likit kod seçimi yanlış: {U.to_dict('records')}")
    Ka = K.k62_kod_adaylari(L)
    if list(Ka.kod) != ["AAAA", "AAAB", "ZZZZ"] or int(Ka[Ka.kod == "AAAA"].kayit.iloc[0]) != 3 or len(K.k62_kod_adaylari(L.assign(stockCodes="AB, TRSXYZ12345"))):
        hata.append("11) aday kod listesi yanlış")
    if K._k62_parcalar(2010, 2012) != [("01-01-2008", "31-12-2011"), ("01-01-2012", "31-12-2015")] or K._k62_parcalar(2026, 2026)[-1][1] != "31-08-2026":
        hata.append(f"11) fiyat parçaları yanlış: {K._k62_parcalar(2010, 2012)}")
    with tempfile.TemporaryDirectory() as td:
        Et = copy.deepcopy(E); Et["veri"]["kap"].update({"bas": "2010-01-01", "bit": "2010-01-28", "pencere_gun": 14, "sinir": 5}); cagri = []

        def sahte(a: str, b: str):
            cagri.append((a, b)); gunler = pd.date_range(a, b)
            return [{"publishDate": g_.strftime("%d.%m.%Y 10:00:00"), "stockCodes": "AAA", "year": 2009, "period": 4, "subject": "Finansal Rapor" if g_.day % 2 else "Faaliyet Raporu",
                     "disclosureIndex": int(g_.strftime("%Y%m%d"))} for g_ in gunler if g_.day <= 20][:5]
        d1 = K.k62_kap_indir(td, Et, sahte); Lk = K.k62_kap_oku(td); n1 = len(cagri); d2 = K.k62_kap_indir(td, Et, sahte)
        if d1["kayit"] != 10 or len(Lk) != 10 or set(Lk.subject) != {"Finansal Rapor"} or d1["hata"] or len(cagri) != n1 or d2["indirilen"] != 0 or d2["kayit"] != 10:
            hata.append(f"11) KAP pencere bölme / tekilleştirme / konu süzgeci / önbellek yanlış: {d1}, {d2}, çağrı {n1}->{len(cagri)}")
        # önbellekten demet: sentetik demetin 12 hissesi dosyalara yazılır, geri okunur
        kods = D["kod"][:12]; os.makedirs(os.path.join(td, "fiyat")); os.makedirs(os.path.join(td, "mali")); kayit = []
        for k in kods:
            jj = kol[k]
            pd.DataFrame({"tarih": tak, "kapanis": D["C"][:, jj], "ham": D["C"][:, jj], "pd": D["PD"][:, jj], "pd_usd": D["PDU"][:, jj], "hacim_tl": D["HU"][:, jj], "hacim_usd": D["HU"][:, jj],
                          "endeks": D["X"], "sermaye": 1.0}).to_csv(os.path.join(td, "fiyat", f"{k}.csv.gz"), index=False, compression="gzip")
            yl = {}
            for y_, gy in D["mali"][D["mali"].kod == k].groupby("yil"):
                gy = gy.sort_values("ceyrek"); yl[str(int(y_))] = {"kar": list(gy.kar_bir), "ozkaynak": list(gy.ozkaynak), "grup": "XI_29"}
            K._k62_json_yaz(os.path.join(td, "mali", f"{k}.json"), {"kod": k, "yil": yl})
            for r_ in D["duyuru"][D["duyuru"].kod == k].itertuples():
                kayit.append({"publishDate": pd.Timestamp(r_.yayin).strftime("%d.%m.%Y %H:%M:%S"), "stockCodes": f"{k}, {k}X", "year": int(r_.yil), "period": int(r_.ceyrek), "subject": "Finansal Rapor",
                              "disclosureIndex": len(kayit) + 100})
        K._k62_gz_yaz(os.path.join(td, "kap", "2099-01-01_2099-01-02.json.gz"), json.dumps(kayit).encode())
        Et2 = copy.deepcopy(E); Et2["veri"]["takvim_min_hisse"] = 5; Dd = K.k62_demet_kur(td, Et2)
        if Dd["kod"] != kods or len(Dd["takvim"]) != len(tak) or not np.allclose(Dd["C"], D["C"][:, :12]) or not np.allclose(Dd["X"], D["X"]) or len(Dd["duyuru"]) != len(kayit) \
                or len(Dd["mali"]) != int(D["mali"].kod.isin(kods).sum()):
            hata.append("11) önbellekten kurulan demet kaynakla aynı değil")
        vsa = K.k62_veri_sha(td); open(os.path.join(td, "mali", f"{kods[0]}.json"), "a").write(" ")
        if K.k62_veri_sha(td)["sha256"] == vsa["sha256"] or vsa["fiyat_dosya"] != 12 or vsa["mali_dosya"] != 12:
            hata.append("11) veri sha256'sı dosya değişince değişmedi / dosya sayısı yanlış")

    # 12) uçtan uca sentetik koşu (A + B + C) + rapor
    with tempfile.TemporaryDirectory() as td:
        try:
            Sb = sentetik(n=90, bas="2015-06-01", bit="2026-08-31", tohum=21); cik = os.path.join(td, "c"); os.makedirs(cik)
            y = K.k62_onkayit_yaz(cik, kapsam=K.k62_kapsam(demet=Sb["D"], v_semboller=sorted(Sb["V"])), veri_sha={"sha256": "c" * 64, "v_bist_sha256": None})
            Rk = K.k62_kos(cik, demet=Sb["D"], V=Sb["V"], onkayit_yol=y, git_sart=False)
            Tb, Cz, m = Rk["tablo"], Rk["olcut"], Rk["meta"]
            for ad in ("tablo", "regresyon", "olcut", "olay", "meta", "rapor"):
                if not os.path.exists(K._k62_yol(ad, cik)):
                    hata.append(f"12) çıktı yok: {ad}")
            b61 = Tb[(Tb.bolum == "B") & (Tb.ufuk == 61) & ~Tb.tekil & (Tb.notu == "")]
            if set(b61.donem) != {"2017-2021", "2022-2026", "2023-2026"} or set(b61.olcu) != {"SUETF", "EAR"} or int(b61.aile_sinama.iloc[0]) != 18:
                hata.append(f"12) B dönemleri / ölçüleri / sınama ailesi yanlış: {set(b61.donem)}, {set(b61.olcu)}, {b61.aile_sinama.iloc[0]}")
            if not (b61.okuma == "TUTAR").all() or not b61.bh_pead.all():
                hata.append(f"12) ekili etkili sentetik veride B dönemleri TUTAR çıkmadı: {b61[['donem', 'olcu', 'pead', 'p', 'okuma']].to_dict('records')}")
            kirli = Tb[(Tb.bolum == "B") & Tb.notu.str.startswith("TMS29")]; ana_s = b61[(b61.olcu == "SUETF") & (b61.donem == "2023-2026")].iloc[0]; Xk = Rk["olay"]
            if not len(kirli) or set(kirli.olcu) != {"SUETF"} or set(kirli.donem) != {"2022-2026", "2023-2026"} or ana_s.kapsam != "TMS29 temiz çeyrekler" \
                    or set(b61[b61.kapsam != ""].donem) != {"2022-2026", "2023-2026"} or set(b61[b61.kapsam != ""].olcu) != {"SUETF"}:
                hata.append("12) TMS 29: SUETF ana satırı temiz çeyrekler / kirli bilgi satırı (yalnız 2022-2026 ve 2023-2026) kuralı tutmuyor")
            mk = K._k62_t_maske(Xk, "2023-01-01", "2026-12-31") & ~K._k62_haric_maske(Xk, E["bolum_b"]["tms29_haric"]) & (Xk.SUETF_tertil.to_numpy() >= 0)
            if int(ana_s.n) != int(mk.sum()) or Xk[mk].mali_ceyrek.isin(["2022Q4", "2023Q4", "2024Q1", "2024Q2", "2024Q3", "2024Q4", "2025Q4"]).any() or int(ana_s.n) >= int(kirli[(kirli.donem == "2023-2026") & (kirli.ufuk == 61)].n.iloc[0]):
                hata.append("12) TMS 29 temiz satırında kirli çeyrek olayı var / sayı elle sayımla aynı değil")
            sc = K.k62_tertil_onsel(Xo_ := K.k62_olay_tablosu(Sb["D"], E, True).query("onsel").reset_index(drop=True), "SUETF", E, E["bolum_b"]["tms29_haric"])
            kq = Xo_.yil * 10 + Xo_.ceyrek
            if (sc[kq.isin([20224, 20234, 20241, 20242, 20243, 20244, 20254]).to_numpy()] != -1).any() or (sc[(kq == 20251).to_numpy()] != -1).any() or not (sc[(kq == 20231).to_numpy()] >= 0).any() \
                    or not (sc[(kq == 20252).to_numpy()] >= 0).any() or not (sc[(kq == 20261).to_numpy()] >= 0).any():
                hata.append("12) C: TMS 29 kirli çeyrek olayı sınıflandı / havuz kuralı (en yakın temiz çeyrek, en çok 4 geride) tutmuyor")
            g31 = Xo_[(kq == 20231)].index[3]; hv = Xo_[(kq == 20223) & (Xo_.karar_i <= Xo_.karar_i[g31])].SUETF.to_numpy(float); al_, us_ = np.quantile(hv, [1 / 3, 2 / 3])
            if sc[g31] != (2 if Xo_.SUETF[g31] >= us_ else (0 if Xo_.SUETF[g31] <= al_ else 1)):
                hata.append("12) C: 2023Ç1 olayının havuzu 2022Ç3 (en yakın temiz çeyrek) değil")
            Ek_ = Rk["olay"]; son_t = pd.to_datetime(Ek_.t).max(); tk = Sb["D"]["takvim"]
            if int(tk.searchsorted(son_t)) + 61 > len(tk) - 1 or tk[-1] > pd.Timestamp("2026-08-31"):
                hata.append("12) fon krizi kesiği: penceresi 31.08.2026'yı aşan olay ölçüldü")
            if set(Cz.donem) != {"2023", "2024-26", "2017-2021", "2022-2026", "2023-2026"} or set(Cz.uc) != {"Q1", "Q3"} or set(m["karar_c"]) != {"SUETF Q3", "SUETF Q1", "EAR Q3", "EAR Q1"}:
                hata.append(f"12) C hücreleri / karar anahtarları yanlış: {set(Cz.donem)}, {set(m['karar_c'])}")
            if any(v not in ("BIST-BİLGİ: TUTAR", "BIST-BİLGİ: TUTAR (kaçınma)", "İZ DEĞİL") for v in m["karar_c"].values()) or any("ADAY" in v or v == "İZ" for v in m["karar_c"].values()):
                hata.append(f"12) C kararı izin verilen etiketlerden değil: {m['karar_c']}")
            q3 = Cz[(Cz.olcu == "SUETF") & (Cz.uc == "Q3") & (Cz.donem == "2024-26")].iloc[0]; q1 = Cz[(Cz.olcu == "SUETF") & (Cz.uc == "Q1") & (Cz.donem == "2024-26")].iloc[0]
            if not (q3.ort_fark > 0 > q1.ort_fark and q3.n >= 30):
                hata.append(f"12) C: ekili etkide Q3 eşli farkı artı, Q1 eksi çıkmadı: {q3.ort_fark}, {q1.ort_fark}")
            import FON_IZI as FI
            Eo2 = Ek_.copy(); P = FI.fi_olcut_panel(Sb["V"]); Evb = K.k62_olay_tablosu(Sb["D"], E, True); Xo = Evb[Evb.onsel].reset_index(drop=True); so2 = K.k62_tertil_onsel(Xo, "SUETF", E)
            so2 = K.k62_tertil_onsel(Xo, "SUETF", E, E["bolum_b"]["tms29_haric"]); G = K.k62_tekil(Xo[so2 == 2], 60); Tt = FI.fi_olcut_olay(P, pd.DataFrame({"sembol": G.kod.to_numpy(), "giris": pd.to_datetime(G.giris).to_numpy()}))
            h = FI.fi_olcut_hucre(Tt[(Tt.giris >= pd.Timestamp("2024-01-01")) & (Tt.giris <= pd.Timestamp("2026-12-31"))])
            if abs(h["ort_fark"] - q3.ort_fark) > 1e-12 or h["n"] != q3.n:
                hata.append("12) C hücresi FON_IZI fi_olcut_* ile bağımsız yeniden hesapla aynı değil")
            g0 = G.iloc[0]; d0 = int(P["tarih"].get_loc(pd.Timestamp(g0.giris))); jj = P["kol"][g0.kod]; v0 = Sb["V"][g0.kod]
            if pd.Timestamp(g0.giris) != tk[int(g0.t_i) + 2] or abs(P["R"][d0, jj] - (v0.Close.iloc[d0 + 59] / v0.Open.iloc[d0] - 1)) > 1e-9:
                hata.append("12) C girişi t+2 açılışı / r60 = 60. gün kapanışı değil")
            rap = open(K._k62_yol("rapor", cik), encoding="utf-8").read(); once = open(K._k62_yol("rapor", cik), "rb").read(); K.k62_rapor(cik)
            if open(K._k62_yol("rapor", cik), "rb").read() != once:
                hata.append("12) `rapor` çıktılardan aynı raporu yeniden üretmedi")
            for parca in ("## A. Birebir tekrar", "## B. Dönemler", "## C. Proje cetveli", "VERİ YOK", "K28 ile karşılaştırma", "çoklu test", "Kontrollü regresyon", "İZ / ADAY denmez"):
                if parca not in rap:
                    hata.append(f"12) raporda '{parca}' yok")
            Tc = pd.read_csv(K._k62_yol("tablo", cik)); r0 = Tc[(Tc.bolum == "B") & (Tc.donem == "2017-2021") & (Tc.olcu == "EAR") & (Tc.ufuk == 61) & ~Tc.tekil].iloc[0]
            if ("%" + f"{100 * r0.pead:.2f}".replace(".", ",")) not in rap:
                hata.append("12) rapordaki sayı k62_tablo.csv'den yeniden üretilemedi")
            for f in os.listdir(cik):
                if f.endswith((".md", ".csv", ".json")) and K._K62_EPOSTA.search(open(os.path.join(cik, f), encoding="utf-8").read()):
                    hata.append(f"12) sentetik çıktıda e-posta var: {f}")
            try:
                K.k62_kos(cik, veri=os.path.join(td, "yok"), onkayit_yol=y, git_sart=False); hata.append("12) verisi ön kayıttakinden farklı gerçek koşu durmadı")
            except (K.K62Hata, FileNotFoundError):
                pass
        except Exception as ex:
            import traceback
            hata.append(f"12) uçtan uca sentetik koşu çöktü: {type(ex).__name__} {ex}\n{traceback.format_exc()[-1500:]}")

    # 13) e-posta / anahtar yok
    for ad in ("K62.py", "test_k62.py"):
        s_ = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if [x for x in K._K62_EPOSTA.findall(s_) if not x.endswith("@invalid")] or re.search(r"(api[_-]?key|token|secret|password)\s*=\s*['\"][A-Za-z0-9]{12,}", s_, re.I) or ("sec" + ".gov") in s_.lower():
            hata.append(f"13) {ad} içinde e-posta / anahtar / SEC adresi var")
    if os.path.exists(gercek) and K._K62_EPOSTA.search(open(gercek, encoding="utf-8").read()):
        hata.append("13) gerçek ön kayıtta e-posta var")
    return hata


if __name__ == "__main__":
    Hh = testler()
    if Hh:
        print("K62 TEST: HATA", len(Hh)); print("\n".join(Hh)); sys.exit(1)
    print("K62 TEST: 13/13 bölüm GEÇTİ")
