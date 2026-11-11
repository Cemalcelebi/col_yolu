#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""karne.py — ÖNERİ / İZLEME KARNESİ (erken karne, kanıt değil).

Ne yapar
  İki araştırma raporunda (ABD mikro-cap AI 10x denetimi, 4 Kas 2026; BIST 10x adayları, 5 Kas 2026)
  ve 9 Kas 2026 canlı taramalarında ADI GEÇEN her hisseyi, raporun referans kapanışından en son
  kapanışa kadar ölçer: getiri, aynı penceredeki karşılaştırma (endeks + eşit ağırlıklı sepet),
  fazla getiri, pencere içi en büyük düşüş. Alınmayan ve elenen adlar da tabloda kalır.

Kullanım (ayda bir yeniden çalıştırılır; anahtar / şifre gerekmez)
  python karne.py                       # indirir, KARNE_<gün><Ay>.md dosyasını bu klasöre yazar
  python karne.py --veri /tmp/karne_veri --cikti KARNE_11Kas.md
  python karne.py --indirme-yok         # veri klasöründeki dosyalarla yeniden üretir
  python karne.py --son 2026-11-10      # serileri bu günde keser (yeniden üretim için)

Veri
  Yahoo chart API (v8), günlük. İndirilen dosyalar repoya konmaz; varsayılan klasör sistem geçici
  dizinidir (KARNE_VERI ortam değişkeni ya da --veri ile değişir).

Mimari (KURAL_MOTORU düzeni)
  KR_AYAR  : sabitler.   KR_PAZAR : pazar tanımı ve karşılaştırmalar.
  KR_KURAL : hangi ad, hangi rapor, hangi rol, hangi referans günü (tek doğruluk kaynağı).
  KR_ALIM  : gerçekten alınan adlar.   kr_* işlevleri: indir -> oku -> ölç -> grupla -> yaz.
"""
from __future__ import annotations

_CK_ONCE_KR = {k: id(v) for k, v in dict(globals()).items()}   # çakışma kapısı: yüklenmeden önceki adlar

import argparse
import datetime as dt
import json
import logging
import math
import os
import ssl
import statistics
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

KR_LOG = logging.getLogger("karne")

KR_AYAR = {
    "url": "https://query1.finance.yahoo.com/v8/finance/chart/{s}?range={r}&interval=1d&events=div%2Csplits",
    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/126.0.0.0 Safari/537.36",
    "ca_adaylari": ("/root/.ccr/ca-bundle.crt",),      # varsa kullanılır; yoksa sistem güven deposu
    "deneme": 5, "bekleme_sn": 0.6, "zaman_asimi_sn": 30,
    "ay_islem_gunu": 21,                                # bir ayda yaklaşık işlem günü
    "sigma_ay": (0.20, 0.25),                           # mikro-cap aylık kesit std varsayımı
    "delta_ay": (0.05, 0.10, 0.20),                     # sınanacak aylık grup farkı
    "z_guc": 1.96 + 0.84,                               # %5 çift yönlü anlamlılık + %80 güç
    "ayda_secim": (2, 3),                               # Cemal'in hızı (ayda 2 öneri) / izleme 1-3
}

KR_AYLAR = ("Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara")

KR_PAZAR = {
    "ABD": {"sonek": "", "endeks": "IWM", "endeks_ad": "IWM",
            "sepet": ("CRWV", "NBIS", "APLD", "IREN", "WULF", "CIFR", "CORZ"), "sepet_ad": "emsal sepeti (7)",
            "para": "$"},
    "BIST": {"sonek": ".IS", "endeks": "XU100.IS", "endeks_ad": "XU100",
             "sepet": "TUM", "sepet_ad": "karnedeki bütün BIST adları (eş ağırlık)", "para": "TL"},
}

# Grup sırası (özet tablosu bu sırayla yazılır)
KR_GRUP_SIRA = ("izleme 1-3", "mevcut dörtlü", "izleme listesi", "elenenler", "referans",
                "diğer taranan", "emsal sepeti", "canlı tarama 9 Kas")
KR_ANA_GRUPLAR = ("izleme 1-3", "izleme listesi", "elenenler")

_ABD_RAPOR = "ABD mikro-cap AI 10x denetimi (4 Kas 2026; fiyat 3 Kas kapanışı)"
_BIST_RAPOR = "BIST 10x adayları (5 Kas 2026; fiyat 4 Kas kapanışı)"

KR_KURAL = [
    # ---- ABD raporu: §9 sıralama, §7 evren dışı tarama, §3 emsal sepeti
    {"pazar": "ABD", "kaynak": _ABD_RAPOR, "ref": "2026-11-03", "grup": "izleme 1-3",
     "adlar": ("DGXX", "DUOT", "AIB")},
    {"pazar": "ABD", "kaynak": _ABD_RAPOR, "ref": "2026-11-03", "grup": "mevcut dörtlü",
     "adlar": ("DGXX", "AIB", "QMLS", "VIVO")},
    {"pazar": "ABD", "kaynak": _ABD_RAPOR, "ref": "2026-11-03", "grup": "elenenler",
     "adlar": ("VIVO", "GPUS", "BGDE", "DRK", "PWCM", "SGRX", "SOBR", "POLA", "BEEM", "NVVE", "NUAI", "SLNH")},
    {"pazar": "ABD", "kaynak": _ABD_RAPOR, "ref": "2026-11-03", "grup": "diğer taranan",
     "adlar": ("HOST", "SLNG", "VIP", "TSSI", "IPWR", "TGEN", "PPSI", "ZSQR", "AGPU")},
    {"pazar": "ABD", "kaynak": _ABD_RAPOR, "ref": "2026-11-03", "grup": "emsal sepeti",
     "adlar": ("CRWV", "NBIS", "APLD", "IREN", "WULF", "CIFR", "CORZ")},
    {"pazar": "ABD", "kaynak": "K57 canlı ABD Q3 taraması (9 Kas 2026)", "ref": "2026-11-09",
     "grup": "canlı tarama 9 Kas", "adlar": ("CENX", "AEHR")},
    # ---- BIST raporu: §1/§9 sıralama, izleme listesi, elenenler, referans; §5 tablosunda sıralanmayanlar
    {"pazar": "BIST", "kaynak": _BIST_RAPOR, "ref": "2026-11-04", "grup": "izleme 1-3",
     "adlar": ("YEOTK", "GWIND", "EUPWR")},
    {"pazar": "BIST", "kaynak": _BIST_RAPOR, "ref": "2026-11-04", "grup": "izleme listesi",
     "adlar": ("GESAN", "ORGE", "VBTYZ", "FORTE", "INDES", "CWENE", "ULUSE")},
    {"pazar": "BIST", "kaynak": _BIST_RAPOR, "ref": "2026-11-04", "grup": "elenenler",
     "adlar": ("KONTR", "ODINE", "ANELE", "MANAS", "IEYHO", "GEREL", "NETAS", "SMRTG", "MAGEN", "ESEN",
               "EMKEL", "PAPIL", "MIATK", "ARENA", "LINK", "EDATA", "INGRM", "ALFAS", "SAYAS", "KRONT",
               "ATATP", "FONET", "KFEIN", "ESCOM", "DGATE", "PENTA")},
    {"pazar": "BIST", "kaynak": _BIST_RAPOR, "ref": "2026-11-04", "grup": "referans",
     "adlar": ("ASTOR",)},
    {"pazar": "BIST", "kaynak": _BIST_RAPOR, "ref": "2026-11-04", "grup": "diğer taranan",
     "adlar": ("ARDYZ", "TCELL", "TTKOM")},
    {"pazar": "BIST", "kaynak": "K57 canlı BIST 3Ç26 taraması (9 Kas 2026)", "ref": "2026-11-09",
     "grup": "canlı tarama 9 Kas", "adlar": ("PNLSN", "FORTE")},
]

# Duyarlılık: aynı grubun başka bir tanımıyla ortalama (özet tablosunun altına tek satır yazılır)
KR_DUYARLILIK = [
    {"pazar": "ABD", "ref": "2026-11-03", "ad": "ABD elenenler, raporun §1 kısa listesi + NUAI, SLNH (POLA, BEEM, NVVE hariç)",
     "adlar": ("VIVO", "GPUS", "BGDE", "DRK", "PWCM", "SGRX", "SOBR", "NUAI", "SLNH")},
]

# Gerçekten alınan adlar (kaynak: ONERI_DEFTERI.md, 11 Kas 2026 durumu). Elle güncellenir.
KR_ALIM = [
    {"pazar": "ABD", "ad": "DGXX", "maliyet": 2.01, "alim_gunu": None,
     "not": "ort. maliyet 2,01 $ (Midas ekranı); alım günleri bilinmiyor, endeks karşılaştırması yok"},
    {"pazar": "BIST", "ad": "YEOTK", "maliyet": None, "alim_gunu": "2026-11-06",
     "not": "maliyet bildirilmedi; alım günü (6 Kas, tavan) kapanışı vekil alındı"},
]


class KarneHata(RuntimeError):
    """Karnenin üretilemeyeceği durumlar (endeks verisi yok, kural hatası)."""


# --------------------------------------------------------------------------- yardımcılar
def kr_yuzde(x, isaret=True):
    """0.123 -> '+%12,3' (Türkçe ondalık). None -> '—'."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    s = f"%{abs(x) * 100:.1f}".replace(".", ",")
    if not isaret or abs(x) < 0.0005:
        return s
    return ("+" if x >= 0 else "−") + s


