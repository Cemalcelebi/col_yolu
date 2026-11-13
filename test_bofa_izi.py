"""BOFA_IZI testleri — YALNIZ SENTETİK veri (ağ yok; gerçek fiyat ölçümü yok). Çalıştırma: python test_bofa_izi.py

1) ayrıştırıcı: hisse.net tablo (alım / satım, 'Diğer' sayılmaz, maliyet / pay), hisse.net gün içi satırları ('PAHOL: 16.561.430 lot (...)'),
   YatırımX tablo (Şirket | BIST Kodu | Net Alım Tutarı), Rota Borsa ('Şirket (KOD)' + 'Net alım (TL)'), başka kurum bölümü (HSBC), aracı kurum
   tablosu atlanır; liste türü (gün içi / gün sonu / haftalık) ve veri saati; sayı çözücü
2) giriş günü (seans içi haber -> ertesi açılış, sabah 09:55 öncesi -> aynı gün, hafta sonu -> pazartesi) ve veri günü
3) tutma dönemi: açık dönemde alım haberi yeni dönem açmaz, satış ilk 5 kapatır (ilk 6 kapatmaz), girişten önceki satış haberi sayılmaz,
   250 gün tavanı, açık dönem, kapanıştan sonra yeni dönem; varyant (iki ardışık satış haberinde ilk 3)
4) dönem ölçümü elle: getiri, en yüksek / en düşük, eşli ortalama (aynı hücre, aynı giriş / çıkış), sıra, geç kalma; slot portföy; BH
5) günlük liste seçimi (gün sonu > en geç gün içi), ardışık olay, 60 gün tekilleştirme
6) mühür kapısı: ön kayıt yok / git'te değil / eşik / liste / kod farkı -> RET; commit sonrası geçer
7) izleme tek turu sahte getir ile (ağ yok); çakışma kapısı; kodda e-posta yok; yasak defter dosyalarına yazan kod yok
8) uçtan uca sentetik koşu: ana / varyant / kurum / toplu / BH m / kriz tablosu / rapor; ortalama eşli fark csv'den yeniden üretilir
9-13) BofA KÂRI + YOL (bk_*): temizlik nedenleri ve A tekilleştirme; A getirisi / eş (tipik fiyat) / kriz grubu ve FIFO elle; tetik (haber anı),
   G1 / G2, K1..K6 (geleceğe bakma: tetikten sonra yayımlanan liste sayılmaz), olay / dönem, C1 / C2, yol ölçümü elle; karar kuralı ve kâr
   mühür kapısı; uçtan uca sentetik koşu (7 satır x 4 yol, BH, ikincil, kriz, rapor; sayılar csv'den yeniden üretilir, tohumla birebir)
"""
from __future__ import annotations

import copy
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import BOFA_IZI as B  # noqa: E402

HATA: list = []


def kontrol(kosul: bool, mesaj: str) -> None:
    if not kosul:
        HATA.append(mesaj)


def durmali(fn, mesaj: str, icerik: str = "") -> None:
    try:
        fn()
    except (B.BiHata, RuntimeError) as ex:
        if icerik and icerik not in str(ex):
            HATA.append(f"{mesaj} (yanlış neden: {ex})")
        return
    HATA.append(mesaj)


SAYFA = """<html><head><script type="application/ld+json">{{"datePublished":"{tarih}"}}</script></head><body>
<h1 class="post-title">{baslik}</h1><h2 class="post-spot">{spot}</h2>
<div class="detail-content-inner">{govde}<p><em>Yasal Uyarı: ...</em></p><div>ALTTA LISTE: ZZZZ: 9.999.999 lot</div></div></body></html>"""

HN_TABLO = SAYFA.format(tarih="2026-10-27T19:21:28+03:00", baslik="Bank of America (BofA) gün sonu alım satım listesi", spot="Gün sonu belli oldu", govde="""
<p>BofA gün sonunda net satışla kapattı.</p>
<h2>BOFA&rsquo;NIN EN &Ccedil;OK ALIM YAPTI&#286;I H&#304;SSELER</h2>
<table><thead><tr><th>Hisse</th><th>Net lot</th><th>Pay</th><th>Maliyet (TL)</th></tr></thead><tbody>
<tr><td>PEKGY</td><td>40.428.769</td><td>%29,67</td><td>0,856</td></tr>
<tr><td><a href="x">TSPOR</a></td><td>12.452.635</td><td>%9,14</td><td>0,724</td></tr>
<tr><td>KTLEV</td><td>10.181.310</td><td>%7,47</td><td>4,609</td></tr>
<tr><td>Di&#287;er</td><td>55.084.424</td><td>%40,43</td><td>&mdash;</td></tr></tbody></table>
<h2>BOFA&rsquo;NIN EN &Ccedil;OK SATI&#350; YAPTI&#286;I H&#304;SSELER</h2>
<table><thead><tr><th>Hisse</th><th>Net lot</th><th>Pay</th><th>Maliyet (TL)</th></tr></thead><tbody>
<tr><td>TURSG</td><td>-32.189.870</td><td>%12,05</td><td>3,477</td></tr>
<tr><td>SASA</td><td>-24.255.639</td><td>%9,08</td><td>1,544</td></tr></tbody></table>
<h2>HSBC'N&#304;N EN &Ccedil;OK ALDI&#286;I H&#304;SSELER</h2>
<table><tr><th>Hisse</th><th>Net lot</th></tr><tr><td>THYAO</td><td>1.000.000</td></tr></table>
<h2>KTLEV'DE KURUMLAR</h2>
<table><tr><th>Kurum</th><th>Net lot</th></tr><tr><td>BofA</td><td>1.000</td></tr></table>""")

HN_SATIR = SAYFA.format(tarih="2026-11-02T12:58:58+03:00", baslik="BofA alım tahtasında birinci", spot="", govde="""
<p>Saat 12:25 verilerine g&ouml;re Bank of America net al&#305;m yaptı.</p>
<h2>BOFA'NIN ALIM SEPET&#304;NDE BANKALAR</h2>
<p>En çok net alım:</p>
<p><strong>PAHOL:</strong> 16.561.430 lot (%13,05 pay - ortalama maliyet: 0,649 TL)</p>
<p><strong><a href="y">YKBNK</a>:</strong> 13.045.619 lot (%10,28 pay - ortalama maliyet: 34,874 TL)</p>
<p><strong>Diğer Hisseler:</strong> 74.598.446 lot (%58,79 pay)</p>
<h2>SATI&#350; TARAFINDA &Ccedil;&#304;MENTO</h2>
<p><strong>BTCIM:</strong> -6.635.298 lot (%9,66 pay - ortalama maliyet: 1,401 TL)</p>""")

HN_HAFTA = SAYFA.format(tarih="2026-10-24T13:32:38+03:00", baslik="Bank of America'nın (BofA) haftalık alım satım listesi", spot="", govde="""
<h2>BOFA'NIN EN ÇOK ALDIĞI HİSSELER</h2><table><tr><td>Hisse</td><td>Net lot</td><td>Oran</td><td>Maliyet</td></tr>
<tr><td>YKBNK</td><td>58.670.253</td><td>%10,00</td><td>35,416 TL</td></tr></table>""")

YX = """<html><script>{"datePublished":"2026-11-09T13:33:23+03:00"}</script><h1>BofA'dan 2,33 milyar TL satış</h1>
<div id="x" property="articleBody"><p>9 Kasım saat 12:30 itibarıyla BIST 100 ...</p><h4>BofA'nın En Çok Alım Yaptığı Hisseler</h4>
<figure class="table"><table><tbody><tr><td><strong>Şirket Adı</strong></td><td><strong>BIST Kodu</strong></td><td><strong>Net Alım Tutarı (TL)</strong></td></tr>
<tr><td><strong>Turkcell İletişim A.Ş.</strong></td><td>TCELL</td><td>+146.270.000 TL</td></tr>
<tr><td><strong>Katılımevim A.Ş.</strong></td><td>KTLEV</td><td>+75.920.000 TL</td></tr></tbody></table></figure>
<h4>&nbsp;BofA'nın En Çok Satış Yaptığı Hisseler</h4><figure class="table"><table><tbody>
<tr><td><strong>Şirket Adı</strong></td><td><strong>BIST Kodu</strong></td><td><strong>Net Satış Tutarı (TL)</strong></td></tr>
<tr><td><strong>TÜPRAŞ</strong></td><td>TUPRS</td><td>-793.680.000 TL</td></tr></tbody></table></figure></div></html>"""

ROTA = """<html><script>{"datePublished":"2026-11-03T18:10:58+03:00"}</script><h1>Bank of America (BofA) bu hisselerde yüklü alım yaptı (03.11.2026)</h1>
<div class="entry-content"><p>BofA günü net satışla tamamladı.</p><h2>BofA hangi hisseleri alıyor?</h2>
<h3 class="wp-block-heading">TÜPRAŞ &#8211; Türkiye Petrol Rafinerileri A.Ş. (TUPRS)</h3><figure><img src="a.jpg"/></figure>
<figure class="wp-block-table"><table><tbody><tr><td><strong>Net alım (TL)</strong></td></tr><tr><td>552.991.771</td></tr></tbody></table></figure>
<h3 class="wp-block-heading">Türk Hava Yolları A.O. (THYAO)</h3>
<figure class="wp-block-table"><table><tbody><tr><td><strong>Net alım (TL)</strong></td></tr><tr><td>246.466.851</td></tr></tbody></table></figure>
<div class="related-posts">BofA (ASELS) ...</div></div></html>"""


