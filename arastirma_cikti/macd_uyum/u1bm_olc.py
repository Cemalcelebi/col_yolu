# -*- coding: utf-8 -*-
"""U1bm (bariz dip + MACD farkı >= %20) temiz eşle — UYUM_BM_ON_KAYIT.md (426b707). Hüküm MACD_UYUM fonksiyonlarıyla, plasebo hariç."""
import json, sys
import numpy as np, pandas as pd
KOK = "/home/claude/cemalcelebi/col_yolu/"; sys.path.insert(0, KOK)
import CETVEL2 as C2, IZ_KARNE as IK, MACD_UYUM as MU  # noqa: E402
D = KOK + "arastirma_cikti/macd_uyum/"
k = IK.ik_kontrol_kapisi(D + "UYUM_BM_ON_KAYIT.md"); print("KAPI:", k.get("gecti"), k.get("eksik"), k.get("hayir"))
E = pd.read_csv(D + "es_satir.csv.gz", parse_dates=["giris"])
O = pd.read_csv(D + "uyum_olay.csv.gz"); O = O[O.hipotez == "U1"][["pazar", "sembol", "tarih", "F66", "F66m"]]
O["MR"] = O.F66 / (O.F66m - O.F66).abs()
E = E.merge(O[["pazar", "sembol", "tarih", "MR"]], on=["pazar", "sembol", "tarih"], how="left"); E["ay"] = E.giris.dt.strftime("%Y-%m")
def hucre(X, p, h, tek, es="es_r15_temiz", sr="sira_temiz"):
    x = X[(X.pazar == p) & (X.donem == h)].dropna(subset=["r15", es])
    if len(x) < 2: return dict(n=len(x), fark=np.nan, hukum="ÖLÇÜLEMEDİ", guc=np.nan)
    c = C2.c2_hucre(x.r15.to_numpy(float), x[es].to_numpy(float), x[sr].to_numpy(float), x.giris.to_numpy(), "+", tohum_ek=tek, egri=C2._c2_egri22_al(p, h, 15, None))
    c["sira_alt"], _ = MU.mu_sira_boot(x[sr].to_numpy(float), x.ay.to_numpy(), tek); c["plasebo_gecti"] = True
    hk, _ = MU.mu_hukum(c)
    return dict(n=int(c["n"]), fark=c["fark"], a=c["boot_alt"], u=c["boot_ust"], sira=c["sira"], sa=c["sira_alt"], l3o=c["l3o"], guc=c["guc"], hukum=hk, r15=x.r15.mean(), es=x[es].mean(), med=(x.r15 - x[es]).median())
y = lambda v: "-" if v is None or not np.isfinite(v) else f"{v*100:+.2f}".replace(".", ",")
B = E[E.F65 <= -0.05]
v = hucre(B, "ABD", "d1619", 1)
if not (v["n"] == 502 and abs(v["fark"]*100 + 0.16) < 0.006): sys.exit(f"DUR: doğrulama {v['n']} {v['fark']}")
print("DOĞRULAMA tuttu")
G = {"U1bm": B[B.MR >= 0.20], "U1bz": B[B.MR < 0.20], "U1m(fiyat şartsız)": E[E.MR >= 0.20], "U1bm35": B[B.MR >= 0.35]}
S = {}
for g, X in G.items():
    for i, p in enumerate(("ABD", "AVR", "BIST")):
        for j, h in enumerate(("d1619", "d2022")):
            c = hucre(X, p, h, 500 + 10*i + j); S[f"{g}|{p}|{h}"] = c
            e = hucre(X, p, h, 500 + 10*i + j, "es_r15", "sira") if g == "U1bm" else None
            if np.isfinite(c.get("fark", np.nan)):
                print(f"{g:20s} {p:4s} {h} n {c['n']:4d} FARK {y(c['fark'])} [{y(c['a'])}; {y(c['u'])}] med {y(c['med'])} SIRA {c['sira']:.3f} [{c['sa']:.3f}] L3O {y(c['l3o'])} güç {c['guc']:.2f} {c['hukum']:10s} r15 {y(c['r15'])} / eş {y(c['es'])}" + (f" | eski eş FARK {y(e['fark'])}" if e else ""))
KH = [f"{p}|{h}" for p in ("ABD", "AVR") for h in ("d1619", "d2022")]
fk = {q: S["U1bm|" + q]["fark"] - S["U1bz|" + q]["fark"] for q in KH}; hk = {q: S["U1bm|" + q]["hukum"] for q in KH}
print("U1bm - U1bz:", {q: y(v_) for q, v_ in fk.items()})
if all(h == "TUTAR" for h in hk.values()) and all(v_ > 0 for v_ in fk.values()): karar = "AÇIK VERİDE TUTTU (plasebo hariç)"
elif any(h == "TUTMADI" for h in hk.values()): karar = "TUTMADI"
elif all(h == "ÖLÇÜLEMEDİ" for h in hk.values()): karar = "ÖLÇÜLEMEDİ"
else: karar = "ÇELİŞKİLİ"
print("KARAR U1bm:", karar, hk)
json.dump({"on_kayit": "426b707", "karar": karar, "hucre": S, "U1bm_eksi_U1bz": fk}, open(D + "uyum_bm_sonuc.json", "w"), ensure_ascii=False, indent=1, default=float)
