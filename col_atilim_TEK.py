from __future__ import annotations
# =====================================================================
#  ÇÖL ATILIM TARAYICISI — ABD ENTEGRE (TEK DOSYA, v2)
#  Tüm bu metni TEK Colab hücresine yapıştır, çalıştır (saniyeler sürer).
#  Sonra AYRI bir hücrede:   hizli_baslat()
#
#  İÇERİK: tarayıcı + düzeltilmiş akümülasyon + ÇÖL/YAYLA/TREND ayrımı
#          + dinamik çöl penceresi + akıllı önbellek + backtest
# =====================================================================
import subprocess as _sp, sys as _sys
_sp.run([_sys.executable, "-m", "pip", "install", "-q", "yfinance", "requests"], check=False)

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple
import logging
import numpy as np
import pandas as pd

log = logging.getLogger("col_tarayici")
if not log.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    log.addHandler(_h)
    log.setLevel(logging.WARNING)


@dataclass
class Config:
    timeframe: str = "4h"
    emalar: Tuple[int, ...] = (20, 50, 200)
    ma_type: str = "sma"
    ema_agirlik: Optional[dict] = None
    ema_period: int = 200
    bars_per_day: int = 3

    # ZORUNLU ÇEKİRDEK
    sert_bosluk: bool = True
    bosluk_dolmasin: bool = False
    col_alt_oran: float = 0.7          # [FLAG] raporlanıyor, çekirdek kapı DEĞİL
    min_gap_pct: float = 0.0
    min_puan: float = 1.0
    tf_gun_carpan: float = 1.5

    # TAZELİK + konum
    sadece_son_gun: bool = True
    max_days_ago: int = 1
    max_fiyat_sapma_pct: float = 0.50

    # AKÜMÜLASYON (çöl fazı)
    col_window: int = 10
    bb_squeeze_pct: float = 0.35
    mini_body_atr: float = 0.50          # gerçek küçük mumlar (gövde <= ATR*0.50)
    flat_max_pct: float = 0.12
    iz_vol_kat: float = 1.5
    breakout_vol_kat: float = 1.5
    net_alim_min: float = 0.55
    w_squeeze: float = 3.0
    w_mini: float = 0.5
    w_accum: float = 4.0
    w_flat: float = 2.0
    w_iz: float = 2.5
    w_breakout: float = 4.0
    w_fitil: float = 3.0
    w_egim: float = 1.5
    w_obv_diverj: float = 5.0
    obv_diverj_min: float = 0.15       # 0.40 iken sadece %3.6 atesliyordu (gercek veri)
    # [DİP+DARALMA BONUSU] fiyat son 1 yılın alt %30'unda VE daralma (BB dar) ise ekstra puan
    dip_pencere: int = 252             # "yıllık" pencere bar sayısı (1d~252; ABD 4h ~ otomatik orantılı)
    dip_esik: float = 0.30             # fiyat konumu < bu => dipte (0=yıl dibi, 1=yıl tepesi)
    w_dip_daralma: float = 3.0         # dip + daralma birlikteyse bonus
    # [YIL-KONUM ÇARPANI] dipte tam puan, tepede ceza (eleme YOK, sadece puan kaybı)
    yk_dip: float = 0.30               # bu konumun altı = tam puan (1.0)
    yk_tepe: float = 0.60              # bu konumun üstü = taban çarpan
    yk_taban: float = 0.40             # tepedeki hissenin alacağı min çarpan

    # GİRİŞ KALİTESİ
    ideal_sapma: float = 8.0
    max_sapma: float = 30.0
    pump_gap: float = 15.0
    pump_vol: float = 20.0
    giris_taban: float = 0.30
    hard_pump_reddet: bool = True
    hard_likidite_reddet: bool = True
    max_olu_oran: float = 0.50
    # [KANAAT KAPISI] sırf yatay/sıkışma puanıyla geçmeyi engelle:
    #   en az bir GÜÇLÜ emare zorunlu -> a_obv_diverj | a_net_alim | a_bosluk_hacim | a_fitil_temiz
    kanaat_kapisi: bool = False        # KAPALI: liste genişlesin; iyiyi sıralama/bonus öne çıkarır
    # [GAP-SMA KAPANIŞ] GAP ile üstüne çıkılan SMA'nın ALTINDA kapanırsa formasyon iptal.
    #   (açılış üstünde + kapanış üstünde = boşluk dolsa da geçerli; kapanış altında = kötü haber/iptal)
    gap_sma_kapanis_reddet: bool = True

    # KALİTE
    kalite_uygula: bool = True
    kalite_pencere: int = 60
    normal_gap_sik: float = 0.15
    cok_gap_sik: float = 0.50
    normal_olu: float = 0.10
    cok_olu: float = 0.40
    kalite_taban: float = 0.15

    use_rsi: bool = False
    use_macd: bool = False
    rsi_period: int = 14
    rsi_min: float = 50.0
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    # ---- TTM Squeeze (Bollinger, Keltner'in icinde) ----
    kc_period: int = 20
    kc_mult: float = 1.5          # Carter standardi
    ttm_oran_min: float = 0.50    # col barlarinin en az %50'si sikisik olmali
    ttm_uzun_bar: int = 20        # bundan uzun sikisma = ekstra puan
    w_ttm: float = 3.0            # sikisma oranina gore puan
    w_ttm_birakma: float = 2.0    # atilim barinda sikisma birakildiysa bonus
    ttm_kapisi: bool = False      # True -> TTM sikismasi ZORUNLU olsun

    bb_period: int = 20
    bb_std: float = 2.0
    vol_ma: int = 20

    min_bars: int = 250
    sabah_son_saat: int = 12
    ogle_son_saat: int = 16
    sadece_seans: Optional[str] = None

    # ---- v2: dinamik col penceresi ----
    dinamik_col: bool = False   # True -> col uzunlugunu otomatik bul (once backtest ile dogrula)
    col_en_az: int = 5
    col_en_cok: int = 120
    col_tol_buyume: float = 0.6

    # ---- v2: yeni bonuslar ----
    yeni_bonus: bool = True
    mini_medyan_esik: float = 0.60
    fitil_govde_kat: float = 1.80
    w_mini_kalite: float = 1.50
    kapanis_esik: float = 0.55
    w_kapanis_accum: float = 2.00
    ub_genislik_esik: float = 0.55
    ub_hacim_dusus: float = 0.80
    w_ubottom: float = 2.50
    ub_min_bar: int = 8       # 15 iken col 10 bar oldugu icin HIC calismiyordu
    ub_skor_min: float = 0.75 # 0.50 iken %63 atesliyordu (orta-dar kosulu tek basina yeterdi)

    # ---- COL / YAYLA / TREND ayrimi ----
    tip_kapisi: str = "col+yayla"   # "kapali" | "col" | "col+yayla"
    er_max: float = 0.35            # ustu = gercekten kayiyor (TREND)
    drift_max: float = 0.06         # col ici net kayma
    ralli_max: float = 0.25         # 60 barlik dipten % kac yukarida
    ralli_pencere: int = 60
    tip_ceza_yayla: float = 0.85    # YAYLA puan carpani
    tip_ceza_trend: float = 0.35    # TREND puan carpani (kapi kapaliysa)


def ema(s, n): return s.ewm(span=n, adjust=False).mean()
def sma(s, n): return s.rolling(n).mean()
def atr(df, n=14):
    h, l, c = df["High"], df["Low"], df["Close"]
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()
def rsi(s, n=14):
    d = s.diff(); up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))
def macd(s, fast=12, slow=26, signal=9):
    line = ema(s, fast) - ema(s, slow); sig = ema(line, signal); return line, sig, line - sig
