"""MUM_IZI_GOZ — MUM_IZI EK 11: GÖZ ÖLÇÜMÜ. Cemal'in kendi 'benziyor' dediği bölgelerin sonrası (26 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI11_IS_TANIMI.md (commit 07cf050; ana model). Bu iş kod tespitini değil CEMAL'İN ETİKETİNİ tespit sayar: dört setin
(MUM_IZI4_ONAY, MUM_IZI6_ETIKET, MUM_IZI8_ONAY, MUM_IZI10_ONAY) Cemal'in sonrasını görmeden işaretlediği bölgeleri (EVET / KISMEN / HAYIR) alır ve sonrasını
ölçer: giriş = bölgeden sonraki ilk geçerli barın açılışı, ufuk 15 mum, R15, en yüksek / en derin, stop'tan önce dokunma, R30 bilgi; eş = CETVEL2 v2.2 konum eşi
(aynı giriş günü, aynı kova, aynı takvim aralığı). Sonuç BİLGİ'dir: n < 30 hücre 'örneklem yetersiz'; 'iz / tuttu' sözü yok; kasa açılmaz.
Ön kayıt (MUM_IZI11_ON_KAYIT.md) getiriler hesaplanmadan ÖNCE commit edilir; 'kos' kapıdan geçmeden başlamaz. Veri <= 2022-12-31; KASA açılmaz.

Komut:  python MUM_IZI_GOZ.py ornek      örneklem sayımı (getirisiz)
        python MUM_IZI_GOZ.py onkayit    MUM_IZI11_ON_KAYIT.md
        python MUM_IZI_GOZ.py kos        kapı -> olay ölçüleri + eşler + tablolar (mum_izi11_olay.csv, mum_izi11_sonuc.json)
        python MUM_IZI_GOZ.py pdf        MUM_IZI11_SONRASI.pdf
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_GZ = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_GZ = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_GZ not in sys.path:
    sys.path.insert(0, KOK_GZ)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAFTALIK as MH  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ)

gzlog = logging.getLogger("col.mum_izi_goz")
if not gzlog.handlers:
    _gz_h = logging.StreamHandler(sys.stderr)
    _gz_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_goz: %(message)s", "%H:%M:%S"))
    gzlog.addHandler(_gz_h)
    gzlog.setLevel(logging.INFO)
    gzlog.propagate = False


class GZHata(RuntimeError):
    """Durdurucu hata: kapı / şema / veri / kesik."""


GZ_SURUM = "MUM_IZI_GOZ v1.0 (2026-11-26): Cemal'in etiketli bölgelerinin 15 mumluk sonrası (bilgi)"
_C = MI.MI_YOL["cikti"]
GZ_YOL = {"cikti": _C, "kod": os.path.join(KOK_GZ, "MUM_IZI_GOZ.py"), "gecici": "/tmp/mum_izi/goz",
          "set": {"set1": (os.path.join(_C, "cemal_mum_izi4_onay.json"), os.path.join(_C, "mum_izi4_onay_anahtar.json"), "MUM_IZI4_ONAY"),
                  "set2": (os.path.join(_C, "cemal_mum_izi6_etiket.json"), os.path.join(_C, "mum_izi6_anahtar.json"), "MUM_IZI6_ETIKET"),
                  "set3": (os.path.join(_C, "cemal_mum_izi8_onay.json"), os.path.join(_C, "mum_izi8_onay_anahtar.json"), "MUM_IZI8_ONAY"),
                  "set4": (os.path.join(_C, "cemal_mum_izi10_onay.json"), os.path.join(_C, "mum_izi10_onay_anahtar.json"), "MUM_IZI10_ONAY")}}
GZ_DOSYA = {"onkayit": "MUM_IZI11_ON_KAYIT.md", "rapor": "MUM_IZI11_RAPOR.md", "sonuc": "mum_izi11_sonuc.json", "olay": "mum_izi11_olay.csv",
            "pdf": "MUM_IZI11_SONRASI.pdf", "ornek": "mum_izi11_ornek.json"}
SINIF = ["EVET", "KISMEN", "HAYIR"]

GZ_ESIK: Dict[str, Any] = {
    "surum": "GZ-1.0",
    "ornek": {"setler": "set1 MUM_IZI4_ONAY (s3-26), set2 MUM_IZI6_ETIKET (s2-49), set3 MUM_IZI8_ONAY (s3-26), set4 MUM_IZI10_ONAY (s2-25)",
              "isaret": "EVET / KISMEN / HAYIR karar; IKISI / YOK / BELIRSIZ karar dışı (çıkar); başka değer -> DUR",
              "tekrar": "set2'nin katman 'T' sayfaları set1 bölgelerinin tekrarıdır: ayrı bölge sayılmaz, İLK işaret (set1) geçerli; duyarlılık satırı: o bölgeler "
                        "set2'deki SON işaretle (karar dışıysa ilk işaret)",
              "bolge": "anahtardaki hisse, zaman dilimi, bölge sonu ve uzunluk (set4'te bölge başı / sonu / pencere)"},
    "olcu": {"giris": "bölgenin son mumundan sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk geçerli günü; o haftalık barın açılışı)",
             "ufuk": 15, "R15": "15. mumun kapanışı / giriş - 1 (giriş mumu 1. mum; haftalıkta 15. haftanın son geçerli günü)",
             "max_min": "giriş günü .. 15. mumun son günü arasında günlük en yüksek High / giriş - 1 ve en düşük Low / giriş - 1",
             "stop": "bölgenin (kendi zaman diliminde) en düşük Low'u x 0,98; giriş <= stop ise olay ölçülmez (sayısı yazılır); stop payı = ufukta günlük Low <= stop",
             "dokunma": "günlük sırayla High >= giriş x (1 + hedef) olan ilk gün stop gününden ÖNCE (aynı gün = stop önce)",
             "hedef": {"gunluk": [0.05, 0.10], "haftalik": [0.10, 0.20]}, "stop_carpan": 0.98, "bilgi": 30,
             "veri": {"gunluk": "MUM_IZI açık kopya (/tmp/mum_izi/acik, 2015-2022, günlük)", "haftalik": "MUM_IZI_HAFTALIK tam (2000-2022, günlük -> ISO hafta)"},
             "kesik": "15. mumun son günü <= 2022-12-30 değilse ölçülmez (ufuk kesik; sayısı yazılır); R30 aynı kuralla"},
    "es": {"tanim": "CETVEL2 v2.2 paneli (c2_panel22_al, önbelleksiz): aynı giriş günü d, aynı kova KV[d] (ATRP tercili x likidite üçlüsü x F15 çeyreği; KV >= 0), "
                    "olay hissesi ve aynı gün başka örneklem olayı olan hisseler dışı, d'de geçerli açılış; R = olayın 15. mum son günündeki (ya da öncesindeki son "
                    "geçerli) kapanış / d açılışı - 1 (AYNI takvim aralığı); eşin stop'u = olayın bölge takvim aralığında eşin en düşük Low'u x 0,98 (giriş > stop olanlar); "
                    "eş dokunma / stop payları aynı kuralla",
           "min": 5, "panel": "günlük olaylar: açık kopya paneli; haftalık olaylar: bölge sonu <= 2015-12-31 ise p1 paneli (/tmp/mum_izi/haftalik/p1, 2000-2016), değilse "
                               "açık kopya paneli; panelde olmayan / kovasız / eşi < 5 olay eşli tabloya girmez (sayısı yazılır)",
           "fark": "eşli fark = R15 - eş ortalaması"},
    "tablo": {"hucre": "sınıf (EVET, KISMEN, HAYIR, EVET+KISMEN) x zaman dilimi (günlük, haftalık)", "B": 5000, "tohum_boot": 25112111,
              "olcu": "n, R15 ortalama ve medyan, eş ortalaması, eşli fark ortalama ve medyan + olay bootstrap %95 (yerine koyarak, B 5000), artıda kapanan pay "
                      "(R15 > 0), dokunma payları, stop payı, en yüksek / en derin medyanı, R30 ortalama (bilgi)",
              "n_az": 30, "etiket": "n < 30 -> 'örneklem yetersiz'",
              "karsilastirma": "her zaman diliminde EVET - HAYIR (R15 ortalaması ve eşli fark ortalaması) + permütasyon p (iki yönlü, 10.000, tohum 25112112); "
                               "ayrıca (EVET + KISMEN) - HAYIR", "perm": 10000, "tohum_perm": 25112112,
              "bilgi": "pazar dağılımı; BIST ayrı satır; iki zaman dilimi birleşik eşli fark satırı; tekrar duyarlılığı (son işaretle)"},
    "pdf": {"sayfa1": "düz dil tablo (EVET / KISMEN / BENZEMİYOR x günlük / haftalık: n, kaçı artıda, ortalama ve medyan getiri, eş ortalaması, +%10'a kaçı "
                      "dokundu, kaçı stop) + 'Sayılar az (N < 30): bu bir sonuç değil, ilk bakış.'",
            "bolge": "BENZİYOR bölgeleri (önce haftalık sonra günlük; tarih sırası), sonra KISMEN: öncesi 15 mum + bölge (turuncu kutu) + sonrası 30 mum (veri kesiğini "
                     "aşmaz), Bollinger 20 + SMA20, giriş / stop / 15. mum çizgileri, hisse kodu + tarih AÇIK, altında R15, eş ortalaması, en yüksek / en derin"},
}

GZ_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü aynı kova (CETVEL2 v2.2 konum eşi) aynı takvim aralığı, aynı stop geometrisi; HAYIR sınıfı aynı seçim hattından doğal kontrol"),
    "K2": ("EVET", "Cemal bölgeleri sonrasını görmeden işaretledi (PDF'ler bölge sonunda kesik); bölgeler kodun o güne kadarki veriyle seçtikleri; giriş bölgeden "
                   "SONRAKİ barın açılışı; eş kovası giriş günü bilgisiyle; veri <= 2022-12-31 + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0); haftalık barlar tamamlanmış ISO haftaları (MH)"),
    "K4": ("EVET", "tekrar sayfaları ayrı bölge değil (ilk işaret); setler arasında hisse tekrarı yok (onay seçimleri önceki setlerin hisselerini dışladı; denetlenir)"),
    "K5": ("EVET", "giriş = sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk günü açılışı); giriş <= stop olay ölçülmez"),
    "K6": ("EVET", "TEZGAH2 / MI bölünme düzeltmeli fiyatlar; getiriler oransal; BIST TL, ABD USD, AVR yerel para (karşılaştırma eşli farkla)"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz"),
    "K8": ("EVET", "sınıf x zaman dilimi hücrelerinin çoğu n < 30: 'örneklem yetersiz' etiketi; karşılaştırma permütasyonla"),
    "K9": ("EVET", "MUM_IZI11_ON_KAYIT.md: KOD11 / ESIK11 / etiket ve anahtar sha'ları + sınıf sayıları; getiriler bu commit'ten sonra; gz_kapi"),
    "K10": ("EVET", "etiket şeması (isaret; bilinmeyen değer DUR); anahtar alanları (set4: bolge_bas / bolge_son / pencere); bölge başı veriden yeniden hesaplanıp set4'te "
                    "anahtarla denetlenir"),
    "K11": ("EVET", "olay ölçüleri 2 olayda düz döngüyle yeniden; tablo sayıları csv'den yeniden üretilir (test)"),
    "K12": ("EVET", "'iz / tuttu' sözü yok; n < 30 'örneklem yetersiz'; sonuç 'ilk bakış'"),
    "K13": ("EVET", "çakışma kapısı; eski kodlar / defterler / UC_IZ2 değişmez; yalnız kendi yolları commit"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


# ================================================================ 0) YARDIMCI
def _gz_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or GZ_YOL["cikti"], GZ_DOSYA[ad])


def gz_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or GZ_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def gz_isaret_oku(yol: str) -> Dict[int, str]:
    J = json.load(open(yol, encoding="utf-8"))
    if not isinstance(J.get("sayfalar"), dict):
        raise GZHata(f"etiket şeması: 'sayfalar' yok ({yol})")
    out = {}
    for k, v in J["sayfalar"].items():
        t = str(v.get("isaret", "")).strip().replace("İ", "I").replace("ı", "I").upper()
        if t not in ("EVET", "KISMEN", "HAYIR", "IKISI", "YOK", "BELIRSIZ"):
            raise GZHata(f"etiket şeması: {os.path.basename(yol)} sayfa {k} değer {v.get('isaret')!r}")
        out[int(k)] = t
    return out


# ================================================================ 1) ÖRNEKLEM
def gz_ornek() -> pd.DataFrame:
    """Bölgeler (tekrarsız) + sınıf (ilk işaret) + sinif_son (duyarlılık)."""
    rows = []; son: Dict[Tuple[str, str, str], str] = {}
    for st, (iy, ay, ad) in GZ_YOL["set"].items():
        E = gz_isaret_oku(iy); A = json.load(open(ay, encoding="utf-8"))["sayfalar"]
        for r in A:
            pg = int(r.get("sayfa", r.get("yeni_sayfa")))
            lab = E.get(pg, "eksik")
            if st == "set2" and r.get("katman") == "T":
                if lab in SINIF:
                    son[(r["zaman"], r["sembol"], r["tarih"])] = lab
                continue
            if st == "set4":
                rec = {"zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "tarih": r["bolge_son"], "m": int(r["pencere"]), "bolge_bas_anahtar": r["bolge_bas"]}
            else:
                rec = {"zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "tarih": r["tarih"], "m": int(r["m"]), "bolge_bas_anahtar": None}
            rows.append({"set": st, "set_ad": ad, "sayfa": pg, "isaret": lab, **rec})
    X = pd.DataFrame(rows); X["sinif"] = np.where(X.isaret.isin(SINIF), X.isaret, None)
    X["sinif_son"] = [son.get((z, s, t), c) for z, s, t, c in zip(X.zaman, X.sembol, X.tarih, X.sinif)]
    X = X[X.sinif.notna()].reset_index(drop=True)
    if X.duplicated(["zaman", "sembol", "tarih"]).any():
        raise GZHata("K4: aynı bölge iki kez")
    return X


def gz_ornek_sayim(X: pd.DataFrame) -> Dict[str, Any]:
    return {"toplam": int(len(X)), "sinif": X.sinif.value_counts().to_dict(),
            "set_sinif": {f"{a}|{b}": int(v) for (a, b), v in X.groupby(["set", "sinif"]).size().items()},
            "sinif_zaman": {f"{a}|{b}": int(v) for (a, b), v in X.groupby(["sinif", "zaman"]).size().items()},
            "set_sinif_zaman": {f"{a}|{b}|{c}": int(v) for (a, b, c), v in X.groupby(["set", "sinif", "zaman"]).size().items()},
            "pazar": {f"{a}|{b}": int(v) for (a, b), v in X.groupby(["sinif", "pazar"]).size().items()},
            "tekrar_degisen": int((X.sinif != X.sinif_son).sum())}


# ================================================================ 2) OLAY ÖLÇÜLERİ
def gz_olc_bir(Dg: pd.DataFrame, W: Optional[pd.DataFrame], r: Dict[str, Any], kesik: pd.Timestamp) -> Dict[str, Any]:
    """Tek olay: Dg günlük veri; W haftalık bar (haftalık olayda) ya da None. r: zaman, tarih, m."""
    E = GZ_ESIK["olcu"]; U = int(E["ufuk"]); U2 = int(E["bilgi"]); hed = E["hedef"][r["zaman"]]; sc = float(E["stop_carpan"])
    rec: Dict[str, Any] = {"olculdu": False, "neden": ""}
    B = W if r["zaman"] == "haftalik" else Dg
    t = B.index.get_loc(pd.Timestamp(r["tarih"])); m = int(r["m"]); s = t - m + 1
    rec["bolge_bas"] = (W.bas.iloc[s] if r["zaman"] == "haftalik" else Dg.index[s]); rec["bolge_son"] = Dg.index[Dg.index.get_loc(B.index[t])]
    rec["bolge_bas_bar"] = B.index[s]          # ilk barın tarihi (haftalıkta haftanın son günü; MUM_IZI_HAKEM anahtarının 'bolge_bas' tanımı)
    stop = float(B.Low.to_numpy(float)[s:t + 1].min()) * sc; rec["stop"] = stop
    if t + 1 >= len(B):
        rec["neden"] = "giris_yok"; return rec
    g = W.bas.iloc[t + 1] if r["zaman"] == "haftalik" else Dg.index[t + 1]; gi = Dg.index.get_loc(g); E0 = float(Dg.Open.iloc[gi])
    rec["giris"] = g; rec["E0"] = E0
    if t + U >= len(B) or B.index[t + U] > kesik:
        rec["neden"] = "ufuk_kesik"; return rec
    if E0 <= stop:
        rec["neden"] = "giris_stop_altinda"; return rec
    e15 = B.index[t + U]; ei = Dg.index.get_loc(e15); rec["son15"] = e15
    Hs = Dg.High.to_numpy(float)[gi:ei + 1]; Ls = Dg.Low.to_numpy(float)[gi:ei + 1]
    rec["R15"] = float(Dg.Close.iloc[ei]) / E0 - 1; rec["max15"] = float(Hs.max()) / E0 - 1; rec["min15"] = float(Ls.min()) / E0 - 1
    sk = np.flatnonzero(Ls <= stop); ks = int(sk[0]) if len(sk) else 10 ** 9; rec["stop15"] = float(len(sk) > 0)
    for x in hed:
        hk = np.flatnonzero(Hs >= E0 * (1 + x)); rec[f"d{int(round(x * 100))}"] = float(len(hk) > 0 and int(hk[0]) < ks)
    if t + U2 < len(B) and B.index[t + U2] <= kesik:
        rec["R30"] = float(B.Close.iloc[t + U2]) / E0 - 1
    rec["olculdu"] = True
    return rec


def gz_olc(X: pd.DataFrame) -> pd.DataFrame:
    out = []; Vc: Dict[Any, Any] = {}
    for r in X.to_dict("records"):
        k = (r["zaman"], r["pazar"])
        if k not in Vc:
            if r["zaman"] == "gunluk":
                Vc[k] = (MI.mi_veri(r["pazar"], MV.MV_YOL["gunluk"])["V"], None)
            else:
                Vd = MI.mi_veri(r["pazar"], MH.MH_YOL["tam"])["V"]; Vc[k] = (Vd, MV.mv_haftalik_panel(Vd))
        Vd, Vw = Vc[k]
        rec = gz_olc_bir(Vd[r["sembol"]], Vw[r["sembol"]] if Vw is not None else None, r, MI.MI_KESIK)
        if isinstance(r.get("bolge_bas_anahtar"), str) and str(pd.Timestamp(rec["bolge_bas_bar"]).date()) != r["bolge_bas_anahtar"]:
            raise GZHata(f"K10: {r['set']} s{r['sayfa']} bölge başı anahtarla uyuşmuyor")
        out.append(rec)
    Y = pd.DataFrame(out, index=X.index)
    return pd.concat([X, Y], axis=1)


# ================================================================ 3) EŞLER
def gz_es_grup(Pn: Dict[str, Any], X: pd.DataFrame, gun_olay: Dict[int, set]) -> pd.DataFrame:
    """MUM_IZI_HAFTALIK.mh_es ile aynı mantık (aynı gün aynı kova, aynı takvim aralığı); hedefler zaman dilimine göre."""
    P = Pn["P"]; idx = P["tarih"]; kol = P["kol"]; KV = Pn["KV"]; Op, Hi, Lo, Cl = P["Op"], P["Hi"], P["Lo"], Pn["Cl"]
    sc = float(GZ_ESIK["olcu"]["stop_carpan"]); mn = int(GZ_ESIK["es"]["min"]); rows = []
    for r in X.itertuples():
        rec: Dict[str, Any] = {"es_neden": ""}
        j = kol.get(r.sembol)
        try:
            d = idx.get_loc(pd.Timestamp(r.giris)); e = idx.get_loc(pd.Timestamp(r.son15)); a = idx.get_loc(pd.Timestamp(r.bolge_bas)); tt = idx.get_loc(pd.Timestamp(r.bolge_son))
        except KeyError:
            rec["es_neden"] = "panel_tarih_yok"; rows.append(rec); continue
        if j is None or KV[d, j] < 0:
            rec["es_neden"] = "kova_yok"; rows.append(rec); continue
        kv = int(KV[d, j]); rec["kova"] = kv
        uye = np.flatnonzero((KV[d] == kv) & np.isfinite(Op[d]) & (Op[d] > 0)); dis = gun_olay.get(d, set())
        uye = np.array([u for u in uye if u != j and u not in dis], np.int64)
        if len(uye) < mn:
            rec["es_neden"] = "es_az"; rows.append(rec); continue
        E = Op[d, uye]; c = Cl[d:e + 1, uye]; okc = np.isfinite(c)
        sonk = np.where(okc.any(0), c.shape[0] - 1 - np.argmax(okc[::-1], axis=0), -1)
        Rr = np.where(sonk >= 0, c[np.maximum(sonk, 0), np.arange(len(uye))] / E - 1, np.nan)
        h = Hi[d:e + 1, uye]; lo = Lo[d:e + 1, uye]
        with np.errstate(all="ignore"):
            mx = np.nanmax(h, axis=0) / E - 1; mi = np.nanmin(lo, axis=0) / E - 1; st = np.nanmin(Lo[a:tt + 1, uye], axis=0) * sc
        ok = np.isfinite(Rr) & np.isfinite(st) & (E > st)
        if ok.sum() < mn:
            rec["es_neden"] = "es_az"; rows.append(rec); continue
        E, Rr, mx, mi, st, h, lo = E[ok], Rr[ok], mx[ok], mi[ok], st[ok], h[:, ok], lo[:, ok]
        with np.errstate(invalid="ignore"):
            stopm = np.where(np.isnan(lo), False, lo <= st[None, :])
        ks = np.where(stopm.any(0), np.argmax(stopm, axis=0), 10 ** 9)
        rec["es_stop15"] = float(stopm.any(0).mean())
        for x in GZ_ESIK["olcu"]["hedef"][r.zaman]:
            with np.errstate(invalid="ignore"):
                hm = np.where(np.isnan(h), False, h >= E[None, :] * (1 + x))
            kh = np.where(hm.any(0), np.argmax(hm, axis=0), 10 ** 9)
            rec[f"es_d{int(round(x * 100))}"] = float(((kh < ks) & (kh < 10 ** 9)).mean())
        R = float(r.R15); rec.update({"es_R15": float(Rr.mean()), "es_med": float(np.median(Rr)), "n_es": int(len(Rr)), "fark": R - float(Rr.mean()),
                                      "sira": float(((Rr < R).sum() + 0.5 * (Rr == R).sum()) / len(Rr)), "es_max15": float(np.nanmean(mx)), "es_min15": float(np.nanmean(mi))})
        rows.append(rec)
    return pd.DataFrame(rows, index=X.index)


def gz_es(X: pd.DataFrame) -> pd.DataFrame:
    import CETVEL2 as C2
    Y = X.copy(); Y["panel"] = None
    m = Y.olculdu.astype(bool)
    Y.loc[m & (Y.zaman == "gunluk"), "panel"] = "acik"
    hw = m & (Y.zaman == "haftalik"); Y.loc[hw, "panel"] = np.where(pd.to_datetime(Y.loc[hw, "bolge_son"]) <= pd.Timestamp("2015-12-31"), "p1", "acik")
    kl = {"acik": MV.MV_YOL["gunluk"], "p1": MH.MH_YOL["p1"]}; parca = []
    for (pz, pn), g in Y[Y.panel.notna()].groupby(["pazar", "panel"]):
        if not os.path.exists(os.path.join(kl[pn], f"V_{pz}.pkl")):
            parca.append(pd.DataFrame({"es_neden": "panel_yok"}, index=g.index)); continue
        Pn = C2.c2_panel22_al(pz, kl[pn], 15, onbellek=False); idx = Pn["P"]["tarih"]; kol = Pn["P"]["kol"]
        gun: Dict[int, set] = {}
        for r in Y[Y.olculdu.astype(bool) & (Y.pazar == pz)].itertuples():
            try:
                d = idx.get_loc(pd.Timestamp(r.giris))
            except KeyError:
                continue
            if r.sembol in kol:
                gun.setdefault(d, set()).add(kol[r.sembol])
        parca.append(gz_es_grup(Pn, g, gun)); del Pn; gc.collect()
        gzlog.info("eş: %s %s %d olay", pz, pn, len(g))
    E = pd.concat(parca) if parca else pd.DataFrame()
    return Y.join(E, how="left")


# ================================================================ 4) TABLOLAR
def gz_boot(x: np.ndarray, B: int, tohum: int) -> Dict[str, Optional[List[float]]]:
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 2:
        return {"ort95": None, "med95": None}
    rng = np.random.default_rng(tohum); i = rng.integers(0, len(x), (B, len(x))); s = x[i]
    return {"ort95": np.quantile(s.mean(1), [0.025, 0.975]).tolist(), "med95": np.quantile(np.median(s, 1), [0.025, 0.975]).tolist()}


def gz_perm(a: np.ndarray, b: np.ndarray, n: int, tohum: int) -> Optional[float]:
    a = np.asarray(a, float); b = np.asarray(b, float); a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return None
    obs = abs(a.mean() - b.mean()); z = np.r_[a, b]; rng = np.random.default_rng(tohum); say = 0
    for _ in range(n):
        p = rng.permutation(len(z)); say += int(abs(z[p[:len(a)]].mean() - z[p[len(a):]].mean()) >= obs - 1e-15)
    return (1 + say) / (1 + n)


def gz_hucre(g: pd.DataFrame, zaman: str, tohum: int) -> Dict[str, Any]:
    T = GZ_ESIK["tablo"]; o = g[g.olculdu.astype(bool)]; f = o[np.isfinite(o.fark.astype(float))] if "fark" in o else o.iloc[:0]
    out: Dict[str, Any] = {"n_bolge": int(len(g)), "n": int(len(o)), "n_es": int(len(f)), "olculemedi": g[~g.olculdu.astype(bool)].neden.value_counts().to_dict()}
    if not len(o):
        out["etiket"] = "ölçülemedi"; return out
    R = o.R15.astype(float)
    out.update({"R15_ort": float(R.mean()), "R15_med": float(R.median()), "arti_pay": float((R > 0).mean()), "stop_pay": float(o.stop15.astype(float).mean()),
                "max_med": float(o.max15.astype(float).median()), "min_med": float(o.min15.astype(float).median()),
                "R30_ort": float(o.R30.astype(float).mean()) if "R30" in o and np.isfinite(o.R30.astype(float)).any() else None, "R15_boot": gz_boot(R.to_numpy(), T["B"], tohum)})
    for x in GZ_ESIK["olcu"]["hedef"][zaman]:
        c = f"d{int(round(x * 100))}"; out[f"dokunma_{c}"] = float(o[c].astype(float).mean())
    if len(f):
        fa = f.fark.astype(float)
        out.update({"es_ort": float(f.es_R15.astype(float).mean()), "fark_ort": float(fa.mean()), "fark_med": float(fa.median()), "fark_boot": gz_boot(fa.to_numpy(), T["B"], tohum + 1),
                    "sira_ort": float(f.sira.astype(float).mean())})
        for x in GZ_ESIK["olcu"]["hedef"][zaman]:
            c = f"es_d{int(round(x * 100))}"; out[f"es_dokunma_{c[3:]}"] = float(f[c].astype(float).mean())
        out["es_stop_pay"] = float(f.es_stop15.astype(float).mean())
    out["etiket"] = "örneklem yetersiz" if len(o) < T["n_az"] else "bilgi"
    return out


def gz_tablolar(Y: pd.DataFrame, sinif_kol: str = "sinif") -> Dict[str, Any]:
    T = GZ_ESIK["tablo"]; H: Dict[str, Any] = {}; K: Dict[str, Any] = {}
    gruplar = {"EVET": ["EVET"], "KISMEN": ["KISMEN"], "HAYIR": ["HAYIR"], "EVET+KISMEN": ["EVET", "KISMEN"]}
    for zi, z in enumerate(("gunluk", "haftalik")):
        for gi, (ad, sl) in enumerate(gruplar.items()):
            H[f"{ad}|{z}"] = gz_hucre(Y[(Y.zaman == z) & Y[sinif_kol].isin(sl)], z, T["tohum_boot"] + 100 * zi + gi)
            H[f"{ad}|{z}|BIST"] = gz_hucre(Y[(Y.zaman == z) & Y[sinif_kol].isin(sl) & (Y.pazar == "BIST")], z, T["tohum_boot"] + 1000 + 100 * zi + gi)
        o = Y[(Y.zaman == z) & Y.olculdu.astype(bool)]
        for ad, sl in (("EVET-HAYIR", ["EVET"]), ("(EVET+KISMEN)-HAYIR", ["EVET", "KISMEN"])):
            a = o[o[sinif_kol].isin(sl)]; b = o[o[sinif_kol] == "HAYIR"]
            fa = a.fark.astype(float) if "fark" in a else pd.Series(dtype=float); fb = b.fark.astype(float) if "fark" in b else pd.Series(dtype=float)
            K[f"{ad}|{z}"] = {"n_a": int(len(a)), "n_b": int(len(b)), "R15_fark": float(a.R15.astype(float).mean() - b.R15.astype(float).mean()) if len(a) and len(b) else None,
                              "R15_p": gz_perm(a.R15.to_numpy(float), b.R15.to_numpy(float), T["perm"], T["tohum_perm"] + zi),
                              "n_es_a": int(np.isfinite(fa).sum()), "n_es_b": int(np.isfinite(fb).sum()),
                              "esli_fark_fark": float(np.nanmean(fa) - np.nanmean(fb)) if np.isfinite(fa).any() and np.isfinite(fb).any() else None,
                              "esli_p": gz_perm(fa.to_numpy(), fb.to_numpy(), T["perm"], T["tohum_perm"] + 10 + zi)}
    o = Y[Y.olculdu.astype(bool)]
    for ad, sl in (("EVET-HAYIR", ["EVET"]), ("(EVET+KISMEN)-HAYIR", ["EVET", "KISMEN"])):
        a = o[o[sinif_kol].isin(sl)].fark.astype(float); b = o[o[sinif_kol] == "HAYIR"].fark.astype(float)
        K[f"{ad}|birlesik_esli"] = {"n_es_a": int(np.isfinite(a).sum()), "n_es_b": int(np.isfinite(b).sum()),
                                    "esli_fark_fark": float(np.nanmean(a) - np.nanmean(b)) if np.isfinite(a).any() and np.isfinite(b).any() else None,
                                    "esli_p": gz_perm(a.to_numpy(), b.to_numpy(), T["perm"], T["tohum_perm"] + 20)}
    return {"hucre": H, "karsilastirma": K}


# ================================================================ 5) KAPI, ÖN KAYIT, KOŞU
def gz_sha_simdi() -> Dict[str, str]:
    out = {"KOD11_SHA": MI._mi_sha(GZ_YOL["kod"]), "ESIK11_SHA": gz_esik_sha(), "MI_KOD_SHA": MI._mi_sha(MI.MI_YOL["kod"]), "MH_KOD_SHA": MI._mi_sha(MH.MH_YOL["kod"]),
           "MV_KOD_SHA": MI._mi_sha(MV.MV_YOL["kod"])}
    for st, (iy, ay, _) in GZ_YOL["set"].items():
        out[f"ISARET_{st.upper()}_SHA"] = MI._mi_sha(iy); out[f"ANAHTAR_{st.upper()}_SHA"] = MI._mi_sha(ay)
    return out


def gz_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or GZ_YOL["cikti"]; yol = _gz_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise GZHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = gz_sha_simdi()
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise GZHata(f"ön kayıt kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_GZ); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise GZHata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_GOZ.py", "MUM_IZI.py", "MUM_IZI_HAFTALIK.py", "MUM_IZI_V2.py"]):
        raise GZHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def gz_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or GZ_YOL["cikti"]; y = _gz_yol("onkayit", cikti)
    if os.path.exists(y):
        raise GZHata("ön kayıt zaten var")
    X = gz_ornek(); S = gz_ornek_sayim(X); sh = gz_sha_simdi(); ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in GZ_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_GOZ.py"])
    s = [f"# MUM_IZI11 ÖN KAYIT ({MI._mi_simdi()})", "",
         "Göz ölçümü: Cemal'in etiketi tespit sayılır; bölgelerin sonrası ölçülür. Bu dosya GETİRİLER HESAPLANMADAN önce commit edilir; tanımlar sonra değişmez. "
         "Sonuç bilgi: n < 30 hücre 'örneklem yetersiz'; 'iz / tuttu' sözü yok; kasa açılmaz.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_GOZ.py commit'i: {kc or 'yok'}", "",
         "## Örneklem (getirisiz sayım)", "", f"- {json.dumps(S, ensure_ascii=False)}", "",
         "## Tanımlar (GZ_ESIK; sha yukarıda)", "", "```", json.dumps(GZ_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 11")


def gz_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    t0 = time.time(); cikti = cikti or GZ_YOL["cikti"]
    if os.path.exists(_gz_yol("sonuc", cikti)):
        raise GZHata("sonuç zaten var")
    G0 = gz_kapi(cikti)
    kasa = KS.kasa_kapisi([os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] +
                          [os.path.join(MH.MH_YOL["tam"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")],
                          "2022-12-31")
    X = gz_ornek(); Y = gz_es(gz_olc(X)); Y = Y.sort_values(["set", "sayfa"]).reset_index(drop=True)
    kol = ["set", "set_ad", "sayfa", "isaret", "sinif", "sinif_son", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m", "olculdu", "neden", "giris", "E0", "stop", "son15",
           "R15", "max15", "min15", "stop15", "d5", "d10", "d20", "R30", "panel", "kova", "n_es", "es_R15", "es_med", "fark", "sira", "es_max15", "es_min15", "es_d5", "es_d10",
           "es_d20", "es_stop15", "es_neden"]
    for c in kol:
        if c not in Y:
            Y[c] = np.nan
    O = Y[kol].copy()
    for c in ("bolge_bas", "bolge_son", "giris", "son15"):
        O[c] = pd.to_datetime(O[c]).dt.strftime("%Y-%m-%d")
    O.to_csv(_gz_yol("olay", cikti), index=False, float_format="%.6f")
    J = {"surum": GZ_SURUM, "kapi": G0, "kasa": kasa, "ornek": gz_ornek_sayim(X), "olculemedi": Y[~Y.olculdu.astype(bool)].neden.value_counts().to_dict(),
         "es_yok": Y[Y.olculdu.astype(bool)].es_neden.fillna("").replace("", "var").value_counts().to_dict(),
         "tablo": gz_tablolar(Y), "duyarlilik_son_isaret": gz_tablolar(Y, "sinif_son")["karsilastirma"],
         "pazar": {f"{a}|{b}|{c}": int(v) for (a, b, c), v in Y[Y.olculdu.astype(bool)].groupby(["sinif", "zaman", "pazar"]).size().items()},
         "olay_sha": MI._mi_sha(_gz_yol("olay", cikti)), "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_gz_yol("sonuc", cikti), J, "sonuç 11")
    return J


# ================================================================ 6) PDF
def _gz_y(x: Optional[float], n: int = 1) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"%{100 * x:.{n}f}".replace(".", ",")


def gz_pdf(cikti: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    cikti = cikti or GZ_YOL["cikti"]; y = _gz_yol("pdf", cikti)
    J = json.load(open(_gz_yol("sonuc", cikti), encoding="utf-8")); H = J["tablo"]["hucre"]
    if MI._mi_sha(_gz_yol("olay", cikti)) != J["olay_sha"]:
        raise GZHata("olay csv'si sonuç json'uyla uyuşmuyor")
    O = pd.read_csv(_gz_yol("olay", cikti)); Vc: Dict[Any, Any] = {}
    ad = {"EVET": "BENZİYOR", "KISMEN": "KISMEN", "HAYIR": "BENZEMİYOR"}
    with PdfPages(y, metadata={"Title": "MUM_IZI11 sonrası", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); n_e = int(sum(H[f"EVET|{z}"]["n"] for z in ("gunluk", "haftalik")))
        fig.text(0.05, 0.95, f"Senin BENZİYOR dediğin {n_e} bölge sonrasında ne yaptı", fontsize=15, weight="bold")
        fig.text(0.05, 0.915, "Giriş: bölgeden sonraki ilk mumun açılışı. 15 mum sonra kapanışla getiri. Eş: aynı gün, benzer oynaklık ve likiditedeki hisseler.", fontsize=9.5)
        ax = fig.add_axes([0.03, 0.42, 0.94, 0.47]); ax.axis("off"); sat = []
        for z, zad, h2 in (("haftalik", "haftalık (15 hafta)", "d10"), ("gunluk", "günlük (15 gün)", "d10")):
            for s in SINIF:
                c = H[f"{s}|{z}"]; n = c.get("n", 0)
                sat.append([ad[s], zad, str(n), f"{int(round(c.get('arti_pay', 0) * n))} / {n}" if n else "-", _gz_y(c.get("R15_ort")), _gz_y(c.get("R15_med")),
                            _gz_y(c.get("es_ort")), f"{int(round(c.get('dokunma_' + h2, 0) * n))} / {n}" if n else "-", f"{int(round(c.get('stop_pay', 0) * n))} / {n}" if n else "-"])
        tb = ax.table(cellText=sat, colLabels=["senin işaretin", "mum", "bölge", "artıda kapanan", "ortalama", "medyan", "eşlerin ort.", "+%10'a dokunan", "stop olan"],
                      loc="upper center", cellLoc="center", colWidths=[0.14, 0.15, 0.07, 0.12, 0.1, 0.1, 0.1, 0.12, 0.1])
        tb.auto_set_font_size(False); tb.set_fontsize(9); tb.scale(1, 2.0)
        fig.text(0.05, 0.36, "Sayılar az (N < 30): bu bir sonuç değil, ilk bakış.", fontsize=13, weight="bold")
        fig.text(0.05, 0.32, "Sonraki sayfalar: BENZİYOR dediğin her bölge (önce haftalık, sonra günlük), sonra KISMEN dediklerin. Hisse ve tarih açık;\n"
                 "turuncu kutu = bölge, yeşil çizgi = giriş, kırmızı = stop (bölge dibi x 0,98), gri dikey = 15. mum.", fontsize=9.5, va="top")
        pdf.savefig(fig); plt.close(fig)
        for s in ("EVET", "KISMEN"):
            X = O[(O.sinif == s)].copy(); X["zs"] = X.zaman.map({"haftalik": 0, "gunluk": 1}); X = X.sort_values(["zs", "bolge_son"])
            for r in X.itertuples():
                k = (r.zaman, r.pazar)
                if k not in Vc:
                    Vc[k] = MV.mv_veri(*k)
                d = Vc[k][r.sembol]; t = d.index.get_loc(pd.Timestamp(r.bolge_son)) if r.zaman == "gunluk" else int(np.flatnonzero(d.index >= pd.Timestamp(r.bolge_son))[0])
                m = int(r.m); i0 = max(0, t - m + 1 - 15); i1 = min(len(d) - 1, t + 30); eksik = (t + 30) - i1
                BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(i0, i1 + 1)
                fig = plt.figure(figsize=(8.3, 11.7)); ax = fig.add_axes([0.07, 0.36, 0.9, 0.56])
                MV._mv_ciz(ax, *(d[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl], BA[sl], (t - m + 1 - i0, t - i0),
                           f"{ad[s]} · {r.sembol} ({r.pazar}) · {'haftalık' if r.zaman == 'haftalik' else 'günlük'} · bölge {r.bolge_bas} .. {r.bolge_son}")
                if bool(r.olculdu) or np.isfinite(getattr(r, "E0", np.nan)):
                    xg = t + 1 - i0; ax.axvline(xg - 0.5, color="#1a9850", linewidth=1.2, linestyle="--")
                    if np.isfinite(r.E0):
                        ax.hlines(r.E0, xg - 0.5, i1 - i0 + 0.5, color="#1a9850", linewidth=1)
                    if np.isfinite(r.stop):
                        ax.hlines(r.stop, t - m + 1 - i0 - 0.5, i1 - i0 + 0.5, color="#d73027", linewidth=1)
                    if t + 15 <= i1:
                        ax.axvline(t + 15 - i0 + 0.4, color="#777777", linewidth=1.2)
                ax.set_xticks([t - m + 1 - i0, t + 1 - i0] + ([t + 15 - i0] if t + 15 <= i1 else []))
                ax.set_xticklabels([str(d.index[t - m + 1].date()), "giriş", "15. mum"] if t + 15 <= i1 else [str(d.index[t - m + 1].date()), "giriş"], fontsize=8)
                if bool(r.olculdu):
                    alt = (f"15 mum getirisi: {_gz_y(r.R15)}   ·   eşlerin ortalaması: {_gz_y(r.es_R15) if np.isfinite(r.es_R15) else 'eş yok'}   ·   en yüksek: {_gz_y(r.max15)}   ·   "
                           f"en derin: {_gz_y(r.min15)}\n30 mum getirisi: {_gz_y(r.R30) if np.isfinite(r.R30) else '-'}   ·   stop: {'oldu' if r.stop15 == 1 else 'olmadı'}")
                else:
                    alt = f"ölçülmedi: {r.neden}"
                if eksik > 0:
                    alt += f"\nsonrası {30 - eksik} mum (veri 2022-12-30'da bitiyor)"
                fig.text(0.07, 0.3, alt, fontsize=11, va="top")
                pdf.savefig(fig); plt.close(fig)
    return y


# ================================================================ 7) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_gz(_once=_CK_ONCE_GZ, _dosya="MUM_IZI_GOZ.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_GZ",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_gz()


def _gz_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_GOZ")
    ap.add_argument("komut", choices=["ornek", "onkayit", "kos", "pdf"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "ornek":
            print(json.dumps(gz_ornek_sayim(gz_ornek()), ensure_ascii=False))
        elif a.komut == "onkayit":
            print(gz_onkayit_yaz())
        elif a.komut == "kos":
            J = gz_kos(); print(json.dumps(MI._mi_json({k: J[k] for k in ("ornek", "olculemedi", "es_yok")}), ensure_ascii=False))
        elif a.komut == "pdf":
            print(gz_pdf())
    except GZHata as ex:
        gzlog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_gz_ana())
