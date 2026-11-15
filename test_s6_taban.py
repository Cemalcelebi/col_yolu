"""S6_TABAN testleri (sentetik veri + gerçek veride Pine aynası / önek değişmezliği; getiri ÖLÇMEZ). Çalıştırma: python test_s6_taban.py

1) çakışma kapısı  2) sakin taban bulunur (DİP sınıfı, uzunluk nMin..nMax)  3) eğimli pencere -> taban yok  4) kayan düşüş kanalı -> (3) dip
şartı eler (net ve bant gevşekken)  5) tek mum sıçrama (kapanış içeride) bölgeyi bitirmez, AL yok  6) kapanışla tavanı kıran mum -> AL, bölge
o barda biter  7) taban kırılımı -> KIRILDI  8) nMin / nMax sınırları  9) ÖNEK DEĞİŞMEZLİĞİ (sentetik + gerçek; al / kirildi / bolge_id dahil)
ve t sonrası bozma  10) beş şart elle (ham OHLC'den, bir barda)  11) Pine aynası (döngü) = vektörel (sentetik + gerçek, daralma açık / kapalı)
12) parametre denetimi  13) tasarım json'u: seçilen = S6_PRM, puan  14) Pine dosyası: girdiler = S6_PRM, ASCII kopya, yasak kalıplar
15) e-posta / anahtar yok.
"""
from __future__ import annotations

import json
import os
import re
import sys

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
os.chdir(KOK); sys.path.insert(0, KOK)
import S6_TABAN as S  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402

SONUC = []
VERI = os.environ.get("S6_VERI", "/tmp/veri")
CIKTI = os.path.join(KOK, "arastirma_cikti", "sikisma_s6")
KOLON = ["n", "bas_i", "tavan", "dip", "tavan_i", "al", "kirildi", "bolge_id", "durum", "kutu_sol_i", "kutu_sag_i", "kutu_ust", "kutu_alt", "sinif"]


def kontrol(ad, kosul, ek=""):
    SONUC.append((ad, bool(kosul)))
    print(("TAMAM " if kosul else "HATA  ") + ad + (f"  [{ek}]" if ek != "" else ""))


def _seri(segler, tohum=1, bas="2016-01-04"):
    """segler: [(gün, günlük kayma, getiri oynaklığı, mum yarı genişliği)]."""
    rng = np.random.default_rng(tohum)
    r, w = [], []
    for g, k, s, m in segler:
        r += list(k + rng.normal(0, s, g)); w += list(np.abs(rng.normal(m, m * 0.2, g)))
    r = np.array(r); w = np.array(w); n = len(r)
    C = 100 * np.exp(np.cumsum(r))
    O = np.r_[C[0], C[:-1]]
    H = np.fmax(C, O) * (1 + w); L = np.fmin(C, O) * (1 - w)
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1e5, 2e5, n).astype(float)},
                        index=pd.bdate_range(bas, periods=n))


ARKA = (400, 0.0, 0.015, 0.015)
DUS = (60, -0.008, 0.004, 0.012)
BAZ = (45, 0.0, 0.001, 0.003)


def _hz(d):
    return SY.sy_veri_hazirla(d, SY.SY_ESIK)


def _ayni(A, B, kol, ad):
    fark = []
    for c in kol:
        a, b = A[c].to_numpy(), B[c].to_numpy()
        if a.dtype.kind in "fc" or b.dtype.kind in "fc":
            a = a.astype(float); b = b.astype(float)
            esit = (np.isclose(a, b, rtol=1e-12, atol=0) | (np.isnan(a) & np.isnan(b)))
        else:
            esit = a == b
        if not esit.all():
            fark.append((c, int((~esit).sum()), int(np.where(~esit)[0][0])))
    kontrol(ad, not fark, str(fark[:4]))