def kr_sayi(x, hane=2):
    if x is None:
        return "—"
    return f"{x:,.{hane}f}".replace(",", "_").replace(".", ",").replace("_", ".").replace("-", "−")


def kr_gun(t):
    """'2026-11-03' -> '3 Kas'."""
    if not t:
        return "—"
    d = dt.date.fromisoformat(t)
    return f"{d.day} {KR_AYLAR[d.month - 1]}"


def kr_kural_denetle():
    """KR_KURAL'ı mekanik sınar: bilinmeyen pazar / grup, bozuk tarih, aynı kuralda yinelenen ad."""
    for i, k in enumerate(KR_KURAL):
        if k["pazar"] not in KR_PAZAR:
            raise KarneHata(f"KR_KURAL[{i}]: bilinmeyen pazar {k['pazar']!r}")
        if k["grup"] not in KR_GRUP_SIRA:
            raise KarneHata(f"KR_KURAL[{i}]: bilinmeyen grup {k['grup']!r}")
        dt.date.fromisoformat(k["ref"])
        if len(set(k["adlar"])) != len(k["adlar"]):
            raise KarneHata(f"KR_KURAL[{i}]: yinelenen ad var")
    gorulen = {}
    for k in KR_KURAL:                       # aynı ad aynı pazarda iki ANA gruba giremez
        if k["grup"] in KR_ANA_GRUPLAR:
            for a in k["adlar"]:
                anahtar = (k["pazar"], a)
                if anahtar in gorulen:
                    raise KarneHata(f"{a} iki ana grupta: {gorulen[anahtar]} ve {k['grup']}")
                gorulen[anahtar] = k["grup"]


def kr_sembol(pazar, ad):
    return ad + KR_PAZAR[pazar]["sonek"]


# --------------------------------------------------------------------------- indirme
def kr_ssl_baglam():
    for yol in (os.environ.get("SSL_CERT_FILE"),) + KR_AYAR["ca_adaylari"]:
        if yol and os.path.isfile(yol):
            return ssl.create_default_context(cafile=yol)
    return ssl.create_default_context()


