# -*- coding: utf-8 -*-
"""Toplam uyumsuzluk (zincir tek uyumsuzluk) — UYUM_T_ON_KAYIT.md (c4cc7d7). Temiz eş; hüküm MACD_UYUM fonksiyonlarıyla, plasebo hariç."""
import json, sys
import numpy as np, pandas as pd
KOK = "/home/claude/cemalcelebi/col_yolu/"; sys.path.insert(0, KOK)
import CETVEL2 as C2, IZ_KARNE as IK, MACD_UYUM as MU  # noqa: E402
D = KOK + "arastirma_cikti/macd_uyum/"
k = IK.ik_kontrol_kapisi(D + "UYUM_T_ON_KAYIT.md"); print("KAPI:", k.get("gecti"), k.get("eksik"), k.get("hayir"))
E = pd.read_csv(D + "es_satir.csv.gz", parse_dates=["giris"]).merge(pd.read_csv(D + "uyum_toplam.csv.gz"), on=["pazar", "sembol", "tarih"], how="left")
S = pd.read_csv(D + "uyum_satir.csv.gz"); S = S[S.hipotez == "U1"][["pazar", "sembol", "tarih", "h5", "st5", "es_h5", "es_st5"]]
E = E.merge(S, on=["pazar", "sembol", "tarih"], how="left"); E["ay"] = E.giris.dt.strftime("%Y-%m"); assert E.PFc.notna().all()
def hucre(X, p, h, tek):
    x = X[(X.pazar == p) & (X.donem == h)].dropna(subset=["r15", "es_r15_temiz"])
    if len(x) < 2: return dict(n=len(x), fark=np.nan, hukum="ÖLÇÜLEMEDİ")
    c = C2.c2_hucre(x.r15.to_numpy(float), x.es_r15_temiz.to_numpy(float), x.sira_temiz.to_numpy(float), x.giris.to_numpy(), "+", tohum_ek=tek, egri=C2._c2_egri22_al(p, h, 15, None))
    c["sira_alt"], _ = MU.mu_sira_boot(x.sira_temiz.to_numpy(float), x.ay.to_numpy(), tek); c["plasebo_gecti"] = True
    return dict(n=int(c["n"]), fark=c["fark"], a=c["boot_alt"], u=c["boot_ust"], sira=c["sira"], sa=c["sira_alt"], l3o=c["l3o"], guc=c["guc"], hukum=MU.mu_hukum(c)[0],
                r15=x.r15.mean(), es=x.es_r15_temiz.mean(), h5=x.h5.mean(), es_h5=x.es_h5.mean(), st=x.st5.mean(), es_st=x.es_st5.mean())
y = lambda v: "-" if v is None or not np.isfinite(v) else f"{v*100:+.2f}".replace(".", ",")
v = hucre(E[E.F65 <= -0.05], "ABD", "d1619", 1)
if not (v["n"] == 502 and abs(v["fark"]*100 + 0.16) < 0.006): sys.exit("DUR: doğrulama")
print("DOĞRULAMA tuttu")
T = (E.PFc <= -0.10) & (E.MRc >= 0.30); R = {}
for g, X in {"T (derin toplam)": E[T], "Tz (kalan)": E[~T]}.items():
    for i, p in enumerate(("ABD", "AVR", "BIST")):
        for j, h in enumerate(("d1619", "d2022")):
            c = hucre(X, p, h, 900 + 10*i + j); R[f"{g}|{p}|{h}"] = c
            print(f"{g:17s} {p:4s} {h} n {c['n']:4d} FARK {y(c['fark'])} [{y(c['a'])}; {y(c['u'])}] SIRA {c['sira']:.3f} [{c['sa']:.3f}] L3O {y(c['l3o'])} güç {c['guc']:.2f} {c['hukum']:10s} r15 {y(c['r15'])}/{y(c['es'])} h5 {c['h5']*100:.1f}/{c['es_h5']*100:.1f} stop {c['st']*100:.1f}/{c['es_st']*100:.1f}")
KH = [(p, h) for p in ("ABD", "AVR") for h in ("d1619", "d2022")]
fk = {f"{p}|{h}": R[f"T (derin toplam)|{p}|{h}"]["fark"] - R[f"Tz (kalan)|{p}|{h}"]["fark"] for p, h in KH}; hk = {q: R["T (derin toplam)|" + q]["hukum"] for q in fk}
print("T - Tz:", {q: y(x) for q, x in fk.items()})
karar = "AÇIK VERİDE TUTTU (plasebo hariç)" if all(h == "TUTAR" for h in hk.values()) and all(x > 0 for x in fk.values()) else ("TUTMADI" if any(h == "TUTMADI" for h in hk.values()) else ("ÖLÇÜLEMEDİ" if all(h == "ÖLÇÜLEMEDİ" for h in hk.values()) else "ÇELİŞKİLİ"))
print("KARAR T:", karar, hk)
E["ft"] = E.r15 - E.es_r15_temiz; doz = {}
for ad, kol, kes in (("PFc", -E.PFc, [0.05, 0.10, 0.20]), ("MRc", E.MRc, [0.10, 0.30, 0.50])):
    b = np.digitize(kol, kes)
    for p, h in KH:
        x = E[(E.pazar == p) & (E.donem == h)]; f = [x.ft[b[x.index] == q].mean() for q in range(4)]; n = [int((b[x.index] == q).sum()) for q in range(4)]
        rho = pd.Series(f).corr(pd.Series(range(4)), method="spearman"); doz[f"{ad}|{p}|{h}"] = dict(fark=f, n=n, rho=rho)
        print(f"DOZ {ad} {p} {h}: " + " | ".join(f"n {a} {y(c)}" for a, c in zip(n, f)) + f" | Spearman {rho:+.2f}")
json.dump({"on_kayit": "c4cc7d7", "karar": karar, "hucre": R, "T_eksi_Tz": fk, "doz": doz}, open(D + "uyum_t_sonuc.json", "w"), ensure_ascii=False, indent=1, default=float)
