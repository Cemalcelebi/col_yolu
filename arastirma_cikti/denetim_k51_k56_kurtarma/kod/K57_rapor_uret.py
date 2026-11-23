"""K57 rapor üretici: iş akışı günlüklerindeki (journal.jsonl) mekanizma, alan, hipotez, açık soru, rapor ve öneri sonuçlarından okunabilir dosyaları üretir.
Yalnız günlükleri + bu klasördeki CSV'leri okur; yalnız bu klasöre yazar (K57_envanter_birlestir.cikti_yolu). Ajanların verdiği test ve veri kaynağı kimlikleri
TEST_ENVANTERI.csv / VERI_KAYNAKLARI.csv ile denetlenir; geçersizler K57_ATIF_DENETIMI.csv'ye yazılır ve ilgili satırlarda işaretlenir.
Kullanım: python K57_rapor_uret.py <bölüm> <journal.jsonl> [...]   bölüm: ham | mekanizma | alan | oncekihip | acik | rapor | oneri | durum"""
import csv, json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import K57_envanter_birlestir as K

ALAN_AD = {"A1": "Fiyat davranışı", "A2": "Hacim ve işlem akışı", "A3": "Volatilite ve risk rejimi", "A4": "Zaman ve süre davranışı", "A5": "Piyasa mikro yapısı",
           "A6": "Göreceli güç ve piyasa konumu", "A7": "Şirket temelleri", "A8": "Sahiplik, sermaye ve kurumsal olaylar", "A9": "Sektör, makroekonomi ve dış etkenler",
           "A10": "Birleşik davranışlar ve alanlar arası ilişkiler"}
DURUMLAR = ["BEKLEMEDE", "DENETLENİYOR", "VERİ BEKLİYOR", "TESTE HAZIR", "DEVAM EDİYOR", "TAMAMLANDI", "REDDEDİLDİ", "YÖNTEMSEL OLARAK GEÇERSİZ"]
BUGUN = "2026-11-02"