def _rolling_rank(arr, pencere=100, min_periods=40):
    """BBWrank'in VEKTOREL surumu.

    Eskisi: rolling().apply(lambda w: w.rank(pct=True).iloc[-1])
    -> her hisse icin ~500 pencerede Python dongusu, taramanin en yavas yeri.
    Bu surum sliding_window_view ile ayni sonucu numpy'da tek seferde uretir.
    """
    from numpy.lib.stride_tricks import sliding_window_view
    n = len(arr)
    out = np.full(n, np.nan)
    if n < min_periods:
        return out

    # baslangic (pencere dolmadan once): genisleyen pencere
    for i in range(min_periods - 1, min(pencere - 1, n)):
        w = arr[:i + 1]
        gecerli = w[np.isfinite(w)]
        if len(gecerli) and np.isfinite(arr[i]):
            out[i] = (gecerli <= arr[i]).sum() / len(gecerli)

    if n >= pencere:
        W = sliding_window_view(arr, pencere)          # (n-pencere+1, pencere)
        son = W[:, -1:]
        gecerli = np.isfinite(W)
        say = ((W <= son) & gecerli).sum(axis=1)
        top = gecerli.sum(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            r = np.where(top > 0, say / top, np.nan)
        out[pencere - 1:] = r
    return out


def keltner(df, n=20, mult=1.5, atr_n=20):
    """Keltner Kanali: orta = EMA(kapanis), genislik = ATR tabanli.
       Bollinger kapanislarin STANDART SAPMASINI olcer;
       Keltner ise ATR'yi, yani gercek islem araligini."""
    mid = ema(df["Close"], n)
    rng = atr(df, atr_n)
    return mid + mult * rng, mid - mult * rng


def ttm_squeeze(df, bb_n=20, bb_k=2.0, kc_n=20, kc_mult=1.5):
    """TTM Squeeze (John Carter): Bollinger, Keltner'in ICINE girdiginde True.
         BB_ust < KC_ust  VE  BB_alt > KC_alt
       Anlami: kapanislar sikismis ama gun ici aralik suruyor -> yay geriliyor.
       BBWrank'ten farki: BBWrank yuzdeliktir, tanim geregi barlarin ~%35'inde
       ateslenir. TTM mutlak bir kosuldur, cok daha seyrek ve secicidir."""
    c = df["Close"]
    m = sma(c, bb_n); sd = c.rolling(bb_n).std(ddof=0)
    bb_u, bb_l = m + bb_k * sd, m - bb_k * sd
    kc_u, kc_l = keltner(df, kc_n, kc_mult)
    return (bb_u < kc_u) & (bb_l > kc_l)


def bb_width(s, n=20, k=2.0):
    m = sma(s, n); sd = s.rolling(n).std(ddof=0); return ((m + k * sd) - (m - k * sd)) / m


def _seans(ts, cfg):
    if cfg.bars_per_day == 1:
        return "Günlük"
    try: h = pd.Timestamp(ts).hour
    except Exception: return "?"
    if cfg.bars_per_day == 2:                 # ABD 4h: 2 bar
        return "ABD-Sabah" if h < 20 else "ABD-Öğleden"
    if h < cfg.sabah_son_saat: return "Sabah"
    if h < cfg.ogle_son_saat: return "Öğle"
    return "Akşam(ABD)"


def _agirlik(cfg):
    if cfg.ema_agirlik: return dict(cfg.ema_agirlik)
    return {p: i + 1 for i, p in enumerate(sorted(cfg.emalar))}


@dataclass
class Sonuc:
    eslesti: bool
    atilim_index: Optional[int] = None
    atilim_tarihi: Optional[str] = None
    gun_once: Optional[float] = None
    seans: Optional[str] = None
    puan: float = 0.0
    detay: Dict[str, bool] = field(default_factory=dict)
    notlar: Dict[str, float] = field(default_factory=dict)


def _hazirla(df, cfg):
    if df is None or len(df) < cfg.min_bars:
        return None
    d = df.copy(); c = d["Close"]
    ma = sma if cfg.ma_type == "sma" else ema
    for p in cfg.emalar:
        d[f"EMA{p}"] = ma(c, p)
    d["EMA"] = ma(c, cfg.ema_period)
    d["ATR"] = atr(d)
    d["VOLMA"] = sma(d["Volume"], cfg.vol_ma)
    d["BBW"] = bb_width(c, cfg.bb_period, cfg.bb_std)
    d["BBWrank"] = _rolling_rank(d["BBW"].to_numpy(dtype=float), 100, 40)
    d["BODY"] = (d["Close"] - d["Open"]).abs()
    # TTM Squeeze: Bollinger, Keltner'in icinde mi?
    d["SQZ"] = ttm_squeeze(d, cfg.bb_period, cfg.bb_std,
                           cfg.kc_period, cfg.kc_mult).fillna(False)
    # kac bardir kesintisiz sikisik (sikisma suresi = biriken enerji)
    _s = d["SQZ"].astype(int)
    _grp = (_s != _s.shift()).cumsum()
    d["SQZ_BAR"] = _s.groupby(_grp).cumsum()
    yon = np.sign(d["Close"].diff().fillna(0.0))
    d["OBV"] = (yon * d["Volume"]).cumsum()
    if cfg.use_rsi: d["RSI"] = rsi(c, cfg.rsi_period)
    if cfg.use_macd: _, _, d["MACDh"] = macd(c, cfg.macd_fast, cfg.macd_slow, cfg.macd_signal)
    return d


def tara(df, cfg: Config = Config()) -> Sonuc:
    d = _hazirla(df, cfg)
    if d is None:
        return Sonuc(False, notlar={"hata_yetersiz_bar": float(len(df) if df is not None else 0)})
    last = len(d) - 1
    last_date = d.index[last].normalize()
    window = (1 if cfg.sadece_son_gun else cfg.max_days_ago) * cfg.bars_per_day + 1
    en_iyi = None
    for go in range(0, window + 1):
        D = last - go
        if D < cfg.col_window + 2: break
        if cfg.sadece_son_gun and d.index[D].normalize() != last_date: break
        r = _atilim_kontrol(d, D, go, last, cfg)
        if r.eslesti and (en_iyi is None or r.puan > en_iyi.puan):
            en_iyi = r
    return en_iyi if en_iyi else Sonuc(False, notlar={"sebep_yok": -1.0})


def col_uzunluk_bul(d, D, cfg) -> int:
    """Atilimdan geriye yuruyerek colun GERCEK uzunlugunu bulur.
       Bant toleransi uzunlukla logaritmik genisler: 3 aylik sikisma
       dogal olarak 3 gunlukten genis salinir."""
    en_az, en_cok = cfg.col_en_az, cfg.col_en_cok
    en_iyi = en_az
    for n in range(en_az, min(en_cok, D) + 1):
        seg = d.iloc[D - n:D]
        ort = float(seg["Close"].mean())
        if not ort:
            break
        bant = (float(seg["High"].max()) - float(seg["Low"].min())) / ort
        tol = cfg.flat_max_pct * (1 + np.log(n / en_az) * cfg.col_tol_buyume)
        if bant <= tol:
            en_iyi = n
        else:
            break
    return en_iyi


def _akumulasyon(d, D, cfg):
    """v2 — DUZELTILMIS + COL/YAYLA/TREND siniflandirmasi.

    DUZELTILEN HATALAR (eski surume gore):
      1) OBV: ham kumulatif OBV yerine COL ICI egim.
         (OBVnorm'un 50-100 cikmasinin ve 5 puanin bedava dagilmasinin sebebi)
      2) base["_obv"] = ...  -> SettingWithCopyWarning (binlerce satir). Kaldirildi.
      3) yatay: *100 yapilip 0.12 ile karsilastiriliyordu -> a_yatay hic atesle-
         miyordu. Oran olarak birakildi.
      4) net_alim: OBV'nin ilk degerine bolunuyordu (sifira yakin -> patlama).
         Orijinal anlamina dondu: yukari hacim / toplam hacim, [0,1].
      5) a_bolsuk_hacim yazim hatasi -> a_bosluk_hacim (kanaat kapisi bunu arar)
      6) Bonuslar bayraga bakilmadan puan veriyordu -> artik kosullu
      7) Ciplak except -> except Exception
    """
    _cw = col_uzunluk_bul(d, D, cfg) if cfg.dinamik_col else cfg.col_window
    base = d.iloc[max(0, D - _cw):D]
    prev = d.iloc[D - 1]; row = d.iloc[D]
    det = {}; nt = {"col_bar": float(_cw)}
    if len(base) < max(5, cfg.col_window // 2):
        det["a_col_gercek"] = True
        return 0.0, det, nt

    # ---------------- CEKIRDEK ----------------
    bbr = float(prev["BBWrank"]) if not pd.isna(prev["BBWrank"]) else 1.0
    det["a_sikisma"] = bool(bbr <= cfg.bb_squeeze_pct)
    sikisma_puan = cfg.w_squeeze * (1.0 - bbr) if det["a_sikisma"] else 0.0
    nt["bbw_rank"] = round(bbr, 2)

    # ---- TTM SQUEEZE: Bollinger, Keltner'in icinde mi? ----
    # BBWrank "bu hisse icin normalden dar" der (yuzdelik, ~%35 atesler).
    # TTM ise mutlak bir kosuldur: kapanislar sikismis ama gun ici aralik suruyor.
    sqz = base["SQZ"].to_numpy(dtype=bool)
    ttm_oran = float(sqz.mean()) if len(sqz) else 0.0
    ttm_bar = int(prev["SQZ_BAR"]) if np.isfinite(prev["SQZ_BAR"]) else 0
    det["a_ttm_sikisma"] = bool(ttm_oran >= cfg.ttm_oran_min)
    ttm_puan = cfg.w_ttm * ttm_oran if det["a_ttm_sikisma"] else 0.0
    if det["a_ttm_sikisma"] and ttm_bar >= cfg.ttm_uzun_bar:
        ttm_puan *= 1.5                       # uzun sikisma = daha cok biriken enerji

    # SIKISMA BIRAKMA: onceki bar sikisikti, atilim barinda birakildi.
    # TTM mantiginda asil giris sinyali budur.
    det["a_ttm_birakma"] = bool(bool(prev["SQZ"]) and not bool(row["SQZ"]))
    ttm_birakma_puan = cfg.w_ttm_birakma if det["a_ttm_birakma"] else 0.0

    nt["ttm_oran"] = round(ttm_oran, 2)
    nt["ttm_bar"] = float(ttm_bar)
    nt["ttm_birakma"] = "VAR" if det["a_ttm_birakma"] else "-"

    atr_base = float(base["ATR"].mean())
    body_orani = (float(base["BODY"].mean()) / atr_base) if atr_base else np.nan
    det["a_mini"] = bool(np.isfinite(body_orani) and body_orani <= cfg.mini_body_atr)
    nt["govde_atr"] = round(float(body_orani), 2) if np.isfinite(body_orani) else -1.0

    # [FIX-4] net alim = yukari hacim / toplam hacim -> [0,1]
    up = float(base.loc[base["Close"] >= base["Open"], "Volume"].sum())
    dn = float(base.loc[base["Close"] < base["Open"], "Volume"].sum())
    tot = up + dn
    net_oran = (up / tot) if tot > 0 else 0.0
    det["a_net_alim"] = bool(net_oran >= cfg.net_alim_min)
    nt["net_alim_orani"] = round(net_oran, 2)

    # [FIX-3] oran olarak kalsin (flat_max_pct de oran)
    cmean = float(base["Close"].mean())
    taban = (float(base["High"].max()) - float(base["Low"].min())) / cmean if cmean else np.nan
    det["a_yatay"] = bool(np.isfinite(taban) and taban <= cfg.flat_max_pct)
    nt["taban_genislik"] = round(float(taban) * 100, 1) if np.isfinite(taban) else -1.0

    iz = int(((base["Volume"] > base["VOLMA"] * cfg.iz_vol_kat) &
              (base["Close"] >= base["Open"])).sum())
    det["a_kurum_izi"] = bool(iz >= 1)
    nt["kurum_iz_sayisi"] = float(iz)

    base_vol = float(base["Volume"].mean())
    bvol = float(row["Volume"] / base_vol) if base_vol else 0.0
    det["a_bosluk_hacim"] = bool(bvol >= cfg.breakout_vol_kat)   # [FIX-5]
    nt["bosluk_hacim_kat"] = round(bvol, 2)
    nt["col_vol_ort"] = base_vol if np.isfinite(base_vol) else 0.0

    p_main = min(cfg.emalar)
    if D - 5 >= 0:
        ma_now = float(d.iloc[D][f"EMA{p_main}"]); ma_pre = float(d.iloc[D - 5][f"EMA{p_main}"])
        egim = (ma_now - ma_pre) / ma_pre if ma_pre else 0.0
    else:
        egim = 0.0
    det["a_ma_yukari"] = bool(egim >= -0.005)
    nt["ma_egim_yuzde"] = round(float(egim) * 100, 2)

    # [FIX-1] OBV: ham kumulatif DEGIL, col ici egim / ortalama hacim
    obvw = base["OBV"].to_numpy(dtype=float)
    volw = base["Volume"].to_numpy(dtype=float)
    if len(obvw) >= 5:
        egim_obv = float(np.polyfit(np.arange(len(obvw)), obvw, 1)[0])
        obv_norm = egim_obv / (float(volw.mean()) + 1e-9)
    else:
        obv_norm = 0.0
    c0 = float(base["Close"].iloc[0]); cN = float(base["Close"].iloc[-1])
    fdeg = (cN - c0) / c0 if c0 else 0.0
    diverj = obv_norm * (1.0 + max(0.0, -fdeg) * 8.0) if (obv_norm > 0 and fdeg <= 0.03) else 0.0
    det["a_obv_diverj"] = bool(diverj >= cfg.obv_diverj_min)
    obv_puan = cfg.w_obv_diverj * min(diverj / 1.5, 1.0)
    nt["obv_norm"] = round(float(obv_norm), 3)
    nt["obv_diverj"] = round(float(diverj), 2)

    yil = d.iloc[max(0, D - cfg.dip_pencere):D]
    if len(yil) >= 30:
        yhi = float(yil["High"].max()); ylo = float(yil["Low"].min())
        fiyat = float(d.iloc[D - 1]["Close"])
        konum = (fiyat - ylo) / (yhi - ylo) if (yhi - ylo) > 0 else 1.0
    else:
        konum = 1.0
    det["a_dip_daralma"] = bool(konum <= cfg.dip_esik and det["a_sikisma"])
    dip_puan = cfg.w_dip_daralma if det["a_dip_daralma"] else 0.0
    nt["yil_konum"] = round(float(konum), 2)

    # ---------------- COL / YAYLA / TREND ----------------
    c = base["Close"].to_numpy(dtype=float)
    yol = float(np.abs(np.diff(c)).sum())
    er = (float(abs(c[-1] - c[0])) / yol) if yol > 0 else 0.0   # verimlilik orani
    drift = abs(c[-1] / c[0] - 1.0) if c[0] else 0.0
    pen = d.iloc[max(0, D - cfg.ralli_pencere):D]
    dip_f = float(pen["Low"].min()) if len(pen) else 0.0
    ralli = ((c[-1] - dip_f) / dip_f) if dip_f > 0 else 0.0

    det["a_er_dusuk"]   = bool(er <= cfg.er_max)
    det["a_yatay_akis"] = bool(drift <= cfg.drift_max)
    det["a_dipte"]      = bool(ralli <= cfg.ralli_max)
    duz = det["a_er_dusuk"] and det["a_yatay_akis"]

    if duz and det["a_dipte"]:
        tip = "COL"        # dipte + duz  -> asil aradigin formasyon
    elif duz:
        tip = "YAYLA"      # duz ama ralli sonrasi -> trend ici dinlenme
    else:
        tip = "TREND"      # gercekten kayiyor -> col degil
    det["a_col_gercek"] = bool(tip == "COL")
    nt["ER"] = round(er, 2)
    nt["drift_pct"] = round(drift * 100, 1)
    nt["ralli_pct"] = round(ralli * 100, 1)
    nt["col_tipi"] = tip

    # ---------------- YENI BONUSLAR (hepsi KOSULLU) ----------------
    mini_kalite_puani = kapanis_puani = ub_puani = 0.0
    det["a_mini_kalite"] = det["a_kapanis_accum"] = det["a_ubottom"] = False

    if cfg.yeni_bonus:
        # 1) EMILIM MUMU: govde col medyaninin altinda + fitil baskin
        try:
            med = float(np.median(base["BODY"].to_numpy(dtype=float)))
            son_govde = float(base["BODY"].iloc[-1])
            rel = son_govde / (med + 1e-9)
            r_ = base.iloc[-1]
            ust = float(r_["High"]) - max(float(r_["Open"]), float(r_["Close"]))
            alt = min(float(r_["Open"]), float(r_["Close"])) - float(r_["Low"])
            det["a_mini_kalite"] = bool(rel < cfg.mini_medyan_esik and
                                        (ust + alt) > son_govde * cfg.fitil_govde_kat)
            if det["a_mini_kalite"]:                       # [FIX-6] kosullu
                mini_kalite_puani = cfg.w_mini_kalite * (1.0 - min(rel, 1.0))
            nt["rel_govde"] = round(rel, 2)
        except Exception:
            pass

        # 2) KAPANIS KONUMU + HACIM ASIMETRISI
        try:
            rng_ = (base["High"] - base["Low"]).replace(0, np.nan)
            kap_pos = float(((base["Close"] - base["Low"]) / rng_).mean(skipna=True))
            yuk = base.loc[base["Close"] >= base["Open"], "Volume"].mean()
            dus = base.loc[base["Close"] < base["Open"], "Volume"].mean()
            yuk = float(yuk) if np.isfinite(yuk) else 0.0
            dus = float(dus) if np.isfinite(dus) else 0.0
            asim = yuk / (dus + 1e-9) if dus > 0 else (1.5 if yuk > 0 else 0.0)
            det["a_kapanis_accum"] = bool(np.isfinite(kap_pos) and
                                          kap_pos >= cfg.kapanis_esik and asim >= 1.0)
            if det["a_kapanis_accum"]:
                guc = min((kap_pos - 0.5) / 0.3, 1.0) * min(asim / 1.5, 1.0)
                kapanis_puani = cfg.w_kapanis_accum * max(0.0, guc)
            nt["kapanis_pos"] = round(kap_pos, 2) if np.isfinite(kap_pos) else -1.0
            nt["hacim_asim"] = round(asim, 2)
        except Exception:
            pass

        # 3) U-TABAN: ortada daralma + hacim kurumasi + yukselen dip
        try:
            n = len(base)
            if n >= cfg.ub_min_bar:
                k = n // 3
                sol, orta, sag = base.iloc[:k], base.iloc[k:2 * k], base.iloc[2 * k:]
                tam_ar = float(base["High"].max() - base["Low"].min())
                orta_ar = float(orta["High"].max() - orta["Low"].min())
                skor = 0.0
                if tam_ar > 0 and (orta_ar / tam_ar) < cfg.ub_genislik_esik: skor += 0.5
                if float(orta["Volume"].mean()) < float(sol["Volume"].mean()) * cfg.ub_hacim_dusus:
                    skor += 0.2
                if float(sag["Low"].min()) > float(orta["Low"].min()): skor += 0.15
                if float(sag["Close"].iloc[-1]) > float(orta["High"].max()): skor += 0.15
                det["a_ubottom"] = bool(skor >= cfg.ub_skor_min)
                if det["a_ubottom"]:
                    ub_puani = cfg.w_ubottom * min(skor, 1.0)
                nt["ub_skor"] = round(skor, 2)
        except Exception:
            pass

    # ---------------- TOPLAM ----------------
    if tip != "COL" and det["a_dip_daralma"]:
        dip_puan = 0.0                      # dip bonusu ralli sonrasina gitmesin
        det["a_dip_daralma"] = False

    puan = (sikisma_puan
            + cfg.w_mini * det["a_mini"]
            + cfg.w_accum * det["a_net_alim"]
            + cfg.w_flat * det["a_yatay"]
            + cfg.w_iz * det["a_kurum_izi"]
            + cfg.w_breakout * det["a_bosluk_hacim"]
            + cfg.w_egim * det["a_ma_yukari"]
            + obv_puan + dip_puan + ttm_puan + ttm_birakma_puan
            + mini_kalite_puani + kapanis_puani + ub_puani)

    if tip == "YAYLA":
        puan *= cfg.tip_ceza_yayla
    elif tip == "TREND":
        puan *= cfg.tip_ceza_trend

    nt["mini_kalite_p"] = round(mini_kalite_puani, 2)
    nt["kapanis_p"] = round(kapanis_puani, 2)
    nt["ub_p"] = round(ub_puani, 2)
    return max(0.0, float(puan)), det, nt


def _kalite(d, D, cfg):
    seg = d.iloc[max(0, D - cfg.kalite_pencere):D]
    if len(seg) < 20:
        return 1.0, {}
    o = seg["Open"]; ph = seg["High"].shift(); pl = seg["Low"].shift()
    eps = seg["ATR"].shift() * 0.15
    gapped = (o > ph + eps) | (o < pl - eps)
    gap_sik = float(gapped.mean(skipna=True))
    dead = (seg["High"] == seg["Low"]) | (seg["Volume"] <= 0)
    olu = float(dead.mean())
    if gap_sik <= cfg.normal_gap_sik:
        r = 1.0
    else:
        r = max(cfg.kalite_taban, 1 - (gap_sik - cfg.normal_gap_sik) /
                max(1e-9, cfg.cok_gap_sik - cfg.normal_gap_sik))
    if olu <= cfg.normal_olu:
        lq = 1.0
    else:
        lq = max(cfg.kalite_taban, 1 - (olu - cfg.normal_olu) /
                 max(1e-9, cfg.cok_olu - cfg.normal_olu))
    kal = round(float(r * lq), 3)
    return kal, {"gap_siklik": round(gap_sik * 100, 1), "olu_oran": round(olu * 100, 1)}


def _atilim_kontrol(d, D, gun_once_bar, last, cfg) -> Sonuc:
    row, prev, cur = d.iloc[D], d.iloc[D - 1], d.iloc[last]
    det = {}; nt = {}
    seans_now = _seans(d.index[D], cfg)
    agir = _agirlik(cfg)

    gap_pct = (row["Open"] - prev["High"]) / prev["High"] * 100
    nt["gap_pct"] = round(float(gap_pct), 3)   # [FIX-2] erken yaz
    det["c1_sert_bosluk"] = (bool(row["Open"] > prev["High"]) and (gap_pct >= cfg.min_gap_pct)) if cfg.sert_bosluk else True
    det["c1b_bosluk_dolmamis"] = bool(row["Low"] >= prev["High"]) if cfg.bosluk_dolmasin else True

    gecen = []; ma_puan = 0.0; gap_altinda = []
    for p in cfg.emalar:
        ep_prev = float(prev[f"EMA{p}"]); ep = float(row[f"EMA{p}"])
        gap_ustune = (prev["Close"] < ep_prev) and (row["Open"] > ep)   # GAP ile üstüne çıkılan SMA
        if gap_ustune and (row["Close"] > ep):
            gecen.append(p); ma_puan += agir[p]
        elif gap_ustune and (row["Close"] < ep):
            gap_altinda.append(p)                                       # üstüne gap'ledi ama altında kapadı
    det["c2_ma_gecisi"] = len(gecen) >= 1
    # [GAP-SMA KAPANIŞ] gap'lenen bir SMA altında kapandıysa iptal
    det["c8_gap_sma_kapanis"] = (len(gap_altinda) == 0) if cfg.gap_sma_kapanis_reddet else True
    nt["gap_alti_kapanan"] = ",".join(str(p) for p in sorted(gap_altinda)) if gap_altinda else "-"

    if gecen:
        ref_sma = max(float(row[f"EMA{p}"]) for p in gecen)   # SADECE gap ile geçilen SMA'lar
        det["c2b_onceki_altinda"] = bool(prev["Close"] < ref_sma)
        base = d.iloc[max(0, D - cfg.col_window):D]
        alt_oran = float((base["Close"] < ref_sma).mean()) if len(base) else 0.0
        nt["col_alt_oran"] = round(alt_oran * 100, 0)
    else:
        det["c2b_onceki_altinda"] = False
        nt["col_alt_oran"] = 0.0

    det["c3_taze"] = bool(d.index[D].normalize() == d.index[last].normalize()) if cfg.sadece_son_gun else True

    if gecen:
        en_dusuk_cur = min(float(cur[f"EMA{p}"]) for p in gecen)
        sapma = (cur["Close"] - en_dusuk_cur) / en_dusuk_cur
        det["c4_fiyat_ustte"] = bool((cur["Close"] > en_dusuk_cur) and (sapma <= cfg.max_fiyat_sapma_pct))
        nt["sapma_ma_yuzde"] = round(float(sapma) * 100, 2)
    else:
        det["c4_fiyat_ustte"] = False
        nt["sapma_ma_yuzde"] = 0.0

    akum_puan, adet, ant = _akumulasyon(d, D, cfg)
    det.update(adet); nt.update(ant)

    if gecen:
        en_yuksek_gecen = max(float(row[f"EMA{p}"]) for p in gecen)
        fitil_temiz = bool(row["Low"] >= en_yuksek_gecen)
    else:
        fitil_temiz = False
    det["a_fitil_temiz"] = fitil_temiz
    akum_puan += cfg.w_fitil * fitil_temiz
    nt["fitil"] = "temiz" if fitil_temiz else "delik"

    kalite, knt = _kalite(d, D, cfg) if cfg.kalite_uygula else (1.0, {})
    nt.update(knt)

    ham_puan = ma_puan + akum_puan
    tf_carpan = cfg.tf_gun_carpan if cfg.bars_per_day == 1 else 1.0

    sapma_pct = float(nt.get("sapma_ma_yuzde", 0.0))
    if sapma_pct <= cfg.ideal_sapma:
        f_sapma = 1.0
    else:
        f_sapma = max(cfg.giris_taban, 1 - (sapma_pct - cfg.ideal_sapma) /
                      max(1e-9, cfg.max_sapma - cfg.ideal_sapma))
    f_pump = 1.0
    if gap_pct > cfg.pump_gap:                                   # [FIX-2] yerel gap_pct
        f_pump *= 0.5
    if float(nt.get("bosluk_hacim_kat", 0.0)) > cfg.pump_vol:
        f_pump *= 0.5
    giris_kalite = round(float(f_sapma * f_pump), 2)

    pump = (gap_pct > cfg.pump_gap) or (float(nt.get("bosluk_hacim_kat", 0.0)) > cfg.pump_vol)
    det["c5_pump_degil"] = (not pump) if cfg.hard_pump_reddet else True
    nt["pump"] = bool(pump)

    row_vol = float(row["Volume"])
    col_vol = float(nt.get("col_vol_ort", 0.0))
    olu_oran = float(nt.get("olu_oran", 0.0))
    likit = (row_vol > 0) and (col_vol > 0) and (olu_oran < cfg.max_olu_oran * 100)
    det["c6_likit"] = likit if cfg.hard_likidite_reddet else True

    # [KANAAT KAPISI] en az bir güçlü emare olmalı; yoksa sırf yataylıktan geçmesin
    guclu_emare = bool(det.get("a_obv_diverj") or det.get("a_net_alim")
                       or det.get("a_bosluk_hacim") or det.get("a_fitil_temiz"))
    det["c7_kanaat"] = guclu_emare if cfg.kanaat_kapisi else True
    nt["kanaat"] = "var" if guclu_emare else "yok"

    # [YIL-KONUM ÇARPANI] dipte tam puan, tepede ceza (kademeli, eleme yok)
    yk = float(nt.get("yil_konum", 1.0))
    if yk <= cfg.yk_dip:
        f_konum = 1.0
    elif yk >= cfg.yk_tepe:
        f_konum = cfg.yk_taban
    else:
        # dip ile tepe arasında doğrusal iniş
        f_konum = 1.0 - (yk - cfg.yk_dip) / max(1e-9, cfg.yk_tepe - cfg.yk_dip) * (1.0 - cfg.yk_taban)
    f_konum = round(float(f_konum), 2)
    nt["konum_carpan"] = f_konum

    puan = ham_puan * kalite * tf_carpan * giris_kalite * f_konum
    nt["puan"] = round(float(puan), 2)
    nt["ham_puan"] = round(float(ham_puan), 2)
    nt["ma_puan"] = round(float(ma_puan), 2)
    nt["akum_puan"] = round(float(akum_puan), 2)
    nt["kalite"] = round(float(kalite), 2)
    nt["giris_kalite"] = giris_kalite
    nt["tf"] = "1d" if cfg.bars_per_day == 1 else "4h"
    nt["gecen_emalar"] = ",".join(str(p) for p in sorted(gecen)) if gecen else "-"

    if cfg.use_rsi:
        det["o_rsi"] = bool((row["RSI"] >= cfg.rsi_min) and (row["RSI"] >= prev["RSI"]))
    if cfg.use_macd:
        det["o_macd"] = bool(row["MACDh"] > 0)

    # [TIP KAPISI] COL / YAYLA / TREND
    _tip = nt.get("col_tipi", "COL")
    if cfg.tip_kapisi == "col":
        det["c9_tip"] = bool(_tip == "COL")
    elif cfg.tip_kapisi == "col+yayla":
        det["c9_tip"] = bool(_tip in ("COL", "YAYLA"))
    else:
        det["c9_tip"] = True
    det["c10_ttm"] = bool(det.get("a_ttm_sikisma", False)) if cfg.ttm_kapisi else True

    seans_ok = (cfg.sadece_seans is None) or seans_now.startswith(cfg.sadece_seans)
    cekirdek = (det["c9_tip"] and det["c10_ttm"] and det["c1_sert_bosluk"] and det["c1b_bosluk_dolmamis"] and det["c2_ma_gecisi"]
                and det["c2b_onceki_altinda"] and det["c3_taze"] and det["c4_fiyat_ustte"]
                and det["c5_pump_degil"] and det["c6_likit"] and det["c7_kanaat"]
                and det["c8_gap_sma_kapanis"]
                and (puan >= cfg.min_puan))
    # [FLAG] col_alt_oran kapısını açmak istersen:
    # cekirdek = cekirdek and (nt["col_alt_oran"] >= cfg.col_alt_oran * 100)
    ops_ok = True
    for k in ("o_rsi", "o_macd"):
        if k in det: ops_ok &= det[k]
    eslesti = bool(cekirdek and ops_ok and seans_ok)

    return Sonuc(eslesti=eslesti, atilim_index=D, atilim_tarihi=str(d.index[D]),
                 gun_once=round(gun_once_bar / cfg.bars_per_day, 2), seans=seans_now,
                 puan=float(puan), detay=det, notlar=nt)


def taramayi_calistir(veri, cfg: Config = Config()) -> pd.DataFrame:
    satirlar = []
    for sembol, df in veri.items():
        try:
            r = tara(df, cfg)
        except Exception as e:
            log.warning("%s tarama hatası: %s", sembol, e); continue
        if r.eslesti:
            satirlar.append({
                "Sembol": sembol, "Puan": r.notlar.get("puan"), "TF": r.notlar.get("tf"),
                "Tip": r.notlar.get("col_tipi"), "ÇölBar": r.notlar.get("col_bar"),
                "ER": r.notlar.get("ER"), "Ralli%": r.notlar.get("ralli_pct"),
                "TTM%": r.notlar.get("ttm_oran"), "TTMBar": r.notlar.get("ttm_bar"),
                "TTMBırak": r.notlar.get("ttm_birakma"),
                "Ham": r.notlar.get("ham_puan"), "Kalite": r.notlar.get("kalite"),
                "MA_P": r.notlar.get("ma_puan"), "Akum_P": r.notlar.get("akum_puan"),
                "OBVnorm": r.notlar.get("obv_norm"), "OBVdiv": r.notlar.get("obv_diverj"),
                "GirişK": r.notlar.get("giris_kalite"),
                "GeçenMA": r.notlar.get("gecen_emalar"), "Fitil": r.notlar.get("fitil"),
                "Kanaat": r.notlar.get("kanaat"),
                "YılKonum": r.notlar.get("yil_konum"),
                "KonumÇrp": r.notlar.get("konum_carpan"),
                "ÇölAlt%": r.notlar.get("col_alt_oran"),
                "Gap%": r.notlar.get("gap_pct"), "GapSık%": r.notlar.get("gap_siklik"),
                "Net_Alım": r.notlar.get("net_alim_orani"),
                "BoşHacim×": r.notlar.get("bosluk_hacim_kat"),
                "Atılım": r.atilim_tarihi, "Seans": r.seans,
                "MA Sapma%": r.notlar.get("sapma_ma_yuzde"),
            })
    out = pd.DataFrame(satirlar)
    if not out.empty:
        out = out.sort_values(["Puan", "Gap%"], ascending=[False, False])
    return out


def to_4h(df_1h):
    return df_1h.resample("4h").agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}).dropna()


