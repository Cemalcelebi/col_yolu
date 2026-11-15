"""K60-EK — ASİMETRİ ÖLÇÜTÜ (K60_EK_ON_KAYIT.md; KASA açılmadan önce yazılan ek), tek dosya (11 Kasım 2026; ana oturum iş tanımı).

Ne yapar: KASA'ya giren her (sinyal, uç) çifti için, üç dönemin (KEŞİF, DOĞRULAMA, KASA) HER BİRİNDE 12 ay ufuklu aylık sayımlardan
lift_p100, lift_m50, ASIM = lift_p100 / lift_m50 ve %95 aralıklarını (K60 §5 ile AYNI çekilişler: K60.k60_blok_dizini içe aktarılır), uç /
evren ortalama ve medyan getirisini, R1 net fazlasını bir araya getirir; ek ön kayıttaki üç etiketi ve 'YAKIN' işaretini verir.
YALNIZ K60 çıktı dosyalarını okur (<dönem>_r2_aylik.csv, <dönem>_r2.csv, <dönem>_r1.csv, dogrulama_gecen.json); K60.py DEĞİŞMEZ, eşik /
kural eklenmez. Sağlama: buradaki lift nokta değerleri ve aralıkları <dönem>_r2.csv'dekilerle birebir aynı olmalıdır.
Plasebo sınaması (isteğe bağlı; veri önbelleği yerindeyse): dönem plaseboları K60 fonksiyonlarıyla (aynı tohumlar) yeniden üretilir, <dönem>
plasebo dosyasıyla birebir aynılığı denetlenir ve aynı etiket kuralları uygulanır. Üretilemezse 'plasebo sınaması yok' yazılır.

Komut:  python arastirma_cikti/k60_kutuphane/k60_ek.py [--plasebo evet|hayir] [--cikti KLASOR]
Çıktı:  ek_tablo.csv (çift x dönem), ek_plasebo.csv (plasebo x dönem; üretilebildiyse), K60_EK_RAPOR.md. Ağ kullanılmaz; kişisel bilgi yok.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K60EK = {k: id(v) for k, v in globals().items()}

import json  # noqa: E402
import logging  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

EK_KLASOR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
EK_KOK = os.path.dirname(os.path.dirname(EK_KLASOR))
if EK_KOK not in sys.path:
    sys.path.insert(0, EK_KOK)

import K60  # noqa: E402

eklog = logging.getLogger("col.k60ek")
if not eklog.handlers:
    _ek_h = logging.StreamHandler(sys.stderr)
    _ek_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k60ek: %(message)s", "%H:%M:%S"))
    eklog.addHandler(_ek_h)
    eklog.setLevel(logging.INFO)
    eklog.propagate = False

EK_SURUM = "K60-EK v1.0 (2026-11-11): asimetri ölçütü (ASIM = lift_p100 / lift_m50), üç etiket + YAKIN; yalnız K60 çıktılarından"
# Ek ön kayıttaki sabitler (K60_EK_ON_KAYIT.md 'Tanımlar' ve 'Etiketler'); yeni eşik YOK
EK_KURAL: Dict[str, Any] = {"min_gecerli_cekilis": 400, "guven": [2.5, 97.5],
                            "etiket": {"firsat": "EK-ASİMETRİK FIRSAT", "guvenli": "EK-GÜVENLİ UÇ", "piyango": "EK-PİYANGO UCU (kaçın)", "yakin": "YAKIN"}}
EK_DOSYA = {"tablo": "ek_tablo.csv", "plasebo": "ek_plasebo.csv", "rapor": "K60_EK_RAPOR.md", "onkayit": "K60_EK_ON_KAYIT.md"}
EK_PLASEBO_DOSYA = {"kesif": K60.K60_DOSYA["plasebo"], "dogrulama": "dogrulama_plasebo.csv", "kasa": "kasa_plasebo.csv"}


class EkHata(RuntimeError):
    """K60-EK'e özgü durdurucu hata (çıktı dosyası yok / beklenen sütun yok / KASA açılmamış)."""


