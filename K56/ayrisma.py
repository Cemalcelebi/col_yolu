"""K56-AYR: (iii) 'olay dizisinden rastgele gün' ile 'dizinin bütün günleri' ayrışması (ONKAYIT_K56 v1.3-AYR; Cemal, 31 Eki madde 4).

Olay dizisi D_e: K55 olayından (t0) başlayan kesintisiz nitelikli likit gün dizisi (aynı sembol, ardışık i, dönem içinde kesik; faz1_yerel ile aynı döngü).
Gün katkısı u = z − c: z = gün × vd içinde standartlaştırılmış değişken (K55 _z_gun_vd), c = aynı (gün, vd) grubunda hiçbir dizide olmayan satırların z
ortalaması (grup < 5 ise gün içi). f_e = dizinin geçerli günlerinde u ortalaması.
E1 = olay ağırlıklı ortalama (her olay bir; (iii)'ün beklenen değeri); E2 = gün ağırlıklı ortalama (Σ L f / Σ L; dizi günleri havuzu); G = isaret × (E1 − E2),
isaret = KEŞİF d(i) işareti (±1). Kimlik: E1 − E2 = −Cov_e(L, f) / ortalama L (ağırlık farkı). Konum bantları (1, 2-5, 6-20, 21+) ve uzunluk katmanları.
Kümeli bootstrap (aynı çekilişlerden bütün istatistikler): birincil ay(t0) (K55 standardı), ikinci sembol|yıl(t0); bilgi: olay, blok60.
Yapay veri: aynı ölçüler dört Faz 0 spekinde (karar) ve iki kalibre spekte (duyarlılık). Hiçbir sonuç bir satırı 'gerçek etki'ye çevirmez (v1.3 P7).
"""
from __future__ import annotations

import hashlib
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .ortak import donem_kapisi, log

AYR: Dict[str, Any] = {"bantlar": ((1, 1), (2, 5), (6, 20), (21, 10 ** 9)), "boot": 2000, "n_min": 30, "cekilis": 200, "cekilis_tohum0": 56,
                       "grup_en_az": 5, "kimlik_tol": 1e-9, "e2_sifir_oran": 0.20}
ETIKET_GERCEK = "gercek"   # v1.3-c: bootstrap tohum metni etiketi içerir; gerçek veri koşuları (AYR ve sızıntı T1 ayrışma karşılaştırması) bu etiketle koşar
BANT_AD = ("1", "2-5", "6-20", "21+")


# ---------------------------------------------------------------- olay dizileri
def diziler(sem: np.ndarray, ii: np.ndarray, olay_ix: np.ndarray, nit_d: np.ndarray) -> np.ndarray:
    """Her olay satırı için dizi uzunluğu L (faz1_yerel.rastgele_gun_maskesi ile aynı döngü)."""
    n = len(sem); L = np.ones(len(olay_ix), dtype=np.int64)
    for j, k in enumerate(olay_ix):
        q = 1
        while k + q < n and sem[k + q] == sem[k] and ii[k + q] == ii[k] + q and nit_d[k + q]:
            q += 1
        L[j] = q
    return L


def kesilme_nedeni(sem: np.ndarray, ii: np.ndarray, son_ix: np.ndarray, likit: np.ndarray, nit: np.ndarray, don_ok: np.ndarray) -> np.ndarray:
    """Dizinin bittiği satırdan sonraki satır neden nitelikli değil (betimleyici): seri sonu / boşluk, likit değil, dönem etiketi, getiri eşik altı ya da
    pencere tanımsız."""
    n = len(sem); out = np.empty(len(son_ix), dtype=object)
    for j, k in enumerate(son_ix):
        q = k + 1
        if q >= n or sem[q] != sem[k] or ii[q] != ii[k] + 1:
            out[j] = "seri sonu / boşluk"
        elif not likit[q]:
            out[j] = "likit değil"
        elif not don_ok[q]:                                               # dönem dışı etiketli günün getirisi okunmaz (İÇ -> BAĞIMSIZ sızıntısı yok)
            out[j] = "dönem etiketi (pencere dönem dışı)"
        else:
            out[j] = "getiri eşik altı ya da pencere tanımsız"
    return out


