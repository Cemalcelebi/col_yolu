"""gemini_hakem — ÜÇÜNCÜ HAKEM: kör hakem sayfalarını Gemini'ye (görsel) etiketletir ve (sonuç varsa) puanlar.

Cemal (18 Kas 2026, 'Hakem turları'): iki taraf (Cemal + model) aynı kör sayfaları etiketler. Bu betik üçüncü, bağımsız
bir hakem ekler: Gemini, model etiketleyicinin kural metnini (C1-C13, VD, CD, tur güncellemeleri; AŞAMA C çıkarılmış)
sistem metni olarak alır, her sayfa için yalnız PNG'yi görür. Gemini'ye sonuç, anahtar, sembol, tarih ya da Cemal'in yanıtı
VERİLMEZ.

Kullanım (Colab'da ya da yerelde; anahtar koda yazılmaz, proxy / ortam sağlar):
    python gemini_hakem.py --no 5 --png-klasor .../tur5_png --cikti tur/5 --kurallar TUR5_MODEL_KURALLAR.md
    python gemini_hakem.py --no 4 --png-klasor .../tur4_png --cikti tur/4 --kurallar ... --cemal-sonrasi
    python gemini_hakem.py --no 4 --puan --cikti tur/4          # tur_4_satir.csv ile puan (bilgi) -> TUR_4_GEMINI.md

Anahtar: GEMINI_API_KEY ortam değişkeni varsa o kullanılır; yoksa 'proxy-injected' (ajan proxy'si gerçek anahtarı koyar).
Anahtar hiçbir dosyaya ve loga yazılmaz.
"""
from __future__ import annotations

_CK_ONCE_GMH = {k: id(v) for k, v in globals().items()}

import argparse
import base64
import hashlib
import json
import logging
import math
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Tuple

GMH_UC = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
GMH_MODEL = "gemini-3.8-flash"
GMH_BEKLE = 4.0          # her istek arası (s)
GMH_429_BEKLE = 20.0     # 429'da bekleme (s)
GMH_429_DENEME = 5       # 429'da en çok yeniden deneme
GMH_KARARLAR = ("OLUR", "OLMAZ", "BELİRSİZ")
GMH_ZAMAN_ASIMI = 600    # istek zaman aşımı (s); uç kuyrukta ~130-160 s bekletiyor (19 Kas ön test)
GMH_MAX_TOKEN = 2000     # düşünme tokenleri içeriği kesmesin (ana model ön testi: 120 -> finish_reason length)
GMH_DUSUNME = "low"      # reasoning_effort ('none' görselle hata listesi döndü, 'minimal' desteklenmiyor)
GMH_GENISLIK = 900       # görsel 900 px genişliğe küçültülür, JPEG kalite 80
GMH_PARALEL = 2          # eşzamanlı istek (başlangıçlar arası yine >= 4 s); 8 ile dakika kotası 429 fırtınası verdi
GMH_TALIMAT = ("Grafik sinyal gününde kesilmiştir, sonrası yok, hisse adı yok. Yalnız şu JSON'u döndür: "
               "{\"karar\": \"OLUR|OLMAZ|BELİRSİZ\", \"bolge\": \"DOĞRU|YANLIŞ\", \"nedenler\": [\"C2+\", ...], "
               "\"guven\": 1-5, \"not\": \"tek cümle Türkçe\"}. BELİRSİZ yalnız yapı yoksa.")

GMH_LOG = logging.getLogger("gemini_hakem")


def gmh_log_kur(yol: str) -> None:
    """Dosya + ekran logu (anahtar hiç loglanmaz)."""
    GMH_LOG.setLevel(logging.INFO)
    GMH_LOG.handlers.clear()
    bic = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    for h in (logging.FileHandler(yol, encoding="utf-8"), logging.StreamHandler(sys.stdout)):
        h.setFormatter(bic)
        GMH_LOG.addHandler(h)


def gmh_sistem_metni(kural_yolu: str) -> str:
    """Kural metni (AŞAMA C bölümü çıkarılmış) + talimat."""
    with open(kural_yolu, encoding="utf-8") as f:
        satirlar = f.read().splitlines()
    cikis: List[str] = []
    atla = False
    for s in satirlar:
        if s.startswith("## "):
            atla = "AŞAMA C" in s
        if not atla:
            cikis.append(s)
    metin = "\n".join(cikis).strip()
    if "AŞAMA C" in metin:
        raise RuntimeError("AŞAMA C bölümü çıkarılamadı")
    return metin + "\n\n" + GMH_TALIMAT