def america_4h_ozel(df_1h: pd.DataFrame) -> pd.DataFrame:
    """ABD seansını platformdaki gibi 2 bara böler (TR saati):
       1. bar 16:30-20:30 (sabah ABD), 2. bar 20:30-23:00 (öğleden sonra/kapanış ABD).
       yfinance saatlik veriyi Europe/Istanbul'a çevirip ET seansına göre gruplar."""
    df = df_1h.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    idx = pd.DatetimeIndex(df.index)
    try:
        if idx.tz is None:
            idx = idx.tz_localize("UTC")
        idx = idx.tz_convert("Europe/Istanbul").tz_localize(None)
    except Exception:
        pass
    df.index = idx
    h = df.index.hour
    grup = pd.Series(0, index=df.index, dtype=int)
    grup[(h >= 16) & (h < 20)] = 1     # 16:30-20:30 dilimi (sabah ABD)
    grup[(h >= 20) & (h <= 23)] = 2    # 20:30-23:00 dilimi (öğleden sonra ABD)
    df["__grup"] = grup.values
    df["__tarih"] = df.index.normalize()
    df = df[df["__grup"] != 0]
    if df.empty:
        return df.iloc[0:0][["Open", "High", "Low", "Close", "Volume"]]
    g = (df.groupby(["__tarih", "__grup"])
           .agg(Open=("Open", "first"), High=("High", "max"),
                Low=("Low", "min"), Close=("Close", "last"),
                Volume=("Volume", "sum"))
           .reset_index())
    saat = {1: "16:30", 2: "20:30"}
    g["datetime"] = pd.to_datetime(
        g["__tarih"].dt.strftime("%Y-%m-%d") + " " + g["__grup"].map(saat))
    return (g.set_index("datetime").sort_index()
              [["Open", "High", "Low", "Close", "Volume"]])


# =====================================================================
#  ÇALIŞTIRMA KATMANI — BIST
# =====================================================================
import os
import io
import glob
import sys
import time
import pickle

# ============================================================================
#  AYAR  —  ABD İÇİN
# ============================================================================
KAYNAK = "yfinance"        # "yfinance" | "csv"
VERI_KLASORU = "./veri"
EVREN = None               # None => tüm ABD otomatik | ya da ["AAPL","NVDA",...]
EVREN_CSV = "endeks_bilesenleri.csv"
BILESEN_URL = ""
PERIOD = "1y"
TIMEFRAME = "1d"           # ABD => GÜNLÜK (bars_per_day=1)
LIMIT = None              # tüm ABD evreni (UZUN SÜRER, yfinance atlamaları artabilir)
SLEEP = 0.25
DEBUG = True               # True => önce KOŞUL HUNİSİ basar
OTO_CALISTIR = True        # True => hücre çalışınca otomatik yükle + tara (~30 sn, önbellekten)
                           # False => sadece tanımlar yüklensin, taramayı sen tetikle

# --- ÖNBELLEK (Google Drive) ---
USE_CACHE = True           # True => veriyi Drive'a kaydet/oku (aynı gün tekrar indirmez)
FORCE_DOWNLOAD = False     # True => önbelleği yok say, zorla yeniden indir

MARKETS = ["america"]      # <<< ABD
PIYASALAR = {
    "turkey":  {"tv": "turkey",  "suffix": ".IS", "bar": "platform", "min_hacim": 0,       "min_fiyat": 0},
    # ABD EVREN FİLTRESİ — SABİT, DEĞİŞTİRME. ~1600 gerçek hisseye indirir.
    "america": {"tv": "america", "suffix": "",    "bar": "america4h", "min_hacim": 600000,  "min_fiyat": 3},
    "germany": {"tv": "germany", "suffix": ".DE", "bar": "std4h",    "min_hacim": 50000,   "min_fiyat": 1},
}

cfg = Config()
VERI = {}                  # son indirilen veri (bölge röntgeni için global)
# --- ister kalibrasyon ---
# cfg.min_gap_pct = 1.0
# cfg.min_puan = 3.0
# cfg.kalite_uygula = False
# cfg.hard_pump_reddet = False
# cfg.hard_likidite_reddet = False


# ============================================================================
#  EVREN — bileşen tablosundan / canlı / yedek
# ============================================================================
BIST_YEDEK = [
    "GARAN","AKBNK","ISCTR","YKBNK","VAKBN","HALKB","TSKB","SKBNK","ALBRK","ICBCT",
    "KCHOL","SAHOL","DOHOL","AGHOL","GLYHO","ALARK","TKFEN","ECILC","GSDHO","BERA","IHLAS",
    "THYAO","PGSUS","TAVHL","CLEBI","DOCO","RYSAS","BEYAZ",
    "TUPRS","PETKM","SASA","AYGAZ","ENJSA","AKSEN","ODAS","ZOREN","AKENR","AKSUE",
    "MAGEN","BIOEN","ESEN","NATEN","GWIND","AKFYE","ALFAS","CWENE","CANTE","EUPWR","CVKMD",
    "GUBRF","BAGFS","HEKTS","ALKIM","EGGUB",
    "EREGL","KRDMD","ISDMR","SARKY","DOKTA","BURCE","CEMTS","BRSAN","CELHA","KUTPO","IZMDC","DMSAS",
    "TOASO","FROTO","DOAS","OTKAR","TTRAK","KARSN","ASUZU","TMSN","EGEEN","BFREN","PARSN","KATMR","KLMSN",
    "ARCLK","VESTL","VESBE",
    "SISE","CIMSA","AKCNS","OYAKC","NUHCM","GOLTS","BUCIM","BSOKE","CMBTN","AFYON","KONYA","BTCIM","CMENT",
    "ENKAI","ANELE","EDIP","GLRMK","DAPGM",
    "ASELS","ALTNY","TCELL","TTKOM","LOGO","NETAS","ARENA","INDES","KFEIN","ALCTL","ESCOM","DESPC","DGATE",
    "PKART","LINK","PENTA","MIATK","MTRKS","ARDYZ","FONET","KAREL","SMART","OBASE","REEDR",
    "BIMAS","MGROS","SOKM","MAVI","BIZIM","CRFSA","TKNSA","VAKKO","DESA","BOSSA","YATAS","YUNSA","MNDRS","SKTAS","DAGI",
    "ULKER","CCOLA","AEFES","TATGD","PETUN","PINSU","PNSUT","BANVT","TUKAS","KNFRT","SOKE","TBORG",
    "DEVA","SELEC","ECZYT","LKMNH","MPARK","GENIL","ALKLC","EFOR","KTLEV",
    "EKGYO","ISGYO","TRGYO","HLGYO","PEKGY","ZRGYO","VKGYO","KLGYO","RYGYO","NUGYO","AVGYO","DZGYO","OZKGY","SRVGY","AKSGY","SNGYO",
]
BIST_YEDEK = sorted(set(BIST_YEDEK))


def _temizle_kodlar(seri) -> list:
    out = []
    for x in pd.Series(seri).dropna().astype(str):
        k = x.strip().upper().split(".")[0].split(" ")[0]
        if k.isalnum() and 3 <= len(k) <= 6 and not k.isdigit():
            out.append(k)
    return sorted(set(out))


def universe_from_table(df: pd.DataFrame) -> list:
    cols = {str(c).strip().upper(): c for c in df.columns}
    hedef = None
    for key, c in cols.items():
        if ("BILESEN" in key and "KOD" in key) or "CONSTITUENT CODE" in key \
           or key in ("KOD", "CODE", "HISSE KODU", "HISSE", "SEMBOL"):
            hedef = c
            break
    if hedef is None:
        hedef = df.columns[0]
    return _temizle_kodlar(df[hedef])


def universe_from_csv(path: str) -> list:
    for enc in ("utf-8", "latin-1", "cp1254"):
        for sep in (None, ";", ",", "\t"):
            try:
                df = pd.read_csv(path, sep=sep, engine="python", encoding=enc)
                kodlar = universe_from_table(df)
                if len(kodlar) >= 20:
                    return kodlar
            except Exception:
                continue
    return []


def universe_from_url(url: str, timeout: int = 15) -> list:
    import requests
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.borsaistanbul.com/"}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    raw = r.content
    if url.lower().endswith((".xlsx", ".xls")) or raw[:2] == b"PK":
        df = pd.read_excel(io.BytesIO(raw))
        return universe_from_table(df)
    text = raw.decode("utf-8", errors="replace")
    for sep in (None, ";", ",", "\t"):
        try:
            df = pd.read_csv(io.StringIO(text), sep=sep, engine="python")
            kodlar = universe_from_table(df)
            if len(kodlar) >= 20:
                return kodlar
        except Exception:
            continue
    return []


def tv_market_universe(tv_market: str, timeout: int = 20, min_hacim: float = 0, min_fiyat: float = 0) -> list:
    """TradingView tarayıcısından bir piyasanın TÜM hisseleri (auth gerektirmez)."""
    import requests
    url = f"https://scanner.tradingview.com/{tv_market}/scan"
    flt = [{"left": "type", "operation": "in_range", "right": ["stock"]}]
    if min_hacim:
        flt.append({"left": "volume", "operation": "greater", "right": min_hacim})
    if min_fiyat:
        flt.append({"left": "close", "operation": "greater", "right": min_fiyat})
    payload = {
        "filter": flt,
        "options": {"lang": "en"}, "markets": [tv_market],
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": ["name", "close", "volume"], "sort": {"sortBy": "volume", "sortOrder": "desc"},
        "range": [0, 12000],
    }
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json",
               "Origin": "https://www.tradingview.com", "Referer": "https://www.tradingview.com/"}
    r = requests.post(url, json=payload, headers=headers, timeout=timeout)
    r.raise_for_status()
    data = r.json().get("data", []) or []
    kodlar = []
    for row in data:
        s = row.get("s", "")
        if ":" in s:
            kodlar.append(s.split(":")[1])
        elif row.get("d"):
            kodlar.append(str(row["d"][0]))
    return _temizle_kodlar(pd.Series(kodlar))


def bist_universe_tradingview(timeout: int = 15) -> list:
    return tv_market_universe("turkey", timeout)


def bist_universe_live(timeout: int = 12) -> list:
    import requests
    url = ("https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/"
           "Common/Data.aspx/IndexComp?endeks=09%23XUTUM%23")
    headers = {"User-Agent": "Mozilla/5.0",
               "Referer": "https://www.isyatirim.com.tr/",
               "X-Requested-With": "XMLHttpRequest"}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    rows = data.get("value") or data.get("Value") or []
    kodlar = []
    for d in rows:
        kod = (d.get("Hisse Kodu") or d.get("HISSEKODU") or d.get("HisseKodu")
               or d.get("HISSE_KODU") or d.get("code") or d.get("Kod"))
        if kod:
            kodlar.append(str(kod))
    return _temizle_kodlar(pd.Series(kodlar))


def bist_universe() -> list:
    if EVREN_CSV and os.path.exists(EVREN_CSV):
        kodlar = universe_from_csv(EVREN_CSV)
        if kodlar:
            print(f"[evren] '{EVREN_CSV}' tablosundan {len(kodlar)} hisse okundu.")
            return kodlar
        print(f"[evren] '{EVREN_CSV}' okunamadı/uygun değil, diğer kaynaklara geçiliyor.")
    if BILESEN_URL:
        try:
            kodlar = universe_from_url(BILESEN_URL)
            if kodlar:
                print(f"[evren] URL'den {len(kodlar)} hisse alındı.")
                return kodlar
        except Exception as e:
            print(f"[evren] URL alınamadı ({type(e).__name__}).")
    try:
        kodlar = bist_universe_tradingview()
        if len(kodlar) >= 100:
            print(f"[evren] TradingView'den tüm BIST: {len(kodlar)} hisse.")
            return kodlar
        print(f"[evren] TradingView yetersiz ({len(kodlar)}).")
    except Exception as e:
        print(f"[evren] TradingView alınamadı ({type(e).__name__}).")
    try:
        kodlar = bist_universe_live()
        if len(kodlar) >= 100:
            print(f"[evren] Canlı İş Yatırım listesi: {len(kodlar)} hisse.")
            return kodlar
    except Exception as e:
        print(f"[evren] Canlı liste yok ({type(e).__name__}).")
    print(f"[evren] Yedek liste kullanılıyor: {len(BIST_YEDEK)} hisse.")
    return BIST_YEDEK


# ============================================================================
#  PLATFORMUN 3 ÖZEL SEANSINA GÖRE 1h -> "4h" GRUPLAMA
# ============================================================================
def platform_4h_ozel(df_1h: pd.DataFrame) -> pd.DataFrame:
    df = df_1h.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    idx = pd.DatetimeIndex(df.index)
    try:
        if idx.tz is not None:
            idx = idx.tz_convert("Europe/Istanbul").tz_localize(None)
    except Exception:
        pass
    df.index = idx
    h = df.index.hour
    grup = pd.Series(0, index=df.index, dtype=int)
    grup[(h >= 9) & (h <= 11)] = 1
    grup[(h >= 12) & (h <= 15)] = 2
    grup[(h >= 16) & (h <= 18)] = 3
    df["__grup"] = grup.values
    df["__tarih"] = df.index.normalize()
    df = df[df["__grup"] != 0]
    if df.empty:
        return df.iloc[0:0][["Open", "High", "Low", "Close", "Volume"]]
    g = (df.groupby(["__tarih", "__grup"])
           .agg(Open=("Open", "first"), High=("High", "max"),
                Low=("Low", "min"), Close=("Close", "last"),
                Volume=("Volume", "sum"))
           .reset_index())
    saat = {1: "09:55", 2: "12:00", 3: "16:00"}
    g["datetime"] = pd.to_datetime(
        g["__tarih"].dt.strftime("%Y-%m-%d") + " " + g["__grup"].map(saat))
    return (g.set_index("datetime").sort_index()
              [["Open", "High", "Low", "Close", "Volume"]])


# ============================================================================
#  VERİ YÜKLEME
# ============================================================================
def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    tarih_kol = next((c for c in df.columns if c in
                      ("datetime", "date", "time", "tarih", "zaman")), None)
    if tarih_kol:
        df[tarih_kol] = pd.to_datetime(df[tarih_kol])
        df = df.set_index(tarih_kol)
    else:
        df.index = pd.to_datetime(df.index)
    ren = {"open": "Open", "high": "High", "low": "Low",
           "close": "Close", "adj close": "Close",
           "volume": "Volume", "vol": "Volume", "hacim": "Volume",
           "açılış": "Open", "yüksek": "High", "düşük": "Low", "kapanış": "Close"}
    df = df.rename(columns=ren)
    eksik = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c not in df.columns]
    if eksik:
        raise ValueError(f"Eksik sütun(lar): {eksik}")
    return df[["Open", "High", "Low", "Close", "Volume"]].sort_index().dropna()


def csv_yukle(klasor: str) -> dict:
    veri = {}
    yollar = sorted(glob.glob(os.path.join(klasor, "*.csv")))
    if not yollar:
        sys.exit(f"'{klasor}' içinde CSV bulunamadı.")
    for yol in yollar:
        sembol = os.path.splitext(os.path.basename(yol))[0].upper()
        try:
            veri[sembol] = _normalize(pd.read_csv(yol))
        except Exception as e:
            print(f"[ATLA] {sembol}: {e}")
    return veri


