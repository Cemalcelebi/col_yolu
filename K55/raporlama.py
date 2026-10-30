"""K55 raporlama: Faz 0 raporu (K55_FAZ0_RAPOR.md: Cemal'in 7 sorusu), veri kapsamı (K55_VERI_KAPSAMI.md), sızıntı testi (K55_SIZINTI_TESTI.md),
koşu kimliği (K55_KOSU.json). Hiçbir satır silinmez; başarısız sonuçlar da yazılır.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from .veri_kalitesi import kapsam_md


def _f(x: Any, p: int = 3) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return ""
    if isinstance(x, (float, np.floating)):
        return f"{x:+.{p}f}"
    return str(x)


TAM = {"n_degisim", "varyant", "A_etki_varyant", "B_tutar_varyant", "C_etki_varyant", "yil_tekrar", "yil_n", "fiyat_yok", "kisa_seri_320", "eksik_islem_gunu", "ciddi_bosluk_sayi", "yinelenen_islem_gunu", "takvim_disi_satir", "ohlc_high_low", "getiri_100_ustu_sayi", "muhtemel_bolunme", "aciklanamayan_sicrama", "sert_haber_hareketi", "cik_bos", "sektor_bos", "kota", "aday", "secilen", "eksik", "toplam_secilen", "istenen", "evren", "once", "sonra", "atilan", "n", "n_olay", "n_olmayan", "n_degisim", "hisse", "olay", "tanimli_likit_gun", "n_gun", "bosluk_sayi", "bosluk_max_gun", "asiri_getiri_sayi", "sert_hareket_sayi", "ohlc_hata", "hucre", "varyant", "test", "ret",
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
    L = kapsam_md(Q, ozet, f"({kimlik['kimlik']}; kod {kimlik['kod_surum']}; evren sürümü {kimlik['evren_surum'][:12]})")
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
    L += ["", "## Sembol başına kalite (ilk 60 satır; tamamı K55_VERI_KALITESI.csv; her sorun ayrı sütun)", ""]
    L += tablo(Q.head(60), ["sembol", "kaynak", "sinif", "n_gun", "ilk", "son", "fiyat_yok", "kisa_seri_320", "eksik_islem_gunu", "ciddi_bosluk_sayi", "yinelenen_islem_gunu", "takvim_disi_satir", "sifir_hacim_pay", "eksik_hacim_pay",
                           "ohlc_high_low", "getiri_100_ustu_sayi", "muhtemel_bolunme", "aciklanamayan_sicrama", "sert_haber_hareketi", "cik_bos", "sektor_bos", "veri_hatasi", "veri_yetersiz", "kullanilabilir"])
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
         f"- Kod {k['kod_surum']}; commit {k['commit']}{' (KİRLİ: ' + str(k['git_kirli']) + ')' if k.get('git_kirli') else ''}; kilit sha {k['onkayit_sha'][:12]}; ayar sha {k.get('ayar_sha', '')[:12]}; "
         f"kod dosyası sha {len(k.get('kod_sha', {}))} adet, veri dosyası sha {len(k.get('veri_sha', {}))} adet (K55_KOSU.json); evren sürümü {k['evren_surum'][:12]}; örnek: {k['ayar']['ornek'] or 'tam evren'}; veri paketleri: {k['veri_paketleri']}.",
         "- Faz 0 amacı altyapıyı kanıtlamaktır; hücre sonuçları iskele denetimidir, iz iddiası değildir (optimize edilmedi).", "",
         "## Cemal'in 7 sorusu", "",
         f"1. Kaç hisse eksiksiz işlendi? Veri hatası ve veri yetersizliği olmayan (kullanılabilir) {oz['kullanilabilir']} / {oz['sembol_ev']}. Veri hatalı {oz['veri_hatali']} (sırasız {oz['sirasiz']}, yinelenen işlem günü {oz['yinelenen_islem_gunlu']}, takvim dışı satır {oz['takvim_disi_satirli']}, NaN fiyat {oz['nan_fiyatli']}, sıfır / negatif fiyat {oz['sifir_negatif_fiyatli']}, negatif hacim {oz['negatif_hacimli']}, OHLC ilişki {oz['ohlc_high_dusuk']} / {oz['ohlc_low_yuksek']} / {oz['ohlc_high_low']}); veri yetersiz {oz['veri_yetersiz']}; olağan piyasa davranışı (bilgi, hata değil) {oz['piyasa_davranisli']}; şüpheli sıçrama {oz['supheli_sicramali']} (muhtemel bölünme {oz['muhtemel_bolunme']}, açıklanamayan {oz['aciklanamayan_sicrama']}; kurumsal işlem verisi {'var' if oz['kurumsal_veri_var'] else 'YOK, kesin sınıflandırma yapılmadı'}).",
         f"2. Kaç hissede tarihsel veri eksik? Fiyat yok {oz['fiyat_yok']}, boş seri {oz['bos_seri']}, kısa seri (< 320) {oz['kisa_seri_320']}, ciddi boşluklu (> 5 işlem günü) {oz['ciddi_bosluklu']} (boşluklu {oz['bosluklu']}, eksik işlem günü toplam {oz['eksik_islem_gunu_toplam']}, en uzun {oz['en_uzun_bosluk_max']}; ABD işlem takvimi, tatiller eksik sayılmaz), eksik hacim payı yüksek {oz['eksik_hacim_pay_yuksek']}, sıfır hacim payı yüksek {oz['sifir_hacim_pay_yuksek']}; K54 kesilmiş seri {oz['kesilmis_k54']}; yükleyici dışı kısa geçmişli {oz.get('dislama_kategorileri', {}).get('kisa_seri_yukleyici', 0)} (K55_EVREN_DISI.csv); özellik penceresi yeterli {oz['ozellik_yeterli']}, sonuç penceresi yeterli Y60 {oz['sonuc_Y60_yeterli']} / Y120 {oz['sonuc_Y120_yeterli']} / Y250 {oz['sonuc_Y250_yeterli']}; olay penceresi eksik {oz['olay_pencere_eksik']}; dönem kapsamı {oz['donem_kapsami']}.",
         f"3. Kaç sembol şirketle güvenilir eşleştirildi? CIK geçerli {oz['cik_eslesen']} / {oz['sembol_ev']} (boş {oz['cik_bos']}, geçersiz {oz['cik_gecersiz']}, bir CIK'ye birden fazla sembol {oz['cik_coklu_sembol']}, sembol yeniden kullanımı (4b) {oz['sembol_yeniden_kullanim']}); şirket adı boş {oz['sec_ad_bos']}; sektör bilinen {oz['sektor_bilinen']} (boş / NaN {oz['sektor_bos']}); seri_erken geçersiz {oz['seri_erken_gecersiz']}; EV yinelenen {oz['ev_yinelenen']}; V'de fazla {oz['v_fazla']}.",
         f"3b. Evren dışı kalanlar (kategori ayrı; K55_EVREN_DISI.csv): {oz.get('dislama_kategorileri', {})}. V / EV çift yönlü tutarlılık: {oz.get('v_ev_tutarlilik', {})}.",
         f"4. Delist olmuş şirketler nasıl ele alındı? Seri erken biten {oz['seri_erken']}; sınıf dağılımı {oz['sinif']} (4a {oz['sinif_4a']}, 4b {oz['sinif_4b']}); seri sonu işlemi (d100 = iflas −%100, d0 = birleşme bedeli, k51 = son kapanış ve negatifse −%30); 4b kod yeniden kullanımı kesimi uygulandı; sınıf 6 dışarıda; olay tanımında tam pencere şartı (seri sonunu aşan pencere tanımsız).",
         f"5. Gelecek bilgisi sızıntısı testleri geçti mi? {'EVET' if all(r.get('gecti') for r in S.values()) else 'HAYIR'} — " + "; ".join(f"{ad}: {'geçti' if r.get('gecti') else 'KALDI'}" for ad, r in S.items()) + ".",
         f"6. Denemede bütün modüller doğru çalıştı mı? {'EVET' if R['moduller_ok'] else 'HAYIR'} — " + "; ".join(f"{m}: {d}" for m, d in R['modul_durum'].items()) + ".",
         f"7. Tam evren koşusunun tahmini süresi ve kaynağı: {tam}.", "",
         "## Süreler (sn)", ""] + [f"- {ad}: {s}" for ad, s in sure.items()]
    L += ["", "## Panel", ""] + [f"- {kk}: {v}" for kk, v in b.items()]
    if len(R.get("kesim", pd.DataFrame())):
        L += ["", "## 4b kod yeniden kullanımı kesimi (kesim öncesi / sonrası satır; kesim günü işlem günü mü)", ""] + tablo(R["kesim"], ["sembol", "kesim", "kesim_islem_gunu", "etkin_kesim", "once", "sonra", "atilan"])
    if len(R.get("orneklem", pd.DataFrame())):
        L += ["", "## Deneme örneklemi dağılımı (tabaka = kaynak × sınıf × likidite üçlüsü; eksik tabaka gizlenmez)", ""] + tablo(R["orneklem"], ["tabaka", "kota", "aday", "secilen", "eksik", "toplam_secilen", "istenen", "evren"])
    L += ["", "## Olay tekilliği ve dönem (purge / embargo) dağılımı", "", f"- {R['tekillik']}", f"- olay × ufuk × dönem: {R.get('olay_donem', {})}"]
    if len(R.get("coklu_test", pd.DataFrame())):
        L += ["", "## Çoklu test yükü (aile = dal × yöntem × dönem; hücre içi Holm, aile içinde BH q = 0,10)", ""] + tablo(R["coklu_test"], ["dal", "yontem", "donem", "hucre", "varyant", "test", "ret"])
    if len(H):
        L += ["", "## Hücre iskelesi (D01-S01 + olumlu / olumsuz kontrol; yalnız pipeline denetimi)", ""]
        L += tablo(H, ["hucre", "yontem", "donem", "ufuk", "n_olay", "n", "n_degisim", "d", "d_alt", "d_ust", "d_alt_blok", "d_ust_blok", "auc", "fark", "fark_alt", "fark_alt_blok", "fark_alt_hisse_ceyrek", "net_fark", "slot_rastgele_yuzdelik", "lift", "eksik_pay", "karar"])
    L += ["", "## Çıktılar", "", "- K55_VERI_KALITESI.csv, K55_VERI_KAPSAMI.md, K55_EVREN.csv, K55_EVREN_DISI.csv (kategori ayrı), K55_KESIM.csv, K55_K54_TUTARLILIK.csv, K55_ORNEKLEM.csv, K55_OLAYLAR.csv.gz, K55_SIZINTI_TESTI.md, K55_HUCRE_ISKELE.csv, K55_COKLU_TEST.csv, K55_KOSU.json (kod / veri / ayar sha), panel/ pickle (repoya girmez)."]
    yol = os.path.join(cikti, "K55_FAZ0_RAPOR.md"); open(yol, "w", encoding="utf-8").write("\n".join(L) + "\n")
    with open(os.path.join(cikti, "K55_KOSU.json"), "w", encoding="utf-8") as f:
        json.dump(k, f, ensure_ascii=False, indent=1, default=str)
    return yol


def faz1_yaz(R: Dict[str, Any], cikti: str) -> str:
    """K55_FAZ1_RAPOR.md + K55_ADAYLAR.md (dal dal; her dal bittiğinde yenilenir). Başarısızlar da yazılır."""
    k = R["kimlik"]; H = R.get("H", pd.DataFrame()); D = R.get("D", pd.DataFrame()); yuk = R.get("yuk", pd.DataFrame()); sure = R.get("sure", {})
    L = [f"# K55 — FAZ 1 RAPORU ({k['kimlik']}; yalnız KEŞİF 2016-21; İÇ DOĞRULAMA ve BAĞIMSIZ açılmadı)", "",
         f"- Kod {k['kod_surum']}; commit {k['commit']}; kilit sha {k['onkayit_sha'][:12]}; ayar sha {k.get('ayar_sha', '')[:12]}; evren sürümü {k['evren_surum'][:12]}; örnek: {k['ayar']['ornek'] or 'tam evren'}.",
         f"- Tamamlanan dallar: {R.get('tamamlanan', [])}; süreler (sn): {sure}; toplam {R.get('toplam_sure_dk', '')} dk.",
         "- Yöntem: A olay öncesi (gün × oynaklık ondalığı içinde z; Cohen d, ay / blok kümeli aralık, bootstrap p, AUC, yıl tekrarı, rejim), B eşleşmiş ileri (beşte bir sinyal, örtüşmez; r60 − kontrol; aralıklar; slot portföyü), C değişim noktası (CUSUM lift). Hücre içi Holm, aile (dal × yöntem × KEŞİF) BH q = 0,10.",
         "- Durum: KEŞİF = A (FDR + ETKİ + yıl tekrarı ≥ 5 / 6 + rejim tutarlı) ya da B (FDR + TUTAR + yıl tekrarı); REDDEDİLDİ; VERİ YETERSİZ; HATA. KEŞİF iz değildir: dallanma (10 alt hücre) ve İÇ DOĞRULAMA sonra.", ""]
    if len(D):
        L += ["## Hücre durumları (özet)", ""] + [f"- {dal}: {g.durum.value_counts().to_dict()}" for dal, g in D.groupby("dal")]
        L += ["", "## KEŞİF adayları", ""]
        K_ = D[D.durum == "KEŞİF"]
        L += tablo(K_, ["hucre", "soru", "A_en_iyi", "A_d", "A_auc", "A_p_holm", "A_q", "B_en_iyi", "B_fark", "B_fark_alt", "B_p_holm", "B_q", "C_lift_max"]) if len(K_) else ["(KEŞİF yok)"]
        L += ["", "## Bütün hücreler", ""] + tablo(D, ["hucre", "durum", "varyant", "A_etki_varyant", "B_tutar_varyant", "C_etki_varyant", "A_en_iyi", "A_d", "A_auc", "A_p_holm", "A_q", "B_en_iyi", "B_fark", "B_fark_alt", "B_q", "C_lift_max", "eksik_pay_max", "not"])
    if len(yuk):
        L += ["", "## Çoklu test yükü (aile = dal × yöntem × dönem)", ""] + tablo(yuk, ["dal", "yontem", "donem", "hucre", "varyant", "test", "ret"])
    if len(H):
        L += ["", "## Varyant satırları (A ve B; tamamı K55_VARYANTLAR.csv)", ""]
        kol = ["hucre", "varyant", "yontem", "ufuk", "n_olay", "n", "d", "d_alt", "d_ust", "auc", "yil_tekrar", "yil_n", "rejim_tutarli", "fark", "fark_alt", "fark_alt_blok", "net_fark", "slot_rastgele_yuzdelik", "p", "p_holm", "q_bh", "ret", "karar"]
        L += tablo(H[H.yontem.isin(["A", "B"])], kol)
        L += ["", "## C değişim noktası satırları", ""] + tablo(H[H.yontem == "C"], ["hucre", "varyant", "ufuk", "n_degisim", "degisim_sonrasi_olay_orani", "taban_orani", "lift", "yanlis_pozitif_pay", "karar"])
    yol = os.path.join(cikti, "K55_FAZ1_RAPOR.md"); open(yol, "w", encoding="utf-8").write("\n".join(L) + "\n")
    A_ = ["# K55 — ADAYLAR (KEŞİF; dallanma ve İÇ DOĞRULAMA bekliyor)", ""] + ([f"- {r.hucre}: {r.soru} — A {r.A_en_iyi} d {_f(r.A_d)} q {_f(r.A_q)}; B {r.B_en_iyi} fark {_f(r.B_fark)} q {_f(r.B_q)}" for r in D[D.durum == "KEŞİF"].itertuples()] if len(D) else [])
    open(os.path.join(cikti, "K55_ADAYLAR.md"), "w", encoding="utf-8").write("\n".join(A_ or ["(yok)"]) + "\n"); return yol