def gmh_json_ayristir(metin: str) -> Optional[Dict[str, Any]]:
    """Yanıttan JSON'u çıkarır (kod bloğu / fazlalık temizlenir) ve alanları denetler; olmazsa None."""
    if not metin:
        return None
    t = re.sub(r"```(?:json)?", "", metin).strip()
    i, j = t.find("{"), t.rfind("}")
    if i < 0 or j <= i:
        return None
    try:
        d = json.loads(t[i:j + 1])
    except json.JSONDecodeError:
        return None
    karar = str(d.get("karar", "")).strip().upper().replace("BELIRSIZ", "BELİRSİZ")
    if karar not in GMH_KARARLAR:
        return None
    bolge = str(d.get("bolge", "")).strip().upper().replace("DOGRU", "DOĞRU").replace("YANLIS", "YANLIŞ")
    ned = d.get("nedenler", [])
    if not isinstance(ned, list):
        ned = [str(ned)]
    try:
        guven = int(d.get("guven"))
    except (TypeError, ValueError):
        guven = None
    return {"karar": karar, "bolge": bolge if bolge in ("DOĞRU", "YANLIŞ") else "", "nedenler": [str(x) for x in ned],
            "guven": guven, "not": str(d.get("not", "")).strip()}


def gmh_gorsel_b64(yol: str) -> str:
    """PNG -> GMH_GENISLIK px genişlik, JPEG kalite 80, base64 (uç büyük görselde çok yavaş)."""
    import io
    from PIL import Image
    im = Image.open(yol).convert("RGB")
    if im.width > GMH_GENISLIK:
        im = im.resize((GMH_GENISLIK, round(im.height * GMH_GENISLIK / im.width)), Image.LANCZOS)
    tampon = io.BytesIO()
    im.save(tampon, "JPEG", quality=80)
    return base64.b64encode(tampon.getvalue()).decode("ascii")


class GmhIstemci:
    """OpenAI uyumlu uç; 429'da bekle-yeniden dene; istek ve 429 sayacı."""

    def __init__(self, model: str = GMH_MODEL):
        import requests  # yerel içe aktarma: puan kipi requests gerektirmez
        self._rq = requests
        self.model = model
        self.istek = 0
        self.n429 = 0
        self.hata = 0
        self._son = 0.0
        self._kilit = threading.Lock()
        anahtar = os.environ.get("GEMINI_API_KEY") or "proxy-injected"
        self._baslik = {"Authorization": f"Bearer {anahtar}", "Content-Type": "application/json"}

    def _say(self, alan: str) -> None:
        with self._kilit:
            setattr(self, alan, getattr(self, alan) + 1)

    def _sira_bekle(self) -> None:
        """İstek başlangıçları arasında en az GMH_BEKLE saniye (iş parçacıkları arasında ortak)."""
        with self._kilit:
            simdi = time.time()
            basla = max(simdi, self._son + GMH_BEKLE)
            self._son = basla
            self.istek += 1
        if basla > simdi:
            time.sleep(basla - simdi)

    def sor(self, sistem: str, png_b64: str) -> str:
        govde = {"model": self.model, "temperature": 0, "max_tokens": GMH_MAX_TOKEN, "reasoning_effort": GMH_DUSUNME,
                 "messages": [{"role": "system", "content": sistem},
                              {"role": "user", "content": [
                                  {"type": "text", "text": GMH_TALIMAT},
                                  {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + png_b64}}]}]}
        deneme = 0
        while True:
            self._sira_bekle()
            try:
                r = self._rq.post(GMH_UC, headers=self._baslik, json=govde, timeout=GMH_ZAMAN_ASIMI)
            except self._rq.RequestException as e:
                self._say("hata")
                deneme += 1
                GMH_LOG.warning("ağ hatası (%s), deneme %d", type(e).__name__, deneme)
                if deneme > GMH_429_DENEME:
                    raise
                time.sleep(GMH_429_BEKLE)
                continue
            if r.status_code == 429 and "PerDay" in r.text:
                self._say("n429")
                raise GmhGunlukKota(re.sub(r"\s+", " ", r.text)[:300])
            if r.status_code == 429 or r.status_code >= 500:
                self._say("n429" if r.status_code == 429 else "hata")
                deneme += 1
                GMH_LOG.warning("HTTP %d, %d. yeniden deneme %.0f s sonra", r.status_code, deneme, GMH_429_BEKLE)
                if deneme > GMH_429_DENEME:
                    raise RuntimeError(f"HTTP {r.status_code}: deneme sınırı aşıldı")
                time.sleep(GMH_429_BEKLE)
                continue
            if r.status_code != 200:
                self._say("hata")
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
            d = r.json()
            try:
                return d["choices"][0]["message"]["content"] or ""
            except (KeyError, IndexError, TypeError):
                self._say("hata")
                return ""