def kr_aralik(en_eski_ref, bugun):
    """Yahoo 'range' değeri: referans gününden en az 10 gün öncesini kapsayan en kısa aralık."""
    gun = (bugun - dt.date.fromisoformat(en_eski_ref)).days + 10
    for sinir, ad in ((80, "3mo"), (170, "6mo"), (350, "1y"), (715, "2y"), (1800, "5y")):
        if gun <= sinir:
            return ad
    return "10y"


def kr_indir(sembol, veri_dir, aralik, baglam):
    """Tek sembolü indirir, veri_dir/<sembol>.json olarak yazar. Dönüş: (yol | None, durum metni)."""
    yol = os.path.join(veri_dir, sembol.replace("/", "_") + ".json")
    url = KR_AYAR["url"].format(s=urllib.parse.quote(sembol), r=aralik)
    istek = urllib.request.Request(url, headers={"User-Agent": KR_AYAR["ua"],
                                                 "Accept": "application/json,text/plain,*/*",
                                                 "Accept-Language": "en-US,en;q=0.9"})
    son_hata = "bilinmiyor"
    for deneme in range(1, KR_AYAR["deneme"] + 1):
        try:
            with urllib.request.urlopen(istek, timeout=KR_AYAR["zaman_asimi_sn"], context=baglam) as y:
                govde = y.read()
            json.loads(govde)                                  # bozuk gövdeyi diske yazma
            with open(yol, "wb") as f:
                f.write(govde)
            return yol, "indi"
        except urllib.error.HTTPError as e:
            son_hata = f"HTTP {e.code}"
            if e.code == 404:
                KR_LOG.warning("%s: Yahoo'da yok (404)", sembol)
                return None, son_hata
            if e.code in (403, 407):                           # vekil / politika reddi: yeniden deneme yok
                KR_LOG.error("%s: erişim reddi (%s)", sembol, son_hata)
                return None, son_hata
        except (urllib.error.URLError, TimeoutError, ssl.SSLError, ValueError, OSError) as e:
            son_hata = f"{type(e).__name__}: {e}"
        KR_LOG.warning("%s: deneme %d başarısız (%s)", sembol, deneme, son_hata)
        time.sleep(KR_AYAR["bekleme_sn"] * (2 ** deneme))
    KR_LOG.error("%s: indirilemedi (%s)", sembol, son_hata)
    return None, son_hata


# --------------------------------------------------------------------------- okuma
def kr_oku(yol, son_kesim=None, simdi_utc=None):
    """Yahoo chart JSON -> {'tarih': [...], 'kap': [...], 'duz': [...], 'olay': [...]} (yerel borsa günü).

    Yarım seans (borsa açıkken gelen son çubuk) atılır. son_kesim verilirse o günden sonrası atılır.
    Veri yoksa None döner."""
    try:
        with open(yol, "rb") as f:
            j = json.load(f)
        sonuc = (j.get("chart") or {}).get("result") or []
        if not sonuc:
            return None
        r = sonuc[0]
        meta = r.get("meta") or {}
        zaman = r.get("timestamp") or []
        gosterge = r.get("indicators") or {}
        kap = ((gosterge.get("quote") or [{}])[0]).get("close") or []
        duz = ((gosterge.get("adjclose") or [{}])[0]).get("adjclose") or kap
        kayma = int(meta.get("gmtoffset") or 0)
        donem = ((meta.get("currentTradingPeriod") or {}).get("regular")) or {}
        simdi = simdi_utc if simdi_utc is not None else time.time()
        seri = {"tarih": [], "kap": [], "duz": [], "olay": [], "para": meta.get("currency"), "son_alan": None}
        yerel = lambda ts: dt.datetime.fromtimestamp(ts + kayma, dt.timezone.utc).date().isoformat()
        for i, ts in enumerate(zaman):
            k = kap[i] if i < len(kap) else None
            d = duz[i] if i < len(duz) else None
            if donem and ts >= int(donem.get("start", 0)) and simdi < int(donem.get("end", 0)):
                continue                                       # seans sürüyor: kapanış değil
            gun = yerel(ts)
            if k is None and i == len(zaman) - 1:
                # Biten seansın çubuğunda kapanış boş: Yahoo'nun son fiyat alanı (regularMarketPrice) o günün
                # son fiyatıdır; yalnız aynı güne aitse ve seans bitmişse kullanılır, satır işaretlenir.
                sf, sz = meta.get("regularMarketPrice"), meta.get("regularMarketTime")
                if sf and sf > 0 and sz and yerel(int(sz)) == gun:
                    k = d = float(sf)
                    seri["son_alan"] = gun
            if k is None or not (k > 0):
                continue
            if son_kesim and gun > son_kesim:
                continue
            if seri["tarih"] and seri["tarih"][-1] == gun:     # aynı güne iki çubuk: sonuncusu geçerli
                seri["kap"][-1], seri["duz"][-1] = float(k), float(d if d and d > 0 else k)
                continue
            seri["tarih"].append(gun)
            seri["kap"].append(float(k))
            seri["duz"].append(float(d if d and d > 0 else k))
        for tur, kayitlar in (r.get("events") or {}).items():
            for _, e in (kayitlar or {}).items():
                ts = e.get("date")
                if ts is not None:
                    seri["olay"].append((dt.datetime.fromtimestamp(ts + kayma, dt.timezone.utc).date().isoformat(),
                                         "bölünme" if tur == "splits" else "temettü"))
        return seri if seri["tarih"] else None
    except (OSError, ValueError, KeyError, TypeError, IndexError) as e:
        KR_LOG.error("%s okunamadı: %s: %s", yol, type(e).__name__, e)
        return None