def evren_coklu() -> list:
    cikti = []
    for mk in MARKETS:
        if mk not in PIYASALAR:
            print(f"[evren] bilinmeyen piyasa atlandı: {mk}"); continue
        if mk == "turkey":
            kodlar = EVREN if EVREN else bist_universe()
        else:
            try:
                meta = PIYASALAR[mk]
                kodlar = tv_market_universe(meta["tv"], min_hacim=meta.get("min_hacim", 0),
                                            min_fiyat=meta.get("min_fiyat", 0))
            except Exception as e:
                print(f"[evren] {mk} alınamadı ({type(e).__name__})"); kodlar = []
        print(f"[evren] {mk}: {len(kodlar)} hisse")
        if mk != "turkey" and len(kodlar) > 800:
            print(f"  (uyarı: {mk} çok büyük; LIMIT kullanmazsan indirme çok uzun sürer)")
        for k in kodlar:
            cikti.append((k, mk))
    return cikti


def yfinance_yukle(evren: list) -> dict:
    import yfinance as yf
    import logging as _lg
    _lg.getLogger("yfinance").setLevel(_lg.CRITICAL)
    veri = {}
    toplam = len(evren)
    atlanan = 0
    for i, (s, mk) in enumerate(evren, 1):
        if i % 25 == 0 or i == toplam:
            print(f"  ...indiriliyor {i}/{toplam}  (bulunan: {len(veri)}, atlanan: {atlanan})")
        meta = PIYASALAR[mk]
        yt = f"{s}{meta['suffix']}"
        try:
            if TIMEFRAME == "1d":
                dfd = yf.download(yt, period=GUNLUK_PERIOD, interval="1d",
                                  auto_adjust=False, progress=False)
                if dfd is None or dfd.empty:
                    atlanan += 1; time.sleep(SLEEP); continue
                if isinstance(dfd.columns, pd.MultiIndex):
                    dfd.columns = dfd.columns.get_level_values(0)
                df_son = dfd.rename(columns=str.title)[["Open", "High", "Low", "Close", "Volume"]].dropna()
            else:
                df1h = yf.download(yt, period=PERIOD, interval="1h",
                                   auto_adjust=False, progress=False)
                if df1h is None or df1h.empty:
                    atlanan += 1; time.sleep(SLEEP); continue
                if isinstance(df1h.columns, pd.MultiIndex):
                    df1h.columns = df1h.columns.get_level_values(0)
                df1h = df1h.rename(columns=str.title)[["Open", "High", "Low", "Close", "Volume"]].dropna()
                if meta["bar"] == "platform":
                    df_son = platform_4h_ozel(df1h)
                elif meta["bar"] == "america4h":
                    df_son = america_4h_ozel(df1h)
                else:
                    df_son = to_4h(df1h)
            if len(df_son) >= cfg.min_bars:
                anahtar = s if mk == "turkey" else f"{s}.{mk[:2].upper()}"
                veri[anahtar] = df_son
            else:
                atlanan += 1
        except Exception:
            atlanan += 1
        time.sleep(SLEEP)
    return veri


def _cache_dir():
    try:
        from google.colab import drive  # type: ignore
        if not os.path.exists("/content/drive/MyDrive"):
            drive.mount("/content/drive")
        cd = "/content/drive/MyDrive/col_tarayici"
    except Exception:
        cd = "."
    os.makedirs(cd, exist_ok=True)
    return cd


def _cache_yolu():
    mk = MARKETS[0] if MARKETS else "x"
    return os.path.join(_cache_dir(), f"veri_{TIMEFRAME}_{mk}.pkl")


def son_islem_gunu(simdi=None):
    """Beklenen en son bar tarihi. Hafta sonu -> Cuma.
       Piyasa henuz kapanmadiysa -> dun."""
    t = pd.Timestamp.now() if simdi is None else pd.Timestamp(simdi)
    kapanis = 23 if "america" in MARKETS else 18
    g = t.normalize()
    if t.hour < kapanis:
        g -= pd.Timedelta(days=1)
    while g.weekday() >= 5:
        g -= pd.Timedelta(days=1)
    return g


def onbellek_oku() -> dict:
    yol = _cache_yolu()
    if os.path.exists(yol):
        try:
            with open(yol, "rb") as f:
                p = pickle.load(f)
            return p.get("veri", {}) if isinstance(p, dict) else {}
        except Exception as e:
            print(f"[cache] okunamadi ({type(e).__name__})")
    mk = MARKETS[0] if MARKETS else "x"
    for alt in sorted(glob.glob(os.path.join(_cache_dir(), f"veri_{TIMEFRAME}_{mk}*.pkl"))):
        try:
            with open(alt, "rb") as f:
                p = pickle.load(f)
            v = p.get("veri", {}) if isinstance(p, dict) else {}
            if v:
                print(f"[cache] eski dosyadan devralindi: {os.path.basename(alt)} ({len(v)})")
                return v
        except Exception:
            continue
    return {}


def onbellek_yaz(veri: dict, sessiz=False):
    """Atomik yazma: once .tmp, sonra rename. Yazarken kopsa bile
       eski dosya bozulmaz."""
    yol = _cache_yolu(); tmp = yol + ".tmp"
    try:
        with open(tmp, "wb") as f:
            pickle.dump({"kayit": str(pd.Timestamp.now()), "veri": veri}, f,
                        protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, yol)
        if not sessiz:
            print(f"[cache] {len(veri)} hisse kaydedildi -> {yol}")
    except Exception as e:
        print(f"[cache] yazilamadi ({type(e).__name__}).")


def bayat_semboller(veri: dict, evren: list, tolerans_gun: int = 4):
    hedef = son_islem_gunu()
    sinir = hedef - pd.Timedelta(days=tolerans_gun)
    eksik, bayat = [], []
    for s, mk in evren:
        an = s if mk == "turkey" else f"{s}.{mk[:2].upper()}"
        df = veri.get(an)
        if df is None or df.empty:
            eksik.append((s, mk))
        elif pd.Timestamp(df.index[-1]).normalize() < sinir:
            bayat.append((s, mk))
    return eksik, bayat, hedef


def _tek_indir(s, mk):
    import yfinance as yf
    meta = PIYASALAR[mk]
    yt = f"{s}{meta['suffix']}"
    if TIMEFRAME == "1d":
        df = yf.download(yt, period=GUNLUK_PERIOD, interval="1d",
                         auto_adjust=False, progress=False)
        if df is None or df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df.rename(columns=str.title)[["Open", "High", "Low", "Close", "Volume"]].dropna()
    df1h = yf.download(yt, period=PERIOD, interval="1h", auto_adjust=False, progress=False)
    if df1h is None or df1h.empty:
        return None
    if isinstance(df1h.columns, pd.MultiIndex):
        df1h.columns = df1h.columns.get_level_values(0)
    df1h = df1h.rename(columns=str.title)[["Open", "High", "Low", "Close", "Volume"]].dropna()
    if meta["bar"] == "platform":
        return platform_4h_ozel(df1h)
    if meta["bar"] == "america4h":
        return america_4h_ozel(df1h)
    return to_4h(df1h)


def veri_yukle_akilli(evren=None, tolerans_gun: int = 4, checkpoint: int = 150,
                      sadece_eksik: bool = False) -> dict:
    """Onbellegi okur, SADECE eksik/bayat sembolleri indirir, ara ara kaydeder.
       Kopma olursa checkpoint sayesinde ilerleme kaybolmaz."""
    evren = evren if evren is not None else evren_coklu()
    veri = onbellek_oku()
    print(f"[cache] mevcut: {len(veri)} hisse")
    eksik, bayat, hedef = bayat_semboller(veri, evren, tolerans_gun)
    inecek = eksik if sadece_eksik else eksik + bayat
    print(f"[cache] beklenen son bar: {hedef.date()}  |  eksik: {len(eksik)}  bayat: {len(bayat)}")
    if not inecek:
        print("[cache] Her sey guncel — indirme yok.")
        return veri
    print(f"[cache] {len(inecek)} sembol inecek (toplam {len(evren)} yerine).\n")
    yeni = 0
    for i, (s, mk) in enumerate(inecek, 1):
        try:
            df = _tek_indir(s, mk)
            if df is not None and len(df) >= cfg.min_bars:
                veri[s if mk == "turkey" else f"{s}.{mk[:2].upper()}"] = df
                yeni += 1
        except Exception:
            pass
        if i % 25 == 0 or i == len(inecek):
            print(f"  ...{i}/{len(inecek)}  (guncellenen: {yeni})")
        if i % checkpoint == 0:
            onbellek_yaz(veri, sessiz=True)
            print(f"  [checkpoint] {len(veri)} hisse kaydedildi — kopsa bile kayip yok.")
        time.sleep(SLEEP)
    onbellek_yaz(veri)
    return veri


def guncel_filtre(veri: dict, tolerans_gun: int = 6) -> dict:
    """Son bari geride kalmis hisseleri eler.
       (Bayat veri 'bugun atilim oldu' diye yanlis sinyal uretiyordu.)"""
    hedef = son_islem_gunu()
    sinir = hedef - pd.Timedelta(days=tolerans_gun)
    out = {k: v for k, v in veri.items()
           if not v.empty and pd.Timestamp(v.index[-1]).normalize() >= sinir}
    print(f"[filtre] guncel: {len(out)} / {len(veri)}  (sinir: {sinir.date()})")
    return out


# ============================================================================
#  DEBUG HUNİSİ + MAIN
# ============================================================================
def debug_funnel(veri: dict, cfg=cfg):
    indep = {}; n = 0; tam = 0; cekirdek_keys = None
    akum_keys = []; opsiyon_keys = []; cum = None
    for sym, df in veri.items():
        d = _hazirla(df, cfg)
        if d is None:
            continue
        n += 1
        last = len(d) - 1
        last_date = d.index[last].normalize()
        window = (1 if cfg.sadece_son_gun else cfg.max_days_ago) * cfg.bars_per_day + 1
        rows = []; eslesti_var = False
        for go in range(0, window + 1):
            D = last - go
            if D < 5:
                break
            if cfg.sadece_son_gun and d.index[D].normalize() != last_date:
                break
            r = _atilim_kontrol(d, D, go, last, cfg)
            if cekirdek_keys is None:
                keys = list(r.detay.keys())
                cekirdek_keys = [k for k in keys if k.startswith("c")]
                opsiyon_keys = [k for k in keys if k.startswith("o")]
                akum_keys = [k for k in keys if k.startswith("a")]
                tum_keys = cekirdek_keys + akum_keys + opsiyon_keys
                indep = {k: 0 for k in tum_keys}
                cum = [0] * (len(cekirdek_keys) + 1)
            rows.append([bool(r.detay.get(k, False)) for k in tum_keys])
            if r.eslesti:
                eslesti_var = True
        if not rows:
            continue
        arr = np.array(rows)
        anytrue = arr.any(axis=0)
        for i, k in enumerate(tum_keys):
            if anytrue[i]:
                indep[k] += 1
        carr = arr[:, [tum_keys.index(k) for k in cekirdek_keys]]
        for p in range(len(cekirdek_keys) + 1):
            if p == 0 or carr[:, :p].all(axis=1).any():
                cum[p] += 1
        if eslesti_var:
            tam += 1

    if not n or cekirdek_keys is None:
        print("Analiz edilecek (yeterli barlı) hisse yok."); return
    print(f"\n=== KOŞUL HUNİSİ  (analiz edilen hisse: {n}) ===")
    print("\n[A] Bağımsız geçiş (pencerede en az 1 aday bu koşulu geçti):")
    for k in cekirdek_keys + akum_keys + opsiyon_keys:
        oran = 100 * indep[k] / n if n else 0
        if k.startswith("a"): ek = "  (akümülasyon-puan)"
        elif k.startswith("o"): ek = "  (opsiyonel)"
        else: ek = ""
        print(f"  {k:24s} {indep[k]:4d}/{n}  %{oran:5.1f}  {'█'*int(oran/4)}{ek}")
    print("\n[B] Kümülatif AND (çekirdek koşullar):")
    onceki = n
    for p in range(1, len(cekirdek_keys) + 1):
        dusus = onceki - cum[p]
        en = max(cum[i] - cum[i+1] for i in range(len(cekirdek_keys)))
        isaret = "  <<< en büyük düşüş" if dusus == en and dusus > 0 else ""
        print(f"  +{cekirdek_keys[p-1]:24s} {cum[p]:4d}{isaret}")
        onceki = cum[p]
    print(f"\nTAM EŞLEŞEN: {tam}")
    print("İpucu: hangi çekirdek satırda sayı sıfıra iniyorsa darboğaz odur.")
    return indep, cum


def bolge_rontgen(veri: dict, sembol: str, baslangic: str, bitis: str, cfg=cfg):
    """Bir hissenin BELİRLİ tarih aralığındaki her barın gerçek matematiğini döker.
       Senin gözünün 'iyi çöl' dediği bölgeyi sayıya çevirir.
       Kullanım: bolge_rontgen(veri, 'HTLD.AM', '2026-06-18', '2026-06-24')
       (anahtarlar ABD'de 'XXX.AM' biçimindedir; istersen sembol='HTLD' de yazabilirsin)"""
    # anahtar bul (HTLD veya HTLD.AM)
    key = sembol if sembol in veri else None
    if key is None:
        adaylar = [k for k in veri if k.upper().split(".")[0] == sembol.upper().split(".")[0]]
        if not adaylar:
            print(f"[röntgen] '{sembol}' veride yok. Örnek anahtarlar: {list(veri)[:5]}")
            return
        key = adaylar[0]
    d = _hazirla(veri[key], cfg)
    if d is None:
        print(f"[röntgen] {key}: yeterli bar yok."); return

    b = pd.Timestamp(baslangic); e = pd.Timestamp(bitis) + pd.Timedelta(days=1)
    mask = (d.index >= b) & (d.index < e)
    seg = d[mask]
    if seg.empty:
        print(f"[röntgen] {key}: {baslangic}–{bitis} aralığında bar yok. "
              f"Veri aralığı: {d.index[0].date()} .. {d.index[-1].date()}")
        return

    p_main = min(cfg.emalar)
    satir = []
    for i in range(len(seg)):
        r = seg.iloc[i]
        gpos = d.index.get_loc(seg.index[i])
        atrv = float(r["ATR"]) if np.isfinite(r["ATR"]) and r["ATR"] else np.nan
        govde = abs(float(r["Close"]) - float(r["Open"]))
        govde_atr = govde / atrv if atrv else np.nan
        rng = max(float(r["High"]) - float(r["Low"]), 1e-9)
        ust_fitil = (float(r["High"]) - max(float(r["Open"]), float(r["Close"]))) / rng
        alt_fitil = (min(float(r["Open"]), float(r["Close"])) - float(r["Low"])) / rng
        kapanis_pos = (float(r["Close"]) - float(r["Low"])) / rng     # 1=tepeden, 0=dipten kapadı
        bbr = float(r["BBWrank"]) if not pd.isna(r["BBWrank"]) else np.nan
        yon = "YEŞİL" if r["Close"] >= r["Open"] else "kırmızı"
        # SMA20 5-bar eğimi
        if gpos - 5 >= 0:
            mn = float(d.iloc[gpos][f"EMA{p_main}"]); mp = float(d.iloc[gpos-5][f"EMA{p_main}"])
            egim = (mn - mp) / mp * 100 if mp else 0.0
        else:
            egim = 0.0
        satir.append({
            "tarih": str(seg.index[i]),
            "yon": yon,
            "O": round(float(r["Open"]), 2), "H": round(float(r["High"]), 2),
            "L": round(float(r["Low"]), 2), "C": round(float(r["Close"]), 2),
            "govde/ATR": round(govde_atr, 2) if np.isfinite(govde_atr) else None,
            "üstFitil%": round(ust_fitil*100, 0), "altFitil%": round(alt_fitil*100, 0),
            "kapanışPos": round(kapanis_pos, 2),
            "BBrank": round(bbr, 2) if np.isfinite(bbr) else None,
            "SMA20eğim%": round(egim, 2),
            "Vol": int(r["Volume"]),
        })
    tablo = pd.DataFrame(satir)

    # bölge özeti (senin "iyi çöl" tanımının matematiği)
    govdeler = tablo["govde/ATR"].dropna()
    lows = seg["Low"].values
    higher_lows = int(sum(lows[j] >= lows[j-1] for j in range(1, len(lows))))
    print(f"\n=== BÖLGE RÖNTGENİ: {key}  ({baslangic} → {bitis}) ===")
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", None)
    print(tablo.to_string(index=False))
    print("\n--- BÖLGE ÖZETİ (matematik) ---")
    print(f"  bar sayısı            : {len(seg)}")
    print(f"  ort. gövde/ATR        : {govdeler.mean():.2f}   (küçük mum => ~0.5 altı)")
    print(f"  en küçük / en büyük göv/ATR: {govdeler.min():.2f} / {govdeler.max():.2f}")
    print(f"  ort. BB rank          : {tablo['BBrank'].dropna().mean():.2f}   (sıkışma => ~0.35 altı)")
    print(f"  taban genişliği %     : {(seg['High'].max()-seg['Low'].min())/seg['Close'].mean()*100:.1f}")
    print(f"  yükselen dip sayısı   : {higher_lows}/{len(seg)-1}")
    print(f"  yeşil/kırmızı mum     : {int((seg['Close']>=seg['Open']).sum())}/{int((seg['Close']<seg['Open']).sum())}")
    print(f"  ort. SMA20 eğim %     : {tablo['SMA20eğim%'].mean():.2f}")
    # yıllık konum
    gpos0 = d.index.get_loc(seg.index[0])
    yil = d.iloc[max(0, gpos0 - cfg.dip_pencere):gpos0]
    if len(yil) >= 30:
        konum = (float(seg['Close'].iloc[0]) - float(yil['Low'].min())) / \
                (float(yil['High'].max()) - float(yil['Low'].min()) + 1e-9)
        print(f"  yıllık konum (0=dip)  : {konum:.2f}")
    return tablo