class GmhGunlukKota(RuntimeError):
    """Ücretsiz katman GÜNLÜK istek kotası doldu (429 RESOURCE_EXHAUSTED, PerDay): yeniden denemek kotayı yakar, durulur."""


def gmh_etiketle(no: int, png_klasor: str, cikti: str, kural_yolu: str, cemal_sonrasi: bool,
                 model: str = GMH_MODEL, paralel: int = GMH_PARALEL) -> Dict[str, Any]:
    """Her PNG için tek istek (ayrıştırılamazsa bir kez daha). Her sayfa bitince ara dosyaya yazılır
    (tur_K_gemini_kismi.json); yeniden koşuda biten sayfalar atlanır. Günlük kota dolarsa durur, ara dosya kalır.
    Son dosyalar (etiket + ham) yalnız bütün sayfalar etiketlenince yazılır."""
    sistem = gmh_sistem_metni(kural_yolu)
    sistem_sha = hashlib.sha256(sistem.encode("utf-8")).hexdigest()
    dosyalar = sorted((f for f in os.listdir(png_klasor) if re.fullmatch(r"No_\d+\.png", f)),
                      key=lambda f: int(re.findall(r"\d+", f)[0]))
    if not dosyalar:
        raise RuntimeError(f"PNG yok: {png_klasor}")
    os.makedirs(cikti, exist_ok=True)
    kismi_yol = os.path.join(cikti, f"tur_{no}_gemini_kismi.json")
    kismi: Dict[str, Any] = {"model": model, "sistem_sha256": sistem_sha, "etiket": {}, "ham": {}, "hatalar": [],
                             "istek": 0, "http_429": 0, "diger_hata": 0, "kosu": []}
    if os.path.exists(kismi_yol):
        with open(kismi_yol, encoding="utf-8") as fh:
            onceki = json.load(fh)
        if onceki.get("model") != model or onceki.get("sistem_sha256") != sistem_sha:
            raise RuntimeError("ara dosya başka model / sistem metniyle yazılmış; karıştırılmaz (dosyayı elle kaldır)")
        kismi = onceki
    kilit = threading.Lock()
    dur = threading.Event()

    def _kaydet() -> None:
        with open(kismi_yol + ".tmp", "w", encoding="utf-8") as fh:
            json.dump(kismi, fh, ensure_ascii=False, indent=1)
        os.replace(kismi_yol + ".tmp", kismi_yol)

    ist = GmhIstemci(model)
    kalan = [f for f in dosyalar if str(int(re.findall(r"\d+", f)[0])) not in kismi["etiket"]]
    GMH_LOG.info("tur %d: %d sayfa, %d hazır, %d kalan; model %s, paralel %d", no, len(dosyalar),
                 len(dosyalar) - len(kalan), len(kalan), model, paralel)

    def _sayfa(f: str) -> None:
        if dur.is_set():
            return
        k = str(int(re.findall(r"\d+", f)[0]))
        b64 = gmh_gorsel_b64(os.path.join(png_klasor, f))
        yanitlar: List[str] = []
        sonuc = None
        for tur in range(2):
            try:
                y = ist.sor(sistem, b64)
            except GmhGunlukKota as e:
                dur.set()
                with kilit:
                    kismi["hatalar"].append(f"No {k}: günlük kota doldu, durdu ({str(e)[:120]})")
                GMH_LOG.error("No %s: GÜNLÜK KOTA doldu, koşu durur", k)
                return
            except Exception as e:  # noqa: BLE001 — sayfa düzeyinde yakala, kayda geç
                y = ""
                with kilit:
                    kismi["hatalar"].append(f"No {k}: istek hatası {type(e).__name__}: {str(e)[:200]}")
                GMH_LOG.error("No %s istek hatası: %s", k, e)
            yanitlar.append(y)
            sonuc = gmh_json_ayristir(y)
            if sonuc is not None:
                break
            GMH_LOG.warning("No %s: yanıt ayrıştırılamadı (deneme %d)", k, tur + 1)
        if sonuc is None:
            if any(yanitlar):  # yanıt geldi ama JSON değil: kurala göre BELİRSİZ
                sonuc = {"karar": "BELİRSİZ", "bolge": "", "nedenler": [], "guven": None, "not": "ayrıştırılamadı"}
                with kilit:
                    kismi["hatalar"].append(f"No {k}: iki denemede ayrıştırılamadı -> BELİRSİZ")
            else:  # hiç yanıt yok (ağ / kota): sayfa boş kalır, sonraki koşuda yeniden denenir
                return
        with kilit:
            kismi["etiket"][k] = sonuc
            kismi["ham"][k] = yanitlar
            _kaydet()
        GMH_LOG.info("No %s -> %s (güven %s)", k, sonuc["karar"], sonuc["guven"])

    try:
        with ThreadPoolExecutor(max_workers=max(1, paralel)) as hav:
            list(hav.map(_sayfa, kalan))
    finally:
        with kilit:
            kismi["istek"] += ist.istek
            kismi["http_429"] += ist.n429
            kismi["diger_hata"] += ist.hata
            kismi["kosu"].append({"zaman_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "istek": ist.istek,
                                  "http_429": ist.n429, "diger_hata": ist.hata, "gunluk_kota": dur.is_set()})
            _kaydet()
    etiket = kismi["etiket"]
    eksik = [str(int(re.findall(r"\d+", f)[0])) for f in dosyalar if str(int(re.findall(r"\d+", f)[0])) not in etiket]
    sayim = {c: sum(1 for v in etiket.values() if v["karar"] == c) for c in GMH_KARARLAR}
    if eksik:
        GMH_LOG.warning("EKSİK %d sayfa %s; son dosya yazılmadı, ara dosya: %s", len(eksik), eksik, kismi_yol)
        return {"tamam": False, "eksik": eksik, "karar": sayim, "istek": kismi["istek"], "http_429": kismi["http_429"]}
    sirali = {k: etiket[k] for k in sorted(etiket, key=int)}
    meta = {"tur": no, "model": model, "zaman_utc": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "sistem_sha256": sistem_sha, "n": len(sirali), "karar": sayim,
            "istek": kismi["istek"], "http_429": kismi["http_429"], "diger_hata": kismi["diger_hata"],
            "hatalar": kismi["hatalar"], "kosu": kismi["kosu"],
            "gorsel": f"PNG -> {GMH_GENISLIK} px JPEG q80", "reasoning_effort": GMH_DUSUNME, "max_tokens": GMH_MAX_TOKEN,
            "girdi": "yalnız PNG (sembol / tarih / sonuç / Cemal yanıtı verilmedi)",
            "cemal_yanitindan_sonra": bool(cemal_sonrasi)}
    if cemal_sonrasi:
        meta["not_cemal"] = "Cemal'in yanıtı bu turda vardı ama Gemini'ye verilmedi; Gemini sonucu görmedi (bilgi etiketi)."
    cikti_d = {"surum": f"{model}, TUR{no} kuralları, temperature 0", "etiket": sirali, "meta": meta}
    with open(os.path.join(cikti, f"tur_{no}_gemini_etiket.json"), "w", encoding="utf-8") as fh:
        json.dump(cikti_d, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(cikti, f"tur_{no}_gemini_ham.json"), "w", encoding="utf-8") as fh:
        json.dump({"model": model, "sistem_metni": sistem, "yanit": {k: kismi["ham"][k] for k in sirali}},
                  fh, ensure_ascii=False, indent=1)
    os.remove(kismi_yol)
    GMH_LOG.info("bitti: %s; istek %d, 429 %d, hata %d", sayim, kismi["istek"], kismi["http_429"], kismi["diger_hata"])
    meta["tamam"] = True
    return meta