def t1_ayristirici() -> None:
    G = {"PEKGY", "TSPOR", "KTLEV", "TURSG", "SASA", "THYAO", "PAHOL", "YKBNK", "BTCIM", "TCELL", "TUPRS"}
    M, R = B.bi_ayristir(HN_TABLO, "https://www.hisse.net/haber/bank-of-america-bofa-gun-sonu-alim-satim-listesi-104272", "hissenet", G)
    D = pd.DataFrame(R)
    kontrol(M["tur"] == "gun_sonu", f"tablo haberi gün sonu olmalı: {M['tur']}")
    kontrol(str(M["yayin"]) == "2026-10-27 19:21:28", f"yayın zamanı: {M['yayin']}")
    a = D[(D.kurum == "BofA") & (D.yon == "alim")]
    kontrol(a.hisse.tolist() == ["PEKGY", "TSPOR", "KTLEV"], f"alım sırası / 'Diğer' atlanmalı: {a.hisse.tolist()}")
    kontrol(a.sira.tolist() == [1, 2, 3], "alım sıra 1-3")
    kontrol(abs(a.net.iloc[0] - 40428769) < 1e-6 and abs(a.maliyet.iloc[0] - 0.856) < 1e-9 and abs(a.pay.iloc[0] - 29.67) < 1e-9, "PEKGY değerleri")
    s = D[(D.kurum == "BofA") & (D.yon == "satim")]
    kontrol(s.hisse.tolist() == ["TURSG", "SASA"] and (s.net < 0).all(), f"satış listesi: {s.hisse.tolist()}")
    h = D[D.kurum == "HSBC"]
    kontrol(h.hisse.tolist() == ["THYAO"] and h.yon.iloc[0] == "alim", f"HSBC bölümü ayrı kurum: {h.to_dict('records')}")
    kontrol(M["kurum_tablosu"] == 1 and "ZZZZ" not in D.hisse.tolist(), "aracı kurum tablosu atlanmalı; 'Yasal Uyarı' sonrası okunmamalı")
    kontrol((D.birim == "lot").all() and D.gecerli.all(), "birim lot, kodlar geçerli")
    M, R = B.bi_ayristir(HN_SATIR, "https://www.hisse.net/haber/bofa-alim-104953", "hissenet", G); D = pd.DataFrame(R)
    kontrol(M["tur"] == "gun_ici" and M["veri_saati"] == "12:25", f"gün içi + veri saati: {M['tur']} {M['veri_saati']}")
    a = D[D.yon == "alim"]; s = D[D.yon == "satim"]
    kontrol(a.hisse.tolist() == ["PAHOL", "YKBNK"] and abs(a.maliyet.iloc[1] - 34.874) < 1e-9, f"satır biçimi alım: {a.to_dict('records')}")
    kontrol(s.hisse.tolist() == ["BTCIM"] and s.sira.iloc[0] == 1, f"satır biçimi satış: {s.to_dict('records')}")
    M, R = B.bi_ayristir(HN_HAFTA, "https://www.hisse.net/haber/bank-of-america-nin-bofa-haftalik-alim-satim-listesi-103759", "hissenet", G)
    kontrol(M["tur"] == "haftalik" and len(R) == 1 and R[0]["hisse"] == "YKBNK", f"haftalık: {M['tur']} {R}")
    M, R = B.bi_ayristir(YX, "https://www.yatirimx.com.tr/piyasa/bofadan-x/27876", "yatirimx", G); D = pd.DataFrame(R)
    kontrol(M["tur"] == "gun_ici" and M["veri_saati"] == "12:30", f"YatırımX tür: {M['tur']} {M['veri_saati']}")
    kontrol(D[D.yon == "alim"].hisse.tolist() == ["TCELL", "KTLEV"] and (D.birim == "TL").all(), f"YatırımX alım TL: {D.to_dict('records')}")
    kontrol(D[D.yon == "satim"].hisse.tolist() == ["TUPRS"], "YatırımX satış")
    M, R = B.bi_ayristir(ROTA, "https://rotaborsa.com/bank-of-america-bofa-bu-hisselerde-yuklu-alim-yapti-03-11-2026/", "rotaborsa", G); D = pd.DataFrame(R)
    kontrol(M["tur"] == "gun_sonu", f"Rota gün sonu: {M['tur']}")
    kontrol(D.hisse.tolist() == ["TUPRS", "THYAO"] and D.sira.tolist() == [1, 2] and (D.birim == "TL").all() and (D.yon == "alim").all()
            and abs(D.net.iloc[0] - 552991771) < 1e-6, f"Rota düzeni: {D.to_dict('records')}")
    # sayı çözücü
    for x, b in (("40.428.769", 40428769), ("-32.189.870", -32189870), ("0,856", 0.856), ("%29,67", 29.67), ("1,5 milyar", 1.5e9),
                 ("+146.270.000 TL", 146270000), ("35,416 TL", 35.416), ("−6.635.298", -6635298), ("12", 12)):
        kontrol(abs(B.bi_sayi(x) - b) < 1e-6 * max(1, abs(b)), f"bi_sayi({x}) = {B.bi_sayi(x)} != {b}")
    kontrol(not np.isfinite(B.bi_sayi("—")), "tire NaN")
    kontrol(B.bi_tur("BofA listesi", "", "", pd.Timestamp("2026-11-03 18:20"), None) == "gun_sonu", "18:05 sonrası gün sonu")
    kontrol(B.bi_tur("BofA listesi", "", "", pd.Timestamp("2026-11-03 15:20"), None) == "gun_ici", "seans içi, saat yok -> gün içi")
    kontrol(B.bi_tur("BofA listesi", "", "gün sonunda net satışla kapattı", pd.Timestamp("2026-11-03 17:20"), None) == "gun_sonu", "gün sonu ibaresi")
    kontrol(B.bi_veri_saati(B.bi_norm("BIST 100 11.023,55 puan; saat 15:40 itibarıyla")) == "15:40", "veri saati")
    kontrol(B.bi_veri_saati(B.bi_norm("endeks 11.535 puan, %0,45")) is None, "puan sayısı saat sanılmamalı")
    kontrol(B.bi_aday_url("https://www.hisse.net/haber/bofa-alim-listesi-1") and not B.bi_aday_url("https://www.hisse.net/haber/bofa-altin-raporu-5")
            and B.bi_aday_url("https://www.hisse.net/haber/hsbc-bugun-hangi-hisseleri-aliyor-3"), "URL süzgeci")


def takvim() -> pd.DatetimeIndex:
    return pd.bdate_range("2026-01-05", periods=400)


def t2_giris() -> None:
    T = takvim()
    kontrol(B.bi_giris_gunu(pd.Timestamp("2026-01-05 12:58"), T) == pd.Timestamp("2026-01-06"), "seans içi -> ertesi açılış")
    kontrol(B.bi_giris_gunu(pd.Timestamp("2026-01-06 08:30"), T) == pd.Timestamp("2026-01-06"), "09:55 öncesi -> aynı gün açılış")
    kontrol(B.bi_giris_gunu(pd.Timestamp("2026-01-06 09:56"), T) == pd.Timestamp("2026-01-07"), "09:56 -> ertesi gün")
    kontrol(B.bi_giris_gunu(pd.Timestamp("2026-01-09 19:21"), T) == pd.Timestamp("2026-01-12"), "cuma akşamı -> pazartesi")
    kontrol(B.bi_giris_gunu(pd.Timestamp("2026-01-10 13:32"), T) == pd.Timestamp("2026-01-12"), "cumartesi -> pazartesi")
    kontrol(B.bi_veri_gunu(pd.Timestamp("2026-01-06 08:30"), T) == pd.Timestamp("2026-01-05"), "sabah yayın -> önceki gün verisi")
    kontrol(B.bi_veri_gunu(pd.Timestamp("2026-01-06 19:00"), T) == pd.Timestamp("2026-01-06"), "akşam yayın -> aynı gün")
    kontrol(B.bi_veri_gunu(pd.Timestamp("2026-01-10 13:00"), T) == pd.Timestamp("2026-01-09"), "cumartesi -> cuma")


def L_(sat) -> pd.DataFrame:
    """sat: (haber_id, yayin, tur, yon, sira, hisse, maliyet)."""
    T = takvim()
    L = pd.DataFrame(sat, columns=["haber_id", "yayin", "tur", "yon", "sira", "hisse", "maliyet"])
    L["yayin"] = pd.to_datetime(L.yayin); L["net"] = 1.0
    L["veri_gunu"] = [B.bi_veri_gunu(t, T) for t in L.yayin]; L["giris"] = [B.bi_giris_gunu(t, T) for t in L.yayin]
    return L