# --------------------------------------------------------------------------- ölçüm
def kr_olc(seri, ref, pazar_son):
    """Referans kapanışından son kapanışa getiri ve pencere içi en büyük düşüş (kapanıştan kapanışa).

    Getiri düzeltilmiş kapanışla (bölünme + temettü) hesaplanır; gösterilen fiyat ham kapanıştır."""
    if seri is None:
        return None
    t = seri["tarih"]
    i0 = max((i for i, g in enumerate(t) if g <= ref), default=None)
    if i0 is None:
        return None                                            # referans gününde henüz işlem görmüyor
    i1 = max((i for i, g in enumerate(t) if g <= pazar_son), default=None)
    if i1 is None or i1 < i0:
        return None
    d = seri["duz"][i0:i1 + 1]
    tepe, mdd = d[0], 0.0
    for x in d:
        tepe = max(tepe, x)
        mdd = min(mdd, x / tepe - 1.0)
    bayrak = []
    if t[i0] != ref:
        bayrak.append(f"ref günü işlem yok, {kr_gun(t[i0])} kapanışı")
    if t[i1] != pazar_son:
        bayrak.append(f"son işlem {kr_gun(t[i1])}")
    if seri.get("son_alan") == t[i1]:
        bayrak.append(f"{kr_gun(t[i1])} kapanışı Yahoo son fiyat alanından (kapanış çubuğu henüz boş)")
    olaylar = sorted({f"{tur} {kr_gun(g)}" for g, tur in seri["olay"] if t[i0] < g <= t[i1]})
    if olaylar:
        bayrak.append("düzeltme: " + ", ".join(olaylar))
    return {"ref_t": t[i0], "ref_k": seri["kap"][i0], "son_t": t[i1], "son_k": seri["kap"][i1],
            "get": d[-1] / d[0] - 1.0, "mdd": mdd, "bayrak": bayrak, "gun": i1 - i0}


def kr_ort(x):
    x = [v for v in x if v is not None]
    return statistics.fmean(x) if x else None


def kr_medyan(x):
    x = [v for v in x if v is not None]
    return statistics.median(x) if x else None


def kr_duzey(seri, ref, gun):
    """Serinin 'gun' günündeki (yoksa önceki son) düzeltilmiş kapanışı / referans kapanışı. Yoksa None."""
    if seri is None:
        return None
    t = seri["tarih"]
    i0 = max((i for i, g in enumerate(t) if g <= ref), default=None)
    i1 = max((i for i, g in enumerate(t) if g <= gun), default=None)
    if i0 is None or i1 is None or i1 < i0:
        return None
    return seri["duz"][i1] / seri["duz"][i0]


def kr_sepet_dip(seriler, endeks, semboller, ref, son):
    """Eş ağırlıklı sepetin pencere içi en düşük günü ve o günden bugüne sepet / endeks getirisi."""
    gunler = [g for g in seriler[endeks]["tarih"] if ref <= g <= son]
    duzey = []
    for g in gunler:
        x = [kr_duzey(seriler.get(s), ref, g) for s in semboller]
        x = [v for v in x if v is not None]
        duzey.append(statistics.fmean(x) if x else None)
    if not duzey or any(v is None for v in duzey):
        return None
    i = min(range(len(duzey)), key=lambda k: duzey[k])
    e_dip, e_son = kr_duzey(seriler[endeks], ref, gunler[i]), kr_duzey(seriler[endeks], ref, gunler[-1])
    return {"gun": gunler[i], "ref_dip": duzey[i] - 1.0, "dip_son": duzey[-1] / duzey[i] - 1.0,
            "endeks_dip_son": e_son / e_dip - 1.0}


def kr_karne_kur(seriler, pazar_son):
    """KR_KURAL'ı satırlara çevirir. Dönüş: (satirlar, karsilastirma) — karsilastirma[(pazar, ref)] = dict."""
    satirlar, sira = {}, []
    for k in KR_KURAL:
        for ad in k["adlar"]:
            anahtar = (k["pazar"], ad, k["ref"])
            if anahtar not in satirlar:
                o = kr_olc(seriler.get(kr_sembol(k["pazar"], ad)), k["ref"], pazar_son[k["pazar"]])
                satirlar[anahtar] = {"pazar": k["pazar"], "ad": ad, "ref": k["ref"], "gruplar": [], "kaynak": k["kaynak"],
                                     "olcum": o}
                sira.append(anahtar)
            satirlar[anahtar]["gruplar"].append(k["grup"])
    kars = {}
    for pazar, p in KR_PAZAR.items():
        for ref in sorted({k["ref"] for k in KR_KURAL if k["pazar"] == pazar}):
            e = kr_olc(seriler.get(p["endeks"]), ref, pazar_son[pazar])
            if e is None:
                raise KarneHata(f"{pazar} endeksi ({p['endeks']}) {ref} için ölçülemedi")
            if p["sepet"] == "TUM":
                adlar = sorted({a for (pz, a, _r) in satirlar if pz == pazar})
            else:
                adlar = list(p["sepet"])
            g = [kr_olc(seriler.get(kr_sembol(pazar, a)), ref, pazar_son[pazar]) for a in adlar]
            g = [x["get"] for x in g if x is not None]
            kars[(pazar, ref)] = {"endeks": e["get"], "sepet": kr_ort(g), "sepet_n": len(g), "sepet_top": len(adlar),
                                  "gun": e["gun"], "ref_t": e["ref_t"], "son_t": e["son_t"],
                                  "dip": kr_sepet_dip(seriler, p["endeks"], [kr_sembol(pazar, a) for a in adlar],
                                                      ref, pazar_son[pazar])}
    for anahtar in sira:
        s = satirlar[anahtar]
        o, c = s["olcum"], kars[(s["pazar"], s["ref"])]
        s["end"], s["sepet"] = c["endeks"], c["sepet"]
        s["fazla_end"] = None if o is None else o["get"] - c["endeks"]
        s["fazla_sepet"] = None if (o is None or c["sepet"] is None) else o["get"] - c["sepet"]
    return [satirlar[a] for a in sira], kars