# ---------------------------------------------------------------- puan (bilgi)
def gmh_fisher(a: int, b: int, c: int, d: int) -> float:
    """İki yönlü Fisher p (2x2: [[a,b],[c,d]])."""
    try:
        from scipy.stats import fisher_exact
        return float(fisher_exact([[a, b], [c, d]])[1])
    except ImportError:
        n, r1, c1 = a + b + c + d, a + b, a + c
        def p(x):
            return math.comb(c1, x) * math.comb(n - c1, r1 - x) / math.comb(n, r1)
        p0 = p(a)
        return min(1.0, sum(p(x) for x in range(max(0, r1 + c1 - n), min(r1, c1) + 1) if p(x) <= p0 * (1 + 1e-9)))


def gmh_kappa(x: List[str], y: List[str]) -> float:
    n = len(x)
    if n == 0:
        return float("nan")
    po = sum(1 for a, b in zip(x, y) if a == b) / n
    sinif = set(x) | set(y)
    pe = sum((x.count(s) / n) * (y.count(s) / n) for s in sinif)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def gmh_puanla(kararlar: Dict[str, str], h5: Dict[str, float]) -> Dict[str, Any]:
    olur = [k for k, v in kararlar.items() if v == "OLUR" and not math.isnan(h5.get(k, float("nan")))]
    olmaz = [k for k, v in kararlar.items() if v == "OLMAZ" and not math.isnan(h5.get(k, float("nan")))]
    bel = sum(1 for v in kararlar.values() if v not in ("OLUR", "OLMAZ"))
    a = sum(1 for k in olur if h5[k] == 1); b = len(olur) - a
    c = sum(1 for k in olmaz if h5[k] == 1); d = len(olmaz) - c
    nk = len(olur) + len(olmaz)
    return {"OLUR": len(olur), "OLMAZ": len(olmaz), "BELİRSİZ": bel, "olur_dogru": a, "olmaz_dogru": d,
            "basari_pay": (a + d) / nk if nk else float("nan"), "basari_n": a + d, "karar_n": nk,
            "fisher_p": gmh_fisher(a, b, c, d) if nk else float("nan")}


