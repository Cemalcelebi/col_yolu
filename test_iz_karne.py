# =====================================================================
#  test_iz_karne.py — IZ_KARNE mekanik denetimi (indeks + tek cetvel)
#  1) Kayıt: kodlar tekil, sinyaller tanımlı, yön geçerli, sinyali olan kaydın yönü var.
#  2) Defter kapsamı: IZ_DEFTERI A/B tablolarındaki her madde (A1.., B1..) en az bir kaydın 'defter' alanında geçer
#     (yeni madde eklenip indekse yazılmazsa test kırılır).
#  3) İndeks eşitliği: IZ_DEFTERI içindeki işaretli bölüm, ik_indeks_metni() ile birebir aynı (elle düzenleme / bayat indeks yakalanır).
#  4) Tekilleştirme: aynı hissede 60 işlem günü içindeki ikinci olay düşer.
#  5) Karar kuralı: 4/4 >=1,3 + ters <1,3 -> İZ; ters de >=1,3 -> İZ DEĞİL; 3/4 -> ADAY; koruma yönü ters çevrilir;
#     ABD verisi yok -> en fazla BIST-ADAY; n<30 -> KÜÇÜK ÖRNEK.
#  6) Sinyaller (sentetik): tavan/taban günü, hacimli düşüş, ileriye bakmama (olay günü sonrası veri değişince sinyal aynı).
#  7) Doji kutusu seçimi ileriye bakan 'kirilim' sütununu kullanmaz.
# =====================================================================
import inspect
import os
import re
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import IZ_KARNE as I   # noqa: E402


def sina():
    hata = []
    ay = I.IKAyar()
    # 1) kayıt
    kod = [r["kod"] for r in I.IK_KAYIT]
    if len(kod) != len(set(kod)):
        hata.append("1) tekrar eden kod")
    for r in I.IK_KAYIT:
        if r["sinyal"] and (r["sinyal"] not in I.IK_SINYAL or r["yon"] not in ("yukari", "asagi", "koruma")):
            hata.append(f"1) {r['kod']} sinyal/yön tanımsız")
    # 1b) hata defteri (Cemal, 14 Kas 2026): her satır tam, tür listeden, tarih artan
    son = ""
    for n, h in enumerate(I.IK_HATA, 1):
        if any(not str(h.get(k, "")).strip() for k in ("tarih", "kayit", "hata", "tur", "bulan", "etki", "duzeltme", "ders", "kaynak")):
            hata.append(f"1b) H{n} eksik alan")
        if h["tur"] not in I.IK_HATA_TUR:
            hata.append(f"1b) H{n} tür tanımsız: {h['tur']}")
        if h["tarih"] < son:
            hata.append(f"1b) H{n} tarih sırası bozuk ({h['tarih']} < {son})")
        son = max(son, h["tarih"])
    # 2) defter kapsamı
    metin = open(ay.defter, encoding="utf-8").read()
    maddeler = set(re.findall(r"^\| (A\d+|B\d+(?:'')?) \|", metin, flags=re.M))
    alan = " ".join(r["defter"] for r in I.IK_KAYIT)
    eksik = sorted(m for m in maddeler if not re.search(r"(?<![A-Z0-9])" + re.escape(m) + r"(?![0-9])", alan))
    if eksik:
        hata.append(f"2) defter maddesi indekste yok: {eksik}")
    # 3) indeks eşitliği
    if I.IK_ISARET[0] not in metin or I.IK_ISARET[1] not in metin:
        hata.append("3) IZ_DEFTERI'nde indeks bölümü yok")
    else:
        bolum = metin[metin.index(I.IK_ISARET[0]):metin.index(I.IK_ISARET[1]) + len(I.IK_ISARET[1])]
        if bolum != I.ik_indeks_metni(ay):
            hata.append("3) indeks bayat ya da elle düzenlenmiş: `python IZ_KARNE.py indeks`")
    # 4) tekilleştirme
    g = pd.to_datetime(["2024-01-02", "2024-02-15", "2024-04-20", "2024-01-03"])
    T = I.ik_tekil(pd.DataFrame({"sembol": ["X", "X", "X", "Y"], "gun": g}), 60)
    if sorted(zip(T.sembol, T.gun.dt.strftime("%m-%d"))) != [("X", "01-02"), ("X", "04-20"), ("Y", "01-03")]:
        hata.append(f"4) tekilleştirme yanlış: {list(zip(T.sembol, T.gun))}")
    # 5) karar kuralı
    def Z(kat, ters, n=100, erken=1.0):
        s = []
        for p in ("BIST", "ABD"):
            for d, _, _ in I.IK_DONEM:
                k = erken if d == "2016-22" else kat
                s.append({"pazar": p, "donem": d, "n": n, "ana_kat": k, "ters_kat": ters})
        return pd.DataFrame(s)
    beklenen = [(Z(1.5, 1.0), False, "yukari", "İZ"), (Z(1.5, 1.4), False, "yukari", "İZ DEĞİL"),
                (Z(1.5, 1.0, n=20), False, "yukari", "KÜÇÜK ÖRNEK"), (Z(0.6, 1.0), False, "koruma", "İZ"),
                (Z(1.5, 1.0, erken=1.5), True, "asagi", "BIST-ADAY"), (Z(1.1, 1.0), False, "yukari", "İZ DEĞİL")]
    z3 = Z(1.5, 1.0); z3.loc[(z3.pazar == "ABD") & (z3.donem == "2023"), "ana_kat"] = 1.1
    beklenen.append((z3, False, "yukari", "ADAY"))
    for z, abd, yon, k in beklenen:
        sonuc = I.ik_karar(z, abd, ay, yon)[0]
        if sonuc != k:
            hata.append(f"5) karar {yon} abd_yok={abd}: {sonuc} != {k}")
    # 6) sinyaller (sentetik)
    idx = pd.bdate_range("2023-01-02", periods=120)
    c = np.full(120, 10.0); c[50] = 11.0; c[51:] = 11.0; c[80] = 10.3; c[81:] = 10.3
    v = np.full(120, 1000.0); v[80] = 5000
    d = pd.DataFrame({"Open": c, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": v}, index=idx)
    V = {"X": d}
    tv = I.ik_s_tavan(ay, "BIST", V); tb = I.ik_s_taban(ay, "BIST", V); hd = I.ik_s_hacim_dus(ay, "BIST", V)
    if list(tv.gun) != [idx[50]] or list(tb.gun) != [idx[80]] or list(hd.gun) != [idx[80]]:
        hata.append(f"6) sinyal yanlış: {list(tv.gun)} {list(tb.gun)} {list(hd.gun)}")
    d2 = d.copy(); d2.iloc[90:, :4] *= 0.5
    if list(I.ik_s_hacim_dus(ay, "BIST", {"X": d2}).gun)[:1] != [idx[80]]:
        hata.append("6) sinyal ileriye bakıyor")
    # 7) doji seçimi
    kod7 = "\n".join(l.split("#")[0] for l in inspect.getsource(I.ik_s_doji_kutu).split('"""')[-1].splitlines())
    if "kirilim" in kod7:      # denetim 24 Eki: eskiden yalnız ilk yorumdan önceki metne bakıyordu (seçim satırı denetlenmiyordu)
        hata.append("7) doji kutusu seçimi ileriye bakan 'kirilim' sütununu kullanıyor")
    return hata


if __name__ == "__main__":
    h = sina()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_iz_karne: 7/7 OK")