# ############################################################################
# ############################################################################
#
#   [EK BÖLÜM]  KÂR / ZARAR TESTİ  (BACKTEST)
#   Yukarıdaki tarayıcı mantığına HİÇ dokunulmadı. Bu bölüm sadece EKLENTİDİR.
#
#   NEDEN AYRI: tarayıcı sadece "bugünkü" atılımı arar (c3_taze).
#   Backtest için aynı fonksiyon geçmişteki HER bara, o barı "son bar" kabul
#   ederek uygulanır -> _atilim_kontrol(d, D, 0, D, cfg). Böylece hiçbir
#   gelecek bilgisi sızmaz (look-ahead yok), formasyon tanımı da değişmez.
#
#   KULLANIM (main() bittikten sonra AYRI bir hücrede):
#       tr = backtest_calistir()                    # VERI global'ini kullanır
#       bt_rapor(tr)                                # genel + tüm filtre testleri
#       bt_filtre_karsilastir(tr, "OBVdiv", 0.40)   # tek filtre
#       bt_esik_tarama(tr, "Puan", [5, 10, 15, 20, 30])
#
#   ÖNEMLİ: Anlamlı backtest için GEÇMİŞ VERİ gerekir.
#   Aşağıdaki GUNLUK_PERIOD'u "5y" veya "10y" yap, FORCE_DOWNLOAD=True ile
#   bir kez yeniden indir. min_bars=250 olduğu için 2y veride test edilebilir
#   alan çok dar kalır.
# ############################################################################
# ############################################################################

GUNLUK_PERIOD = "2y"      # <<< BACKTEST İÇİN "5y" / "10y" YAP, sonra FORCE_DOWNLOAD=True


@dataclass
class BTConfig:
    """Çıkış kuralları — asıl kâr/zararı BELİRLEYEN kısım burasıdır."""
    horizon: int = 15                 # en fazla kaç bar tutulur (süre dolunca kapanıştan çık)
    stop_pct: Optional[float] = 0.07  # zarar kes (girişten % kaç aşağı)
    hedef_pct: Optional[float] = 0.15 # kâr al (girişten % kaç yukarı)
    ma_cikis: Optional[int] = None    # örn 20 -> SMA20 altında kapanınca çık (None=kapalı)
    giris: str = "sonraki_acilis"     # "sonraki_acilis" (gerçekçi) | "ayni_kapanis" (iyimser)
    cooldown_bar: int = 5             # aynı sembolde ard arda sinyalleri seyrelt
    baslangic: Optional[str] = None   # "2021-01-01" gibi; None = tüm geçmiş
    bitis: Optional[str] = None
    komisyon_pct: float = 0.0         # gidiş-dönüş toplam maliyet (örn 0.002 = %0.2)
    # --- RETEST girisi (giris="retest") ---
    retest_max_bar: int = 10           # kac bar icinde geri cekilme beklensin
    retest_tol: float = 0.01           # seviyeye "dokundu" toleransi (%1)
    retest_vol_kat: float = 0.70       # retest bari hacmi, kirilim hacminin bu kati altinda


def _bt_simule(d, D, bt: BTConfig):
    """Tek sinyali ileri simüle eder. Aynı barda stop+hedef -> STOP (muhafazakâr)."""
    if getattr(bt, "giris", "") == "retest":
        return _bt_simule_retest(d, D, bt)
    if bt.giris == "ayni_kapanis":
        e = D
        giris = float(d["Close"].iloc[e])
    else:
        e = D + 1
        if e >= len(d):
            return None
        giris = float(d["Open"].iloc[e])

    if not np.isfinite(giris) or giris <= 0:
        return None

    stop_f = giris * (1 - bt.stop_pct) if bt.stop_pct else None
    hedef_f = giris * (1 + bt.hedef_pct) if bt.hedef_pct else None
    ma_kol = f"EMA{bt.ma_cikis}" if (bt.ma_cikis and f"EMA{bt.ma_cikis}" in d.columns) else None

    son = min(e + bt.horizon, len(d) - 1)
    for i in range(e, son + 1):
        lo = float(d["Low"].iloc[i]); hi = float(d["High"].iloc[i])
        if stop_f is not None and lo <= stop_f:
            return _bt_sonuc(d, e, i, giris, stop_f, "stop", bt)
        if hedef_f is not None and hi >= hedef_f:
            return _bt_sonuc(d, e, i, giris, hedef_f, "hedef", bt)
        if ma_kol and i > e:
            mv = float(d[ma_kol].iloc[i])
            if np.isfinite(mv) and float(d["Close"].iloc[i]) < mv:
                return _bt_sonuc(d, e, i, giris, float(d["Close"].iloc[i]), "ma_alti", bt)

    return _bt_sonuc(d, e, son, giris, float(d["Close"].iloc[son]), "süre", bt)


def _bt_sonuc(d, e, x, giris, cikis, neden, bt: BTConfig):
    getiri = cikis / giris - 1.0 - bt.komisyon_pct
    return {
        "GirişTarih": str(d.index[e]), "ÇıkışTarih": str(d.index[x]),
        "Giriş": round(giris, 4), "Çıkış": round(cikis, 4),
        "Getiri%": round(getiri * 100, 2), "Bar": x - e, "ÇıkışNedeni": neden,
    }


def _aday_barlar(d, cfg) -> np.ndarray:
    """Vektorel on-eleme: gap + MA gecisi olan bar indeksleri.

    NEDEN: backtest her hisse icin ~250 barin HEPSINI tek tek kontrol
    ediyordu (1900 hisse x 250 bar = ~480.000 agir cagri, ~95 dk).
    c1_sert_bosluk ve c2_ma_gecisi cekirdekte ZORUNLU ve ikisi de numpy ile
    toplu hesaplanabiliyor. Gecemeyecek barlari atlamak sonucu DEGISTIRMEZ,
    sadece hesabi atlar. Olculen kazanc: ~17x, sonuclar birebir ayni.
    """
    n = len(d)
    o = d["Open"].to_numpy(dtype=float)
    h = d["High"].to_numpy(dtype=float)
    c = d["Close"].to_numpy(dtype=float)

    if cfg.sert_bosluk:
        gap = np.zeros(n, dtype=bool)
        with np.errstate(invalid="ignore", divide="ignore"):
            gap[1:] = (o[1:] > h[:-1]) & ((o[1:] - h[:-1]) / h[:-1] * 100 >= cfg.min_gap_pct)
    else:
        gap = np.ones(n, dtype=bool)

    cross = np.zeros(n, dtype=bool)
    for p in cfg.emalar:
        m = d[f"EMA{p}"].to_numpy(dtype=float)
        cross[1:] |= (c[:-1] < m[:-1]) & (o[1:] > m[1:])

    return np.where(gap & cross)[0]


def backtest_calistir(veri=None, cfg=cfg, bt: BTConfig = None, ilerleme=True) -> pd.DataFrame:
    """Geçmişteki TÜM atılım sinyallerini bulur ve simüle eder.
       Dönen tabloda tarayıcının bütün sütunları (Puan, OBVdiv, Net_Alım, ...)
       + işlem sonucu (Getiri%, ÇıkışNedeni) yan yana durur."""
    bt = bt or BTConfig()
    veri = VERI if veri is None else veri
    if not veri:
        print("[backtest] Veri yok. Önce main() çalıştır ya da veri= parametresi ver.")
        return pd.DataFrame()

    b0 = pd.Timestamp(bt.baslangic) if bt.baslangic else None
    b1 = pd.Timestamp(bt.bitis) if bt.bitis else None

    satirlar = []
    toplam = len(veri)
    for i, (sembol, df) in enumerate(veri.items(), 1):
        if ilerleme and (i % 100 == 0 or i == toplam):
            print(f"  ...backtest {i}/{toplam}  (sinyal: {len(satirlar)})")
        try:
            d = _hazirla(df, cfg)
        except Exception:
            continue
        if d is None:
            continue

        bas = max(cfg.min_bars, cfg.col_window + 2, cfg.kalite_pencere + 2)
        adaylar = _aday_barlar(d, cfg)
        adaylar = adaylar[(adaylar >= bas) & (adaylar < len(d) - 1)]
        son_D = -10 ** 9
        for D in adaylar:
            D = int(D)
            ts = d.index[D]
            if b0 is not None and ts < b0:
                continue
            if b1 is not None and ts > b1:
                break
            if D - son_D < bt.cooldown_bar:
                continue
            try:
                # last=D  ->  o bar "son bar" kabul edilir, gelecek sızmaz
                r = _atilim_kontrol(d, D, 0, D, cfg)
            except Exception:
                continue
            if not r.eslesti:
                continue
            islem = _bt_simule(d, D, bt)
            if islem is None:
                continue
            son_D = D
            n = r.notlar
            satirlar.append({
                "Sembol": sembol, "Atılım": str(d.index[D]), "Seans": r.seans,
                "Puan": n.get("puan"), "TF": n.get("tf"),
                "Tip": n.get("col_tipi"), "ÇölBar": n.get("col_bar"),
                "ER": n.get("ER"), "Ralli%": n.get("ralli_pct"),
                "TTM%": n.get("ttm_oran"), "TTMBar": n.get("ttm_bar"),
                "TTMBırak": n.get("ttm_birakma"),
                "MiniKalP": n.get("mini_kalite_p"), "KapanışP": n.get("kapanis_p"),
                "UBP": n.get("ub_p"), "UBSkor": n.get("ub_skor"),
                "Ham": n.get("ham_puan"), "Kalite": n.get("kalite"),
                "MA_P": n.get("ma_puan"), "Akum_P": n.get("akum_puan"),
                "OBVnorm": n.get("obv_norm"), "OBVdiv": n.get("obv_diverj"),
                "GirişK": n.get("giris_kalite"),
                "GeçenMA": n.get("gecen_emalar"), "Fitil": n.get("fitil"),
                "Kanaat": n.get("kanaat"),
                "YılKonum": n.get("yil_konum"), "KonumÇrp": n.get("konum_carpan"),
                "ÇölAlt%": n.get("col_alt_oran"),
                "Gap%": n.get("gap_pct"), "GapSık%": n.get("gap_siklik"),
                "Net_Alım": n.get("net_alim_orani"),
                "BoşHacim×": n.get("bosluk_hacim_kat"),
                "BBrank": n.get("bbw_rank"), "Gövde/ATR": n.get("govde_atr"),
                "Taban%": n.get("taban_genislik"), "KurumİZ": n.get("kurum_iz_sayisi"),
                "MA Sapma%": n.get("sapma_ma_yuzde"),
                **islem,
            })

    tr = pd.DataFrame(satirlar)
    if not tr.empty:
        tr = tr.sort_values("Atılım").reset_index(drop=True)
        tr.to_csv("backtest_islemler.csv", index=False)
        print(f"\n[backtest] {len(tr)} işlem simüle edildi -> 'backtest_islemler.csv'")
        print(f"[backtest] Tarih aralığı: {tr['Atılım'].min()[:10]} .. {tr['Atılım'].max()[:10]}")
    else:
        print("\n[backtest] Hiç sinyal bulunamadı. GUNLUK_PERIOD'u artır ya da filtreleri gevşet.")
    return tr


def bt_metrikler(tr: pd.DataFrame) -> dict:
    """Bir işlem kümesinin performans özeti."""
    if tr is None or tr.empty:
        return {"işlem": 0}
    r = tr["Getiri%"].to_numpy(dtype=float) / 100.0
    kaz = r[r > 0]; kyb = r[r <= 0]
    kar = kaz.sum(); zar = abs(kyb.sum())
    eq = np.cumprod(1 + r)
    dd = float((eq / np.maximum.accumulate(eq) - 1).min()) if len(eq) else 0.0
    return {
        "işlem": len(r),
        "kazanma%": round(100 * len(kaz) / len(r), 1),
        "ortGetiri%": round(100 * r.mean(), 2),
        "medyan%": round(100 * float(np.median(r)), 2),
        "ortKazanç%": round(100 * kaz.mean(), 2) if len(kaz) else 0.0,
        "ortKayıp%": round(100 * kyb.mean(), 2) if len(kyb) else 0.0,
        "karFaktörü": round(kar / zar, 2) if zar > 0 else np.inf,
        "std%": round(100 * r.std(ddof=1), 2) if len(r) > 1 else np.nan,
        "maxDüşüş%": round(100 * dd, 1),
        "ortBar": round(float(tr["Bar"].mean()), 1),
    }


def bt_filtre_karsilastir(tr: pd.DataFrame, kolon: str, esik=0.0, op: str = ">") -> pd.DataFrame:
    """Filtreyi geçen / geçemeyen / tümü — üç satırlık karşılaştırma.
       Metin sütunları için: bt_filtre_karsilastir(tr, "Fitil", "temiz", "==")"""
    if tr is None or tr.empty:
        print("[bt] tablo boş."); return pd.DataFrame()
    if kolon not in tr.columns:
        print(f"[bt] '{kolon}' yok. Mevcut: {[c for c in tr.columns]}"); return pd.DataFrame()

    if op == "==":
        mask = tr[kolon].astype(str) == str(esik)
    else:
        v = pd.to_numeric(tr[kolon], errors="coerce")
        mask = (v > esik) if op == ">" else (v < esik)
    mask = mask.fillna(False)

    out = pd.DataFrame([
        {"grup": "TÜMÜ", **bt_metrikler(tr)},
        {"grup": f"VAR ({kolon}{op}{esik})", **bt_metrikler(tr[mask])},
        {"grup": "YOK", **bt_metrikler(tr[~mask])},
    ]).set_index("grup")
    return out


def bt_esik_tarama(tr: pd.DataFrame, kolon: str, esikler) -> pd.DataFrame:
    """Eşiği kaydırıp bak. Sağlam filtre yumuşak davranır; tek eşikte parlayıp
       diğerlerinde çöküyorsa o AŞIRI UYDURMADIR (overfit)."""
    if tr is None or tr.empty:
        return pd.DataFrame()
    v = pd.to_numeric(tr[kolon], errors="coerce")
    return pd.DataFrame([{"eşik": t, **bt_metrikler(tr[(v > t).fillna(False)])}
                         for t in esikler]).set_index("eşik")


def bt_permutasyon_p(tr: pd.DataFrame, kolon: str, esik=0.0, n: int = 3000, seed: int = 42) -> float:
    """Filtrenin getirdiği fark şansa mı bağlı? p<0.05 => rastlantıyla açıklanması zor.
       50'den az işlemde bu sayıya fazla güvenme."""
    if tr is None or tr.empty:
        return float("nan")
    v = pd.to_numeric(tr[kolon], errors="coerce")
    m = (v > esik).fillna(False).to_numpy()
    r = tr["Getiri%"].to_numpy(dtype=float)
    if m.sum() < 2 or (~m).sum() < 2:
        return float("nan")
    gercek = abs(r[m].mean() - r[~m].mean())
    rng = np.random.default_rng(seed)
    say = 0
    for _ in range(n):
        p = rng.permutation(m)
        if abs(r[p].mean() - r[~p].mean()) >= gercek:
            say += 1
    return say / n


def bt_rapor(tr: pd.DataFrame):
    """Tek komutla tam rapor: genel + çıkış dağılımı + her filtrenin etkisi."""
    if tr is None or tr.empty:
        print("[bt] tablo boş."); return
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", None)

    print("\n" + "=" * 78)
    print("  GENEL SONUÇ")
    print("=" * 78)
    for k, v in bt_metrikler(tr).items():
        print(f"  {k:14s}: {v}")

    print("\n  Çıkış nedeni dağılımı:")
    for neden, grp in tr.groupby("ÇıkışNedeni"):
        print(f"    {neden:8s} {len(grp):5d} adet   ort getiri %{grp['Getiri%'].mean():6.2f}")

    testler = [
        ("TTM%",     cfg.ttm_oran_min,   ">"),
        ("TTMBar",   cfg.ttm_uzun_bar,   ">"),
        ("TTMBırak", "VAR",              "=="),
        ("Tip",      "COL",              "=="),
        ("Tip",      "YAYLA",            "=="),
        ("ER",       cfg.er_max,         "<"),
        ("Ralli%",   cfg.ralli_max * 100, "<"),
        ("UBP",      0.01,               ">"),
        ("MiniKalP", 0.01,               ">"),
        ("KapanışP", 0.01,               ">"),
        ("OBVdiv",   cfg.obv_diverj_min, ">"),
        ("Net_Alım", cfg.net_alim_min,   ">"),
        ("BoşHacim×", cfg.breakout_vol_kat, ">"),
        ("BBrank",   cfg.bb_squeeze_pct, "<"),
        ("YılKonum", cfg.dip_esik,       "<"),
        ("Fitil",    "temiz",            "=="),
        ("Kanaat",   "var",              "=="),
        ("Puan",     float(tr["Puan"].median()), ">"),
        ("GirişK",   0.99,               ">"),
    ]
    print("\n" + "=" * 78)
    print("  FİLTRE ETKİ TESTLERİ  (VAR satırı YOK'tan belirgin iyiyse filtre işe yarıyor)")
    print("=" * 78)
    for kol, esik, op in testler:
        if kol not in tr.columns:
            continue
        t = bt_filtre_karsilastir(tr, kol, esik, op)
        if t.empty:
            continue
        print(f"\n--- {kol} {op} {esik} ---")
        print(t.to_string())
        if op != "==":
            p = bt_permutasyon_p(tr, kol, esik if op == ">" else esik)
            if np.isfinite(p):
                yorum = "ANLAMLI" if p < 0.05 else "anlamsız (şans olabilir)"
                print(f"    permütasyon p = {p:.4f}  -> {yorum}")

    print("\n" + "=" * 78)
    print("  PUAN EŞİĞİ TARAMASI (min_puan'ı nereye çekmeli?)")
    print("=" * 78)
    q = tr["Puan"].quantile([0.2, 0.4, 0.5, 0.6, 0.8]).round(1).tolist()
    print(bt_esik_tarama(tr, "Puan", sorted(set(q))).to_string())

    print("\n" + "=" * 78)
    if "TTMBar" in tr.columns:
        print("\n" + "=" * 78)
        print("  TTM SIKISMA SURESI (uzun sikisma daha mi iyi?)")
        print("=" * 78)
        print(bt_esik_tarama(tr, "TTMBar", [0, 5, 10, 20, 40]).to_string())
        print("\n" + "=" * 78)
    print("  YIL BAZINDA")
    print("=" * 78)
    tr2 = tr.copy(); tr2["_yil"] = tr2["Atılım"].str[:4]
    print(pd.DataFrame([{"yıl": y, **bt_metrikler(g)}
                        for y, g in tr2.groupby("_yil")]).set_index("yıl").to_string())