def gmh_yuzde(x: float) -> str:
    return "—" if x is None or (isinstance(x, float) and math.isnan(x)) else f"%{x * 100:.1f}".replace(".", ",")


def gmh_puan(no: int, cikti: str) -> str:
    import csv
    with open(os.path.join(cikti, f"tur_{no}_gemini_etiket.json"), encoding="utf-8") as fh:
        gem = {k: v["karar"] for k, v in json.load(fh)["etiket"].items()}
    satir = list(csv.DictReader(open(os.path.join(cikti, f"tur_{no}_satir.csv"), encoding="utf-8")))
    h5 = {r["sayfa"]: (float(r["h5"]) if r["h5"] not in ("", "nan", "NaN") else float("nan")) for r in satir}
    taraf = {"Gemini": gem, "Cemal": {r["sayfa"]: r["cemal"] for r in satir}, "model": {r["sayfa"]: r["model"] for r in satir}}
    if set(gem) != set(h5):
        raise RuntimeError(f"sayfa kümeleri farklı: gemini {len(gem)}, satır {len(h5)}")
    gecerli = [v for v in h5.values() if not math.isnan(v)]
    hep_olmaz = sum(1 for v in gecerli if v == 0) / len(gecerli)
    P = {t: gmh_puanla(k, h5) for t, k in taraf.items()}
    s = [f"# HAKEM TURU {no} — GEMİNİ ÜÇÜNCÜ HAKEM PUANI (BİLGİ)", "",
         f"Gemini ({GMH_MODEL}, temperature 0) bu turu Cemal'in yanıtından SONRA etiketledi; Gemini'ye yalnız PNG ve model "
         "kural metni verildi (sonuç, anahtar, sembol, tarih, Cemal yanıtı yok). Bu yüzden puan BİLGİdir, mühürlü kör sonuç değildir.",
         "", "Karar ölçüsü (TUR_4_SONUC ile aynı): h5 = 15 geçerli barda +%5 kapanış, stop'tan önce. OLUR doğru = h5 1, "
         "OLMAZ doğru = h5 0, BELİRSİZ karar dışı. BAŞARI = (doğru OLUR + doğru OLMAZ) / karar sayısı. "
         "Fisher iki yönlü (karar x h5). Sayılar bu betikle tur_" + str(no) + "_satir.csv'den üretildi.", "",
         "| Taraf | OLUR / OLMAZ / BELİRSİZ | OLUR isabeti | OLMAZ doğruluğu | BAŞARI | Fisher p |",
         "|---|---|---|---|---|---|"]
    for t in ("Gemini", "Cemal", "model"):
        p = P[t]
        s.append(f"| {t} | {p['OLUR']} / {p['OLMAZ']} / {p['BELİRSİZ']} | {p['olur_dogru']} / {p['OLUR']} "
                 f"({gmh_yuzde(p['olur_dogru'] / p['OLUR'] if p['OLUR'] else float('nan'))}) | {p['olmaz_dogru']} / {p['OLMAZ']} "
                 f"({gmh_yuzde(p['olmaz_dogru'] / p['OLMAZ'] if p['OLMAZ'] else float('nan'))}) | **{gmh_yuzde(p['basari_pay'])}** "
                 f"({p['basari_n']} / {p['karar_n']}) | " + f"{p['fisher_p']:.3f}".replace(".", ",") + " |")
    s += ["", f"- 'Hep OLMAZ' tabanı (h5 = 0 payı, {len(gecerli)} sayfa): {gmh_yuzde(hep_olmaz)}.", ""]
    s += ["## Uyum (yalnız iki tarafın da OLUR / OLMAZ dediği sayfalar)", "", "| Çift | ortak sayfa | uyum oranı | kappa |", "|---|---|---|---|"]
    for a_, b_ in (("Cemal", "Gemini"), ("model", "Gemini"), ("Cemal", "model")):
        ks = [k for k in h5 if taraf[a_][k] in ("OLUR", "OLMAZ") and taraf[b_][k] in ("OLUR", "OLMAZ")]
        x = [taraf[a_][k] for k in ks]; y = [taraf[b_][k] for k in ks]
        uy = sum(1 for i, j in zip(x, y) if i == j) / len(ks) if ks else float("nan")
        kp = gmh_kappa(x, y)
        s.append(f"| {a_}-{b_} | {len(ks)} | {gmh_yuzde(uy)} | {'—' if math.isnan(kp) else f'{kp:.3f}'.replace('.', ',')} |")
    s += ["", "Not: n = 40 sayfa; tek tur küçük örneklemdir, 'bulgu' değildir. Cemal'in hedefi BAŞARI %80-90; taban ~%50 "
          "(bu turda 'hep OLMAZ' payı) olduğu için hedef zordur.", ""]
    metin = "\n".join(s)
    with open(os.path.join(cikti, f"TUR_{no}_GEMINI.md"), "w", encoding="utf-8") as fh:
        fh.write(metin)
    return metin