def _ek_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or EK_KLASOR, EK_DOSYA.get(ad, ad))


def _ek_oku(ad: str, cikti: Optional[str]) -> pd.DataFrame:
    y = _ek_yol(ad, cikti)
    if not os.path.exists(y):
        raise EkHata(f"K60 çıktısı yok: {y}")
    return pd.read_csv(y)


def ek_asim(kd100: Any, nd: Any, kb100: Any, nb: Any, kdm: Any, kbm: Any) -> Dict[str, float]:
    """Aylık sayımlardan (uçta +%100 olayı, uç hisse, evrende +%100, evren hisse, uçta -%50, evrende -%50) lift_p100, lift_m50, ASIM ve
    %95 aralıkları. Çekilişler K60.k60_blok_dizini (blok 12 ay, 500 çekiliş, tohum 60002). lift aralıkları K60.k60_lift kuralıyla (evren
    oranı > 0 olan çekilişler; en az yarısı geçerli). ASIM: paydası sıfır olan çekiliş atlanır; geçerli çekiliş < 400 ise 'ölçülemez' (NaN)."""
    kd100, nd, kb100, nb, kdm, kbm = (np.asarray(x, float) for x in (kd100, nd, kb100, nb, kdm, kbm)); T = len(nd); g = EK_KURAL["guven"]
    out = {k: np.nan for k in ("lift_p100", "alt_p100", "ust_p100", "lift_m50", "alt_m50", "ust_m50", "asim", "asim_alt", "asim_ust")}
    out["asim_gecerli"] = 0
    if not T or nd.sum() <= 0 or nb.sum() <= 0:
        return out
    ix = K60.k60_blok_dizini(T)
    with np.errstate(invalid="ignore", divide="ignore"):
        cek = {}
        for ad, kd, kb in (("p100", kd100, kb100), ("m50", kdm, kbm)):
            Pb = kb.sum() / nb.sum()
            if Pb > 0:
                out[f"lift_{ad}"] = float((kd.sum() / nd.sum()) / Pb)
            Ld = kd[ix].sum(axis=1) / nd[ix].sum(axis=1); Lb = kb[ix].sum(axis=1) / nb[ix].sum(axis=1)
            L = np.where(Lb > 0, Ld / np.where(Lb > 0, Lb, 1.0), np.nan); cek[ad] = L; s = L[np.isfinite(L)]
            if Pb > 0 and len(s) >= 0.5 * len(L):
                out[f"alt_{ad}"], out[f"ust_{ad}"] = (float(x) for x in np.percentile(s, g))
        if np.isfinite(out["lift_p100"]) and np.isfinite(out["lift_m50"]) and out["lift_m50"] > 0:
            out["asim"] = out["lift_p100"] / out["lift_m50"]
        A = np.where(np.isfinite(cek["p100"]) & np.isfinite(cek["m50"]) & (cek["m50"] > 0), cek["p100"] / np.where(cek["m50"] > 0, cek["m50"], 1.0), np.nan)
    s = A[np.isfinite(A)]; out["asim_gecerli"] = int(len(s))
    if len(s) >= EK_KURAL["min_gecerli_cekilis"]:
        out["asim_alt"], out["asim_ust"] = (float(x) for x in np.percentile(s, g))
    return out


def ek_sartlar(r: Dict[str, Any]) -> Dict[str, bool]:
    """Bir (çift, dönem) satırı için üç etiketin şartları ve 'yalnız aralık şartı kaçtı' (nokta değeri doğru yönde) bayrakları.
    Değeri olmayan (NaN) ölçü şartı SAĞLAMAZ (en dar yorum)."""
    f = lambda k: float(r.get(k, np.nan)) if r.get(k) is not None else np.nan  # noqa: E731
    with np.errstate(invalid="ignore"):
        ort = bool(f("ort") > f("taban_ort")); med = bool(f("medyan") < f("taban_medyan")); r1 = bool(f("r1_fazla") > 0)
        firsat = bool(f("alt_p100") > 1 and f("asim_alt") > 1 and ort)
        guvenli = bool(f("ust_m50") < 1 and r1)
        piyango = bool(f("alt_m50") > 1 and f("asim") < 1 and med)
        return {"firsat": firsat, "guvenli": guvenli, "piyango": piyango,
                "firsat_nokta": bool(not firsat and f("lift_p100") > 1 and f("asim") > 1 and ort),
                "guvenli_nokta": bool(not guvenli and f("lift_m50") < 1 and r1),
                "piyango_nokta": bool(not piyango and f("lift_m50") > 1 and f("asim") < 1 and med)}