def t3_donem() -> None:
    T = takvim()
    L = L_([("h1", "2026-01-05 19:00", "gun_sonu", "alim", 2, "AAA", 1.0),
            ("h1", "2026-01-05 19:00", "gun_sonu", "satim", 1, "BBB", 1.0),
            ("h0", "2026-01-05 21:00", "gun_sonu", "satim", 1, "AAA", 1.0),      # girişten (06.01 10:00) önce: sayılmaz
            ("h2", "2026-01-07 12:00", "gun_ici", "alim", 1, "AAA", 1.1),        # açık dönemde: yeni dönem açmaz
            ("h3", "2026-01-08 19:00", "gun_sonu", "satim", 6, "AAA", 1.0),      # ilk 6: kapatmaz
            ("h4", "2026-01-12 19:00", "gun_sonu", "satim", 5, "AAA", 1.0),      # ilk 5: kapatır -> çıkış 13.01
            ("h5", "2026-01-12 19:30", "gun_sonu", "alim", 1, "AAA", 1.2),       # çıkış haberinden sonra: yeni dönem (13.01)
            ("h6", "2026-01-14 19:00", "gun_sonu", "alim", 4, "CCC", 1.0),       # ilk 4: dönem açmaz
            ("h7", "2026-01-14 19:00", "gun_sonu", "alim", 3, "DDD", 1.0)])
    D = B.bi_donemler(L, T, T[200])
    a = D[D.hisse == "AAA"].reset_index(drop=True)
    kontrol(len(a) == 2, f"AAA iki dönem olmalı: {len(a)}")
    if len(a) == 2:
        kontrol(a.giris[0] == pd.Timestamp("2026-01-06") and a.cikis[0] == pd.Timestamp("2026-01-13") and a.neden[0] == "satis"
                and a.cikis_haber[0] == "h4", f"1. dönem: {a.iloc[0].to_dict()}")
        kontrol(a.giris[1] == pd.Timestamp("2026-01-13") and a.neden[1] == "acik_veri_sonu" and a.cikis[1] == T[200], f"2. dönem açık: {a.iloc[1].to_dict()}")
    kontrol("CCC" not in set(D.hisse) and "DDD" in set(D.hisse), "ilk 3 süzgeci")
    D2 = B.bi_donemler(L, T, T[-1])
    kontrol(len(D2) == len(D) and D2[D2.hisse == "AAA"].neden.tolist()[-1] == "satis_gorulmedi_250", "uzun veride 250 gün tavanı")
    # 250 gün tavanı
    L2 = L_([("h1", "2026-01-05 19:00", "gun_sonu", "alim", 1, "EEE", 1.0)])
    D3 = B.bi_donemler(L2, T, T[-1])
    kontrol(D3.neden.iloc[0] == "satis_gorulmedi_250" and T.get_loc(D3.cikis.iloc[0]) - T.get_loc(D3.giris.iloc[0]) == 250, f"250 gün: {D3.iloc[0].to_dict()}")
    D4 = B.bi_donemler(L2, T, T[100])
    kontrol(D4.neden.iloc[0] == "acik_veri_sonu" and D4.cikis.iloc[0] == T[100], "veri sonu açık dönem")
    # varyant: iki ardışık satış haberinde ilk 3
    L3 = L_([("a1", "2026-01-05 19:00", "gun_sonu", "alim", 1, "FFF", 1.0),
             ("s1", "2026-01-07 19:00", "gun_sonu", "satim", 2, "FFF", 1.0),
             ("s2", "2026-01-08 19:00", "gun_sonu", "satim", 1, "GGG", 1.0),
             ("s3", "2026-01-09 19:00", "gun_sonu", "satim", 3, "FFF", 1.0),
             ("s4", "2026-01-12 12:00", "gun_ici", "satim", 1, "FFF", 1.0)])
    V = B.bi_donemler(L3, T, T[-1], varyant=True)
    kontrol(V.cikis_haber.iloc[0] == "s4" and V.cikis.iloc[0] == pd.Timestamp("2026-01-13"), f"varyant çıkış s3+s4: {V.iloc[0].to_dict()}")
    A_ = B.bi_donemler(L3, T, T[-1])
    kontrol(A_.cikis_haber.iloc[0] == "s1", "ana çıkış ilk satış ilk 5")


def panel_el() -> dict:
    """4 hisse, 12 gün; hepsi aynı hücre (H = 0)."""
    T = pd.bdate_range("2026-03-02", periods=12); n = len(T)
    Op = np.array([[10, 20, 30, 40]] * n, float)
    Op[:, 0] = np.linspace(10, 21, n); Op[:, 1] = 20.0; Op[:, 2] = np.linspace(30, 27, n); Op[5, 3] = np.nan
    Hh = Op * 1.02; Ll = Op * 0.97; Cf = Op.copy(); Cf[5, 3] = 40.0
    Hh[5, 3] = np.nan; Ll[5, 3] = np.nan
    H = np.zeros((n, 4), int); ok = np.isfinite(Op); dd = np.full((n, 4), -0.7)
    return {"tarih": T, "sembol": ["A", "B", "C", "D"], "kol": {"A": 0, "B": 1, "C": 2, "D": 3}, "Op": Op, "Hh": Hh, "Ll": Ll, "Cf": Cf,
            "H": H, "ok": ok, "dd": dd}


def t4_olcum() -> None:
    A = panel_el(); T = A["tarih"]
    X = pd.DataFrame([{"hisse": "A", "giris": T[1], "cikis": T[6], "neden": "satis", "bofa_maliyet": 10.5}])
    Y = B.bi_donem_olc(A, X)
    r = Y.iloc[0]; o = A["Op"]
    kontrol(abs(r.ret - (o[6, 0] / o[1, 0] - 1)) < 1e-12, f"dönem getirisi: {r.ret}")
    kontrol(abs(r["max"] - (np.nanmax(A["Hh"][1:6, 0]) / o[1, 0] - 1)) < 1e-12 and abs(r["min"] - (np.nanmin(A["Ll"][1:6, 0]) / o[1, 0] - 1)) < 1e-12,
            "en yüksek / en düşük çıkış gününden önceki barlar")
    es = [o[6, 1] / o[1, 1] - 1, o[6, 2] / o[1, 2] - 1, o[6, 3] / o[1, 3] - 1]
    kontrol(abs(r.esli - np.mean(es)) < 1e-12 and abs(r.fark - (r.ret - np.mean(es))) < 1e-12, f"eşli: {r.esli} vs {np.mean(es)}")
    kontrol(abs(r.sira - 1.0) < 1e-12 and r.gun == 5 and abs(r.gec - (o[1, 0] / 10.5 - 1)) < 1e-12 and bool(r.cokmus) is True, "sıra / gün / geç kalma / çökmüş")
    # çıkış günü açılış yok -> sonraki açılış
    X2 = pd.DataFrame([{"hisse": "D", "giris": T[1], "cikis": T[5], "neden": "satis", "bofa_maliyet": np.nan}])
    kontrol(abs(B.bi_donem_olc(A, X2).ret.iloc[0] - (A["Op"][6, 3] / A["Op"][1, 3] - 1)) < 1e-12, "durdurmada sonraki açılış")
    # slot portföy
    g = np.array([0, 0, 5]); c = np.array([10, 3, 8]); r_ = np.array([0.1, 0.2, -0.5])
    kontrol(abs(B.bi_slot(g, c, r_, yuva=2) - ((0.5 * 1.1 + 0.5 * 1.2 * 0.5) - 1)) < 1e-12, "slot: yuva çıkışta boşalır")
    kontrol(abs(B.bi_slot(g, c, r_, yuva=1) - 0.1) < 1e-12, "tek yuva doluyken yeni olay alınmaz")
    # BH
    bh = B.bi_bh({"a": 0.001, "b": 0.02, "c": 0.04, "d": 0.5}, 0.10)
    kontrol(bh == {"a": True, "b": True, "c": True, "d": False}, f"BH: {bh}")
    bh = B.bi_bh({"a": 0.03, "b": 0.5, "c": 0.6, "d": 0.9}, 0.10)
    kontrol(bh == {"a": False, "b": False, "c": False, "d": False}, f"BH (0,03 > 0,025): {bh}")
    # bootstrap tohumla birebir, p
    f = np.array([0.1, 0.2, -0.05, 0.3, 0.15, 0.05]); ay = np.array(["a", "a", "b", "b", "c", "c"])
    x1, x2 = B.bi_boot(f, ay), B.bi_boot(f, ay)
    kontrol(x1 == x2 and x1[0] <= f.mean() <= x1[1] and 0 < x1[2] < 0.1, f"bootstrap: {x1}")
    # özet + karar
    rng = np.random.default_rng(1); n = 40
    Z = pd.DataFrame({"hisse": [f"H{i}" for i in range(n)], "giris": pd.bdate_range("2025-09-01", periods=n, freq="5B"),
                      "fark": rng.normal(0.05, 0.02, n), "ret": rng.normal(0.1, 0.1, n), "esli": 0.05, "sira": 0.6, "gun": 10,
                      "max": 0.2, "min": -0.1, "gec": 0.02, "_esler": [np.array([0.0, 0.1])] * n, "olcuk": True, "neden": "satis"})
    Z["cikis"] = Z.giris + pd.Timedelta(days=14)
    o_ = B.bi_donem_ozet(Z, "2026-02-01")
    k = B.bi_donem_karar(o_)
    kontrol(o_["n"] == n and o_["yari_A"]["n"] + o_["yari_B"]["n"] == n and k["karar"].startswith("BofA tutma"), f"karar iz adayı: {k} {o_['yari_A']}")
    Z2 = Z.copy(); Z2.loc[Z2.giris >= "2026-02-01", "fark"] = -0.05
    kontrol(B.bi_donem_karar(B.bi_donem_ozet(Z2, "2026-02-01"))["karar"] == "kanıt yok", "alt dönem ters -> kanıt yok")
    kontrol(B.bi_donem_karar(B.bi_donem_ozet(Z.head(20), "2026-02-01"))["karar"] == "kanıt yok", "n < 30 -> kanıt yok")


