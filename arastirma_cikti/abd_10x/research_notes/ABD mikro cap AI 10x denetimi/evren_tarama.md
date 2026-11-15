# ABD mikro/küçük cap AI veri merkezi altyapısı — evren taraması (4 Kasım 2026)

Kapsam: ABD borsalarında (Nasdaq / NYSE / NYSE American; OTC yalnız not olarak) piyasa değeri ~30–300 M$ olan AI veri merkezi altyapısı, GPU bulut / neocloud, hesaplama için güç ve yan sağlayıcılar (soğutma, şalt, modüler DC, fiber). Amaç: önceki kısa liste (QMLS, DGXX, AIB, VVPR→VIVO) ile kıyaslanacak daha iyi/kötü alternatifler bulmak; SLNH, MIGI, NUAI'yi yeniden kontrol etmek; büyük isimlerin bant dışı olduğunu belgelemek.

Veri kaynakları ve tarih kuralı: Bütün piyasa değeri / EV / nakit / borç / hisse adedi değişimi rakamları aksi belirtilmedikçe StockAnalysis.com "statistics" sayfalarından, 3 Kasım 2026 kapanışı (sayfa 4 Kasım 2026 güncel). Nakit ve borç StockAnalysis'te son bilanço (çoğunlukla 30 Haziran 2026 10-Q) rakamıdır; sonraki olaylar (borç geri ödemesi, PIPE) ayrıca not edildi. Fiyat performansı: StockAnalysis "history" tablosundan 3 Kas 2026 kapanışı ile 5 Eki 2026 (~30 gün), 4 Eyl 2026 (~60 gün) ve 25 Ağu 2026 (~70 gün; tablo 25 Ağustos'ta başladığı için 90 gün yerine kullanıldı) kapanışları. Hesaplanan yüzdeler benim hesabımdır (çıkarım).

Kısa Türkçe özet (ayrıntı aşağıda İngilizce):
- Bant içinde (30–300 M$) ve GERÇEK sözleşmesi olanlar: DGXX (Cerebras 40 MW, 10 yıl, ~1,1 Mr$), HOST (43 MW, 15 yıl take-or-pay, ~1,25 Mr$), AIB (Nebius 50 MW, 12 yıl), DUOT (20 MW 10 yıl >400 M$ + 10 MW 5 yıl 111 M$), QMLS (523 M$ birikmiş GPU sözleşmesi), SLNG (200 M$ 2 yıllık LNG güç sözleşmesi, 2027). Hiçbiri "enerjilendirilmiş + sözleşmeli + finansmanı kapanmış" üçlüsünü bugün tam sağlamıyor; en yakını DGXX (Aralık 2026 hedef, 200 M$ borç taahhüt mektubu henüz kapanmadı).
- Seyreltme >%50 (12 ay) → elenenler: SLNH (+%846), GPUS (+%7.263), NUAI (+%239 + 29 Ekim 64 M$ PIPE), VIVO (+%372), AGPU (+%412), DUOT (+%160, ama nakit zengin), AIB (+%102, halka arz kaynaklı), DGXX (+%92, ATM). Sınırda: QMLS (+%49).
- Going-concern bayrağı: VIP (ex-GREE) Q1 2026'da açık göstermiş; HOST için çelişkili kaynaklar; GPUS/VIVO/BGDE/DRK bilanço olarak zayıf.
- Son 90 günde >%100 koşan YOK. Tersine, tüm grup Ekim 2026'da sert düştü (çoğu 26 Ekim–2 Kasım'da dip yaptı).
- Büyük isimler bant dışı: KEEL (ex-BITF) 1,35 Mr$, IREN 9,6 Mr$, CIFR 3,4 Mr$, HUT 7,9 Mr$, APLD 5,4 Mr$, CORZ 4,6 Mr$, BTDR 1,9 Mr$, NBIS 41,6 Mr$, ABTC 481 M$, IOND ~2,4–3,4 Mr$, SIFY 926 M$, ERII 366 M$. Bant içinde kalanlar: TSSI 198 M$, DUOT 194 M$.
- Bant altı/ölü: BGDE (ex-MIGI) 17,8 M$, DRK (ex-ANY) 19,6 M$, PWCM (ex-LMFA) 1,0 M$, POLA 2,2 M$, BEEM 18 M$, NVVE 0,75 M$ (OTC), SGRX (ex-BTOG) 0,6 M$, SOBR 0,23 M$.

---

## KQ0. Screened candidate list (per-name fact sheets)

### Takeaway
Fourteen names were screened in depth; six carry a binding, named-or-counterparty-described contract (DGXX, HOST, AIB, DUOT, QMLS, SLNG). The entire micro-cap AI-infra group fell 15–60% between early September and 3 November 2026, so nothing in the set is "already run"; the risks are financing, dilution and delivery timing, not price momentum.

### Cited Findings