def kr_grup_ozet(satirlar, kars):
    """Pazar × grup × referans günü özetleri (KR_GRUP_SIRA sırasıyla)."""
    ozet = []
    for pazar in KR_PAZAR:
        for grup in KR_GRUP_SIRA:
            for ref in sorted({s["ref"] for s in satirlar if s["pazar"] == pazar and grup in s["gruplar"]}):
                uye = [s for s in satirlar if s["pazar"] == pazar and grup in s["gruplar"] and s["ref"] == ref]
                olc = [s for s in uye if s["olcum"] is not None]
                g = [s["olcum"]["get"] for s in olc]
                c = kars[(pazar, ref)]
                ozet.append({"pazar": pazar, "grup": grup, "ref": ref, "n": len(olc), "top": len(uye),
                             "ort": kr_ort(g), "med": kr_medyan(g), "end": c["endeks"], "sepet": c["sepet"],
                             "fazla_end": kr_ort([s["fazla_end"] for s in olc]),
                             "fazla_sepet": kr_ort([s["fazla_sepet"] for s in olc]),
                             "isabet_end": sum(1 for s in olc if s["fazla_end"] > 0),
                             "isabet_sepet": sum(1 for s in olc if s["fazla_sepet"] is not None and s["fazla_sepet"] > 0),
                             "mdd_med": kr_medyan([s["olcum"]["mdd"] for s in olc]), "getiriler": g})
    return ozet


def kr_guc(ozet, kars):
    """Dürüstlük hesabı: gözlenen izleme 1-3 − elenenler farkı şanstan ayrılır mı, ayrılması için ne gerekir."""
    cikti = {"pazar": {}, "tablo": []}
    for pazar in KR_PAZAR:
        izl = next((o for o in ozet if o["pazar"] == pazar and o["grup"] == "izleme 1-3"), None)
        ele = next((o for o in ozet if o["pazar"] == pazar and o["grup"] == "elenenler"), None)
        if not izl or not ele or izl["n"] < 1 or ele["n"] < 2:
            continue
        hepsi = izl["getiriler"] + ele["getiriler"]
        for o in ozet:
            if o["pazar"] == pazar and o["grup"] == "izleme listesi" and o["ref"] == izl["ref"]:
                hepsi = hepsi + o["getiriler"]
        sigma_goz = statistics.stdev(hepsi) if len(hepsi) > 2 else None
        gun = kars[(pazar, izl["ref"])]["gun"]
        fark = izl["ort"] - ele["ort"]
        carpan = math.sqrt(1.0 / izl["n"] + 1.0 / ele["n"])
        sigma_var = [s * math.sqrt(gun / KR_AYAR["ay_islem_gunu"]) for s in KR_AYAR["sigma_ay"]]
        sh_goz = sigma_goz * carpan if sigma_goz else None
        cikti["pazar"][pazar] = {
            "n1": izl["n"], "n2": ele["n"], "gun": gun, "fark": fark, "sigma_goz": sigma_goz, "sh_goz": sh_goz,
            "z_goz": (fark / sh_goz) if sh_goz else None,
            "sh_var": [s * carpan for s in sigma_var], "sigma_var": sigma_var,
            # Gözlenen fark AYLIK gerçek fark olsaydı: izleme tarafında gereken seçim-ay ve ay (ayda n1 ad)
            "ay_gerek": ([math.ceil((KR_AYAR["z_guc"] * s / abs(fark)) ** 2 * (1.0 + izl["n"] / ele["n"]) / izl["n"])
                          for s in KR_AYAR["sigma_ay"]] if abs(fark) > 1e-9 else None)}
    for sigma in KR_AYAR["sigma_ay"]:
        for delta in KR_AYAR["delta_ay"]:
            n_sec = (KR_AYAR["z_guc"] * sigma / delta) ** 2            # karşı grup çok büyük (endeks gibi) ise
            n_iki = 2.0 * n_sec                                        # iki eşit küçük grup karşılaştırılıyorsa
            cikti["tablo"].append({"sigma": sigma, "delta": delta, "n_sec": math.ceil(n_sec), "n_iki": math.ceil(n_iki),
                                   "ay": [math.ceil(n_sec / a) for a in KR_AYAR["ayda_secim"]]})
    return cikti


def kr_alim_olc(seriler, pazar_son, kars):
    """Gerçekten alınan adlar: maliyete (ya da alım günü kapanışına) göre getiri."""
    cikti = []
    for a in KR_ALIM:
        seri = seriler.get(kr_sembol(a["pazar"], a["ad"]))
        son = kr_olc(seri, pazar_son[a["pazar"]], pazar_son[a["pazar"]])
        satir = {"ad": a["ad"], "pazar": a["pazar"], "not": a["not"], "son_k": None, "son_t": None,
                 "taban": a["maliyet"], "get": None, "end": None, "baglam": None}
        ilk = min(r for (pz, r) in kars if pz == a["pazar"])
        dip = kars[(a["pazar"], ilk)]["dip"]
        if not a["alim_gunu"] and dip and dip["gun"] != ilk:      # alım günü yok: sepet dibinden beri kıyas
            d = kr_duzey(seri, dip["gun"], pazar_son[a["pazar"]])
            if d is not None:
                satir["baglam"] = (f"sepet dibinden ({kr_gun(dip['gun'])} kapanışı) beri {a['ad']} {kr_yuzde(d - 1.0)}, "
                                   f"sepet {kr_yuzde(dip['dip_son'])}")
        if son is not None:
            satir["son_k"], satir["son_t"] = son["son_k"], son["son_t"]
            if a["maliyet"]:
                satir["get"] = son["son_k"] / a["maliyet"] - 1.0
            elif a["alim_gunu"]:
                o = kr_olc(seri, a["alim_gunu"], pazar_son[a["pazar"]])
                e = kr_olc(seriler.get(KR_PAZAR[a["pazar"]]["endeks"]), a["alim_gunu"], pazar_son[a["pazar"]])
                if o is not None:
                    satir["taban"], satir["get"] = o["ref_k"], o["get"]
                    satir["end"] = None if e is None else e["get"]
        cikti.append(satir)
    return cikti


# --------------------------------------------------------------------------- yazım
def _tablo(basliklar, satirlar):
    return ["| " + " | ".join(basliklar) + " |", "|" + "---|" * len(basliklar)] + \
           ["| " + " | ".join(s) + " |" for s in satirlar]