def t5_gunluk() -> None:
    T = takvim()
    L = L_([("g1", "2026-01-05 12:00", "gun_ici", "alim", 1, "AAA", 1.0), ("g2", "2026-01-05 15:00", "gun_ici", "alim", 1, "BBB", 1.0),
            ("g3", "2026-01-05 19:00", "gun_sonu", "alim", 1, "CCC", 1.0), ("g4", "2026-01-06 08:00", "gun_sonu", "alim", 1, "DDD", 1.0),
            ("g5", "2026-01-06 14:00", "gun_ici", "alim", 1, "EEE", 1.0), ("g6", "2026-01-06 16:00", "gun_ici", "alim", 2, "CCC", 1.0),
            ("g7", "2026-01-07 19:00", "gun_sonu", "alim", 3, "CCC", 1.0)])
    G = B.bi_gunluk_secim(L)
    s = G.drop_duplicates("veri_gunu").set_index("veri_gunu").haber_id.to_dict()
    kontrol(s.get(pd.Timestamp("2026-01-05")) == "g3", f"gün sonu seçilmeli (en erken; sabahki g4 ikinci): {s}")
    kontrol(s.get(pd.Timestamp("2026-01-06")) == "g6", f"gün sonu yoksa en geç gün içi: {s}")
    X = B.bi_olaylar60(L, T, "alim", 3, 2, 60)
    kontrol(X.hisse.tolist() == ["CCC"] and X.veri_gunu.iloc[0] == pd.Timestamp("2026-01-06"), f"ardışık 2 gün: {X[['hisse', 'veri_gunu']]}")
    X = B.bi_olaylar60(L, T, "alim", 3, 1, 60)
    kontrol(sorted(X.hisse) == ["CCC", "EEE"] or sorted(X.hisse) == ["CCC"], f"tekil: {X.hisse.tolist()}")
    kontrol((X.hisse == "CCC").sum() == 1, "60 günde tek olay")


def t6_kapi() -> None:
    kl = tempfile.mkdtemp(); eski = dict(B.BI_YOL)
    try:
        subprocess.run(["git", "init", "-q", kl], check=True)
        subprocess.run(["git", "-C", kl, "config", "user.email", "t@t"], check=True); subprocess.run(["git", "-C", kl, "config", "user.name", "t"], check=True)
        durmali(lambda: B.bi_kapi(kl), "ön kayıt yokken RET", "ön kayıt yok")
        y = B._bi_yol("onkayit", kl)
        metin = B.bi_onkayit_metin("t", {}, {"liste_sha256": "a" * 64, "haber_sha256": "b" * 64}, {})
        B._bi_yaz(y, metin)
        durmali(lambda: B.bi_kapi(kl), "git'te değilken RET", "işlenmemiş")
        subprocess.run(["git", "-C", kl, "add", "."], check=True); subprocess.run(["git", "-C", kl, "commit", "-qm", "x"], check=True)
        K = B.bi_kapi(kl, liste_sha="a" * 64, haber_sha="b" * 64)
        kontrol(K["kod_ayni"] and len(K["onkayit_git"]["commit"]) == 40, "commit sonrası kapı geçmeli")
        durmali(lambda: B.bi_kapi(kl, liste_sha="c" * 64), "liste farkı RET", "liste")
        durmali(lambda: B.bi_kapi(kl, haber_sha="c" * 64), "haber farkı RET", "haber")
        E2 = copy.deepcopy(B.BI_ESIK); E2["donem"]["cikis_sira"] = 3
        durmali(lambda: B.bi_kapi(kl, E=E2), "eşik değişince RET", "eşik")
        with open(y, encoding="utf-8") as f:
            t = f.read()
        B._bi_yaz(y, re.sub(r"KOD_SHA256: [0-9a-f]{64}", "KOD_SHA256: " + "0" * 64, t))
        subprocess.run(["git", "-C", kl, "commit", "-qam", "y"], check=True)
        durmali(lambda: B.bi_kapi(kl), "kod farkı sapmasız RET", "sapma")
        K = B.bi_kapi(kl, sapma="test"); kontrol(K.get("sapma") == "test", "sapma gerekçesi kayda geçmeli")
        with open(y, "a", encoding="utf-8") as f:
            f.write("ek\n")
        durmali(lambda: B.bi_kapi(kl, sapma="x"), "commit sonrası değişen ön kayıt RET", "farklı")
        durmali(lambda: B._bi_yaz(os.path.join(kl, "IZ_DEFTERI.md"), "x"), "defter dosyasına yazılmamalı", "defter")
        durmali(lambda: B._bi_yaz(os.path.join(kl, "a.md"), "iletisim: kisi" + "@" + "ornek.com"), "e-posta yazılmamalı", "e-posta")
    finally:
        B.BI_YOL.update(eski); shutil.rmtree(kl, ignore_errors=True)


def t7_izle_kapi() -> None:
    xml = ("<urlset><url><loc>https://www.hisse.net/haber/bofa-alim-104953</loc><news:news><news:publication_date>2026-11-02T12:58:58+03:00"
           "</news:publication_date><news:title><![CDATA[ BofA alım tahtasında birinci ]]></news:title></news:news></url>"
           "<url><loc>https://www.hisse.net/haber/dolar-kuru-1</loc><news:news><news:title><![CDATA[ Dolar ]]></news:title></news:news></url></urlset>")
    istek = []

    def getir(u: str):
        istek.append(u)
        return xml if u == B.BI_HABER_HARITA else HN_SATIR
    T, g = B.bi_izle_tur(set(), getir, k=3)
    kontrol(istek == [B.BI_HABER_HARITA, "https://www.hisse.net/haber/bofa-alim-104953"], f"izle istekleri: {istek}")
    kontrol(sorted(T.hisse.tolist()) == ["BTCIM", "PAHOL", "YKBNK"] and "https://www.hisse.net/haber/bofa-alim-104953" in g, f"izle tablo: {T}")
    istek.clear(); T2, _ = B.bi_izle_tur(g, getir)
    kontrol(len(T2) == 0 and len(istek) == 1, "görülen haber yeniden indirilmez")
    kontrol(B.BI_AG["izle_bekle"] >= 60 and B.BI_AG["bekle"] >= 2, "nazik bekleme süreleri")
    # çakışma kapısı
    kod = open(os.path.join(KOK, "BOFA_IZI.py"), encoding="utf-8").read()
    ns = {"__name__": "bofa_test", "__file__": os.path.join(KOK, "BOFA_IZI.py"), "bi_norm": lambda x: x, "_CK_KAYIT": {"bi_norm": "BASKA.py"}}
    try:
        exec(compile(kod, "BOFA_IZI.py", "exec"), ns)
        HATA.append("çakışma kapısı başka dosyanın adını ezince durmalı")
    except RuntimeError as ex:
        kontrol("bi_norm" in str(ex), f"çakışma kapısı nedeni: {ex}")
    ns2 = {"__name__": "bofa_test", "__file__": os.path.join(KOK, "BOFA_IZI.py")}
    exec(compile(kod, "BOFA_IZI.py", "exec"), ns2)
    try:
        exec(compile(kod, "BOFA_IZI.py", "exec"), ns2)
    except RuntimeError as ex:
        HATA.append(f"aynı dosyayı yeniden yüklemek durmamalı: {ex}")
    kontrol(not re.search(r"[\w.+-]+@[\w-]+\.(com|net|org|tr)\b", kod), "kodda e-posta olmamalı")
    for y in B._BI_YASAK:
        kontrol(not re.search(r"open\([^)]*" + re.escape(y), kod), f"{y} dosyasına yazan kod olmamalı")


