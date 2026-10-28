# KONTROL (Cemal 28 Eki: 'ya sen hata yapıyorsun görmüyorsun'): ölçüm hattı kör mü, sağır mı?
# POZİTİF KONTROL: sinyal = GELECEĞE bakarak seçilen günler (60 gün sonra +%20 üstü olacak olaylar). Hat sağlamsa bütün hücrelerde 'tutar'.
# NEGATİF KONTROL: sinyal = rastgele günler (20 tohum). Hat sağlamsa hücre başına yanlış 'tutar' oranı ~%5 ve karar İZ DEĞİL.
# YARI-POZİTİF: geleceğe bakan sinyallerin yarısı rastgeleyle karıştırılır (+%10 beklenen fark); hat bunu da görmeli (zayıf iz).
import sys, pandas as pd, numpy as np; sys.path.insert(0, "/home/user/col_yolu"); import FON_IZI as F
Vs = {pz: pd.read_pickle(f"/tmp/veri/V_{pz}.pkl") for pz in ("ABD", "AVR", "BIST")}
Pn = {pz: pd.read_pickle(f"/tmp/claude-0/-home-user-col-yolu/82c570e4-187d-577a-9149-eeb29748a7da/scratchpad/olcut_panel_{pz}.pkl") for pz in ("ABD", "AVR", "BIST")}
O = F.FI_OLCUT; Z = []; rng = np.random.default_rng(0)
def olc(ad, pz, E):
    T = F.fi_olcut_olay(Pn[pz], E); out = []
    for dn, a, b in O["donem"]:
        h = F.fi_olcut_hucre(T[(T.giris >= a) & (T.giris <= b)], O)
        out.append({"kontrol": ad, "pazar": pz, "donem": dn, **h, "tutar": bool(h.get("n", 0) >= 30 and h.get("alt95", -1) > 0 and h.get("sira", 0) > 0.5 and h.get("portfoy", -1) > h.get("portfoy_esli_p90", 9))})
    return out
for pz in Vs:
    P = Pn[pz]; R = P["R"]; ok = P["ok"]; tarih = P["tarih"]; sem = P["sembol"]
    # pozitif: her ay rastgele 40 (gün, hisse) çifti, r60 >= +0.20 olanlardan
    iyi = np.argwhere(ok & (R >= 0.20)); kotu_iyi = np.argwhere(ok)
    sec = iyi[rng.choice(len(iyi), min(3000, len(iyi)), replace=False)]
    E = pd.DataFrame({"sembol": [sem[j] for _, j in sec], "giris": [tarih[i] for i, _ in sec]}).drop_duplicates().sort_values("giris")
    Z += olc("POZITIF_gelecek_r60>=20", pz, E)
    # yarı pozitif: yarısı iyi, yarısı rastgele
    r2 = kotu_iyi[rng.choice(len(kotu_iyi), 1500, replace=False)]
    E2 = pd.concat([E.iloc[:1500], pd.DataFrame({"sembol": [sem[j] for _, j in r2], "giris": [tarih[i] for i, _ in r2]})]).drop_duplicates().sort_values("giris")
    Z += olc("YARI_POZITIF", pz, E2)
    # negatif: 20 tohum rastgele
    for t in range(20):
        r3 = kotu_iyi[np.random.default_rng(100 + t).choice(len(kotu_iyi), 1500, replace=False)]
        Z += olc(f"NEGATIF_{t}", pz, pd.DataFrame({"sembol": [sem[j] for _, j in r3], "giris": [tarih[i] for i, _ in r3]}).drop_duplicates().sort_values("giris"))
Z = pd.DataFrame(Z); Z.to_csv("/tmp/claude-0/-home-user-col-yolu/82c570e4-187d-577a-9149-eeb29748a7da/scratchpad/kontrol.csv", index=False)
pd.set_option("display.width", 250)
print(Z[~Z.kontrol.str.startswith("NEGATIF")][["kontrol","pazar","donem","n","ort_fark","alt95","sira","portfoy","portfoy_esli_p90","tutar"]].round(3).to_string())
N = Z[Z.kontrol.str.startswith("NEGATIF")]
print("NEGATİF: hücre başına yanlış 'tutar' oranı", round(N.tutar.mean(), 3), "| ort fark ortalaması", round(N.ort_fark.mean(), 4), "| alt95>0 oranı", round((N.alt95 > 0).mean(), 3), "| sıra>0,5 oranı", round((N.sira > 0.5).mean(), 3))
print("NEGATİF: dört karar hücresi (ABD+AVR) birden tutan tohum sayısı /20:", sum(all(N[(N.kontrol == f"NEGATIF_{t}") & (N.pazar == pz) & (N.donem == dn)].tutar.iat[0] for pz in ("ABD", "AVR") for dn in ("2023", "2024-26")) for t in range(20)))
print("BITTI", flush=True)
