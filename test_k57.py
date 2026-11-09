"""K57 testleri (ağ gerekmez; çıktı denetimleri için önce `python K57.py kos`). Çalıştırma: python test_k57.py

1) çakışma kapısı  2) ön kayıt mührü ve zamanı  3) geleceğe bakma yok (temel / fon / pay bilgi tarihi <= açıklama günü; giriş tepkiden
sonra; kayan eşik geleceği görmüyor)  4) olay sayıları > 0  5) çıktılar ve hucre.csv yapısı  6) süzgeç birimleri (F2, F4 bölünme,
ABD frames 4. çeyrek türetme, bilgi tarihi)  7) karar mantığı  8) e-posta yok  9) K57-B (ayrı mühür, çıktılar, B1 geniş
evrende geleceğe bakma yok, e-posta yok; önce `python K57.py b_kos`)  10) K57-C (mühür çıktılardan önce, K57 / K57-B mühürleri ve
kaynakları değişmedi, C1-C3 hücreleri ve karar, geleceğe bakma yok, Ç150 bloğu, e-posta yok; önce `python K57.py c_kos`).
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import K57 as K  # noqa: E402

C = K.K57_YOL["cikti"]


def _sentetik_frames(klasor: str) -> None:
    """İki şirket: 1 (takvim yılı, 2023Q4 yalnız yıllıkta), 2 (veri yok). Bütün gerekli dosyalar ('{}' boş)."""
    os.makedirs(klasor, exist_ok=True)
    veri = {}
    gelir = {"CY2022Q1": 100, "CY2022Q2": 100, "CY2022Q3": 100, "CY2022Q4": 100, "CY2023Q1": 110, "CY2023Q2": 120, "CY2023Q3": 130}
    sinir = {1: ("01-01", "03-31"), 2: ("04-01", "06-30"), 3: ("07-01", "09-30"), 4: ("10-01", "12-31")}
    for c, v in gelir.items():
        y, q = int(c[2:6]), int(c[-1])
        veri[("Revenues", c)] = [{"cik": 1, "start": f"{y}-{sinir[q][0]}", "end": f"{y}-{sinir[q][1]}", "val": v, "accn": "x"}]
        veri[("NetIncomeLoss", c)] = [{"cik": 1, "start": f"{y}-{sinir[q][0]}", "end": f"{y}-{sinir[q][1]}", "val": v / 10, "accn": "x"}]
    veri[("Revenues", "CY2023")] = [{"cik": 1, "start": "2023-01-01", "end": "2023-12-31", "val": 110 + 120 + 130 + 250, "accn": "x"}]
    veri[("NetIncomeLoss", "CY2023")] = [{"cik": 1, "start": "2023-01-01", "end": "2023-12-31", "val": 11 + 12 + 13 + 30, "accn": "x"}]
    veri[("StockholdersEquity", "CY2023Q4I")] = [{"cik": 1, "end": "2023-12-31", "val": 1000, "accn": "x"}]
    veri[("Liabilities", "CY2023Q4I")] = [{"cik": 1, "end": "2023-12-31", "val": 2000, "accn": "x"}]
    for etiket, donem in K.k57_sec_listesi():
        with open(os.path.join(klasor, f"us-gaap_{etiket}_{donem}.json"), "w") as f:
            json.dump({"data": veri[(etiket, donem)]} if (etiket, donem) in veri else {}, f)


def testler() -> list:
    hata = []
    # 1) çakışma kapısı: başka dosyanın adını ezince durur; temiz ad alanında yüklenir
    src = open(os.path.join(KOK, "K57.py"), encoding="utf-8").read().replace("from __future__ import annotations\n", "")
    g = {"__name__": "kapi_test", "k57_kos": object(), "_CK_KAYIT": {"k57_kos": "BASKA.py"}}
    try:
        exec(compile(src, "K57.py", "exec"), g)
        hata.append("1) çakışma kapısı başka dosyanın adını ezince durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"1) beklenmeyen hata: {ex}")
    g2 = {"__name__": "kapi_test2"}
    try:
        exec(compile(src, "K57.py", "exec"), g2)
        exec(compile(src, "K57.py", "exec"), g2)   # aynı dosyanın yeniden yüklenmesi serbest
    except Exception as ex:
        hata.append(f"1) temiz yükleme / yeniden yükleme durdu: {type(ex).__name__} {ex}")
    # 2) ön kayıt: mühür, zaman, üzerine yazmama
    ok = K.k57_onkayit_dogrula()
    meta = json.load(open(os.path.join(C, K.K57_DOSYA["meta"]), encoding="utf-8"))
    if not ok["zaman_utc"] or pd.Timestamp(ok["zaman_utc"]) > pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")):
        hata.append(f"2) ön kayıt koşudan sonra yazılmış: {ok['zaman_utc']} vs {meta['kos_baslangic']}")
    if meta["onkayit"]["sha"] != K.k57_esik_sha():
        hata.append("2) koşunun mührü bugünkü eşiklerle aynı değil")
    with tempfile.TemporaryDirectory() as td:
        y = K.k57_onkayit(td); ilk = open(y, encoding="utf-8").read()
        K.k57_onkayit(td)
        if open(y, encoding="utf-8").read() != ilk:
            hata.append("2) ön kayıt üzerine yazıldı")
        open(y, "w", encoding="utf-8").write(ilk.replace(K.k57_esik_sha(), "0" * 64))
        try:
            K.k57_onkayit_dogrula(td); hata.append("2) bozuk mühür kabul edildi")
        except K.K57Hata:
            pass
    # 3) geleceğe bakma yok
    Xb = pd.read_csv(os.path.join(C, K.K57_DOSYA["bist"]), parse_dates=["D", "d0", "tepki_son", "giris", "bilgi_son", "fon_bil"])
    Xa = pd.read_csv(os.path.join(C, K.K57_DOSYA["abd"]), parse_dates=["D", "d0", "tepki_son", "giris", "pay_filed"])
    for ad, X in (("BIST", Xb), ("ABD", Xa)):
        if not ((X.d0 < X.D) & (X.tepki_son >= X.D) & (X.giris > X.tepki_son)).all():
            hata.append(f"3) {ad}: d0 < D <= tepki günü < giriş sırası bozuk")
    if (Xb.bilgi_son.notna() & (Xb.bilgi_son > Xb.D)).any():
        hata.append(f"3) BIST: açıklama gününden sonra bilinen temel değer kullanıldı ({int((Xb.bilgi_son > Xb.D).sum())})")
    if Xb.satis0.notna().sum() == 0 or (Xb.satis0.notna() & Xb.bilgi_son.isna()).any():
        hata.append("3) BIST: kullanılan temel değerin bilgi tarihi yok")
    if (Xb.fon_bil.notna() & (Xb.fon_bil >= Xb.D)).any():
        hata.append("3) BIST: fon payı açıklama gününde / sonra yayımlanmış rapordan")
    if (Xa.pay_filed.notna() & (Xa.pay_filed > Xa.D)).any() or (Xa.pay_yil.notna() & Xa.pay_filed.isna()).any():
        hata.append("3) ABD: pay değişimi açıklama gününden sonra başvurulmuş bildirimden")
    if "bilgi_son" in Xa and (pd.to_datetime(Xa.bilgi_son).notna() & (pd.to_datetime(Xa.bilgi_son) > Xa.D)).any():
        hata.append("3) ABD: açıklama gününden sonra bilinen temel değer kullanıldı")
    kes = Xb.tepki_son.quantile(0.5); Y = Xb[Xb.tepki_son <= kes]
    e1 = K.k57_kayan_esik(Y.tepki_son, Y.ear, 0.8, 92, 30)
    if not np.allclose(e1, Y.f7_esik.to_numpy(float), equal_nan=True):
        hata.append("3) F7 eşiği geleceği görüyor (sonraki olaylar eşiği değiştiriyor)")
    Yb = Xb[Xb.D <= Xb.D.quantile(0.6)]
    if not np.allclose(K.k57_kayan_esik(Yb.D, Yb.satis_yoy, 0.6, 92, 30), Yb.f1_esik.to_numpy(float), equal_nan=True):
        hata.append("3) BIST F1 eşiği geleceği görüyor")
    kriz = pd.Timestamp(K.FI.FI_OLCUT["kriz"])
    if (Xb.fark.notna() & (Xb.giris > kriz)).any() or (Xa.fark.notna() & (Xa.giris > kriz)).any():
        hata.append("3) kriz sonrası giriş ölçülmüş")
    # 4) olay sayıları
    for ad, X in (("BIST", Xb), ("ABD", Xa)):
        if len(X) == 0 or X.V0.sum() == 0 or X.fark.notna().sum() == 0:
            hata.append(f"4) {ad}: olay / V0 / ölçülen olay yok")
    if Xb.V3.sum() == 0:
        hata.append("4) BIST V3 olayı yok")
    if not (Xb.V3 <= Xb.V2).all() or not (Xb.V2 <= Xb.V1).all() or not (Xb.V1 <= Xb.V0).all():
        hata.append("4) BIST varyantlar iç içe değil")
    # 5) çıktılar
    for a in ("onkayit", "bist", "abd", "hucre", "rapor", "meta"):
        if not os.path.exists(os.path.join(C, K.K57_DOSYA[a])):
            hata.append(f"5) çıktı yok: {K.K57_DOSYA[a]}")
    Z = pd.read_csv(os.path.join(C, K.K57_DOSYA["hucre"]))
    gerek = {"deney", "varyant", "pazar", "donem", "rol", "n", "ort_fark", "alt95", "ust95", "sira", "portfoy", "portfoy_esli_p90",
             "portfoy_yuzdelik", "tutar", "karar"}
    if not gerek <= set(Z.columns):
        hata.append(f"5) hucre.csv sütun eksik: {gerek - set(Z.columns)}")
    ana = Z[Z.deney == "ANA"]
    if len(ana) != 5 * 5 or set(ana.varyant) != set(K.K57_ESIK["varyant"]):
        hata.append(f"5) ANA satır sayısı {len(ana)} != 25")
    if set(Z.deney) != {"ANA", "D1", "D2", "D3"}:
        hata.append(f"5) devam deneyleri eksik: {set(Z.deney)}")
    O = K._k57_olcut()
    for r in Z.itertuples():
        bek = bool(r.n >= O["n_esik"] and r.alt95 > 0 and r.sira > 0.5 and r.portfoy > r.portfoy_esli_p90) if r.n and r.n > 0 else False
        if bek != bool(r.tutar):
            hata.append(f"5) tutar hesabı yanlış: {r.deney} {r.varyant} {r.pazar} {r.donem}"); break
    rap = open(os.path.join(C, K.K57_DOSYA["rapor"]), encoding="utf-8").read()
    for parca in ("## KARAR:", "Ç148", "en son 10 V3", "Önceden yazılı 3 devam"):
        if parca not in rap:
            hata.append(f"5) raporda '{parca}' yok")
    # 6) süzgeç birimleri
    f2 = K._k57_f2([150, 150, 150, 100], [100, 100, 100, 100], [100, 100, 100, 100], [5, -1, 5, 5], [4, -2, 6, 4], 1.4)
    if list(f2) != [True, False, False, False]:
        hata.append(f"6) F2 yanlış: {list(f2)}")
    f4 = K.k57_f4(pd.Series([0.05, 0.25, 1.0, 1.97, 2.5, -0.5, np.nan]))
    if list(f4) != [True, False, True, True, False, True, False]:
        hata.append(f"6) F4 / bölünme kuralı yanlış: {list(f4)}")
    eski = dict(K.K57_YOL)
    with tempfile.TemporaryDirectory() as td:
        K.K57_YOL["frames"] = td; K.K57_YOL["frames_ek"] = []
        try:
            _sentetik_frames(td)
            T, neden = K.k57_abd_temel_tablo()
            if T is None:
                hata.append(f"6) sentetik frames okunamadı: {neden}")
            else:
                q4 = T["Q"].get(("1", "Revenues"), {}).get(2023 * 4 + 3)
                if q4 is None or abs(q4[1] - 250) > 1e-9:
                    hata.append(f"6) 4. çeyrek türetme yanlış: {q4}")
                N = pd.DataFrame({"sembol": ["AAA"] * 2, "D": pd.to_datetime(["2023-10-25", "2024-02-01"])})
                B = pd.DataFrame({"cik": ["1"], "adsh": ["a"], "form": ["10-Q"], "period": pd.to_datetime(["2023-06-30"]),
                                  "filed": pd.to_datetime(["2023-08-05"])})
                bilgi = K._k57_abd_bilgi_tarihleri(T, N, B, {"1": "AAA"})
                if bilgi[("1", 2023 * 4 + 2)] != pd.Timestamp("2023-10-25") or bilgi[("1", 2023 * 4 + 1)] != pd.Timestamp("2023-08-05"):
                    hata.append("6) ABD bilgi tarihi yanlış")
                X = pd.DataFrame({"sembol": ["AAA", "AAA"], "D": pd.to_datetime(["2023-10-25", "2024-02-01"])})
                X = K.k57_abd_temel_ekle(X, T, bilgi, {"1": "AAA"}, (1.4, 1.2))
                if not (X.ceyrek_sira.tolist() == [2023 * 4 + 2, 2023 * 4 + 3] and abs(X.satis_yoy.iloc[0] - 0.30) < 1e-9
                        and abs(X.satis_yoy.iloc[1] - 1.5) < 1e-9 and bool(X.F1.iloc[0]) and not bool(X.F2.iloc[0]) and bool(X.F2.iloc[1])
                        and bool(X.F3.iloc[1]) and not bool(X.F3.iloc[0])):
                    hata.append(f"6) ABD temel süzgeçleri yanlış: {X[['ceyrek_sira', 'satis_yoy', 'F1', 'F2', 'F3']].to_dict('records')}")
                if (pd.to_datetime(X.bilgi_son) > X.D).any():
                    hata.append("6) ABD temel: gelecekteki bilgi kullanıldı")
        finally:
            K.K57_YOL.update(eski)
    # 7) karar mantığı
    zt = pd.DataFrame([{"deney": "ANA", "varyant": v, "pazar": p, "donem": d, "tutar": True}
                       for v in ("V0", "V3") for p, d in (("ABD", "2021-22"), ("ABD", "2023"), ("ABD", "2024-26"), ("BIST", "2022-23"), ("BIST", "2024-26"))])
    k1 = K.k57_karar(zt, True); k0 = K.k57_karar(zt, False)
    if k1[("ANA", "V3")]["karar"] != "ABD-ADAY (AVRUPA VERİSİ YOK)" or not k0[("ANA", "V3")]["karar"].startswith("ÖLÇÜLEMEDİ") \
            or k0[("ANA", "V0")]["karar"] != "ABD-ADAY (AVRUPA VERİSİ YOK)":
        hata.append(f"7) karar mantığı yanlış: {k1}, {k0}")
    zt.loc[(zt.pazar == "ABD") & (zt.donem == "2024-26"), "tutar"] = False
    if K.k57_karar(zt, True)[("ANA", "V3")]["karar"] != "İZ DEĞİL":
        hata.append("7) bir ABD hücresi tutmazken İZ DEĞİL denmedi")
    # 8) e-posta yok (kod ve çıktılar)
    for y in [os.path.join(KOK, "K57.py"), os.path.join(KOK, "test_k57.py")] + [os.path.join(C, K.K57_DOSYA[a]) for a in ("onkayit", "rapor", "meta")]:
        if re.search(r"[\w.+-]+@(gmail|hotmail|yahoo|outlook|icloud|yandex)\.", open(y, encoding="utf-8").read()):
            hata.append(f"8) e-posta var: {y}")
    hata += testler_b()
    hata += testler_c()
    return hata


def testler_b() -> list:
    """9) K57-B: ayrı mühür (var, tutuyor, K57 mührü değişmedi, çıktılardan ve Yahoo indirmesinden önce), çıktı yapısı ve tutar / karar
    hesabı, B1 geniş evrende geleceğe bakma yok (bilgi tarihi, giriş sırası, likidite yalnız tepki gününe kadar, F7 kayan eşiği, kriz
    kesiği), e-posta yok."""
    hata = []
    # mühür
    try:
        okb = K.k57b_onkayit_dogrula()
    except K.K57Hata as ex:
        return [f"9) K57-B ön kaydı: {ex}"]
    ok = K.k57_onkayit_dogrula()
    metin = open(okb["yol"], encoding="utf-8").read()
    if f"K57 mührü (değişmeden): {ok['sha']}" not in metin:
        hata.append("9) K57-B ön kaydı K57 mührünü taşımıyor / K57 mührü değişmiş")
    if pd.Timestamp(okb["zaman_utc"]) <= pd.Timestamp(ok["zaman_utc"]):
        hata.append("9) K57-B ön kaydı K57 ön kaydından önce")
    with tempfile.TemporaryDirectory() as td:
        import shutil
        shutil.copy(os.path.join(C, K.K57_DOSYA["onkayit"]), td)
        y = K.k57b_onkayit(td); ilk = open(y, encoding="utf-8").read(); K.k57b_onkayit(td)
        if open(y, encoding="utf-8").read() != ilk:
            hata.append("9) K57-B ön kaydı üzerine yazıldı")
        open(y, "w", encoding="utf-8").write(ilk.replace(K.k57b_esik_sha(), "0" * 64))
        try:
            K.k57b_onkayit_dogrula(td); hata.append("9) K57-B bozuk mühür kabul edildi")
        except K.K57Hata:
            pass
    yol = {a: os.path.join(C, K.K57B_DOSYA[a]) for a in K.K57B_DOSYA}
    eksik = [K.K57B_DOSYA[a] for a, y in yol.items() if not os.path.exists(y)]
    if eksik:
        return hata + [f"9) K57-B çıktısı yok: {eksik} (önce `python K57.py b_kos`)"]
    meta = json.load(open(yol["meta"], encoding="utf-8"))
    bas = pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")); muhur = pd.Timestamp(okb["zaman_utc"])
    if muhur > bas:
        hata.append(f"9) K57-B ön kaydı koşudan sonra: {okb['zaman_utc']} > {meta['kos_baslangic']}")
    ilk_ind = (meta.get("yahoo") or {}).get("ilk_indirme_utc")
    if ilk_ind and pd.Timestamp(ilk_ind.replace(" UTC", "")) < muhur:
        hata.append(f"9) Yahoo fiyatları K57-B ön kaydından önce indirilmiş: {ilk_ind}")
    if meta["onkayit_b"]["sha"] != K.k57b_esik_sha() or meta["k57_muhur"] != K.k57_esik_sha():
        hata.append("9) koşunun mühürleri bugünkü eşiklerle aynı değil")
    for y in (yol["hucre"], yol["rapor"], yol["b1_olay"], yol["b1_evren"]):
        if pd.Timestamp(os.path.getmtime(y), unit="s") < muhur:
            hata.append(f"9) çıktı ön kayıttan eski: {os.path.basename(y)}")
    if not meta.get("yeniden_uretim") or not all(r["esit"] for r in meta["yeniden_uretim"]):
        hata.append("9) K57 ANA V1 yeniden üretimi tutmadı / yapılmadı")
    # hücreler
    Z = pd.read_csv(yol["hucre"]); O = K._k57_olcut()
    bek = {("B1", "ABD"), ("B2", "ABD"), ("B2", "BIST"), ("B3", "ABD"), ("B3", "BIST")}
    if set(zip(Z.deney, Z.pazar)) != bek or len(Z) != 3 + 5 + 5:
        hata.append(f"9) hucre_b.csv deneme / pazar / satır yanlış: {sorted(set(zip(Z.deney, Z.pazar)))} {len(Z)}")
    if set(Z[Z.deney == "B2"].ufuk) != {20} or set(Z[Z.deney != "B2"].ufuk) != {60}:
        hata.append("9) ufuklar yanlış (B2 20, B1 / B3 60)")
    for r in Z.itertuples():
        b = bool(r.n >= O["n_esik"] and r.alt95 > 0 and r.sira > 0.5 and r.portfoy > r.portfoy_esli_p90) if r.n and r.n > 0 else False
        if b != bool(r.tutar):
            hata.append(f"9) tutar hesabı yanlış: {r.deney} {r.pazar} {r.donem}"); break
    if set(Z[Z.rol == "KARAR"].apply(lambda r: (r.pazar, r.donem), axis=1)) != {("ABD", "2023"), ("ABD", "2024-26")}:
        hata.append("9) karar hücreleri ABD 2023 + ABD 2024-26 değil")
    for d, g in Z.groupby("deney"):
        iki = all(bool(g[(g.pazar == "ABD") & (g.donem == x)].tutar.iloc[0]) for x in ("2023", "2024-26"))
        if iki != g.karar.iloc[0].startswith("ABD-ADAY"):
            hata.append(f"9) {d} kararı hücrelerle uyuşmuyor: {g.karar.iloc[0]}")
    # B1 geniş evren: geleceğe bakma yok
    X = pd.read_csv(yol["b1_olay"], parse_dates=["D", "d0", "tepki_son", "giris", "bilgi_son"])
    for c in ("F7", "F1", "F2", "F3", "V1"):
        X[c] = K._k57b_bayrak(X[c])
    if not ((X.d0 < X.D) & (X.tepki_son >= X.D) & (X.giris > X.tepki_son)).all():
        hata.append("9) B1: d0 < D <= tepki günü < giriş sırası bozuk")
    if (X.bilgi_son.notna() & (X.bilgi_son > X.D)).any() or ((X.F1 | X.F2 | X.F3) & X.bilgi_son.isna()).any():
        hata.append("9) B1: açıklama gününden sonra bilinen (ya da bilgi tarihi olmayan) temel değer kullanıldı")
    if (X.likit20 < K.K57B_ESIK["likit_taban_usd"]).any() or X.likit20.isna().any():
        hata.append("9) B1: likidite tabanı altında olay var")
    kriz = pd.Timestamp(K.FI.FI_OLCUT["kriz"])
    if (X.fark.notna() & (X.giris > kriz)).any():
        hata.append("9) B1: kriz sonrası giriş ölçülmüş")
    if not (X.V1 == (X.F7 & X.F1 & X.F2 & X.F3)).all() or X.V1.sum() == 0:
        hata.append("9) B1: V1 = F7 + F1 + F2 + F3 değil / V1 olayı yok")
    kes = X.tepki_son.quantile(0.5); Y = X[X.tepki_son <= kes]
    E = K.K57_ESIK
    if not np.allclose(K.k57_kayan_esik(Y.tepki_son, Y.ear, 1 - E["F7_dilim"], E["F7_pencere_gun"], E["F7_min_n"]), Y.f7_esik.to_numpy(float), equal_nan=True):
        hata.append("9) B1: F7 eşiği geleceği görüyor ya da taban altı olaylarla hesaplanmış")
    U = pd.read_csv(yol["b1_evren"], parse_dates=["son"])
    if (U.son.notna() & (U.son > kriz)).any():
        hata.append("9) B1: fiyat kriz gününden sonrasını içeriyor")
    if not set(X.sembol) <= set(U[U.durum == "fiyat"].sembol):
        hata.append("9) B1: evren dışı hisseden olay")
    # likidite yalnız tepki gününe kadarki fiyatlardan (önbellek varsa; Colab'da yoksa atlanır)
    if os.path.isdir(K.K57B_YOL["fiyat"]):
        orn = X.sample(min(40, len(X)), random_state=57); kotu = 0
        for r in orn.itertuples():
            d, _ = K.k57b_yahoo_oku(K._k57b_dosya(r.sembol))
            if d is None:
                kotu += 1; continue
            g = d[d.index <= r.tepki_son].tail(K.K57B_ESIK["likit_gun"])
            if len(g) < K.K57B_ESIK["likit_gun"] or g.index[-1] != r.tepki_son or abs(float((g.Close * g.Volume).median()) / r.likit20 - 1) > 1e-9:
                kotu += 1
        if kotu:
            hata.append(f"9) B1: likidite tepki gününe kadarki 20 günden hesaplanmamış ({kotu} / {len(orn)})")
    # likidite fonksiyonu sentetik: tepki gününden sonraki hacim değeri değiştirmez
    gun = pd.bdate_range("2024-01-01", periods=40)
    d = pd.DataFrame({"Close": 10.0, "Volume": np.r_[np.full(30, 1e5), np.full(10, 1e9)]}, index=gun)
    Xs = pd.DataFrame({"sembol": ["S"], "tepki_son": [gun[29]]})
    if abs(K.k57b_likit({"S": d}, Xs)[0] - 1e6) > 1e-6:
        hata.append("9) k57b_likit geleceği görüyor")
    # e-posta yok
    for y in [os.path.join(KOK, "K57.py"), os.path.join(KOK, "test_k57.py")] + [yol[a] for a in ("onkayit", "rapor", "meta", "hucre", "b1_evren")]:
        if re.search(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b", open(y, encoding="utf-8").read()):
            hata.append(f"9) e-posta var: {os.path.basename(y)}")
    rap = open(yol["rapor"], encoding="utf-8").read()
    for parca in ("## KARAR:", "Ç149", "Düz dille", "## B1", "## B2", "## B3"):
        if parca not in rap:
            hata.append(f"9) K57B raporunda '{parca}' yok")
    return hata


def testler_c() -> list:
    """10) K57-C: mühür (var, tutuyor, K57 / K57-B mühürleri ve K57-B kaynak dosyaları değişmedi, koşudan ve çıktılardan önce, üzerine
    yazılmaz, çıktıdan sonra yazılamaz), hücre / karar yapısı, olaylarda geleceğe bakma yok (bilgi tarihi, pay bildirimi, giriş sırası,
    likidite tabanı, kayan F7 eşikleri, kriz kesiği), deneme maskeleri, Ç150 bloğu (tek tırnak), e-posta yok."""
    import ast
    import shutil
    hata = []
    try:
        oc = K.k57c_onkayit_dogrula()
    except K.K57Hata as ex:
        return [f"10) K57-C ön kaydı: {ex}"]
    ok, okb = K.k57_onkayit_dogrula(), K.k57b_onkayit_dogrula()
    muhur = pd.Timestamp(oc["zaman_utc"])
    if muhur <= pd.Timestamp(okb["zaman_utc"]) or muhur <= pd.Timestamp(ok["zaman_utc"]):
        hata.append("10) K57-C ön kaydı K57 / K57-B ön kayıtlarından önce")
    metin = open(oc["yol"], encoding="utf-8").read()
    if f"K57 mührü (değişmeden): {ok['sha']}" not in metin or f"K57B mührü (değişmeden): {okb['sha']}" not in metin:
        hata.append("10) K57-C ön kaydı K57 / K57-B mühürlerini taşımıyor")
    if "BOŞLUK" not in metin or "K57B_ON_KAYIT.md §6" not in metin:
        hata.append("10) K57-C ön kaydı boşluk doldurmayı / kaynağını yazmıyor")
    for d in ("C1", "C2", "C3"):
        if f"- {d}: {K.K57B_ESIK['sonraki'][d]}." not in metin:
            hata.append(f"10) {d} tanımı K57B_ON_KAYIT ile aynen değil")
    # üzerine yazmama, bozuk mühür, değişen kaynak, çıktıdan sonra ön kayıt
    with tempfile.TemporaryDirectory() as td:
        for y in [os.path.join(C, K.K57_DOSYA["onkayit"]), os.path.join(C, K.K57B_DOSYA["onkayit"])] + \
                 [os.path.join(C, K.K57B_DOSYA[a]) for a in K.K57C_ESIK["kaynak"]]:
            shutil.copy(y, td)
        open(os.path.join(td, K.K57C_DOSYA["hucre"]), "w").write("x")
        try:
            K.k57c_onkayit(td); hata.append("10) çıktı varken K57-C ön kaydı yazıldı")
        except K.K57Hata:
            pass
        os.remove(os.path.join(td, K.K57C_DOSYA["hucre"]))
        y = K.k57c_onkayit(td); ilk = open(y, encoding="utf-8").read(); K.k57c_onkayit(td)
        if open(y, encoding="utf-8").read() != ilk:
            hata.append("10) K57-C ön kaydı üzerine yazıldı")
        K.k57c_onkayit_dogrula(td)
        with open(os.path.join(td, K.K57B_DOSYA["hucre"]), "a") as f:
            f.write("\n")
        try:
            K.k57c_onkayit_dogrula(td); hata.append("10) değişen K57-B kaynak dosyası kabul edildi")
        except K.K57Hata:
            pass
        open(y, "w", encoding="utf-8").write(ilk.replace(K.k57c_esik_sha(), "0" * 64))
        try:
            K.k57c_onkayit_dogrula(td, kaynak=False); hata.append("10) K57-C bozuk mühür kabul edildi")
        except K.K57Hata:
            pass
    yol = {a: os.path.join(C, K.K57C_DOSYA[a]) for a in K.K57C_DOSYA}
    eksik = [K.K57C_DOSYA[a] for a, y in yol.items() if not os.path.exists(y)]
    if eksik:
        return hata + [f"10) K57-C çıktısı yok: {eksik} (önce `python K57.py c_kos`)"]
    meta = json.load(open(yol["meta"], encoding="utf-8"))
    if muhur > pd.Timestamp(meta["kos_baslangic"].replace(" UTC", "")):
        hata.append(f"10) K57-C ön kaydı koşudan sonra: {oc['zaman_utc']} > {meta['kos_baslangic']}")
    for a in ("hucre", "meta", "rapor", "olay"):
        if pd.Timestamp(os.path.getmtime(yol[a]), unit="s") < muhur:
            hata.append(f"10) çıktı ön kayıttan eski: {K.K57C_DOSYA[a]}")
    mc = meta["onkayit_c"]
    if mc["sha"] != K.k57c_esik_sha() or meta["k57_muhur"] != ok["sha"] or meta["k57b_muhur"] != okb["sha"]:
        hata.append("10) koşunun mühürleri bugünkü eşiklerle aynı değil")
    if mc["dosya_sha256"] != oc["dosya_sha256"]:
        hata.append("10) K57-C ön kayıt dosyası koşudan sonra değişmiş")
    if any(meta.get("yeni_istek", {}).values()):
        hata.append("10) K57-C yeni SEC / Yahoo isteği yapmış")
    de = meta.get("denetim", {})
    if not (de.get("evren", {}).get("evren_b1_ile_ayni") and de.get("b1_v1_olay", {}).get("esit") and de.get("b1_hucre")
            and all(r["esit"] for r in de["b1_hucre"])):
        hata.append("10) B1 yeniden üretimi (evren / V1 olayları / hücreler) tutmadı ya da yapılmadı")
    # hücreler ve karar
    Z = pd.read_csv(yol["hucre"]); O = K._k57_olcut(); Cx = K.K57C_ESIK["deney"]
    if set(Z.deney) != set(Cx) or len(Z) != 9 or set(Z.pazar) != {"ABD"} or set(Z.ufuk) != {60}:
        hata.append(f"10) hucre_c.csv yapısı yanlış: {sorted(set(Z.deney))} {len(Z)} {set(Z.pazar)} {set(Z.ufuk)}")
    for d, s in Cx.items():
        g = Z[Z.deney == d]
        if not len(g) or float(g.taban_usd.iloc[0]) != s["taban_usd"] or float(g.f7_dilim.iloc[0]) != s["f7_dilim"]:
            hata.append(f"10) {d} taban / dilim ön kayıttan farklı")
    if set(Z[Z.rol == "KARAR"].apply(lambda r: (r.pazar, r.donem), axis=1)) != {("ABD", "2023"), ("ABD", "2024-26")}:
        hata.append("10) karar hücreleri ABD 2023 + ABD 2024-26 değil")
    for r in Z.itertuples():
        b = bool(r.n >= O["n_esik"] and r.alt95 > 0 and r.sira > 0.5 and r.portfoy > r.portfoy_esli_p90) if r.n and r.n > 0 else False
        if b != bool(r.tutar):
            hata.append(f"10) tutar hesabı yanlış: {r.deney} {r.donem}"); break
    for d, g in Z.groupby("deney"):
        iki = all(bool(g[g.donem == x].tutar.iloc[0]) for x in ("2023", "2024-26"))
        if iki != g.karar.iloc[0].startswith("ABD-ADAY") or (not iki and g.karar.iloc[0] != "İZ DEĞİL"):
            hata.append(f"10) {d} kararı hücrelerle uyuşmuyor: {g.karar.iloc[0]}")
    # olaylar: geleceğe bakma yok, maskeler
    X = pd.read_csv(yol["olay"], parse_dates=["D", "d0", "tepki_son", "giris", "bilgi_son", "pay_filed"], low_memory=False)
    E = K.K57_ESIK
    for c in ("F1", "F2", "F3", "F4", "F7", "V1", "F7_C1", "F7_C2", "F7_C3", "C1", "C2", "C3"):
        X[c] = K._k57b_bayrak(X[c])
    if not ((X.d0 < X.D) & (X.tepki_son >= X.D) & (X.giris > X.tepki_son)).all():
        hata.append("10) d0 < D <= tepki günü < giriş sırası bozuk")
    if (X.bilgi_son.notna() & (X.bilgi_son > X.D)).any() or ((X.F1 | X.F2 | X.F3) & X.bilgi_son.isna()).any():
        hata.append("10) açıklama gününden sonra bilinen (ya da bilgi tarihi olmayan) temel değer kullanıldı")
    if (X.pay_filed.notna() & (X.pay_filed > X.D)).any() or (X.pay_yil.notna() & X.pay_filed.isna()).any():
        hata.append("10) F4: açıklama gününden sonra başvurulmuş pay bildirimi kullanıldı")
    sinir = (X.pay_yil - E["F4_pay_yil"]).abs() < 1e-9          # CSV yuvarlaması: tam eşikteki değer (0,1000000001 -> 0,1) karşılaştırılmaz
    if not (K.k57_f4(X.pay_yil).to_numpy(bool) == X.F4.to_numpy(bool))[~sinir.to_numpy()].all():
        hata.append("10) F4 pay değişiminden yeniden üretilemedi")
    if X.likit20.isna().any() or (X.likit20 < Cx["C1"]["taban_usd"]).any() or (X.C2 & (X.likit20 < Cx["C2"]["taban_usd"])).any() \
            or X.loc[X.likit20 < Cx["C2"]["taban_usd"], "f7_esik_C2"].notna().any():
        hata.append("10) likidite tabanı altında olay / C2 eşiğine 5 milyon $ altı olay girmiş")
    kriz = pd.Timestamp(K.FI.FI_OLCUT["kriz"])
    if (X.fark.notna() & (X.giris > kriz)).any():
        hata.append("10) kriz sonrası giriş ölçülmüş")
    for d in ("C1", "C2", "C3"):
        S = X[X.likit20 >= Cx[d]["taban_usd"]]; Y = S[S.tepki_son <= S.tepki_son.quantile(0.5)]
        e = K.k57_kayan_esik(Y.tepki_son, Y.ear, 1 - Cx[d]["f7_dilim"], E["F7_pencere_gun"], E["F7_min_n"])
        if not np.allclose(e, Y[f"f7_esik_{d}"].to_numpy(float), equal_nan=True):
            hata.append(f"10) {d}: F7 kayan eşiği geleceği görüyor / yanlış olay kümesinden")
        f7 = (S.ear >= S[f"f7_esik_{d}"]) & (S.ham >= E["F7_ham"])
        if not (f7.to_numpy(bool) == S[f"F7_{d}"].to_numpy(bool)).all():
            hata.append(f"10) {d}: F7 eşikten yeniden üretilemedi")
        bek = S[f"F7_{d}"] & S.F1 & S.F2 & S.F3 & (S.F4 if d == "C1" else True)
        if not (bek.to_numpy(bool) == S[d].to_numpy(bool)).all() or X.loc[X.likit20 < Cx[d]["taban_usd"], d].any():
            hata.append(f"10) {d} maskesi süzgeçlerle uyuşmuyor")
    if not (X.F7_C1 == X.F7).all() or (X.C1 & ~X.V1).any() or (X.C3 & ~X.V1).any():
        hata.append("10) C1 / C3 B1 V1'in alt kümesi değil ya da C1 F7 B1 F7'den farklı")
    if not ((X.V1 == (X.F7 & X.F1 & X.F2 & X.F3)).all()):
        hata.append("10) V1 = F7 + F1 + F2 + F3 değil")
    # rapor ve Ç150 bloğu
    rap = open(yol["rapor"], encoding="utf-8").read()
    for parca in ("## KARAR:", "Düz dille", "## Hat kapanış önerisi", "Ç150", "C1 —", "C2 —", "C3 —"):
        if parca not in rap:
            hata.append(f"10) K57C raporunda '{parca}' yok")
    m = re.search(r"```\n(_ik_k\(\"Ç150\".*?)\n```", rap, re.S)
    if not m:
        hata.append("10) Ç150 bloğu yok")
    else:
        try:
            agac = ast.parse(m.group(1))
            dz = [n.value for n in ast.walk(agac) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
            if any('"' in v or "\\" in v for v in dz):
                hata.append("10) Ç150 dize değerlerinde çift tırnak / ters bölü var")
            if "\\" in m.group(1):
                hata.append("10) Ç150 bloğunda ters bölü var")
        except SyntaxError as ex:
            hata.append(f"10) Ç150 bloğu Python olarak ayrışmıyor: {ex}")
    H = K.k57c_abd_karar_hucreleri()
    satir = len(re.findall(r"^\| K57(-B|-C)? \| ", rap, re.M))
    if satir != len(H) or len(H) != 36 + 6 + 6:
        hata.append(f"10) hat kapanış tablosu eksik: {satir} satır, {len(H)} hücre (beklenen 48)")
    # e-posta yok
    for y in [os.path.join(KOK, "K57.py"), os.path.join(KOK, "test_k57.py")] + [yol[a] for a in ("onkayit", "rapor", "meta", "hucre")]:
        if re.search(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b", open(y, encoding="utf-8").read()):
            hata.append(f"10) e-posta var: {os.path.basename(y)}")
    return hata


if __name__ == "__main__":
    H = testler()
    if H:
        print("K57 TEST: HATA", len(H)); print("\n".join(H)); sys.exit(1)
    print("K57 TEST: 10/10 bölüm GEÇTİ (K57 + K57-B + K57-C)")