def bt_cikis_kurallari_karsilastir(veri=None, cfg=cfg, senaryolar=None) -> pd.DataFrame:
    """Farklı çıkış kurallarını yan yana dener. Hangi stop/hedef/süre en iyi?"""
    veri = VERI if veri is None else veri
    senaryolar = senaryolar or [
        ("5 bar, stop yok",      BTConfig(horizon=5,  stop_pct=None, hedef_pct=None)),
        ("10 bar, stop yok",     BTConfig(horizon=10, stop_pct=None, hedef_pct=None)),
        ("20 bar, stop yok",     BTConfig(horizon=20, stop_pct=None, hedef_pct=None)),
        ("stop%5 / hedef%10",    BTConfig(horizon=20, stop_pct=0.05, hedef_pct=0.10)),
        ("stop%7 / hedef%15",    BTConfig(horizon=20, stop_pct=0.07, hedef_pct=0.15)),
        ("stop%10 / hedef%25",   BTConfig(horizon=30, stop_pct=0.10, hedef_pct=0.25)),
        ("stop%7 / SMA20 altı",  BTConfig(horizon=40, stop_pct=0.07, hedef_pct=None, ma_cikis=20)),
    ]
    satir = []
    for ad, b in senaryolar:
        print(f"\n>>> senaryo: {ad}")
        tr = backtest_calistir(veri, cfg, b, ilerleme=False)
        satir.append({"senaryo": ad, **bt_metrikler(tr)})
    return pd.DataFrame(satir).set_index("senaryo")


def _tf_ayarla():
    cfg.timeframe = TIMEFRAME
    if TIMEFRAME == "1d":
        cfg.bars_per_day = 1
    elif "america" in MARKETS:
        cfg.bars_per_day = 2
    else:
        cfg.bars_per_day = 3


def col_teshis(sembol, veri=None):
    """Tek hissenin neden COL / YAYLA / TREND sayildigini gosterir.
       Ornek: col_teshis('SPSC')"""
    veri = veri if veri is not None else VERI
    key = sembol if sembol in veri else next(
        (k for k in veri if k.upper().split(".")[0] == sembol.upper().split(".")[0]), None)
    if key is None:
        print(f"[teshis] '{sembol}' veride yok."); return
    d = _hazirla(veri[key], cfg)
    if d is None:
        print(f"[teshis] {key}: yeterli bar yok."); return
    D = len(d) - 1
    puan, det, nt = _akumulasyon(d, D, cfg)
    print(f"\n=== {key} ===")
    print(f"  col uzunlugu : {int(nt.get('col_bar', 0))} bar")
    print(f"  ER           : {nt.get('ER')}   (<= {cfg.er_max})  "
          f"{'OK' if det.get('a_er_dusuk') else '<-- KAYIYOR'}")
    print(f"  drift%       : {nt.get('drift_pct')}  (<= {cfg.drift_max*100:.0f})  "
          f"{'OK' if det.get('a_yatay_akis') else '<-- KAYIYOR'}")
    print(f"  ralli%       : {nt.get('ralli_pct')}  (<= {cfg.ralli_max*100:.0f})  "
          f"{'OK' if det.get('a_dipte') else '<-- DIPTEN KALKMIS'}")
    print(f"  yil konumu   : {nt.get('yil_konum')}")
    print(f"  BBWrank      : {nt.get('bbw_rank')}   (<= {cfg.bb_squeeze_pct})")
    print(f"  TTM sikisma  : oran {nt.get('ttm_oran')} | sure {int(nt.get('ttm_bar',0))} bar"
          f" | birakma {nt.get('ttm_birakma')}")
    print(f"  OBVnorm      : {nt.get('obv_norm')}   (v2 ise -1..1 arasinda olmali)")
    print(f"  SONUC        : {nt.get('col_tipi')}   | puan {puan:.2f}")
    return nt


def hizli_baslat(tarama=True, debug=True, tolerans_gun=4, sadece_eksik=False):
    """TEK KOMUT: onbellekten yukle -> eksikleri tamamla -> bayatlari ele -> tara.
       Colab koptuysa bu hucreyi tekrar calistirmak yeter (saniyeler)."""
    global VERI
    _tf_ayarla()
    t0 = time.time()
    if KAYNAK == "csv":
        veri = csv_yukle(VERI_KLASORU)
    else:
        veri = veri_yukle_akilli(tolerans_gun=tolerans_gun, sadece_eksik=sadece_eksik)
    # filtre toleransi indirme toleransindan GENIS olmali; aksi halde
    # indirilmeyen ama filtrede elenen hisseler olusur (evren cokerdi)
    VERI = guncel_filtre(veri, tolerans_gun=tolerans_gun + 2)
    print(f"\n[hazir] {len(VERI)} hisse  |  {time.time()-t0:.1f} sn")
    if not tarama:
        return None

    if debug:
        debug_funnel(VERI, cfg)
    tablo = taramayi_calistir(VERI, cfg)
    if tablo.empty:
        print("\nKriterlere uyan TAZE atilim bulunamadi.")
        return tablo
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", 260)
    pd.set_option("display.max_columns", None)
    print(f"\n=== ESLESENLER ({len(tablo)}) — Puan'a gore sirali ===")
    print(tablo.to_string(index=False))
    tablo.to_csv("sonuc.csv", index=False)
    print(f"\n{len(tablo)} eslesme 'sonuc.csv' dosyasina yazildi.")
    if "Tip" in tablo.columns:
        print("\nTip dagilimi:", dict(tablo["Tip"].value_counts()))
    print("\n[IPUCU] col_teshis('SPSC')            -> tek hisse rontgeni")
    print("[IPUCU] tr = backtest_calistir(); bt_rapor(tr)   -> kar/zarar testi")
    return tablo


def main():
    """Eski giris noktasi — hizli_baslat'i cagirir."""
    return hizli_baslat()



# #####################################################################
#  EK OLCUMLER — gercek taban olcumu + kontrol grubu
#  (onceden ayri hucrelerdi, artik dosyaya gomulu)
# #####################################################################

# ---- taban olcum ayarlari ----
cfg.taban_en_az     = 5      # taban en az kac bar
cfg.taban_en_cok    = 250    # en fazla kac bar geriye bakilsin (1 yil)
cfg.taban_max_atr   = 4.0    # taban yuksekligi bu ATR katini asinca taban biter
cfg.dokunus_tol_atr = 0.25   # tavan/dibe "dokundu" sayilma toleransi (ATR kati)
cfg.taban_penceresi_kullan = True   # olculen tabani akumulasyon penceresi yap
cfg.w_yay = 0.0              # YaySkoru puani (once OLC, sonra ac)


def taban_olc(d, D, cfg):
    """Atilimdan geriye yuruyerek tabanin GERCEK yapisini olcer.

    Yontem: D-1'den geriye yuru, calisan yuksek/dusuk tut. Bant yuksekligi
    ATR'nin taban_max_atr katini asinca taban orada biter. ATR normalizasyonu
    sayesinde farkli volatilitedeki hisseler ayni olcekte karsilastirilir ve
    pencere trendi yutmaz.
    """
    if D < cfg.taban_en_az + 1:
        return None
    atr0 = float(d["ATR"].iloc[D - 1])
    if not np.isfinite(atr0) or atr0 <= 0:
        return None

    H = d["High"].to_numpy(dtype=float)
    L = d["Low"].to_numpy(dtype=float)
    C = d["Close"].to_numpy(dtype=float)

    en_uzun = cfg.taban_en_az
    hi = lo = None
    ust = min(cfg.taban_en_cok, D)
    for n in range(cfg.taban_en_az, ust + 1):
        i0 = D - n
        h = float(H[i0:D].max()); l = float(L[i0:D].min())
        if (h - l) / atr0 > cfg.taban_max_atr:
            break            # bant tasti -> taban burada bitiyor
        en_uzun, hi, lo = n, h, l

    if hi is None:
        return None

    n = en_uzun
    i0 = D - n
    seg_h, seg_l, seg_c = H[i0:D], L[i0:D], C[i0:D]
    yukseklik = (hi - lo) / atr0
    tol = cfg.dokunus_tol_atr * atr0

    # tavan/dip dokunuslari: cok dokunus = test edilmis, birikmis seviye
    tavan_dok = int((seg_h >= hi - tol).sum())
    dip_dok = int((seg_l <= lo + tol).sum())

    # daralma: ikinci yari / ilk yari genisligi. <1 ise yay geriliyor.
    k = n // 2
    if k >= 2:
        r1 = float(seg_h[:k].max() - seg_l[:k].min())
        r2 = float(seg_h[k:].max() - seg_l[k:].min())
        daralma = r2 / r1 if r1 > 0 else 1.0
    else:
        daralma = 1.0

    # dip egimi: dipler yukseliyor mu (ATR/bar)
    if n >= 6:
        x = np.arange(n)
        dip_egim = float(np.polyfit(x, seg_l, 1)[0]) / atr0
    else:
        dip_egim = 0.0

    # YAY SKORU: uzunluk + darlik + daralma + dokunus + yukselen dip
    s_uzun   = min(n / 40.0, 1.0)                       # 40 bar = tam puan
    s_dar    = max(0.0, 1.0 - yukseklik / cfg.taban_max_atr)
    s_daralma = max(0.0, min((1.0 - daralma) / 0.5, 1.0))
    s_dokunus = min((tavan_dok + dip_dok) / 8.0, 1.0)
    s_dip    = 1.0 if dip_egim > 0.005 else (0.5 if dip_egim > -0.005 else 0.0)
    yay = 0.30 * s_uzun + 0.25 * s_dar + 0.20 * s_daralma + 0.15 * s_dokunus + 0.10 * s_dip

    return {
        "taban_bar": float(n),
        "taban_atr": round(yukseklik, 2),
        "taban_tavan": float(hi),
        "taban_dip": float(lo),
        "daralma": round(daralma, 2),
        "tavan_dok": float(tavan_dok),
        "dip_dok": float(dip_dok),
        "dip_egim": round(dip_egim, 4),
        "yay_skoru": round(float(yay), 3),
    }


# ---------------------------------------------------------------- sarmalayici
if not globals().get("_TABAN_YAMASI"):
    _ak_taban_onceki = _akumulasyon

    def _akumulasyon(d, D, cfg):
        olcum = taban_olc(d, D, cfg)

        # olculen tabani akumulasyon penceresi olarak kullan
        eski_cw, eski_dyn = cfg.col_window, getattr(cfg, "dinamik_col", False)
        if olcum and cfg.taban_penceresi_kullan:
            cfg.col_window = int(olcum["taban_bar"])
            cfg.dinamik_col = False
        try:
            puan, det, nt = _ak_taban_onceki(d, D, cfg)
        finally:
            cfg.col_window, cfg.dinamik_col = eski_cw, eski_dyn

        if olcum:
            nt.update(olcum)
            det["a_uzun_taban"] = bool(olcum["taban_bar"] >= 20)
            det["a_daralan"] = bool(olcum["daralma"] < 0.8)
            det["a_test_edilmis"] = bool(olcum["tavan_dok"] + olcum["dip_dok"] >= 4)
            puan += cfg.w_yay * olcum["yay_skoru"]
        else:
            det["a_uzun_taban"] = det["a_daralan"] = det["a_test_edilmis"] = False
            nt["taban_bar"] = float(cfg.col_window)
            nt["yay_skoru"] = 0.0
        return float(puan), det, nt

    _TABAN_YAMASI = True


def taban_sutun_ekle(tr, veri=None):
    """Backtest tablosuna taban olcumlerini ekler (sinyal tarihine gore)."""
    veri = veri if veri is not None else globals().get("VERI", {})
    if tr is None or tr.empty:
        return tr
    ek = []
    onbellek = {}
    for _, r in tr.iterrows():
        s = r["Sembol"]
        if s not in onbellek:
            df = veri.get(s)
            onbellek[s] = _hazirla(df, cfg) if df is not None else None
        d = onbellek[s]
        if d is None:
            ek.append({}); continue
        try:
            D = int(d.index.searchsorted(pd.Timestamp(r["Atılım"])))
            o = taban_olc(d, D, cfg) or {}
        except Exception:
            o = {}
        ek.append(o)
    add = pd.DataFrame(ek, index=tr.index)
    ren = {"taban_bar": "TabanBar", "taban_atr": "TabanATR", "daralma": "Daralma",
           "tavan_dok": "TavanDok", "dip_dok": "DipDok", "dip_egim": "DipEğim",
           "yay_skoru": "YaySkoru"}
    for k_, v_ in ren.items():
        if k_ in add.columns:
            tr[v_] = add[k_]
    return tr


def taban_teshis(sembol, veri=None):
    """Tek hissenin tabanini olcup dokumunu basar. Ornek: taban_teshis('TPG')"""
    veri = veri if veri is not None else globals().get("VERI", {})
    key = sembol if sembol in veri else next(
        (k for k in veri if k.upper().split(".")[0] == sembol.upper().split(".")[0]), None)
    if key is None:
        print(f"[taban] '{sembol}' veride yok."); return
    d = _hazirla(veri[key], cfg)
    if d is None:
        print(f"[taban] {key}: yeterli bar yok."); return
    D = len(d) - 1
    o = taban_olc(d, D, cfg)
    if not o:
        print(f"[taban] {key}: taban olculemedi."); return
    print(f"\n=== {key} TABAN ===")
    print(f"  uzunluk      : {int(o['taban_bar'])} bar   (eskiden hep 10 sayiliyordu)")
    print(f"  yukseklik    : {o['taban_atr']} ATR   (<{cfg.taban_max_atr} = dar)")
    print(f"  tavan / dip  : {o['taban_tavan']:.2f} / {o['taban_dip']:.2f}")
    print(f"  daralma      : {o['daralma']}   (<1 = yay geriliyor)")
    print(f"  dokunus      : tavan {int(o['tavan_dok'])}x, dip {int(o['dip_dok'])}x")
    print(f"  dip egimi    : {o['dip_egim']} ATR/bar")
    print(f"  YAY SKORU    : {o['yay_skoru']}")
    return o


def olcum_ayarlari_uygula():
    """3813 islemlik backtest bulgularini uygular."""
    cfg.w_breakout = 0.0       # BosHacim x TERS calisiyor, p=0.0007
    cfg.w_ttm = 0.0            # TTM sinyal yok, p=0.735
    cfg.w_ttm_birakma = 0.0    # ayni
    cfg.w_ubottom = 5.0        # en guclu olumlu sinyal, p=0.0117
    cfg.w_mini_kalite = 3.0    # calisiyor, p=0.047
    cfg.tip_kapisi = "col"     # YAYLA medyani -%7.00
    print("[ok] olculen ayarlar uygulandi:")
    print("  w_breakout=0 (ters), w_ttm=0 (etkisiz), w_ubottom=5, w_mini_kalite=3")
    print("  tip_kapisi='col' (YAYLA elendi)")


def kontrol_grubu(tr, veri=None, bt=None, kat=1, seed=42):
    """Gercek sinyallere karsi iki rastgele kontrol grubu uretir.

    tr  : backtest_calistir() ciktisi
    kat : her gercek sinyal icin kac kontrol uretilsin (1 = esit buyukluk)
    """
    veri = veri if veri is not None else globals().get("VERI", {})
    bt = bt or BTConfig()
    if tr is None or tr.empty:
        print("[kontrol] tablo bos."); return None
    rng = np.random.default_rng(seed)

    # hazirlanmis veriyi bir kez uret (yavas kisim burasi)
    print("[kontrol] veri hazirlaniyor...")
    hazir = {}
    for s, df in veri.items():
        try:
            d = _hazirla(df, cfg)
        except Exception:
            d = None
        if d is not None:
            hazir[s] = d
    semboller = list(hazir)
    if len(semboller) < 10:
        print("[kontrol] yeterli hisse yok."); return None
    print(f"[kontrol] {len(hazir)} hisse hazir, {len(tr)*kat} kontrol uretilecek")

    bas_pay = max(cfg.min_bars, cfg.kalite_pencere + 2)

    ayni_gun, ayni_hisse = [], []
    tarihler = pd.to_datetime(tr["Atılım"]).tolist()
    gercek_semboller = tr["Sembol"].tolist()

    for i in range(len(tr)):
        ts = tarihler[i]
        for _ in range(kat):
            # --- KONTROL 1: ayni tarih, rastgele hisse ---
            for _deneme in range(8):
                s = semboller[rng.integers(len(semboller))]
                d = hazir[s]
                D = int(d.index.searchsorted(ts))
                if bas_pay <= D < len(d) - 1:
                    islem = _bt_simule(d, D, bt)
                    if islem:
                        ayni_gun.append({"Sembol": s, "Atılım": str(d.index[D]), **islem})
                    break

            # --- KONTROL 2: ayni hisse, rastgele tarih ---
            s = gercek_semboller[i]
            d = hazir.get(s)
            if d is None or len(d) <= bas_pay + 2:
                continue
            for _deneme in range(8):
                D = int(rng.integers(bas_pay, len(d) - 1))
                islem = _bt_simule(d, D, bt)
                if islem:
                    ayni_hisse.append({"Sembol": s, "Atılım": str(d.index[D]), **islem})
                    break

    k1 = pd.DataFrame(ayni_gun)
    k2 = pd.DataFrame(ayni_hisse)

    print("\n" + "=" * 78)
    print("  EDGE TESTI — formasyon rastgeleden iyi mi?")
    print("=" * 78)
    satir = [{"grup": "FORMASYON (gercek)", **bt_metrikler(tr)}]
    if not k1.empty:
        satir.append({"grup": "kontrol: ayni gun, rastgele hisse", **bt_metrikler(k1)})
    if not k2.empty:
        satir.append({"grup": "kontrol: ayni hisse, rastgele gun", **bt_metrikler(k2)})
    tablo = pd.DataFrame(satir).set_index("grup")
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", None)
    print(tablo.to_string())

    # anlamlilik: formasyon vs ayni-gun kontrolu
    if not k1.empty:
        p = _perm_p(tr["Getiri%"].to_numpy(dtype=float),
                    k1["Getiri%"].to_numpy(dtype=float), seed=seed)
        fark = tr["Getiri%"].mean() - k1["Getiri%"].mean()
        print(f"\n  FORMASYON - (ayni gun rastgele) = {fark:+.2f} puan   p = {p:.4f}")
        if p < 0.05 and fark > 0:
            print("  -> Formasyonun GERCEK bir edge'i var. Kalibrasyon anlamli.")
        elif p < 0.05 and fark < 0:
            print("  -> Formasyon rastgeleden KOTU. Cekirdek kosullar gozden gecirilmeli.")
        else:
            print("  -> Fark anlamsiz. Olculen getiri buyuk olcude PIYASA suruklenmesi.")
            print("     Bu durumda filtre ince ayari yapmak bos ceki dovmek olur;")
            print("     once cekirdek kosullarin (gap + MA gecisi) degistirilmesi gerekir.")
    return {"formasyon": tr, "ayni_gun": k1, "ayni_hisse": k2, "tablo": tablo}


