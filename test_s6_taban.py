"""S6_TABAN testleri (sentetik veri + gerçek veride Pine aynası / önek değişmezliği; getiri ÖLÇMEZ). Çalıştırma: python test_s6_taban.py

1) çakışma kapısı  2) sakin taban bulunur (DİP sınıfı, uzunluk nMin..nMax)  3) eğimli pencere -> taban yok  4) kayan düşüş kanalı -> (3) dip
şartı eler (net ve bant gevşekken)  5) tek mum sıçrama (kapanış içeride) bölgeyi bitirmez, AL yok  6) kapanışla tavanı kıran mum -> AL, bölge
o barda biter  7) taban kırılımı -> KIRILDI  8) nMin / nMax sınırları  9) ÖNEK DEĞİŞMEZLİĞİ (sentetik + gerçek; al / kirildi / bolge_id dahil)
ve t sonrası bozma  10) beş şart elle (ham OHLC'den, bir barda)  11) Pine aynası (döngü) = vektörel (sentetik + gerçek, daralma açık / kapalı)
12) parametre denetimi  13) tasarım json'u: seçilen = S6_PRM, puan  14) Pine dosyası: girdiler = S6_PRM, ASCII kopya, yasak kalıplar
15) e-posta / anahtar yok.
v1.1 (S6_V11_IS_TANIMI.md): 16) referans ATR% pencere dışı (pencere içi bozulunca değişmez; elle ortalama; 120 bar alt sınırı)
17) BB yüzdeliği (elle numpy; SIKISMA_OBEK.so_s5 ile karşılaştırma)  18) sönme (SONDU günü taban yok, AL / KIRILDI yok, bolge_son_tur)
19) onay günü (bölgenin ilk barı; o güne kadar kutu bilinmiyor; kutu >= nMin)  20) v1.0 KİPİ BİREBİR: refOnce = bbSart = False ile git'teki v1.0
koduyla bütün sütunlar aynı (sentetik + 4 gerçek hisse) ve 16 etiket çıktısı v1.0 json'u ile aynı  21) v1.1 tasarım json'u (seçim kuralı).
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
    gev = dict({"netMax": 0.9, "bantMax": 0.9, "kM": 5.0}, **S.S6_V10_KIP)   # yalnız (3) dip şartı sınanır: v1.1 şartları (ref, BB) kapalı
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
        for s, prm in (("ENJSA", None), ("PAPIL", None), ("TUCLK", {"daralmaOran": 0.8, "bantMax": 0.2}), ("KNFRT", None),
                       ("ENJSA", dict(S.S6_V10_KIP)), ("PAPIL", {"bbEsik": 0.15, "refOnce": False}), ("TUCLK", {"bbSart": False})):
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
    kotuler = ({"nMin": 80}, {"nMax": 300}, {"bantMax": 0}, {"daralmaOran": -1}, {"yok": 1}, {"refMin": 300}, {"bbEsik": 0}, {"refOnce": "evet"},
               {"bbSart": 1})
    for kotu in kotuler:
        try:
            S.s6_prm(kotu)
        except S6Hata_:
            hatalar += 1
    kontrol(f"geçersiz parametreler reddedilir ({len(kotuler)}/{len(kotuler)})", hatalar == len(kotuler), str(hatalar))
    try:
        S.s6_pine_ayna(d, {"surTol": 2}); kontrol("Pine aynası yalnız birleşim kipi", False)
    except S6Hata_:
        kontrol("Pine aynası yalnız birleşim kipi", True)
    Tl = S.s6_durum(S.s6_bilesen(d), S.s6_sec(S.s6_bilesen(d)), {"surTol": 2})
    kontrol("iş tanımının harfi kipi (surTol 2, yalnız Python bilgi) çalışır", (Tl["bolge_id"] >= 0).any())

    v11_testleri(d, gercek)

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
        ad_map = {k: k for k in S.S6_PRM if k not in ("surTol", "refOnce", "bbSart")}
        yanlis = []
        for k, v in ad_map.items():
            m = re.search(rf"^{v}\s*=\s*input\.(?:int|float)\(\s*(-?[0-9.]+)", metin, re.M)
            if not m or abs(float(m.group(1)) - float(S.S6_PRM[k])) > 1e-12:
                yanlis.append((k, m.group(1) if m else None))
        for k in ("refOnce", "bbSart"):
            m = re.search(rf"^{k}\s*=\s*input\.bool\(\s*(true|false)", metin, re.M)
            if not m or (m.group(1) == "true") != bool(S.S6_PRM[k]):
                yanlis.append((k, m.group(1) if m else None))
        kontrol(f"Pine girdi varsayılanları = S6_PRM ({len(ad_map) + 2} alan, v1.1 dahil)", not yanlis, str(yanlis))
        kod = [ln for ln in metin.splitlines() if not ln.lstrip().startswith("//")]
        kontrol("Pine: tab yok", "\t" not in metin)
        kontrol("Pine: geri sayan 'by -1' döngüsü yok", not any(re.search(r"\bfor\b.*\bby\s*-", ln) for ln in kod))
        kontrol("Pine: //@version=5 ve indicator(overlay=true)", "//@version=5" in metin and re.search(r"indicator\(.*overlay\s*=\s*true", metin) is not None)
        kontrol("Pine: plotshape / bgcolor / plot yalnız global (girintisiz)", all(not re.match(r"^\s+(plotshape|bgcolor|plot)\(", ln) for ln in kod))
        kontrol("Pine v1.1: mor elmas, kesik kutu, sönme etiketi, tarih etiketi, bool girdiler",
                "shape.diamond" in metin and "border_style=line.style_dashed" in metin and '"sonme"' in metin and "label.style_label_upper_left" in metin
                and re.search(r"^refOnce\s*=\s*input\.bool", metin, re.M) is not None and re.search(r"^bbSart\s*=\s*input\.bool", metin, re.M) is not None)
        kontrol("Pine: 4 boşluk girinti (kod satırları)", all((len(ln) - len(ln.lstrip(" "))) % 4 == 0 for ln in kod if ln.strip()))
        kontrol("Pine: nesne sınırı (kutu 240 + 240, çizgi 480, etiket 240 + 240 <= 500)",
                metin.count("> 240") == 4 and metin.count("> 480") == 1 and "max_labels_count=500" in metin)
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


def _v10_modul():
    """git geçmişindeki son v1.0 S6_TABAN.py (S6_SURUM 'S6_TABAN v1.0' olan en yeni commit) ayrı ad alanında; yoksa None."""
    import subprocess
    try:
        refs = subprocess.run(["git", "log", "--format=%H", "--", "S6_TABAN.py"], cwd=KOK, capture_output=True, text=True, check=True).stdout.split()
    except Exception:  # git yok
        return None
    for ref in refs:
        try:
            kod = subprocess.run(["git", "show", f"{ref}:S6_TABAN.py"], cwd=KOK, capture_output=True, text=True, check=True).stdout
        except Exception:  # bu commit'te dosya yok
            continue
        if 'S6_SURUM = "S6_TABAN v1.0' in kod:
            g = {"__name__": "s6_v10", "__file__": os.path.join(KOK, "S6_TABAN.py")}
            exec(compile(kod, "S6_TABAN_v10.py", "exec"), g)
            return g
    return None


def v11_testleri(d, gercek):
    P = S.S6_PRM
    # 16) referans ATR% pencere dışı
    Z = S.s6_bilesen(d)
    i = len(d) - 30; j = 10; n = int(Z["ns"][j])
    trp = (np.fmax(d.High.to_numpy(), np.r_[np.nan, d.Close.to_numpy()[:-1]]) - np.fmin(d.Low.to_numpy(), np.r_[np.nan, d.Close.to_numpy()[:-1]])) \
        / np.r_[np.nan, d.Close.to_numpy()[:-1]]
    elle = np.mean(trp[i - n - P["refGun"] + 1:i - n + 1])
    kontrol("referans ATR%: = ort(TR/C_önceki) [i-n-249, i-n] (elle)", abs(Z["B"]["atrRef"][i, j] - elle) < 1e-12 * max(1, elle), f"{Z['B']['atrRef'][i, j]} {elle}")
    bz = d.copy(); w = bz.index[i - n + 1:i + 1]
    bz.loc[w, "High"] = bz.loc[w, "High"] * 1.3; bz.loc[w, "Low"] = bz.loc[w, "Low"] * 0.75
    Zb = S.s6_bilesen(bz)
    kontrol("referans ATR%: pencere içi mumlar büyüyünce değişmez (pencere dışı)", Zb["B"]["atrRef"][i, j] == Z["B"]["atrRef"][i, j])
    kontrol("v1.0 ATR% ise pencere içi bozulunca değişir (karşı sınama)", Zb["atr"][i] != Z["atr"][i])
    ii = np.arange(len(d)); kk = ii - n
    alt = (kk >= P["refMin"]) & (kk < P["refGun"])
    tr2 = np.r_[0.0, trp[1:]]
    kisa_ok = all(abs(Z["B"]["atrRef"][t, j] - np.mean(tr2[1:t - n + 1])) < 1e-12 for t in np.where(alt)[0][:20])
    kontrol("referans ATR%: 120 <= önceki bar < 250 iken mevcut barların ortalaması, < 120 iken ölçülemez",
            kisa_ok and np.isnan(Z["B"]["atrRef"][kk < P["refMin"], j]).all() and np.isfinite(Z["B"]["atrRef"][kk >= P["refMin"], j]).all())
    # 17) BB yüzdeliği
    C = d.Close.to_numpy(); t = len(d) - 5
    bw = np.array([2 * P["bbK"] * np.std(C[k - P["bbGun"] + 1:k + 1]) / np.mean(C[k - P["bbGun"] + 1:k + 1]) if k >= P["bbGun"] - 1 else np.nan
                   for k in range(len(C))])
    elle_p = np.mean(bw[t - P["bbDagilim"]:t] <= bw[t])
    kontrol("BB yüzdeliği (elle numpy std ddof 0, önceki 250) = Z['bbp']", abs(Z["bbp"][t] - elle_p) < 1e-12, f"{Z['bbp'][t]} {elle_p}")
    kontrol("BB yüzdeliği ilk 250 + 19 barda yok (NaN)", np.isnan(Z["bbp"][:P["bbDagilim"] + P["bbGun"] - 1]).all() and np.isfinite(Z["bbp"][P["bbDagilim"] + P["bbGun"] - 1:]).all())
    T0 = S.s6_taban(d, {"bbSart": False}); T1 = S.s6_taban(d)
    kontrol("BB şartı: tabanlı barlar BB kapalının alt kümesi, hepsinde bbp <= bbEsik",
            bool(((T1["n"] > 0) <= (T0["n"] > 0)).all() and (T1.loc[T1["n"] > 0, "bbp"] <= P["bbEsik"]).all()))
    if gercek:
        import SIKISMA_OBEK as SO
        Vb = S.s6_veri(VERI, ["ENJSA", "TUCLK", "PAPIL"])
        top = es = 0; enb = 0.0
        for x in Vb:
            a_ = SO.so_s5(Vb[x], "BIST")["bbp"].to_numpy(); b_ = S.s6_taban(Vb[x])["bbp"].to_numpy()
            ok = np.isfinite(a_) & np.isfinite(b_)
            top += int(ok.sum()); es += int((a_[ok] == b_[ok]).sum()); enb = max(enb, float(np.max(np.abs(a_[ok] - b_[ok]))))
            kontrol(f"BB yüzdeliği tanımlı barlar SIKISMA_OBEK ile aynı ({x})", bool((np.isfinite(a_) == np.isfinite(b_)).all()))
        kontrol("BB yüzdeliği = SIKISMA_OBEK.so_s5 bbp (>= %99,5 bar birebir; fark yalnız eşitlikte 1/250: pandas std son ondalık)",
                es / top >= 0.995 and enb <= 1 / 250 + 1e-12, f"{es}/{top}, en büyük fark {enb}")
    # 18) sönme ve 19) onay günü (sentetik + gerçek)
    kume = [("sentetik", d, None)]
    if gercek:
        Vg = S.s6_veri(VERI, ["ENJSA", "PAPIL", "TUCLK", "DESA"])
        kume += [(x, Vg[x], None) for x in Vg] + [("ENJSA v1.0 kipi", Vg["ENJSA"], S.S6_V10_KIP)]
    for ad_, dd, prm in kume:
        T = S.s6_taban(dd, prm); R = S.s6_bolgeler(T)
        sd = np.where(T["durum"].to_numpy() == "SONDU")[0]
        sonme_ok = all(T["n"].iat[k] != T["n"].iat[k] and not T["al"].iat[k] and not T["kirildi"].iat[k] and T["bolge_id"].iat[k] == -1
                       and T["bolge_id"].iat[k - 1] >= 0 and T["bolge_son_tur"].iat[k] == "SONDU" for k in sd)
        bas_son = all(T["bolge_son_tur"].iat[r["sag_i"]] in ("AL", "KIRILDI") if r["durum"] in ("AL", "KIRILDI") else True for r in R)
        kontrol(f"sönme ({ad_}): {len(sd)} SÖNDÜ günü taban yok, AL / KIRILDI yok, önceki gün bölge açık, bolge_son_tur SONDU",
                len(sd) > 0 and sonme_ok and bas_son)
        son_tur = all(r["bolge_son_tur"] == r["durum"] and (r["durum"] != "SONDU" or T["bolge_son_tur"].iat[-1] in ("SONDU", "AL", "KIRILDI", "ACIK")) for r in R)
        kontrol(f"bolge_son_tur ({ad_}): AL / KIRILDI / SONDU / ACIK ve son bölgede son barın değeriyle aynı",
                son_tur and (not R or T["bolge_son_tur"].iat[-1] == R[-1]["durum"]) and set(r["durum"] for r in R) <= {"AL", "KIRILDI", "SONDU", "ACIK"})
        bid = T["bolge_id"].to_numpy(); on = np.where(T["onay"].to_numpy())[0]
        ilk = [int(np.where(bid == r["id"])[0][0]) for r in R]
        onay_ok = (list(on) == ilk == [r["onay_i"] for r in R] and all(r["sol_i"] <= r["onay_i"] <= r["sag_i"] for r in R)
                   and all(T["onay_i"].iat[k] == r["onay_i"] for r in R for k in range(r["onay_i"], r["sag_i"] + 1))
                   and all(r["onay_i"] - int(T["kutu_sol_i"].iat[r["onay_i"]]) + 1 >= S.S6_PRM["nMin"] for r in R)
                   and all((bid[r["sol_i"]:r["onay_i"]] != r["id"]).all() for r in R))
        kontrol(f"onay günü ({ad_}, {len(R)} bölge): bölgenin ilk barı, kutu o gün >= nMin bar, öncesinde bölge bilinmiyor", onay_ok)
    # 20) v1.0 kipi birebir (git'teki v1.0 koduyla)
    g10 = _v10_modul()
    if g10 is None:
        print("ATLANDI: git'te v1.0 S6_TABAN.py yok")
    else:
        kume = [("sentetik", d)]
        if gercek:
            Vg = S.s6_veri(VERI, ["ENJSA", "PAPIL", "TUCLK", "KNFRT", "CCOLA"])
            kume += [(x, Vg[x]) for x in Vg]
        for ad_, dd in kume:
            for prm in (None, {"bantMax": 0.2, "daralmaOran": 0.8}):
                A = g10["s6_taban"](dd, prm); B = S.s6_taban(dd, dict(prm or {}, **S.S6_V10_KIP))
                _ayni(A, B, KOLON + ["bant", "net", "mum_atr", "daralma", "dip_sav", "al_boy", "al_hacim", "atr"],
                      f"v1.0 kipi = git v1.0 kodu ({ad_}{' ' + str(prm) if prm else ''}, {len(dd)} bar)")
    yj = os.path.join(CIKTI, "s6_tasarim.json")
    if os.path.exists(yj) and gercek:
        J = json.load(open(yj, encoding="utf-8"))
        sem = sorted({et["sembol"] for et in S.S6_ETIKET})
        Ve = S.s6_veri(VERI, sem); Z_ = {x: S.s6_bilesen(Ve[x]) for x in sem}
        e = dict(J["secim"]["secilen"], **S.S6_V10_KIP)
        T_ = {x: S.s6_durum(Z, S.s6_sec(Z, e), e) for x, Z in Z_.items()}; R_ = {x: S.s6_bolgeler(T) for x, T in T_.items()}
        yeni = [S.s6_etiket_sina(T_, R_, et) for et in S.S6_ETIKET]
        eski = J["secim"]["secilen_satir"]["etiket"]
        kes = [{k: (y.get(k) if k != "bolge" else ({kk: y["bolge"][kk] for kk in (e_["bolge"] or {})} if y.get("bolge") else None)) for k in e_}
               for e_, y in zip(eski, yeni)]
        kontrol("v1.0 kipi: 16 etiket (+3 bilgi) çıktısı v1.0 json'u ile BİREBİR", len(eski) == len(yeni) and S._s6_json_esit(eski, kes))
        # 21) v1.1 tasarım json'u
        if "v11" in J:
            V1 = J["v11"]
            sec = V1["secilen"]
            kontrol("v1.1 tasarım: seçilen = S6_PRM (refOnce, bbSart, bbEsik)", sec["refOnce"] == P["refOnce"] and sec["bbSart"] == P["bbSart"]
                    and (not sec["bbSart"] or abs(sec["bbEsik"] - P["bbEsik"]) < 1e-12), str(sec))
            kontrol("v1.1 tasarım: 8 nokta, v1.0 kipi birebir bayrağı", len(V1["izgara"]) == 8 and V1["v10_kipi_birebir"] is True)
            ilk = None
            for r, b in S.S6_IZGARA_V11["sade_sira"]:
                x = [y for y in V1["izgara"] if y["ref"] == r and y["bb"] == b][0]
                if x["puan14"] >= V1["taban_puan14"]:
                    ilk = x; break
            kontrol("v1.1 tasarım: seçim kuralına uyar (tabanın altına düşmeyen ilk sade aday)", ilk is not None and ilk["ad"] == V1["secilen_ad"])
            tb = [y for y in V1["izgara"] if y["ref"] is False and y["bb"] is None][0]
            kontrol("v1.1 tasarım: v1.0 kipi puanı = v1.0 seçilen satır puanı (KNFRT iki etiket düşülmüş)",
                    tb["puan16"] == J["secim"]["secilen_satir"]["puan"] and tb["puan14"] == tb["puan16"] - sum(
                        1 for y in tb["etiket"] if y["ad"] in S.S6_IZGARA_V11["puan_disi"] and y["tuttu"]))
        else:
            kontrol("v1.1 tasarım json'u var", False)


S6Hata_ = S.S6Hata

if __name__ == "__main__":
    sys.exit(main())
