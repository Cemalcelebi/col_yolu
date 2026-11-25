# -*- coding: utf-8 -*-
"""U1n (net derin ikinci dip) alt küme ölçümü — UYUM_N_ON_KAYIT.md (ff9a3ba) kuralıyla. Ç217 satır dosyasından;
hücre hükmü MACD_UYUM ile aynı fonksiyonlar (C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum), plasebo hariç."""
import hashlib
import json
import sys

import numpy as np
import pandas as pd

KOK = "/home/claude/cemalcelebi/col_yolu/"
sys.path.insert(0, KOK)
import CETVEL2 as C2  # noqa: E402
import MACD_UYUM as MU  # noqa: E402

D = KOK + "arastirma_cikti/macd_uyum/"
secim = json.load(open(D + "uyum_ornek20_secim.json"))
sha = hashlib.sha256(open(D + "uyum_satir.csv.gz", "rb").read()).hexdigest()
if sha != secim["satir_sha256"]:
    sys.exit("DUR: satır dosyası sha farklı")
S = pd.read_csv(D + "uyum_satir.csv.gz", parse_dates=["giris", "tarih"])
U = S[S.hipotez == "U1"].copy()
U["ay"] = U.giris.dt.to_period("M").astype(str)


def hucre(X, p, h, tohum_ek):
    x = X[(X.pazar == p) & (X.donem == h)].dropna(subset=["r15", "es_r15"])
    eg = C2._c2_egri22_al(p, h, 15, None)
    c = C2.c2_hucre(x.r15.to_numpy(float), x.es_r15.to_numpy(float), x.sira.to_numpy(float), x.giris.to_numpy(), "+",
                    tohum_ek=tohum_ek, egri=eg)
    c["sira_alt"], c["sira_ust"] = MU.mu_sira_boot(x.sira.to_numpy(float), x.ay.to_numpy(), tohum_ek)
    c["plasebo_gecti"] = True  # plasebo HARİÇ hüküm (ön kayıt)
    hk, neden = MU.mu_hukum(c)
    return dict(n=int(c.get("n", len(x))), fark=c.get("fark"), boot_alt=c.get("boot_alt"), boot_ust=c.get("boot_ust"),
                sira=c.get("sira"), sira_alt=c["sira_alt"], l3o=c.get("l3o"), guc=c.get("guc"), hukum=hk, neden=neden,
                h5=x.h5.mean(), es_h5=x.es_h5.mean(), h10=x.h10.mean(), es_h10=x.es_h10.mean(), st=x.st5.mean(),
                es_st=x.es_st5.mean(), r15=x.r15.mean(), es_r15=x.es_r15.mean())


def yuz(v, k=2):
    return "-" if v is None or not np.isfinite(v) else f"{v*100:+.{k}f}".replace(".", ",")


# 1) doğrulama: U1 ABD d1619 Ç217 değerleri
v = hucre(U, "ABD", "d1619", 1)
print("DOĞRULAMA U1 ABD d1619: n", v["n"], "FARK", yuz(v["fark"]), "SIRA", round(v["sira"], 3), "L3O", yuz(v["l3o"]), "güç",
      round(v["guc"], 2), v["hukum"])
if not (v["n"] == 1279 and abs(v["fark"] * 100 + 0.39) < 0.006 and abs(v["sira"] - 0.481) < 0.0006):
    sys.exit("DUR: Ç217 yeniden üretilemedi")

# 2) U1n / U1e
gr = {"U1n": U[U.F65 <= -0.01], "U1e": U[U.F65 > -0.01]}
print("olay sayısı U1n / U1e / U1:", len(gr["U1n"]), len(gr["U1e"]), len(U))
SON = {}
for kod, X in gr.items():
    for i, p in enumerate(["ABD", "AVR", "BIST"]):
        for j, h in enumerate(["d1619", "d2022"]):
            SON[f"{kod}|{p}|{h}"] = hucre(X, p, h, 100 + 10 * i + j)
