# S7 PDF'indeki 50 bölgeye Ş9 (U dip + parabolik devam) uygulaması — MÜHÜR
Ana model, 19 Kas 2026. Kaynak: ozellik_Y1_s9.csv.gz (commit 146e278, ön kayıt 5; eşikler iş tanımı 5 §2, ayar yapılmadı). Cemal'in kendi işaretleri bu dosya commit'lenmeden AÇILMADI (bağımsız kıyas). h5 / sonuç okunmadı; yalnız F24-F29.

Özet: U DOĞRU 6 / 50 (ABD 4 / 31, AVR 2 / 9, BIST 0 / 10). En sık neden: dip pencerenin sağ kenarında (x* > 0,75) ve sağ kalkış yok = bölge, çanağın dibi değil düz bir durak; ikinci: gerçek en düşük dip uyum dibinden 6+ bar uzakta (daha derin / daha eski dip).

| No | pazar | Ş9 | neden (tutmayan alt şartlar) |
|---|---|---|---|
| 1 | ABD | U DOĞRU |  |
| 2 | ABD | U DEĞİL | dip kenarda (x* 0.86); sağ kalkmamış (0.5 ATR); gerçek dip uyum dibinden uzak (-9 bar) |
| 3 | ABD | U DEĞİL | dip kenarda (x* 0.90); sağ kalkmamış (0.1 ATR) |
| 4 | ABD | U DEĞİL | dip kenarda (x* 0.76); gerçek dip uyum dibinden uzak (-11 bar) |
| 5 | ABD | U DEĞİL | dip kenarda (x* 0.85); sağ kalkmamış (0.1 ATR); gerçek dip uyum dibinden uzak (-10 bar) |
| 6 | ABD | U DEĞİL | gerçek dip uyum dibinden uzak (-14 bar) |
| 7 | ABD | U DEĞİL | dip kenarda (x* 0.80); gerçek dip uyum dibinden uzak (-6 bar) |
| 8 | ABD | U DEĞİL | gerçek dip uyum dibinden uzak (-14 bar) |
| 9 | ABD | U DEĞİL | uyum zayıf (R² 0.09); sol derinlik az (0.8 ATR); sağ kalkmamış (0.3 ATR); gerçek dip uyum dibinden uzak (+6 bar) |
| 10 | ABD | U DEĞİL | uyum zayıf (R² 0.32); sol derinlik az (0.1 ATR); gerçek dip uyum dibinden uzak (+9 bar) |
| 11 | ABD | U DEĞİL | çanak değil (a<=0) |
| 12 | ABD | U DOĞRU |  |
| 13 | ABD | U DEĞİL | dip kenarda (x* 0.93); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-16 bar) |
| 14 | ABD | U DEĞİL | gerçek dip uyum dibinden uzak (-9 bar) |
| 15 | ABD | U DEĞİL | dip kenarda (x* 1.17); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-19 bar) |
| 16 | ABD | U DEĞİL | dip kenarda (x* 0.86); sağ kalkmamış (0.2 ATR); gerçek dip uyum dibinden uzak (-10 bar) |
| 17 | ABD | U DEĞİL | gerçek dip uyum dibinden uzak (-9 bar) |
| 18 | ABD | U DEĞİL | çanak değil (a<=0) |
| 19 | ABD | U DEĞİL | çanak değil (a<=0) |
| 20 | ABD | U DEĞİL | çanak değil (a<=0) |
| 21 | ABD | U DEĞİL | dip kenarda (x* 0.81); sağ kalkmamış (0.5 ATR); gerçek dip uyum dibinden uzak (-6 bar) |
| 22 | ABD | U DOĞRU |  |
| 23 | ABD | U DEĞİL | çanak değil (a<=0) |
| 24 | ABD | U DEĞİL | dip kenarda (x* 0.98); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-10 bar) |
| 25 | ABD | U DEĞİL | dip kenarda (x* 1.84); uyum zayıf (R² 0.34); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-56 bar) |
| 26 | ABD | U DEĞİL | dip kenarda (x* 29.04); uyum zayıf (R² 0.39); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-1104 bar) |
| 27 | ABD | U DOĞRU |  |
| 28 | ABD | U DEĞİL | uyum zayıf (R² 0.11); sol derinlik az (0.5 ATR); gerçek dip uyum dibinden uzak (-9 bar) |
| 29 | ABD | U DEĞİL | gerçek dip uyum dibinden uzak (+7 bar) |
| 30 | ABD | U DEĞİL | gerçek dip uyum dibinden uzak (-8 bar) |
| 31 | ABD | U DEĞİL | gerçek dip uyum dibinden uzak (-6 bar) |
| 32 | AVR | U DOĞRU |  |
| 33 | AVR | U DEĞİL | çanak değil (a<=0) |
| 34 | AVR | U DEĞİL | dip kenarda (x* 1.86); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-47 bar) |
| 35 | AVR | U DEĞİL | dip kenarda (x* 0.94); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-13 bar) |
| 36 | AVR | U DEĞİL | dip kenarda (x* 1.37); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-28 bar) |
| 37 | AVR | U DOĞRU |  |
| 38 | AVR | U DEĞİL | dip kenarda (x* 1.23); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-17 bar) |
| 39 | AVR | U DEĞİL | uyum zayıf (R² 0.33); sol derinlik az (0.9 ATR); sağ kalkmamış (0.2 ATR) |
| 40 | AVR | U DEĞİL | gerçek dip uyum dibinden uzak (-10 bar) |
| 41 | BIST | U DEĞİL | gerçek dip uyum dibinden uzak (-13 bar) |
| 42 | BIST | U DEĞİL | dip kenarda (x* 0.79); sağ kalkmamış (0.4 ATR) |
| 43 | BIST | U DEĞİL | uyum zayıf (R² 0.33); sol derinlik az (0.5 ATR); sağ kalkmamış (0.5 ATR) |
| 44 | BIST | U DEĞİL | sağ kalkmamış (0.4 ATR); gerçek dip uyum dibinden uzak (-10 bar) |
| 45 | BIST | U DEĞİL | uyum zayıf (R² 0.05); sol derinlik az (0.2 ATR); sağ kalkmamış (0.2 ATR); gerçek dip uyum dibinden uzak (+7 bar) |
| 46 | BIST | U DEĞİL | çanak değil (a<=0) |
| 47 | BIST | U DEĞİL | çanak değil (a<=0) |
| 48 | BIST | U DEĞİL | dip kenarda (x* 1.22); sağ kalkmamış (0.0 ATR); gerçek dip uyum dibinden uzak (-25 bar) |
| 49 | BIST | U DEĞİL | dip kenarda (x* 0.76); sağ kalkmamış (0.2 ATR); gerçek dip uyum dibinden uzak (-20 bar) |
| 50 | BIST | U DEĞİL | çanak değil (a<=0) |
