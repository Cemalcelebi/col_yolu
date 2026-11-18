"""tur_ders_pdf — HAKEM TURU DERS PDF'i (18 Kas 2026; iş tanımı TUR_DERS_PDF_IS_TANIMI.md, düzen HAKEM_DERS_PDF_IS_TANIMI.md).

Genel betik: `--no N` ile tur N'nin ders PDF'i. Cemal'in el yazısıyla işaretlediği TUR_N_KOR.pdf'in her sayfası (pdftoppm 110 dpi)
sol yarıya, AYNI olayın SONRASI AÇIK grafiği (sinyal öncesi 60 bar + giriş + 20 bar; +%5 / +%10 / stop0 / çıkış; hacim) sağ yarıya
konur; başlıkta Cemal / model kararı, sonuç ve puan; altta Cemal'in notu, modelin nedenleri (açılımıyla) + notu ve DERS kutusu
(Cemal yanıldıysa kırmızı, doğruysa yeşil, karar yoksa gri; model için ayrı küçük etiket).
Kapak: tur puan tablosu (tur_N_sonuc.json = TUR_N_SONUC.md), taban, hep-OLMAZ karşılaştırması, bu turun dersleri, birikimli tablo
(hakem seti + tur 1..N). Son sayfa: özet tablo.

YENİ ÖLÇÜ YOK: sonuç sütunları olay_Y1.csv.gz (h5, h10, st5, k5, kst, getiri, cikis_bar, cikis_tur, es_h5) ve tur_N_satir.csv'den
okunur; ikisi karşılaştırılır, tutmazsa betik durur. Tur puanı tur_N_sonuc.json'daki sayılarla karşılaştırılır, tutmazsa durur.
Grafik çizimi hakem_ders_pdf.hd_grafik ile aynıdır (ortak kod; t'de kesik veriden hat / tavan, olay dosyasıyla eşitlik kapısı).
Kimlik zinciri: tur_N_anahtar.json sayfa -> (pazar, sembol, tarih) -> olay_Y1 satırı. HİSSE ADI / TARİH PDF'E GİRMEZ.

Kullanım:  OC_VERI=/tmp/veri python arastirma_cikti/goz_etiket/tur_ders_pdf.py --no 1 --cemal-pdf YOL [--cikti PDF] [--is KLASOR]
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_TD = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

TD_KLASOR = os.path.dirname(os.path.abspath(__file__))
TD_KOK = os.path.abspath(os.path.join(TD_KLASOR, "..", ".."))
for _p in (TD_KOK, TD_KLASOR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import GOZ_ETIKET as GE  # noqa: E402  (yalnız okunur)
import hakem_ders_pdf as HD  # noqa: E402  (ortak grafik / puan / kırpma; yalnız okunur)

tdlog = logging.getLogger("col.tur_ders")
if not tdlog.handlers:
    _h = logging.StreamHandler(sys.stderr)
    _h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s tur_ders: %(message)s", "%H:%M:%S"))
    tdlog.addHandler(_h)
    tdlog.setLevel(logging.INFO)
    tdlog.propagate = False


class TDHata(RuntimeError):
    """tur_ders_pdf hatası: durur, yarım PDF yazılmaz."""


TD_AYAR = {"dpi_sayfa": 110, "azami_mb": 12.0, "sonra": 20}


def td_yol(no: int) -> Dict[str, str]:
    k = os.path.join(TD_KLASOR, "tur", str(no))
    return {"klasor": k, "notlar": os.path.join(k, f"tur_{no}_cemal_notlar.json"), "model": os.path.join(k, f"tur_{no}_model_etiket.json"),
            "anahtar": os.path.join(k, f"tur_{no}_anahtar.json"), "satir": os.path.join(k, f"tur_{no}_satir.csv"),
            "sonuc": os.path.join(k, f"tur_{no}_sonuc.json"), "cikti": os.path.join(k, f"TUR_{no}_DERS.pdf"),
            "dersler": os.path.join(TD_KLASOR, "HAKEM_DERSLER.md"), "olay": HD.HD_YOL["olay"], "veri": os.environ.get("OC_VERI", "/tmp/veri")}


# ================================================================ TUR DERSLERİ (HAKEM_DERSLER.md '# TUR N' bölümünden; kısaltılmış)
# Her kod md'nin ilgili TUR bölümünde geçmek zorundadır (kapı). Sayfa eşlemesi md'deki sayfa listeleridir.
TD_DERS: Dict[int, Dict[str, Any]] = {
    1: {
        "metin": {
            "CD2": "(tekrar) 'Tepede raf OLUR değil' dersi 2. kez yanılttı: yükseliş sonrası tepe rafında OLUR dedin, +%5 gelmedi (10, 12, 22, 28).",
            "CD3": "(tekrar) Dipte kazan + ✓ ama stop (1, 23): kazanın sağ kenarı dönmeden (dönüş görülmeden) giriş; kendi D4 kuralın.",
            "CD8": "'Kodun bölgesi yanlış' hükmü ile 'fiyat gitmez' hükmü ayrı şeyler. Kodu eleştirmekte haklıydın (gerçek alış mumu daha önceki "
                   "kazanda, kodun bölgesi yol almış raf), ama ölçü kodun girişine göre ve 17 / 26 / 30 +%5 gördü. Sonraki turda iki soru: "
                   "(a) kodun bölgesi doğru mu, (b) bu mumdan girilir mi.",
            "CD9": "Şemsiye çizimi (9, 11) bu turda hedefe engel olmadı: 'şemsiye = OLMAZ' tek başına yetmiyor; bağlam (yükselen büyük resim) "
                   "ve kırılım gövdesi birlikte okunmalı.",
            "VD6": "'Dipte kazan + kırılım' tanımı 7 OLUR'un 4'ünde yanıldı (20-23): dönüş teyidi (D4) ve kırılım mumunun tavanı ortalaması eklenmeli.",
            "VD7": "'Tepede raf = OLMAZ' kuralı yükselen trend raflarını eledi, +%5 geldi (tepe rafı 7 / 12 hedefe gitti). Düşüş sonrası tepe "
                   "(dağıtım) = OLMAZ; yükselen trend içinde raf = bağlam lehte (C6+).",
            "VD8": "(Cemal s2) Alış mumu tavan çizgisini TAM ORTADAN kesmeli (gövdenin yarısı tavanın altında, yarısı üstünde); tavana ancak "
                   "değen ya da tamamen üstünde açılan mum zayıf. TUR 2 model kuralı.",
        },
        "cemal": {10: "CD2", 12: "CD2", 22: "CD2", 28: "CD2", 1: "CD3", 23: "CD3", 9: "CD9", 11: "CD9", 17: "CD8", 19: "CD8", 26: "CD8", 30: "CD8"},
        "model": {**{s: "VD7" for s in (3, 4, 5, 6, 7, 8, 9, 11, 17, 26, 29, 30)}, **{s: "VD6" for s in (20, 21, 22, 23)}, 2: "VD8"},
        "yeni": ("CD8", "CD9", "VD6", "VD7", "VD8"),
        "tekrar": ("CD2", "CD3"),
    },
    2: {
        "metin": {
            "CD2": "(tekrar, 3. kez; kendi C6 kuralın) Alçalan büyük resimde (alçalan tepeler kanalı) dipte kazan + ✓ dedin, stop oldu "
                   "(10, 15, 30). Büyük resim aşağıyken dipteki kazan OLUR değil; önce alçalan tepeler kırılmalı.",
            "CD3": "(tekrar) Kazan + ✓ ama kırılımdan hemen sonra geri döndü, stop (4, 16, 20, 26): kazanın sağ kenarı dönüşü (D4) görülmeden giriş.",
            "CD12": "(hakem setinden; artık yazılı) Önceki tepe aşılmadan giriş yok: 16, 20, 26'da önceki tepe aşılmamıştı, üçü de stop.",
            "CD13": "(yeni) 'Alıcı mumu büyük, yolun çoğunu almış, girmem' (s2) -> +%5 geldi (takip stoplu +%12,9). Büyük kırılım mumu tek başına "
                    "eleme nedeni değil; modelin VD8 kuralıyla (mum tavanı ortalamalı) çelişiyor, ikisi birlikte sınanacak.",
            "CD9": "(TUR 1 dersinin benzeri) Çizgi / X tek başına yetmez: alçalan trend çizgisi (14) ve X (27) ile OLMAZ dedin, ikisi de +%5 gördü "
                   "(14 +%10 da). Çizginin yanında kırılım mumu ve dip savunması birlikte okunmalı.",
            "CD11": "(sınıf: sönük) OLUR dedin, stop olmadı ama 15 günde +%5 de gelmedi (5, 8, 28). Yön yanlış değil, hedef gelmedi; puan ölçüsü "
                    "değişmez (kapanışla +%5).",
            "CD14": "(yeni) BELİRSİZ 11 / 30: kararsızlık arttı. BELİRSİZ dediğin 11 sayfanın 4'ü hedefe gitti (12, 13, 18, 21): puan değil ama "
                    "fırsat kaybı. TUR 3'te BELİRSİZ en çok 5 sayfa.",
            "VD9": "(yeni) TUR 1 dersleri uygulanınca (tepe rafı artık OLMAZ değil, C11 / C5 gevşedi) model OLUR'u 7'den 21'e çıktı, isabet %48 = taban; "
                   "OLUR seçiciliği kayboldu (11 OLUR gelmedi, 7'si stop). TUR 3: OLUR için en az iki lehte yapı (dönüş + gövdeli kırılım + "
                   "büyük resim yükselen / yatay); C13- (dev mum) varsa OLUR yok.",
            "VD7": "(tekrar, bağlam tek başına) Alçalan kanal + kırılım yakın tavanı geçemedi diye OLMAZ; +%5 ve +%10 geldi.",
            "VD6": "(tekrar, kırılım mumu tanımı) Kırılım mumu tavanın tamamen üstünde boşluklu açıldı ve yapı kısa diye OLMAZ; +%5 geldi "
                   "(takip stoplu +%28). Kırılım mumu şartı tek başına eleme nedeni değil (CD13 ile aynı soru).",
        },
        "cemal": {**{s: "CD2" for s in (10, 15, 30)}, 4: "CD3", **{s: ("CD12", "CD3") for s in (16, 20, 26)}, 2: "CD13",
                  14: "CD9", 27: "CD9", **{s: "CD11" for s in (5, 8, 28)}, **{s: "CD14" for s in (12, 13, 18, 21)}},
        "model": {**{s: "VD9" for s in (4, 7, 8, 9, 16, 17, 20, 24, 25, 26, 29)}, 14: "VD7", 23: "VD6"},
        "yeni": ("CD13", "CD14", "VD9"),
        "tekrar": ("CD2", "CD3", "CD12", "CD9", "CD11", "VD6", "VD7"),
        "tekrar_baslik": "TEKRAR EDEN (hakem seti ve TUR 1'den)",
        "yanlis_kod": ("VD6", "VD7", "VD9"),
        "cemal_yanlis_kod": ("CD2", "CD3", "CD12", "CD13", "CD9", "CD11"),
        "kapak_sonuc": ("Sonuç: model tabanın biraz üstünde, sen tabanın altında. Sen {ck} kararda {cb}, model {mk} kararda {mb}; taban {tb}; "
                        "hepsine OLMAZ deseydin {ho} olurdu (sayfaların {sh}'ı +%5 gördü). Uyum (kappa) {ka}. Fisher p sen {cp} / model {mp}. "
                        "Senin OLUR'larının 7'si stop; 11 BELİRSİZ. Hedef %80-90; taban ~%40 olduğu için zor. n küçük; dersler SINANMADI, kural değil."),
    },
}


# ================================================================ VERİ
def _td_json(yol: str) -> Dict[str, Any]:
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as ex:
        raise TDHata(f"okunamadı: {yol}: {ex}") from ex


def _td_md_bolum(md: str, no: int) -> str:
    m = re.search(rf"^# TUR {no} .*?(?=^# TUR {no + 1} |\Z)", md, flags=re.S | re.M)
    if not m:
        raise TDHata(f"HAKEM_DERSLER.md'de '# TUR {no}' bölümü yok")
    return m.group(0)


def td_tablo(no: int) -> pd.DataFrame:
    """Tur sayfaları: kimlik + Cemal / model kararı + olay_Y1 sonuç sütunları + puanlar + ders kodları. Kaynaklar arası eşitlik kapıları."""
    Y_ = td_yol(no)
    if no not in TD_DERS:
        raise TDHata(f"tur {no} için ders eşlemesi (TD_DERS) yazılmamış")
    D = TD_DERS[no]
    md = open(Y_["dersler"], encoding="utf-8").read()
    bolum = _td_md_bolum(md, no)
    for k in D["metin"]:
        # tur 1: bütün kodlar TUR 1 bölümünde; tur >= 2: yeni kodlar TUR N bölümünde, tekrar eden kodlar md'nin herhangi bir yerinde
        if k not in (bolum if (no == 1 or k in D["yeni"]) else md):
            raise TDHata(f"ders kodu {k} HAKEM_DERSLER.md{f' TUR {no} bölümünde' if (no == 1 or k in D['yeni']) else ''} yok")
    for kim in ("cemal", "model"):
        for s, kk in D[kim].items():
            for k in ((kk,) if isinstance(kk, str) else kk):
                if k not in D["metin"]:
                    raise TDHata(f"sayfa {s}: ders kodu {k} metinde yok")
    C = _td_json(Y_["notlar"])["cevap"]; M = _td_json(Y_["model"])["etiket"]; A = _td_json(Y_["anahtar"])["sayfa"]
    S = pd.read_csv(Y_["satir"], dtype={"tarih": str, "giris": str}).set_index("sayfa")
    Y = pd.read_csv(Y_["olay"], dtype={"tarih": str, "giris": str}).set_index(["pazar", "sembol", "tarih"])
    if not Y.index.is_unique:
        raise TDHata("olay_Y1 (pazar, sembol, tarih) tekil değil")
    sat = []
    for s in range(1, len(A) + 1):
        a = A[str(s)]; c = C.get(str(s)); m = M.get(str(s))
        if c is None or m is None:
            raise TDHata(f"sayfa {s}: Cemal ya da model kaydı yok")
        if "cevap" not in c:  # tur >= 2 yanıt biçimi: A (kodun bölgesi doğru mu) / B (bu mumdan girilir mi = karar)
            if "B" not in c:
                raise TDHata(f"sayfa {s}: Cemal kaydında karar (cevap / B) yok")
            c = {**c, "cevap": c["B"]}
        key = (a["pazar"], a["sembol"], a["tarih"])
        if key not in Y.index:
            raise TDHata(f"sayfa {s}: olay_Y1 satırı yok")
        r = Y.loc[key]; sr = S.loc[s]
        if (sr.sembol, sr.pazar, sr.tarih) != (a["sembol"], a["pazar"], a["tarih"]):
            raise TDHata(f"sayfa {s}: satır dosyası anahtarla tutmadı")
        if sr.cemal != c["cevap"] or sr.model != m["karar"]:
            raise TDHata(f"sayfa {s}: satır dosyasındaki kararlar json'larla tutmadı")
        if not bool(r["olc"]):
            raise TDHata(f"sayfa {s}: olay 15 barda ölçülebilir değil")
        for k in ("h5", "h10", "st5", "es_h5", "getiri"):
            if abs(float(r[k]) - float(sr[k])) > 1e-5:
                raise TDHata(f"sayfa {s}: {k} olay_Y1 ile satır dosyası arasında tutmadı")
        h5 = float(r["h5"]); cemal = c["cevap"]; model = m["karar"]
        sat.append({"sayfa": s, "pazar": a["pazar"], "sembol": a["sembol"], "tarih": a["tarih"], "giris": a["giris"], "donem": a["donem"],
                    "parmak": int(a.get("parmak", 0)), "cemal": cemal, "cemal_tur": c.get("tur", ""), "cemal_not": c.get("not", ""),
                    "model": model, "nedenler": list(m.get("nedenler", [])), "model_not": m.get("not", ""), "guven": m.get("guven", ""),
                    "h5": h5, "h10": float(r["h10"]), "st5": float(r["st5"]), "k5": int(r["k5"]), "kst": int(r["kst"]),
                    "getiri": float(r["getiri"]), "cikis_bar": int(r["cikis_bar"]), "cikis_tur": str(r["cikis_tur"]), "es_h5": float(r["es_h5"]),
                    "hat": float(r["hat"]), "tavan": float(r["tavan"]), "stop0": float(r["stop0"]), "E0": float(r["E0"]),
                    "puan_c": HD.hd_puan(cemal, h5), "puan_m": HD.hd_puan(model, h5),
                    "cd": _td_kod(D["cemal"].get(s, "")), "vd": _td_kod(D["model"].get(s, ""))})
    T = pd.DataFrame(sat)
    # ders eşlemesi tutarlılığı: Cemal'in kırmızı (yanlış) sayfası ders kodsuz kalabilir (md eşlemiyorsa), ama kodlu yanlış sayfa yanlış olmalı
    for kim, pk, yk, vars_ in (("model", "puan_m", "yanlis_kod", ("VD6", "VD7")), ("cemal", "puan_c", "cemal_yanlis_kod", ())):
        for s, kk in D[kim].items():
            for k in ((kk,) if isinstance(kk, str) else kk):
                if k in D.get(yk, vars_) and int(T.loc[T.sayfa == s, pk].iloc[0]) != -1:
                    raise TDHata(f"sayfa {s}: {k} {kim} yanıldığı sayfa olarak eşlenmiş ama {kim} yanılmamış")
    return T


def _td_kod(kk: Any) -> str:
    """Ders eşlemesi tek kod ya da kod demeti; tabloda boşlukla birleşik dize."""
    return kk if isinstance(kk, str) else " ".join(kk)


def _td_ders_metni(kod: str, D: Dict[str, Any]) -> str:
    return " · ".join(f"{k}: {D['metin'][k]}" for k in kod.split())


def td_ozet(T: pd.DataFrame, kim: str, pk: str) -> Dict[str, Any]:
    k = T[T[kim].isin(["OLUR", "OLMAZ"])]
    olur = k[k[kim] == "OLUR"]; olmaz = k[k[kim] == "OLMAZ"]
    beklenen = np.where(k[kim] == "OLUR", k.es_h5, 1 - k.es_h5)
    return {"OLUR": len(olur), "OLMAZ": len(olmaz), "BELİRSİZ": int((T[kim] == "BELİRSİZ").sum()), "karar": len(k),
            "arti": int((k[pk] == 1).sum()), "eksi": int((k[pk] == -1).sum()), "basari": float((k[pk] == 1).mean()) if len(k) else np.nan,
            "dogru_OLUR": int((olur.h5 == 1).sum()), "dogru_OLMAZ": int((olmaz.h5 == 0).sum()),
            "beklenen": float(np.mean(beklenen)) if len(k) else np.nan, "hep_olmaz_karar": float((k.h5 == 0).mean()) if len(k) else np.nan,
            "yanilinan": sorted(int(x) for x in k[k[pk] == -1].sayfa)}


def td_sonuc_kapisi(T: pd.DataFrame, no: int) -> Dict[str, Any]:
    """Betiğin saydığı ile tur_N_sonuc.json (TUR_N_SONUC.md) aynı olmak zorunda."""
    J = _td_json(td_yol(no)["sonuc"])
    for kim, pk in (("model", "puan_m"), ("cemal", "puan_c")):
        o = td_ozet(T, kim, pk); j = J[kim]
        for k in ("OLUR", "OLMAZ", "BELİRSİZ", "karar", "dogru_OLUR", "dogru_OLMAZ"):
            if int(o[k]) != int(j[k]):
                raise TDHata(f"{kim} {k}: betik {o[k]} / sonuç dosyası {j[k]}")
        if abs(o["basari"] - j["basari"]) > 1e-9 or o["yanilinan"] != sorted(j["yanilinan"]):
            raise TDHata(f"{kim}: başarı / yanılınan sayfalar sonuç dosyasıyla tutmadı")
    return J


def td_birikimli(no: int) -> List[Dict[str, Any]]:
    """Hakem seti (hakem_ders_pdf.hd_tablo; 40 sayfa, açık yarıda etkin karar) + tur 1..N. Cemal ve model ayrı; tek tanımlı taban."""
    H = HD.hd_tablo()
    parca = {"Cemal": [], "Model": []}
    parca["Cemal"].append(("Hakem seti (40)", H.rename(columns={"puan_c": "p"})[["cemal", "p", "es_h5", "h5"]].rename(columns={"cemal": "k"})))
    parca["Model"].append(("Hakem seti (40; vekil)", H.rename(columns={"puan_v": "p"})[["vekil", "p", "es_h5", "h5"]].rename(columns={"vekil": "k"})))
    for t in range(1, no + 1):
        Tt = td_tablo(t)
        parca["Cemal"].append((f"TUR {t} (30)", Tt.rename(columns={"puan_c": "p", "cemal": "k"})[["k", "p", "es_h5", "h5"]]))
        parca["Model"].append((f"TUR {t} (30)", Tt.rename(columns={"puan_m": "p", "model": "k"})[["k", "p", "es_h5", "h5"]]))
    out = []
    for kim, L in parca.items():
        for ad, Dd in L + [("Birikimli", pd.concat([d for _, d in L], ignore_index=True))]:
            k = Dd[Dd.k.isin(["OLUR", "OLMAZ"])]
            bek = np.where(k.k == "OLUR", k.es_h5, 1 - k.es_h5)
            out.append({"kim": kim, "bolum": ad, "karar": len(k), "arti": int((k.p == 1).sum()), "eksi": int((k.p == -1).sum()),
                        "basari": float((k.p == 1).mean()) if len(k) else np.nan, "beklenen": float(np.mean(bek)) if len(k) else np.nan,
                        "hep_olmaz": float((k.h5 == 0).mean()) if len(k) else np.nan, "disi": int(len(Dd) - len(k))})
    return out


# ================================================================ GÖRSEL
def td_sayfa_png(cemal_pdf: str, klasor: str, n: int) -> List[str]:
    if not os.path.exists(cemal_pdf):
        raise TDHata(f"Cemal'in PDF'i yok: {cemal_pdf}")
    os.makedirs(klasor, exist_ok=True)
    try:
        subprocess.run(["pdftoppm", "-r", str(TD_AYAR["dpi_sayfa"]), "-png", cemal_pdf, os.path.join(klasor, "s")], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError) as ex:
        raise TDHata(f"pdftoppm başarısız: {ex}") from ex
    ps = sorted((p for p in os.listdir(klasor) if re.fullmatch(r"s-\d+\.png", p)), key=lambda p: int(re.findall(r"\d+", p)[0]))
    if len(ps) != n:
        raise TDHata(f"Cemal'in PDF'inden {n} sayfa bekleniyordu, {len(ps)}")
    return [os.path.join(klasor, p) for p in ps]


def _pz(p: int) -> str:
    return {1: "+1", -1: "-1", 0: "0"}[int(p)]


def td_dogru_cumle(r: pd.Series, no: int = 1) -> str:
    notu = str(r.cemal_not).strip()
    if r.puan_c == 1 and r.cemal == "OLUR":
        return f"Doğru karar: OLUR; gözün tuttu ({notu[:120]}), +%5 gün +{r.k5} geldi."
    if r.puan_c == 1 and r.cemal == "OLMAZ":
        return f"Doğru karar: OLMAZ; eleme tuttu ({notu[:120]}), 15 günde +%5 gelmedi."
    if r.cemal == "BELİRSİZ":
        return f"Karar yok (puan 0): sonuç {'+%5 geldi' if r.h5 == 1 else '+%5 gelmedi'}; bu şekil bir sonraki turda karar verilecek şekil olarak not edilir."
    return (f"Ders kodu yok (HAKEM_DERSLER TUR {no}: 'OLUR dedi, gelmedi' listesinde, ortak derse bağlanmadı): 15 günde +%5 gelmedi"
            + (f"; takip stoplu çıkış {r.getiri * 100:+.1f}% (gün +{r.cikis_bar}), hedef penceresinden sonra." if r.getiri > 0.05 else "."))


def td_model_etiket(r: pd.Series, D: Dict[str, Any]) -> str:
    durum = "DOĞRU" if r.puan_m == 1 else ("YANLIŞ" if r.puan_m == -1 else "karar yok")
    s = f"MODEL {r.model}: {durum} ({_pz(r.puan_m)})"
    if r.vd:
        s += f" · {_td_ders_metni(r.vd, D)}"
    return s


# ================================================================ PDF
def td_pdf(no: int, cemal_pdf: str, cikti: Optional[str] = None, is_klasor: Optional[str] = None) -> Dict[str, Any]:
    from PIL import Image
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.utils import simpleSplit
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    Y_ = td_yol(no); D = TD_DERS.get(no)
    cikti = cikti or Y_["cikti"]
    if os.path.abspath(is_klasor or "/").startswith(TD_KOK + os.sep):
        raise TDHata("ara klasör repo içinde olamaz")
    is_klasor = is_klasor or tempfile.mkdtemp(prefix=f"tur{no}_ders_")
    T = td_tablo(no); J = td_sonuc_kapisi(T, no); B = td_birikimli(no)
    sayfa_png = td_sayfa_png(cemal_pdf, os.path.join(is_klasor, "sayfa"), len(T))
    os.makedirs(os.path.join(is_klasor, "graf"), exist_ok=True)
    ek: Dict[int, Dict[str, Any]] = {}
    for p in sorted(T.pazar.unique()):
        Vd = GE.OC.oc_veri(p, klasor=Y_["veri"])
        for _, r in T[T.pazar == p].iterrows():
            if r.sembol not in Vd["V"]:
                raise TDHata(f"sayfa {r.sayfa}: sembol veride yok")
            d = GE.ge_hazir(Vd["V"][r.sembol])
            try:
                g = HD.hd_grafik(r, d, os.path.join(is_klasor, "graf", f"g{r.sayfa:02d}.png"))
            except HD.HDHata as ex:
                raise TDHata(str(ex)) from ex
            g["sol_png"] = HD.hd_kirp(sayfa_png[r.sayfa - 1], os.path.join(is_klasor, "graf", f"c{r.sayfa:02d}.png"))
            ek[int(r.sayfa)] = g
        tdlog.info("grafik %s: %d", p, int((T.pazar == p).sum()))
        del Vd
    T["k10"] = [ek[s]["k10"] for s in T.sayfa]

    for ad, y in (("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), ("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")):
        if not os.path.exists(y):
            raise TDHata(f"yazı tipi yok: {y}")
        pdfmetrics.registerFont(TTFont(ad, y))
    W, Hh = landscape(A4)
    tmp = cikti + ".tmp"
    cv = canvas.Canvas(tmp, pagesize=(W, Hh), invariant=1)
    cv.setTitle(f"TUR {no} DERS"); cv.setAuthor(""); cv.setCreator(""); cv.setProducer("")

    def yaz(x, y, s, f="DV", n=9, renk=(0, 0, 0)):
        cv.setFillColorRGB(*renk); cv.setFont(f, n); cv.drawString(x, y, s); cv.setFillColorRGB(0, 0, 0)

    def paragraf(x, y, s, gen, f="DV", n=8, ara=None, renk=(0, 0, 0)):
        ara = ara or n + 2
        for ln in simpleSplit(s, f, n, gen):
            yaz(x, y, ln, f, n, renk); y -= ara
        return y

    def yuzde(v: float, ond: int = 1) -> str:
        return ("%" + f"{v * 100:.{ond}f}").replace(".", ",")

    # ---------------- KAPAK
    n = len(T)
    yaz(30, Hh - 36, f"HAKEM TURU {no} DERSİ — senin çizimlerin + sonrası + puan + ders", "DVB", 15)
    yaz(30, Hh - 52, f"{n} sayfa: solda senin işaretlediğin tur sayfası (aynen), sağda aynı olayın sonrası. Hisse adı ve tarih yok; yalnız pazar.", n=9)
    yaz(30, Hh - 64, "Puan: OLUR ve 15 günde +%5 stop'tan önce geldi = +1, gelmedi = -1; OLMAZ ve gelmedi = +1, geldi = -1; BELİRSİZ = 0 (karar dışı).", n=8)
    yaz(30, Hh - 75, "Ölçü kodun girişiyle (sinyal ertesi açılış). Taban = bütün sayfaların eş payı (aynı gün aynı kovadaki hisselerin +%5 payı).", n=8)
    kol = [("Taraf", 30), ("OLUR/OLMAZ/B", 95), ("OLUR isabeti", 190), ("OLMAZ isabeti", 275), ("BAŞARI", 355), ("Taban", 440),
           ("Hep OLMAZ", 482), ("Fisher p", 542)]
    y = Hh - 98
    for k, x in kol:
        yaz(x, y, k, "DVB", 9)
    cv.line(30, y - 4, 585, y - 4); y -= 16
    for kim, ad, renk in (("cemal", "Cemal", (0.0, 0.35, 0.0)), ("model", "Model", (0.15, 0.15, 0.45))):
        j = J[kim]
        vals = [ad, f"{j['OLUR']} / {j['OLMAZ']} / {j['BELİRSİZ']}", f"{j['dogru_OLUR']} / {j['OLUR']}", f"{j['dogru_OLMAZ']} / {j['OLMAZ']}",
                f"{yuzde(j['basari'])} ({j['dogru_OLUR'] + j['dogru_OLMAZ']}/{j['karar']})", yuzde(j["taban_es"]), yuzde(j["hep_OLMAZ_basari"]),
                f"{j['fisher_p']:.3f}".replace(".", ",")]
        for (k, x), s in zip(kol, vals):
            yaz(x, y, s, "DVB" if k == "BAŞARI" else "DV", 9, renk)
        y -= 14
    y -= 2
    jc, jm = J["cemal"], J["model"]
    if "kapak_sonuc" in D:
        f2 = lambda v: f"{v:.2f}".replace(".", ",")  # noqa: E731
        y = paragraf(30, y, D["kapak_sonuc"].format(ck=jc["karar"], cb=yuzde(jc["basari"]), mk=jm["karar"], mb=yuzde(jm["basari"]),
                     tb=yuzde(jc["taban_es"]), ho=yuzde(jc["hep_OLMAZ_basari"]), sh=yuzde(jc["sayfa_h5"], 0), ka=f2(J["uyum"]["kappa"]),
                     cp=f2(jc["fisher_p"]), mp=f2(jm["fisher_p"])), 555, "DVB", 8.5)
    else:
        y = paragraf(30, y, f"Sonuç: iki taraf da yazı-tura düzeyinde. Sen {jc['karar']} kararda {yuzde(jc['basari'])}, model {jm['karar']} kararda "
                     f"{yuzde(jm['basari'])}; taban {yuzde(jc['taban_es'])}; hepsine OLMAZ deseydin {yuzde(jc['hep_OLMAZ_basari'])} olurdu (sayfaların "
                     f"yarısı +%5 gördü). Uyum (kappa) {J['uyum']['kappa']:.2f}".replace(".", ",") + f". Fisher p {jc['fisher_p']:.1f}".replace(".", ",")
                     + ". Hedef %80-90; taban ~%40 olduğu için zor. n küçük; dersler SINANMADI, kural değil.", 555, "DVB", 8.5)
    # birikimli
    y -= 8
    yaz(30, y, "BİRİKİMLİ (hakem seti + tur)", "DVB", 10); y -= 14
    kol2 = [("Taraf", 30), ("Bölüm", 85), ("Karar", 225), ("+1", 265), ("-1", 295), ("Başarı", 325), ("Beklenen*", 380), ("Hep OLMAZ*", 445), ("Karar dışı", 515)]
    for k, x in kol2:
        yaz(x, y, k, "DVB", 8.5)
    cv.line(30, y - 4, 585, y - 4); y -= 14
    for b in B:
        renk = (0.0, 0.35, 0.0) if b["kim"] == "Cemal" else (0.15, 0.15, 0.45)
        f = "DVB" if b["bolum"] == "Birikimli" else "DV"
        vals = [b["kim"], b["bolum"], str(b["karar"]), str(b["arti"]), str(b["eksi"]), yuzde(b["basari"], 0), yuzde(b["beklenen"], 0),
                yuzde(b["hep_olmaz"], 0), str(b["disi"])]
        for (k, x), s in zip(kol2, vals):
            yaz(x, y, s, f, 8.5, renk)
        y -= 12
        if b["bolum"] == "Birikimli":
            y -= 4
    y = paragraf(30, y, "* Beklenen = kararlarının eş payına göre beklenen başarısı (OLUR'da eş payı, OLMAZ'da 1 - eş payı); Hep OLMAZ = aynı karar "
                 "sayfalarında hep OLMAZ deseydin. Hakem seti sayfa 20 düzeltmesiyle (Cemal OLUR; ölçü kodun girişiyle -1) sayıldı: 31 karar; "
                 "düzeltme öncesi 30 karar / 21 doğru.", 555, n=7, ara=8.6, renk=(0.35, 0.35, 0.35))
    # sağ sütun: bu turun dersleri
    xr = 600; yr = Hh - 98
    yaz(xr, yr, "BU TURUN DERSLERİ", "DVB", 10, (0.6, 0.0, 0.0)); yr -= 14
    for k in D["yeni"]:
        if k.startswith("CD"):
            yr = paragraf(xr, yr, f"{k} {D['metin'][k]}", W - xr - 25, n=7.5, ara=9.2) - 3
    yr -= 2
    yaz(xr, yr, D.get("tekrar_baslik", "TEKRAR EDEN (hakem setinden)"), "DVB", 9, (0.6, 0.0, 0.0)); yr -= 12
    for k in (k for k in D["tekrar"] if k.startswith("CD")):
        yr = paragraf(xr, yr, f"{k} {D['metin'][k]}", W - xr - 25, n=7.5, ara=9.2) - 3
    yr -= 2
    yaz(xr, yr, "MODELE (ana modelin kuralları)", "DVB", 9, (0.15, 0.15, 0.45)); yr -= 12
    for k in list(D["yeni"]) + list(D["tekrar"]):
        if k.startswith("VD"):
            yr = paragraf(xr, yr, f"{k} {D['metin'][k]}", W - xr - 25, n=7.5, ara=9.2) - 3
    pm = T[T.parmak == 1]; pz = T[T.parmak == 0]
    yr -= 2
    yr = paragraf(xr, yr, f"Parmak izi (F19, bilgi): +%5 gören parmaklı {int(pm.h5.sum())} / {len(pm)}, parmaksız {int(pz.h5.sum())} / "
                  f"{len(pz)}; n küçük, fark yorumlanmaz.", W - xr - 25, n=7.5, ara=9.2, renk=(0.3, 0.3, 0.3))
    if min(y, yr) < 30:
        raise TDHata("kapak sayfaya sığmadı")
    yaz(30, 18, f"Kaynak: tur_{no}_sonuc.json (= TUR_{no}_SONUC.md), tur_{no}_cemal_notlar.json, tur_{no}_model_etiket.json, tur_{no}_anahtar.json, "
        "olay_Y1.csv.gz, HAKEM_DERSLER.md. 'gün +k' = girişten sonraki k. geçerli bar (gün +0 = giriş günü).", n=6.5, renk=(0.35, 0.35, 0.35))
    cv.showPage()

    # ---------------- DERS SAYFALARI
    for _, r in T.iterrows():
        g = ek[int(r.sayfa)]
        sonuc = HD.hd_sonuc_metni(r, g["k10"])
        baslik = (f"Sayfa {r.sayfa} · Cemal: {r.cemal} · Model: {r.model} · SONUÇ: {sonuc} · PUAN Cemal {_pz(r.puan_c)} / model {_pz(r.puan_m)}")
        renk = (0.0, 0.45, 0.0) if r.puan_c == 1 else ((0.7, 0.0, 0.0) if r.puan_c == -1 else (0.3, 0.3, 0.3))
        yy = Hh - 24
        for ln in simpleSplit(baslik, "DVB", 11, W - 50):
            yaz(25, yy, ln, "DVB", 11, renk); yy -= 13
        yaz(25, yy, f"{r.pazar} · {r.donem} · parmak izi {'var' if r.parmak else 'yok'} · {HD.hd_takip_metni(r)} · eş payı (+%5) "
            f"{yuzde(r.es_h5, 0)}", n=8, renk=(0.3, 0.3, 0.3))
        top = yy - 6; kutu_h = top - 172; kw = ((W - 60) * 0.56, (W - 60) * 0.44); hmax = 0.0
        for k, (p, x0) in enumerate(((g["sol_png"], 25), (os.path.join(is_klasor, "graf", f"g{r.sayfa:02d}.png"), 35 + kw[0]))):
            iw, ih = Image.open(p).size; kutu_w = kw[k]
            sc = min(kutu_w / iw, kutu_h / ih); w_, h_ = iw * sc, ih * sc; hmax = max(hmax, h_)
            cv.drawImage(p, x0 + (kutu_w - w_) / 2, top - h_, width=w_, height=h_)
        alt = top - hmax
        yaz(25, alt - 9, "Sol: senin işaretlediğin sayfa (aynen)", n=7, renk=(0.4, 0.4, 0.4))
        yaz(35 + kw[0], alt - 9, "Sağ: aynı olay, sonrası açık (sarı = 15 bar penceresi)", n=7, renk=(0.4, 0.4, 0.4))
        y = alt - 24
        y = paragraf(25, y, f"(1) Cemal'in notu [işaret: {r.cemal_tur}]: {r.cemal_not}", W - 50, n=9, ara=11) - 3
        ned = ", ".join(GE.ge_neden_acilim(k).replace(": UYUYOR (lehte)", " +").replace(": UYMUYOR (aleyhte)", " -") for k in r.nedenler)
        y = paragraf(25, y, f"(2) Model: {r.model} (güven {r.guven}) · nedenler: {ned} · not: {r.model_not}", W - 50, n=8, ara=9.8) - 7
        metin = "(3) DERS: " + (_td_ders_metni(r.cd, D) if r.cd else td_dogru_cumle(r, no))
        sat = simpleSplit(metin, "DVB", 9.5, W - 66)
        msat = simpleSplit(td_model_etiket(r, D), "DV", 7.8, W - 66)
        bh = 12.5 * len(sat) + 9.5 * len(msat) + 10
        kr = (0.8, 0.0, 0.0) if r.puan_c == -1 else ((0.0, 0.55, 0.0) if r.puan_c == 1 else (0.55, 0.55, 0.55))
        cv.setStrokeColorRGB(*kr); cv.setLineWidth(1.8); cv.rect(25, y - bh + 9, W - 50, bh, stroke=1, fill=0); cv.setStrokeColorRGB(0, 0, 0)
        cv.setLineWidth(1)
        yb = y
        for ln in sat:
            yaz(33, yb, ln, "DVB", 9.5); yb -= 12.5
        mr = (0.15, 0.15, 0.45) if r.puan_m == 1 else (0.6, 0.1, 0.1)
        for ln in msat:
            yaz(33, yb, ln, "DV", 7.8, mr); yb -= 9.5
        if yb < 8:
            raise TDHata(f"sayfa {r.sayfa}: metin sayfaya sığmadı")
        cv.showPage()

    # ---------------- ÖZET
    yaz(30, Hh - 32, f"ÖZET — TUR {no}, {n} sayfa", "DVB", 13)
    kol = [("Sayfa", 30), ("Pazar", 72), ("Dönem", 115), ("Parmak", 165), ("Cemal", 210), ("Model", 280), ("Sonuç (15 gün)", 345),
           ("Takip (bilgi)", 545), ("Puan C", 615), ("Puan M", 660), ("Ders", 710)]
    y = Hh - 54
    for k, x in kol:
        yaz(x, y, k, "DVB", 8)
    cv.line(30, y - 3, W - 30, y - 3); y -= 13
    for _, r in T.iterrows():
        rc = (0.0, 0.45, 0.0) if r.puan_c == 1 else ((0.7, 0.0, 0.0) if r.puan_c == -1 else (0.3, 0.3, 0.3))
        rm = (0.0, 0.45, 0.0) if r.puan_m == 1 else ((0.7, 0.0, 0.0) if r.puan_m == -1 else (0.3, 0.3, 0.3))
        vals = [str(r.sayfa), r.pazar, r.donem, "var" if r.parmak else "yok", r.cemal, r.model, HD.hd_sonuc_metni(r, r.k10),
                f"{r.getiri * 100:+.1f}%", _pz(r.puan_c), _pz(r.puan_m), " ".join(x for x in (r.cd, r.vd) if x) or "—"]
        for (k, x), s in zip(kol, vals):
            yaz(x, y, s, "DV", 7.6, rc if k in ("Cemal", "Puan C") else (rm if k in ("Model", "Puan M") else (0, 0, 0)))
        y -= 13.5
    y -= 4
    for kim, pk, ad in (("cemal", "puan_c", "Cemal"), ("model", "puan_m", "Model")):
        o = td_ozet(T, kim, pk)
        yaz(30, y, f"{ad}: {o['karar']} karar, +1 {o['arti']}, -1 {o['eksi']}, başarı {yuzde(o['basari'])}, BELİRSİZ {o['BELİRSİZ']}; "
            f"yanıldığı sayfalar {', '.join(map(str, o['yanilinan']))}", "DVB", 8.5); y -= 12
    if y < 10:
        raise TDHata("özet sayfaya sığmadı")
    cv.showPage(); cv.save()
    mb = os.path.getsize(tmp) / 2 ** 20
    if mb > TD_AYAR["azami_mb"]:
        os.remove(tmp)
        raise TDHata(f"PDF {mb:.1f} MB > {TD_AYAR['azami_mb']} MB")
    os.replace(tmp, cikti)
    return {"pdf": cikti, "mb": round(mb, 2), "sayfa": 2 + n, "cemal": td_ozet(T, "cemal", "puan_c"), "model": td_ozet(T, "model", "puan_m"),
            "birikimli": B, "is_klasor": is_klasor}


# ================================================================ ÇAKIŞMA KAPISI ve KOMUT
def _cakisma_kontrol_td(_once=_CK_ONCE_TD):
    """Bellekte (Colab exec) önceden var olan bir ad bu dosyayla ezildiyse durur."""
    g = globals()
    atla = {"_CK_ONCE_TD", "_cakisma_kontrol_td", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit", "__builtins__",
            "__name__", "__doc__", "__file__", "__loader__", "__spec__", "__package__", "__cached__", "__annotations__"}
    ezilen = [k for k, i in _once.items() if k not in atla and k in g and id(g[k]) != i and not k.startswith("__")]
    if ezilen:
        raise TDHata(f"çakışma kapısı: bellekteki adlar ezildi: {ezilen[:10]}")


_cakisma_kontrol_td()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="HAKEM TURU DERS PDF'i")
    ap.add_argument("--no", type=int, required=True)
    ap.add_argument("--cemal-pdf", required=True)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--is", dest="is_klasor", default=None)
    a = ap.parse_args()
    try:
        R = td_pdf(a.no, a.cemal_pdf, a.cikti, a.is_klasor)
        print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
    except (TDHata, HD.HDHata, GE.GEHata) as ex:
        tdlog.error("%s", ex); sys.exit(1)
