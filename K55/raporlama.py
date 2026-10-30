"""K55 raporlama: Faz 0 raporu (K55_FAZ0_RAPOR.md: Cemal'in 7 sorusu), veri kapsamı (K55_VERI_KAPSAMI.md), sızıntı testi (K55_SIZINTI_TESTI.md),
koşu kimliği (K55_KOSU.json). Hiçbir satır silinmez; başarısız sonuçlar da yazılır.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import numpy as np
import pandas as pd


def _f(x: Any, p: int = 3) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return ""
    if isinstance(x, (float, np.floating)):
        return f"{x:+.{p}f}"
    return str(x)


TAM = {"n", "n_olay", "n_olmayan", "n_degisim", "hisse", "olay", "tanimli_likit_gun", "n_gun", "bosluk_sayi", "bosluk_max_gun", "asiri_getiri_sayi", "sicrama_sayi", "ohlc_hata",
       "sinif", "yil", "Y60", "Y120", "Y250", "slot_n_islem", "yil_tekrar", "yon_yukari", "yon_asagi", "sinanan_olay", "kontrol"}


def _hucre(v: Any, kol: str) -> str:
    if isinstance(v, (bool, np.bool_)):
        return str(bool(v))
    if kol in TAM and isinstance(v, (int, float, np.integer, np.floating)) and np.isfinite(v):
        return str(int(round(float(v))))
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    return _f(v)


def tablo(D: pd.DataFrame, kol: List[str]) -> List[str]:
    kol = [c for c in kol if c in D.columns]
    if not kol or not len(D):
        return ["(boş)"]
    L = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
    for r in D[kol].itertuples(index=False):
        L.append("| " + " | ".join(_hucre(v, c) for c, v in zip(kol, r)) + " |")
    return L


def veri_kapsami_yaz(Q: pd.DataFrame, ozet: Dict[str, Any], bilgi: Dict[str, Any], O: pd.DataFrame, say: pd.DataFrame, cikti: str, kimlik: Dict[str, Any]) -> str:
    L = [f"# K55 — VERİ KAPSAMI ({kimlik['kimlik']}; kod {kimlik['kod_surum']}; evren sürümü {kimlik['evren_surum'][:12]})", "",
         "## Evren ve seri kalitesi", ""] + [f"- {k}: {v}" for k, v in ozet.items()]
    L += ["", "## Panel", ""] + [f"- {k}: {v}" for k, v in bilgi.items()]
    if len(O):
        L += ["", "## Olaylar (kilitli tanımlar: Y60 +%30, Y120 +%50, Y250 +%100; örtüşmez; tam pencere)", ""]
        g = O.groupby("ufuk").agg(olay=("sembol", "size"), hisse=("sembol", "nunique"), getiri_medyan=("getiri", "median"), en_yuksek_medyan=("en_yuksek_getiri", "median")).reset_index()
        if len(say):
            top = {f"Y{h}": int(say[f"tanimli_Y{h}"].sum()) for h in (60, 120, 250) if f"tanimli_Y{h}" in say}
            g["tanimli_likit_gun"] = g.ufuk.map(top); g["taban_orani"] = g.olay / g.tanimli_likit_gun
        L += tablo(g, ["ufuk", "olay", "hisse", "tanimli_likit_gun", "taban_orani", "getiri_medyan", "en_yuksek_medyan"])
        O2 = O.assign(yil=O.tarih.dt.year); yt = O2.pivot_table(index="yil", columns="ufuk", values="sembol", aggfunc="size", fill_value=0).reset_index()
        L += ["", "Yıl başına olay sayısı:", ""] + tablo(yt, list(yt.columns))
    L += ["", "## Sembol başına kalite (ilk 60 satır; tamamı K55_VERI_KALITESI.csv)", ""]
    L += tablo(Q.head(60), ["sembol", "kaynak", "sinif", "n_gun", "ilk", "son", "bosluk_sayi", "bosluk_max_gun", "sifir_hacim_pay", "asiri_getiri_sayi", "sicrama_sayi", "ohlc_hata", "cik_var", "eksiksiz", "tarihsel_eksik"])
    yol = os.path.join(cikti, "K55_VERI_KAPSAMI.md"); open(yol, "w", encoding="utf-8").write("\n".join(L) + "\n"); return yol


def sizinti_yaz(S: Dict[str, Any], cikti: str) -> str:
    L = ["# K55 — GELECEK BİLGİSİ SIZINTISI TESTLERİ", "", "Kural (ONKAYIT_K55 bölüm 10): hepsi geçmeden Faz 1'e geçilmez.", ""]
    for ad, r in S.items():
        L.append(f"- **{ad}**: {'GEÇTİ' if r.get('gecti') else 'KALDI'} — " + "; ".join(f"{k}: {v}" for k, v in r.items() if k != "gecti"))
    L += ["", f"- SONUÇ: {'HEPSİ GEÇTİ' if all(r.get('gecti') for r in S.values()) else 'KALAN VAR'}"]
    yol = os.path.join(cikti, "K55_SIZINTI_TESTI.md"); open(yol, "w", encoding="utf-8").write("\n".join(L) + "\n"); return yol


def faz0_yaz(R: Dict[str, Any], cikti: str) -> str:
    k = R["kimlik"]; oz = R["kalite_ozet"]; b = R["panel_bilgi"]; S = R["sizinti"]; H = R.get("hucre", pd.DataFrame()); sure = R["sure"]
    tam = R.get("tam_tahmin", {})
    L = [f"# K55 — FAZ 0 RAPORU ({k['kimlik']})", "",
         f"- Kod {k['kod_surum']}; commit {k['commit']}; kilit sha {k['onkayit_sha'][:12]}; evren sürümü {k['evren_surum'][:12]}; örnek: {k['ayar']['ornek'] or 'tam evren'}; veri paketleri: {k['veri_paketleri']}.",
         "- Faz 0 amacı altyapıyı kanıtlamaktır; hücre sonuçları iskele denetimidir, iz iddiası değildir (optimize edilmedi).", "",
         "## Cemal'in 7 sorusu", "",
         f"1. Kaç hisse eksiksiz işlendi? {oz['eksiksiz']} / {oz['sembol']} (eksiksiz = ≥ 260 gün, boşluksuz, sıfır hacim payı ≤ %20, OHLC hatasız, bölünme sıçraması yok, yinelenen tarih yok).",
         f"2. Kaç hissede tarihsel veri eksik? {oz['tarihsel_eksik']} (boşluklu {oz['bosluklu']}, kısa seri {oz['kisa_seri']}, sıfır hacim yüksek {oz['sifir_hacim_yuksek']}); sıçramalı {oz['sicramali']}, aşırı getirili {oz['asiri_getirili']}, OHLC hatalı {oz['ohlc_hatali']}.",
         f"3. Kaç sembol şirketle güvenilir eşleştirildi? CIK eşleşen {oz['cik_eslesen']} / {oz['sembol']}; sektör bilinen {oz['sektor_bilinen']}; K54 sınıfı olmayan (doğrulanamayan) semboller evren dışı.",
         f"4. Delist olmuş şirketler nasıl ele alındı? Seri erken biten {oz['seri_erken_biten']}; sınıf dağılımı {oz['sinif']}; seri sonu işlemi {oz['seri_sonu']} (d100 = iflas −%100, d0 = birleşme bedeli, k51 = son kapanış ve negatifse −%30); 4b kod yeniden kullanımı kesimi uygulandı; sınıf 6 dışarıda; olay tanımında tam pencere şartı (seri sonunu aşan pencere tanımsız).",
         f"5. Gelecek bilgisi sızıntısı testleri geçti mi? {'EVET' if all(r.get('gecti') for r in S.values()) else 'HAYIR'} — " + "; ".join(f"{ad}: {'geçti' if r.get('gecti') else 'KALDI'}" for ad, r in S.items()) + ".",
         f"6. Denemede bütün modüller doğru çalıştı mı? {'EVET' if R['moduller_ok'] else 'HAYIR'} — " + "; ".join(f"{m}: {d}" for m, d in R['modul_durum'].items()) + ".",
         f"7. Tam evren koşusunun tahmini süresi ve kaynağı: {tam}.", "",
         "## Süreler (sn)", ""] + [f"- {ad}: {s}" for ad, s in sure.items()]
    L += ["", "## Panel", ""] + [f"- {kk}: {v}" for kk, v in b.items()]
    L += ["", "## Olay tekilliği", "", f"- {R['tekillik']}"]
    if len(H):
        L += ["", "## Hücre iskelesi (D01-S01 + olumlu / olumsuz kontrol; yalnız pipeline denetimi)", ""]
        L += tablo(H, ["hucre", "yontem", "donem", "ufuk", "n_olay", "n", "n_degisim", "d", "d_alt", "d_ust", "auc", "fark", "fark_alt", "net_fark", "slot_rastgele_yuzdelik", "lift", "eksik_pay", "karar"])
    L += ["", "## Çıktılar", "", "- K55_VERI_KALITESI.csv, K55_VERI_KAPSAMI.md, K55_EVREN.csv, K55_OLAYLAR.csv.gz, K55_SIZINTI_TESTI.md, K55_HUCRE_ISKELE.csv, K55_KOSU.json, panel pickle (veri klasörü, repoya girmez)."]
    yol = os.path.join(cikti, "K55_FAZ0_RAPOR.md"); open(yol, "w", encoding="utf-8").write("\n".join(L) + "\n")
    with open(os.path.join(cikti, "K55_KOSU.json"), "w", encoding="utf-8") as f:
        json.dump(k, f, ensure_ascii=False, indent=1, default=str)
    return yol
