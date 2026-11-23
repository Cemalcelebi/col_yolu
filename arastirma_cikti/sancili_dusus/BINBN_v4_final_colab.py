# Cemal'in 21 Kasım 2026'da yapıştırdığı kod ("Çöl Yolu v3, BINBN sancılı düşüş debug" sohbetinden; Colab). OLDUĞU GİBİ saklanır.
# Değerlendirme ve ölçülebilir karşılığı: arastirma_cikti/sancili_dusus/ altındaki rapor dosyaları.
import gdown, os
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import matplotlib.dates as md
import pandas as pd, numpy as np

if not os.path.exists("/content/BINBN.csv"):
    gdown.download("https://drive.google.com/uc?id=1-eMtoi4bLxeQSwR3gdxxmGKetyvCzugg","/content/BINBN.csv",quiet=True)

df=pd.read_csv("/content/BINBN.csv")
cm={"price":"Date","date":"Date","open":"Open","high":"High","low":"Low","close":"Close","adj close":"Close","volume":"Volume"}
df.columns=[cm.get(c.strip().lower(),c.strip()) for c in df.columns]
df["Date"]=pd.to_datetime(df["Date"],errors="coerce")
df=df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
for c in ["Open","High","Low","Close"]:
    df[c]=pd.to_numeric(df[c].astype(str).str.replace(",","",regex=False),errors="coerce")
df["Volume"]=pd.to_numeric(df.get("Volume",pd.Series([0]*len(df))).astype(str).str.replace(",","",regex=False),errors="coerce").fillna(0)
df=df.dropna(subset=["Open","High","Low","Close"]).reset_index(drop=True)
n=len(df)
df["body_pct"]=((df["Close"]-df["Open"]).abs()/df["Open"].replace(0,np.nan))*100
gm=df["body_pct"].median()

W=10; W_once=10; W_dip=30

body_r=df["body_pct"].rolling(W).median()/gm
rh=df["High"].rolling(W).max()
rl=df["Low"].rolling(W).min()
rm=(rh+rl)/2
hw=(rh-rl)/rm.replace(0,np.nan)
cl_end=df["Close"]
cl_start=df["Close"].shift(W-1)
sl_col=(cl_end-cl_start)/(rm.replace(0,np.nan)*W)

mask=(body_r<0.75)&(hw>=0.02)&(hw<=0.28)

# ── YENİ: Sancılı Düşüş Tespiti ──────────────────────────────────────────────
# Mantık:
#   1) Çöl öncesi W_dip barda fiyat düşüş eğiminde (pre_slope < 0)
#   2) Çöl boyunca küçük mumlar (body_r düşük) → zaten mask kapsıyor
#   3) Çöl alt bandı, önceki W_dip periyodunun en düşük seviyesine yakın (dip_yakin < eşik)
#   4) Çöl sonrası sonuç → sağ ayak doğrulaması P gibi davranır (yukarı çıkış)

def pre_slope(start, lookback=20):
    """Çöl başından lookback bar önceye bak, kapanış eğimini hesapla."""
    s = max(0, start - lookback)
    e = start
    if e - s < 3:
        return 0.0
    prices = df["Close"].iloc[s:e].values
    x = np.arange(len(prices))
    slope = np.polyfit(x, prices, 1)[0]
    # Normalize: eğimi ortalama fiyata böl
    mean_p = prices.mean()
    return slope / mean_p if mean_p > 0 else 0.0

cols=[]; in_col=False; start=0; gap=0; GAP_TOL=2
for i in range(W+W_once, n):
    if mask.iloc[i]:
        if not in_col:
            in_col=True; start=max(0,i-W+1)
        gap=0
    elif in_col:
        gap+=1
        if gap<=GAP_TOL and i<n-1:
            continue
        in_col=False; end=i-gap
        gap=0
        if end-start<5: continue
        t=df["High"].iloc[start:end+1].max()
        b=df["Low"].iloc[start:end+1].min()
        sl_val=sl_col.iloc[end]
        pre_low=df["Low"].iloc[max(0,start-W_dip):start].min()
        pre_high=df["High"].iloc[max(0,start-W_dip):start].max()
        col_start_price=df["Close"].iloc[start]
        dip_yakin=(col_start_price-pre_low)/pre_low if pre_low>0 else 999
        zirve_yakin=(pre_high-col_start_price)/pre_high if pre_high>0 else 999

        # Sancılı düşüş eğimi
        pslope = pre_slope(start, lookback=25)

        # ── TİP KARARI ───────────────────────────────────────────────────────
        # Önce Sancılı Düşüş kontrolü:
        #   - Önceki eğim negatif (düşüş içinde donmuş)
        #   - Çöl alt bandı dip bölgesine çok yakın
        #   - Çöl eğimi yatay veya hafif negatif (sancılı düşüş = yavaş iner)
        sancili = (
            sl_val < -0.0003           # çöl içi aşağı sürünüyor
            and dip_yakin < 0.35       # dip bölgesinde
        )

        if sancili:
            tip = "SD"
        elif sl_val>0.0005 and dip_yakin<0.15: tip="P"
        elif sl_val<-0.0005 and zirve_yakin<0.15: tip="N"
        elif sl_val>0.0005: tip="P?"
        elif sl_val<-0.0005: tip="N?"
        else: tip="?"

        egim="→" if abs(sl_val)<0.0005 else ("↗" if sl_val>0 else "↘")
        cols.append({"sd":df["Date"].iloc[start],"ed":df["Date"].iloc[end],
                     "si":start,"ei":end,
                     "t":t,"b":b,"n":end-start,"tip":tip,"egim":egim,
                     "ed_price":df["Close"].iloc[end],
                     "pslope":pslope,"dip_yakin":dip_yakin})