def oku_csv(ad):
    with open(os.path.join(K.CIKTI, ad), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def yaz(ad, metin):
    with open(K.cikti_yolu(ad), "w", encoding="utf-8") as fh:
        fh.write(metin if metin.endswith("\n") else metin + "\n")


def yaz_csv(ad, satirlar, sutunlar):
    with open(K.cikti_yolu(ad), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=sutunlar); w.writeheader()
        for r in satirlar:
            w.writerow({k: r.get(k, "") for k in sutunlar})


def kisalt(m, n=300):
    m = " ".join(str(m).split()); return m if len(m) <= n else m[: n - 1] + "…"


def ham_yaz(g):
    for k, v in g.items():
        with open(K.cikti_yolu(os.path.join("ham", k.replace(":", "_").replace("+", "_") + ".json")), "w", encoding="utf-8") as fh:
            json.dump(v, fh, ensure_ascii=False, indent=1)


class Kimlik:
    """Ajan çıktısındaki test / veri kaynağı kimliklerini doğrular; geçersizleri kaydeder."""
    def __init__(self):
        self.test = {r["id"] for r in oku_csv("TEST_ENVANTERI.csv")}; self.kaynak = {r["kaynak_id"] for r in oku_csv("VERI_KAYNAKLARI.csv")}; self.gecersiz = []

    def testler(self, ids, nerede):
        out = []
        for i in ids:
            if i in self.test: out.append(i)
            else: self.gecersiz.append((nerede, "test", i)); out.append(i + "[GEÇERSİZ KİMLİK]")
        return out

    def kaynaklar(self, ids, nerede):
        out = []
        for i in ids:
            if i in self.kaynak: out.append(i)
            else: self.gecersiz.append((nerede, "veri_kaynagi", i)); out.append(i + "[GEÇERSİZ KİMLİK]")
        return out


def atif_yaz(kim, ek=False):
    yol = os.path.join(K.CIKTI, "K57_ATIF_DENETIMI.csv"); eski = []
    if ek and os.path.exists(yol):
        eski = [(r["nerede"], r["tur"], r["kimlik"]) for r in oku_csv("K57_ATIF_DENETIMI.csv")]
    tum = eski + [x for x in kim.gecersiz if x not in eski]
    yaz_csv("K57_ATIF_DENETIMI.csv", [{"nerede": a, "tur": b, "kimlik": c} for a, b, c in tum], ["nerede", "tur", "kimlik"])
    return len(tum)


# ------------------------------------------------------------------ mekanizma soruları 4.1-4.6
def mekanizma(g):
    kim = Kimlik(); satirlar = []
    for k in sorted(x for x in g if x.startswith("mekanizma:")):
        for s in g[k]["sorular"]:
            satirlar.append({"soru_id": s["soru_id"], "soru": s["soru_metni"], "durum": s["kapsam_durumu"], "ilgili_testler": ", ".join(kim.testler(s["ilgili_testler"], s["soru_id"])),
                             "ilgili_k56_hipotezleri": ", ".join(s["ilgili_k56_hipotezleri"]), "neyi_cevapladi": s["neyi_cevapladi"], "neyi_cevaplayamadi": s["neyi_cevaplayamadi"],
                             "negatif_dislananlar": s["negatif_sonuc_dislananlar"], "negatif_dislanmayanlar": s["negatif_sonuc_dislanmayanlar"], "gerekli_dogrudan_veri": s["gerekli_dogrudan_veri"],
                             "veri_durumu": s["veri_durumu"], "veri_kaynaklari": ", ".join(kim.kaynaklar(s["veri_kaynak_idleri"], s["soru_id"])),
                             "kapsam_disi_onceki_calismalar": " | ".join(s["kapsam_disi_onceki_calismalar"]), "acik_sorular": " | ".join(s["acik_sorular"]), "kaynak_atiflari": " | ".join(s["kaynak_atiflari"])})
    yaz_csv("MEKANIZMA_SORULARI.csv", satirlar, list(satirlar[0].keys()))
    sayim = Counter(r["durum"] for r in satirlar)
    L = ["# MEKANİZMA SORULARI 4.1-4.6 — geçmiş testler ve yeterlilik", "",
         f"Soru düzeyinde durum: A geçerli ve yeterli test var; B geçerli fakat sınırlı; C yalnız yöntemsel olarak sorunlu test var; D veri yetersizliğiyle cevaplanamadı; E hiç test edilmemiş. Dağılım ({len(satirlar)} alt soru): " + ", ".join(f"{k} {v}" for k, v in sorted(sayim.items())) + ".",
         "Test kimlikleri TEST_ENVANTERI.csv'ye, veri kaynağı kimlikleri VERI_KAYNAKLARI.csv'ye bağlıdır. Ayrıntı sütunları MEKANIZMA_SORULARI.csv'dedir.", "",
         "| Soru | Durum | İlgili testler | Veri |", "|---|---|---|---|"]
    for r in satirlar:
        L.append(f"| {r['soru_id']} {kisalt(r['soru'], 90)} | {r['durum']} | {kisalt(r['ilgili_testler'], 70)} | {r['veri_durumu']} |")
    bas = None
    for r in satirlar:
        b = r["soru_id"].split("-")[0]
        if b != bas:
            L += ["", f"## {b}"]; bas = b
        L += ["", f"### {r['soru_id']} {r['soru']}  [{r['durum']}]", f"- Cevaplanan: {kisalt(r['neyi_cevapladi'], 520)}", f"- Cevaplanamayan: {kisalt(r['neyi_cevaplayamadi'], 520)}",
              f"- Negatif sonuç dışlıyor: {kisalt(r['negatif_dislananlar'], 380)}", f"- Negatif sonuç dışlamıyor: {kisalt(r['negatif_dislanmayanlar'], 380)}",
              f"- Gerekli doğrudan veri: {kisalt(r['gerekli_dogrudan_veri'], 380)} (durum: {r['veri_durumu']}; kaynaklar: {r['veri_kaynaklari'] or 'yok'})"]
        if r["kapsam_disi_onceki_calismalar"]:
            L.append(f"- K51 öncesi (kapsam dışı) ilgili çalışmalar: {kisalt(r['kapsam_disi_onceki_calismalar'], 260)}")
    yaz("MEKANIZMA_SORULARI.md", "\n".join(L)); return atif_yaz(kim), satirlar


# ------------------------------------------------------------------ alan haritası
def alan_sayimlari():
    d = oku_csv("TEST_ENVANTERI.csv"); out = {}
    for kod in ALAN_AD:
        ana = [r for r in d if r["alanlar"].split(",")[0] == kod]; her = [r for r in d if kod in r["alanlar"].split(",")]
        out[kod] = {"ana": Counter(r["sinif"] for r in ana), "her": Counter(r["sinif"] for r in her), "n_ana": len(ana), "n_her": len(her)}
    return out


def alan(g, mek_satirlari=None):
    kim = Kimlik(); sayim = alan_sayimlari(); bloklar = {}
    for k in sorted(x for x in g if x.startswith("alan:")):
        for a in g[k]["alanlar"]:
            bloklar[a["alan"].split(" ")[0]] = a
    L = ["# ARAŞTIRMA YOL HARİTASI — 10 ana alan (K51-K56 denetimi sonrası)", "",
         f"Sürüm K57-DENETIM-v1.0, {BUGUN}. Bu belge bir haritadır: sinyal ya da iz iddiası içermez, yeni test başlatmaz. Sayılar TEST_ENVANTERI.csv'den (137 test satırı; sınıf A geçerli ve yeterli, B geçerli fakat sınırlı, C yöntemsel sorunlu, D veri yetersiz) hesaplanır; metinler alan başına bağımsız bir ajanın kaynak okumasıdır.", "",
         "## Özet tablo (ana alanı o olan test sayısı; parantezde alanı ikincil olarak da içerenler dahil)", "", "| Alan | Test (ana / tümü) | A | B | C | D | Hiç yapılmayan (konu sayısı) |", "|---|---|---|---|---|---|---|"]
    for kod, ad in ALAN_AD.items():
        s = sayim[kod]; b = bloklar.get(kod)
        L.append(f"| {kod} {ad} | {s['n_ana']} ({s['n_her']}) | {s['ana'].get('A', 0)} | {s['ana'].get('B', 0)} | {s['ana'].get('C', 0)} | {s['ana'].get('D', 0)} | {len(b['hic_yapilmayan']) if b else '?'} |")
    for kod, ad in ALAN_AD.items():
        b = bloklar.get(kod)
        L += ["", f"## {kod} {ad}"]
        if not b:
            L.append("- Bu alan için ajan çıktısı yok."); continue
        L += [f"- Değerlendirme: {kisalt(b['alan_degerlendirmesi'], 700)}", "", "**Tamamlanan** (test, sınıf, güvenilirlik)"]
        for t in b["tamamlanan"][:14]:
            L.append(f"- {kim.testler([t['test_id']], kod)[0]} [{t['sinif']}] {kisalt(t['ne_yapildi'], 150)} — {kisalt(t['ne_kadar_guvenilir'], 150)}")
        if len(b["tamamlanan"]) > 14:
            L.append(f"- … ve {len(b['tamamlanan']) - 14} test daha (ayrıntı: ham/alan_*.json, TEST_ENVANTERI.csv)")
        L += ["", "**Eksik kalan**"] + [f"- {kisalt(e['konu'], 140)}: {kisalt(e['neden_eksik'], 220)} (testler: {', '.join(kim.testler(e['ilgili_testler'], kod)) or 'yok'}; gerekli veri: {kisalt(e['gerekli_veri'], 120)})" for e in b["eksik_kalan"]]
        L += ["", "**Hiç yapılmayan**"] + [f"- {kisalt(h['konu'], 140)}: {kisalt(h['neden_onemli'], 220)} (veri: {kisalt(h['veri_durumu'], 140)}; kaynaklar: {', '.join(kim.kaynaklar(h['veri_kaynak_idleri'], kod)) or 'yok'})" for h in b["hic_yapilmayan"]]
        L += ["", "**Açık sorular**"] + [f"- {kisalt(s, 220)}" for s in b["acik_sorular"]]
    if mek_satirlari:
        L += ["", "## Mekanizma soruları (4.1-4.6) durum özeti", "", "| Soru | Durum | Veri |", "|---|---|---|"] + [f"| {r['soru_id']} {kisalt(r['soru'], 80)} | {r['durum']} | {r['veri_durumu']} |" for r in mek_satirlari]
        L.append("\nAyrıntı: MEKANIZMA_SORULARI.md.")
    yaz("ARASTIRMA_YOL_HARITASI.md", "\n".join(L)); return atif_yaz(kim, ek=True), bloklar


# ------------------------------------------------------------------ önceki hipotezler
def oncekihip(g):
    kim = Kimlik(); satirlar = []
    for k in sorted(x for x in g if x.startswith("hipotez:")):
        for h in g[k]["hipotezler"]:
            if h["durum"] not in DURUMLAR: raise ValueError(h["durum"])
            satirlar.append({"id": h["id"], "ana_alan": h["ana_alan"], "hipotez": h["hipotez"], "kaynak": "ÖNCEKİ (K51-K56)", "onceki_ilgili_calismalar": " | ".join(h["onceki_ilgili_calismalar"]),
                             "onceki_test_sonucu": h["onceki_test_sonucu"], "test_gecerliligi": h["test_gecerliligi"], "ilgili_test_idleri": ", ".join(kim.testler(h["ilgili_test_idleri"], h["id"])),
                             "eksik_veri": h["eksik_veri"], "acik_kalan_soru": h["acik_kalan_soru"], "sonraki_islem": h["sonraki_islem"], "durum": h["durum"], "durum_gerekcesi": h["durum_gerekcesi"],
                             "kaynak_atiflari": " | ".join(h["kaynak_atiflari"])})
    ids = [r["id"] for r in satirlar]; kopya = [i for i, c in Counter(ids).items() if c > 1]
    yaz_csv("HIPOTEZ_ENVANTERI_ONCEKI.csv", satirlar, list(satirlar[0].keys())); return atif_yaz(kim, ek=True), len(satirlar), kopya


# ------------------------------------------------------------------ açık sorular
def acik(g):
    kim = Kimlik(); a = g["sentez:acik-sorular"]; t = g.get("sentez:tamlik"); S = a["sorular"]
    for s in S:
        s["ilgili_testler"] = kim.testler(s["ilgili_testler"], s["id"])
    with open(K.cikti_yolu("acik_sorular.json"), "w", encoding="utf-8") as fh:
        json.dump({"sorular": S, "birlestirme_notu": a["birlestirme_notu"], "tamlik_elestirmeni": t}, fh, ensure_ascii=False, indent=1)
    sira = {"YÜKSEK": 0, "ORTA": 1, "DÜŞÜK": 2}; S2 = sorted(S, key=lambda s: (sira[s["onem"]], s["id"]))
    L = ["# AÇIK SORULAR — önceki testlerin cevaplayamadığı sorular", "",
         f"Sürüm K57-DENETIM-v1.0, {BUGUN}. {len(S)} soru; önem: " + ", ".join(f"{k} {v}" for k, v in sorted(Counter(s['onem'] for s in S).items(), key=lambda x: sira[x[0]])) + ". Bunlar yalnız sorudur: hipotez, sinyal ya da çözüm değildir. Önem = mekanizmayı ayırt etme değeri + başka soruları kapatma gücü (gerekçesi her satırda).",
         "", "| ID | Önem | Kategori | Soru |", "|---|---|---|---|"] + [f"| {s['id']} | {s['onem']} | {s['kategori']} | {kisalt(s['soru'], 110)} |" for s in S2]
    for s in S2:
        L += ["", f"### {s['id']} [{s['onem']}] {s['soru']}", f"- Neden açık: {kisalt(s['neden_acik'], 500)}", f"- Kategori: {s['kategori']}; alanlar: {', '.join(s['alanlar'])}; mekanizma soruları: {', '.join(s['mekanizma_sorulari']) or '-'}",
              f"- İlgili testler: {', '.join(s['ilgili_testler']) or 'yok'}", f"- Gerekli veri: {kisalt(s['gerekli_veri'], 300)} (durum: {kisalt(s['veri_durumu'], 160)})", f"- Önem gerekçesi: {kisalt(s['onem_gerekcesi'], 300)}"]
    if t:
        L += ["", "## Tamlık eleştirmeninin bulguları (bağımsız okuyucu)", f"- {kisalt(t['genel_not'], 600)}"] + [f"- Eksik soru adayı: {kisalt(e['soru'], 200)} — {kisalt(e['neden_onemli'], 200)} ({kisalt(e['kaynak'], 100)})" for e in t["eksik_sorular"]] + [f"- Hatalı satır {h['id']}: {kisalt(h['sorun'], 250)}" for h in t["hatali_satirlar"]]
    yaz("ACIK_SORULAR.md", "\n".join(L)); return atif_yaz(kim, ek=True), len(S)


# ------------------------------------------------------------------ yöntemsel denetim raporu
def rapor(g):
    kim = Kimlik(); s = g["rapor:sentez"]; d = g.get("rapor:dogrulama"); T = oku_csv("TEST_ENVANTERI.csv")
    sayim = Counter(r["sinif"] for r in T); birim = defaultdict(Counter)
    for r in T: birim[r["calisma_birimi"]][r["sinif"]] += 1
    dz = {k["baslik"]: k for k in (d["kontrol"] if d else [])}
    L = ["# K51-K56 TEST ENVANTERİ VE YÖNTEMSEL DENETİM RAPORU", "",
         f"Sürüm K57-DENETIM-v1.0, {BUGUN}. Denetlenen: K51, K51 v1.2, K52, K53, K54, K55 (Faz 0 / Faz 1 / vekil), K56 (Faz 0, Faz 1 + BAĞIMSIZ, AYR / PBO / SIZ / EVREN2 hazırlığı). K51-K56 sonuçları, kodları ve ön kayıtları DEĞİŞTİRİLMEDİ (KAYNAK_MANIFEST.csv: 392 dosya, sha256).",
         "", "## Bir bakışta", "",
         f"- {len(T)} test satırı: A {sayim.get('A', 0)}, B {sayim.get('B', 0)}, C {sayim.get('C', 0)}, D {sayim.get('D', 0)}. (E = hiç test edilmemiş soru; soru düzeyinde: MEKANIZMA_SORULARI.md, ACIK_SORULAR.md.)",
         "- Her satır bağımsız bir doğrulayıcıyla (kaynak doğruluğu) ve ayrı bir eleştirel okuyucuyla (sınıf / mantık / eksiklik) sınandı; sınıf itirazlarında üçüncü okuyucu karar verdi. Doğrulayıcı, satırların büyük çoğunluğunda en az bir olgusal düzeltme yaptı (duzeltme_kaydi sütunu); düzeltmeler üzerine yazılmadı, eski ve yeni değer saklandı.",
         "- Yöntemsel kusur bulunması bir hipotezi doğru yapmaz; testin yapılmış olması da doğru yapıldığı anlamına gelmez. Aşağıdaki bulgular eski sonuçları değiştirmez, yalnız hangi yorumların yapılamayacağını sınırlar.", "",
         "| Birim | A | B | C | D | Toplam |", "|---|---|---|---|---|---|"] + [f"| {b} | {c.get('A', 0)} | {c.get('B', 0)} | {c.get('C', 0)} | {c.get('D', 0)} | {sum(c.values())} |" for b, c in sorted(birim.items())]
    L += ["", f"Birimler: K51A = K51 v1.0/v1.1 (ABD Çöl Yolu akademik + D1), K51B = K51 v1.2 bağımsız denetim, K52 = analist revizyonları, K53 = bilgi direnci, K54 = evren denetimi, K55 = dallanmalı OHLCV taraması, K56A = Faz 0, K56B = Faz 1 + BAĞIMSIZ, K56C = AYR / PBO / SIZ / EVREN2.", "",
          "## Sınıf dağılımı yorumu", "", kisalt(s["sinif_dagilimi_yorumu"], 1400), "", "## Ana yöntemsel bulgular (şiddete göre)"]
    for i, b in enumerate(s["yontemsel_ana_bulgular"], 1):
        ids = kim.testler(b["etkilenen_testler"], f"rapor-bulgu-{i}"); dk = dz.get(b["baslik"])
        L += ["", f"### {i}. [{b['siddet']}] {b['baslik']}", f"{kisalt(b['aciklama'], 900)}", f"- Etkilenen testler ({len(ids)}): {', '.join(ids[:14])}{' …' if len(ids) > 14 else ''}",
              f"- Etki yönü: {kisalt(b['etki_yonu'], 360)}", f"- Eski sonuçlara etkisi: {kisalt(b['eski_sonuclara_etkisi'], 360)}", f"- Kanıt: {kisalt(b['kanit'], 360)}"]
        if dk and dk["durum"] != "DOĞRU":
            L.append(f"- Bağımsız doğrulama notu ({dk['durum']}): {kisalt(dk['sorun'], 300)} → {kisalt(dk['duzeltme'], 300)}")
    L += ["", "## Güvenilebilecek dar dayanaklar (A / B sınıfı testlerin gerçekten desteklediği)"] + [f"- {kisalt(x['dayanak'], 260)} ({', '.join(kim.testler(x['testler'], 'rapor-dayanak')[:8])}). Sınır: {kisalt(x['sinir'], 260)}" for x in s["guvenilir_dayanaklar"]]
    L += ["", "## Güvenilmemesi gereken yorumlar"] + [f"- {kisalt(x['iddia'], 240)} ({', '.join(kim.testler(x['testler'], 'rapor-guvenilmez')[:8])}): {kisalt(x['neden'], 300)}" for x in s["guvenilmemesi_gerekenler"]]
    L += ["", "## Negatif sonuçların genel sınırı", "", kisalt(s["negatif_sonuclarin_genel_siniri"], 1400), "", "## Sonraki her araştırma kartı için zorunlu tasarım ilkeleri (bulgulardan)"] + [f"{i}. {kisalt(x, 380)}" for i, x in enumerate(s["zorunlu_tasarim_ilkeleri"], 1)]
    L += ["", "## Bu denetimin sınırları"] + [f"- {kisalt(x, 360)}" for x in s["sinirlamalar"]]
    if d:
        L += ["", "## Rapor bulgularının bağımsız doğrulaması", f"- {kisalt(d['genel_not'], 500)}"] + ([f"- Geçersiz kimlik: {', '.join(d['gecersiz_kimlikler'])}"] if d["gecersiz_kimlikler"] else [])
    L += ["", "## Test listesi (özet; ayrıntı TEST_ENVANTERI.csv)", "", "| ID | Test | Sınıf | Alan |", "|---|---|---|---|"] + [f"| {r['id']} | {kisalt(r['ad'], 85)} | {r['sinif']} | {r['alanlar'].split(',')[0]} |" for r in T]
    yaz("K57_DENETIM_RAPORU.md", "\n".join(L)); return atif_yaz(kim, ek=True)


def main(bolum, yollar):
    g = K.gunluk_oku(yollar)
    if bolum == "ham": ham_yaz(g); print(len(g), "ham dosya"); return
    ham_yaz(g)
    if bolum == "mekanizma": print("geçersiz kimlik toplamı:", mekanizma(g)[0])
    elif bolum == "alan":
        mek = oku_csv("MEKANIZMA_SORULARI.csv") if os.path.exists(os.path.join(K.CIKTI, "MEKANIZMA_SORULARI.csv")) else None
        print("geçersiz kimlik toplamı:", alan(g, [dict(r, durum=r["durum"]) for r in mek] if mek else None)[0])
    elif bolum == "oncekihip": print(oncekihip(g))
    elif bolum == "acik": print(acik(g))
    elif bolum == "rapor": print("geçersiz kimlik toplamı:", rapor(g))
    else: raise SystemExit(__doc__)


if __name__ == "__main__":
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2:])