# ---------------------------------------------------------------- kümeli bootstrap (bütün istatistikler aynı çekilişten)
def kume_cekilis(kume: np.ndarray, B: int, rng: np.random.Generator) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """K55 istatistik.boot_kume ile aynı algoritma: kümeler yerine koyarak, (B, K) dizini. Dönüş: (küme dizini inv, seçim)."""
    k, inv = np.unique(kume, return_inverse=True); K = len(k)
    return inv, (rng.integers(0, K, size=(B, K)) if K >= 2 else None)


def oran_boot(pay: np.ndarray, payda: np.ndarray, inv: np.ndarray, sec: Optional[np.ndarray]) -> Tuple[float, np.ndarray]:
    """Σ pay / Σ payda ve aynı çekilişlerdeki bootstrap dağılımı (boot_kume: x·w / w)."""
    K = int(inv.max()) + 1 if len(inv) else 0
    sp = np.bincount(inv, weights=pay, minlength=K); sq = np.bincount(inv, weights=payda, minlength=K)
    nokta = float(sp.sum() / sq.sum()) if sq.sum() > 0 else np.nan
    if sec is None:
        return nokta, np.full(1, np.nan)
    den = sq[sec].sum(axis=1)
    return nokta, sp[sec].sum(axis=1) / np.where(den > 0, den, np.nan)


def _ara(bs: np.ndarray) -> Tuple[float, float]:
    bs = bs[np.isfinite(bs)]
    return (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))) if len(bs) else (np.nan, np.nan)