def ek_etiket(sart: Dict[str, Dict[str, bool]]) -> List[str]:
    """Üç dönemin şartlarından etiketler: şart üç dönemin HER BİRİNDE -> etiket; iki dönemde şart + üçüncüde yalnız aralık kaçmış
    (nokta doğru yönde) -> 'YAKIN (...)'."""
    Et = EK_KURAL["etiket"]; out = []
    if set(sart) != set(K60.K60_DONEM):
        return out
    for k in ("firsat", "guvenli", "piyango"):
        tam = [d for d in K60.K60_DONEM if sart[d][k]]; nokta = [d for d in K60.K60_DONEM if sart[d][k + "_nokta"]]
        if len(tam) == 3:
            out.append(Et[k])
        elif len(tam) == 2 and len(nokta) == 1:
            out.append(f"{Et['yakin']} ({Et[k]}; aralık {K60.K60_DONEM_AD[nokta[0]]}'de kaçtı)")
    return out


def ek_tablo(cikti: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """KASA'ya giren her çift x üç dönem tablosu + sağlama (lift nokta değeri ve aralıklarının <dönem>_r2.csv ile en büyük mutlak farkı)."""
    yg = _ek_yol("dogrulama_gecen.json", cikti)
    if not os.path.exists(yg) or not os.path.exists(_ek_yol("kasa_r2.csv", cikti)):
        raise EkHata("KASA çıktıları / dogrulama_gecen.json yok: ek yalnız KASA açıldıktan sonra uygulanır")
    with open(yg, encoding="utf-8") as f:
        giren = [(x["sinyal"], x["taraf"], bool(x.get("kesif_secili", True)), "+".join(x.get("kesif_yol", []))) for x in json.load(f)["gecen"]]
    au = K60.K60_ESIK["r2"]["ana_ufuk"]; sat = []; fark = {"lift": 0.0, "aralik": 0.0, "karsilastirilan": 0}
    for d in K60.K60_DONEM:
        A = _ek_oku(f"{d}_r2_aylik.csv", cikti); R2 = _ek_oku(f"{d}_r2.csv", cikti); R1 = _ek_oku(f"{d}_r1.csv", cikti)
        if "ufuk" in A:
            A = A[A.ufuk == au]
        eksik = {"ay_sonu", "n", "n_evren", "k_p100", "k_evren_p100", "k_m50", "k_evren_m50", "sinyal", "taraf"} - set(A.columns)
        if eksik:
            raise EkHata(f"{d}_r2_aylik.csv'de sütun yok: {sorted(eksik)}")
        Ag = {k: v.sort_values("ay_sonu") for k, v in A.groupby(["sinyal", "taraf"], sort=False)}
        i2 = {(r.sinyal, r.taraf): r for r in R2[R2.ufuk == au].itertuples()}; i1 = {(r.sinyal, r.taraf): r for r in R1.itertuples()}
        for s, t, secili, yol in giren:
            a = Ag.get((s, t)); b = i2.get((s, t)); c = i1.get((s, t))
            row: Dict[str, Any] = {"sinyal": s, "taraf": t, "donem": d, "kesif_secili": secili, "kesif_yol": yol, "ay": 0 if a is None else len(a)}
            if a is not None and len(a):
                row.update({"n": int(a.n.sum()), "n_evren": int(a.n_evren.sum()), "P_p100": a.k_p100.sum() / a.n.sum(), "taban_p100": a.k_evren_p100.sum() / a.n_evren.sum(),
                            "P_m50": a.k_m50.sum() / a.n.sum(), "taban_m50": a.k_evren_m50.sum() / a.n_evren.sum(),
                            **ek_asim(a.k_p100, a.n, a.k_evren_p100, a.n_evren, a.k_m50, a.k_evren_m50)})
            if b is not None:
                row.update({k: float(getattr(b, k)) for k in ("ort", "medyan", "taban_ort", "taban_medyan") if pd.notna(getattr(b, k, np.nan))})
                if a is not None and len(a):
                    for k, tur in (("lift_p100", "lift"), ("lift_m50", "lift"), ("alt_p100", "aralik"), ("ust_p100", "aralik"), ("alt_m50", "aralik"), ("ust_m50", "aralik")):
                        x, y = row.get(k, np.nan), float(getattr(b, k, np.nan))
                        if np.isfinite(x) and np.isfinite(y):
                            fark[tur] = max(fark[tur], abs(x - y)); fark["karsilastirilan"] += 1
                        elif np.isfinite(x) != np.isfinite(y):
                            fark[tur] = np.inf
            if c is not None and str(getattr(c, "olculdu", False)).strip().lower() in ("true", "1", "1.0") and pd.notna(getattr(c, "yillik_fazla", np.nan)):
                row.update({"r1_fazla": float(c.yillik_fazla), "r1_t_alfa": float(c.t_alfa)})
            row.update(ek_sartlar(row)); sat.append(row)
    Z = pd.DataFrame(sat)
    et = {}
    for (s, t), g in Z.groupby(["sinyal", "taraf"], sort=False):
        et[(s, t)] = ek_etiket({r["donem"]: {k: bool(r[k]) for k in ("firsat", "guvenli", "piyango", "firsat_nokta", "guvenli_nokta", "piyango_nokta")} for r in g.to_dict("records")})
    Z["etiket"] = ["; ".join(et[(s, t)]) for s, t in zip(Z.sinyal, Z.taraf)]
    return Z, fark


def ek_plasebo(cikti: Optional[str] = None) -> Tuple[Optional[pd.DataFrame], str]:
    """Plasebo sınaması: her dönemin 200 plasebosu K60 fonksiyonlarıyla (aynı tohum, aynı ÜST uç, aynı aylar) yeniden üretilir; +%100 ve -%50
    lift'leri <dönem> plasebo dosyasıyla birebir karşılaştırılır; aynı etiket şartları uygulanır. Döner (tablo | None, açıklama)."""
    try:
        E = K60.K60_ESIK; D = K60.k60_demet_yukle(); P = K60.k60_panel(D, E, True); U = P["U"]; au = E["r2"]["ana_ufuk"]; sat = []; enb = 0.0
        for d in K60.K60_DONEM:
            Pl = _ek_oku(EK_PLASEBO_DOSYA[d], cikti); pm = K60.k60_donem_aylari(P, d, 1, E)
            for i in range(E["coklu"]["plasebo_n"]):
                S = np.random.default_rng(E["coklu"]["plasebo_tohum"] + i).random(U.shape); S[~U] = np.nan
                sec = K60.K58.k58_ust_dilim(S, U, E["portfoy"]["dilim"]); rr, A = K60.k60_r2(P, sec, pm, E, [au]); r = rr[0]
                p = Pl[Pl.plasebo == i].iloc[0]
                enb = max(enb, abs(r["lift_p100"] - float(p.r2_lift_p100)), abs(r["lift_m50"] - float(p.r2_lift_m50)), abs(r["alt_p100"] - float(p.r2_alt_p100)))
                row = {"plasebo": i, "donem": d, "ort": r["ort"], "medyan": r["medyan"], "taban_ort": r["taban_ort"], "taban_medyan": r["taban_medyan"],
                       "r1_fazla": float(p.yillik_fazla), **ek_asim(A.k_p100, A.n, A.k_evren_p100, A.n_evren, A.k_m50, A.k_evren_m50)}
                row.update(ek_sartlar(row)); sat.append(row)
            eklog.info("plasebo %s: %d yeniden üretildi (dosyayla en büyük fark %.2e)", d, E["coklu"]["plasebo_n"], enb)
        if enb > 1e-9:
            return None, f"plasebo sınaması yok: yeniden üretilen plasebolar dosyadakilerle aynı değil (en büyük fark {enb:.3g})"
        return pd.DataFrame(sat), f"plasebolar K60 fonksiyonlarıyla yeniden üretildi; lift ve alt sınırları plasebo dosyalarıyla aynı (en büyük fark {enb:.1e})"
    except Exception as ex:     # veri önbelleği yok / K60 çağrısı başarısız: ek ön kayıt gereği 'plasebo sınaması yok'
        eklog.warning("plasebo yeniden üretilemedi: %s %s", type(ex).__name__, str(ex)[:200])
        return None, f"plasebo sınaması yok ({type(ex).__name__}: {str(ex)[:160]})"


def _yuz(x: Any, n: int = 1) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return ("%" + f"{100 * v:.{n}f}".replace(".", ",")) if np.isfinite(v) else "—"


def _say(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return f"{v:.{n}f}".replace(".", ",") if np.isfinite(v) else "—"


def _ara(r: Any, ad: str, alt: str, ust: str) -> str:
    return f"{_say(r.get(ad))} [{_say(r.get(alt))}; {_say(r.get(ust))}]"


def ek_rapor(Z: pd.DataFrame, fark: Dict[str, Any], Pz: Optional[pd.DataFrame], pl_not: str, cikti: Optional[str] = None) -> str:
    Et = EK_KURAL["etiket"]; cift = Z.drop_duplicates(["sinyal", "taraf"]); n_cift = len(cift)
    say = {k: int(cift.etiket.str.split("; ").apply(lambda L: Et[k] in L).sum()) for k in ("firsat", "guvenli", "piyango")}
    yakin = cift[cift.etiket.str.contains(Et["yakin"], regex=False)]
    bas = ("| çift | dönem | ay | hisse-ay | P(+%100) uç / evren | lift [%95] | P(-%50) uç / evren | lift [%95] | ASIM [%95] | ort. 12 ay uç / evren | medyan uç / evren | R1 net fazla | şart F / G / P |\n"
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")

    def blok(secim: pd.DataFrame) -> str:
        out = []
        for s, t in zip(secim.sinyal, secim.taraf):
            for r in Z[(Z.sinyal == s) & (Z.taraf == t)].to_dict("records"):
                out.append(f"| {s} ({'ÜST' if t == 'UST' else 'ALT'}) | {K60.K60_DONEM_AD[r['donem']]} | {r['ay']} | {_say(r.get('n'), 0)} | {_yuz(r.get('P_p100'))} / {_yuz(r.get('taban_p100'))} | "
                           f"{_ara(r, 'lift_p100', 'alt_p100', 'ust_p100')} | {_yuz(r.get('P_m50'))} / {_yuz(r.get('taban_m50'))} | {_ara(r, 'lift_m50', 'alt_m50', 'ust_m50')} | "
                           f"{_ara(r, 'asim', 'asim_alt', 'asim_ust')} | {_yuz(r.get('ort'))} / {_yuz(r.get('taban_ort'))} | {_yuz(r.get('medyan'))} / {_yuz(r.get('taban_medyan'))} | "
                           f"{_yuz(r.get('r1_fazla'))} | {'E' if r['firsat'] else 'h'} / {'E' if r['guvenli'] else 'h'} / {'E' if r['piyango'] else 'h'} |")
        return bas + ("\n".join(out) if out else "| (çift yok) |" + " |" * 12)
    par = [f"# K60-EK — asimetri ölçütü: RAPOR\n\n{EK_SURUM}. Kaynak: K60_EK_ON_KAYIT.md (KASA'dan önce yazıldı). Yalnız K60 çıktı dosyalarından üretildi; K60.py değişmedi.\n",
           f"## Sonuç\n- KASA'ya giren {n_cift} çiftten '{Et['firsat']}' alan {say['firsat']}, '{Et['guvenli']}' alan {say['guvenli']}, '{Et['piyango']}' alan {say['piyango']}; "
           f"'{Et['yakin']}' {len(yakin)} çift.\n- Hiçbir etiket İZ değildir (yalnız ABD, yalnız yaşayanlar; KEŞİF ve DOĞRULAMA bu etiketler için örneklem içi, bağımsız sınama yalnız KASA: "
           f"12 ay ufukta {int(Z[Z.donem == 'kasa'].ay.max())} oluşum ayı).\n",
           f"## Sağlama\nlift_p100 ve lift_m50 nokta değerleri ile %95 aralıkları <dönem>_r2.csv ile karşılaştırıldı ({fark['karsilastirilan']} değer): en büyük mutlak fark nokta "
           f"{fark['lift']:.2e}, aralık {fark['aralik']:.2e} ({'BİREBİR AYNI' if max(fark['lift'], fark['aralik']) < 1e-9 else 'FARK VAR'}).\n"]
    for k, baslik in (("firsat", f"## '{Et['firsat']}' (üç dönemin her birinde: +%100 lift alt sınırı > 1, ASIM alt sınırı > 1, uç ortalaması > evren ortalaması)"),
                      ("guvenli", f"## '{Et['guvenli']}' (üç dönemin her birinde: -%50 lift üst sınırı < 1, R1 net yıllık fazla > 0)"),
                      ("piyango", f"## '{Et['piyango']}' (üç dönemin her birinde: -%50 lift alt sınırı > 1, ASIM < 1, uç medyanı < evren medyanı)")):
        par.append(baslik + "\n" + blok(cift[cift.etiket.str.split("; ").apply(lambda L: Et[k] in L)]) + "\n")
    par.append(f"## '{Et['yakin']}' (iki dönemde şart tam, üçüncüde yalnız aralık şartı kaçmış; nokta değeri doğru yönde)\n"
               + ("\n".join(f"- {s} ({'ÜST' if t == 'UST' else 'ALT'}): {e}" for s, t, e in zip(yakin.sinyal, yakin.taraf, yakin.etiket)) or "- yok") + "\n\n" + blok(yakin) + "\n")
    par.append("## Yanlış keşif sınaması (plasebo)\n" + pl_not + ".")
    if Pz is not None:
        sat = []
        for d in K60.K60_DONEM:
            g = Pz[Pz.donem == d]
            sat.append(f"| {K60.K60_DONEM_AD[d]} | {len(g)} | {_yuz(g.firsat.mean())} | {_yuz(g.guvenli.mean())} | {_yuz(g.piyango.mean())} | {_say(g.asim.median())} | {_say(g.asim.quantile(0.05))} - {_say(g.asim.quantile(0.95))} |")
        uc = Pz.groupby("plasebo")[["firsat", "guvenli", "piyango"]].all()
        par.append("Tek dönemde şartı (o dönemin şartlarının hepsini) sağlayan plasebo oranı:\n\n| dönem | plasebo | FIRSAT | GÜVENLİ UÇ | PİYANGO UCU | ASIM medyan | ASIM %5 - %95 |\n|---|---|---|---|---|---|---|\n"
                   + "\n".join(sat) + f"\n\nAynı plasebo sinyalinin (aynı tohum) ÜÇ dönemin üçünde de şartı sağlama oranı: FIRSAT {_yuz(uc.firsat.mean())}, GÜVENLİ UÇ {_yuz(uc.guvenli.mean())}, "
                   f"PİYANGO UCU {_yuz(uc.piyango.mean())} ({len(uc)} plasebo).\n")
    par.append("\n## BOŞLUK (ek ön kayıtta açık kalan yerler; en dar yorum uygulandı)\n"
               "BOŞLUK 1. Bir ölçü hesaplanamıyorsa (R1 o dönemde ölçülemedi; ASIM'in geçerli çekilişi < 400; uçta hiç -%50 olayı yok ve ASIM tanımsız) şart SAĞLANMADI sayıldı.\n"
               "BOŞLUK 2. 'YAKIN': iki dönemde bütün şartlar tam; üçüncü dönemde aralık dışı şartlar (ortalama / medyan / R1 fazla) tam VE aralık şartlarının nokta karşılıkları doğru yönde "
               "(FIRSAT: lift_p100 > 1 ve ASIM > 1; GÜVENLİ: lift_m50 < 1; PİYANGO: lift_m50 > 1), ama aralık şartlarından en az biri kaçmış.\n"
               "BOŞLUK 3. KASA'ya giren ama KEŞİF'te seçilmemiş bileşik uçları (AİLE BİLGİSİ) da etiket alabilir (ek 'KASA'ya giren çift' diyor); tabloda kesif_secili sütunu bunu gösterir.\n"
               "BOŞLUK 4. ASIM aralığında evren oranı sıfır olan çekilişler de atlandı (lift tanımsız).\n"
               "BOŞLUK 5. Plasebo için R1 net fazla, plasebo dosyasındaki yillik_fazla sütunundan alındı (plasebo R1'i yeniden hesaplanmadı).\n"
               "\n## Sınırlar\nEk, KEŞİF ve DOĞRULAMA görüldükten sonra yazıldı; KASA 12 ay ufukta kısa ve pencereleri örtüşüyor: aralıklar dar çıkar (plasebo oranlarına bakınız). "
               "Yalnız yaşayanlar: -%50 olasılığı alt sınırdır.\n")
    metin = "\n".join(par); yol = _ek_yol("rapor", cikti)
    if K60._K60_EPOSTA.search(metin):
        raise EkHata("rapor metninde e-posta biçimli parça var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def ek_kos(cikti: Optional[str] = None, plasebo: bool = True) -> Dict[str, Any]:
    """Eki uygular: ek_tablo.csv, (üretilebilirse) ek_plasebo.csv ve K60_EK_RAPOR.md yazar."""
    if not os.path.exists(_ek_yol("onkayit", cikti)):
        raise EkHata(f"ek ön kayıt yok: {_ek_yol('onkayit', cikti)}")
    Z, fark = ek_tablo(cikti)
    Z.to_csv(_ek_yol("tablo", cikti), index=False)
    eklog.info("tablo: %d çift x %d dönem; r2.csv ile en büyük fark nokta %.2e, aralık %.2e", Z.drop_duplicates(["sinyal", "taraf"]).shape[0], Z.donem.nunique(), fark["lift"], fark["aralik"])
    Pz, pl_not = ek_plasebo(cikti) if plasebo else (None, "plasebo sınaması yok (--plasebo hayir)")
    if Pz is not None:
        Pz.to_csv(_ek_yol("plasebo", cikti), index=False)
    yol = ek_rapor(Z, fark, Pz, pl_not, cikti)
    eklog.info("rapor: %s", yol)
    return {"tablo": Z, "fark": fark, "plasebo": Pz, "plasebo_not": pl_not, "rapor": yol}


def _cakisma_kontrol_k60ek(_once=_CK_ONCE_K60EK, _dosya="k60_ek.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K60EK", "_CK_KAYIT", "_cakisma_kontrol_k60ek", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "annotations", "Any", "Dict", "List", "Optional", "Tuple", "K60")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k60ek()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=EK_SURUM)
    ap.add_argument("--plasebo", choices=["evet", "hayir"], default="evet")
    ap.add_argument("--cikti", default=None)
    a = ap.parse_args()
    try:
        R_ = ek_kos(a.cikti, a.plasebo == "evet")
        print(R_["rapor"]); print("sağlama:", R_["fark"]); print(R_["plasebo_not"])
    except (EkHata, K60.K60Hata, FileNotFoundError) as ex:
        eklog.error("%s", ex); sys.exit(1)
