# -*- coding: utf-8 -*-
"""Zincir sırası (devam eden uyumsuzluk) — UYUM_Z_ON_KAYIT.md (f5edc17). Temiz eş, hüküm MACD_UYUM fonksiyonlarıyla, plasebo hariç."""
import json, sys
import numpy as np, pandas as pd
KOK = "/home/claude/cemalcelebi/col_yolu/"; sys.path.insert(0, KOK)
import CETVEL2 as C2, IZ_KARNE as IK, MACD_UYUM as MU  # noqa: E402
D = KOK + "arastirma_cikti/macd_uyum/"
k = IK.ik_kontrol_kapisi(D + "UYUM_Z_ON_KAYIT.md"); print("KAPI:", k.get("gecti"), k.get("eksik"), k.get("hayir"))
E = pd.read_csv(D + "es_satir.csv.gz", parse_dates=["giris"]); Z = pd.read_csv(D + "uyum_zincir.csv.gz")
S = pd.read_csv(D + "uyum_satir.csv.gz"); S = S[S.hipotez == "U1"][["pazar", "sembol", "tarih", "h5", "st5", "es_h5", "es_st5"]]
E = E.merge(Z, on=["pazar", "sembol", "tarih"], how="left").merge(S, on=["pazar", "sembol", "tarih"], how="left"); E["ay"] = E.giris.dt.strftime("%Y-%m")
assert E.zincir.notna().all()
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
G = {"Z1 (ilk)": E[E.zincir == 1], "Z2 (devam, >=2)": E[E.zincir >= 2], "sıra 2": E[E.zincir == 2], "sıra 3+": E[E.zincir >= 3], "Z2 ∧ bariz dip": E[(E.zincir >= 2) & (E.F65 <= -0.05)]}
R = {}
for g, X in G.items():
    for i, p in enumerate(("ABD", "AVR", "BIST")):
        for j, h in enumerate(("d1619", "d2022")):
            c = hucre(X, p, h, 700 + 10*i + j); R[f"{g}|{p}|{h}"] = c
            if np.isfinite(c.get("fark", np.nan)):
                print(f"{g:16s} {p:4s} {h} n {c['n']:4d} FARK {y(c['fark'])} [{y(c['a'])}; {y(c['u'])}] SIRA {c['sira']:.3f} [{c['sa']:.3f}] L3O {y(c['l3o'])} güç {c['guc']:.2f} {c['hukum']:10s} r15 {y(c['r15'])}/{y(c['es'])} h5 {c['h5']*100:.1f}/{c['es_h5']*100:.1f} stop {c['st']*100:.1f}/{c['es_st']*100:.1f}")
KH = [f"{p}|{h}" for p in ("ABD", "AVR") for h in ("d1619", "d2022")]
fk = {q: R["Z2 (devam, >=2)|" + q]["fark"] - R["Z1 (ilk)|" + q]["fark"] for q in KH}; hk = {q: R["Z2 (devam, >=2)|" + q]["hukum"] for q in KH}
print("Z2 - Z1:", {q: y(x) for q, x in fk.items()})
karar = "AÇIK VERİDE TUTTU (plasebo hariç)" if all(h == "TUTAR" for h in hk.values()) and all(x > 0 for x in fk.values()) else ("TUTMADI" if any(h == "TUTMADI" for h in hk.values()) else ("ÖLÇÜLEMEDİ" if all(h == "ÖLÇÜLEMEDİ" for h in hk.values()) else "ÇELİŞKİLİ"))
print("KARAR Z2:", karar, hk)
# BETİMSEL: sıra 1 olayından sonra zincir devam etti mi (sonradan bakma)
O = pd.read_csv(D + "uyum_olay.csv.gz"); O = O[O.hipotez == "U1"].sort_values(["pazar", "sembol", "i"]).merge(Z, on=["pazar", "sembol", "tarih"])
sonra = (O.zincir.shift(-1) == O.zincir + 1) & (O.sembol.shift(-1) == O.sembol) & (O.pazar.shift(-1) == O.pazar)
O["devam"] = sonra.to_numpy()
M = E.merge(O[["pazar", "sembol", "tarih", "devam"]], on=["pazar", "sembol", "tarih"])
M1 = M[(M.zincir == 1) & M.pazar.isin(["ABD", "AVR"]) & M.r15.notna()]
bt = M1.groupby("devam").agg(n=("r15", "size"), r15=("r15", "mean"), es=("es_r15_temiz", "mean"), h5=("h5", "mean"), stop=("st5", "mean")).round(4)
print("BETİMSEL (ABD + AVR, sıra 1): 60 barda daha derin dipte yeni uyumsuzluk geldi mi?\n", bt.to_string())
print("zincir uzunluğu dağılımı (bütün U1, zincirin son halkası):", O[~O.devam].zincir.clip(upper=5).value_counts(normalize=True).sort_index().round(3).to_dict())
json.dump({"on_kayit": "f5edc17", "karar": karar, "hucre": R, "Z2_eksi_Z1": fk, "betimsel": bt.reset_index().to_dict("records")}, open(D + "uyum_z_sonuc.json", "w"), ensure_ascii=False, indent=1, default=float)