**1. Digi Power X (Nasdaq: DGXX) — power + AI data center developer (Alabama, NY, NC)**
- Market cap $231.68M; EV $103.55M; cash $128.12M; debt n/a (none); shares 102.06M, +92.48% YoY; 52-week −62.35% (3 Nov 2026 close) — [StockAnalysis DGXX statistics](https://stockanalysis.com/stocks/dgxx/statistics/)
- 10-Q cover: 101,393,355 subordinate voting shares as of 14 Aug 2026; cash $128,121,977 at 30 Jun 2026; no loans/borrowings; Q2 2026 revenue $6,628,607 (vs $8,111,451 a year earlier); ATM issued 27,950,000 shares in H1 2026 for $163.2M gross; 2.85M more shares after quarter-end for $11.26M — [SEC 10-Q Q2 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- Cerebras contract (signed 4 May 2026): 10-year colocation/MSA, Tier III facility in Columbiana AL, up to 40 MW IT load; Phase 1 15 MW, conditional Phase 2 25 MW; $195.00/kW/month take-or-pay ≈ $2.925M/month Phase 1 and $4.875M/month Phase 2, 3.0% annual escalator; facility under construction and not ready for use at 30 Jun 2026 — [SEC 10-Q Q2 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- TCV ≈ $1.1B initial term, potential $2.5B with one seven-year extension; Phase 2 conditioned on financing; company owns the land, built its own substation for Phase 1; grid connection finalized, Alabama Power supply agreement in place; operational readiness target 15 Dec 2026, full commissioning end Q1 2027 — [DCD: Cerebras signs for 40MW](https://www.datacenterdynamics.com/en/news/cerebras-signs-on-for-40mw-of-capacity-at-digi-power-x-data-center-in-alabama/); [Rallies summary](https://rallies.ai/news/digi-power-x-lands-11b-10-year-ai-colocation-deal-for-40-mw-alabama-center)
- 13 Oct 2026: commitment letter for US$200M debt financing from an unnamed "major lending institution", syndicated by Goldman Sachs, expected to close within 90 days subject to documentation and diligence; SPV-level structure with unsecured company guarantee through completion; company held ~US$135M cash and had invested ~US$153M capex YTD 2026; Phase 1 expected December 2026, Phase 2 March 2027 — [Finviz / press release](https://finviz.com/news/401609/digi-power-x-announces-200-million-debt-financing-commitment-to-support-completion-of-alabama-ai-data-center-and-provides-expansion-update); [DCD](https://datacenterdynamics.com/en/news/digi-power-x-secures-200m-in-debt-financing-for-alabama-data-center-project)
- Next earnings 13 Nov 2026; Jones initiated Buy $8 PT (~early Oct); registration statement filed 11 Sep 2026; analyst consensus $8.50 — [StockAnalysis DGXX](https://stockanalysis.com/stocks/dgxx/)
- Price: $2.27 (3 Nov) / $3.73 (5 Oct) / $3.75 (4 Sep) / $4.05 (25 Aug); low $2.13 on 2 Nov 2026 — [StockAnalysis DGXX history](https://stockanalysis.com/stocks/dgxx/history/)
- Earlier: ~400 MW secured power across sites claimed in a promotional piece — [Barchart](https://www.barchart.com/story/news/2157675/mojo-smallcap-watch-dgxx-plug-mnts-ndra-poet-driving-ai-glp-1-and-energy-trends) (promotional, not verified)

**2. Host Digital (NYSE American: HOST; ex-Healthy Choice Wellness HCWC) — Oklahoma AI data center developer, listed 18 Sep 2026**
- Market cap $73.04M on 28.20M shares; EV, cash, debt, revenue all n/a on the data page; price $2.59 (3 Nov) — [StockAnalysis HOST statistics](https://stockanalysis.com/stocks/host/statistics/)
- Lease (signed 7 Aug 2026): 15-year take-or-pay, 43 MW critical IT load at Host Digital's northeast Oklahoma site, with "a large cloud infrastructure company", expected backstop by an investment-grade technology company; base-term rent ≈ $1.25B incl. 3% escalators; up to ~$3.2B over 30 years if all renewals exercised; delivery expected H1 2027 — [SEC 8-K Ex.99.1](https://www.sec.gov/Archives/edgar/data/0001948864/000149315226043135/ex99-1.htm); [Zacks](https://www.zacks.com/stock/news/2988418/hcwc-nears-host-digital-merger-as-125b-ai-lease-adds-momentum)
- Merger closed 17 Sep 2026 (reverse acquisition; former Host members ~96.4%); trading as HOST from 18 Sep — [Panabee](https://www.panabee.com/news/healthy-choice-wellness-completes-reverse-merger-with-host-digital-rebrands-to-host)
- Offering (424B5): 2,187,500 Class A shares at $8.00 = $17.5M gross, ~$15.0M net; Cantor lead; shares 26,012,821 before → 28,200,321 after; 19,888,093 shares under pre-funded warrants issued in the merger are excluded from the count; prospectus says cash + proceeds sufficient for 12 months (no going-concern language); Site I described as 43 MW critical IT under 15-year take-or-pay, delivery Q1 2027; no capex figure — [SEC 424B5](https://www.sec.gov/Archives/edgar/data/0001948864/000149315226043454/form424b5.htm)
- Debut release (22 Sep 2026): outstanding shares after offering 48,088,414 (i.e., incl. pre-funded warrants), implied market cap $384.9M at 21 Sep close; sponsor pipeline four more sites >450 MW gross; Site II (NE Oklahoma, ~20 MW gross / 16 MW critical IT) has a 12-year take-or-pay lease signed by the sponsor with a publicly traded AI cloud provider, ~$391M base rent, year-1 $28.3M, 2.5% escalator, described as "energized and leased"; HOST has only begun negotiations to acquire it, no definitive agreement — [Finviz / GlobeNewswire](https://finviz.com/news/394186/host-digital-debuts-on-nyse-american-as-host-and-exercises-its-right-to-acquire-a-second-site-from-its-sponsor-for-its-ai-data-center-platform)
- S-3 resale: 45,385,000 Class A shares registered for selling stockholders (Graham Macro Strategic 19.79M, BDS Infrastructure 10.12M, 10X Master 10.12M, Graham Credit Opps 2.70M, Biscayne 2.25M, others); 26,355,685 Class A outstanding as of 1 Oct 2026; last price $2.50 on 15 Oct 2026; no going-concern language in S-3 — [SEC S-3](https://www.sec.gov/Archives/edgar/data/0001948864/000149315226047468/forms-3.htm)
- $15M buyback authorized 19 Oct 2026 (to 19 Oct 2027) — [Finviz](https://finviz.com/news/404549/host-digital-authorizes-15-million-share-buyback-program); a third-party summary states the company "remains development-stage and has going-concern doubt absent project financing and capital raises" — [roic.ai HOST](https://www.roic.ai/quote/HOST) (secondary; conflicts with 424B5 language)
- Next earnings 17 Nov 2026 — [StockAnalysis HOST](https://stockanalysis.com/stocks/host/)
- Price: $2.59 (3 Nov) / $3.09 (5 Oct) / $8.00 (21 Sep, first full day in table) / high $8.06 (22 Sep) / low $1.90 (16 Oct) — [StockAnalysis HOST history](https://stockanalysis.com/stocks/host/history/)

**3. AIB Data Centers (NYSE American: AIB; ex-BlockchAIn Digital Infrastructure) — Southeast/Texas AI DC developer**
- Market cap $66.11M; EV $13.35M; cash $52.78M; debt ~$27K; shares 75.98M, +101.83% YoY; 52-week −94.51% — [StockAnalysis AIB statistics](https://stockanalysis.com/stocks/aib/statistics/)
- 30 Sep 2026: binding 12-year agreement with Nebius for 50 MW critical IT capacity at CLT1 with two five-year renewal options; backed by a 15-year Electric Service Agreement for 65 MW utility load at the site — [SEC 8-K Ex.99.1](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105865/ea030737801ex99-1.htm); [Capital.com](https://capital.com/en-eu/news/aib-data-centers-signs-contract-with-nebius-for-ai-data)
- 14 Sep 2026: acquisition of two Texas parcels (~29.4 acres) raised contracted utility power from 65 MW to ~120 MW; 15 MW energized at closing plus 40 MW under a facilities extension agreement — [Finviz](https://finviz.com/news/391604/aib-data-centers-nearly-doubles-contracted-power-capacity-to-120-mw-through-strategic-acquisition)
- CEO letter (7 Oct 2026): CLT1 funding = customer prepayments ("meaningful portion of initial development") + project-level debt and preferred equity; "does not currently anticipate requiring corporate-level common equity"; no capex figure, no timeline in letter — [SEC 8-K Ex.99.1 CEO letter](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026107421/ea030792301ex99-1.htm)
- Investor update (~22 Oct 2026): first data hall at CLT1 targeted August 2027; Oct deck: energized capacity excludes the 50 MW contracted at CLT1 (expected energized 2027); legacy operations de-energized 5 Jun 2026; ~570 MW identified pipeline, most sites without definitive agreements — [StockAnalysis AIB news](https://stockanalysis.com/stocks/aib/); [SEC 8-K Ex.99.1 (Oct)](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105249/ea030723301ex99-1.htm)
- IPO $63M; added to Russell Microcap — [Barchart](https://www.barchart.com/story/news/3691572/aib-data-centers-to-present-recent-financial-power-and-ai-infrastructure-milestones-at-the-emerging-growth-conference)
- TTM revenue $17.10M (−12.8%); Freedom Capital Buy $2.50 (Oct); next earnings ~13 Nov 2026 — [StockAnalysis AIB](https://stockanalysis.com/stocks/aib/)
- Price: $0.87 (3 Nov) / $1.62 (5 Oct) / $1.28 (4 Sep) / $1.30 (25 Aug); high $1.71 (29 Sep), low $0.83 (26 Oct) — [StockAnalysis AIB history](https://stockanalysis.com/stocks/aib/history/)

**4. QumulusAI (Nasdaq: QMLS) — GPU neocloud (Atlanta), direct listing 16 Jul 2026**
- Market cap $118.44M; EV $229.29M; cash $19.97M; total debt $130.81M; shares 33.46M, +49.01% YoY; price $3.54 (3 Nov), 52-week range $3.10–$38.00 — [StockAnalysis QMLS statistics](https://stockanalysis.com/stocks/qmls/statistics/); [StockAnalysis QMLS](https://stockanalysis.com/stocks/qmls/)
- Q2 2026: revenue $6.7M (+118% YoY), compute power revenue $5.6M (84%); net loss $22.8M incl. $19.2M non-cash loss on convertible note issuance; 21 new direct contracts with aggregate expected take-or-pay value $169.7M; deployed GPU fleet 952 → 3,088; 8 MW of HPC capacity under executed lease; Atlanta colocation up to 3.75 MW with ROFO on 7 MW; Blackwell contracts generating $18–20M annualized revenue per MW; operating cash flow $22.3M H1 helped by $30.5M deferred revenue; 31,727,001 shares at 30 Jun 2026 — [QumulusAI Q2 2026 press release PDF](https://s21.q4cdn.com/597044239/files/doc_financials/2026/q2/QumulusAI_Q2_2026_Earnings_Press_Release_LETTERHEAD.pdf)
- 29 Sep 2026: $240.9M in two three-year agreements (>2,000 B300 GPUs; $211.9M + $29.1M) with "AI inference platform providers" (unnamed); potential $401.6M with extension options — [QumulusAI PR PDF](https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Signs-240-9-Million-in-New-AI-Inference-Customer-Contracts-for-NVIDIA-Blackwell-B300-Capacity-2026.pdf)
- 15 Oct 2026: cumulative signed contract value $523.4M; ~$209M ARR on initial terms once deployed — [QumulusAI PR PDF](https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Puts-71-9-Million-Blackwell-Agreement-into-Production-Signed-Customer-Contracts-Surpass-500-Million-2026.pdf)
- Financing: TFC equipment lease expanded to ~$123.6M (22 Oct 2026); $500M USD.AI facility described as non-recourse by one source and non-binding by another (unreconciled); ATW Partners $90M convertible facility (two $45M tranches) — [citybiz](https://www.citybiz.co/?p=923238); [Newswire USD.AI](https://www.newswire.com/news/qumulusai-deploys-1-144-nvidia-blackwell-gpus-through-drawdown-under-500m-usd); [Newswire ATW](https://www.newswire.com/news/atw-partners-backs-qumulusai-with-second-45-million-facility-lifting-total)
- 3 Nov 2026: contracted 0.5 MW in Columbia SC; B. Riley Buy $11 (21 Oct), Compass Point Buy $9 (17 Oct); next earnings ~25 Nov 2026; TTM net income −$176.21M — [StockAnalysis QMLS](https://stockanalysis.com/stocks/qmls/)
- Price: $3.54 (3 Nov) / $6.16 (5 Oct) / $5.90 (4 Sep); high $8.10 (21 Sep), low $3.14 (26 Oct) — [StockAnalysis QMLS history](https://stockanalysis.com/stocks/qmls/history/)

**5. Duos Technologies (Nasdaq: DUOT) — edge AI data center colocation (Duos Edge AI)**
- Market cap $193.87M; EV $82.52M; cash $112.31M; debt $0.95M; shares 31.47M, +159.56% YoY; 52-week −40.48% — [StockAnalysis DUOT statistics](https://stockanalysis.com/stocks/duot/statistics/)
- 20 Oct 2026: 10-year colocation agreement, 20 MW facility load, with "a publicly traded U.S. cloud services provider", >$400M TCV, deployment expected Q2 2027; ~100 MW additional powered DC-zoned land (≈25 MW under contract, 75 MW in negotiation) — [SEC 8-K Ex.99.2](https://www.sec.gov/Archives/edgar/data/1396536/000107997326000262/ex99x2.htm); [DCD](https://datacenterdynamics.com/en/news/duos-secures-cloud-provider-as-customer-for-20mw-of-data-center-capacity)
- July 2026: five-year 10 MW colocation with an investment-grade hyperscaler, >$111M contracted revenue, Columbus GA campus to 20 MW by Q4 2026 — [Finviz](https://finviz.com/news/369071/duos-edge-ai-signs-five-year-10-mw-colocation-agreement-with-investment-grade-hyperscaler-valued-at-111-million-in-contracted-revenue)
- 5 Oct 2026: sold GPU-as-a-Service entity to Axe Compute, removing ~$98.1M prospective equipment financing; Cantor PT $24 (Overweight), Chardan Neutral $9.50, Titan Buy $24; next earnings ~16 Nov 2026 — [StockAnalysis DUOT](https://stockanalysis.com/stocks/duot/)
- Price: $6.16 (3 Nov) / $9.19 (5 Oct) / $8.76 (4 Sep) / $10.22 (25 Aug); low $5.40 (16 Oct) — [StockAnalysis DUOT history](https://stockanalysis.com/stocks/duot/history/)

**6. Soluna Holdings (Nasdaq: SLNH) — renewable-powered compute campuses (Texas, Kentucky)**
- Market cap $138.90M; EV $64.83M; cash $113.36M; debt $39.30M; shares 244.59M, +845.86% YoY; 52-week −83.73% — [StockAnalysis SLNH statistics](https://stockanalysis.com/stocks/slnh/statistics/)
- 10-Q: 244,590,575 shares at 10 Aug 2026 (225,821,479 at 30 Jun); cash $113.4M + restricted $17.9M; debt carrying $33.1M ($30.1M current due to Generate covenant); Q2 2026 revenue $15.06M (hosting $12.65M, mining $1.72M, wind $0.37M, demand response $0.32M, HPC $0); ATM: 74,174,213 shares sold H1 2026 for $113.5M net, plus 18,769,096 shares after quarter-end for ~$23.6M; HPE GPU agreement terminated March 2025; Kati 2 (Willacy County TX) is first large-scale HPC development with lease negotiations begun with a prospective tenant, no assurance — [SEC 10-Q Q2 2026](https://www.sec.gov/Archives/edgar/data/0000064463/000162828026056702/slnh-20260630.htm); [theenergymag summary](https://www.theenergymag.com/news/market-news/soluna-holdings-reports-q2-2026-financial-results-and-debt-prepayment-agreement)
- 26 Oct 2026: full repayment of Generate Capital facility ($28.7M principal at 30 Jun; $19.1M paid Aug, remainder Oct); total debt principal cut from $37.9M to ~$9.2M; liens released — [Panabee](https://www.panabee.com/news/soluna-repays-29-million-generate-capital-debt-reducing-total-principal-by-76); [miningstockeducation](https://www.miningstockeducation.com/2026/10/soluna-completes-full-repayment-of-generate-capital-debt/)
- 21 Oct 2026: definitive agreement (not closed) with Applied Digital for a JV (APLD 51% / SLNH 49%) to build 50 MW critical IT at Dorothy 3 (Briscoe County TX, beside 150 MW Briscoe Wind; grid + wind power); ChronoScale Holdings (Nasdaq: CHRN) signed a non-binding LOI to lease — [DCD](https://datacenterdynamics.com/en/news/soluna-and-applied-digital-to-build-50mw-data-center-in-texas); [Finviz/BusinessWire](https://finviz.com/news/405148/soluna-agrees-to-form-strategic-partnership-with-applied-digital-to-develop-wind-powered-ai-data-center-in-texas)
- Sept 2026: Kati 1 completed, conditional ERCOT Batch Zero base-load position for all 166 MW; Dorothy 100 MW also conditional base load; Bitdeer expanded to 35 MW at Kati 1 (hosting); Dorothy 2 energization (48 MW) completed Nov 2025, campus 123 MW; Rosenblatt Buy PT cut to $2 (Oct); next earnings 16 Nov 2026 — [StockAnalysis SLNH news](https://stockanalysis.com/stocks/slnh/); [Bitcoin.com on Dorothy 1B buyout](https://news.bitcoin.com/soluna-buys-out-dorothy-1b-as-bitcoin-to-ai-campus-conversion-advances/)
- Price: $0.57 (3 Nov) / $1.03 (5 Oct) / $1.20 (4 Sep) / $1.23 (25 Aug); low $0.52 (26 Oct) — [StockAnalysis SLNH history](https://stockanalysis.com/stocks/slnh/history/)

**7. Vulcan Infrastructure and Power (Nasdaq: VIP; ex-Greenidge GREE, renamed 24 Jul 2026) — 104 MW Dresden NY plant + Mississippi site**
- Market cap $42.01M; EV $78.41M; cash $3.20M; debt $39.60M; shares 35.60M, +26.08% YoY; TTM revenue $50.89M; 52-week −35.52% — [StockAnalysis VIP statistics](https://stockanalysis.com/stocks/vip/statistics/)
- Q2 2026 (14 Aug): revenue $3.4M; net loss $9.9M; cash incl. restricted $3.2M, $9.2M cash + digital assets; debt $36.9M; $39.4M PIPE (Machine Investment Group, Atlas Holdings, Conversant Capital, others) to redeem $33.1M 8.50% notes due Oct 2026; Columbus MS 34-acre site with ~40 MW expected by Q3 2027 — [AccessNewswire Q2 2026](https://www.accessnewswire.com/newsroom/en/oil-gas-and-energy/vulcan-infrastructure-and-power-reports-second-quarter-2026-results-1207572); [pulse2 on PIPE](https://pulse2.com/vulcan-infrastructure-and-power-raises-39-4-million-strategic-investment-from-machine-investment-group-atlas-holdings-conversant-capital-and-others/)
- 13 Oct 2026: redeemed all 8.50% senior notes due 2026 — [StockAnalysis VIP](https://stockanalysis.com/stocks/vip/)
- Q1 2026 (May): going-concern warning; proposed NYSEG interconnection for 60 MW Dresden AI/HPC; 250 MW load study Mississippi — [Rallies summary of Q1](https://rallies.ai/news/greenidge-doubles-power-revenue-to-187m-and-advances-60mw-ai-datacenter); [Greenidge Q1 2026 release PDF](https://greenidge.com/wp-content/uploads/2026/05/GREE_Q1_2026_Earnings_Release_FINAL.pdf)
- Dresden: approval for 60 MW non-curtailable grid power, 200 MW request pending; NY Governor's pause covers data centers ≥50 MW; Seneca County supervisors asked the state to deny air permit renewal; no tenant/lease found — [DCD rebrand](https://www.datacenterdynamics.com/en/news/greenidge-generation-rebrands-as-vulcan-infrastructure-and-power-targets-aihpc/); [FingerLakes1](https://www.fingerlakes1.com/2026/08/24/dresden-power-plant-could-shift-from-bitcoin-mining-to-ai-data-centers/)
- Price: $1.18 (3 Nov) / $1.52 (5 Oct) / $1.89 (4 Sep) / $1.82 (25 Aug); low $1.17 (2 Nov) — [StockAnalysis VIP history](https://stockanalysis.com/stocks/vip/history/)

**8. New Era Energy & Digital (Nasdaq: NUAI) — Texas Critical Data Centers (TCDC), Ector County TX**
- Market cap $296.23M; EV $241.59M; cash $69.82M; debt $15.17M; shares 106.56M, +239.18% YoY; TTM revenue $0.9M; 52-week −50.93% — [StockAnalysis NUAI statistics](https://stockanalysis.com/stocks/nuai/statistics/)
- 21 Sep 2026: 20-year PPA, TCDC PowerCo with Luminant (Vistra): minimum 200 MW, up to 207 MW for Phase 1 from Vistra's Odessa gas plant adjacent to site; firm power expected Q3 2027; Vistra gets 5% non-voting interest in the powered portion and ROFR — [Benzinga](https://www.benzinga.com/node/61890201); [Latitude Media](https://www.latitudemedia.com/industry-news/new-era-energy-digital-secures-20-year-207-mw-ppa-with-vistra/)
- 29 Oct 2026: $64M PIPE, 23,272,727 shares at $2.75, closing ~30 Oct; proceeds to repay Macquarie borrowings and working capital; management ties raise to leasing talks for 757 MW across Phases 1–2 — [SEC 8-K Ex.99.1](https://www.sec.gov/Archives/edgar/data/0002028336/000121390026113530/ea031006601ex99-1.htm)
- Bought out SharonAI's 50% of TCDC for $70M; non-binding LOI with Stream Data Centers; H1 2026 net loss $31M; no anchor tenant lease found — [Panabee](https://www.panabee.com/news/new-era-consolidates-texas-data-center-assets-in-70-million-sharonai-deal); [Panabee Q2](https://www.panabee.com/news/new-era-energy-digital-earnings-q2-2026)
- Next earnings 12 Nov 2026; B. Riley PT cut to $10 (31 Oct), Roth Buy (8 Oct) — [StockAnalysis NUAI](https://stockanalysis.com/stocks/nuai/)
- Price: $2.78 (3 Nov) / $6.05 (5 Oct) / $5.41 (4 Sep) / $5.07 (25 Aug); high $7.65 (21 Sep), low $2.33 (2 Nov) — [StockAnalysis NUAI history](https://stockanalysis.com/stocks/nuai/history/)

**9. VivoPower (Nasdaq: VIVO; ex-VVPR, renamed Mar 2026) — Norway/UAE/Finland data center sites (non-US assets)**
- Market cap $51.19M; EV $88.20M; cash $2.02M; debt $39.03M; shares 31.99M, +371.90% YoY; TTM revenue $2.55M; 52-week −45.76% — [StockAnalysis VIVO statistics](https://stockanalysis.com/stocks/vivo/statistics/)
- Acquired 41.5 MW Mo i Rana (Norway, hydro) 21 Apr 2026; preferred tenant selected 29 Jun 2026; 30 MW prequalified for Statnett reserve markets (~$1.9M EBITDA target); UAE 25 MW site/power access (Jan 2026); Finland 291 MW powered sites; $30M PIPE at $6.80 conversion — [Rallies RFP](https://rallies.ai/news/vivopower-launches-lease-rfp-for-415mw-norway-data-center-with-80mw-expansion-path); [TipRanks tenant](https://www.tipranks.com/news/company-announcements/vivopower-picks-global-ai-leader-as-preferred-tenant-for-norway-data-center); [Yahoo UAE](https://finance.yahoo.com/news/vivopower-secures-strategic-power-access-130000711.html)
- 3 Nov 2026: FY2026 results with partial-period Mo i Rana contribution; stock −27.4% that day to $1.60; mid-Oct: mobilized construction of 40 MW AI conversion in Norway; 21 Oct: heads of agreement with Open Innovation AI for sovereign AI DCs; next earnings ~23 Nov — [StockAnalysis VIVO](https://stockanalysis.com/stocks/vivo/)
- Price: $1.60 (3 Nov) / $3.36 (5 Oct) / $3.89 (4 Sep) / $4.17 (25 Aug) — [StockAnalysis VIVO history](https://stockanalysis.com/stocks/vivo/history/)

**10. Hyperscale Data (NYSE American: GPUS; ex-Ault Alliance / BitNile) — Michigan AI campus**
- Market cap $28.92M; EV $133.15M; cash $36.78M; debt $141.01M; shares 170.04M, +7,262.90% YoY; TTM revenue $130.16M; 52-week −91.56% — [StockAnalysis GPUS statistics](https://stockanalysis.com/stocks/gpus/statistics/)
- Alliance Cloud Services signed 20 MW agreement with an unnamed California neocloud, 10-year initial term + two 5-year options, ~$1.2B at max term; 30 MW energized at Michigan, 300+ MW long-term target; >$70M invested as of 15 Sep 2026; November 2026 targeted for operations; $120M Michigan reserve account; 830 BTC sold (~$53M); May 2026 registration of 43M resale shares from note conversions — [DCD](https://www.datacenterdynamics.com/en/news/hyperscale-data-signs-20mw-capacity-agreement-with-neocloud-customer-at-its-michigan-data-center/); [Finviz Sept update](https://finviz.com/news/392953/hyperscale-data-provides-update-on-progress-of-michigan-ai-data-center-more-than-70-million-invested-in-alliance-cloud-services-and-the-michigan-facility); [Quartr investor presentation](https://quartr.com/events/hyperscale-data-inc-gpus-investor-presentation_ojkNFE1m)
- Price: $0.17 (3 Nov) / $0.16 (5 Oct) / $0.19 (4 Sep) / $0.40 (25 Aug); low $0.13 (14 & 22 Oct) — [StockAnalysis GPUS history](https://stockanalysis.com/stocks/gpus/history/)

**11. Stabilis Solutions (Nasdaq: SLNG) — LNG behind-the-meter power for data centers (enabler)**
- Market cap $80.34M; EV $83.94M; cash $4.62M; debt $8.22M; shares −0.01% YoY; TTM revenue $55.89M; 52-week −12.73% — [StockAnalysis SLNG statistics](https://stockanalysis.com/stocks/slng/statistics/)
- Awarded an estimated $200M two-year behind-the-meter power contract for a U.S. data center, deliveries early 2027 to early 2029 (~$100M/yr); separate six-month LNG supply for commissioning another U.S. data center from Q3 2026; ~$25M customer prepayments fund equipment; Q2 2026 revenue $11.9M (−31% YoY) — [Newswire Q2 2026](https://www.newswire.com/news/stabilis-solutions-announces-second-quarter-2026-results); [Nasdaq Q2 call highlights](https://www.nasdaq.com/articles/stabilis-solutions-q2-earnings-call-highlights); [Simply Wall St narrative](https://simplywall.st/narratives/m1a5s0sl-multi-year-contract-risks-will-pressure-lng-while-optimism-grows-rye3)
- Customer not named in sources found; Q3 2026 results not checked.

**12. Pioneer Power Solutions (Nasdaq: PPSI) — PRYMUS mobile power / e-Boost (enabler)**
- Market cap $27.30M; EV $17.97M; cash $10.67M; debt $1.34M; shares 11.10M (YoY figure −99.8% is a data error); TTM revenue $21.80M; 52-week −46.52% — [StockAnalysis PPSI statistics](https://stockanalysis.com/stocks/ppsi/statistics/)
- Aug 2026: ~$200M PRYMUS quote pipeline, ~80% data center — quotes, not orders; Feb 2026 orders $1.8M mostly EV charging — [pulse2](https://pulse2.com/pioneer-power-builds-200-million-prymus-quote-pipeline-with-80-tied-to-data-centers/amp/); [Quantisnow](https://quantisnow.com/insight/pioneer-announces-18-million-in-new-orders-6409176)
- Price: $2.46 (3 Nov) / $3.25 (5 Oct) / $2.89 (4 Sep) / $2.85 (25 Aug) — [StockAnalysis PPSI history](https://stockanalysis.com/stocks/ppsi/history/)

**13. Ideal Power (Nasdaq: IPWR) — B-TRAN solid-state switch for 800V DC data center power (enabler)**
- Market cap $40.59M; EV −$0.34M; cash $41.29M; debt $0.36M; shares 16.43M, +28.86% YoY; TTM revenue $30K; 52-week −55.97% — [StockAnalysis IPWR statistics](https://stockanalysis.com/stocks/ipwr/statistics/)
- May 2026 ~$30M raise for B-TRAN commercialization and data center expansion; lead Asia customer building B-TRAN solid-state circuit breakers for 800V AI DC systems, prototypes Q4 2026; LOI to co-develop prototype for a U.S. hyperscaler evaluation (NVIDIA Rubin Ultra 800V DC) — [MarketChameleon](https://marketchameleon.com/articles/b/2026/5/15/ideal-power-30-million-btran-commercialization-data-center-industrials); [Trefis](https://www.trefis.com/data/companies/IPWR)
- Price: $2.47 (3 Nov) / $3.95 (5 Oct) / $4.82 (4 Sep) / $4.70 (25 Aug) — [StockAnalysis IPWR history](https://stockanalysis.com/stocks/ipwr/history/)

**14. Tecogen (TGEN) — gas-engine chillers for power-constrained data centers (enabler)**
- Market cap $56.75M; EV $52.59M; cash $6.78M; debt $2.62M; shares +18.65% YoY; TTM revenue $24.58M; 52-week −81.16% — [StockAnalysis TGEN statistics](https://stockanalysis.com/stocks/tgen/statistics/)
- Q2 2026 (12 Aug): revenue $5.75M (−21%), net loss $2.15M; backlog $6.95M; 12 data-center demos (attendees' DCs >8 GW); 1 MW chiller demo with Vertiv described as imminent PO in May 2026; July update: POs $3.3M, backlog expected >$8M; no confirmed data-center production orders — [Tecogen Q2 2026 release](https://ir.tecogen.com/press-releases/detail/477); [Tecogen Q1 8-K](https://www.sec.gov/Archives/edgar/data/0001537435/000153743526000036/tgenq12026earningsrelease.htm); [Barchart business update](https://www.barchart.com/story/news/3141246/tecogen-business-update)
- Price: $1.88 (3 Nov) / $2.54 (5 Oct) / $3.13 (4 Sep) / $3.18 (25 Aug) — [StockAnalysis TGEN history](https://stockanalysis.com/stocks/tgen/history/)

**Other in-band names screened (brief)**
- TSS Inc (Nasdaq: TSSI): market cap $198.38M; EV $169.47M; cash $67.68M; debt $38.77M; shares +9.13%; 52-week −65.30%; AI rack integration services, leased 380,000 sq ft warehouse (~early Oct 2026); earnings 5 Nov 2026; price $7.03 (3 Nov) / $10.05 (5 Oct) / $8.42 (4 Sep) / $8.52 (25 Aug) — [StockAnalysis TSSI statistics](https://stockanalysis.com/stocks/tssi/statistics/); [StockAnalysis TSSI](https://stockanalysis.com/stocks/tssi/); [history](https://stockanalysis.com/stocks/tssi/history/). Not an asset/power owner.
- Z Squared (Nasdaq: ZSQR): market cap $197.69M; 53.0M shares; 52-week −75.49%; cash/debt/revenue n/a — [StockAnalysis ZSQR statistics](https://stockanalysis.com/stocks/zsqr/statistics/). Acquired Paradox Data's Union County (El Dorado, AR) campus with existing Entergy Arkansas interruptible service up to ~8.0 MW; 150+ MW is an uncontracted development target; Union County data center moratorium July 2026–2027; consideration $5M Series A preferred + up to $20M on milestones — [SEC 8-K Ex.99.1](https://www.sec.gov/Archives/edgar/data/0001759186/000118518526003984/zsqrex99-1.htm); [DCD](https://www.datacenterdynamics.com/en/news/z-squared-agrees-to-acquire-full-ownership-of-paradox-data/)
- Axe Compute (Nasdaq: AGPU): market cap $87.63M; EV $67.38M; cash $21.91M; debt $1.66M; shares +412.02% YoY; TTM revenue $3.26M; 52-week −15.25% — [StockAnalysis AGPU statistics](https://stockanalysis.com/stocks/agpu/statistics/). $260M 36-month take-or-pay for 2,304 B300 GPUs (capacity provisioned by Aethir), $43M upfront received, go-live targeted Q3 2026 (unconfirmed as of search); separate claimed $1.5B five-year 9,200-GPU contract with unnamed customer; bought Duos' GPUaaS unit — [Finviz $43M](https://finviz.com/news/357350/axe-compute-receives-43m-payment-for-landmark-contract); [DCD $1.5B](https://www.datacenterdynamics.com/en/news/axe-compute-secures-15bn-compute-contract-with-unnamed-customer/); [Aethir blog](https://aethir.com/blog-posts/aethir-begins-provisioning-axe-computes-260m-b300-cluster-as-first-payment-lands)
- NeoVolta (Nasdaq: NEOV): market cap $122.75M; cash $22.20M; debt $9.21M; shares +16.98%; TTM revenue $13.33M; 52-week −52.73% — [StockAnalysis NEOV statistics](https://stockanalysis.com/stocks/neov/statistics/); Sept 2026 binding ~$53M capacity reservation (Infinite Grid Capital) for BESS for Northern Ontario edge AI DC projects in 2027 — [Finviz](https://finviz.com/news/393115/neovolta-announces-capacity-reservation-agreement-with-infinite-grid-capital-ahead-of-pendergrass-facility-grand-opening). Canadian end-market, battery maker; weak fit.
- Perma-Pipe (Nasdaq: PPIH): market cap $240.86M; EV $262.12M; shares +1.78%; TTM revenue $226.11M; 52-week +6.03% — [StockAnalysis PPIH statistics](https://stockanalysis.com/stocks/ppih/statistics/); orders >$28M first two months of fiscal Q3 incl. U.S. data center projects; backlog $121.6M at 31 Jan 2026; Ohio facility for data center market — [OffshoreSource](https://offshoresource.com/business-wire/perma-pipe-announces-new-orders-exceeding-28-million-in-north-america-through-first-two-months-of-fiscal-q3-with-strong-winter-activity-expected-in-canadian-oil-and-gas-sector/); [PGJ](https://pgjonline.com/news/2026/april/perma-pipe-books-54-million-in-q1-awards-across-energy-data-center-projects). Steady industrial, no un-priced story.
- AirJoule (Nasdaq: AIRJ): market cap $181.90M; cash $41.39M; pre-revenue; 52-week −51.94% — [StockAnalysis AIRJ statistics](https://stockanalysis.com/stocks/airj/statistics/); Aug 2026 collaboration with Net Zero Innovation Hub for Data Centers, pilot only — [AirJoule PR](https://airjouletech.com/2026/08/18/airjoule-technologies-and-the-net-zero-innovation-hub-for-data-centers-announce-strategic-collaboration-to-deploy-heat-to-water-technology-in-data-centers/). Drop (no contracts).
- Espey Mfg (ESP): market cap $151.15M; 52-week +38.26%; defense power electronics, no data center exposure found — [StockAnalysis ESP statistics](https://stockanalysis.com/stocks/esp/statistics/). Drop.

### Inferences
- EV / forward contracted annual revenue (my arithmetic from cited contract terms): DGXX ≈ $103.6M EV vs $93.6M/yr at full 40 MW ($195/kW/mo × 40,000 kW × 12) → ~1.1x EV, ~2.5x market cap; Phase 1 only ($35.1M/yr) → ~3x EV. HOST ≈ fully diluted ~48.1M shares × $2.59 ≈ $125M vs ~$83M/yr average base rent ($1.25B/15) → ~1.5x (cash/debt unknown). DUOT ≈ $82.5M EV vs ~$62M/yr (>$400M/10 + $111M/5) → ~1.3x EV, ~3.1x market cap. QMLS ≈ $229M EV vs ~$209M ARR claimed → ~1.1x. SLNG ≈ $84M EV vs ~$100M/yr for 2027–28 → ~0.8x. AIB: Nebius TCV not disclosed; EV $13M is tiny versus any plausible 50 MW 12-year lease, but revenue starts no earlier than Aug 2027.
- Fully diluted HOST share count is ~48.1M (28.2M Class A + 19.9M pre-funded warrants), so the $73M StockAnalysis market cap understates equity value by ~40%; the 45.4M-share resale registration (Graham Macro, BDS, 10X) is a large overhang relative to ~160K/day volume.
- DGXX is the only name where the three legs (binding named tenant, grid connection + own substation, financing) are all at least contractually identified; the financing leg is a commitment letter, not a closed loan, and energization is a December 2026 target.

### Gaps
- HOST: cash, debt and capex for Site I are not in the sources found; going-concern status conflicts between a secondary summary (doubt) and the 424B5 (12-month sufficiency). Q3 10-Q due ~17 Nov 2026.
- AIB: Nebius contract value and CLT1 capex not disclosed; no closing of project debt/preferred equity found.
- QMLS: the $500M USD.AI facility is described inconsistently (non-recourse vs non-binding); counterparties of the $240.9M contracts unnamed; Q2 PDF liquidity section not fully extracted.
- VIVO FY2026 results (3 Nov 2026) content not retrieved; whether the Mo i Rana preferred tenant signed a lease is unconfirmed.
- SLNG: data center customer unnamed; Q3 2026 results not checked.
- 90-day performance uses 25 Aug 2026 as the earliest available close (history page 1 of 3); exact 5 Aug closes not retrieved.

---

## KQ1. Which names have a binding, named customer contract AND energized power AND financing largely secured, yet trade below ~3x forward contracted revenue?

### Takeaway
None fully satisfies all three today. DGXX comes closest (Cerebras 40 MW take-or-pay, own substation and Alabama Power supply, $135M cash plus a $200M Goldman-syndicated commitment letter; ~1.1x EV / ~2.5x market cap to full-run-rate contracted revenue) but Phase 1 energization is a 15 Dec 2026 target and the loan is uncommitted until closing. HOST, AIB, DUOT and SLNG have binding contracts and sub-3x multiples but their power/build is 2027 and financing is open; QMLS is sub-3x but counterparties are unnamed and the balance sheet is lease-debt heavy.

### Cited Findings
- DGXX: Cerebras MSA $195/kW/mo take-or-pay, 15 MW + 25 MW, 3% escalator; substation built, grid connection finalized, Alabama Power agreement; $200M commitment letter 13 Oct 2026 to close within 90 days; ~$135M cash; Phase 1 Dec 2026 — [SEC 10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm); [DCD financing](https://datacenterdynamics.com/en/news/digi-power-x-secures-200m-in-debt-financing-for-alabama-data-center-project); [DCD Cerebras](https://www.datacenterdynamics.com/en/news/cerebras-signs-on-for-40mw-of-capacity-at-digi-power-x-data-center-in-alabama/)
- HOST: 43 MW, 15-year take-or-pay, ~$1.25B base rent, IG-backstopped, delivery H1 2027; only $17.5M gross raised at listing; capex not disclosed — [SEC 8-K Ex.99.1](https://www.sec.gov/Archives/edgar/data/0001948864/000149315226043135/ex99-1.htm); [SEC 424B5](https://www.sec.gov/Archives/edgar/data/0001948864/000149315226043454/form424b5.htm)
- AIB: Nebius 50 MW 12-year binding; 65 MW ESA at CLT1; first hall Aug 2027; funding via prepayments + project debt/pref equity, none closed — [SEC 8-K Nebius](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105865/ea030737801ex99-1.htm); [CEO letter](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026107421/ea030792301ex99-1.htm); [StockAnalysis AIB news](https://stockanalysis.com/stocks/aib/)
- DUOT: 20 MW 10-year >$400M TCV (publicly traded U.S. cloud provider, unnamed), Q2 2027; 10 MW 5-year $111M (IG hyperscaler), Q4 2026; cash $112M — [SEC 8-K Ex.99.2](https://www.sec.gov/Archives/edgar/data/1396536/000107997326000262/ex99x2.htm); [StockAnalysis DUOT statistics](https://stockanalysis.com/stocks/duot/statistics/)
- QMLS: $523.4M cumulative signed, ~$209M ARR once deployed; 8 MW HPC under lease; debt $130.8M; counterparties "AI inference platform providers" — [QumulusAI PR 15 Oct](https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Puts-71-9-Million-Blackwell-Agreement-into-Production-Signed-Customer-Contracts-Surpass-500-Million-2026.pdf); [StockAnalysis QMLS statistics](https://stockanalysis.com/stocks/qmls/statistics/)
- SLNG: ~$200M two-year BTM power contract from early 2027, $25M prepayments; EV $83.9M — [Newswire Q2](https://www.newswire.com/news/stabilis-solutions-announces-second-quarter-2026-results); [StockAnalysis SLNG statistics](https://stockanalysis.com/stocks/slng/statistics/)
- GPUS: 20 MW neocloud MSA (unnamed CA neocloud), 30 MW energized, but debt $141M vs market cap $29M — [DCD](https://www.datacenterdynamics.com/en/news/hyperscale-data-signs-20mw-capacity-agreement-with-neocloud-customer-at-its-michigan-data-center/); [StockAnalysis GPUS statistics](https://stockanalysis.com/stocks/gpus/statistics/)
- SLNH, VIP, NUAI, VIVO, ZSQR: no binding HPC tenant lease found (SLNH: Bitdeer 35 MW mining hosting + ChronoScale non-binding LOI; VIVO: preferred tenant only; NUAI: 207 MW PPA but no tenant; VIP: no tenant; ZSQR: 8 MW interruptible) — sources in KQ0.

### Inferences
- Multiples (my arithmetic): DGXX ~1.1x EV (~2.5x cap) at 40 MW; HOST ~1.5x fully diluted cap; DUOT ~1.3x EV / ~3.1x cap; QMLS ~1.1x EV; SLNG ~0.8x EV; AIB EV/contract not computable but EV $13M is far below any 50 MW 12-year lease value.
- Ranking on "closest to all three legs": DGXX > DUOT (cash-funded, hyperscaler-grade tenants, but edge-scale) > HOST (strongest single contract, weakest funding) > AIB (cheapest, latest delivery) > SLNG (enabler, binding but unnamed) > QMLS (contracted but credit/counterparty risk).

### Gaps
- Energized-MW-today for DGXX's other sites (NY, NC) and for HOST Site I not found; AIB's 15 MW energized in Texas is unrelated to the Nebius CLT1 contract.
- Whether DGXX's $200M facility closed is unknown (90-day window runs to ~mid-January 2027).

---

## KQ2. Which have diluted share count by >50% in 12 months (exclude)?

### Takeaway
By the >50% rule, exclude SLNH (+846%), GPUS (+7,263%), VIVO (+372%), AGPU (+412%), NUAI (+239% before a further 23.3M-share PIPE on 29 Oct), DUOT (+160%), AIB (+102%, IPO-driven) and DGXX (+92%, ATM-driven). QMLS (+49%) sits at the threshold; HOST has no 12-month history (reverse merger, 19.9M pre-funded warrants outstanding).

### Cited Findings
- SLNH shares +845.86% YoY (244.59M) — [StockAnalysis SLNH statistics](https://stockanalysis.com/stocks/slnh/statistics/); ATM 74.2M shares H1 2026 + 18.8M after quarter-end — [SEC 10-Q](https://www.sec.gov/Archives/edgar/data/0000064463/000162828026056702/slnh-20260630.htm)
- GPUS +7,262.90% (170.04M) — [StockAnalysis GPUS statistics](https://stockanalysis.com/stocks/gpus/statistics/)
- VIVO +371.90% (31.99M) — [StockAnalysis VIVO statistics](https://stockanalysis.com/stocks/vivo/statistics/)
- AGPU +412.02% — [StockAnalysis AGPU statistics](https://stockanalysis.com/stocks/agpu/statistics/)
- NUAI +239.18% (106.56M) plus 23,272,727 new shares at $2.75 (29 Oct 2026) — [StockAnalysis NUAI statistics](https://stockanalysis.com/stocks/nuai/statistics/); [SEC 8-K](https://www.sec.gov/Archives/edgar/data/0002028336/000121390026113530/ea031006601ex99-1.htm)
- DUOT +159.56% (31.47M) — [StockAnalysis DUOT statistics](https://stockanalysis.com/stocks/duot/statistics/)
- AIB +101.83% (75.98M) — [StockAnalysis AIB statistics](https://stockanalysis.com/stocks/aib/statistics/)
- DGXX +92.48% (102.06M); 27.95M ATM shares H1 2026 ($163.2M gross) — [StockAnalysis DGXX statistics](https://stockanalysis.com/stocks/dgxx/statistics/); [SEC 10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- QMLS +49.01% (33.46M) — [StockAnalysis QMLS statistics](https://stockanalysis.com/stocks/qmls/statistics/)
- Low-dilution names: VIP +26.08%; TGEN +18.65%; IPWR +28.86%; TSSI +9.13%; SLNG −0.01%; PPIH +1.78%; NEOV +16.98%; AIRJ +9.73% — respective StockAnalysis statistics pages cited in KQ0
- Below-band dilution cases: BGDE +245.65% (5.66M shares, market cap $17.84M) — [StockAnalysis BGDE statistics](https://stockanalysis.com/stocks/bgde/statistics/); DRK (ex-ANY) +49.87% — [StockAnalysis DRK](https://stockanalysis.com/stocks/any/statistics/); PWCM (ex-LMFA) +309.22% — [StockAnalysis PWCM](https://stockanalysis.com/stocks/lmfa/statistics/); SGRX (ex-BTOG) +341.08% — [StockAnalysis SGRX](https://stockanalysis.com/stocks/btog/statistics/); SOBR +175.37% — [StockAnalysis SOBR](https://stockanalysis.com/stocks/sobr/statistics/)

### Inferences
- The >50% rule removes most of the "real-asset" names; if the rule is applied strictly, the surviving in-band candidates with contracts are QMLS (borderline), HOST (no history; structural overhang) and SLNG (enabler). If IPO/ATM-funded capex dilution is tolerated when cash is retained (DGXX, AIB, DUOT), those three are the better-capitalised builders.
- HOST's 19.9M pre-funded warrants plus 45.4M registered resale shares mean effective float dilution risk is high even though the YoY metric is undefined.

### Gaps
- PPSI YoY figure (−99.8%) is a data error on the source page; true change not verified.
- Post-August share counts for SLNH (ATM may have continued) not checked.

---

## KQ3. Which have going-concern language (flag)?

### Takeaway
Explicit going-concern language was found for VIP/GREE (Q1 2026). HOST is contested (secondary summary says doubt; 424B5 says 12-month sufficiency). GPUS, VIVO, BGDE, DRK, PWCM, POLA, BEEM, NVVE, SGRX and SOBR show distress-level balance sheets but the search did not surface their going-concern text.

### Cited Findings
- GREE/VIP: Q1 2026 going-concern warning; exploring debt retirement, refinancing, equity — [Rallies Q1 summary](https://rallies.ai/news/greenidge-doubles-power-revenue-to-187m-and-advances-60mw-ai-datacenter); cash $3.2M vs debt $36.9M at 30 Jun 2026; $39.4M PIPE and Oct 2026 note redemption since — [AccessNewswire](https://www.accessnewswire.com/newsroom/en/oil-gas-and-energy/vulcan-infrastructure-and-power-reports-second-quarter-2026-results-1207572); [StockAnalysis VIP](https://stockanalysis.com/stocks/vip/)
- HOST: "going-concern doubt absent project financing and capital raises" — [roic.ai](https://www.roic.ai/quote/HOST) (secondary); 424B5 states cash + proceeds sufficient 12 months — [SEC 424B5](https://www.sec.gov/Archives/edgar/data/0001948864/000149315226043454/form424b5.htm)
- DGXX: statements "prepared on a going concern basis", no substantial-doubt language in the portion read — [SEC 10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- SLNH: $30.1M of debt classified current for covenant reasons at 30 Jun; Generate not accelerated; subsequently repaid in full — [theenergymag](https://www.theenergymag.com/news/market-news/soluna-holdings-reports-q2-2026-financial-results-and-debt-prepayment-agreement); [Panabee](https://www.panabee.com/news/soluna-repays-29-million-generate-capital-debt-reducing-total-principal-by-76)
- Sphere 3D/DarkHorse (DRK): cash $2.8M "insufficient for heavy infrastructure development" — [Panabee](https://www.panabee.com/news/sphere-3d-earnings-q2-2026-report); market cap $19.61M — [StockAnalysis DRK](https://stockanalysis.com/stocks/any/statistics/)
- LM Funding → PowerCompute (PWCM): market cap $1.02M, debt $19.97M, 52-week −97.87% — [StockAnalysis PWCM](https://stockanalysis.com/stocks/lmfa/statistics/); liquidity constraints noted — [Panabee](https://www.panabee.com/news/lm-funding-america-earnings-q2-2026)
- GPUS: debt $141.01M vs market cap $28.92M — [StockAnalysis GPUS statistics](https://stockanalysis.com/stocks/gpus/statistics/)
- VIVO: cash $2.02M, debt $39.03M — [StockAnalysis VIVO statistics](https://stockanalysis.com/stocks/vivo/statistics/)
- NeoVolta cash ~$212K at 31 Dec 2025 (liquidity concern) before 2026 raises — [MarketBeat](https://www.marketbeat.com/instant-alerts/neovolta-q3-earnings-call-highlights-2026-05-15/)

### Inferences
- VIP's post-PIPE/post-redemption 10-Q (Q3, due ~16 Nov 2026) will show whether the going-concern paragraph was lifted; until then treat as flagged.
- GPUS and VIVO behave like distressed equities (EV ≫ market cap, tiny cash); treat as "dilution trap / distress" regardless of going-concern text.

### Gaps
- Going-concern paragraphs of the latest 10-Qs for VIP, GPUS, VIVO (20-F), SLNH, QMLS, HOST were not read in full; VIP's Q2 10-Q link returned the 8-K instead.

---

## KQ4. Which have run >100% in the last 90 days (flag as possibly priced)?

### Takeaway
None. Every screened name is down over ~30, ~60 and ~70 days; most set 52-week or listing lows between 16 Oct and 2 Nov 2026. The group-wide drawdown, not a run-up, is the pricing signal.

### Cited Findings (close 3 Nov vs 5 Oct / 4 Sep / 25 Aug 2026; % are my calculations)
- SLNH $0.57 vs $1.03 / $1.20 / $1.23 → −45% / −53% / −54% — [history](https://stockanalysis.com/stocks/slnh/history/)
- VIP $1.18 vs $1.52 / $1.89 / $1.82 → −22% / −38% / −35% — [history](https://stockanalysis.com/stocks/vip/history/)
- HOST $2.59 vs $3.09 / — / $8.00 (21 Sep) → −16% / — / −68% since first full session — [history](https://stockanalysis.com/stocks/host/history/)
- AIB $0.87 vs $1.62 / $1.28 / $1.30 → −46% / −32% / −33% — [history](https://stockanalysis.com/stocks/aib/history/)
- DGXX $2.27 vs $3.73 / $3.75 / $4.05 → −39% / −39% / −44% — [history](https://stockanalysis.com/stocks/dgxx/history/)
- QMLS $3.54 vs $6.16 / $5.90 → −43% / −40%; −91% from $38 52-week high — [history](https://stockanalysis.com/stocks/qmls/history/); [statistics](https://stockanalysis.com/stocks/qmls/)
- NUAI $2.78 vs $6.05 / $5.41 / $5.07 → −54% / −49% / −45% — [history](https://stockanalysis.com/stocks/nuai/history/)
- VIVO $1.60 vs $3.36 / $3.89 / $4.17 → −52% / −59% / −62% — [history](https://stockanalysis.com/stocks/vivo/history/)
- GPUS $0.17 vs $0.16 / $0.19 / $0.40 → +6% / −11% / −58% — [history](https://stockanalysis.com/stocks/gpus/history/)
- DUOT $6.16 vs $9.19 / $8.76 / $10.22 → −33% / −30% / −40% — [history](https://stockanalysis.com/stocks/duot/history/)
- TSSI $7.03 vs $10.05 / $8.42 / $8.52 → −30% / −17% / −17% — [history](https://stockanalysis.com/stocks/tssi/history/)
- PPSI $2.46 vs $3.25 / $2.89 / $2.85 → −24% / −15% / −14% — [history](https://stockanalysis.com/stocks/ppsi/history/)
- IPWR $2.47 vs $3.95 / $4.82 / $4.70 → −37% / −49% / −47% — [history](https://stockanalysis.com/stocks/ipwr/history/)
- TGEN $1.88 vs $2.54 / $3.13 / $3.18 → −26% / −40% / −41% — [history](https://stockanalysis.com/stocks/tgen/history/)
- 52-week changes: AIB −94.5%, GPUS −91.6%, SLNH −83.7%, TGEN −81.2%, DGXX −62.4%, TSSI −65.3%, IPWR −56.0%, NUAI −50.9%, VIVO −45.8%, DUOT −40.5%, VIP −35.5%, SLNG −12.7%, PPIH +6.0% — StockAnalysis statistics pages cited in KQ0

### Inferences
- The uniform October 2026 collapse (many lows 26 Oct–2 Nov) looks sector-wide rather than name-specific; this matters for a "çöl" (desert/base-building) screen: none of these is in a multi-month tight base yet — they are still in the decline leg.

### Gaps
- Exact 90-day (5 Aug) closes were not retrieved (history page 1 covers 25 Aug onward); the 70-day proxy is used.

---

## KQ5. Re-check of SLNH, MIGI, NUAI; band check of large names; irrelevant names dropped

### Takeaway
SLNH: real power assets (Dorothy 123 MW energized, Kati 1 166 MW completed, ERCOT base-load positions) and now near debt-free, but no HPC lease and +846% share count — remains a dilution-funded option, not a contracted asset. MIGI is now Big Digital Energy (BGDE), $17.8M market cap, related-party colocation deals — below band and governance-flagged. NUAI has a real 207 MW Vistra PPA and $70M site consolidation but no tenant, +239% dilution plus a fresh $64M PIPE — story priced on a 1 GW narrative. All the listed large names are far above $300M except TSSI ($198M) and DUOT ($194M).

### Cited Findings
- SLNH facts: see KQ0 item 6 (10-Q, Generate repayment, APLD JV, Kati/Dorothy ERCOT positions, Bitdeer 35 MW) — [SEC 10-Q](https://www.sec.gov/Archives/edgar/data/0000064463/000162828026056702/slnh-20260630.htm); [StockAnalysis SLNH](https://stockanalysis.com/stocks/slnh/); [DCD JV](https://datacenterdynamics.com/en/news/soluna-and-applied-digital-to-build-50mw-data-center-in-texas)
- MIGI → Big Digital Energy (BGDE) from 30 Apr 2026; Endeavor colocation (~25,000 miners, ~75 MW, 50/50 profit share) with an affiliate controlled by the Executive Chair/CEO/COO — related-party under Nasdaq rules; July 2026 second 50/50 affiliate deal; Aug 2026 Tensor IQ LOI for Hood County TX AI campus — [Barchart](https://www.barchart.com/story/news/1535116/big-digital-energy-inc-announces-colocation-agreement-with-the-endeavor-group); [BriefGlance](https://briefglance.com/companies/mawson-infrastructure-group-inc/pulses/8377); [bitcoinminingstock.io](https://bitcoinminingstock.io/company/bgde). Market cap $17.84M, EV $33.98M, cash $16.29M, debt $32.43M, shares +245.65%, 52-week −86.18% — [StockAnalysis BGDE statistics](https://stockanalysis.com/stocks/bgde/statistics/)
- NUAI facts: see KQ0 item 8 — [Benzinga PPA](https://www.benzinga.com/node/61890201); [SEC 8-K PIPE](https://www.sec.gov/Archives/edgar/data/0002028336/000121390026113530/ea031006601ex99-1.htm); [StockAnalysis NUAI statistics](https://stockanalysis.com/stocks/nuai/statistics/)
- Band check (market cap, 3 Nov 2026 close, StockAnalysis statistics): KEEL (ex-Bitfarms) $1.35B, EV $1.68B, cash $715.5M, debt $1.04B — [KEEL](https://stockanalysis.com/stocks/keel/statistics/); IREN $9.64B — [IREN](https://stockanalysis.com/stocks/iren/statistics/); CIFR (Cipher Digital) $3.37B — [CIFR](https://stockanalysis.com/stocks/cifr/statistics/); HUT $7.86B — [HUT](https://stockanalysis.com/stocks/hut/statistics/); APLD $5.39B — [APLD](https://stockanalysis.com/stocks/apld/statistics/); CORZ $4.58B — [CORZ](https://stockanalysis.com/stocks/corz/statistics/); BTDR $1.88B — [BTDR](https://stockanalysis.com/stocks/btdr/statistics/); NBIS $41.56B — [NBIS](https://stockanalysis.com/stocks/nbis/statistics/); TSSI $198.38M (in band) — [TSSI](https://stockanalysis.com/stocks/tssi/statistics/); DUOT $193.87M (in band) — [DUOT](https://stockanalysis.com/stocks/duot/statistics/)
- Other large/out-of-band: ABTC (American Bitcoin, ex-Gryphon) $481.34M, shares +1,496% — [ABTC](https://stockanalysis.com/stocks/abtc/statistics/); Ionic Digital (IOND) ~$2.4B at reference price, aggregator snapshots $3.1–3.4B; 234 MW Nscale lease (+89 MW contingent) — [DCD](https://www.datacenterdynamics.com/en/news/ionic-digital-goes-public-on-nasdaq/); [Simply Wall St](https://simplywall.st/stock/NasdaqGS/IOND); SIFY $925.71M — [SIFY](https://stockanalysis.com/stocks/sify/statistics/); ERII $365.99M — [ERII](https://stockanalysis.com/stocks/erii/statistics/); Keel has no signed lease as of its Q2 report (goal: three leases in 2026) — [Keel Q2 2026](https://bitfarms.gcs-web.com/news-releases/news-release-details/keel-infrastructure-reports-second-quarter-2026-results)
- Below band / dead: DRK (ex-Sphere 3D ANY) $19.61M; 53 MW energized across five sites, 50 MW Hopkinsville KY plan, no AI/HPC commercial agreement — [StockAnalysis DRK](https://stockanalysis.com/stocks/any/statistics/); [Panabee](https://www.panabee.com/news/sphere-3d-earnings-q2-2026); PWCM (ex-LMFA, "PowerCompute") $1.02M; 26 MW OK/MS power, no hosting contract — [StockAnalysis PWCM](https://stockanalysis.com/stocks/lmfa/statistics/); [Panabee](https://www.panabee.com/news/lm-funding-america-pivots-to-ai-infrastructure-with-26mw-capacity); POLA $2.19M — [POLA](https://stockanalysis.com/stocks/pola/statistics/); BEEM $18.04M — [BEEM](https://stockanalysis.com/stocks/beem/statistics/); NVVE $0.75M (OTC) — [NVVE](https://stockanalysis.com/stocks/nvve/statistics/); Bit Origin → Sangrix (SGRX) $0.63M, debt $10.62M — [SGRX](https://stockanalysis.com/stocks/btog/statistics/); SOBR Safe $0.23M, merging with Clean World Ventures (clean energy for data centers), Nasdaq compliance issues — [SOBR](https://stockanalysis.com/stocks/sobr/statistics/); [Stocktwits](https://stocktwits.com/news-articles/Markets/Equity/sobr-stock-merger-/cZQVaFFReeS)
- Dropped as irrelevant: Prairie Operating (PROP) — oil & gas driller, no data center business ([Barchart Q1 2026](https://www.barchart.com/story/news/1942403/prairie-operating-co-announces-first-quarter-2026-results-and-reaffirms-2026-guidance)); BTCS, Vinco, Digital Ally — no 2026 data center news found; Arkon Energy — private; Polar Power — no data center activity found; Espey, AirJoule — no contracts.

### Inferences
- SLNH's EV ($65M) now sits below its cash after the Generate payoff, which makes it an "asset-rich, contract-poor, dilution-financed" name; the APLD JV cedes 51% of the only announced HPC project.
- NUAI's effective post-PIPE share count is ~130M, so at $2.78 the market cap is ~$360M — above the $300M band ceiling.

### Gaps
- MIGI/BGDE Q3 2026 status and whether the Tensor IQ LOI progressed were not found.
- Keel's Q3 2026 (late Oct/Nov) lease status not retrieved.

---

## Source list (primary and secondary, as used)

SEC EDGAR filings
- Digi Power X 10-Q Q2 2026 — https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm
- Soluna 10-Q Q2 2026 — https://www.sec.gov/Archives/edgar/data/0000064463/000162828026056702/slnh-20260630.htm
- Host Digital (HCWC) 8-K Ex.99.1 lease — https://www.sec.gov/Archives/edgar/data/0001948864/000149315226043135/ex99-1.htm
- Host Digital 424B5 (Sept 2026 offering) — https://www.sec.gov/Archives/edgar/data/0001948864/000149315226043454/form424b5.htm
- Host Digital S-3 resale (45.385M shares) — https://www.sec.gov/Archives/edgar/data/0001948864/000149315226047468/forms-3.htm
- AIB 8-K Nebius contract — https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105865/ea030737801ex99-1.htm
- AIB 8-K CEO letter (7 Oct 2026) — https://www.sec.gov/Archives/edgar/data/0002070542/000121390026107421/ea030792301ex99-1.htm
- AIB 8-K investor deck (Oct 2026) — https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105249/ea030723301ex99-1.htm
- Duos 8-K Ex.99.2 (20 MW) — https://www.sec.gov/Archives/edgar/data/1396536/000107997326000262/ex99x2.htm
- New Era 8-K PIPE — https://www.sec.gov/Archives/edgar/data/0002028336/000121390026113530/ea031006601ex99-1.htm
- Z Squared 8-K Ex.99.1 — https://www.sec.gov/Archives/edgar/data/0001759186/000118518526003984/zsqrex99-1.htm
- Tecogen Q1 2026 8-K — https://www.sec.gov/Archives/edgar/data/0001537435/000153743526000036/tgenq12026earningsrelease.htm

Company releases / IR
- QumulusAI Q2 2026 PR — https://s21.q4cdn.com/597044239/files/doc_financials/2026/q2/QumulusAI_Q2_2026_Earnings_Press_Release_LETTERHEAD.pdf
- QumulusAI 29 Sep / 15 Oct 2026 PRs — https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Signs-240-9-Million-in-New-AI-Inference-Customer-Contracts-for-NVIDIA-Blackwell-B300-Capacity-2026.pdf ; https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Puts-71-9-Million-Blackwell-Agreement-into-Production-Signed-Customer-Contracts-Surpass-500-Million-2026.pdf
- Vulcan Q2 2026 — https://www.accessnewswire.com/newsroom/en/oil-gas-and-energy/vulcan-infrastructure-and-power-reports-second-quarter-2026-results-1207572
- Greenidge Q1 2026 — https://greenidge.com/wp-content/uploads/2026/05/GREE_Q1_2026_Earnings_Release_FINAL.pdf
- Tecogen Q2 2026 — https://ir.tecogen.com/press-releases/detail/477
- Stabilis Q2 2026 — https://www.newswire.com/news/stabilis-solutions-announces-second-quarter-2026-results
- Keel Q2 2026 — https://bitfarms.gcs-web.com/news-releases/news-release-details/keel-infrastructure-reports-second-quarter-2026-results
- Host Digital debut (via Finviz) — https://finviz.com/news/394186/...
- Digi Power X $200M commitment (via Finviz) — https://finviz.com/news/401609/...
- AIB Texas acquisition (via Finviz) — https://finviz.com/news/391604/...
- Soluna/APLD JV (via Finviz) — https://finviz.com/news/405148/...
- AirJoule collaboration — https://airjouletech.com/2026/08/18/...

Market data (all 3 Nov 2026 close, StockAnalysis.com statistics / history / overview pages)
- https://stockanalysis.com/stocks/{slnh,vip,host,aib,dgxx,qmls,nuai,vivo,gpus,duot,tssi,ppsi,ipwr,tgen,slng,ppih,neov,airj,esp,agpu,zsqr,keel,iren,cifr,hut,apld,corz,btdr,nbis,abtc,sify,erii,beem,nvve,bgde,any,lmfa,pola,btog,sobr}/statistics/ and corresponding /history/ pages

Trade press / secondary (leads only)
- DataCenterDynamics (Cerebras–DGXX; DGXX financing; Soluna–APLD; Duos 20 MW; GPUS 20 MW; Vulcan rebrand; Ionic Digital; Z Squared; Axe Compute)
- Panabee, Rallies, Zacks, BriefGlance, roic.ai, Quartr, MarketBeat, pulse2, Stocktwits, TipRanks, Benzinga, Latitude Media, FingerLakes1, Capital.com (as cited inline; treated as secondary)
