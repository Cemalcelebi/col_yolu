"""K57 denetim çıktılarının mekanik testi (CLAUDE.md: basit hatalar mekanik yakalanır).
1) K51-K56 değişmezliği: KAYNAK_MANIFEST.csv'deki dosyalar (açık çalışma EVREN2 hariç) sha256 ile aynı mı; K51-K56 yollarında git değişikliği yok mu.
2) TEST_ENVANTERI.csv: tekil kimlik, sınıf A-D, her satır bağımsız doğrulamadan geçmiş, hash sütunu manifestten.
3) VERI_KAYNAKLARI.csv: tekil kimlik, erişim testi değerleri izinli küme.
4) Kimlik atıfları: mekanizma / hipotez / açık soru / öneri dosyalarındaki test ve kaynak kimlikleri gerçek; K57_ATIF_DENETIMI.csv boş.
5) Durum dosyası: durum değerleri izinli küme, sayılar CSV ile aynı; çıktı yolu sınırı K57 klasörü dışına yazmayı reddeder.
Çalıştırma: python test_k57.py (depo kökünden)."""
import csv, hashlib, json, os, subprocess, sys

KOK = os.path.dirname(os.path.abspath(__file__)); K57 = os.path.join(KOK, "arastirma_cikti", "k57_denetim")
sys.path.insert(0, K57)
DURUMLAR = {"BEKLEMEDE", "DENETLENİYOR", "VERİ BEKLİYOR", "TESTE HAZIR", "DEVAM EDİYOR", "TAMAMLANDI", "REDDEDİLDİ", "YÖNTEMSEL OLARAK GEÇERSİZ"}
KORUNAN = ["COL_YOLU_ABD.py", "K55", "K55.py", "K56", "K56.py", "arastirma_cikti/col_yolu_abd", "arastirma_cikti/k55_dallanma", "arastirma_cikti/k56_mekanizma"]