def _perm_p(a, b, n=3000, seed=42):
    """Iki grubun ortalama farki sansla aciklanabilir mi?"""
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    gercek = abs(a.mean() - b.mean())
    hep = np.concatenate([a, b]); na = len(a)
    rng = np.random.default_rng(seed); say = 0
    for _ in range(n):
        p = rng.permutation(hep)
        if abs(p[:na].mean() - p[na:].mean()) >= gercek:
            say += 1
    return say / n


def piyasa_egilimi(veri=None, bt=None, ornek=400, seed=7):
    """Saf piyasa taban cizgisi: rastgele hisse, rastgele gun.
       'Hicbir sey yapmasam ne olurdu' sorusunun cevabi."""
    veri = veri if veri is not None else globals().get("VERI", {})
    bt = bt or BTConfig()
    rng = np.random.default_rng(seed)
    semboller = list(veri)
    bas_pay = max(cfg.min_bars, cfg.kalite_pencere + 2)
    satir = []
    for _ in range(ornek):
        s = semboller[rng.integers(len(semboller))]
        try:
            d = _hazirla(veri[s], cfg)
        except Exception:
            continue
        if d is None or len(d) <= bas_pay + 2:
            continue
        D = int(rng.integers(bas_pay, len(d) - 1))
        islem = _bt_simule(d, D, bt)
        if islem:
            satir.append(islem)
    df = pd.DataFrame(satir)
    print("\n  PIYASA TABAN CIZGISI (rastgele hisse, rastgele gun):")
    for k, v in bt_metrikler(df).items():
        print(f"    {k:12s}: {v}")
    return df




# #####################################################################
#  IZLEME LISTESI — ATILIM SARTI OLMADAN YAY/TABAN ARAMA
#
#  NEDEN: tarayici atilimi SART kosuyor, yani sadece coktan patlamis
#  olanlari goruyor. En temiz, en uzun, en siki yaylar henuz patlamadiklari
#  icin listeye hic giremiyor.
#
#  BU FONKSIYON: gap/MA gecisi ARAMAZ. Sadece taban kalitesini olcer ve
#  fiyat HALA taban icindeyse (patlamamis) listeye alir. Patlamayi
#  beklemek yerine once adayi bulursun.
# #####################################################################

def izleme_listesi(veri=None, n=40, min_bar=15, min_sikilik=8.0,
                   patlamamis=True, yazdir=True):
    """Atilim beklemeden en iyi yay/taban adaylarini siralar.

    min_bar     : taban en az kac bar olmali
    min_sikilik : bar / ATR yogunlugu. taban_olc yuksekligi hep ~4 ATR'ye
                  sabitledigi icin TabanATR kalite olcusu DEGILDIR; asil olcu
                  ayni yuksekige kac bar sigdigidir. 70 bar / 3.7 ATR = 19 (cok siki),
                  20 bar / 3.3 ATR = 6 (gevsek).
    patlamamis  : True -> fiyat hala tavanin altinda olanlar (henuz patlamamis)
    """
    veri = veri if veri is not None else VERI
    if not veri:
        print("[izleme] VERI bos. Once hizli_baslat() calistir."); return pd.DataFrame()

    if RS_TABLO is None:
        rs_hesapla(veri)

    satir = []
    for sembol, df in veri.items():
        try:
            d = _hazirla(df, cfg)
        except Exception:
            d = None
        if d is None:
            continue
        D = len(d) - 1
        o = taban_olc(d, D + 1, cfg) if D + 1 <= len(d) else None
        if o is None:
            o = taban_olc(d, D, cfg)
        if o is None:
            continue
        sikilik = o["taban_bar"] / max(o["taban_atr"], 0.01)   # bar / ATR
        if o["taban_bar"] < min_bar or sikilik < min_sikilik:
            continue

        son = float(d["Close"].iloc[D])
        tavan, dip = o["taban_tavan"], o["taban_dip"]
        if tavan <= dip:
            continue
        konum = (son - dip) / (tavan - dip)          # 0 = dipte, 1 = tavanda
        # "patlamis" sayilmak icin tavani ATR'nin yarisi kadar asmis olmali.
        # (dar tabanda son bar cogu zaman tavanin KENDISIDIR; duz "son > tavan"
        #  kontrolu en siki tabanlari yanlislikla eliyordu)
        _atr = float(d["ATR"].iloc[D])
        if patlamamis and np.isfinite(_atr) and son > tavan + 0.5 * _atr:
            continue

        # olculebilir kalite gostergeleri
        bbr = float(d["BBWrank"].iloc[D]) if not pd.isna(d["BBWrank"].iloc[D]) else 1.0
        nb = int(o["taban_bar"])
        seg = d.iloc[max(0, D - nb):D + 1]
        up = float(seg.loc[seg["Close"] >= seg["Open"], "Volume"].sum())
        dn = float(seg.loc[seg["Close"] < seg["Open"], "Volume"].sum())
        net_alim = up / (up + dn) if (up + dn) > 0 else 0.0
        sqz_oran = float(seg["SQZ"].mean()) if "SQZ" in seg.columns else 0.0
        sqz_bar = int(d["SQZ_BAR"].iloc[D]) if "SQZ_BAR" in d.columns else 0

        obvw = seg["OBV"].to_numpy(dtype=float)
        volw = seg["Volume"].to_numpy(dtype=float)
        if len(obvw) >= 5:
            obv_norm = float(np.polyfit(np.arange(len(obvw)), obvw, 1)[0]) / (volw.mean() + 1e-9)
        else:
            obv_norm = 0.0

        yil = d.iloc[max(0, D - cfg.dip_pencere):D + 1]
        yhi, ylo = float(yil["High"].max()), float(yil["Low"].min())
        yil_konum = (son - ylo) / (yhi - ylo) if yhi > ylo else 1.0

        # ---- IZLEME SKORU (bilesenler ayri sutunda, kendin agirlik verebilirsin)
        s_dar     = min(sikilik / 25.0, 1.0)          # 25 bar/ATR = tam puan
        s_uzun    = min(nb / 60.0, 1.0)
        s_daralma = max(0.0, min((1 - o["daralma"]) / 0.5, 1.0))
        s_sqz     = sqz_oran
        s_bb      = max(0.0, 1 - bbr / 0.5)
        s_alim    = max(0.0, min((net_alim - 0.5) / 0.2, 1.0))
        s_obv     = max(0.0, min(obv_norm / 0.5, 1.0))
        s_dip     = max(0.0, 1 - yil_konum)
        s_hazir   = konum                                  # tavana yakinsa yakin

        skor = (2.0 * s_dar + 1.5 * s_uzun + 1.5 * s_daralma + 1.5 * s_sqz +
                1.0 * s_bb + 1.0 * s_alim + 1.5 * s_obv + 1.0 * s_dip + 1.0 * s_hazir)

        satir.append({
            "Sembol": sembol, "Skor": round(skor, 2),
            "TabanBar": nb, "TabanATR": o["taban_atr"],
            "Sıkılık": round(sikilik, 1), "Daralma": o["daralma"],
            "TavanDok": int(o["tavan_dok"]), "DipDok": int(o["dip_dok"]),
            "Konum": round(konum, 2), "Tavan": round(tavan, 2), "Fiyat": round(son, 2),
            "TavanaUzak%": round((tavan / son - 1) * 100, 1),
            "BBrank": round(bbr, 2), "TTM%": round(sqz_oran, 2), "TTMBar": sqz_bar,
            "Net_Alım": round(net_alim, 2), "OBVnorm": round(obv_norm, 3),
            "YılKonum": round(yil_konum, 2),
            **{k: v for k, v in zip(
                ["RS%", "Tepe%", "SMA200E%", "Mom126"],
                [(round(rs_oku(sembol, d.index[D]), 2) if RS_TABLO is not None else np.nan),
                 momentum_olc(d, D)["tepe_pct"],
                 momentum_olc(d, D)["sma200_egim"],
                 momentum_olc(d, D)["mom126"]])},
        })

    out = pd.DataFrame(satir)
    if out.empty:
        print("[izleme] Kriterlere uyan taban bulunamadi. min_bar/max_atr gevset.")
        return out
    out = out.sort_values("Skor", ascending=False).head(n).reset_index(drop=True)
    out.to_csv("izleme_listesi.csv", index=False)
    if yazdir:
        pd.set_option("display.max_rows", None)
        pd.set_option("display.width", 260)
        pd.set_option("display.max_columns", None)
        print(f"\n=== IZLEME LISTESI — en iyi {len(out)} yay/taban (atilim BEKLENMEDI) ===")
        print(out.to_string(index=False))
        print(f"\n'izleme_listesi.csv' yazildi.")
        print("  Sıkılık    : bar/ATR — yuksek = ayni yuksekige daha cok bar sigmis (siki yay)")
        print("  Konum      : 0 = taban dibinde, 1 = tavanda (patlamaya yakin)")
        print("  TavanaUzak%: kirilim seviyesine yuzde kac kaldi")
    return out




# #####################################################################
#  GORELI GUC / MOMENTUM — "olcemedigimiz durum"
#
#  GOZLEM: trend hisseleri kar veriyor, dip donusu yapanlar zarar.
#  (AAL +%11 vs JBS -%1; TEHOL +%60 vs PSPIL/Visne -%30)
#
#  TESHIS: kod bu ekseni hic olcmuyordu. Dahasi TERSINI odullendiriyor:
#  KonumCrp, yil dibindeki hisseye 1.00, zirvedekine 0.40 veriyor.
#
#  EKLENEN 4 OLCU (hicbiri puana katilmaz; once OLCULUR, sonra karar):
#    RS%      : caprazkesit goreli guc. 126 gunluk getirinin TUM evren
#               icindeki yuzdelik sirasi. 0.9 = evrenin en guclu %10'u.
#    Tepe%    : 52 haftanin zirvesinden yuzde kac asagida (tepe yuku).
#               Cok asagidaysa her seviyede sikismis satici var.
#    SMA200E% : 200 gunluk ortalamanin 20 barlik egimi (uzun vade yon).
#    Mom126   : 126 gunluk ham getiri.
# #####################################################################

RS_TABLO = None      # caprazkesit RS onbellegi (tarih x sembol)


def rs_hesapla(veri=None, pencere=126, sakla=True):
    """Tum evren icin caprazkesit goreli guc tablosu uretir.

    Her tarih icin: hissenin `pencere` gunluk getirisinin evren icindeki
    yuzdelik sirasi. Piyasa endeksi indirmeye gerek yok — evrenin kendisi
    olcut. Backtest'te de gecmis tarihlerde dogru RS okunabilir.
    """
    global RS_TABLO
    veri = veri if veri is not None else VERI
    if not veri:
        print("[rs] VERI bos."); return None
    kapanis = pd.DataFrame({s: df["Close"] for s, df in veri.items()})
    getiri = kapanis / kapanis.shift(pencere) - 1.0
    rs = getiri.rank(axis=1, pct=True)          # her tarihte capraz kesit
    if sakla:
        RS_TABLO = rs
        print(f"[rs] {rs.shape[1]} hisse x {rs.shape[0]} tarih icin RS hesaplandi "
              f"({pencere} gunluk getiri, caprazkesit yuzdelik)")
    return rs


def rs_oku(sembol, tarih):
    """RS_TABLO'dan (sembol, tarih) degerini okur. Yoksa nan."""
    if RS_TABLO is None or sembol not in RS_TABLO.columns:
        return np.nan
    try:
        i = RS_TABLO.index.searchsorted(pd.Timestamp(tarih))
        if i >= len(RS_TABLO):
            i = len(RS_TABLO) - 1
        v = RS_TABLO[sembol].iloc[i]
        return float(v) if np.isfinite(v) else np.nan
    except Exception:
        return np.nan


def momentum_olc(d, D, sembol=None):
    """Tek bar icin momentum/tepe yuku olculeri."""
    out = {}
    C = d["Close"].to_numpy(dtype=float)
    H = d["High"].to_numpy(dtype=float)
    son = float(C[D])

    # 52 haftalik zirveden uzaklik (tepe yuku / overhead supply)
    i0 = max(0, D - 252)
    zirve = float(H[i0:D + 1].max())
    out["tepe_pct"] = round((son / zirve - 1) * 100, 1) if zirve > 0 else 0.0

    # 126 gunluk ham getiri
    if D >= 126 and C[D - 126] > 0:
        out["mom126"] = round((son / C[D - 126] - 1) * 100, 1)
    else:
        out["mom126"] = np.nan

    # SMA200 egimi (uzun vade yon)
    kol = "EMA200" if "EMA200" in d.columns else ("EMA" if "EMA" in d.columns else None)
    if kol and D >= 20:
        a = float(d[kol].iloc[D]); b = float(d[kol].iloc[D - 20])
        out["sma200_egim"] = round((a / b - 1) * 100, 2) if (np.isfinite(a) and np.isfinite(b) and b) else np.nan
    else:
        out["sma200_egim"] = np.nan

    if sembol is not None:
        out["rs"] = round(rs_oku(sembol, d.index[D]), 2) if RS_TABLO is not None else np.nan
    return out


def momentum_sutun_ekle(tr, veri=None):
    """Backtest/tarama tablosuna RS%, Tepe%, SMA200E%, Mom126 ekler."""
    veri = veri if veri is not None else VERI
    if tr is None or tr.empty:
        return tr
    if RS_TABLO is None:
        rs_hesapla(veri)
    hazir = {}
    ek = []
    for _, r in tr.iterrows():
        s = r["Sembol"]
        if s not in hazir:
            df = veri.get(s)
            hazir[s] = _hazirla(df, cfg) if df is not None else None
        d = hazir[s]
        if d is None:
            ek.append({}); continue
        try:
            tarih = r["Atılım"] if "Atılım" in r else r.get("Tarih")
            D = int(d.index.searchsorted(pd.Timestamp(tarih)))
            D = min(D, len(d) - 1)
            ek.append(momentum_olc(d, D, s))
        except Exception:
            ek.append({})
    add = pd.DataFrame(ek, index=tr.index)
    ren = {"rs": "RS%", "tepe_pct": "Tepe%", "sma200_egim": "SMA200E%", "mom126": "Mom126"}
    for k_, v_ in ren.items():
        if k_ in add.columns:
            tr[v_] = add[k_]
    return tr


def momentum_testi(tr, veri=None):
    """Trend mi dip donusu mu kazandiriyor? Rakamla."""
    tr = momentum_sutun_ekle(tr, veri)
    print("\n" + "=" * 78)
    print("  TREND vs DIP DONUSU  (goreli guc ekseni)")
    print("=" * 78)
    for kol, esik, op, aciklama in [
            ("RS%", 0.7, ">", "evrenin en guclu %30'u"),
            ("RS%", 0.3, "<", "evrenin en zayif %30'u"),
            ("Tepe%", -15.0, ">", "52h zirvesine yakin (tepe yuku az)"),
            ("Tepe%", -50.0, "<", "zirveden %50+ asagida (tepe yuku agir)"),
            ("SMA200E%", 0.0, ">", "uzun vade trend YUKARI"),
            ("Mom126", 0.0, ">", "son 6 ay pozitif")]:
        if kol not in tr.columns:
            continue
        t = bt_filtre_karsilastir(tr, kol, esik, op)
        if t.empty:
            continue
        print(f"\n--- {kol} {op} {esik}   ({aciklama}) ---")
        print(t.to_string())
        p = bt_permutasyon_p(tr, kol, esik) if op == ">" else np.nan
        if np.isfinite(p):
            print(f"    p = {p:.4f}  -> {'ANLAMLI' if p < 0.05 else 'anlamsiz'}")

    if "RS%" in tr.columns:
        print("\n" + "=" * 78)
        print("  RS ESIK TARAMASI (goreli guc yukseldikce getiri ne oluyor?)")
        print("=" * 78)
        print(bt_esik_tarama(tr, "RS%", [0.1, 0.3, 0.5, 0.7, 0.9]).to_string())
    return tr




# #####################################################################
#  KIRILIM MUM KALITESI + RETEST GIRISI
#
#  DOKTRIN: "hacimli VE tam govdeli yesil mumla kirarsa balina teyidi;
#  hacimli kirmizi mumla asagi kirarsa gel-gel tuzagi."
#
#  OLCUM NOTU: hacmi TEK BASINA test ettik ve TERS cikti
#  (BosHacim x >1.5 -> %0.30 vs %1.30, p=0.0007). Ama govde kalitesi hic
#  olculmedi. Yuksek hacim + fitilli/kirmizi mum zaten "gel gel" tanimidir;
#  o -%0.30'u uretenler muhtemelen onlar. Bu yuzden BILESIMI olcuyoruz.
#
#  EKLENEN OLCULER (puana katilmaz, once olculur):
#    Gövde%    : govde / bar araligi. tam govde = yuksek.
#    KapPos    : kapanisin bar icindeki yeri. 1.0 = tepeden kapatti.
#    Yeşil     : kapanis > acilis
#    TamGövde  : yesil + govde>=%60 + kapanis ust %25'te  (balina mumu)
#    HacimTam  : TamGövde VE hacim > breakout_vol_kat  (doktrinin tam hali)
# #####################################################################

def mum_kalitesi(d, D):
    """Kirilim barinin mum yapisi."""
    o = float(d["Open"].iloc[D]); c = float(d["Close"].iloc[D])
    h = float(d["High"].iloc[D]); l = float(d["Low"].iloc[D])
    rng = max(h - l, 1e-9)
    govde = abs(c - o) / rng
    kap_pos = (c - l) / rng
    yesil = c > o
    tam = bool(yesil and govde >= 0.60 and kap_pos >= 0.75)
    return {"govde_pct": round(govde * 100, 0),
            "kap_pos": round(kap_pos, 2),
            "yesil": "YEŞİL" if yesil else "kırmızı",
            "tam_govde": "VAR" if tam else "-"}


def mum_sutun_ekle(tr, veri=None):
    """Backtest tablosuna mum kalitesi sutunlarini ekler."""
    veri = veri if veri is not None else VERI
    if tr is None or tr.empty:
        return tr
    hazir = {}; ek = []
    for _, r in tr.iterrows():
        sy = r["Sembol"]
        if sy not in hazir:
            df = veri.get(sy)
            hazir[sy] = _hazirla(df, cfg) if df is not None else None
        d = hazir[sy]
        if d is None:
            ek.append({}); continue
        try:
            D = int(d.index.searchsorted(pd.Timestamp(r["Atılım"])))
            D = min(D, len(d) - 1)
            m = mum_kalitesi(d, D)
            hac = float(r.get("BoşHacim×", 0) or 0)
            m["hacim_tam"] = "VAR" if (m["tam_govde"] == "VAR" and
                                       hac >= cfg.breakout_vol_kat) else "-"
            ek.append(m)
        except Exception:
            ek.append({})
    add = pd.DataFrame(ek, index=tr.index)
    ren = {"govde_pct": "Gövde%", "kap_pos": "KapPos", "yesil": "Yeşil",
           "tam_govde": "TamGövde", "hacim_tam": "HacimTam"}
    for k_, v_ in ren.items():
        if k_ in add.columns:
            tr[v_] = add[k_]
    return tr