satir = []
for k, c in SON.items():
    kod, p, h = k.split("|")
    satir.append([kod, p, h, c["n"], f"{yuz(c['fark'])} [{yuz(c['boot_alt'])}; {yuz(c['boot_ust'])}]",
                  f"{c['sira']:.3f} [{c['sira_alt']:.3f}]", yuz(c["l3o"]), f"{c['guc']:.2f}", c["hukum"],
                  f"{c['h5']*100:.1f} / {c['es_h5']*100:.1f}", f"{c['st']*100:.1f} / {c['es_st']*100:.1f}",
                  f"{yuz(c['r15'])} / {yuz(c['es_r15'])}"])
T = pd.DataFrame(satir, columns=["hip", "pazar", "hücre", "n", "FARK [%95]", "SIRA [alt]", "L3O", "güç", "hüküm",
                                 "h5 olay/eş", "stop olay/eş", "r15 olay/eş"])
print(T.to_string(index=False))
fk = {}
for p in ["ABD", "AVR", "BIST"]:
    for h in ["d1619", "d2022"]:
        a, b = SON[f"U1n|{p}|{h}"]["fark"], SON[f"U1e|{p}|{h}"]["fark"]
        fk[f"{p}|{h}"] = a - b
print("U1n - U1e FARK (puan):", {k: yuz(v_) for k, v_ in fk.items()})
karar_h = [f"{p}|{h}" for p in ["ABD", "AVR"] for h in ["d1619", "d2022"]]
tut = all(SON["U1n|" + k]["hukum"] == "TUTAR" for k in karar_h) and all(fk[k] > 0 for k in karar_h)
olc = [SON["U1n|" + k]["hukum"] for k in karar_h]
karar = "AÇIK VERİDE TUTTU (plasebo hariç)" if tut else ("ÖLÇÜLEMEDİ" if all(o == "ÖLÇÜLEMEDİ" for o in olc) else "TUTMADI")
print("KARAR U1n:", karar, "| hücreler:", dict(zip(karar_h, olc)))

# 3) anahtar (hesaptan SONRA): Cemal'in 20 sayfası DOĞRU vs YANLIŞ
A = json.load(open(D + "uyum_ornek20_anahtar.json"))
sayfa = pd.DataFrame(A["sayfalar"])
isaret = {1: "Y", 2: "Y", 3: "Y", 4: "D", 5: "D", 6: "Y", 7: "D", 8: "D", 9: "D", 10: "D", 11: "Y", 12: "D", 13: "Y", 14: "D",
          15: "Y", 16: "D", 17: "Y", 18: "D", 19: "Y", 20: "D"}
sayfa["isaret"] = sayfa["sayfa"].map(isaret)
kol = [c for c in ["h5", "h10", "stop_oldu", "r15", "es_r15", "fark"] if c in sayfa.columns]
print("anahtar alanları:", list(sayfa.columns)[:20])
print(sayfa.groupby("isaret")[kol].mean().round(4).to_string())
print(sayfa.groupby("isaret").size().to_dict())
json.dump({"on_kayit": "ff9a3ba", "dogrulama": {k: (float(v[k]) if isinstance(v[k], (int, float, np.floating)) else v[k])
                                                for k in ["n", "fark", "sira", "l3o", "guc", "hukum"]},
           "hucre": {k: {kk: (float(vv) if isinstance(vv, (int, float, np.floating)) else vv) for kk, vv in c.items()}
                     for k, c in SON.items()},
           "U1n_eksi_U1e": {k: float(v_) for k, v_ in fk.items()}, "karar": karar,
           "n_U1n": int(len(gr["U1n"])), "n_U1e": int(len(gr["U1e"]))},
          open(D + "uyum_n_sonuc.json", "w"), ensure_ascii=False, indent=1, default=str)
print("yazıldı: uyum_n_sonuc.json")