# ---------------------------------------------------------------- satır ölçüsü
def satir_olc(z: np.ndarray, gun: np.ndarray, vd: np.ndarray, gunler: List[np.ndarray], pozlar: List[np.ndarray], L: np.ndarray, s: float,
              kumeler: Dict[str, np.ndarray], gun_t0: np.ndarray, tohum_metni: str, B: int = AYR["boot"]) -> Dict[str, Any]:
    """z, gun, vd: m satırları (dönem, likit, x tanımlı). gunler[j]: olay j'nin dizi günlerinin m içindeki konumları (x tanımsız gün atlanır);
    pozlar[j]: bu günlerin dizideki konumu (1 = t0); L: dizinin tam uzunluğu; kumeler: olay başına küme etiketleri; gun_t0: olay günü."""
    n = len(z); N = len(gunler)
    birlesim = np.zeros(n, bool)
    for g in gunler:
        birlesim[g] = True
    # kontrol c: aynı (gün, vd) grubunda dizi dışı satırların z ortalaması; grup < 5 ise gün içi
    D = pd.DataFrame({"g": gun, "v": vd, "z": np.where(birlesim, np.nan, z)})
    c1 = D.groupby(["g", "v"]).z.transform("mean").to_numpy(); n1 = D.groupby(["g", "v"]).z.transform("count").to_numpy()
    c2 = D.groupby("g").z.transform("mean").to_numpy(); n2 = D.groupby("g").z.transform("count").to_numpy()
    c = np.where(n1 >= AYR["grup_en_az"], c1, np.where(n2 >= AYR["grup_en_az"], c2, np.nan)); u = z - c
    f = np.full(N, np.nan); Lm = np.zeros(N); bant = np.full((N, 4), np.nan); u1 = np.full(N, np.nan)
    for j, g in enumerate(gunler):
        if not len(g):
            continue
        ug = u[g]; v = np.isfinite(ug); poz = pozlar[j]
        if v.any():
            f[j] = ug[v].mean(); Lm[j] = v.sum()
        for b, (a_, b_) in enumerate(AYR["bantlar"]):
            mb = v & (poz >= a_) & (poz <= b_)
            if mb.any():
                bant[j, b] = ug[mb].mean()
        if poz[0] == 1 and v[0]:
            u1[j] = ug[0]
    gec = np.isfinite(f); out: Dict[str, Any] = {"n_olay": int(N), "n_gecerli": int(gec.sum()), "n_kayip": int(N - gec.sum())}
    if gec.sum() < AYR["n_min"]:
        out["karar_veri"] = "VERİ YETERSİZ"; return out
    rng = np.random.default_rng(int(hashlib.sha256(tohum_metni.encode()).hexdigest()[:12], 16))
    fe, Le = f[gec], Lm[gec]; kum = {k: np.asarray(v)[gec] for k, v in kumeler.items()}
    for kad, kv in kum.items():
        inv, sec = kume_cekilis(kv, B, rng)
        e1, b1 = oran_boot(fe, np.ones(len(fe)), inv, sec); e2, b2 = oran_boot(fe * Le, Le, inv, sec); bg = s * (b1 - b2)
        out.update({f"E1_{kad}_alt": _ara(b1)[0], f"E1_{kad}_ust": _ara(b1)[1], f"E2_{kad}_alt": _ara(b2)[0], f"E2_{kad}_ust": _ara(b2)[1],
                    f"G_{kad}_alt": _ara(bg)[0], f"G_{kad}_ust": _ara(bg)[1], f"K_{kad}": int(inv.max() + 1)})
        if kad == "ay":
            out.update({"E1": e1, "E2": e2, "G": s * (e1 - e2)})
            for b in range(4):                                             # konum bantları (olay ağırlıklı), aynı çekilişler
                vb = np.isfinite(bant[gec, b])
                if vb.sum() >= 1:
                    nb, bb = oran_boot(np.where(vb, bant[gec, b], 0.0), vb.astype(float), inv, sec)
                    out.update({f"bant{BANT_AD[b]}": nb, f"bant{BANT_AD[b]}_alt": _ara(bb)[0], f"bant{BANT_AD[b]}_ust": _ara(bb)[1], f"bant{BANT_AD[b]}_n": int(vb.sum())})
    Lbar = Le.mean(); out["kimlik_fark"] = float((out["E1"] - out["E2"]) - (-np.mean((Le - Lbar) * (fe - fe.mean())) / Lbar))     # 0 olmalı (1e-9)
    # uzunluk katmanları: E1 ve konum 1 (t0)
    for b, (a_, b_) in enumerate(AYR["bantlar"]):
        mk = (L[gec] >= a_) & (L[gec] <= b_); out[f"Lkat{BANT_AD[b]}_n"] = int(mk.sum())
        out[f"Lkat{BANT_AD[b]}_E1"] = float(fe[mk].mean()) if mk.sum() >= AYR["n_min"] else np.nan
        u1k = u1[gec][mk]; u1k = u1k[np.isfinite(u1k)]; out[f"Lkat{BANT_AD[b]}_t0"] = float(u1k.mean()) if len(u1k) >= AYR["n_min"] else np.nan
    # L dağılımı (tam uzunluk), gün eşit ağırlık, (iii) 200 çekiliş
    Lt = L[gec].astype(float); out.update({"L_ort": float(Lt.mean()), "L_q25": float(np.percentile(Lt, 25)), "L_med": float(np.median(Lt)), "L_q75": float(np.percentile(Lt, 75)),
                                           "L_P1": float((Lt == 1).mean()), "L_E_ters": float((1.0 / Lt).mean())})
    _, gi, gc = np.unique(np.asarray(gun_t0)[gec], return_inverse=True, return_counts=True); w = 1.0 / gc[gi]; out["E1_gun_esit"] = float((fe * w).sum() / w.sum())
    cek = []
    for t in range(AYR["cekilis"]):
        r2 = np.random.default_rng(AYR["cekilis_tohum0"] + t); vals = []
        for j in np.flatnonzero(gec):                                   # (iii) gibi: dizinin tam uzunluğundan tek tip konum; geçersiz güne düşerse olay kaybolur
            q = int(r2.integers(L[j])) + 1; hit = np.flatnonzero(pozlar[j] == q)
            if len(hit) and np.isfinite(u[gunler[j][hit[0]]]):
                vals.append(u[gunler[j][hit[0]]])
        cek.append(np.mean(vals) if vals else np.nan)
    out["iii_cekilis_ort"] = float(np.nanmean(cek)); out["iii_cekilis_sd"] = float(np.nanstd(cek))
    return out