def merge_cols(cols):
    if not cols: return []
    cols=sorted(cols,key=lambda x:x["sd"])
    merged=[cols[0].copy()]
    for d in cols[1:]:
        prev=merged[-1]
        if d["sd"]<=prev["ed"]+pd.Timedelta(days=3):
            prev["ed"]=max(prev["ed"],d["ed"])
            prev["ei"]=max(prev["ei"],d["ei"])
            prev["t"]=max(prev["t"],d["t"])
            prev["b"]=min(prev["b"],d["b"])
            if "P" in d["tip"] and "N" not in prev["tip"]: prev["tip"]=d["tip"]
        else:
            merged.append(d.copy())
    return merged

cols=merge_cols(cols)

# ── PUAN FONKSİYONU ──────────────────────────────────────────────────────────
def puan_hesapla(max_h):
    if max_h >= 1.00: return 5, "[5P]"
    elif max_h >= 0.50: return 4, "[4P]"
    elif max_h >= 0.25: return 3, "[3P]"
    elif max_h >= 0.10: return 2, "[2P]"
    elif max_h >= 0.01: return 1, "[1P]"
    else: return 0, "[-]"

def ihlal_tolerans(max_h):
    """Getiri büyüdükçe ihlal toleransı genişler"""
    if max_h >= 1.00: return 0.08
    elif max_h >= 0.50: return 0.05
    elif max_h >= 0.25: return 0.03
    elif max_h >= 0.10: return 0.02
    else: return 0.01

# ── SAĞ AYAK DOĞRULAMA ────────────────────────────────────────────────────────
for d in cols:
    t=d["t"]; b=d["b"]
    ei=d["ei"]
    baslangic_fiyat=df["Close"].iloc[ei]
    max_hareket=0.0; ihlal=False

    pozitif_tip = d["tip"] in ("P","P?","SD")

    ihlal_sayac = 0
    for j in range(ei+1, min(ei+30, n)):
        close=df["Close"].iloc[j]
        tol = ihlal_tolerans(max_hareket)  # anlık getiriye göre dinamik tolerans

        if pozitif_tip:
            if close < b * (1 - tol):
                ihlal_sayac += 1
                if ihlal_sayac >= 2:
                    ihlal=True; break
            else:
                ihlal_sayac = 0
            yukari=(close-baslangic_fiyat)/baslangic_fiyat
            max_hareket=max(max_hareket, yukari)
        else:
            if close > t * (1 + tol):
                ihlal_sayac += 1
                if ihlal_sayac >= 2:
                    ihlal=True; break
            else:
                ihlal_sayac = 0
            asagi=(baslangic_fiyat-close)/baslangic_fiyat
            max_hareket=max(max_hareket, asagi)

    # En az 2 kapanış %10 üstünde tutunma kontrolü
    hedef_tutunma = False
    tutunma_sayac = 0
    for j2 in range(ei+1, min(ei+30, n)):
        close2 = df["Close"].iloc[j2]
        yukari2 = (close2 - baslangic_fiyat) / baslangic_fiyat
        if yukari2 >= 0.10:
            tutunma_sayac += 1
            if tutunma_sayac >= 2:
                hedef_tutunma = True
                break
        else:
            tutunma_sayac = 0  # tutunma bozuldu, sıfırla

    puan, yildiz = puan_hesapla(max_hareket)
    d["ihlal"]=ihlal
    d["puan"]=puan
    d["yildiz"]=yildiz
    d["max_hareket"]=max_hareket
    d["dogru"]=not ihlal and hedef_tutunma