def kr_md(satirlar, kars, ozet, guc, alim, pazar_son, eksik, uretim):
    L = []
    son_metin = ", ".join(f"{p} {kr_gun(t)} {t[:4]}" for p, t in pazar_son.items())
    L += [f"# Öneri / izleme karnesi — {uretim} (ERKEN KARNE, KANIT DEĞİL)", "",
          f"Son kapanışlar: {son_metin}. Kaynak: Yahoo günlük kapanış. Üreten: `python karne.py`.",
          "İki rapordaki ve 9 Kas canlı taramalardaki **her ad** burada; alınmayanlar ve elenenler dahil.", ""]

    # 1) grup özeti
    L += ["## 1. Grup özeti", ""]
    for pazar, p in KR_PAZAR.items():
        govde = []
        for o in [o for o in ozet if o["pazar"] == pazar]:
            n = f"{o['n']}" if o["n"] == o["top"] else f"{o['n']} / {o['top']}"
            govde.append([o["grup"], kr_gun(o["ref"]), n, kr_yuzde(o["ort"]), kr_yuzde(o["med"]),
                          kr_yuzde(o["end"]), kr_yuzde(o["sepet"]), kr_yuzde(o["fazla_end"]),
                          f"{o['isabet_end']} / {o['n']}", f"{o['isabet_sepet']} / {o['n']}", kr_yuzde(o["mdd_med"])])
        L += [f"**{pazar}** (endeks: {p['endeks_ad']}; sepet: {p['sepet_ad']})", ""]
        L += _tablo(["Grup", "Ref.", "n", "Ort.", "Medyan", p["endeks_ad"], "Sepet", "Ort. fazla (endeks)",
                     "Endeksi geçen", "Sepeti geçen", "Medyan en büyük düşüş"], govde) + [""]
    L += ["n = ölçülen / toplam ad. İsabet = karşılaştırmayı geçen ad sayısı. 'mevcut dörtlü' izleme 1-3 ve "
          "elenenlerle örtüşür (DGXX, AIB, VIVO)."]
    for dy in KR_DUYARLILIK:
        g = [s["olcum"]["get"] for s in satirlar if s["pazar"] == dy["pazar"] and s["ref"] == dy["ref"]
             and s["ad"] in dy["adlar"] and s["olcum"] is not None]
        if g:
            L.append(f"Duyarlılık: {dy['ad']}: n = {len(g)}, ort. {kr_yuzde(kr_ort(g))}, medyan {kr_yuzde(kr_medyan(g))}.")
    L.append("")

    # 2) alınan adlar
    L += ["## 2. Alınan iki ad", ""]
    govde = []
    for a in alim:
        s = next((x for x in satirlar if x["ad"] == a["ad"] and x["pazar"] == a["pazar"]
                  and "izleme 1-3" in x["gruplar"]), None)
        o = s["olcum"] if s else None
        para = KR_PAZAR[a["pazar"]]["para"]
        govde.append([a["ad"],
                      "—" if o is None else f"{kr_sayi(o['ref_k'])} {para} ({kr_gun(o['ref_t'])})",
                      "—" if a["son_k"] is None else f"{kr_sayi(a['son_k'])} {para} ({kr_gun(a['son_t'])})",
                      "—" if o is None else kr_yuzde(o["get"]),
                      "—" if s is None else f"{kr_yuzde(s['end'])} / {kr_yuzde(s['sepet'])}",
                      "—" if s is None else f"{kr_yuzde(s['fazla_end'])} / {kr_yuzde(s['fazla_sepet'])}",
                      "—" if o is None else kr_yuzde(o["mdd"]),
                      "—" if a["get"] is None else
                      f"{kr_yuzde(a['get'])} ({kr_sayi(a['taban'])} {para}'den"
                      + ("" if a["end"] is None else f"; endeks {kr_yuzde(a['end'])}") + ")"])
    L += _tablo(["Ad", "Rapor ref. kapanışı", "Son kapanış", "Rapordan beri", "Endeks / sepet", "Fazla (endeks / sepet)",
                 "En büyük düşüş", "Alımdan beri"], govde) + [""]
    L += [f"- {a['ad']}: {a['not']}" + (f"; {a['baglam']}" if a["baglam"] else "") + "." for a in alim] + [""]

    # 3) dürüstlük notu
    L += ["## 3. Dürüstlük notu (önce bunu oku)", ""]
    pencere = ", ".join(f"{pz} {kr_gun(ref)} → {kr_gun(c['son_t'])}: {c['gun']} işlem günü"
                        for (pz, ref), c in sorted(kars.items()))
    L += [f"- **Pencere çok kısa:** {pencere}. Bu sürede hiçbir tez sınanmış olmaz.",
          "- **n çok küçük:** izleme 1-3 grubunda pazar başına 3 ad var; tek bir ad ortalamayı belirler."]
    for pazar, p in KR_PAZAR.items():
        ilk = min(r for (pz, r) in kars if pz == pazar)
        c = kars[(pazar, ilk)]
        dip = c["dip"]
        L.append(f"- **{pazar}, ortak hareket:** {kr_gun(ilk)} kapanışından beri {p['endeks_ad']} "
                 f"{kr_yuzde(c['endeks'])}, {p['sepet_ad']} {kr_yuzde(c['sepet'])}."
                 + ("" if not dip or dip["gun"] == ilk else
                    f" Sepetin pencere içi dibi {kr_gun(dip['gun'])} ({kr_yuzde(dip['ref_dip'])}); dipten beri sepet "
                    f"{kr_yuzde(dip['dip_son'])}, {p['endeks_ad']} {kr_yuzde(dip['endeks_dip_son'])}.")
                 + (" Dipten ya da dip yakınından alınan her ad bu ortak tepkiyle artıda görünür;"
                    if dip and dip["gun"] != ilk else " Adların çoğu birlikte hareket etti;")
                 + " karşılaştırmayı aşmayan getiri seçimin değil pazarın getirisidir.")
    for pazar, g in guc["pazar"].items():
        if g["z_goz"] is None:
            continue
        L.append(f"- **{pazar}, izleme 1-3 eksi elenenler:** fark {kr_yuzde(g['fark'])} puan "
                 f"(n = {g['n1']} ve {g['n2']}, {g['gun']} gün). Bu penceredeki adlar arası dağılım "
                 f"(std) {kr_yuzde(g['sigma_goz'], False)}; farkın standart hatası "
                 f"{kr_yuzde(g['sh_goz'], False)}; z = {kr_sayi(g['z_goz'], 1)} (2'nin altı şanstan ayrılmaz). "
                 f"Aylık std %20-25 varsayımıyla aynı pencerede standart hata "
                 f"{kr_yuzde(g['sh_var'][0], False)}-{kr_yuzde(g['sh_var'][1], False)}. "
                 + (f"Bu büyüklükte bir fark her ay gerçekten olsaydı bile, ayda {g['n1']} adla ayırt etmek için "
                    f"yaklaşık {kr_sayi(g['ay_gerek'][0], 0)}-{kr_sayi(g['ay_gerek'][1], 0)} ay gerekirdi."
                    if g["ay_gerek"] else ""))
    olcusuz = sorted({s["ad"] for s in satirlar if s["olcum"] is None})
    durgun = sorted({s["ad"] for s in satirlar if s["olcum"] and any(b.startswith("son işlem") for b in s["olcum"]["bayrak"])})
    if olcusuz or durgun:
        L.append("- **Eksik / durgun adlar:** "
                 + (f"ölçülemeyen: {', '.join(olcusuz)} (ortalamalara girmedi; batan ad buradaysa grup olduğundan iyi görünür). "
                    if olcusuz else "")
                 + (f"Son günlerde işlem görmeyen: {', '.join(durgun)} (son kapanışı taşındı)." if durgun else ""))
    else:
        L.append(f"- **Kapsam:** {len(satirlar)} satırın hepsi ölçüldü; eksik ya da işlemi durmuş ad yok.")
    L += ["- **Sonuç:** bu tablo bir yön göstergesi değil, ayda bir güncellenecek kaydın ilk satırıdır. "
          "Hiçbir grup farkı şanstan ayrılmıyor.", ""]
    L += ["**Fark şanstan ne zaman ayrılır? (basit hesap)** Gereken seçim-ay sayısı N = (2,8 × σ / Δ)²; "
          "σ = bir mikro-cap'in aylık getirisinin adlar arası std'si, Δ = seçilenlerin aylık fazla getirisi, "
          "2,8 = %5 anlamlılık + %80 güç. İki küçük grup birbiriyle kıyaslanırsa N iki katına çıkar.", ""]
    govde = [[kr_yuzde(t["sigma"], False), kr_yuzde(t["delta"], False) + " / ay", str(t["n_sec"]), str(t["n_iki"]),
              f"{t['ay'][0]} ay", f"{t['ay'][1]} ay"] for t in guc["tablo"]]
    L += _tablo(["σ (aylık)", "Δ (aylık fazla)", "N (endekse karşı)", "N (iki küçük grup, grup başına)",
                 f"Ayda {KR_AYAR['ayda_secim'][0]} seçimle", f"Ayda {KR_AYAR['ayda_secim'][1]} seçimle"], govde) + [""]
    L += ["Aynı sektördeki adlar birlikte oynar; bağımsız gözlem sayısı ad sayısından azdır, süreler alt sınırdır. "
          "Aylık 5 puanlık gerçek bir üstünlük bile yıllarca veri ister; ancak 20 puan / ay gibi çok büyük bir "
          "fark bir yıl içinde görünür.", ""]

    # 4) ayrıntı
    L += ["## 4. Ad ad tablo", ""]
    dipnot = {}
    for pazar, p in KR_PAZAR.items():
        govde = []
        olculen = [s for s in satirlar if s["pazar"] == pazar and s["olcum"] is not None]
        ortak = set.intersection(*[set(s["olcum"]["bayrak"]) for s in olculen]) if olculen else set()
        for s in [s for s in satirlar if s["pazar"] == pazar]:
            o = s["olcum"]
            rol = ", ".join(s["gruplar"])
            if o is None:
                govde.append([s["ad"], rol, kr_gun(s["ref"]), "veri yok", "—", "—", "—", "—", "—", "—"])
                continue
            isaret = ""
            for b in [b for b in o["bayrak"] if b not in ortak]:
                dipnot.setdefault((pazar, b), [])
                if s["ad"] not in dipnot[(pazar, b)]:
                    dipnot[(pazar, b)].append(s["ad"])
                isaret = " †"
            govde.append([s["ad"] + isaret, rol, kr_gun(s["ref"]), kr_sayi(o["ref_k"]), kr_sayi(o["son_k"]),
                          kr_yuzde(o["get"]), kr_yuzde(s["end"]), kr_yuzde(s["fazla_end"]), kr_yuzde(s["fazla_sepet"]),
                          kr_yuzde(o["mdd"])])
        L += [f"**{pazar}** (son kapanış {kr_gun(pazar_son[pazar])}; para {p['para']}"
              + "".join(f"; bütün adlarda {b}" for b in sorted(ortak)) + ")", ""]
        L += _tablo(["Ad", "Rol", "Ref.", "Ref. kapanış", "Son kapanış", "Getiri", p["endeks_ad"], "Fazla (endeks)",
                     "Fazla (sepet)", "En büyük düşüş"], govde) + [""]
    for (pazar, b), adlar in dipnot.items():
        L.append(f"† {b}: {', '.join(adlar)}.")
    if dipnot:
        L.append("")
    if eksik:
        L += ["Veri yok: " + ", ".join(f"{s} ({n})" for s, n in sorted(eksik.items())) + ".", ""]
    L += ["## 5. Yöntem", "",
          "- Getiri = son kapanış / referans kapanışı − 1 (Yahoo düzeltilmiş kapanış: bölünme ve temettü dahil; "
          "tabloda görünen fiyat ham kapanış).",
          "- Referans günü: ABD raporu 3 Kas, BIST raporu 4 Kas, canlı taramalar 9 Kas kapanışı.",
          "- Karşılaştırma aynı pencerede: ABD için IWM ve 7'li emsal sepeti (CRWV, NBIS, APLD, IREN, WULF, CIFR, CORZ; "
          "eş ağırlık); BIST için XU100 ve karnedeki bütün BIST adlarının eş ağırlıklı ortalaması.",
          "- En büyük düşüş: pencere içinde kapanıştan kapanışa tepe-dip (gün içi fitiller yok).",
          "- ABD elenenler listesi raporun §9'undaki tam listedir (POLA, BEEM, NVVE dahil); 'diğer taranan' = raporda "
          "tabloda olup sıralamaya girmeyen adlar.",
          "- Roller ve tarihler karne.py içindeki KR_KURAL'dadır; yeni öneri oraya bir satır olarak eklenir.", ""]
    return "\n".join(L)


