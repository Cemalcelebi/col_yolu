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
        durmali(lambda: B._bi_yaz(os.path.join(kl, "a.md"), "iletisim: kisi@ornek.com"), "e-posta yazılmamalı", "e-posta")
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


if __name__ == "__main__":
    for fn in (t1_ayristirici, t2_giris, t3_donem, t4_olcum, t5_gunluk, t6_kapi, t7_izle_kapi, t8_uctan_uca):
        try:
            fn()
        except Exception as ex:  # bir test bölümü çökerse ötekiler sürer
            import traceback
            HATA.append(f"{fn.__name__} çöktü: {type(ex).__name__}: {ex}\n{traceback.format_exc()[-1500:]}")
    if HATA:
        print("BAŞARISIZ:\n- " + "\n- ".join(HATA)); sys.exit(1)
    print("test_bofa_izi: tüm testler geçti (8 bölüm)")