def t8_uctan_uca() -> None:
    """Sentetik fiyat (40 hisse) + sentetik liste arşivi -> bi_kos (git kapısız, geçici klasör) -> sonuç ve rapor yazılır."""
    rng = np.random.default_rng(5); T = pd.bdate_range("2025-01-02", "2026-11-13"); n = len(T)
    V = {}
    for i in range(40):
        c = 10 * np.exp(np.cumsum(rng.normal(0, 0.02, n))); o = c * (1 + rng.normal(0, 0.003, n))
        V[f"S{i:02d}"] = pd.DataFrame({"Open": o, "High": np.maximum(o, c) * 1.01, "Low": np.minimum(o, c) * 0.99, "Close": c,
                                       "Volume": rng.integers(1e5, 1e7, n).astype(float)}, index=T)
    sat, H = [], []
    gunler = pd.bdate_range("2025-08-04", "2026-11-12", freq="3B")
    for k, g in enumerate(gunler):
        hid = f"h{k}"; y = g + pd.Timedelta(hours=19); kur = "BofA" if k % 4 else "HSBC"
        H.append({"haber_id": hid, "site": "hissenet", "yayin": y, "tur": "gun_sonu", "veri_saati": None, "baslik": "x"})
        al = rng.choice(40, 5, replace=False); st = rng.choice(40, 5, replace=False)
        for j, a in enumerate(al, 1):
            sat.append({"site": "hissenet", "haber_id": hid, "url": "u", "yayin": y, "tur": "gun_sonu", "veri_saati": None, "kurum": kur, "yon": "alim",
                        "blok": 1, "sira": j, "birim": "lot" if k % 2 else "TL", "bicim": "tablo", "hisse": f"S{a:02d}", "net": 1e6, "pay": 1.0,
                        "maliyet": 10.0, "gecerli": True})
        for j, a in enumerate(st, 1):
            sat.append({"site": "hissenet", "haber_id": hid, "url": "u", "yayin": y, "tur": "gun_sonu", "veri_saati": None, "kurum": kur, "yon": "satim",
                        "blok": 1, "sira": j, "birim": "lot", "bicim": "tablo", "hisse": f"S{a:02d}", "net": -1e6, "pay": 1.0, "maliyet": 10.0,
                        "gecerli": True})
    Ld = pd.DataFrame(sat); Hd = pd.DataFrame(H)
    kl = tempfile.mkdtemp(); eski = dict(B.BI_YOL)
    try:
        B.BI_YOL["is"] = kl
        B._bi_yaz(B._bi_yol("onkayit", kl), B.bi_onkayit_metin("t", B.bi_sayim(Ld, Hd, B.bi_takvim(V, 10)), {}, {}))
        S = B.bi_kos(kl, git=False, V=V, F={}, Ld=Ld, Hd=Hd)
        kontrol(S["donem"]["ana"].get("n", 0) >= 30 and "karar" in S and "karar60" in S, f"uçtan uca ana dönem: {S['donem']['ana'].get('n')}")
        kontrol(set(S["kurum"]) >= {"BofA", "HSBC", "TOPLU"} and S["kurum"]["Citi"] == {"veri": "veri yok"}, f"kurum satırları: {list(S['kurum'])}")
        kontrol(S["kurum"]["TOPLU"]["n"] >= S["kurum"]["BofA"]["n"], "toplu satır en az BofA kadar dönem")
        kontrol(S["bh_m"] == 2, f"BH m = 2 (BofA, HSBC): {S['bh_m']}")
        kontrol(0 <= S["olay60"]["alim_ilk3"]["fi"]["sira"] <= 1 and 0 <= S["donem"]["ana"]["sira"] <= 1, "sıra 0-1 arası (liste sırası karışmamalı)")
        kontrol(len(S["kriz"]["donemler"]) > 0 and all(pd.Timestamp(r["giris"]) >= pd.Timestamp("2026-09-01") for r in S["kriz"]["donemler"]),
                "kriz tablosu yalnız Eylül sonrası")
        r = open(B._bi_yol("rapor", kl), encoding="utf-8").read()
        kontrol("KARAR (ana" in r and "Yabancı kodlar" in r and "En erken bilgi" in r, "rapor bölümleri")
        D = pd.read_csv(os.path.join(kl, B.BI_DOSYA["donem"]))
        ana = D[(D.tanim == "ana") & (pd.to_datetime(D.cikis) <= pd.Timestamp("2026-08-31")) & (D.neden != "acik_veri_sonu")]
        kontrol(len(ana) == S["donem"]["ana"]["n_olculen"], "kesik içi dönem sayısı csv ile aynı")
        kontrol(abs(ana.dropna(subset=["fark"]).fark.mean() - S["donem"]["ana"]["ort_fark"]) < 1e-12, "ortalama eşli fark csv'den yeniden üretilir")
    finally:
        B.BI_YOL.update(eski); shutil.rmtree(kl, ignore_errors=True)


# ---------------------------------------------------------------- BofA KÂRI (A) + HABER SONRASI YOL (B) — bk_* (13 Kasım 2026)
def kar_panel(seed: int = 11, n_hisse: int = 100, eksik: tuple = ("S01",)) -> tuple:
    """Sentetik fiyat (n_hisse x iş günleri 2025-01-02 .. 2026-11-13); S01'in V_GUN barı yok. Döner (V, A, takvim, V_GUN)."""
    rng = np.random.default_rng(seed); T = pd.bdate_range("2025-01-02", "2026-11-13"); n = len(T)
    V = {}
    for i in range(n_hisse):
        c = 10 * np.exp(np.cumsum(rng.normal(0, 0.02, n))); o = c * (1 + rng.normal(0, 0.003, n))
        V[f"S{i:02d}"] = pd.DataFrame({"Open": o, "High": np.maximum(o, c) * 1.01, "Low": np.minimum(o, c) * 0.99, "Close": c,
                                       "Volume": rng.integers(1e5, 1e7, n).astype(float)}, index=T)
    vg = T[300]
    for s in eksik:
        V[s] = V[s].drop(index=vg)
    A = B.bi_panel(V); takvim = B.bi_takvim(V, 10)
    return V, A, takvim, vg


def kar_satir(hid, yayin, tur, yon, sira, hisse, net, maliyet=np.nan, pay=np.nan, birim="lot", kurum="BofA", bicim="tablo"):
    return {"site": "hissenet", "haber_id": hid, "url": "u", "yayin": pd.Timestamp(yayin), "tur": tur, "veri_saati": None, "kurum": kurum, "yon": yon,
            "blok": 1, "sira": sira, "birim": birim, "bicim": bicim, "hisse": hisse, "net": net, "pay": pay, "maliyet": maliyet, "gecerli": True}


def t9_kar_temizlik() -> None:
    V, A, takvim, v = kar_panel()
    j0 = A["kol"]["S00"]; i = list(A["tarih"]).index(v); c0 = A["Cf"][i, j0]; h0 = A["Hh"][i, j0]; l0 = A["Ll"][i, j0]
    y = v + pd.Timedelta(hours=19)
    sat = [kar_satir("a1", y, "gun_sonu", "alim", 1, "S00", 2e6, c0),
           kar_satir("a2", y, "gun_sonu", "alim", 2, "S02", 2e6, A["Hh"][i, A["kol"]["S02"]] * 1.05),
           kar_satir("a3", y, "gun_sonu", "alim", 3, "S03", 500, A["Cf"][i, A["kol"]["S03"]]),
           kar_satir("a4", y, "gun_sonu", "alim", 4, "S04", 5000, 10.0 if A["Cf"][i, A["kol"]["S04"]] < 15 else 1.0),
           kar_satir("a5", y, "gun_sonu", "alim", 5, "S05", 5e5, birim="TL"),
           kar_satir("a6", y, "gun_sonu", "alim", 6, "YOKK", 5e6, birim="TL"),
           kar_satir("a7", y, "gun_sonu", "alim", 7, "S06", np.nan),
           kar_satir("a8", y, "gun_sonu", "alim", 8, "S01", 5e6, birim="TL"),
           kar_satir("a9", y, "gun_sonu", "alim", 1, "S07", 5e6, birim="TL", kurum="HSBC"),
           kar_satir("a10", y, "gun_sonu", "satim", 1, "S08", 3e6, birim="TL", bicim="duzyazi")]
    # haftalık: maliyet gün aralığı dışında, hafta aralığında
    jw = A["kol"]["S09"]; lo5, hi5 = np.nanmin(A["Ll"][i - 4:i + 1, jw]), np.nanmax(A["Hh"][i - 4:i + 1, jw])
    mw = hi5 * 1.02 if hi5 * 1.02 > A["Hh"][i, jw] * 1.03 else lo5 * 0.98
    sat.append(kar_satir("w1", v + pd.Timedelta(hours=20), "haftalik", "alim", 1, "S09", 2e6, mw))
    Ld = pd.DataFrame(sat)
    T = B.bk_temizle(Ld, A, takvim)
    nd = dict(zip(T.haber_id, T.neden))
    kontrol(nd == {"a1": "", "a2": "maliyet_bant_disi", "a3": "esik_alti", "a4": "esik_alti", "a5": "esik_alti", "a6": "fiyat_paneli_yok",
                   "a7": "net_yok", "a8": "veri_gunu_bar_yok", "a10": "", "w1": ""}, f"temizlik nedenleri: {nd}")
    kontrol(all(pd.Timestamp(x) == v for x in T.veri_gunu), "veri günü (haftalık da bi_veri_gunu)")
    say = B.bk_temiz_sayim(T)
    kontrol(say["gecerli"] == 3 and say["dusen"]["esik_alti"] == 3 and say["duzyazi_gecerli"] == 1, f"temizlik sayımı: {say}")
    kontrol(abs(c0 - A["Cf"][i, j0]) < 1e-12 and l0 * 0.97 <= c0 <= h0 * 1.03, "geçerli satır bantta")
    # A tekilleştirme: gün sonu (en erken) > gün içi (en geç); haftalık ayrı
    X = pd.DataFrame([kar_satir("g1", v + pd.Timedelta(hours=12), "gun_ici", "alim", 1, "S02", 2e6, 1.0),
                      kar_satir("g2", v + pd.Timedelta(hours=15), "gun_ici", "alim", 1, "S02", 2e6, 1.0),
                      kar_satir("g3", v + pd.Timedelta(hours=19), "gun_sonu", "alim", 1, "S02", 2e6, 1.0),
                      kar_satir("g4", v + pd.Timedelta(days=1, hours=8), "gun_sonu", "alim", 1, "S02", 2e6, 1.0),
                      kar_satir("g5", v + pd.Timedelta(hours=12), "gun_ici", "alim", 1, "S03", 2e6, 1.0),
                      kar_satir("g6", v + pd.Timedelta(hours=16), "gun_ici", "alim", 1, "S03", 2e6, 1.0),
                      kar_satir("g7", v + pd.Timedelta(hours=16), "gun_ici", "satim", 1, "S03", 2e6, 1.0),
                      kar_satir("g8", v + pd.Timedelta(days=1, hours=12), "haftalik", "alim", 1, "S03", 2e6, 1.0)])
    X["veri_gunu"] = v
    Z = B.bk_a_tekil(X)
    kontrol(sorted(Z.haber_id) == ["g3", "g6", "g7", "g8"], f"A tekil: {sorted(Z.haber_id)}")


