# =====================================================================
#  KALIBRASYON — Cemal'in el ile isaretledigi coller vs kodun buldugu
#  "Edit-based validation": kac bar kaydirdik = hata olcusu
# =====================================================================
import numpy as np, pandas as pd

# Cemal'in defterinden (2 Eylul 2026). Tarihler DD/MM okundu; belirsizler '?'
CEMAL = [
    ("TEHOL", "2024-10-07", "2024-12-12", "yukseliyor"),
    ("INVES", "2025-05-08", "2025-06-20", "yukseliyor"),
    ("BURVA", "2025-06-26", "2025-07-21", "yukseliyor"),
    ("EYGYO", "2025-05-28", "2025-07-10", "bitiyor"),
    ("BASCM", "2025-03-02", "2025-07-01", "bitiyor"),
    ("SEYKM", "2025-04-15", "2025-07-16", ""),
    ("GEDZA", "2024-10-15", "2024-12-02", ""),
    ("SUNTK", "2024-08-27", "2024-11-11", "bitiyor"),
    ("HDFGS", "2025-04-22", "2025-06-12", "bitiyor ?"),
    ("INFO",  "2025-03-26", "2025-05-20", "bitiyor"),
    ("KATMR", "2025-04-16", "2025-07-16", ""),
    ("OTTO",  "2024-07-02", "2024-09-12", "bitiyor"),
]

def _bar_fark(df, t1, t2):
    """t1'den t2'ye kac islem gunu (negatif = t2 once)"""
    a = df.index.get_indexer([pd.Timestamp(t1)], method="nearest")[0]
    b = df.index.get_indexer([pd.Timestamp(t2)], method="nearest")[0]
    return int(b - a)

def kalibrasyon(liste=None, veri=None, **ayar):
    liste = liste or CEMAL; veri = veri if veri is not None else VERI
    R = []
    for s, cb, cs, nt in liste:
        k = s if s in veri else next((z for z in veri if z.split('.')[0]==s), None)
        d = {"sembol": s, "cemal_bas": cb, "cemal_son": cs}
        if not k: d["durum"]="VERIDE YOK"; R.append(d); continue
        df = veri[k]
        x = df[df.index <= pd.Timestamp(cs)]
        if len(x) < 250: d["durum"]="VERI KISA"; R.append(d); continue
        try: r = col_segment(x, **ayar)
        except Exception as e: r = None
        if not r: d["durum"]="SEGMENT YOK"; R.append(d); continue
        cemal_uz = _bar_fark(df, cb, cs) + 1
        d.update({"durum":"bulundu",
                  "kod_bas": r["bas_tarih"], "kod_son": r["son_tarih"],
                  "cemal_bar": cemal_uz, "kod_bar": r["uzunluk"],
                  # + = kod GEC basladi (colun bir kismini kacirdi), - = erken (fazla aldi)
                  "bas_fark": _bar_fark(df, cb, r["bas_tarih"]),
                  "yuk_atr": r["yukseklik_atr"], "govde": r["govde_ort"], "not": nt})
        R.append(d)
    t = pd.DataFrame(R)
    pd.set_option("display.width", 220); pd.set_option("display.max_columns", None)
    print(t.to_string(index=False))
    b = t[t.durum=="bulundu"]
    if len(b):
        print(f"\n  bulundu        : {len(b)}/{len(t)}")
        print(f"  bas farki      : medyan {b.bas_fark.median():+.0f} bar | "
              f"ort |fark| {b.bas_fark.abs().mean():.1f} bar")
        print(f"  uzunluk orani  : kod/cemal medyan {(b.kod_bar/b.cemal_bar).median():.2f}")
        print(f"  <=5 bar isabet : {int((b.bas_fark.abs()<=5).sum())}/{len(b)}")
        gec = b[b.bas_fark > 5]; erk = b[b.bas_fark < -5]
        if len(gec): print(f"  GEC baslayan   : {', '.join(gec.sembol)}  (colun basini kacirdi)")
        if len(erk): print(f"  ERKEN baslayan : {', '.join(erk.sembol)}  (fazla bar aldi)")
    return t

def parametre_tara(liste=None, veri=None):
    """Hangi ayar Cemal'in bolgelerine en yakin sonucu veriyor?"""
    liste = liste or CEMAL; veri = veri if veri is not None else VERI
    import itertools
    S = []
    for esik, tol, band in itertools.product((0.55,0.65,0.75,0.85),(1,2,3),(0.35,0.5,0.75)):
        hatalar=[]; bul=0
        for s, cb, cs, _ in liste:
            k = s if s in veri else next((z for z in veri if z.split('.')[0]==s), None)
            if not k: continue
            df=veri[k]; x=df[df.index<=pd.Timestamp(cs)]
            if len(x)<250: continue
            try: r=col_segment(x, esik=esik, tolerans=tol, band_tol=band)
            except Exception: r=None
            if not r: continue
            bul+=1; hatalar.append(abs(_bar_fark(df, cb, r["bas_tarih"])))
        if hatalar:
            S.append({"esik":esik,"tolerans":tol,"band_tol":band,"bulundu":bul,
                      "ort_hata":round(float(np.mean(hatalar)),1),
                      "isabet5":int(sum(h<=5 for h in hatalar))})
    t=pd.DataFrame(S).sort_values(["bulundu","ort_hata"],ascending=[False,True])
    print("\n  EN IYI 10 AYAR (cok bulan + az hata):")
    print(t.head(10).to_string(index=False))
    print(f"\n  MEVCUT (0.65 / 2 / 0.35): ", end="")
    m=t[(t.esik==0.65)&(t.tolerans==2)&(t.band_tol==0.35)]
    print(m.to_string(index=False, header=False) if len(m) else "-")
    return t

print("[ok] kalibrasyon yuklendi")
print("  t = kalibrasyon()        <- kod vs Cemal, bar bar")
print("  p = parametre_tara()     <- hangi ayar en yakin (36 kombinasyon)")
