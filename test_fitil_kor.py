"""test_fitil_kor — FITIL_KOR.py sentetik testleri (veri gerekmez).

1) taban içi tanımı (S6 açık bölge + DİP sınıfı) ve satır maskeleri   2) geleceğe bakma: seri t'de kesilince bayraklar / kutu aynı
3) kırılım (YUKARI / AŞAĞI / YOK / ölçülmez)   4) iki grup ay kümeli fark bootstrap yönü   5) ayrışma etiketi
6) kör sayfa: ad / tarih yok, t'den sonra bar yok   7) yanıt ayrıştırma + Fisher   8) kapı: ön kayıt yok -> durur; kontrol listesi 14 satır geçer
9) e-posta / anahtar taraması
Çalıştır: python test_fitil_kor.py
"""
import os
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
warnings.filterwarnings("ignore")

import FITIL_KOR as FK  # noqa: E402

GECTI, KALDI = [], []


def kontrol(ad, kosul, ek=""):
    (GECTI if kosul else KALDI).append(ad)
    print(("  OK   " if kosul else "  HATA ") + ad + (f"  ({ek})" if ek else ""))


def seri(n=700, tohum=5):
    """Düşüş -> uzun dar taban (alt fitilsiz, üst fitilli mumlar) -> çıkış."""
    rng = np.random.default_rng(tohum); C = []
    x = 100.0
    for i in range(n):
        if i < 320:
            x *= 1 + rng.normal(0.0005, 0.02)
        elif i < 420:
            x *= 1 - 0.006 + rng.normal(0, 0.01)
        elif i < 600:
            x = 50 * (1 + 0.01 * np.sin(i / 3)) if x > 0 else 50
        else:
            x *= 1.01
        C.append(x)
    C = np.array(C); O = np.r_[C[0], C[:-1]]
    H = np.maximum(O, C) * (1 + np.abs(rng.normal(0.006, 0.003, n)))
    L = np.minimum(O, C) * (1 - np.abs(rng.normal(0.006, 0.003, n)))
    L[420:600] = np.minimum(O, C)[420:600] * 0.9995                     # alt fitil ~ yok
    H[420:600] = np.maximum(O, C)[420:600] * 1.008                      # üst fitil
    return pd.DataFrame({"Open": O, "High": H, "Low": L, "Close": C, "Volume": rng.integers(1e5, 2e5, n).astype(float)},
                        index=pd.bdate_range("2018-01-01", periods=n))


print("1) taban içi tanımı")
d = seri(); Z = FK.fk_hisse(d)
kontrol("ic -> ölçülür", bool((~Z.ic | Z.olculur).all()))
kontrol("ic ve dis ayrık, birleşimi ölçülür", bool((~(Z.ic & Z.dis)).all() and ((Z.ic | Z.dis) == Z.olculur).all()))
kontrol("ic günlerinde kutu tanımlı", bool(Z.loc[Z.ic, ["ust", "alt"]].notna().all().all()), f"ic {int(Z.ic.sum())}")
kontrol("taban içi gün var (sentetik taban)", int(Z.ic.sum()) > 0)
M = FK.fk_satir_maske(Z, "SENT")
kontrol("SP_ic = SP & ic", bool((M["SP_ic"] == (Z.SP & Z.ic).to_numpy()).all()))
kontrol("K_SP ∩ SP_ic boş", not bool((M["K_SP"] & M["SP_ic"]).any()))
kontrol("K_SP_r ⊆ K_SP, bölge başına 1", bool((~M["K_SP_r"] | M["K_SP"]).all()) and
        int(M["K_SP_r"].sum()) == len(np.unique(Z.bolge.to_numpy()[M["K_SP"]])))
kontrol("K_SP_r tekrar üretilir (tohum)", bool((FK.fk_satir_maske(Z, "SENT")["K_SP_r"] == M["K_SP_r"]).all()))