def t10_kar_a_fifo() -> None:
    V, A, takvim, v = kar_panel()
    i = list(A["tarih"]).index(v); j = A["kol"]["S00"]; mal = A["Cf"][i, j] * 0.99
    X = pd.DataFrame([kar_satir("a", v + pd.Timedelta(hours=19), "gun_sonu", "alim", 1, "S00", 2e6, mal, 25.0)]).assign(veri_gunu=v)
    Y = B.bk_a_olc(A, takvim, X)
    p = list(takvim).index(v); x = list(A["tarih"]).index(takvim[p + 20])
    kontrol(abs(Y.r20.iloc[0] - (A["Cf"][x, j] / mal - 1)) < 1e-12, "A r20 = Kapanış(veri günü + 20) / maliyet - 1")
    c = B._bk_esler(A, i, j); tp = (A["Hh"][i, c] + A["Ll"][i, c] + A["Cf"][i, c]) / 3; e = A["Cf"][x, c] / tp - 1; e = e[np.isfinite(e)]
    kontrol(len(e) >= 3 and abs(Y.e20.iloc[0] - e.mean()) < 1e-12 and abs(Y.f20.iloc[0] - (Y.r20.iloc[0] - e.mean())) < 1e-12, "A eş: tipik fiyattan")
    kontrol(abs(Y.eu20.iloc[0] - (e >= 0.3).mean()) < 1e-12 and Y.grup20.iloc[0] == "ana", f"A eş oranı / grup: {Y.grup20.iloc[0]}")
    kontrol(j not in c and all(A["H"][i, c] == A["H"][i, j]), "eşler aynı hücre, hisse kendisi hariç")
    # kriz sonrası satır: pencere yoksa 'kriz_sonrasi_pencere_yok', varsa 'kriz_sonrasi'
    v2 = takvim[list(takvim).index(pd.Timestamp("2026-09-01")) + 0]; i2 = list(A["tarih"]).index(v2)
    X2 = pd.DataFrame([kar_satir("b", v2 + pd.Timedelta(hours=19), "gun_sonu", "alim", 1, "S00", 2e6, A["Cf"][i2, j])]).assign(veri_gunu=v2)
    Y2 = B.bk_a_olc(A, takvim, X2)
    kontrol(Y2.grup5.iloc[0] == "kriz_sonrasi" and Y2.grup60.iloc[0] == "kriz_sonrasi_pencere_yok" and pd.isna(Y2.r60.iloc[0]),
            f"kriz sonrası grup: {Y2.grup5.iloc[0]}, {Y2.grup60.iloc[0]}")
    v3 = takvim[list(takvim).index(pd.Timestamp("2026-08-24"))]; i3 = list(A["tarih"]).index(v3)
    X3 = pd.DataFrame([kar_satir("c", v3 + pd.Timedelta(hours=19), "gun_sonu", "alim", 1, "S00", 2e6, A["Cf"][i3, j])]).assign(veri_gunu=v3)
    Y3 = B.bk_a_olc(A, takvim, X3)
    kontrol(Y3.grup5.iloc[0] == "ana" and Y3.grup20.iloc[0] == "kesik_asan", f"kesik aşan: {Y3.grup5.iloc[0]}, {Y3.grup20.iloc[0]}")
    o = B.bk_a_ozet(pd.concat([Y, Y3]), 5)
    kontrol(o["n"] == 2 and abs(o["medyan"] - np.median([Y.r5.iloc[0], Y3.r5.iloc[0]])) < 1e-12, "A özet")
    # FIFO elle
    d = takvim[300:306]
    R = pd.DataFrame([kar_satir("f1", d[0] + pd.Timedelta(hours=19), "gun_sonu", "alim", 1, "AAA", 1000, 1.0),
                      kar_satir("f2", d[1] + pd.Timedelta(hours=19), "gun_sonu", "alim", 1, "AAA", 500, 2.0),
                      kar_satir("f3", d[3] + pd.Timedelta(hours=19), "gun_sonu", "satim", 1, "AAA", -1200, 3.0),
                      kar_satir("f4", d[5] + pd.Timedelta(hours=19), "gun_sonu", "satim", 1, "AAA", 500, 1.0)])
    R["veri_gunu"] = [d[0], d[1], d[3], d[5]]
    M, F = B.bk_fifo(R, A, takvim)
    kontrol(len(M) == 3 and np.allclose(M.ret.values, [2.0, 0.5, -0.5]) and np.allclose(M.lot.values, [1000, 200, 300]), f"FIFO eşleşmeler: {M}")
    kontrol(np.allclose(M.gun.values, [3, 2, 4]), f"FIFO tutma günü: {M.gun.values}")
    kontrol(abs(F["tum"]["ret_lot_agirlik"] - 0.95) < 1e-12 and abs(F["kapsam"] - 1500 / 1500) < 1e-12 and abs(F["eslesmeyen_satis_lot"] - 200) < 1e-9,
            f"FIFO özet: {F['tum']}, kapsam {F['kapsam']}, eşleşmeyen {F['eslesmeyen_satis_lot']}")