def main():
    # 1) çakışma kapısı
    g = {"s6_taban": lambda: None, "__name__": "x"}
    try:
        exec(compile(open(os.path.join(KOK, "S6_TABAN.py"), encoding="utf-8").read(), "S6_TABAN.py", "exec"), g)
        kontrol("çakışma kapısı bellekteki adı ezince durur", False)
    except RuntimeError as ex:
        kontrol("çakışma kapısı bellekteki adı ezince durur", "EZDİ" in str(ex))

    # 2) sakin taban (düşüş sonrası)
    d = _hz(_seri([ARKA, DUS, BAZ, (60, 0.0, 0.015, 0.015)], 1))
    T = S.s6_taban(d); R = S.s6_bolgeler(T)
    b0, b1 = 460, 504
    ic = [r for r in R if r["sag_i"] >= b0 and r["sol_i"] <= b1]
    enr = max(ic, key=lambda r: min(b1, r["sag_i"]) - max(b0, r["sol_i"])) if ic else None
    ort = (min(b1, enr["sag_i"]) - max(b0, enr["sol_i"]) + 1) / (b1 - b0 + 1) if enr else 0
    kontrol("sakin taban: tek bölge tabanın >= %80'ini örter", ort >= 0.8, f"{ort:.2f} {enr['bas'] if enr else '-'}..{enr['bitis'] if enr else '-'}")
    kontrol("sakin taban: açılış sınıfı DİP", enr is not None and enr["sinif"] == "DIP", enr["sinif"] if enr else "-")
    nn = T["n"].dropna()
    kontrol("taban n her yerde nMin..nMax", nn.between(S.S6_PRM["nMin"], S.S6_PRM["nMax"]).all(), f"{nn.min()}..{nn.max()}")
    kontrol("bölge (kutu) uzunluğu >= nMin (tek mumluk bölge yok)", all(r["gun"] >= S.S6_PRM["nMin"] for r in R), str(min((r["gun"] for r in R), default=0)))
    kontrol("kutular üst üste binmez", S._s6_ust_uste(R) == 0)

    # 3) eğimli pencere
    de = _hz(_seri([ARKA, DUS, (45, 0.01, 0.001, 0.003), (60, 0.0, 0.015, 0.015)], 2))
    Te = S.s6_taban(de)
    icinde = (Te["n"].to_numpy() > 0) & (Te["bas_i"].to_numpy() >= 460) & (np.arange(len(Te)) <= 504)
    kontrol("eğimli (+%1/gün) küçük mumlu parça: penceresi tamamen içinde olan taban yok", not icinde.any(), str(np.where(icinde)[0][:5]))

    # 4) kayan düşüş kanalı: net ve bant gevşek, yalnız (3) dip savunulur eler
    dk = _hz(_seri([ARKA, (60, -0.015, 0.0005, 0.003), (60, 0.0, 0.015, 0.015)], 3))
    gev = {"netMax": 0.9, "bantMax": 0.9, "kM": 5.0}
    Tk = S.s6_taban(dk, gev)
    Tk2 = S.s6_taban(dk, dict(gev, dipTol=0.5))
    ic_k = slice(400 + 12, 460)
    kontrol("kayan kanal (-%1,5/gün): dip şartı eler", not (Tk["n"].iloc[ic_k] > 0).any(), str(Tk["n"].iloc[ic_k].dropna().tolist()[:5]))
    kontrol("kayan kanal: dipTol 0,5 ile taban çıkar (eleyen şart dip)", (Tk2["n"].iloc[ic_k] > 0).all())

    # 5) tek mum sıçrama (kapanış içeride)
    ds = _seri([ARKA, DUS, BAZ, (60, 0.0, 0.015, 0.015)], 1)
    k = 495
    ds.iloc[k, ds.columns.get_loc("High")] = ds["Close"].iloc[k] * 1.06
    dsz = _hz(ds); Ts = S.s6_taban(dsz)
    kontrol("tek mum sıçrama: o gün ve ertesi bölge sürer (aynı bolge_id), AL yok",
            Ts["bolge_id"].iat[k] >= 0 and Ts["bolge_id"].iat[k + 1] == Ts["bolge_id"].iat[k] and Ts["bolge_id"].iat[k - 1] == Ts["bolge_id"].iat[k]
            and not Ts["al"].iloc[k:k + 2].any(), f"{Ts['bolge_id'].iat[k - 1]} {Ts['bolge_id'].iat[k]} {Ts['bolge_id'].iat[k + 1]}")

    # 6) al mumu
    da = _seri([ARKA, DUS, BAZ, (60, 0.0, 0.015, 0.015)], 1)
    k = 505
    tav = da["High"].iloc[400:505].max()          # her pencerenin tavanından yüksek
    da.iloc[k, da.columns.get_loc("Close")] = tav * 1.03; da.iloc[k, da.columns.get_loc("High")] = tav * 1.04
    Ta = S.s6_taban(_hz(da)); Ra = S.s6_bolgeler(Ta)
    al = np.where(Ta["al"].to_numpy())[0]
    rk = [r for r in Ra if r["sag_i"] == k]
    kontrol("kapanışla tavan kırılımı: AL o barda", k in al and Ta["bolge_id"].iat[k] == Ta["bolge_id"].iat[k - 1] >= 0, str(al[:5]))
    kontrol("AL: bölge o barda biter (kutu AL barını içerir), durum AL", len(rk) == 1 and rk[0]["durum"] == "AL" and rk[0]["al_gun"] == str(Ta.index[k].date()))
    kontrol("AL: tavan = önceki bar tabanının en yüksek High'ı", abs(Ta["tavan"].iat[k - 1] - _hz(da)["High"].iloc[int(Ta["bas_i"].iat[k - 1]):k].max()) < 1e-9)
    kontrol("AL sonrası yeni bölgenin kutusu AL barından sonra başlar", all(r["sol_i"] > k for r in Ra if r["id"] > rk[0]["id"]) if rk else False)

    # 7) taban kırılımı
    dkr = _seri([ARKA, DUS, BAZ, (60, 0.0, 0.015, 0.015)], 1)
    k = 505
    dp = dkr["Low"].iloc[400:505].min()           # her pencerenin dibinden düşük
    dkr.iloc[k, dkr.columns.get_loc("Close")] = dp * 0.96; dkr.iloc[k, dkr.columns.get_loc("Low")] = dp * 0.95
    Tkr = S.s6_taban(_hz(dkr))
    kontrol("kapanış < DİP x 0,98: KIRILDI o barda, AL yok", bool(Tkr["kirildi"].iat[k]) and not Tkr["al"].iat[k] and Tkr["durum"].iat[k] == "KIRILDI")

    # 8) nMin / nMax
    du = _hz(_seri([ARKA, DUS, (150, 0.0, 0.001, 0.003), (60, 0.0, 0.015, 0.015)], 4))
    Tu = S.s6_taban(du)
    kontrol("uzun taban (150 bar): n en çok nMax = 70", Tu["n"].max() == 70, str(Tu["n"].max()))
    Tu2 = S.s6_taban(du, {"nMin": 10, "nMax": 20})
    kontrol("nMax = 20, nMin = 10: n 10..20", Tu2["n"].dropna().between(10, 20).all() and Tu2["n"].max() == 20)
    Ru = S.s6_bolgeler(Tu)
    kontrol("uzun taban: tek bölge (birleşim) tabanın >= %80'i", any((min(609, r["sag_i"]) - max(460, r["sol_i"]) + 1) / 150 >= 0.8 for r in Ru),
            str([(r["bas"], r["bitis"]) for r in Ru][:4]))

    # 9) önek değişmezliği ve t sonrası bozma
    for ad_, dd in (("sentetik", _hz(_seri([ARKA, DUS, BAZ, (30, 0.0, 0.015, 0.015), BAZ, (60, 0.0, 0.015, 0.015)], 5))),):
        Tt = S.s6_taban(dd); fark = 0
        for Tk_ in range(300, len(dd) + 1, 7):
            Tp = S.s6_taban(dd.iloc[:Tk_])
            for c in KOLON:
                a = Tt[c].to_numpy()[:Tk_]; b = Tp[c].to_numpy()
                if a.dtype.kind == "f":
                    fark += int((~(np.isclose(a, b.astype(float), rtol=1e-12, atol=0) | (np.isnan(a) & np.isnan(b.astype(float))))).sum())
                else:
                    fark += int((a != b).sum())
        kontrol(f"önek değişmezliği ({ad_}, her 7 barda kesim, {len(KOLON)} sütun)", fark == 0, str(fark))
        bz = dd.copy(); bz.iloc[520:, :4] = bz.iloc[520:, :4] * 1.7
        Tb = S.s6_taban(bz)
        _ayni(Tt.iloc[:520], Tb.iloc[:520], KOLON, f"t sonrası bozma ({ad_}): ilk 520 satır aynı")

    # 10) beş şart elle (sentetik, taban seçilen bir bar)
    i = int(np.where(T["n"].to_numpy() > 0)[0][len(np.where(T["n"].to_numpy() > 0)[0]) // 2])
    P = S.S6_PRM; H, L, C = d.High.to_numpy(), d.Low.to_numpy(), d.Close.to_numpy()
    Cp = np.r_[np.nan, C[:-1]]; trp = (np.fmax(H, Cp) - np.fmin(L, Cp)) / Cp
    atr = np.mean(trp[i - P["atrGun"] + 1:i + 1])

    def tutar(n):
        w = slice(i - n + 1, i + 1); h = n // 2
        mum = (H[w] - L[w]) / C[w]
        c1 = H[w].max() / L[w].min() - 1 <= P["bantMax"]
        c2 = abs(C[i] / C[i - n + 1] - 1) <= P["netMax"]
        c3 = L[i - n + h + 1:i + 1].min() >= L[i - n + 1:i - n + h + 1].min() * (1 - P["dipTol"])
        c4 = np.median(mum) <= P["kM"] * atr
        c5 = True if P["daralmaOran"] == 0 else mum.mean() <= P["daralmaOran"] * np.mean(((H - L) / C)[i - n - P["daralmaGun"] + 1:i - n + 1])
        return c1 and c2 and c3 and c4 and c5
    elle = next((n for n in range(P["nMax"], P["nMin"] - 1, -1) if tutar(n)), 0)
    kontrol("beş şart elle: en büyük tutan n aynı", elle == int(T["n"].iat[i]), f"bar {i}: elle {elle}, kod {T['n'].iat[i]}")

    # 11) Pine aynası = vektörel
    for ad_, dd, prm in (("sentetik", d, None), ("sentetik daralma 0,9", d, {"daralmaOran": 0.9}),
                         ("al / kırılım", _hz(da), None), ("kırıldı", _hz(dkr), None), ("sıçrama", dsz, None)):
        A = S.s6_pine_ayna(dd, prm); B = S.s6_taban(dd, prm)
        _ayni(A, B, ["n", "tavan", "dip", "al", "kirildi", "bolge_id", "kutu_sol_i", "kutu_sag_i", "kutu_ust", "kutu_alt", "sinif"],
              f"Pine aynası = vektörel ({ad_})")
    gercek = os.path.exists(os.path.join(VERI, "V_BIST.pkl"))
    if gercek:
        V = S.s6_veri(VERI, ["ENJSA", "PAPIL", "TUCLK", "KNFRT"])
        for s, prm in (("ENJSA", None), ("PAPIL", None), ("TUCLK", {"daralmaOran": 0.8, "bantMax": 0.2}), ("KNFRT", None)):
            dd = V[s] if s != "KNFRT" else V[s].loc["2020-01-01":"2023-06-30"]
            A = S.s6_pine_ayna(dd, prm); B = S.s6_taban(dd, prm)
            _ayni(A, B, ["n", "tavan", "dip", "al", "kirildi", "bolge_id", "kutu_sol_i", "kutu_sag_i", "kutu_ust", "kutu_alt", "sinif"],
                  f"Pine aynası = vektörel (gerçek {s}{' ' + str(prm) if prm else ''}, {len(dd)} bar)")
            RB = S.s6_bolgeler(B)
            kontrol(f"gerçek {s}: kutular üst üste binmez, her kutu >= nMin bar", S._s6_ust_uste(RB) == 0 and all(r["gun"] >= S.S6_PRM["nMin"] for r in RB),
                    str(min((r["gun"] for r in RB), default=0)))
        dd = V["PAPIL"]; Tt = S.s6_taban(dd); fark = 0
        for Tk_ in list(range(260, len(dd), 37)) + [len(dd) - 1]:
            Tp = S.s6_taban(dd.iloc[:Tk_])
            for c in KOLON:
                a = Tt[c].to_numpy()[:Tk_]; b = Tp[c].to_numpy()
                if a.dtype.kind == "f":
                    fark += int((~(np.isclose(a, b.astype(float), rtol=1e-12, atol=0) | (np.isnan(a) & np.isnan(b.astype(float))))).sum())
                else:
                    fark += int((a != b).sum())
        kontrol("önek değişmezliği (gerçek PAPIL, her 37 barda kesim)", fark == 0, str(fark))
    else:
        print(f"ATLANDI: gerçek veri yok ({VERI})")

    # 12) parametre denetimi
    hatalar = 0
    for kotu in ({"nMin": 80}, {"nMax": 300}, {"bantMax": 0}, {"daralmaOran": -1}, {"yok": 1}):
        try:
            S.s6_prm(kotu)
        except S6Hata_:
            hatalar += 1
    kontrol("geçersiz parametreler reddedilir (5/5)", hatalar == 5, str(hatalar))
    try:
        S.s6_pine_ayna(d, {"surTol": 2}); kontrol("Pine aynası yalnız birleşim kipi", False)
    except S6Hata_:
        kontrol("Pine aynası yalnız birleşim kipi", True)
    Tl = S.s6_durum(S.s6_bilesen(d), S.s6_sec(S.s6_bilesen(d)), {"surTol": 2})
    kontrol("iş tanımının harfi kipi (surTol 2, yalnız Python bilgi) çalışır", (Tl["bolge_id"] >= 0).any())

    # 13) tasarım json'u
    yj = os.path.join(CIKTI, "s6_tasarim.json")
    if os.path.exists(yj):
        J = json.load(open(yj, encoding="utf-8"))
        sec = J["secim"]["secilen"]
        kontrol("tasarım: seçilen eşikler = S6_PRM", all(abs(float(sec[k]) - float(S.S6_PRM[k])) < 1e-12 for k in S.S6_ESIK_ALAN), str(sec))
        kontrol("tasarım: ızgara 108 nokta, tamamı json'da", len(J["izgara"]) == 108)
        kontrol("tasarım: seçilen satırın puanı en yüksek puan", J["secim"]["secilen_satir"]["puan"] == max(x["puan"] for x in J["izgara"]))
        sadeler = sorted([x for x in J["izgara"] if x["puan"] == J["secim"]["en_puan"]], key=lambda x: S._s6_sade_anahtar(x["esik"]))
        kontrol("tasarım: seçim sadelik kuralına uyar", sadeler[0]["esik"] == sec)
    else:
        print("ATLANDI: s6_tasarim.json yok")

    # 14) Pine dosyası
    yp = os.path.join(CIKTI, "COL_S6_TABAN.pine"); ya = os.path.join(CIKTI, "COL_S6_TABAN_ascii.pine")
    if os.path.exists(yp):
        metin = open(yp, encoding="utf-8").read()
        ad_map = {"nMin": "nMin", "nMax": "nMax", "bantMax": "bantMax", "netMax": "netMax", "kM": "kM", "dipTol": "dipTol", "daralmaOran": "daralmaOran",
                  "kirTol": "kirTol", "atrGun": "atrGun", "daralmaGun": "daralmaGun", "konumGun": "konumGun", "smaGun": "smaGun",
                  "smaEgimGun": "smaEgimGun", "dipKonum": "dipKonum", "dipDusus": "dipDusus", "hacimGun": "hacimGun"}
        yanlis = []
        for k, v in ad_map.items():
            m = re.search(rf"^{v}\s*=\s*input\.(?:int|float)\(\s*(-?[0-9.]+)", metin, re.M)
            if not m or abs(float(m.group(1)) - float(S.S6_PRM[k])) > 1e-12:
                yanlis.append((k, m.group(1) if m else None))
        kontrol("Pine girdi varsayılanları = S6_PRM (16 alan)", not yanlis, str(yanlis))
        kod = [ln for ln in metin.splitlines() if not ln.lstrip().startswith("//")]
        kontrol("Pine: tab yok", "\t" not in metin)
        kontrol("Pine: geri sayan 'by -1' döngüsü yok", not any(re.search(r"\bfor\b.*\bby\s*-", ln) for ln in kod))
        kontrol("Pine: //@version=5 ve indicator(overlay=true)", "//@version=5" in metin and re.search(r"indicator\(.*overlay\s*=\s*true", metin) is not None)
        kontrol("Pine: plotshape / bgcolor / plot yalnız global (girintisiz)", all(not re.match(r"^\s+(plotshape|bgcolor|plot)\(", ln) for ln in kod))
        if os.path.exists(ya):
            asc = open(ya, encoding="utf-8").read()
            kontrol("ASCII kopya: ASCII dışı karakter 0", all(ord(ch) < 128 for ch in asc))
            kontrol("ASCII kopya: satır sayısı aynı", len(asc.splitlines()) == len(metin.splitlines()))
        else:
            kontrol("ASCII kopya var", False)
    else:
        print("ATLANDI: Pine dosyası yok")

    # 15) e-posta / anahtar
    yasak = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|(api[_-]?key|token|secret)\s*[:=]\s*['\"][A-Za-z0-9]{12,}", re.I)
    dosyalar = [os.path.join(KOK, "S6_TABAN.py")] + [os.path.join(CIKTI, f) for f in os.listdir(CIKTI)] if os.path.isdir(CIKTI) else [os.path.join(KOK, "S6_TABAN.py")]
    bulunan = [f for f in dosyalar if os.path.isfile(f) and yasak.search(open(f, encoding="utf-8", errors="ignore").read())]
    kontrol("e-posta / anahtar yok (S6_TABAN.py + sikisma_s6/)", not bulunan, str(bulunan))

    hata = [a for a, ok in SONUC if not ok]
    print(f"\n{len(SONUC) - len(hata)}/{len(SONUC)} TAMAM" + (f"; HATA: {hata}" if hata else ""))
    return 0 if not hata else 1


S6Hata_ = S.S6Hata

if __name__ == "__main__":
    sys.exit(main())