# EK S+DÜZ: düz dip oranı elle
i = 450; w = d.iloc[i - 9:i + 1]
el = (w.Low.max() - w.Low.min()) / (w.High - w.Low).median()
kontrol("düz dip oranı elle", np.isclose(Z.duz_oran.iloc[i], el), f"{el:.3f}")
kontrol("SPD = SP & duz & dipb & ölçülür", bool((M["SPD"] == (Z.SP & Z.duz & Z.dipb & Z.olculur).to_numpy()).all()))
kontrol("K_DUZ ∩ SPD boş; SPD07 ⊆ SPD ⊆ SPD15", not bool((M["K_DUZ"] & M["SPD"]).any()) and bool((~M["SPD07"] | M["SPD"]).all())
        and bool((~M["SPD"] | M["SPD15"]).all()))

print("2) geleceğe bakma")
iyi = True
for t in list(Z.index[Z.ic][:: max(1, int(Z.ic.sum()) // 6)]) + list(Z.index[Z.SP][:3]):
    Zk = FK.fk_hisse(d[d.index <= t]).iloc[-1]; Zt = Z.loc[t]
    iyi &= bool(Zk.duz == Zt.duz and Zk.dipb == Zt.dipb and Zk.ic == Zt.ic and Zk.SP == Zt.SP and Zk.SM == Zt.SM and (not Zt.ic or (np.isclose(Zk.ust, Zt.ust) and np.isclose(Zk.alt, Zt.alt))))
kontrol("kesilmiş seride bayrak / kutu aynı", iyi)

print("3) kırılım")
C = np.array([10.0] * 5 + [10.5, 11.2, 9.0] + [10.0] * 70)
kontrol("YUKARI", FK.fk_kirilim(C, 4, 11.0, 9.5) == "YUKARI")
kontrol("AŞAĞI (x0,98)", FK.fk_kirilim(C, 4, 12.0, 9.5) == "ASAGI")
kontrol("x0,98 sınırı: 9,2 > 9,5*0,98=9,31 değil -> AŞAĞI; 9,4 dip -> 9,212 > 9,0 AŞAĞI", FK.fk_kirilim(C, 4, 12.0, 9.4) == "ASAGI")
kontrol("YOK", FK.fk_kirilim(C, 4, 12.0, 8.0) == "YOK")
kontrol("ölçülmez (60 bar yok)", FK.fk_kirilim(C, 30, 12.0, 8.0) == "OLCULMEZ")

print("4) fark bootstrap")
rng = np.random.default_rng(1)
a = rng.normal(0.05, 0.1, 400); b = rng.normal(0.0, 0.1, 400)
ga = np.array([f"2024-{1 + i % 12:02d}" for i in range(400)]); gb = ga.copy()
r = FK.fk_fark_boot(a, ga, b, gb)
kontrol("fark > 0 ve alt uç > 0", r["fark"] > 0 and r["alt95"] > 0, f"{r['fark']:.3f} [{r['alt95']:.3f}]")
r0 = FK.fk_fark_boot(b, gb, b, gb)
kontrol("aynı grup: aralık 0'ı kapsar", r0["alt95"] < 0 < r0["ust95"])
kontrol("tekrar üretilir", FK.fk_fark_boot(a, ga, b, gb) == r)

print("5) ayrışma etiketi")
kontrol("+ AYRIŞIR", FK.fk_ayrisma(r, "+") == "AYRIŞIR")
kontrol("- ayna AYRIŞMAZ", FK.fk_ayrisma(r, "-") == "AYRIŞMAZ")
kontrol("n < 30 ÖLÇÜLEMEDİ", FK.fk_ayrisma(FK.fk_fark_boot(a[:10], ga[:10], b, gb), "+") == "ÖLÇÜLEMEDİ")
kontrol("genel dört hücre", FK.fk_ayrisma_genel({k: "AYRIŞIR" for k in ["ABD 2023", "ABD 2024-26", "AVR 2023", "AVR 2024-26"]}) == "KONTROLDEN AYRIŞIR")
kontrol("genel kısmi", FK.fk_ayrisma_genel({"ABD 2023": "AYRIŞIR", "ABD 2024-26": "AYRIŞMAZ"}).startswith("KISMİ"))

print("6) kör sayfa")
t = d.index[500]
fig = FK.fk_kor_sayfa(d, t, 7)
m = " ".join(FK._fk_metinler(fig))
kontrol("ad / yıl yok", "SENT" not in m and "2019" not in m and "2020" not in m, m[:80])
ax = fig.axes[0]
nbar = sum(1 for q in ax.patches if abs(getattr(q, "get_width", lambda: 0)() - 0.62) < 1e-9)  # gri zemin hariç mumlar
kontrol("50 mum (sonrası yok)", nbar == 50, f"{nbar}")
kontrol("numara var", "No 7" in m)
import matplotlib.pyplot as plt  # noqa: E402
plt.close(fig)
try:
    FK.fk_kor_sayfa(d, d.index[20], 1); kontrol("kısa pencere durur", False)
except FK.FKHata:
    kontrol("kısa pencere durur", True)

print("7) yanıt + Fisher")
c = FK.fk_cevap_ayristir(",".join(f"{i}:{'E' if i % 2 else 'h'}" for i in range(1, 41)), 40)
kontrol("40 yanıt", len(c) == 40 and c[2] == "H")
for bozuk in ("1:E,2:X", "1:E", "1:E,1:H," + ",".join(f"{i}:E" for i in range(2, 41))):
    try:
        FK.fk_cevap_ayristir(bozuk, 40); kontrol(f"bozuk yanıt durur ({bozuk[:8]})", False)
    except FK.FKHata:
        kontrol(f"bozuk yanıt durur ({bozuk[:8]})", True)
kontrol("Fisher [[8,2],[1,5]] = 0,0350", abs(FK.fk_fisher(8, 2, 1, 5) - 0.0350) < 5e-4, f"{FK.fk_fisher(8, 2, 1, 5):.4f}")
kontrol("Fisher eşit = 1", abs(FK.fk_fisher(5, 5, 5, 5) - 1.0) < 1e-9)

print("8) kapı")
td = tempfile.mkdtemp()
try:
    FK.fk_kapi(td, git=False); kontrol("ön kayıt yok -> durur", False)
except FK.FKHata:
    kontrol("ön kayıt yok -> durur", True)
import IZ_KARNE as IK  # noqa: E402
yol = os.path.join(td, "x.md"); open(yol, "w", encoding="utf-8").write(FK.fk_kontrol_tablosu())
kontrol("kontrol listesi 14 satır kapıdan geçer", IK.ik_kontrol_kapisi(yol, dur=False)["gecti"])
open(yol, "w", encoding="utf-8").write("FK_ESIK_SHA: `" + "0" * 64 + "`\n")
try:
    FK.fk_onkayit_dogrula(yol, git=False); kontrol("sha tutmuyor -> durur", False)
except FK.FKHata:
    kontrol("sha tutmuyor -> durur", True)

print("9) sızıntı taraması")
try:
    FK._fk_sizinti("iletisim: ornek" + "@" + "alan.com", "t"); kontrol("e-posta yakalanır", False)
except FK.FKHata:
    kontrol("e-posta yakalanır", True)
kod = open(os.path.join(KOK, "FITIL_KOR.py"), encoding="utf-8").read()
kontrol("kodda e-posta / anahtar yok", not FK._FK_EPOSTA.search(kod) and not FK._FK_ANAHTAR.search(kod))

print(f"\nSONUÇ: {len(GECTI)} / {len(GECTI) + len(KALDI)} geçti" + (f"; KALAN: {KALDI}" if KALDI else ""))
sys.exit(1 if KALDI else 0)