def t11_kar_tetik_olay() -> None:
    V, A, takvim, v = kar_panel(eksik=())
    tk = list(takvim); p = tk.index(v); D = lambda k: takvim[p + k]  # noqa: E731
    ti = {t: i for i, t in enumerate(A["tarih"])}

    def cf(h, k):
        return A["Cf"][ti[D(k)], A["kol"][h]]
    sat = [kar_satir("t1", D(0) + pd.Timedelta(hours=13), "gun_ici", "alim", 1, "S03", 2e6, cf("S03", 0) * 0.98, 25.0),
           kar_satir("t1b", D(0) + pd.Timedelta(hours=19), "gun_sonu", "alim", 2, "S03", 3e6, cf("S03", 0), 30.0),
           kar_satir("s0", D(0) + pd.Timedelta(hours=10, minutes=30), "gun_ici", "satim", 2, "S03", -2e6, cf("S03", 0), 5.0),
           kar_satir("t2", D(2) + pd.Timedelta(hours=19), "gun_sonu", "alim", 1, "S03", 2e6, cf("S03", 2), 10.0),
           kar_satir("s1", D(3) + pd.Timedelta(hours=19), "gun_sonu", "satim", 4, "S03", -2e6, cf("S03", 3), 5.0),
           kar_satir("t3", D(5) + pd.Timedelta(hours=19), "gun_sonu", "alim", 3, "S03", 2e6, cf("S03", 5) * 0.985, 10.0),
           kar_satir("t4", D(0) + pd.Timedelta(hours=17, minutes=45), "gun_ici", "alim", 1, "S04", 2e6),
           kar_satir("k3a", D(-2) + pd.Timedelta(hours=19), "gun_sonu", "alim", 2, "S05", 5e6, birim="TL"),
           kar_satir("k3b", D(0) + pd.Timedelta(hours=12), "gun_ici", "alim", 1, "S05", 5e6, birim="TL"),
           kar_satir("k3c", D(-1) + pd.Timedelta(hours=12), "gun_ici", "alim", 1, "S06", 5e6, birim="TL"),
           kar_satir("k3d", D(0) + pd.Timedelta(hours=12), "gun_ici", "alim", 2, "S06", 5e6, birim="TL"),
           kar_satir("k3e", D(-6) + pd.Timedelta(hours=19), "gun_sonu", "alim", 1, "S10", 5e6, birim="TL"),
           kar_satir("k3f", D(0) + pd.Timedelta(hours=12), "gun_ici", "alim", 1, "S10", 5e6, birim="TL"),
           kar_satir("k4s", D(-3) + pd.Timedelta(hours=19), "gun_sonu", "satim", 5, "S07", -5e6, birim="TL"),
           kar_satir("k4a", D(0) + pd.Timedelta(hours=12), "gun_ici", "alim", 1, "S07", 5e6, birim="TL"),
           kar_satir("k4t", D(-30) + pd.Timedelta(hours=19), "gun_sonu", "satim", 1, "S08", -5e6, birim="TL"),
           kar_satir("k4b", D(0) + pd.Timedelta(hours=12), "gun_ici", "alim", 1, "S08", 5e6, birim="TL"),
           kar_satir("k4c", D(0) + pd.Timedelta(hours=12), "gun_ici", "alim", 1, "S09", 5e6, birim="TL"),
           kar_satir("k4g", D(0) + pd.Timedelta(hours=15), "gun_ici", "satim", 1, "S09", -5e6, birim="TL"),
           kar_satir("k4h", D(-2) + pd.Timedelta(hours=19), "gun_sonu", "satim", 6, "S11", -5e6, birim="TL"),
           kar_satir("k4i", D(0) + pd.Timedelta(hours=12), "gun_ici", "alim", 1, "S11", 5e6, birim="TL"),
           kar_satir("x4", D(0) + pd.Timedelta(hours=12), "gun_ici", "alim", 4, "S12", 5e6, birim="TL"),
           kar_satir("hf", D(0) + pd.Timedelta(days=1, hours=12), "haftalik", "alim", 1, "S13", 5e6, birim="TL")]
    Ld = pd.DataFrame(sat)
    T = B.bk_temizle(Ld, A, takvim)
    kontrol((T.neden == "").all(), f"tetik testi satırları geçerli olmalı: {T[T.neden != ''][['haber_id', 'neden']]}")
    S5 = B.bk_satis5(Ld, takvim)
    X = B.bk_tetikler(T, S5, A, takvim)
    x = X.set_index("haber_id")
    kontrol("t1b" not in x.index and "x4" not in x.index and "hf" not in x.index, f"tetik: aynı gün ikinci haber / sıra 4 / haftalık tetik değil: {list(x.index)}")
    kontrol(x.loc["t1", "g1"] == D(0) and x.loc["t1", "g1_tip"] == "kapanis" and x.loc["t1", "g2"] == D(1), "G1: gün içi 13:00 -> aynı gün kapanış; G2 ertesi açılış")
    kontrol(x.loc["t4", "g1"] == D(1) and x.loc["t4", "g1_tip"] == "acilis", "G1: 17:45 gün içi -> ertesi açılış")
    kontrol(x.loc["t2", "g1"] == D(3) and x.loc["t2", "g1_tip"] == "acilis", "G1: gün sonu -> ertesi açılış")
    kontrol(x.loc["t1", "K1"] is True or x.loc["t1", "K1"] == True, "K1 pay 25 >= 20")  # noqa: E712
    kontrol(x.loc["t2", "K1"] == False and pd.isna(x.loc["t4", "K1"]), "K1: pay 10 hayır; pay yok bilinmiyor")  # noqa: E712
    kontrol(x.loc["t1", "K2"] == True and abs(x.loc["t1", "g1_fiyat"] - cf("S03", 0)) < 1e-12, "K2: kapanış / maliyet 1/0,98 - 1 <= %5")  # noqa: E712
    kontrol(all((X.K2[i_] == (X.g1_fiyat[i_] / X.maliyet[i_] - 1 <= 0.05)) if np.isfinite(X.maliyet[i_]) else pd.isna(X.K2[i_]) for i_ in X.index),
            "K2 = G1 giriş fiyatı / maliyet - 1 <= %5; maliyet yoksa bilinmiyor")
    kontrol(x.loc["k3b", "K3"] == True and x.loc["k3a", "K3"] == False, "K3: iki farklı gün; ilk gün tek")  # noqa: E712
    kontrol(x.loc["k3c", "K3"] == False and x.loc["k3d", "K3"] == True, "K3: sonraki günün haberi geçmişe sayılmaz (geleceğe bakma yok)")  # noqa: E712
    kontrol(x.loc["k3f", "K3"] == False, "K3: 6 gün önceki liste pencere dışı")  # noqa: E712
    kontrol(x.loc["k4a", "K4"] == True and x.loc["k4b", "K4"] == False and x.loc["k4c", "K4"] == False and x.loc["k4i", "K4"] == False,
            "K4: 3 gün önce satış ilk 5 evet; 30 gün önce hayır; tetikten SONRA yayımlanan satış hayır; satış 6. sıra hayır")
    kontrol(x.loc["t1", "K4"] == True, "K4: aynı gün tetikten önce yayımlanan satış (10:30) sayılır")  # noqa: E712
    kontrol(x.loc["t1", "K6"] == True and x.loc["k3b", "K6"] == False, "K6 birim")  # noqa: E712
    j = A["kol"]["S03"]; d1 = ti[D(0)]
    kontrol((x.loc["t1", "K5"] == (A["dd"][d1 - 1, j] <= -0.6)) if np.isfinite(A["dd"][d1 - 1, j]) else pd.isna(x.loc["t1", "K5"]), "K5 = dd[giriş - 1]")
    # olaylar (TÜMÜ): S03 t1 açar (kapanış girişi 18:10; 10:30 satışı önce, sayılmaz), t2 açıkken yeni dönem açmaz, s1 (4. sıra) kapatır, t3 yeni açar
    ev = B.bk_olaylar(X, S5, takvim)
    e3 = ev[ev.hisse == "S03"].reset_index(drop=True)
    kontrol(len(e3) == 2 and e3.haber_id.tolist() == ["t1", "t3"], f"S03 dönemleri: {e3[['haber_id', 'g1', 'c1', 'c1_neden']]}")
    kontrol(e3.c1.iloc[0] == D(4) and e3.c1_neden.iloc[0] == "satis" and e3.c1_haber.iloc[0] == "s1", f"C1 çıkış: {e3.iloc[0][['c1', 'c1_neden', 'c1_haber']].to_dict()}")
    kontrol(e3.c2.iloc[0] == D(20) and e3.c2_g2.iloc[0] == D(1 + 19), "C2: kapanış girişinde +20, açılış girişinde +19")
    kontrol(e3.c1_neden.iloc[1] in ("satis_gorulmedi_250", "acik_veri_sonu"), "satış yoksa 250 gün / açık")
    # ölçüm elle: G1C1 (kapanış -> açılış), G1C2 (kapanış -> kapanış), G2C1 (açılış -> açılış)
    Y = B.bk_yol_olc(A, e3.head(1), "G1C1"); r = Y.iloc[0]; d, xx = ti[D(0)], ti[D(4)]
    o = A["Cf"][d, j]; ret = A["Op"][xx, j] / o - 1
    kontrol(abs(r.ret - ret) < 1e-12 and r.gun == 4 and r.giris_tip == "kapanis" and r.cikis_tip == "acilis", f"G1C1 getiri: {r.ret} vs {ret}")
    kontrol(abs(r["max"] - (np.nanmax(A["Hh"][d + 1:xx, j]) / o - 1)) < 1e-12, "kapanış girişinde en yüksek giriş ertesinden çıkış öncesine")
    c = B._bk_esler(A, d, j); es = A["Op"][xx, c] / A["Cf"][d, c] - 1; es = es[np.isfinite(es)]
    kontrol(abs(r.esli - es.mean()) < 1e-12 and abs(r.fark - (ret - es.mean())) < 1e-12 and abs(r.b_ret50 - (es >= 0.5).mean()) < 1e-12, "G1C1 eş")
    kontrol(r.liste_sira == 1 and 0 <= r.sira <= 1, "liste sırası ayrı sütun; sıra hücre içi")
    Y2 = B.bk_yol_olc(A, e3.head(1), "G1C2").iloc[0]
    kontrol(abs(Y2.ret - (A["Cf"][ti[D(20)], j] / o - 1)) < 1e-12 and Y2.neden == "sabit_20", "G1C2 getiri")
    Y3 = B.bk_yol_olc(A, e3.head(1), "G2C1").iloc[0]
    kontrol(abs(Y3.ret - (A["Op"][xx, j] / A["Op"][ti[D(1)], j] - 1)) < 1e-12, "G2C1 getiri")
    # koşul alt kümeleri ve tamamlayıcı (None ikisine de girmez)
    k1 = B.bk_kosul_tetik(X, "K1"); k1t = B.bk_kosul_tetik(X, "K1", tamam=True)
    kontrol(set(k1.haber_id) == {"t1"} and "t4" not in set(k1t.haber_id) and "t2" in set(k1t.haber_id), "K1 alt kümesi / tamamlayıcı")
    S = B.bk_b_sayim(X, S5, takvim)
    kontrol(S["tetik"] == len(X) and S["bayrak"]["K1"]["bilinmiyor"] == int(X.K1.isna().sum()) and S["olay"]["TUM"]["toplam"] == len(ev), "B sayımı")