def satir_karari(r: Dict[str, Any], sent_sinif: Optional[str]) -> str:
    """v1.3-AYR P5 (sırayla). sent_sinif: dört Faz 0 spekin çoğunluk sınıfı (>= 3 aynı) ya da 'BELİRSİZ (yapay)'."""
    from .mekanizma import ANLAMSIZ_D
    if r.get("karar_veri") == "VERİ YETERSİZ" or not np.isfinite(r.get("G", np.nan)):
        return "VERİ YETERSİZ"
    if not np.isfinite(r.get("kimlik_fark", np.nan)) or abs(r["kimlik_fark"]) > AYR["kimlik_tol"]:
        return "HESAP HATASI (kimlik)"
    kapsar = lambda a, b: not (a > 0 or b < 0)
    if any(kapsar(r.get(f"G_{k}_alt", np.nan), r.get(f"G_{k}_ust", np.nan)) for k in ("ay", "sembol_yil", "blok60")) or r["G"] < ANLAMSIZ_D:
        return "AYRIŞMA YOK"                                              # ayrışma var = üç küme tanımında da (ay, sembol|yıl, blok60) aralık 0'ı dışlar
    e2_sifir = kapsar(r["E2_ay_alt"], r["E2_ay_ust"]) or abs(r["E2"]) <= AYR["e2_sifir_oran"] * abs(r["E1"])
    if sent_sinif is None or sent_sinif.startswith("BELİRSİZ"):
        return "BELİRSİZ (yapay)"
    if sent_sinif.startswith("VERİ YETERSİZ"):
        return "VERİ YETERSİZ (yapay)"
    if sent_sinif == "MEKANIK_ACIKLAR":
        return ("AĞIRLIK ETKİSİ + " if e2_sifir else "") + "MEKANİK (yapay veri üretiyor)"
    if sent_sinif == "KISMEN_MEKANIK":
        return ("AĞIRLIK ETKİSİ + " if e2_sifir else "") + "KISMEN MEKANİK"
    return "AĞIRLIK ETKİSİ (gerçek veriye özgü, öngörü değil)" if e2_sifir else "AÇIKLANMADI"


def spek_cogunluk(siniflar: List[str]) -> str:
    from .mekanizma import SPEK_UYUM
    s = pd.Series(siniflar).value_counts()
    if len(s) and s.index[0] == "TANIMSIZ" and s.iloc[0] >= SPEK_UYUM:
        return "VERİ YETERSİZ (yapay)"
    return s.index[0] if len(s) and s.iloc[0] >= SPEK_UYUM and s.index[0] != "TANIMSIZ" else "BELİRSİZ (yapay)"


def hucre_karari_ayr(siniflar: List[str]) -> str:
    """Ayrışma hücre kararı: 'AĞIRLIK ETKİSİ + ' öneki atılarak ana sınıfın çoğunluğu (önek ayrı sayılır); eşitlikte BELİRSİZ."""
    ana = pd.Series([str(c).replace("AĞIRLIK ETKİSİ + ", "") for c in siniflar]).value_counts()
    if not len(ana):
        return "TANIMSIZ"
    return ana.index[0] if (len(ana) == 1 or ana.iloc[0] > ana.iloc[1]) else "BELİRSİZ"


# ---------------------------------------------------------------- koşu motoru (gerçek veri: KEŞİF / İÇ; yapay: tek dönem 'KESIF')
_AC: Dict[str, Any] = {}


