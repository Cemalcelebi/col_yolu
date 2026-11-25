# -*- coding: utf-8 -*-
"""U1b (bariz derin ikinci dip, F65 <= -%5) alt küme ölçümü — UYUM_B_ON_KAYIT.md (d1ca775) kuralıyla. Ç217 satır dosyasından;
hücre hükmü MACD_UYUM ile aynı fonksiyonlar (C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum), plasebo hariç; önce kontrol kapısı."""
import hashlib
import json
import sys

import numpy as np
import pandas as pd

KOK = "/home/claude/cemalcelebi/col_yolu/"
sys.path.insert(0, KOK)
import CETVEL2 as C2  # noqa: E402
import IZ_KARNE as IK  # noqa: E402
import MACD_UYUM as MU  # noqa: E402

D = KOK + "arastirma_cikti/macd_uyum/"
kapi = IK.ik_kontrol_kapisi(D + "UYUM_B_ON_KAYIT.md")
print("KONTROL KAPISI:", {k: v for k, v in kapi.items() if k in ("gecti", "durum", "eksik", "hayir")} or kapi)
secim = json.load(open(D + "uyum_ornek20_secim.json"))
if hashlib.sha256(open(D + "uyum_satir.csv.gz", "rb").read()).hexdigest() != secim["satir_sha256"]:
    sys.exit("DUR: satır dosyası sha farklı")
S = pd.read_csv(D + "uyum_satir.csv.gz", parse_dates=["giris", "tarih"])
U = S[S.hipotez == "U1"].copy()
U["ay"] = U.giris.dt.to_period("M").astype(str)
KARAR_H = [(p, h) for p in ("ABD", "AVR") for h in ("d1619", "d2022")]


def hucre(X, p, h, tohum_ek):
    x = X[(X.pazar == p) & (X.donem == h)].dropna(subset=["r15", "es_r15"])
    if len(x) < 2:
        return dict(n=len(x), fark=np.nan, hukum="ÖLÇÜLEMEDİ")
    c = C2.c2_hucre(x.r15.to_numpy(float), x.es_r15.to_numpy(float), x.sira.to_numpy(float), x.giris.to_numpy(), "+",
                    tohum_ek=tohum_ek, egri=C2._c2_egri22_al(p, h, 15, None))
    c["sira_alt"], c["sira_ust"] = MU.mu_sira_boot(x.sira.to_numpy(float), x.ay.to_numpy(), tohum_ek)
    c["plasebo_gecti"] = True  # plasebo HARİÇ hüküm (ön kayıt)
    hk, neden = MU.mu_hukum(c)
    return dict(n=int(c.get("n", len(x))), fark=c.get("fark"), boot_alt=c.get("boot_alt"), boot_ust=c.get("boot_ust"),
                sira=c.get("sira"), sira_alt=c["sira_alt"], l3o=c.get("l3o"), guc=c.get("guc"), hukum=hk, neden=neden,
                h5=x.h5.mean(), es_h5=x.es_h5.mean(), st=x.st5.mean(), es_st=x.es_st5.mean(), r15=x.r15.mean(),
                es_r15=x.es_r15.mean())


def y(v, k=2):
    return "-" if v is None or not np.isfinite(v) else f"{v*100:+.{k}f}".replace(".", ",")


v = hucre(U, "ABD", "d1619", 1)
if not (v["n"] == 1279 and abs(v["fark"] * 100 + 0.39) < 0.006 and abs(v["sira"] - 0.481) < 0.0006):
    sys.exit("DUR: Ç217 yeniden üretilemedi")
print("DOĞRULAMA tuttu: U1 ABD d1619 n 1279, FARK", y(v["fark"]))

gr = {"U1b": U[U.F65 <= -0.05], "U1e": U[U.F65 > -0.01], "U1bb": U[U.F65 <= -0.10]}
print("olay sayısı:", {k: len(x) for k, x in gr.items()}, "U1:", len(U))
SON = {}
for kod, X in gr.items():
    for i, p in enumerate(["ABD", "AVR", "BIST"]):
        for j, h in enumerate(["d1619", "d2022"]):
            SON[f"{kod}|{p}|{h}"] = hucre(X, p, h, 300 + 10 * i + j)