def t12_kar_karar_kapi() -> None:
    o = {"n": 40, "ort_fark": 0.05, "alt95": 0.01, "sira": 0.6, "portfoy": 1.0, "portfoy_esli_p90": 0.5,
         "yari_A": {"n": 20, "ort_fark": 0.04}, "yari_B": {"n": 20, "ort_fark": 0.06}}
    kontrol(B.bk_karar(o, True)["karar"] == "YOL ADAYI (BIST)", "bütün şartlar -> YOL ADAYI (BIST)")
    kontrol(B.bk_karar(o, False)["karar"] == "yol yok", "BH reddetmezse yol yok")
    for k, v in (("sira", 0.5), ("alt95", -0.01), ("portfoy", 0.4), ("ort_fark", -0.01), ("n", 29)):
        o2 = dict(o); o2[k] = v
        kontrol(B.bk_karar(o2, True)["karar"] == "yol yok", f"{k} = {v} -> yol yok")
    o2 = dict(o); o2["yari_A"] = {"n": 20, "ort_fark": -0.01}
    kontrol(B.bk_karar(o2, True)["karar"] == "yol yok", "alt dönem A < 0 -> yol yok")
    kontrol(B.BK_ESIK["karar"]["bh_m"] == len(B.BK_SATIR) == 7, "BH m = 7 satır")
    kl = tempfile.mkdtemp()
    try:
        subprocess.run(["git", "init", "-q", kl], check=True)
        subprocess.run(["git", "-C", kl, "config", "user.email", "t@t"], check=True); subprocess.run(["git", "-C", kl, "config", "user.name", "t"], check=True)
        durmali(lambda: B.bk_kapi(kl), "kâr ön kaydı yokken RET", "ön kaydı yok")
        y = B._bk_yol("onkayit", kl)
        B._bi_yaz(y, B.bk_onkayit_metin("t", {}, {"liste_sha256": "a" * 64, "haber_sha256": "b" * 64}, {}))
        durmali(lambda: B.bk_kapi(kl), "git'te değilken RET", "işlenmemiş")
        subprocess.run(["git", "-C", kl, "add", "."], check=True); subprocess.run(["git", "-C", kl, "commit", "-qm", "x"], check=True)
        K = B.bk_kapi(kl, liste_sha="a" * 64, haber_sha="b" * 64)
        kontrol(K["kod_ayni"] and len(K["onkayit_git"]["commit"]) == 40, "commit sonrası kâr kapısı geçmeli")
        durmali(lambda: B.bk_kapi(kl, liste_sha="c" * 64), "liste farkı RET", "liste")
        E2 = copy.deepcopy(B.BK_ESIK); E2["B"]["K1_pay"] = 15.0
        durmali(lambda: B.bk_kapi(kl, E=E2), "BK eşiği değişince RET", "eşik")
        kontrol(B.bk_esik_sha() != B.bi_esik_sha(), "iki mühür ayrı")
        with open(y, encoding="utf-8") as f:
            t = f.read()
        B._bi_yaz(y, re.sub(r"KOD_SHA256: [0-9a-f]{64}", "KOD_SHA256: " + "0" * 64, t))
        subprocess.run(["git", "-C", kl, "commit", "-qam", "y"], check=True)
        durmali(lambda: B.bk_kapi(kl), "kod farkı sapmasız RET", "sapma")
        kontrol(B.bk_kapi(kl, sapma="g").get("sapma") == "g", "sapma gerekçesi kayda geçmeli")
        with open(y, "a", encoding="utf-8") as f:
            f.write("ek\n")
        durmali(lambda: B.bk_kapi(kl, sapma="x"), "commit sonrası değişen kâr ön kaydı RET", "farklı")
        durmali(lambda: B.bk_onkayit(kl), "var olan ön kaydın üzerine yazılmaz", "zaten var")
    finally:
        shutil.rmtree(kl, ignore_errors=True)


def t13_kar_uctan_uca() -> None:
    """Sentetik fiyat + maliyetli / paylı liste arşivi -> bk_kos (git kapısız) -> A, FIFO, B 7 satır x 4 yol, BH, ikincil, kriz, rapor; sayılar csv'den."""
    V, A, takvim, _ = kar_panel(seed=21, eksik=())
    rng = np.random.default_rng(8); ti = {t: i for i, t in enumerate(A["tarih"])}
    sat, H = [], []
    gunler = [t for t in takvim if pd.Timestamp("2025-06-02") <= t <= pd.Timestamp("2026-11-12")][::2]
    for k, g in enumerate(gunler):
        for tur, saat in (("gun_ici", 13), ("gun_sonu", 19)):
            if tur == "gun_ici" and k % 3:
                continue
            hid = f"h{k}{tur}"; y = g + pd.Timedelta(hours=saat); birim = "lot" if k % 2 else "TL"
            H.append({"haber_id": hid, "site": "hissenet", "yayin": y, "tur": tur, "veri_saati": None, "baslik": "x"})
            for yon in ("alim", "satim"):
                for s_, a in enumerate(rng.choice(100, 5, replace=False), 1):
                    h = f"S{a:02d}"; c = A["Cf"][ti[g], A["kol"][h]]
                    sat.append(kar_satir(hid, y, tur, yon, s_, h, (2e7 if birim == "TL" else 1e6) * (1 if yon == "alim" else -1),
                                         c * rng.uniform(0.985, 1.0) if birim == "lot" else np.nan, float(rng.uniform(5, 40)), birim))
    Ld = pd.DataFrame(sat); Hd = pd.DataFrame(H)
    kl = tempfile.mkdtemp(); eski = dict(B.BI_YOL)
    try:
        B.BI_YOL["is"] = kl
        Hx = B.bk_hazirla(Ld, A, takvim)
        B._bi_yaz(B._bk_yol("onkayit", kl), B.bk_onkayit_metin("t", B.bk_sayim(Hx, takvim), {}, {}))
        S = B.bk_kos(kl, git=False, V=V, F={}, Ld=Ld, Hd=Hd)
        kontrol(set(S["B"]) == set(B.BK_SATIR) and all(set(S["B"][a]["yol"]) == {"G1C1", "G1C2", "G2C1", "G2C2"} for a in B.BK_SATIR), "B satır x yol")
        kontrol(all(S["B"][a]["karar"]["karar"] in ("YOL ADAYI (BIST)", "yol yok") for a in B.BK_SATIR), "B kararları")
        kontrol(S["B"]["TUM"]["yol"]["G1C1"].get("n", 0) >= 30, f"TÜMÜ n: {S['B']['TUM']['yol']['G1C1'].get('n')}")
        kontrol(S["A"]["kirilim"]["20"]["tum"]["n"] > 30 and S["A"]["fifo"]["tum"]["n"] > 0, "A ve FIFO ölçüldü")
        kontrol(all(k in S["ikincil"]["TUM"] for k in ("fi", "karar")), "ikincil 60 gün")
        kontrol(all(pd.Timestamp(r["giris"]) >= pd.Timestamp("2026-09-01") for r in S["kriz"]["donemler"]) and S["kriz"]["n"] > 0, "kriz tablosu")
        r = open(B._bk_yol("rapor", kl), encoding="utf-8").read()
        kontrol(all(x in r for x in ("Özet (düz dil)", "KARAR TABLOSU", "OLASILIK TABLOSU", "FIFO", "Kriz sonrası", "Temizlik sayımı")), "rapor bölümleri")
        Bc = pd.read_csv(os.path.join(kl, B.BK_DOSYA["b"]))
        z = Bc[(Bc.satir == "TUM") & (Bc.yol == "G1C1") & (pd.to_datetime(Bc.cikis) <= pd.Timestamp("2026-08-31")) & (Bc.neden != "acik_veri_sonu")
               & Bc.olcuk.astype(bool)].dropna(subset=["fark"])
        kontrol(len(z) == S["B"]["TUM"]["yol"]["G1C1"]["n"] and abs(z.fark.mean() - S["B"]["TUM"]["yol"]["G1C1"]["ort_fark"]) < 1e-12,
                "B TÜMÜ ortalama eşli fark csv'den yeniden üretilir")
        Ac = pd.read_csv(os.path.join(kl, B.BK_DOSYA["a"]))
        za = Ac[(Ac.yon == "alim") & (Ac.grup20 == "ana")].r20.dropna()
        kontrol(len(za) == S["A"]["kirilim"]["20"]["tum"]["n"] and abs(za.median() - S["A"]["kirilim"]["20"]["tum"]["medyan"]) < 1e-12, "A medyan csv'den")
        o_k = S["B"]["K6"]["yol"]["G1C1"]; zk = Bc[(Bc.satir == "K6") & (Bc.yol == "G1C1")]
        kontrol(o_k.get("n", 0) == 0 or set(zk.birim) == {"lot"}, "K6 olayları yalnız lot listesinden")
        S2 = B.bk_kos(kl, git=False, V=V, F={}, Ld=Ld, Hd=Hd)
        kontrol(S2["B"]["TUM"]["yol"]["G1C1"]["ort_fark"] == S["B"]["TUM"]["yol"]["G1C1"]["ort_fark"] and
                S2["B"]["TUM"]["yol"]["G1C1"]["alt95"] == S["B"]["TUM"]["yol"]["G1C1"]["alt95"], "tohumla birebir tekrar")
    finally:
        B.BI_YOL.update(eski); shutil.rmtree(kl, ignore_errors=True)


if __name__ == "__main__":
    for fn in (t1_ayristirici, t2_giris, t3_donem, t4_olcum, t5_gunluk, t6_kapi, t7_izle_kapi, t8_uctan_uca, t9_kar_temizlik, t10_kar_a_fifo,
               t11_kar_tetik_olay, t12_kar_karar_kapi, t13_kar_uctan_uca):
        try:
            fn()
        except Exception as ex:  # bir test bölümü çökerse ötekiler sürer
            import traceback
            HATA.append(f"{fn.__name__} çöktü: {type(ex).__name__}: {ex}\n{traceback.format_exc()[-1500:]}")
    if HATA:
        print("BAŞARISIZ:\n- " + "\n- ".join(HATA)); sys.exit(1)
    print("test_bofa_izi: tüm testler geçti (13 bölüm)")