def mum_testi(tr, veri=None):
    """Doktrini rakamla sina: hacim tek basina mi, govde ile birlikte mi?"""
    tr = mum_sutun_ekle(tr, veri)
    print("\n" + "=" * 78)
    print("  KIRILIM MUMU — 'hacimli + tam govdeli yesil' doktrini")
    print("=" * 78)
    for kol, esik, op, aciklama in [
            ("BoşHacim×", cfg.breakout_vol_kat, ">", "SADECE hacim (once ters cikmisti)"),
            ("TamGövde", "VAR", "==", "yesil + govde>=%60 + tepeden kapanis"),
            ("HacimTam", "VAR", "==", "DOKTRININ TAM HALI: hacim + tam govde"),
            ("Yeşil", "YEŞİL", "==", "sadece yesil mum"),
            ("KapPos", 0.75, ">", "tepeden kapanis"),
            ("Gövde%", 60.0, ">", "dolu govde")]:
        if kol not in tr.columns:
            continue
        t = bt_filtre_karsilastir(tr, kol, esik, op)
        if t.empty:
            continue
        print(f"\n--- {kol} {op} {esik}   ({aciklama}) ---")
        print(t.to_string())
        if op != "==":
            pv = bt_permutasyon_p(tr, kol, esik)
            if np.isfinite(pv):
                print(f"    p = {pv:.4f}  -> {'ANLAMLI' if pv < 0.05 else 'anlamsiz'}")
    return tr


# ---------------------------------------------------------------- RETEST GIRISI

def _bt_simule_retest(d, D, bt):
    """RETEST girisi: kirilimda ALMAZ. Fiyatin kirdigi seviyeye HACIMSIZ
    geri cekilmesini bekler; seviye tutarsa girer.

    Doktrin: 'balina kirdigi cizgiye hacimsiz geri doner, panikleyen satici
    kalmadigini olcer. Cizgi altina inmezse gercek yukselistir.'

    Kurallar:
      seviye  = kirilim barinin ACILISI (gap ile asilan direnc)
      pencere = retest_max_bar bar icinde geri cekilme olmali
      hacimsiz= retest barinin hacmi kirilim barinin retest_vol_kat kati altinda
      iptal   = KAPANIS seviyenin altina inerse islem yok (tuzak)
      giris   = seviyeye dokunan barin KAPANISI
    """
    seviye = float(d["Open"].iloc[D])
    kir_vol = float(d["Volume"].iloc[D])
    son = min(D + bt.retest_max_bar, len(d) - 1)

    for i in range(D + 1, son + 1):
        lo = float(d["Low"].iloc[i]); c = float(d["Close"].iloc[i])
        v = float(d["Volume"].iloc[i])
        if c < seviye:
            return None                      # seviye kaybedildi -> tuzak, islem yok
        if lo <= seviye * (1 + bt.retest_tol):
            if v <= kir_vol * bt.retest_vol_kat:
                return _bt_simule_giris(d, i, c, bt)   # hacimsiz retest -> GIR
            return None                      # hacimli geri cekilme -> saglam degil
    return None                              # hic geri cekilmedi -> islem yok


def _bt_simule_giris(d, e, giris, bt):
    """Verilen bar ve fiyattan cikis kurallarini uygular."""
    if not np.isfinite(giris) or giris <= 0:
        return None
    stop_f = giris * (1 - bt.stop_pct) if bt.stop_pct else None
    hedef_f = giris * (1 + bt.hedef_pct) if bt.hedef_pct else None
    ma_kol = f"EMA{bt.ma_cikis}" if (bt.ma_cikis and f"EMA{bt.ma_cikis}" in d.columns) else None
    son = min(e + bt.horizon, len(d) - 1)
    for i in range(e, son + 1):
        if stop_f is not None and float(d["Low"].iloc[i]) <= stop_f:
            return _bt_sonuc(d, e, i, giris, stop_f, "stop", bt)
        if hedef_f is not None and float(d["High"].iloc[i]) >= hedef_f:
            return _bt_sonuc(d, e, i, giris, hedef_f, "hedef", bt)
        if ma_kol and i > e:
            mv = float(d[ma_kol].iloc[i])
            if np.isfinite(mv) and float(d["Close"].iloc[i]) < mv:
                return _bt_sonuc(d, e, i, giris, float(d["Close"].iloc[i]), "ma_alti", bt)
    return _bt_sonuc(d, e, son, giris, float(d["Close"].iloc[son]), "süre", bt)


def giris_kurallari_karsilastir(veri=None, bt_temel=None):
    """Kirilimda gir vs RETEST bekle — hangisi daha iyi?"""
    temel = bt_temel or BTConfig()
    sonuc = []
    for ad, giris in [("KIRILIMDA GIR (sonraki acilis)", "sonraki_acilis"),
                      ("RETEST BEKLE (hacimsiz geri cekilme)", "retest")]:
        b = BTConfig(**{**temel.__dict__, "giris": giris})
        print(f"\n>>> {ad}")
        tr = backtest_calistir(veri, bt=b, ilerleme=False)
        sonuc.append({"giris": ad, **bt_metrikler(tr)})
    print("\n" + "=" * 78)
    print("  GIRIS ZAMANLAMASI")
    print("=" * 78)
    print(pd.DataFrame(sonuc).set_index("giris").to_string())
    print("\n  NOT: retest'te islem sayisi cok duser (cogu sinyal geri cekilmez).")
    print("       Az islemde metrikler oynak olur; 100'un altinda dikkatli yorumla.")
    return sonuc




# #####################################################################
#  ATILIM BARI = DEV HACIM BARI
#
#  FIKIR: ayrica "dev mum" aramaya gerek yok. Tarayicinin buldugu GAP
#  atilim barinin KENDISI dev hacim baridir. Aradigimiz emareleri o barda
#  ve sonrasinda ariyoruz.
#
#  KRITIK AYRIM (look-ahead):
#    A) BAR KALITESI  -> atilim aninda BILINIR. Puanlamada kullanilabilir.
#       (govde, kapanis yeri, ust fitil, RVOL, CQS, para akisi)
#    B) SONRASI TAKIP -> GELECEK bilgisi. Sinyal puanina katilamaz.
#       Ancak GECIKMELI GIRIS kurali olarak kullanilabilir (retest gibi).
#
#  Kullanicinin gonderdigi motordan duzeltilerek alindi. Duzeltilen
#  hatalar icin bkz. asagidaki [H1]..[H6] notlari.
# #####################################################################

def atilim_bar_kalitesi(d, D):
    """A) Atilim barinin KENDI kalitesi. Look-ahead YOK (sadece D'ye kadar)."""
    o = float(d["Open"].iloc[D]); c = float(d["Close"].iloc[D])
    h = float(d["High"].iloc[D]); l = float(d["Low"].iloc[D])
    rng = max(h - l, 1e-12)

    govde = abs(c - o) / rng
    ust_fitil = (h - max(o, c)) / rng
    alt_fitil = (min(o, c) - l) / rng
    clv = ((c - l) - (h - c)) / rng                       # -1 dipte, +1 tepede

    atr = float(d["ATR"].iloc[D]) if np.isfinite(d["ATR"].iloc[D]) else np.nan
    govde_atr = abs(c - o) / atr if (atr and atr > 0) else np.nan

    # RVOL: dev barin KENDI hacmi ortalamaya girmesin -> shift(1)
    i0 = max(0, D - 20)
    ort_vol = float(d["Volume"].iloc[i0:D].mean()) if D > i0 else np.nan
    rvol = float(d["Volume"].iloc[D]) / ort_vol if (ort_vol and ort_vol > 0) else np.nan

    # [H2] CQS: eski surumde agirliklar 30+25+10+10=75 idi ama esik 70'ti,
    # yani dal HIC ateslemiyordu. Gercek 0-100 olcegine normalize edildi.
    b_ = min(max(govde, 0), 1)
    c_ = min(max((clv + 1) / 2, 0), 1)
    l_ = min(max(alt_fitil, 0), 1)
    a_ = min(max((govde_atr / 3.0) if np.isfinite(govde_atr) else 0, 0), 1)
    u_ = min(max(ust_fitil, 0), 1)
    cqs = (0.35 * b_ + 0.30 * c_ + 0.10 * l_ + 0.15 * a_ - 0.25 * u_) / 0.90 * 100

    # --- GAP-DAHIL HAREKET ---
    # "Tam govdeli yesil mum" doktrini, fiyatin seviyeyi YUKSELEREK gectigi
    # bari varsayar. GAP bari ise seviyeyi ACILISTA atlar; gap govdeye dahil
    # olmadigi icin acilista ziplayip yatay kapanan bar "govdesiz" gorunur.
    # Bu yuzden gap'i iceren ayri bir olcu gerekir:
    pc = float(d["Close"].iloc[D - 1]) if D > 0 else o
    tam_alt = min(l, pc)
    tam_rng = max(h - tam_alt, 1e-12)
    gap_govde = (c - pc) / tam_rng          # onceki kapanistan bugunku kapanisa
    gap_kapanis = (c - tam_alt) / tam_rng   # gap dahil kapanis konumu

    return {"cqs": round(max(0.0, min(cqs, 100)), 1),
            "gap_govde": round(gap_govde, 2),
            "gap_kapanis": round(gap_kapanis, 2),
            "clv": round(clv, 2),
            "govde_r": round(govde, 2),
            "ust_fitil": round(ust_fitil, 2),
            "govde_atr_bar": round(govde_atr, 2) if np.isfinite(govde_atr) else np.nan,
            "rvol": round(rvol, 2) if np.isfinite(rvol) else np.nan}


def atilim_takip(d, D, takip=12, min_suzulme=3, destek_tol=0.015):
    """B) Atilim SONRASI davranis. GELECEK bilgisi — puanlamada KULLANILAMAZ.

    Atilim barinin acilisi = maliyet (gap ile asilan seviye)
    orta nokta / tepe = dev mum referanslari
    Doner: durum + kac barda ne oldugu.
    """
    if D + 1 >= len(d):
        return None
    O = float(d["Open"].iloc[D]); C0 = float(d["Close"].iloc[D])
    maliyet, tepe, orta = O, max(O, C0), (O + C0) / 2
    vol0 = float(d["Volume"].iloc[D])

    suzulme = 0; takip_yuksek = float(d["High"].iloc[D])
    son = min(D + takip, len(d) - 1)
    durum = "NOTR"; kac_bar = 0

    for i in range(D + 1, son + 1):
        kac_bar = i - D
        c = float(d["Close"].iloc[i]); h = float(d["High"].iloc[i])
        v = float(d["Volume"].iloc[i])
        atr = float(d["ATR"].iloc[i]) if np.isfinite(d["ATR"].iloc[i]) else np.nan
        govde_atr = abs(c - float(d["Open"].iloc[i])) / atr if (atr and atr > 0) else 1.0
        takip_yuksek = max(takip_yuksek, h)
        rvol = v / vol0 if vol0 > 0 else np.nan

        if c < maliyet * (1 - destek_tol):
            return {"takip_durum": "TUZAK - GAP DIBI KIRILDI", "takip_bar": kac_bar,
                    "suzulme_bar": suzulme}
        if np.isfinite(rvol) and rvol < 1.0 and govde_atr < 0.75:
            suzulme += 1
        else:
            suzulme = max(0, suzulme - 1)

        if c > tepe and np.isfinite(rvol) and rvol >= 0.5:
            durum = "YUKARI DEVAM"
        elif suzulme >= min_suzulme and c >= maliyet:
            durum = "HACIMSIZ SUZULME - SAGLAM"
        elif c < orta:
            durum = "ORTA NOKTA KIRILDI - ZAYIF"
        elif kac_bar >= 2 and takip_yuksek <= tepe * 1.005 and \
                np.isfinite(rvol) and rvol < 0.5:
            durum = "TALEP SONUYOR - DAGITIM RISKI"

    return {"takip_durum": durum, "takip_bar": kac_bar, "suzulme_bar": suzulme}


def atilim_kalite_sutun_ekle(tr, veri=None, takip_ekle=False):
    """Backtest tablosuna atilim bari kalitesi ekler.

    takip_ekle VARSAYILAN OLARAK FALSE. Tarayici 'atilim YAPAN' hisseyi
    arar; sonrasinin takibi AYRI bir istir. Takip verisi gelecek bilgisidir
    ve yanlislikla filtre olarak kullanilirsa look-ahead yaratir.
    Bilerek gormek istersen: atilim_kalite_sutun_ekle(tr, takip_ekle=True)
    """
    veri = veri if veri is not None else VERI
    if tr is None or tr.empty:
        return tr
    hazir = {}; ek = []
    for _, r in tr.iterrows():
        sy = r["Sembol"]
        if sy not in hazir:
            df = veri.get(sy)
            hazir[sy] = _hazirla(df, cfg) if df is not None else None
        d = hazir[sy]
        if d is None:
            ek.append({}); continue
        try:
            D = int(d.index.searchsorted(pd.Timestamp(r["Atılım"])))
            D = min(D, len(d) - 1)
            rec = atilim_bar_kalitesi(d, D)
            if takip_ekle:
                t = atilim_takip(d, D)
                if t:
                    rec.update(t)
            ek.append(rec)
        except Exception:
            ek.append({})
    add = pd.DataFrame(ek, index=tr.index)
    ren = {"cqs": "CQS", "gap_govde": "GapGövde", "gap_kapanis": "GapKapanış",
           "clv": "CLV", "govde_r": "GövdeR", "ust_fitil": "ÜstFitil",
           "govde_atr_bar": "GövdeATR", "rvol": "RVOL",
           "takip_durum": "TakipDurum", "takip_bar": "TakipBar",
           "suzulme_bar": "SüzülmeBar"}
    for k_, v_ in ren.items():
        if k_ in add.columns:
            tr[v_] = add[k_]
    return tr


def atilim_kalite_testi(tr, veri=None, takip_goster=False):
    """Atilim barinin kalitesi getiriyi ongoruyor mu?

    UYARI: 'TakipDurum' GELECEK bilgisidir. Sinyal filtresi olarak
    KULLANILAMAZ; sadece 'ne oldu' dokumudur. Filtre adayi olanlar
    CQS / CLV / GovdeR / UstFitil / RVOL'dur (atilim aninda bilinir).
    """
    tr = atilim_kalite_sutun_ekle(tr, veri, takip_ekle=takip_goster)
    print("\n" + "=" * 78)
    print("  ATILIM BARI KALITESI  (look-ahead YOK — filtre adayi)")
    print("=" * 78)
    for kol, esik, op, ac in [("GapGövde", 0.6, ">", "GAP DAHIL dolu hareket"),
                              ("GapKapanış", 0.75, ">", "GAP dahil tepeden kapanis"),
                              ("CQS", 65.0, ">", "kaliteli dev mum"),
                              ("CLV", 0.5, ">", "tepeye yakin kapanis"),
                              ("GövdeR", 0.6, ">", "dolu govde"),
                              ("ÜstFitil", 0.3, ">", "uzun ust fitil (satis baskisi)"),
                              ("RVOL", 3.0, ">", "dev hacim")]:
        if kol not in tr.columns:
            continue
        t = bt_filtre_karsilastir(tr, kol, esik, op)
        if t.empty:
            continue
        print(f"\n--- {kol} {op} {esik}  ({ac}) ---")
        print(t.to_string())
        pv = bt_permutasyon_p(tr, kol, esik)
        if np.isfinite(pv):
            print(f"    p = {pv:.4f}  -> {'ANLAMLI' if pv < 0.05 else 'anlamsiz'}")

    if "TakipDurum" in tr.columns:
        print("\n" + "=" * 78)
        print("  ATILIM SONRASI NE OLDU  (GELECEK bilgisi — filtre DEGIL)")
        print("=" * 78)
        for dur, gr in tr.groupby("TakipDurum"):
            m = bt_metrikler(gr)
            print(f"  {dur:38s} {m['işlem']:5d} islem  ort %{m['ortGetiri%']:6.2f}"
                  f"  kazanma %{m['kazanma%']:5.1f}")
        print("\n  Bu tablo 'hangi takip durumu kazandirir' sorusunu cevaplar,")
        print("  ama girisi ONA gore yapamazsin — bilgi giristen SONRA olusur.")
        print("  Kullanilabilir hali: giris_kurallari_karsilastir() icindeki")
        print("  gecikmeli giris (retest) mantigi.")
    return tr


# =====================================================================
#  TEK HUCRE CALISTIRMA
#  OTO_CALISTIR = True ise bu hucre calisinca her sey otomatik yapilir:
#  onbellekten yukle -> eksikleri tamamla -> bayatlari ele -> tara.
#  Onbellek sayesinde ~30 sn surer. Colab oturumu kopunca sadece bu
#  hucreyi tekrar calistir, yeter.
#  Sadece tanimlar yuklensin istersen yukarida OTO_CALISTIR = False yap.
# =====================================================================
SURUM = "2026-08-06c"
print(f"[ok] COL ATILIM TARAYICI yuklendi.  SURUM: {SURUM}")
print("  Tarama    :  hizli_baslat()")
print("  Teshis    :  col_teshis('SPSC')   |  taban_teshis('TPG')")
print("  Ayarlar   :  olcum_ayarlari_uygula()")
print("  Backtest  :  tr = backtest_calistir(); bt_rapor(tr)")
print("  Edge testi:  k = kontrol_grubu(tr)")
print("  IZLEME    :  izleme_listesi()   <- atilim beklemeden yay/taban adaylari")
print("  MOMENTUM  :  momentum_testi(tr)  <- trend mi dip donusu mu kazandiriyor?")
print("  MUM       :  mum_testi(tr)       <- hacimli+tam govde doktrini")
print("  RETEST    :  giris_kurallari_karsilastir()")
print("  ATILIM BAR:  atilim_kalite_testi(tr)  <- gap bari = dev hacim bari")

if OTO_CALISTIR:
    print("\n[oto] OTO_CALISTIR=True -> tarama basliyor...\n")
    tablo = hizli_baslat()