sat = []
for k, c in SON.items():
    kod, p, h = k.split("|")
    if not np.isfinite(c.get("fark", np.nan)):
        sat.append([kod, p, h, c["n"], "-", "-", "-", "-", c["hukum"], "-", "-", "-"])
        continue
    sat.append([kod, p, h, c["n"], f"{y(c['fark'])} [{y(c['boot_alt'])}; {y(c['boot_ust'])}]", f"{c['sira']:.3f} [{c['sira_alt']:.3f}]",
                y(c["l3o"]), f"{c['guc']:.2f}", c["hukum"], f"{c['h5']*100:.1f} / {c['es_h5']*100:.1f}",
                f"{c['st']*100:.1f} / {c['es_st']*100:.1f}", f"{y(c['r15'])} / {y(c['es_r15'])}"])
print(pd.DataFrame(sat, columns=["hip", "pazar", "hücre", "n", "FARK [%95]", "SIRA [alt]", "L3O", "güç", "hüküm", "h5 olay/eş",
                                 "stop olay/eş", "r15 olay/eş"]).to_string(index=False))
fk = {f"{p}|{h}": SON[f"U1b|{p}|{h}"]["fark"] - SON[f"U1e|{p}|{h}"]["fark"] for p in ("ABD", "AVR", "BIST") for h in ("d1619", "d2022")}
print("U1b - U1e FARK:", {k: y(v_) for k, v_ in fk.items()})
olc = {f"{p}|{h}": SON[f"U1b|{p}|{h}"]["hukum"] for p, h in KARAR_H}
tut = all(o == "TUTAR" for o in olc.values()) and all(fk[k] > 0 for k in olc)
karar = "AÇIK VERİDE TUTTU (plasebo hariç; plasebo ve KASA gerekir)" if tut else (
    "ÖLÇÜLEMEDİ" if all(o == "ÖLÇÜLEMEDİ" for o in olc.values()) else "TUTMADI")
print("KARAR U1b:", karar, olc)

# doz-yanıt (bilgi): dilim FARK'ları ve Spearman
dil = [("e", U.F65 > -0.01), ("d1", (U.F65 <= -0.01) & (U.F65 > -0.05)), ("d2", (U.F65 <= -0.05) & (U.F65 > -0.10)),
       ("d3", U.F65 <= -0.10)]
doz = {}
for p, h in KARAR_H + [("BIST", "d1619"), ("BIST", "d2022")]:
    fs, ns = [], []
    for ad, m in dil:
        x = U[m & (U.pazar == p) & (U.donem == h)].dropna(subset=["fark"])
        fs.append(float(x.fark.mean()) if len(x) else np.nan)
        ns.append(int(len(x)))
    rho = pd.Series(fs).rank().corr(pd.Series(range(4)), method="spearman") if np.all(np.isfinite(fs)) else np.nan
    doz[f"{p}|{h}"] = dict(fark=fs, n=ns, spearman=rho)
    print(f"DOZ {p} {h}: " + " | ".join(f"{a} n {n_} {y(f_)}" for (a, _), n_, f_ in zip(dil, ns, fs)) + f" | Spearman {rho:+.2f}")
art = all(np.isfinite(doz[f'{p}|{h}']['spearman']) and doz[f'{p}|{h}']['spearman'] > 0 for p, h in KARAR_H)
print("Derinlikle artıyor (4 karar hücresinde Spearman > 0):", art)
json.dump({"on_kayit": "d1ca775", "kontrol_kapisi": str(kapi)[:300], "karar": karar, "derinlikle_artiyor": bool(art),
           "hucre": {k: {kk: (float(vv) if isinstance(vv, (int, float, np.floating)) else vv) for kk, vv in c.items()} for k, c in SON.items()},
           "U1b_eksi_U1e": {k: float(v_) for k, v_ in fk.items()}, "doz": doz,
           "n": {k: int(len(x)) for k, x in gr.items()}}, open(D + "uyum_b_sonuc.json", "w"), ensure_ascii=False, indent=1, default=str)
print("yazıldı: uyum_b_sonuc.json")