def hazirla(P: pd.DataFrame, V: Dict[str, pd.DataFrame], O: pd.DataFrame, donemler: Tuple[str, ...]) -> Dict[str, Any]:
    """Değişkenden bağımsız kısım: nitelikli günler, olay maskeleri, diziler (L), kesilme nedenleri, olay kümeleri (dönem × ufuk)."""
    from K55.ortak import OLAY
    from .faz1_yerel import nitelikli_gunler, olay_maskesi
    nit = nitelikli_gunler(P, V); sem = P.sembol.to_numpy(); ii = P.i.to_numpy(); lk = P.likit.to_numpy(); out = {}
    for donem in donemler:
        for u, (h, _) in OLAY.items():
            don_ok = P[f"donem{h}"].to_numpy() == donem; nit_d = nit[u] & don_ok; ol = olay_maskesi(P, O, u, donem); oix = np.flatnonzero(ol)
            L = diziler(sem, ii, oix, nit_d); neden = kesilme_nedeni(sem, ii, oix + L - 1, lk, nit[u], don_ok)
            t0 = P.tarih.to_numpy()[oix]
            ortus = np.zeros(len(oix), bool); zincir = np.arange(len(oix))
            for j in range(1, len(oix)):                                  # önceki olayın dizisi içinde başlayan olay: örtüşen; zincir = birleşik küme (bilgi)
                if sem[oix[j]] == sem[oix[j - 1]] and oix[j] < oix[j - 1] + L[j - 1]:
                    ortus[j] = True; zincir[j] = zincir[j - 1]
            out[(donem, u)] = {"oix": oix, "L": L, "neden": neden, "nit_d": nit_d, "t0": t0, "sembol": sem[oix], "ortusen": ortus,
                               "kume": {"ay": pd.to_datetime(t0).to_period("M").astype(str).to_numpy(), "sembol_yil": np.char.add(np.char.add(sem[oix].astype(str), "|"), pd.to_datetime(t0).year.astype(str).to_numpy()),
                                        "olay": np.arange(len(oix)), "blok60": P.blok60.to_numpy()[oix] if "blok60" in P else pd.to_datetime(t0).to_period("Q").astype(str).to_numpy(),
                                        "zincir": zincir}}
    return out


def _isci(arg) -> List[Dict[str, Any]]:
    from K55.hucre import _z_gun_vd, degisken_hesapla
    from K55.hucreler import HUCRELER
    from K55.ortak import OLAY
    hucre, varyant, satirlar, etiket = arg; C = _AC; P = C["P"]; rows = []; t0 = time.time()
    p_ = varyant.split("|")[1]; p_ = None if p_ == "tek" else int(p_)
    try:
        x, _ = degisken_hesapla(P, C["V"], HUCRELER[hucre], p_, varyant); x = np.asarray(x, float)
    except Exception as ex:
        return [{"etiket": etiket, "hucre": hucre, "varyant": varyant, "ufuk": u, "donem": d, "hata": f"{type(ex).__name__}: {ex}"} for (u, d, _) in satirlar]
    for u, donem, s in satirlar:
        h = OLAY[u][0]; m = P.likit.to_numpy() & np.isfinite(x) & (P[f"donem{h}"].to_numpy() == donem)
        donem_kapisi(donem, P.loc[m, ["tarih", f"bitis{h}"]] if f"bitis{h}" in P else P.loc[m, ["tarih"]], h)
        Dm = P.loc[m, ["tarih", "vd"]].copy(); Dm["_x"] = x[m]; z = _z_gun_vd(Dm, "_x")
        H = C["hazir"][(donem, u)]; mix = np.full(len(P), -1, np.int64); mix[np.flatnonzero(m)] = np.arange(int(m.sum()))
        gunler, pozlar = [], []
        for k, Lj in zip(H["oix"], H["L"]):
            mi = mix[k + np.arange(Lj)]; v = mi >= 0; gunler.append(mi[v]); pozlar.append((np.arange(Lj) + 1)[v])
        r = satir_olc(z, Dm.tarih.to_numpy(), Dm.vd.to_numpy(), gunler, pozlar, H["L"], s, H["kume"], H["t0"], f"{etiket}|{hucre}|{varyant}|{u}|{donem}|ayrisma")
        tum = np.concatenate([g for g in gunler if len(g)]) if any(len(g) for g in gunler) else np.empty(0, np.int64)
        r.update({"ortusen_olay": int(H["ortusen"].sum()), "cift_gun_pay": float(1 - len(np.unique(tum)) / len(tum)) if len(tum) else np.nan})
        r.update({"etiket": etiket, "hucre": hucre, "varyant": varyant, "ufuk": u, "donem": donem, "s": s, "L_tam_ort": float(H["L"].mean()) if len(H["L"]) else np.nan,
                  "L_gecerli_ort": float(np.mean([len(g) for g in gunler if len(g)])) if any(len(g) for g in gunler) else np.nan, "sure_sn": round(time.time() - t0, 1)})
        rows.append(r)
    return rows