# --------------------------------------------------------------------------- ana akış
def kr_calistir(veri_dir, cikti, indir=True, son_kesim=None):
    kr_kural_denetle()
    os.makedirs(veri_dir, exist_ok=True)
    bugun = dt.datetime.now(dt.timezone.utc).date()
    semboller = []
    for k in KR_KURAL:
        semboller += [kr_sembol(k["pazar"], a) for a in k["adlar"]]
    for pazar, p in KR_PAZAR.items():
        semboller.append(p["endeks"])
        if p["sepet"] != "TUM":
            semboller += [kr_sembol(pazar, a) for a in p["sepet"]]
    semboller = list(dict.fromkeys(semboller))
    aralik = kr_aralik(min(k["ref"] for k in KR_KURAL), bugun)
    KR_LOG.info("%d sembol, aralık %s, veri klasörü %s", len(semboller), aralik, veri_dir)

    eksik, seriler = {}, {}
    baglam = kr_ssl_baglam() if indir else None
    for i, s in enumerate(semboller, 1):
        yol = os.path.join(veri_dir, s.replace("/", "_") + ".json")
        durum = "dosyadan"
        if indir:
            yol, durum = kr_indir(s, veri_dir, aralik, baglam)
            time.sleep(KR_AYAR["bekleme_sn"])
        elif not os.path.isfile(yol):
            yol, durum = None, "dosya yok"
        seri = kr_oku(yol, son_kesim) if yol else None
        if seri is None:
            eksik[s] = durum if yol is None else "boş seri"
            KR_LOG.warning("[%d/%d] %s: VERİ YOK (%s)", i, len(semboller), s, eksik[s])
        else:
            seriler[s] = seri
            KR_LOG.info("[%d/%d] %s: %d gün, son %s", i, len(semboller), s, len(seri["tarih"]), seri["tarih"][-1])

    pazar_son = {}
    for pazar, p in KR_PAZAR.items():
        if p["endeks"] not in seriler:
            raise KarneHata(f"{pazar} endeksi ({p['endeks']}) indirilemedi; karne üretilmez")
        pazar_son[pazar] = seriler[p["endeks"]]["tarih"][-1]
    satirlar, kars = kr_karne_kur(seriler, pazar_son)
    ozet = kr_grup_ozet(satirlar, kars)
    guc = kr_guc(ozet, kars)
    alim = kr_alim_olc(seriler, pazar_son, kars)
    uretim = f"{bugun.day} {KR_AYLAR[bugun.month - 1]} {bugun.year}"
    if cikti is None:
        cikti = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"KARNE_{bugun.day}{KR_AYLAR[bugun.month - 1]}.md")
    metin = kr_md(satirlar, kars, ozet, guc, alim, pazar_son, eksik, uretim)
    with open(cikti, "w", encoding="utf-8") as f:
        f.write(metin + "\n")
    KR_LOG.info("yazıldı: %s (%d satır ad, %d veri yok)", cikti, len(satirlar), len(eksik))
    return {"satirlar": satirlar, "kars": kars, "ozet": ozet, "guc": guc, "alim": alim, "eksik": eksik, "cikti": cikti}


