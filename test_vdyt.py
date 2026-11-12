"""VDYT testleri — YALNIZ SENTETİK veri (gerçek veriye dokunmaz; ağ yok). Çalıştırma: python test_vdyt.py

1) sıkışma tanımları elle (T1 ATR oranı, T2 RV yüzdeliği, T3 BB genişliği yüzdeliği, T4 dar bant, T5 bileşik)  2) bölge başlangıç / bitiş kuralı elle (GENİŞLEME,
SÖNME, SANSÜR, kopukluk, kısa kesinti, RV genişlemesi), yön Y1 / Y2, karar noktası etiketleri  3) savunma hattı elle + GELECEĞE BAKMAZ (t'den sonraki mumlar
bozulunca hat ve bütün karar noktası özellikleri değişmez)  4) olay hizalama ve bilgi tarihi (KAP saati, beklenen bilanço, bilgi günü > t olay görülmez, olay
penceresi sonucu, E2 eşleme elle)  5) walk-forward: eğitim etiketi test yılına taşmaz, standartlaştırma yalnız eğitimden  6) hazard / KM / CIF elle
7) Brier, log loss, dengeli doğruluk, kesinlik / duyarlılık, küme bootstrap, BH elle  8) temel model tablosu ve geri düşme  9) mühür (eşik değişince değişir,
ön kayıt üzerine yazmaz, bozuk mühür / kod / veri reddi)  10) ret kapısı: git'e işlenmemiş / değişmiş ön kayıt, KASA kapısı  11) uçtan uca sentetik
(kapsam yalnız sayar; kos wf + kasa çıktıları; grafik)  12) makro sayfa ayrıştırıcıları  13) çakışma kapısı  14) bağımsızlık (Çöl Yolu modülü içe alınmaz),
e-posta / anahtar yok.
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
sys.path.insert(0, KOK)
import VDYT as V  # noqa: E402

E0 = V.VDYT_ESIK


def kucuk_E() -> dict:
    E = copy.deepcopy(E0); E["basari"]["bootstrap"] = 200; E["coklu"]["plasebo_bolge_tekrar"] = 1; E["model"]["min_egitim"] = 50
    return E


def durmali(fn, mesaj: str, hata: list, icerik: str = "") -> None:
    try:
        fn()
    except (V.VdytHata, RuntimeError) as ex:
        if icerik and icerik not in str(ex):
            hata.append(f"{mesaj} (yanlış neden: {ex})")
        return
    hata.append(mesaj)


def rastgele_bar(n: int, tohum: int = 1, bas: str = "2015-01-01") -> pd.DataFrame:
    rng = np.random.default_rng(tohum); c = 100 * np.exp(np.cumsum(rng.normal(0, 0.015, n))); o = c * np.exp(rng.normal(0, 0.004, n))
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.006, n))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.006, n)))
    return pd.DataFrame({"o": o, "h": h, "l": l, "c": c, "v": rng.lognormal(10, 0.4, n)}, index=pd.bdate_range(bas, periods=n))


def sentetik_pazar(nh: int = 24, bas: str = "2014-01-01", bit: str = "2025-06-30", tohum: int = 7):
    """Sıkışma (düşük oynaklık) dönemleri ve ardından patlama içeren sentetik OHLCV + olaylar (bilanço, B olayı, FOMC benzeri piyasa olayı)."""
    rng = np.random.default_rng(tohum); gun = pd.bdate_range(bas, bit); n = len(gun); S = {}; ol = []
    for j in range(nh):
        sig = np.full(n, 0.02); i = 300
        while i < n - 150:
            L = int(rng.integers(25, 110)); sig[i: i + L] = 0.005; sig[i + L: i + L + 4] = 0.05; i += L + int(rng.integers(60, 200))
        r = rng.normal(0, 1, n) * sig + rng.choice([-1, 1]) * 0.0002
        c = 50 * np.exp(np.cumsum(r)); o = np.r_[c[0], c[:-1]] * np.exp(rng.normal(0, 0.2, n) * sig)
        h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.5, n)) * sig); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.5, n)) * sig)
        s = f"S{j:02d}"; S[s] = pd.DataFrame({"o": o, "h": h, "l": l, "c": c, "v": rng.lognormal(12, 0.5, n) * (1 + j)}, index=gun)
        for k in range(150, n, 63):
            z = gun[k] + pd.Timedelta(hours=19)
            ol.append(("BIST", s, "BIST_BILANCO", "A", True, z.normalize() + pd.Timedelta(days=1), z.normalize() + pd.Timedelta(days=1), "sentetik", ""))
        for k in rng.choice(n - 10, 15, replace=False):
            ol.append(("BIST", s, "BIST_ICERIDEN_ALIM", "B", False, gun[k], gun[k], "sentetik", ""))
    for k in range(200, n, 30):
        ol.append(("BIST", "*", "MAKRO_FOMC", "C", True, gun[k], gun[k], "sentetik", ""))
    # uç durumlar: kısa geçmişli hisse, işlem durması (boşluk) + sabit fiyatlı / hacimsiz günler, sektörsüz
    if nh < 2:
        Ev = pd.DataFrame(ol, columns=V.OLAY_SUTUN); Ev["g0_tarih"] = pd.to_datetime(Ev.g0_tarih); Ev["bilgi_tarih"] = pd.to_datetime(Ev.bilgi_tarih)
        return {"S": S, "meta": {s: {"tur": "EQUITY"} for s in S}, "kaynak": "sentetik"}, Ev
    S["K1"] = S["S00"].iloc[-300:].copy() * 1.1
    k2 = S["S01"].copy(); k2 = k2.drop(k2.index[1500:1530]); k2.iloc[800:806, :4] = k2.iloc[800, 3]; k2.iloc[900:903, 4] = 0.0; S["K2"] = k2
    Ev = pd.DataFrame(ol, columns=V.OLAY_SUTUN); Ev["g0_tarih"] = pd.to_datetime(Ev.g0_tarih); Ev["bilgi_tarih"] = pd.to_datetime(Ev.bilgi_tarih)
    return {"S": S, "meta": {s: {"tur": "EQUITY"} for s in S}, "kaynak": "sentetik"}, Ev


def git(kl: str, *a: str) -> str:
    return subprocess.run(["git", "-C", kl, "-c", "user.name=vdyt", "-c", "user.email=vdyt@test.invalid"] + list(a), capture_output=True, text=True, check=True).stdout


def testler() -> list:
    hata: list = []
    # ---------------------------------------------------------------- 1) tanımlar elle
    d = rastgele_bar(420); Ol = V.vdyt_olculer(d); o, h, l, c = (d[k].to_numpy() for k in "ohlc"); t = 400
    cp = np.r_[np.nan, c[:-1]]; tr = np.array([h[0] - l[0]] + [max(h[i] - l[i], abs(h[i] - cp[i]), abs(l[i] - cp[i])) for i in range(1, len(c))])
    natr = pd.Series(tr).rolling(14).mean().to_numpy() / c
    if not np.isclose(Ol["natr_oran"][t], natr[t] / np.median(natr[t - 250: t][~np.isnan(natr[t - 250: t])])):
        hata.append("1) T1 ATR oranı elle tutmadı")
    lr = np.log(c / cp); rv = np.array([np.std(lr[i - 19: i + 1], ddof=1) if i >= 20 else np.nan for i in range(len(c))])
    gecmis = rv[t - 250: t]; ok = ~np.isnan(gecmis)
    if not np.isclose(Ol["rv_yuzde"][t], (np.sum(gecmis[ok] < rv[t]) + 0.5 * np.sum(gecmis[ok] == rv[t])) / ok.sum()):
        hata.append("1) T2 RV yüzdeliği elle tutmadı")
    bbw = np.array([4 * np.std(c[i - 19: i + 1]) / np.mean(c[i - 19: i + 1]) if i >= 19 else np.nan for i in range(len(c))])
    gb = bbw[t - 250: t]; okb = ~np.isnan(gb)
    if not np.isclose(Ol["bbw_yuzde"][t], (np.sum(gb[okb] < bbw[t]) + 0.5 * np.sum(gb[okb] == bbw[t])) / okb.sum()):
        hata.append("1) T3 BB genişliği yüzdeliği elle tutmadı")
    w = c[t - 19: t + 1]
    if not np.isclose(Ol["bant"][t], (w.max() - w.min()) / w.mean() / np.median(rv[t - 250: t][~np.isnan(rv[t - 250: t])])):
        hata.append("1) T4 dar bant elle tutmadı")
    if not np.array_equal(V.vdyt_durum(Ol, "T1", 0), np.nan_to_num(Ol["natr_oran"], nan=np.inf) <= 0.70):
        hata.append("1) T1 durum eşiği")
    t5 = sum(V.vdyt_durum(Ol, k, 0).astype(int) for k in ("T1", "T2", "T3", "T4")) >= 3
    if not np.array_equal(V.vdyt_durum(Ol, "T5", 0), t5):
        hata.append("1) T5 bileşik elle tutmadı")
    if not np.array_equal(V.vdyt_durum(Ol, "T2", 1), np.nan_to_num(Ol["rv_yuzde"], nan=np.inf) <= 0.10):
        hata.append("1) T2 alternatif eşik")

    # ---------------------------------------------------------------- 2) bölge kuralı elle
    E = E0; n = 60; kop = np.zeros(n, bool)
    dur = np.zeros(n, bool); dur[10:31] = True; trn = np.full(n, 0.01); trn[23:26] = 0.03; lr0 = np.full(n, 0.001)
    B = V.vdyt_bolgeler(dur, trn, lr0, kop, 2.0, "TR", E)
    if B.tolist() != [[10, 19, 24, V.BITIS_GEN, 22]]:
        hata.append(f"2) GENİŞLEME bölgesi elle tutmadı: {B.tolist()}")
    dur2 = np.zeros(n, bool); dur2[:15] = True; B2 = V.vdyt_bolgeler(dur2, np.full(n, 0.01), lr0, kop, 2.0, "TR", E)
    if B2.tolist() != [[0, 9, 19, V.BITIS_SONME, -1]]:
        hata.append(f"2) SÖNME elle tutmadı: {B2.tolist()}")
    dur3 = np.ones(n, bool); B3 = V.vdyt_bolgeler(dur3, np.full(n, 0.01), lr0, kop, 2.0, "TR", E)
    if B3.tolist() != [[0, 9, 59, V.BITIS_SANSUR, -1]]:
        hata.append(f"2) SANSÜR (veri sonu) elle tutmadı: {B3.tolist()}")
    dur4 = np.ones(n, bool); dur4[20:23] = False; B4 = V.vdyt_bolgeler(dur4, np.full(n, 0.01), lr0, kop, 2.0, "TR", E)
    if B4.tolist() != [[0, 9, 59, V.BITIS_SANSUR, -1]]:
        hata.append(f"2) 3 günlük kesinti bölgeyi bitirmemeli: {B4.tolist()}")
    kop5 = np.zeros(n, bool); kop5[30] = True; B5 = V.vdyt_bolgeler(dur3, np.full(n, 0.01), lr0, kop5, 2.0, "TR", E)
    if B5.tolist() != [[0, 9, 29, V.BITIS_SANSUR, -1], [30, 39, 59, V.BITIS_SANSUR, -1]]:
        hata.append(f"2) kopukluk elle tutmadı: {B5.tolist()}")
    lr6 = np.where(np.arange(n) % 2 == 0, 0.005, -0.005).astype(float); lr6[40:45] = [0.04, -0.04, 0.04, -0.04, 0.04]
    B6 = V.vdyt_bolgeler(dur3, np.full(n, 0.01), lr6, kop, 2.0, "RV", E)
    if not len(B6) or B6[0][3] != V.BITIS_GEN or B6[0][2] < 40 or B6[0][2] > 44:
        hata.append(f"2) RV genişlemesi elle tutmadı: {B6.tolist()}")
    cc = np.full(n, 100.0); cc[10:22] = np.r_[100, 101, 102, 101, 100, 101, 102, 101, 100, 101, 102, 101]; cc[22:] = 105.0
    y1, y2 = V.vdyt_yon(cc, B, E)
    if y1[0] != 1.0 or y2[0] != 1.0:
        hata.append(f"2) yön Y1 / Y2 elle tutmadı: {y1}, {y2}")
    cc2 = cc.copy(); cc2[22:] = 99.0; y1b, _ = V.vdyt_yon(cc2, B, E)
    if y1b[0] != -1.0:
        hata.append("2) aşağı yön")
    KN = V.vdyt_karar_noktalari(B, n, E)
    if KN.to_dict("records") != [{"bolge": 0, "yas": 10, "t": 19, "y5": 1.0, "y10": 1.0, "y20": 1.0}]:
        hata.append(f"2) karar noktası / etiket (GENİŞLEME) elle tutmadı: {KN.to_dict('records')}")
    KN2 = V.vdyt_karar_noktalari(B2, n, E)
    if KN2[["yas", "t", "y5", "y10", "y20"]].values.tolist() != [[10, 9, 0.0, 0.0, 0.0]]:
        hata.append(f"2) SÖNME etiketi 0 olmalı: {KN2.values.tolist()}")
    KN3 = V.vdyt_karar_noktalari(np.array([[0, 9, 59, V.BITIS_SANSUR, -1]]), n, E)
    r50 = KN3[KN3.yas == 40]
    if not (len(r50) and r50.y20.isna().all() and r50.y10.iloc[0] == 0.0):
        hata.append(f"2) SANSÜR / veri sonu etiketi: {KN3.values.tolist()}")

    # ---------------------------------------------------------------- 3) savunma hattı elle + geleceğe bakmaz
    m = 30; oo = np.full(m, 10.8); cc3 = np.full(m, 10.9)
    for i in (3, 10, 20):
        oo[i], cc3[i] = 10.0, 10.3
    for i in range(m):
        if i not in (3, 10, 20):
            oo[i], cc3[i] = (10.8, 11.0) if i % 2 else (11.0, 10.8)
    hh = np.maximum(oo, cc3) + 0.2; ll = np.minimum(oo, cc3) - 0.1; vv = np.full(m, 100.0); vv[[3, 10, 20]] = 200.0
    trr = hh - ll; at = np.full(m, float(np.mean(trr)))
    sv = V.vdyt_savunma(oo, hh, ll, cc3, vv, trr, at, 0, 25, "govde", E)
    if not (sv["hat_var"] == 1 and sv["temas"] == 3 and np.isclose(sv["seviye"], 10.0) and sv["korunma"] == 22 and sv["son_test"] == 5 and sv["kirilma"] == 0
            and np.isclose(sv["hacim_test"], 2.0)):
        hata.append(f"3) savunma hattı elle tutmadı: {sv}")
    oo2, hh2, ll2, cc4 = oo.copy(), hh.copy(), ll.copy(), cc3.copy(); oo2[26:] = 1.0; cc4[26:] = 1.0; ll2[26:] = 0.5; hh2[26:] = 50.0
    sv2 = V.vdyt_savunma(oo2, hh2, ll2, cc4, vv, np.maximum(hh2 - ll2, 0), at, 0, 25, "govde", E)
    if json.dumps(sv, sort_keys=True) != json.dumps(sv2, sort_keys=True):
        hata.append("3) savunma hattı t'den sonraki mumlarla değişti (geleceğe bakıyor)")
    # karar noktası özellikleri: t0'dan sonraki barlar bozulunca t <= t0 satırlarının bütün özellikleri aynı
    Fs, Evs = sentetik_pazar(nh=1, tohum=11); d0 = Fs["S"]["S00"]; Ol0 = V.vdyt_olculer(d0)
    T0 = pd.DataFrame(V.vdyt_bolgeler(V.vdyt_durum(Ol0, "T1"), Ol0["trn"], Ol0["lr"], V.vdyt_kopuk(d0.index), 2.0, "TR", E), columns=["bas", "tespit", "bit", "bit_tur", "gen_bas"])
    T0["uygun"] = True
    kn0 = V.vdyt_karar_noktalari(T0[["bas", "tespit", "bit", "bit_tur", "gen_bas"]].to_numpy(), len(d0), E)
    t0 = int(kn0.t.iloc[len(kn0) // 2]); d1 = d0.copy(); d1.iloc[t0 + 1:] = d1.iloc[t0 + 1:] * 3.0
    ctx = {"rj_pazar": np.zeros(len(d0)), "p_pazar_ret60": np.zeros(len(d0)), "p_lr": np.zeros(len(d0)), "rj_sektor": np.zeros(len(d0)),
           "p_sektor_ret20": np.zeros(len(d0)), "mom_t": np.zeros(len(d0)), "liq_t": np.zeros(len(d0)), "natr_d": np.zeros(len(d0)), "sektor": None,
           "bilanco_tarih": np.array([], "datetime64[D]"), "bilanco_bilgi_i": np.array([], int), "B_bilgi_i": np.array([t0 - 2, t0 + 1]),
           "B_g0_i": np.array([t0 - 2, t0 + 1]), "makro_g0_i": np.array([t0 + 5]), "gun": d0.index.to_numpy("datetime64[D]")}
    D0 = V.vdyt_hisse_karar("S00", d0, Ol0, T0, ctx, "BIST", E); D1 = V.vdyt_hisse_karar("S00", d1, V.vdyt_olculer(d1), T0, ctx, "BIST", E)
    oz = [c_ for g in V.VDYT_OZELLIK.values() for c_ in g] + ["svf_hat_var", "svk_kirilma", "sv_seviye"]
    a0, a1 = D0[D0.t <= t0][oz], D1[D1.t <= t0][oz]
    if not len(a0) or not np.allclose(a0.to_numpy(float), a1.to_numpy(float), equal_nan=True):
        hata.append("3) karar noktası özellikleri t'den sonraki mumlarla değişti (geleceğe bakma)")
    bi_ = ctx["B_bilgi_i"]
    for r_ in D0[D0.t <= t0].itertuples():
        if r_.o_olay_son5 != float(np.sum((bi_ > r_.t - 5) & (bi_ <= r_.t))) or r_.o_makro_10 != float(np.any((ctx["makro_g0_i"] > r_.t) & (ctx["makro_g0_i"] <= r_.t + 10))):
            hata.append(f"3) olay özelliği bilgi günü kuralı (t = {r_.t})"); break
    rt = D0[D0.t == t0]
    if not len(rt) or rt.o_olay_son5.iloc[0] != 1.0 or rt.o_makro_10.iloc[0] != 1.0:
        hata.append("3) karar günündeki satır: bilgi günü t+1 olan olay sayılmamalı, t-2 olan sayılmalı; planlı makro t+5 görülmeli")
    # ---------------------------------------------------------------- 4) olay hizalama, bilgi tarihi
    g0, bi = V._vdyt_kap_g0(pd.Series(pd.to_datetime(["2023-03-01 17:59:59", "2023-03-01 18:00:00", "2023-03-04 10:00:00"])), E)
    if [str(x.date()) for x in g0] != ["2023-03-01", "2023-03-02", "2023-03-04"]:
        hata.append(f"4) KAP saat kuralı: {list(g0)}")
    ix = pd.bdate_range("2023-03-01", periods=10)
    if V.vdyt_olay_hizala(ix, g0).tolist() != [0, 1, 3]:
        hata.append(f"4) hizalama (tatil -> sonraki işlem günü): {V.vdyt_olay_hizala(ix, g0).tolist()}")
    if V.vdyt_olay_hizala(ix, pd.Series(pd.to_datetime(["2030-01-01"]))).tolist() != [-1]:
        hata.append("4) veri dışı olay -1 olmalı")
    gc = np.array(["2022-03-01", "2022-06-01", "2022-09-01", "2022-12-01"], "datetime64[D]")
    bg, bs = V.vdyt_beklenen_bilanco(gc, np.datetime64("2022-10-01"))
    if (bg, bs) != (61.0, 30.0):
        hata.append(f"4) beklenen bilanço (gelecek rapor görülmemeli): {(bg, bs)}")
    bg2, _ = V.vdyt_beklenen_bilanco(np.array(["2021-12-01", "2022-03-01", "2022-06-01", "2022-09-01"], "datetime64[D]"), np.datetime64("2022-11-20"))
    if bg2 != 11.0:
        hata.append(f"4) yıldönümü adayı: {bg2}")
    Bx = np.array([[0, 9, 30, V.BITIS_GEN], [0, 9, 30, V.BITIS_SANSUR], [0, 9, 50, V.BITIS_GEN], [0, 9, 50, V.BITIS_SONME]]); Pw = E["olay"]["pencere_e2"]
    sx = [V.vdyt_olay_sonuc(Bx, 0, 25, 60, Pw), V.vdyt_olay_sonuc(Bx, 0, 30, 60, Pw), V.vdyt_olay_sonuc(Bx, 0, 15, 60, Pw), V.vdyt_olay_sonuc(Bx, 2, 25, 60, Pw),
          V.vdyt_olay_sonuc(Bx, 3, 25, 60, Pw)]
    if sx != [1, 0, 3, 4, 4]:
        hata.append(f"4) olay penceresi sonucu: {sx}")
    if V.vdyt_olay_sonuc(Bx, 1, 25, 60, Pw) != -1 or V.vdyt_olay_sonuc(Bx, 0, 50, 60, Pw) != -1:
        hata.append("4) sansür / veri sonu ölçülmemeli")
    gunH = pd.bdate_range("2020-01-01", periods=120)

    def hav(bit: int, olay: list, s: str) -> dict:
        ac = np.full(120, -1, np.int32); ac[9:bit] = 0
        return {"sembol": s, "havuz": {"T1": {"acik": ac, "B": np.array([[0, 9, bit, V.BITIS_GEN]])},
                                       "_ortak": {"ym": np.full(120, 202001, np.int32), "yil": np.full(120, 2020, np.int32), "mom": np.zeros(120, np.int8),
                                                  "liq": np.zeros(120, np.int8), "ti": {"X": np.array(olay, np.int64)}, "gun": gunH}}}
    H = [hav(40, [40], "A"), hav(40, [40], "B"), hav(90, [], "C"), hav(95, [], "D")]
    r = V.vdyt_olay_analizi(H, "T1", "X", "e2", E)
    tb = {x["pencere"]: x for x in r.get("tablo", [])}
    if not (r.get("olay_kullanilan") == 2 and np.isclose(tb["[0,0]"]["gozlenen"], 1.0) and np.isclose(tb["[0,0]"]["beklenen"], 0.0)
            and np.isclose(tb["yok"]["beklenen"], 1.0)):
        hata.append(f"4) E2 eşleme elle tutmadı: {r}")

    # ---------------------------------------------------------------- 5) walk-forward
    rng = np.random.default_rng(5); tar = pd.to_datetime(rng.choice(pd.bdate_range("2015-01-01", "2020-12-31"), 3000))
    Dw = pd.DataFrame({"tarih": tar, "son10": tar + pd.Timedelta(days=14), "x1": rng.normal(size=3000), "ay": tar.month, "yas_kova": rng.integers(0, 3, 3000)})
    Dw["y10"] = (rng.random(3000) < 1 / (1 + np.exp(-Dw.x1))).astype(float); Dw["sembol"] = rng.choice(list("ABCDEFGH"), 3000)
    P, kay = V.vdyt_wf(Dw, "y10", "son10", {"M": ["x1"]}, {"T1": ["yas_kova", "ay"]}, [2018, 2019], E, kesik="2019-12-20")
    for k_ in kay:
        if k_["durum"] == "tamam" and pd.Timestamp(k_["egitim_son_max"]) >= pd.Timestamp(f"{k_['yil']}-01-01"):
            hata.append(f"5) eğitim etiketi test yılına taştı: {k_}")
        if k_["egitim"] != int((Dw.son10 < pd.Timestamp(f"{k_['yil']}-01-01")).sum()):
            hata.append("5) eğitim satır sayısı elle tutmadı")
    if not len(P) or (Dw.loc[P.satir, "tarih"].dt.year.to_numpy() != P.yil.to_numpy()).any() or (Dw.loc[P.satir, "son10"] > pd.Timestamp("2019-12-20")).any():
        hata.append("5) test satırları yanlış yıl ya da kesik sonrası")
    Xa, Xb = V.vdyt_standart(np.array([[1.0], [2.0], [3.0]]), np.array([[5.0]]), (0.0, 1.0))
    if not (np.isclose(Xa.mean(), 0) and np.isclose(Xb[0, 0], (3.0 - 2.0) / np.std([1, 2, 3]))):
        hata.append("5) standartlaştırma eğitim dışı bilgi kullandı")
    b_ = V.vdyt_lojistik(Dw[["x1"]].to_numpy(), Dw.y10.to_numpy(), ridge=0.0)
    if not (0.7 < b_[1] < 1.3):
        hata.append(f"5) lojistik katsayısı ~1 olmalı: {b_}")

    # ---------------------------------------------------------------- 6) hazard / KM / CIF elle
    Sx = V.vdyt_sureklilik(np.array([11, 12, 12, 15]), np.array([V.BITIS_GEN, V.BITIS_SONME, V.BITIS_GEN, V.BITIS_SANSUR]))
    a11, a12, a15 = (Sx[Sx.yas == a].iloc[0] for a in (11, 12, 15))
    if not (a11.risk == 4 and np.isclose(a11.hazard, 0.25) and np.isclose(a11.cif_gen, 0.25) and a12.risk == 3 and np.isclose(a12.km_gen, 0.5)
            and np.isclose(a12.cif_gen, 0.5) and np.isclose(a12.s_hepsi, 0.25) and a15.sansur == 1 and np.isclose(a15.cif_gen, 0.5)):
        hata.append(f"6) hazard / KM / CIF elle tutmadı:\n{Sx}")

    # ---------------------------------------------------------------- 7) ölçütler, bootstrap, BH
    yy = np.array([1, 0, 1, 0.]); pp = np.array([0.8, 0.3, 0.6, 0.1])
    if not np.isclose(V.vdyt_brier(yy, pp), 0.075) or not np.isclose(V.vdyt_logloss(yy, pp), -np.mean(np.log([0.8, 0.7, 0.6, 0.9]))):
        hata.append("7) Brier / log loss elle")
    if V.vdyt_dengeli_dogruluk(yy, pp) != 1.0 or V.vdyt_dengeli_dogruluk(yy, np.array([0.4, 0.6, 0.7, 0.2])) != 0.5:
        hata.append("7) dengeli doğruluk elle")
    if V.vdyt_kesinlik_duyarlilik(yy, np.array([0.4, 0.6, 0.7, 0.2]), 0.5) != (0.5, 0.5):
        hata.append("7) kesinlik / duyarlılık elle")
    ku = np.repeat(np.arange(20), 10); yb = (rng.random(200) < 0.3).astype(float); pm_ = np.clip(0.3 + 0.4 * (yb - 0.3), 0.01, 0.99); p0_ = np.full(200, 0.3)
    bs = V.vdyt_bootstrap(ku, yb, pm_, p0_, 300, 1, (2.5, 97.5), yon=True)
    if not (np.isclose(bs["brier_skill"], 1 - np.sum((pm_ - yb) ** 2) / np.sum((p0_ - yb) ** 2)) and bs["brier_skill_alt"] <= bs["brier_skill"] <= bs["brier_skill_ust"]):
        hata.append(f"7) küme bootstrap: {bs}")
    if V.vdyt_bootstrap(ku, yb, pm_, p0_, 300, 1)["brier_skill_alt"] != bs["brier_skill_alt"]:
        hata.append("7) bootstrap tohumla tekrarlanmıyor")
    zb = np.random.default_rng(3).normal(0, 1, 20000)
    if not (abs(V.vdyt_p_normal(1.96, zb) - 0.05) < 0.005 and V.vdyt_p_normal(0.0, zb) == 1.0):
        hata.append("7) normal yaklaşımlı p elle")
    if V.vdyt_bh(np.array([0.001, 0.02, 0.04, 0.5]), 0.1).tolist() != [True, True, True, False] or V.vdyt_bh(np.array([0.2, np.nan]), 0.1).any():
        hata.append("7) BH elle")
    bf = V.vdyt_bootstrap_fark(np.array(["a", "b", "c", "d"]), np.array([1, 1, 0, 0.]), np.array([1, 1, 0, 0.]), 100, 1)
    if bf["fark"] != 1.0:
        hata.append("7) grup farkı")
    wt = V.vdyt_tabakali_agirlik(np.array([1, 0, 0, 1, 0]), pd.DataFrame({"k": [1, 1, 1, 2, 3]}))
    if not np.allclose(wt, [1, 0.5, 0.5, 0, 0]):
        hata.append(f"7) tabakalı ağırlık elle: {wt}")

    # ---------------------------------------------------------------- 8) temel tablo
    Dtr = pd.DataFrame({"yas_kova": [0] * 30 + [1] * 5, "ay": [1] * 30 + [1] * 5, "y": [1] * 15 + [0] * 15 + [1] * 5})
    Dte = pd.DataFrame({"yas_kova": [0, 1, 2], "ay": [1, 1, 1]})
    pt = V.vdyt_temel_tablo(Dtr, Dte, ["yas_kova", "ay"], "y", 20)
    if not np.allclose(pt, [0.5, 20 / 35, 20 / 35]):
        hata.append(f"8) temel tablo geri düşme: {pt}")

    # ---------------------------------------------------------------- 9) mühür ve ön kayıt
    E2 = copy.deepcopy(E0); E2["genisleme"]["ana_k"] = 2.1
    if V.vdyt_esik_sha(E2) == V.vdyt_esik_sha() or V.vdyt_esik_sha(copy.deepcopy(E0)) != V.vdyt_esik_sha():
        hata.append("9) eşik mührü değişikliğe duyarsız")
    with tempfile.TemporaryDirectory() as td:
        durmali(lambda: V.vdyt_onkayit_dogrula(td, veri=False, git=False), "9) ön kayıt yokken doğrulama geçti", hata, "ön kayıt yok")
        y = V.vdyt_onkayit(td, kapsam={}, veri_sha={"x": ("a" * 64, 1)})
        if V.vdyt_onkayit(td, kapsam={}) != y:
            hata.append("9) aynı mühürle ikinci yazım yolu döndürmeli")
        if V.vdyt_onkayit_dogrula(td, veri=False, git=False)["esik"] != V.vdyt_esik_sha():
            hata.append("9) doğrulama mührü")
        durmali(lambda: V.vdyt_onkayit_dogrula(td, veri=True, git=False), "9) farklı veri sha256 ile doğrulama geçti", hata, "veri")
        m_ = open(y, encoding="utf-8").read()
        open(y, "w", encoding="utf-8").write(m_.replace(V.vdyt_kod_sha(), "0" * 64))
        durmali(lambda: V.vdyt_onkayit_dogrula(td, veri=False, git=False), "9) farklı kod sha256 ile doğrulama geçti", hata, "VDYT.py")
        open(y, "w", encoding="utf-8").write(m_.replace(V.vdyt_esik_sha(), "1" * 64))
        durmali(lambda: V.vdyt_onkayit_dogrula(td, veri=False, git=False), "9) bozuk mühürle doğrulama geçti", hata, "mühr")
        durmali(lambda: V.vdyt_onkayit(td), "9) farklı mühürlü ön kaydın üzerine yazıldı", hata)
        if "SAPMA" not in m_ or "Tablo şemaları" not in m_ or "BAŞARI ÖLÇÜTÜ" not in m_ or "walk-forward" not in m_.lower():
            hata.append("9) ön kayıt metninde zorunlu bölüm eksik")

    # ---------------------------------------------------------------- 10) ret kapısı (git) ve KASA kapısı
    with tempfile.TemporaryDirectory() as td:
        git(td, "init", "-q"); y = V.vdyt_onkayit(td, kapsam={}, veri_sha={})
        durmali(lambda: V.vdyt_onkayit_dogrula(td, veri=False, git=True), "10) git'e işlenmemiş ön kayıt kabul edildi", hata, "ön kaydı")
        durmali(lambda: V.vdyt_kos("wf", td, 1, git_sart=True, veri_sart=False, pazarlar=[]), "10) işlenmemiş ön kayıtla kos çalıştı", hata, "REDDEDİLDİ")
        git(td, "add", V.VDYT_DOSYA["onkayit"]); git(td, "commit", "-q", "-m", "on kayit")
        if V.vdyt_git_islenmis(y, "ön kayıt")["commit"] != git(td, "rev-parse", "HEAD").strip():
            hata.append("10) git commit kimliği")
        kod_temiz = subprocess.run(["git", "-C", KOK, "status", "--porcelain", "--", "VDYT.py"], capture_output=True, text=True).stdout.strip() == "" and \
            subprocess.run(["git", "-C", KOK, "log", "-1", "--", "VDYT.py"], capture_output=True, text=True).stdout.strip() != ""
        if kod_temiz:
            V.vdyt_onkayit_dogrula(td, veri=False, git=True)
        else:
            durmali(lambda: V.vdyt_onkayit_dogrula(td, veri=False, git=True), "10) git'e işlenmemiş VDYT.py ile doğrulama geçti", hata, "VDYT.py")
        open(y, "a", encoding="utf-8").write("\nsonradan eklenen satır\n")
        durmali(lambda: V.vdyt_git_islenmis(y, "ön kayıt"), "10) işlendikten sonra değişen ön kayıt kabul edildi", hata, "değişmiş")
    with tempfile.TemporaryDirectory() as td:
        V.vdyt_onkayit(td, kapsam={}, veri_sha={})
        durmali(lambda: V.vdyt_kos("kasa", td, 1, git_sart=False, veri_sart=False, pazarlar=[]), "10) wf olmadan KASA açıldı", hata, "KASA")
        V._vdyt_json(V._vdyt_yol("vdyt_sonuc_wf.json", td), {"pazar": {}}); V._vdyt_json(V._vdyt_yol("kasa", td), {"acilis": "önce"})
        durmali(lambda: V.vdyt_kos("kasa", td, 1, git_sart=False, veri_sart=False, pazarlar=[]), "10) KASA ikinci kez açıldı", hata, "zaten")

    # ---------------------------------------------------------------- 11) uçtan uca sentetik
    yedek = dict(V.VDYT_YOL)
    with tempfile.TemporaryDirectory() as td:
        try:
            for k_ in V.VDYT_YOL:
                if k_ not in ("cikti",):
                    V.VDYT_YOL[k_] = os.path.join(td, "yok_" + k_)
            V.VDYT_YOL["ara"] = os.path.join(td, "ara"); V.VDYT_YOL["sektor_bist"] = os.path.join(td, "sektor.csv")
            pd.DataFrame({"sembol": [f"S{j:02d}" for j in range(24)], "sektor": ["A"] * 12 + ["B"] * 12}).to_csv(V.VDYT_YOL["sektor_bist"], index=False)
            Fs, Evs = sentetik_pazar(); Es = kucuk_E(); cik = os.path.join(td, "cikti")
            K = V.vdyt_kapsam(["BIST"], cik, 1, Es, girdi={"BIST": (Fs, Evs)})
            js = json.dumps(K, ensure_ascii=False)
            o_ = K["pazar"]["BIST"]
            if o_["bolge"]["T1"]["bolge_uygun"] <= 0 or o_["karar"]["T1"]["toplam"] <= 0:
                hata.append("11) kapsam sıkışma bölgesi / karar noktası saymadı")
            if any(x in js for x in ("GENISLEME", "\"y10\"", "\"r20\"", "yukari", "brier", "Y1")):
                hata.append("11) kapsam etiket / getiri / başarı bilgisi içeriyor")
            V.vdyt_onkayit(cik, veri_sha={})
            S = V.vdyt_kos("wf", cik, 1, git_sart=False, veri_sart=False, pazarlar=["BIST"], girdi={"BIST": (Fs, Evs)}, p1_tekrar=1, E=Es)
            P = S["pazar"]["BIST"]
            hm = V._vdyt_json_oku(V._vdyt_yol("meta", cik))["hata"]["BIST"]["hisse_hata"]
            if hm:
                hata.append(f"11) uç durum hisselerinde hata: {hm}")
            if "durum" in P or not P.get("motor1") or not P.get("motor2") or not P.get("hipotez") or not P.get("sure"):
                hata.append(f"11) kos wf çıktısı eksik: {list(P)[:12]}")
            if not any(r.get("kombo") == "T1" and r.get("model") == "M_TAM" and r.get("temel") == "T1" and r.get("n", 0) > 0 for r in P.get("motor1", [])):
                hata.append("11) Motor 1 ana hücre ölçülmedi")
            if S["karar"][0]["karar"] != "KASA AÇILMADI":
                hata.append("11) wf aşamasında karar 'KASA AÇILMADI' olmalı")
            for f in ("bolge_BIST_T1.csv.gz", "tahmin_m1_BIST_T1_y10.csv.gz", "olay_eslesme_BIST_T1.csv.gz", "karar_BIST_T1.csv.gz"):
                if not os.path.exists(os.path.join(V.VDYT_YOL["ara"], "wf", f)):
                    hata.append(f"11) {f} yazılmadı")
            Pm = pd.read_csv(os.path.join(V.VDYT_YOL["ara"], "wf", "tahmin_m1_BIST_T1_y10.csv.gz"), parse_dates=["tarih"])
            if (Pm.tarih >= pd.Timestamp("2024-01-01")).any():
                hata.append("11) wf aşamasında KASA dönemi test satırı var")
            for f in ("rapor", "parametre", "hata", "meta"):
                if not os.path.exists(V._vdyt_yol(f, cik)):
                    hata.append(f"11) {V.VDYT_DOSYA[f]} yazılmadı")
            S2 = V.vdyt_kos("kasa", cik, 1, git_sart=False, veri_sart=False, pazarlar=["BIST"], girdi={"BIST": (Fs, Evs)}, E=Es)
            if S2["karar"][0]["karar"] in ("KASA AÇILMADI",) or not os.path.exists(V._vdyt_yol("kasa", cik)):
                hata.append(f"11) KASA aşaması: {S2['karar'][0]}")
            Pk = pd.read_csv(os.path.join(V.VDYT_YOL["ara"], "kasa", "tahmin_m1_BIST_T1_y10.csv.gz"), parse_dates=["tarih"])
            if (Pk.tarih < pd.Timestamp("2024-01-01")).any():
                hata.append("11) KASA aşamasında 2024 öncesi test satırı var")
            try:
                import matplotlib  # noqa: F401
                g_ = V.vdyt_grafik("wf", cik, ["BIST"], Es, F_ver={"BIST": Fs})
                if not g_ or not all(os.path.exists(x) for x in g_) or not any(x.endswith("_sinyal.png") for x in g_):
                    hata.append("11) grafik yazılmadı")
            except ImportError:
                print("not: matplotlib yok, grafik testi atlandı")
        finally:
            V.VDYT_YOL.clear(); V.VDYT_YOL.update(yedek)

    # ---------------------------------------------------------------- 12) makro sayfa ayrıştırıcıları
    fomc = ('<h4><a id="1">2024 FOMC Meetings</a></h4><div class="fomc-meeting__month col-xs-5"><strong>January</strong></div>'
            '<div class="fomc-meeting__date col-xs-4">30-31</div><div class="fomc-meeting__month"><strong>March</strong></div>'
            '<div class="fomc-meeting__date">19-20*</div><div class="fomc-meeting__month"><strong>August</strong></div>'
            '<div class="fomc-meeting__date">22 (notation vote)</div><div class="fomc-meeting__month"><strong>Oct/Nov</strong></div>'
            '<div class="fomc-meeting__date">31-1</div><div class="fomc-meeting__month"><strong>December</strong></div>'
            '<div class="fomc-meeting__date">3 (unscheduled)</div>')
    if V.vdyt_fomc_ayristir(fomc) != [("2024-01-31", True), ("2024-03-20", True), ("2024-11-01", True), ("2024-12-03", False)]:
        hata.append(f"12) FOMC ayrıştırma: {V.vdyt_fomc_ayristir(fomc)}")
    if V.vdyt_fomc_ayristir('<h5 class="x">April/May 30-1 Meeting - 2019</h5><h5>March 15 (unscheduled) Meeting - 2020</h5>'
                            '<h5>March 17-18 (cancelled) Meeting - 2020</h5><h5>March 19 (notation vote) - 2020</h5>') != [
            ("2019-05-01", True), ("2020-03-15", False), ("2020-03-18", False)]:
        hata.append(f"12) FOMC tarihî sayfa: {V.vdyt_fomc_ayristir('<h5>April/May 30-1 Meeting - 2019</h5>')}")
    ppk = '<tr><td style="x"><a href="/a">16 Ocak 2019</a></td><td><a>23 Ocak 2019</a></td></tr><tr><td><a>25 Nisan 2019 </a></td><td>30 Nisan 2019</td></tr>'
    if V.vdyt_ppk_ayristir(ppk) != ["2019-01-16", "2019-04-25"]:
        hata.append(f"12) PPK ayrıştırma: {V.vdyt_ppk_ayristir(ppk)}")

    # ---------------------------------------------------------------- 13) çakışma kapısı
    kaynak = open(os.path.join(KOK, "VDYT.py"), encoding="utf-8").read()
    ns = {"__name__": "vdyt_test", "vdyt_bh": "başka dosyanın adı", "_CK_KAYIT": {"vdyt_bh": "BASKA.py"}}
    try:
        exec(compile(kaynak, "VDYT.py", "exec"), ns); hata.append("13) başka dosyanın adını ezen yükleme durmadı")
    except RuntimeError as ex:
        if "EZDİ" not in str(ex):
            hata.append(f"13) çakışma kapısı yanlış nedenle durdu: {ex}")
    ns2 = {"__name__": "vdyt_test"}
    exec(compile(kaynak, "VDYT.py", "exec"), ns2); exec(compile(kaynak, "VDYT.py", "exec"), ns2)

    # ---------------------------------------------------------------- 14) bağımsızlık, e-posta / anahtar
    if re.search(r"^\s*(import|from)\s+(FON_IZI|K5\d|K6\d|COL_\w+|IZ_KARNE|BASLAT|takip)\b", kaynak, re.M):
        hata.append("14) VDYT Çöl Yolu / K modüllerinden içe alıyor")
    for ad in ("VDYT.py", "test_vdyt.py"):
        mt = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if V._VDYT_EPOSTA.search(mt) or re.search(r"(api[_-]?key|token|password|sifre)\s*=\s*['\"][A-Za-z0-9]{8,}", mt, re.I):
            hata.append(f"14) {ad} içinde e-posta / anahtar biçimli parça var")
    return hata


if __name__ == "__main__":
    h = testler()
    for x in h:
        print("HATA:", x)
    print("test_vdyt:", "TAMAM (14/14)" if not h else f"{len(h)} HATA")
    sys.exit(1 if h else 0)