for i, d in enumerate(cols):
    if not d["dogru"] and not d["ihlal"]:
        # Sonraki çöl var mı?
        if i+1 < len(cols):
            d["basarisiz"] = True
        else:
            d["basarisiz"] = False
    else:
        d["basarisiz"] = False

# ── RAPOR ─────────────────────────────────────────────────────────────────────
print(f"BINBN | {n} bar | {len(cols)} çöl")
print(f"{'='*70}")
for i,d in enumerate(cols,1):
    durum="DOGRU" if d["dogru"] else ("IHLAL" if d["ihlal"] else ("BASARISIZ" if d["basarisiz"] else "BEKLE"))
    sd_tag = " [SANCİLI DÜŞÜŞ]" if d["tip"]=="SD" else ""
    print(f"#{i}[{d['tip']}]{d['egim']}{sd_tag}  {d['sd'].strftime('%Y-%m-%d')} → {d['ed'].strftime('%Y-%m-%d')}")
    print(f"   Ust:{d['t']:.1f} Alt:{d['b']:.1f} | pslope:{d['pslope']:.4f} | dip_yakin:{d['dip_yakin']:.2f}")
    print(f"   Max hareket:{d['max_hareket']:.1%} | Puan:{d['yildiz']} | {durum}")
    print()

# ── PLOTLY GRAFİK ────────────────────────────────────────────────────────────
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ticker = "BINBN"
sd_count = sum(1 for d in cols if d["tip"]=="SD")

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    row_heights=[0.8, 0.2], vertical_spacing=0.02)

fig.add_trace(go.Candlestick(
    x=df["Date"],
    open=df["Open"], high=df["High"],
    low=df["Low"], close=df["Close"],
    increasing_line_color="#26a69a",
    decreasing_line_color="#ef5350",
    name="Fiyat"), row=1, col=1)

colors_vol = ["#26a69a" if c>=o else "#ef5350" for c,o in zip(df["Close"],df["Open"])]
fig.add_trace(go.Bar(x=df["Date"], y=df["Volume"], marker_color=colors_vol,
                     name="Hacim", showlegend=False), row=2, col=1)

for d in cols:
    tip = d["tip"]
    if d["dogru"]:
        color = "rgba(129,201,149,0.15)"; border = "#81c995"
    elif d["ihlal"]:
        color = "rgba(242,139,130,0.15)"; border = "#f28b82"
    elif d["basarisiz"]:
        color = "rgba(136,136,255,0.15)"; border = "#8888ff"
    else:
        color = "rgba(247,201,72,0.15)"; border = "#f7c948"
    if tip=="SD" and not d["dogru"]:
        color = "rgba(255,152,0,0.15)"; border = "#ff9800"

    label_tip = "SD" if tip=="SD" else tip
    durum = "DOGRU" if d["dogru"] else ("IHLAL" if d["ihlal"] else ("BASARISIZ" if d["basarisiz"] else "BEKLE"))
    label = f"[{label_tip}]{d['yildiz']}{d['max_hareket']:.0%} {durum}"

    fig.add_shape(type="rect",
        x0=d["sd"], x1=d["ed"],
        y0=d["b"], y1=d["t"],
        fillcolor=color, line=dict(color=border, width=2),
        row=1, col=1)
    fig.add_annotation(
        x=d["sd"], y=d["t"],
        text=label, showarrow=False,
        font=dict(color=border, size=10, family="monospace"),
        xanchor="left", yanchor="bottom",
        row=1, col=1)

fig.update_layout(
    title=f"{ticker} | {len(cols)} col | SD={sd_count} Sancili Dusus",
    template="plotly_dark",
    xaxis_rangeslider_visible=False,
    height=700,
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(color="#e6edf3"),
)
fig.update_xaxes(gridcolor="#21262d", showgrid=True)
fig.update_yaxes(gridcolor="#21262d", showgrid=True)

fig.write_html("/content/BINBN_v4_final.html")

# Drive'a kopyala
import shutil
try:
    from google.colab import drive
    drive.mount("/content/drive", force_remount=False)
    shutil.copy("/content/BINBN_v4_final.html", "/content/drive/MyDrive/COLAB_VERILER/BINBN_v4_final.html")
    print("Drive'a kaydedildi: COLAB_VERILER/BINBN_v4_final.html")
except:
    print("Drive mount edilemedi, /content/BINBN_v4_final.html adresinde mevcut")

from IPython.display import HTML
HTML("<b>Grafik hazir! Sol menuden Files > BINBN_v4_final.html dosyasini indirin</b>")