def calistir(etiket: str, P: pd.DataFrame, V: Dict[str, pd.DataFrame], O: pd.DataFrame, K: pd.DataFrame, donemler: Tuple[str, ...], isci: int = 3) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """K: 125 KEŞİF satırı (hucre, varyant, ufuk, d). Dönüş: (satır ölçüleri, dizi tablosu: dönem × ufuk × olay). BAĞIMSIZ yasak (v1.3-E)."""
    import multiprocessing as mp
    for d in donemler:
        if d.startswith("BAGIMSIZ"):
            raise ValueError("ayrışma BAĞIMSIZ'da koşulmaz (v1.3-E)")
        donem_kapisi(d)
    H = hazirla(P, V, O, donemler); _AC.clear(); _AC.update({"P": P, "V": V, "hazir": H})
    isler = [(h, v, [(r.ufuk, d, float(np.sign(r.d))) for r in g.itertuples() for d in donemler], etiket) for (h, v), g in K.groupby(["hucre", "varyant"], sort=True)]
    log.info("AYR %s: %d varyant, %d satır × %d dönem, işçi %d", etiket, len(isler), len(K), len(donemler), isci)
    if isci > 1:
        with mp.get_context("fork").Pool(isci) as hv:
            son = hv.map(_isci, isler, chunksize=1)
    else:
        son = [_isci(a) for a in isler]
    S = pd.DataFrame([r for s in son for r in s])
    Dz = pd.concat([pd.DataFrame({"etiket": etiket, "donem": d, "ufuk": u, "sembol": h["sembol"], "t0": h["t0"], "L": h["L"], "kesilme": h["neden"]})
                    for (d, u), h in H.items()], ignore_index=True)
    return S, Dz


# ---------------------------------------------------------------- yapay veri
def sentetik_motor_verisi(tur: str, tohum: int, n: int, gun: int) -> Dict[str, Any]:
    """mekanizma.sentetik_veri + sentetik_panel; motor için bitis{h} ve blok60; D10 bileşenleri (secim_sentetik ile aynı yol)."""
    from K55.faz1 import D10_BILESEN, ek_kur, hucreleri_kur
    from K55.hucre import degisken_hesapla
    from K55.hucreler import HUCRELER
    from K55.ortak import OLAY
    from . import mekanizma as M
    hucreleri_kur(); V, EV, endeks = M.sentetik_veri(n, gun, tohum, tur); P, O = M.sentetik_panel(V, EV, endeks); ek_kur(V, EV, endeks)
    for kb, p in D10_BILESEN:
        if kb in HUCRELER and kb not in P:
            P[kb], _ = degisken_hesapla(P, V, HUCRELER[kb], p, kb)
    for _, (h, _e) in OLAY.items():
        bt = np.full(len(P), np.datetime64("NaT"), dtype="datetime64[ns]")
        for s, g in P.groupby("sembol").groups.items():
            idx = V[s].index.to_numpy(); ii = P.loc[g, "i"].to_numpy(); ok = ii + h < len(idx); v = np.full(len(ii), np.datetime64("NaT"), dtype="datetime64[ns]"); v[ok] = idx[ii[ok] + h]
            bt[np.asarray(g)] = v
        P[f"bitis{h}"] = bt
    O["bitis"] = pd.to_datetime(O.bitis)
    return {"P": P, "V": V, "O": O, "EV": EV, "endeks": endeks}