def _cakisma_kontrol_kr(_once=_CK_ONCE_KR, _dosya="karne.py"):
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_KR", "_CK_KAYIT", "_cakisma_kontrol_kr", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("argparse", "dt", "json", "logging", "math", "os", "ssl", "statistics", "sys", "tempfile", "time", "urllib", "annotations")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_kr()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Öneri / izleme karnesi (erken karne, kanıt değil)")
    ap.add_argument("--veri", default=os.environ.get("KARNE_VERI") or os.path.join(tempfile.gettempdir(), "karne_veri"),
                    help="indirilen Yahoo dosyalarının klasörü (repoya konmaz)")
    ap.add_argument("--cikti", default=None, help="çıktı MD yolu (varsayılan: bu klasörde KARNE_<gün><Ay>.md)")
    ap.add_argument("--indirme-yok", action="store_true", help="indirmeden, veri klasöründeki dosyalarla üret")
    ap.add_argument("--son", default=None, help="serileri bu günde kes (YYYY-AA-GG)")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
    try:
        if a.son:
            dt.date.fromisoformat(a.son)
        kr_calistir(a.veri, a.cikti, indir=not a.indirme_yok, son_kesim=a.son)
    except KarneHata as e:
        KR_LOG.error("KARNE ÜRETİLMEDİ: %s", e)
        return 2
    except Exception:                                           # beklenmeyen hata: iz bırak, sıfırdan farklı çık
        KR_LOG.exception("beklenmeyen hata")
        return 1
    return 0


if __name__ == "__main__" and "get_ipython" not in globals():
    sys.exit(main())