def oku(ad):
    y = os.path.join(K57, ad)
    if not os.path.exists(y):
        return None
    with open(y, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def kimlikler(metin):
    return [k.strip() for k in str(metin or "").replace("|", ",").split(",") if k.strip()]


def testler():
    hata = []
    # 1) değişmezlik
    man = oku("KAYNAK_MANIFEST.csv") or []
    if len(man) < 300:
        hata.append(f"1) manifest kısa / yok ({len(man)})")
    degisen = []
    for r in man:
        if r.get("acik_calisma"):
            continue
        y = os.path.join(KOK, r["yol"])
        if not os.path.exists(y) or hashlib.sha256(open(y, "rb").read()).hexdigest() != r["sha256"]:
            degisen.append(r["yol"])
    if degisen:
        hata.append(f"1) K51-K56 dosyası değişmiş: {degisen[:8]}")
    g = subprocess.run(["git", "-C", KOK, "status", "--porcelain", "--", *KORUNAN], capture_output=True, text=True).stdout
    kirli = [l for l in g.splitlines() if l.strip() and "/evren_v2/" not in l]
    if kirli:
        hata.append(f"1) K51-K56 yollarında git değişikliği: {kirli[:5]}")
    # 2) test envanteri
    T = oku("TEST_ENVANTERI.csv") or []
    ids = [r["id"] for r in T]
    if len(T) < 100 or len(set(ids)) != len(ids):
        hata.append(f"2) test envanteri satır / kimlik sorunu ({len(T)}, tekil {len(set(ids))})")
    if any(r["sinif"] not in "ABCD" or len(r["sinif"]) != 1 for r in T):
        hata.append("2) sınıf A-D dışı")
    if any(r["dogrulama_durumu"].startswith("V1 YOK") or r["dogrulama_durumu"].startswith("V1 satırı yok") for r in T):
        hata.append("2) bağımsız doğrulamadan geçmemiş satır var")
    if any(not r["onkayit_kod_hash"] for r in T) or any(("sha" in r["onkayit_kod_hash"].lower() and ":" not in r["onkayit_kod_hash"]) for r in T):
        hata.append("2) hash sütunu boş ya da manifest biçiminde değil")
    if any(r["sinif"] != r["sinif_denetci"] and not r["sinif_hakem"] for r in T):
        hata.append("2) sınıf hakemsiz değişmiş")
    # 3) veri kaynakları
    V = oku("VERI_KAYNAKLARI.csv") or []
    vid = [r["kaynak_id"] for r in V]
    if len(V) < 40 or len(set(vid)) != len(vid):
        hata.append(f"3) veri kaynakları satır / kimlik sorunu ({len(V)})")
    if any(r["erisim_testi"] not in {"GEÇTİ", "KISMEN GEÇTİ", "BAŞARISIZ", "YAPILMADI"} for r in V):
        hata.append("3) erişim testi değeri izinli küme dışında")
    # 4) kimlik atıfları
    tid, kid = set(ids), set(vid)
    for ad, tsut, ksut in (("MEKANIZMA_SORULARI.csv", "ilgili_testler", "veri_kaynaklari"), ("HIPOTEZ_ENVANTERI.csv", "ilgili_test_idleri", "veri_kaynak_idleri"), ("HIPOTEZ_ENVANTERI_ONCEKI.csv", "ilgili_test_idleri", None)):
        X = oku(ad)
        if X is None:
            continue
        kotu = [k for r in X for k in kimlikler(r.get(tsut)) if k not in tid] + ([k for r in X for k in kimlikler(r.get(ksut)) if k not in kid] if ksut else [])
        if kotu:
            hata.append(f"4) {ad}: geçersiz kimlik {kotu[:5]}")
    A = oku("K57_ATIF_DENETIMI.csv")
    if A:
        hata.append(f"4) K57_ATIF_DENETIMI.csv boş değil: {len(A)} geçersiz atıf")
    acik = os.path.join(K57, "acik_sorular.json")
    if os.path.exists(acik):
        S = json.load(open(acik, encoding="utf-8"))["sorular"]
        kotu = [t for s in S for t in s["ilgili_testler"] if t not in tid]
        if len({s["id"] for s in S}) != len(S) or kotu:
            hata.append(f"4) açık sorular: kimlik tekrarı ya da geçersiz test {kotu[:5]}")
    # 5) durum dosyası ve hipotez envanteri
    H = oku("HIPOTEZ_ENVANTERI.csv")
    if H is not None:
        hid = [r["id"] for r in H]
        if len(set(hid)) != len(hid) or any(r["durum"] not in DURUMLAR for r in H):
            hata.append("5) hipotez envanteri: kimlik tekrarı ya da izinsiz durum")
        if any(r["kaynak"].startswith("YENİ") and r["durum"] not in {"BEKLEMEDE", "VERİ BEKLİYOR", "TESTE HAZIR"} for r in H):
            hata.append("5) yeni hipotez DEVAM EDİYOR / TAMAMLANDI olamaz (yeni test başlatılmadı)")
    dy = os.path.join(K57, "ARASTIRMA_DURUM.json")
    if os.path.exists(dy):
        D = json.load(open(dy, encoding="utf-8"))
        if H is not None and D.get("hipotez_sayisi") != len(H):
            hata.append("5) ARASTIRMA_DURUM hipotez sayısı CSV ile aynı değil")
        if D.get("test_sayisi") != len(T) or set(D.get("durum_sayilari", {})) - DURUMLAR:
            hata.append("5) ARASTIRMA_DURUM test sayısı / durum adları")
        if D.get("yeni_test_baslatildi") is not False:
            hata.append("5) ARASTIRMA_DURUM yeni_test_baslatildi False olmalı")
    try:
        import K57_envanter_birlestir as K
        K.cikti_yolu("../k56_mekanizma/x.csv"); hata.append("5) çıktı yolu sınırı K57 dışını reddetmedi")
    except ValueError:
        pass
    except ImportError as ex:
        hata.append(f"5) birleştirici içe aktarılamadı: {ex}")
    return hata


if __name__ == "__main__":
    h = testler()
    if h:
        print("HATA:"); [print(" -", x) for x in h]; sys.exit(1)
    print("test_k57: 5/5 OK")