# ================================================================ ÇAKIŞMA KAPISI ve KOMUT
def _cakisma_kontrol_gmh(_once=_CK_ONCE_GMH, _dosya="gemini_hakem.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_GMH", "_CK_KAYIT", "_cakisma_kontrol_gmh", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "json", "logging", "time", "re", "math", "base64", "hashlib", "argparse", "annotations", "threading", "ThreadPoolExecutor",
           "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_gmh()


def gmh_ana(argv: Optional[List[str]] = None) -> None:
    ap = argparse.ArgumentParser(description="Gemini üçüncü hakem")
    ap.add_argument("--no", type=int, required=True, help="tur numarası")
    ap.add_argument("--png-klasor", help="No_1..N.png klasörü")
    ap.add_argument("--cikti", required=True, help="tur/K klasörü")
    ap.add_argument("--kurallar", help="TUR<K>_MODEL_KURALLAR.md")
    ap.add_argument("--cemal-sonrasi", action="store_true", help="Cemal yanıtı bu turda zaten var (bilgi etiketi)")
    ap.add_argument("--puan", action="store_true", help="tur_K_satir.csv ile puanla (bilgi)")
    ap.add_argument("--model", default=GMH_MODEL, help="Gemini model adı (/v1beta/openai/models)")
    ap.add_argument("--paralel", type=int, default=GMH_PARALEL, help="eşzamanlı istek sayısı")
    a = ap.parse_args(argv)
    os.makedirs(a.cikti, exist_ok=True)
    gmh_log_kur(os.path.join(a.cikti, f"tur_{a.no}_gemini.log"))
    if a.puan:
        print(gmh_puan(a.no, a.cikti))
        return
    if not (a.png_klasor and a.kurallar):
        ap.error("etiketleme için --png-klasor ve --kurallar gerekli")
    m = gmh_etiketle(a.no, a.png_klasor, a.cikti, a.kurallar, a.cemal_sonrasi, a.model, a.paralel)
    if not m.get("tamam"):
        sys.exit(3)


if __name__ == "__main__":
    gmh_ana()
