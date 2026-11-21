"""K57 veri kaynakları birleştirici: iş akışı günlüğünden (iki envanter ajanı + doğrulayıcı) VERI_KAYNAKLARI.csv üretir. Yalnız okur, yalnız bu klasöre yazar.
Doğrulayıcı düzeltmeleri eski değerle birlikte dogrulayici_notlari sütununa yazılır (eski değer silinmez); doğrulayıcının eklediği kaynaklar kaynak_durumu ile ayrılır."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import K57_envanter_birlestir as K

SUT = ["kaynak_id", "ad", "tur", "alanlar", "kapsam", "point_in_time", "gecikme_ve_sinirlar", "hayatta_kalma_delist_kapsami", "maliyet_lisans", "projede_kullanildi", "erisim_testi",
       "erisim_testi_kaniti", "yerel_kopya", "olcebilen", "olcemeyen", "kaynak_atiflari", "kaynak_durumu", "dogrulayici_notlari"]


def main(journal):
    g = K.gunluk_oku([journal]); a, b, v = g["veri:fiyat-hacim-makro"], g["veri:temel-sahiplik-olay"], g["veri:dogrulama"]
    for k, x in g.items():
        with open(K.cikti_yolu(os.path.join("ham", k.replace(":", "_") + ".json")), "w", encoding="utf-8") as fh:
            json.dump(x, fh, ensure_ascii=False, indent=1)
    satir = {}; sira = []
    for r in a["satirlar"] + b["satirlar"]:
        r = dict(r, alanlar=",".join(r["alanlar"]), kaynak_atiflari=" | ".join(r["kaynak_atiflari"]), kaynak_durumu="ENVANTER AJANI", dogrulayici_notlari="")
        if r["kaynak_id"] in satir:                                   # iki ajan aynı kaynağı yazdıysa ikisi de korunur
            o = satir[r["kaynak_id"]]
            for k in ("kapsam", "point_in_time", "gecikme_ve_sinirlar", "hayatta_kalma_delist_kapsami", "projede_kullanildi", "erisim_testi_kaniti", "olcebilen", "olcemeyen"):
                if r[k] and r[k] != o[k]:
                    o[k] = f"{o[k]} || [2. ajan] {r[k]}"
            o["kaynak_atiflari"] += " | " + r["kaynak_atiflari"]; o["kaynak_durumu"] = "ENVANTER AJANI (iki ajan da yazdı)"
            continue
        satir[r["kaynak_id"]] = r; sira.append(r["kaynak_id"])
    for d in v["duzeltmeler"]:
        r = satir.get(d["kaynak_id"]); alan = d["alan"].split(" (")[0].split(" /")[0].strip()
        if r is None:
            continue
        if alan in r and alan not in ("kaynak_id", "ad"):
            eski = r[alan]; r["dogrulayici_notlari"] += f"[{alan}] eski: {eski[:160]} -> doğrulayıcı: {d['dogru_deger'][:300]} (kanıt: {d['kanit'][:160]}) || "
            r[alan] = d["dogru_deger"] if alan != "erisim_testi" else r[alan]    # erişim_testi serbest metin değil: yalnız not düşülür
        else:
            r["dogrulayici_notlari"] += f"[{d['alan']}] {d['dogru_deger'][:300]} (kanıt: {d['kanit'][:160]}) || "
    for r in v["eksik_kaynaklar"]:
        r = dict(r, alanlar=",".join(r["alanlar"]), kaynak_atiflari=" | ".join(r["kaynak_atiflari"]), kaynak_durumu="DOĞRULAYICI EKLEDİ (envanterde yoktu; erişim testi K56'da yapılmadıysa YAPILMADI)", dogrulayici_notlari="")
        if r["kaynak_id"] not in satir:
            satir[r["kaynak_id"]] = r; sira.append(r["kaynak_id"])
    with open(K.cikti_yolu("VERI_KAYNAKLARI.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=SUT); w.writeheader(); [w.writerow({k: satir[i].get(k, "") for k in SUT}) for i in sira]
    with open(K.cikti_yolu("VERI_BOSLUKLARI.json"), "w", encoding="utf-8") as fh:
        json.dump({"alan_bosluklari_fiyat_hacim_makro": a["alan_bosluklari"], "alan_bosluklari_temel_sahiplik_olay": b["alan_bosluklari"], "kanitlanamayan_iddialar": v["kanitlanamayan"], "dogrulayici_genel_not": v["genel_not"],
                   "notlar_1": a["notlar"], "notlar_2": b["notlar"]}, fh, ensure_ascii=False, indent=1)
    print(len(sira), "kaynak satırı ->", "VERI_KAYNAKLARI.csv")


if __name__ == "__main__":
    main(sys.argv[1])
