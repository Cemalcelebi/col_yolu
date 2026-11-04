# Neocloud / AI veri merkezi ekonomisi ve "10x" matematiği — sektör notları (4 Kasım 2026 itibarıyla)

Amaç: $100–250M piyasa değerli ABD mikro-cap AI-altyapı şirketlerinin (QMLS, DGXX, AIB, VVPR) 1–3 yılda $1–2B'ye çıkıp çıkamayacağını ve hisse başına değerin bunu izleyip izlemeyeceğini yargılamak için gereken sayısal kanıt. Her sayı tarihli; tahminler "(tahmin)" veya "(kendi hesabım)" diye işaretli. Kaynak listesi sonda.

Kısa Türkçe özet (ayrıntı aşağıda, İngilizce):
- Kolokasyon kirası 2025–26 sözleşmelerinde yaklaşık $1,8–2,3M/MW/yıl (APLD–CoreWeave $1,83M; HUT–Fluidstack $1,90M; CIFR–Fluidstack $1,79M; DGXX–Cerebras $2,34M taban, %3 artışlı). GPU-as-a-service ise ~$9,7–12M/MW/yıl ama $40M/MW GPU yatırımı ister.
- AI'ya hazır kabuk+altyapı $15–25M/MW (JLL/Goldman; GPU hariç); GPU dâhil $30–60M/MW.
- Piyasa sözleşmeli MW'a APLD'de $8,2M, WULF'ta $13,2M EV/MW ödüyor (Windsor Drake, 18 Eyl 2026); DGXX'e ~$2,7M/MW, AIB'ye ~$1,3M/MW (kendi hesabım) — mikro-cap iskontosu büyük.
- 2024→2026 hisse sayısı: APLD +148%, CORZ +81%, WULF +65%, CIFR +54%, HUT +38%, BTDR +110% (2 yıl), DGXX +207%, AIB +102% (5 ay), SLNH ×86 (ters bölünme sonrası), MIGI ters bölünme + delist tehdidi (SEC XBRL).
- 10x'i yakalayanlar (IREN, WULF, CIFR, APLD, CORZ) bunu 2022 kripto kışı diplerinden, sözleşme ÖNCESİ, $70–600M değerle ve yüzlerce MW enerjili sahayla yaptı; sözleşmeyi duyurduklarında zaten $0,6–3,9B değerdeydiler. $100–250M bandında sözleşme duyuran mikro-caplar (SLNH, MIGI, DGXX, AIB, ANY) hisse başına çoğunlukla düştü: backlog hisse değerine değil, hisse sayısına dönüştü.
- Tez öldüren tek risk: mikro-caplarda ATM/dilüsyon ve finansman; orta boylarda teslim gecikmesi (CORZ Denton → CoreWeave 2025 tahmin düşüşü); henüz kamuya açık bir GPU-destekli neocloud temerrüdü yok (Ekim 2026).

---

## Key Question 1 — Unit economics: GPU rental prices, depreciation, utilization, margins, capex/MW, revenue/MW

### Takeaway
GPU rental fell through 2025 (H100 1-yr contract ~$1.70/h in Oct 2025) then recovered 2026 (~$2.35 contract, ~$3.9–4.2 on-demand median by Oct–Nov 2026); colocation lease revenue clusters at $1.8–2.3M/MW/yr while GPU-as-a-service yields ~$10–12M/MW/yr but needs ~$40M/MW of GPUs on top of $15–25M/MW of AI-ready shell. Public-neocloud EBITDA margins are high (CoreWeave 59%, Nebius 41–50%) but GAAP losses persist because of interest and depreciation, and the 6-year GPU life is contested.

### Cited Findings
**GPU rental prices (per GPU-hour)**
- H100 on-demand median $4.20 across 16 providers on 7 Oct 2026; H200 median $5.70 (14 providers, range $3.99–10.60); B200 median $8.19 (9 providers) — [Uvik GPU Price Index](https://uvik.net/blog/gpu-price-index/)
- H100 on-demand median $3.87 across 46 providers, week of 2 Nov 2026 — [getdeploying GPU price trends](https://getdeploying.com/gpu-price-trends); hyperscalers charge ~75% more than specialist GPU clouds for H100 — same source
- Runpod Secure Cloud H100: ~$2.89 PCIe / ~$3.99 SXM5 (12 Oct 2026) — [Spheron H100 price 2026](https://www.spheron.network/blog/nvidia-h100-price-2026/)
- B200 on-demand climbed 79% over three months to $8.01 avg by late Sept 2026 (citing SemiAnalysis); specialist-provider B200 $2.12 spot to $4.99–6.04 — [shattered.io B200](https://shattered.io/nvidia-b200-cloud-price-79-percent-surge-2026/) (vendor blog; weak)
- SemiAnalysis H100 index (cited second-hand): 1-year contract rates fell to ~$1.70/GPU-h in Oct 2025, recovered to ~$2.35 by Mar 2026 (attributed to Blackwell supply tightness and inference demand) — [drops-154 GPU depreciation wiki](https://drops-154.pages.dev/ai-capex/wiki/economics/gpu-depreciation/) (aggregator; verify against SemiAnalysis)
- "H100 rental rates climbing nearly 40% since Oct 2025, from ~$1.70 to $2.35" — [shattered.io H100 2026](https://shattered.io/h100-h200-b200-cloud-gpu-pricing-2026/) (vendor blog)
- Sources conflict: one claims in June 2026 B200 was briefly 18% cheaper than H100 — [Uvik](https://uvik.net/blog/gpu-price-index/); treat all index numbers as indicative only.

**Revenue per GPU / per MW (GPU-as-a-service)**
- IREN–Microsoft: 5-year ~$9.7B GPU cloud contract for GB300 capacity across four "Horizon" halls at Childress TX totalling ~200 MW IT load, 8-K filed 3 Nov 2025; $5.8B Dell purchase agreement for the GPUs — [TechInformed](https://techinformed.com/microsoft-signs-9-7-billion-iren-deal-for-nvidia-gb300-capacity/); [Pulse2](https://pulse2.com/iren-secures-9-7-billion-ai-cloud-contract-with-microsoft/amp/). Arithmetic (kendi hesabım): $9.7B/200 MW/5 yr ≈ $9.7M per MW per year; GPU capex $5.8B/200 MW ≈ $29M/MW for GPUs alone.
- SemiAnalysis podcast (via FourWeekMBA): GB300 cluster ~$40M per MW; neocloud rental revenue ~ $12M per MW per year; half-utilized racks "compress the economics quickly" — [FourWeekMBA](https://fourweekmba.com/ai-frontier-tokens-100m-per-mw-payback-half-a-year/) (secondary)
- 8-GPU H100 server at 100% utilization at published rates: $241k/yr (Lambda) to $432k/yr (CoreWeave); blended realized utilization estimated 60–85% depending on provider/contract mix; CoreWeave does not disclose fleet utilization — [Luminix neocloud deep-dive](https://www.useluminix.com/reports/industry-analysis/deep-dive-on-the-neocloud-gpu-rental-industry-coreweave-lambda-crusoe/source/4) (secondary)
- Own arithmetic: $2.35/h × 8,760 h ≈ $20.6k per H100 per year at 100% utilization (contract rate), ~$165k per 8-GPU node.

**Revenue per MW (colocation / powered shell)**
- Applied Digital–CoreWeave: contracted capacity raised from 250 MW to 400 MW at Ellendale (Polaris Forge 1), total contract value ~$11B, 15-year leases — [APLD Q1 FY2026 release](https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-25-000068/apldq126earningsrelease.htm); [DCD](https://www.datacenterdynamics.com/en/news/coreweave-signs-on-for-another-150mw-of-capacity-at-applied-digital-data-center-campus/). Kendi hesabım: $11B/400 MW/15 yr ≈ $1.83M/MW/yr.
- Hut 8–Fluidstack (River Bend, LA): 15-year triple-net lease, 245 MW IT, base-term value $7.0B incl. 3.0% annual escalator; expected cumulative NOI $6.9B (~$454M/yr avg); financing "expected to provide 85% loan-to-cost" (J.P. Morgan, Goldman) — announced 17 Dec 2025 — [Hut 8 press release](https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion). Kendi hesabım: $7.0B/245 MW/15 ≈ $1.90M/MW/yr revenue, NOI ≈ $1.85M/MW/yr.
- Cipher–Fluidstack (Barber Lake, TX): 10-year, 168 MW critical IT, ~$3B contracted revenue; expansion 20 Nov 2025: +39 MW IT, ~$830M over 10 years — [Cipher 8-K exhibit](https://www.sec.gov/Archives/edgar/data/1819989/000095010325012168/dp234624_ex9901.htm); [Cipher PR](https://ciphermining.gcs-web.com/news-releases/news-release-details/cipher-mining-signs-additional-56-mw-10-year-ai-hosting). Kendi hesabım: $1.79M/MW/yr (original), $2.13M/MW/yr (expansion).
- TeraWulf–Fluidstack: $3.7B contracted revenue over initial 10-year terms (~200 MW), two 5-yr extensions worth +$5B; expanded to $6.7B — [The Block](https://www.theblock.co/post/366959/bitcoin-miner-terawulf-shares-jump-50-after-google-secures-8-stake-as-part-of-3-7-billion-10-year-ai-compute-deal). Kendi hesabım ≈ $1.85M/MW/yr.
- Digi Power X–Cerebras (Columbiana, AL): 10-year colocation + MSA signed 4 May 2026; take-or-pay $195.00 per kW per month (≈$2,925,000/mo Phase 1 15 MW; $4,875,000/mo Phase 2 25 MW), escalating 3.0%/yr; DGXX builds Tier III facility "at its sole cost" — [DGXX 10-Q Q2 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm). Kendi hesabım: $2.34M/MW/yr base rent (highest per-MW rate in the sample; small site, Tier III, self-funded).
- Core Scientific: billing 437 MW by mid-July 2026 = ~$635M average annualized colocation GAAP revenue — [Core Scientific Q2 2026 8-K](https://www.sec.gov/Archives/edgar/data/0001839341/000183934126000013/q22026corescientificinc-ea.htm). Kendi hesabım ≈ $1.45M/MW/yr (straight-lined GAAP, older 2024 pricing).
- Median NOI per MW of IT load for 2026 leases: record $1.66M, up from $1.57M (2025) and $1.28M (2024) — [datacentres.com, 11 Aug 2026](https://www.datacentres.com/news/data-centre-m-a-reaches-187b-peak-as-hyperscalers-consolidate-ai-infrastructure-slot1-2026-08-11)

**Capex per MW**
- JLL: global average data center construction cost $11.3M/MW in 2026 (+6% vs 2025); rose from $7.7M (2020) to $10.7M (2025); US major markets ~$10–14M/MW — [CoR Advisors summarizing JLL](https://www.coradvisors.net/2026/06/ai-data-center-development-costs-2026.html)
- Goldman Sachs: next-gen AI facilities $15–20M/MW vs ~$10M/MW conventional hyperscale — same source
- Axis Intelligence (secondary): AI-capable shell + infrastructure $15–25M/MW; all-in with GPU fit-out $30–45M/MW; liquid-cooled halls $4.5–5.2M/MW for cooling alone vs $1.8M/MW air — [Axis Intelligence](https://axis-intelligence.com/ai-data-center-cost-per-mw/)
- Epoch AI 1 GW model: $38B upfront capex (≈$38M/MW) — via [Investing.com](https://www.investing.com/news/stock-market-news/how-much-does-a-gw-of-data-center-capacity-actually-cost-4314046)
- DGXX H1 2026: PP&E additions $55.7M; Tier III project assets $6.9M under construction at 30 Jun 2026; equipment supplier payments $14.6M to date — [DGXX 10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm). No total Phase 1/2 cost disclosed.

**Margins (public neoclouds)**
- CoreWeave Q2 2026 (quarter ended 30 Jun 2026): revenue ~$2.58B (+112% YoY); adjusted EBITDA $1.51B, 59% margin (62% a year earlier); adjusted operating income $128M, 5% margin (16% a year earlier); GAAP net loss $626M; net interest expense ~$640M (vs $267M); backlog ~$104B; FY2026 revenue guidance $12.4–13.2B — [Blockspace](https://blockspace.media/insight/coreweave-q2-revenue-backlog-grows-2026/); [Pulse2](https://pulse2.com/coreweave-revenue-backlog-reaches-104-billion-before-another-25-billion-of-new-commitments/); [Quartr](https://quartr.com/events/coreweave-inc-crwv-q2-2026_F6huCJA4); primary: [CoreWeave IR](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx)
- CoreWeave debt $35bn as of 30 Jun 2026 — [Capacity](https://capacityglobal.com/news/coreweaves-debt-hits-35bn/)
- Nebius Q2 2026 (shareholder letter, 6-K): revenue $582.3M (+454% YoY); group adj. EBITDA $236.2M (41% margin); AI-cloud adj. EBITDA $285.7M (49.7%); Q2 capex ~$5.7B; cash ~$8B; ARR $3.0B; customer commitments >$40B; >$9B customer prepayments expected in 2026, ~70% of Q2 deals included prepayments covering 50–60% of associated capex; ATM: 12.7M shares sold at avg $223.6 (~$2.8B); July secured facility $775M at SOFR+2.50% — [Nebius 6-K Q2 2026](https://www.sec.gov/Archives/edgar/data/0001513845/000110465926094568/tm2622968d1_ex99-2.htm)
- Core Scientific Q2 2026: revenue $164.2M (colocation $136.7M); adj. EBITDA $41.1M; net loss $1.16B (warrant fair-value); liquidity $1.82B — [CORZ 8-K](https://www.sec.gov/Archives/edgar/data/0001839341/000183934126000013/q22026corescientificinc-ea.htm)

**GPU depreciation debate**
- CoreWeave lengthened useful life of technology equipment from 5 to 6 years at the start of 2023 — [Tom's Hardware](https://www.tomshardware.com/tech-industry/gpu-depreciation-could-be-the-next-big-crisis-coming-for-ai-hyperscalers-after-spending-billions-on-buildouts-next-gen-upgrades-may-amplify-cashflow-quirks)
- Chanos: CEO claimed customers would rent GPUs "6 or 7 years"; Chanos argued even 10-year depreciation leaves CoreWeave weak — [Webull/Chanos](https://www.webull.com/news/13650205142680576)
- Burry (Nov 2025): five largest hyperscalers understate depreciation by cumulative $176B 2026–28; chips on 12–18-month obsolescence cycles treated as 4–6-year assets — [Nasdaq/Fool](https://www.nasdaq.com/articles/michael-burrys-latest-warning-could-be-bad-news-coreweave)
- CoreWeave defense: average contract 5 years, GPUs depreciated over 6; A100 prices "appreciating" in 2025 — [247WallSt](https://247wallst.com/investing/2026/02/28/investors-hated-coreweaves-earnings-it-might-be-even-worse-than-they-realize/)
- Kerrisdale (citing SemiAnalysis TCO): CoreWeave EBIT margin ~20.5% under 6-yr depreciation & 87% utilization; near 0% or negative with 4–5-yr lives — [drops-154 wiki](https://drops-154.pages.dev/ai-capex/wiki/economics/gpu-depreciation/) (secondary)
- Used H100 SXM realized sale ~ $14,250 in Oct 2026, dealer median ask $16,576 — [American Compute H100 appraisal](https://www.amcompute.com/appraisals/h100); used H100 $12–22k mid-2026 vs ~$40k late 2023 — [Servnet UK](https://www.servnetuk.com/insights/refurbished-h100-h200-secondary-market-2026-uk); conservative residual forecast 11–19% of list in 2027, 5–7% in 2028 (as of June 2026) — [American Compute residual index](https://www.amcompute.com/gpu-resale-index/residual-value/h100) (vendor with stake)

### Inferences
- A colocation landlord's revenue (~$1.8–2.3M/MW/yr) is ~15–20% of a GPU-as-a-service operator's (~$10–12M/MW/yr), but the landlord's capex is ~$10–25M/MW vs ~$40–60M/MW all-in; the landlord's revenue line is also the one that comes with 10–15-year take-or-pay contracts, while GPU rental repriced ±40% within 12 months.
- DGXX's $195/kW-month is above the sample's $150–160/kW-month equivalents; the premium plausibly reflects Tier III spec, small size and DGXX bearing all construction cost — i.e. it is not evidence of a stronger negotiating position.
- At 85% loan-to-cost (Hut 8) a contracted, Google-backstopped lease can be built with ~15% equity; absent an investment-grade backstop, lenders size to the tenant's credit, not the landlord's (see Q4).

### Gaps
- No primary SemiAnalysis H100/B200 index values retrieved (paywalled); contract-rate figures are second-hand.
- Fleet utilization is not disclosed by CoreWeave/Nebius/IREN; 60–85% is a third-party estimate.
- DGXX and AIB have not disclosed total build cost per MW.
- No Uptime Institute or CBRE primary report fetched; JLL numbers come via a secondary summary.

---

## Key Question 2 — Timeline realities: lease-to-energization, transformer lead times, interconnection backlogs, promised-vs-delivered

### Takeaway
Substation transformer lead times exceed 160 weeks in 2026 (Wood Mackenzie) and PJM projects entering service in 2025 averaged >7 years; operators with pre-existing energized power (ex-bitcoin sites) delivered first halls 5–17 months after lease signing, but the biggest slip in the sample (Core Scientific's Denton shell for CoreWeave) forced CoreWeave to cut 2025 guidance in Nov 2025 and spawned securities suits.

### Cited Findings
**Transformers and grid**
- Wood Mackenzie (Ben Boucher): substation transformer lead times ~140 weeks in 2023, ~150 weeks in 2025, >160 weeks in 2026; large substation and GSU transformers range 80–210 weeks; ~50 weeks in 2021 vs ~120 weeks in 2024 — [Data Center Knowledge, 12 May 2026](https://datacenterknowledge.com/energy-power-supply/why-ai-data-center-projects-face-years-of-delays-after-approval)
- PJM: projects entering service in 2025 averaged over seven years to become operational (≈3 years to interconnection service agreement + ~4 years after); 220 GW proposed for next cycle (preliminary); as of Jan 2026, >21 GW in engineering/procurement and 8.2 GW under construction; 95 large-load adjustment requests ≈ 54 GW through Nov 2025; milestone-change causes: permitting 29%, "other" (EPC, equipment, construction, land) 28%, supply chain 23% — same DCK article
- US transformer lead times "extend to four years" — [ESS News, 12 May 2026](https://www.ess-news.com/2026/05/12/us-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/)
- ERCOT large-load interconnection requests reportedly >230 GW in 2025 vs 63 GW end-2024 — [enkiai](https://enkiai.com/data-center/grid-shortage-pjm-ercot-data/) (aggregator; unverified)
- PJM moved from first-come-first-served to cluster review; Cycle 1 projects expected to receive agreements in 1–2 years — DCK article above

**Promised vs delivered (dated)**
- Core Scientific–CoreWeave: 12-year contracts signed from June 2024; Q1 2026 call (May 2026): billing 243 MW, expected >450 billable MW by end of summer 2026, full 590 MW by early 2027 — [MarketBeat Q1 2026 call](https://www.marketbeat.com/instant-alerts/core-scientific-q1-earnings-call-highlights-2026-05-06/); Q2 2026: 395 billing MW (vs 225 MW in Q1 2026), 437 MW by mid-July 2026 — [CORZ 8-K Q2 2026](https://www.sec.gov/Archives/edgar/data/0001839341/000183934126000013/q22026corescientificinc-ea.htm). Kendi hesabım: ~26 months from first contract to ~400 MW billing; the "450 MW by end of summer" target was not met by mid-July (437 MW reported).
- CoreWeave guidance cut, 10 Nov 2025: 2025 revenue guidance revised to $5.05–5.15B due to a third-party data center developer behind schedule on "power shell delivery"; Q4 capex guidance cut nearly in half; shares −13%; The Information identified the site as Denton, TX (Core Scientific lease; not confirmed by either company); securities class actions filed Jan 2026 — [StreetInsider](https://www.streetinsider.com/Earnings/CoreWeave+flags+hit+from+data+center+delay%2C+shares+fall/25585703.html); [DCD lawsuit](https://www.datacenterdynamics.com/en/news/coreweave-shareholder-files-lawsuit-alleging-company-mislead-investors-over-ability-to-deliver-compute/); [DCD Denton](https://www.datacenterdynamics.com/en/news/coreweave-deploys-16000-gpus-at-delayed-data-center-in-denton-texas/)
- Core Scientific also "missed its publicly announced deadline for securing additional customer contracts" and attributed timeline extensions to reduced hyperscaler engagement during the merger period — [Circlo summary](https://circlo.io/?p=89198) (secondary; verify)
- Applied Digital Ellendale: CoreWeave leases announced mid-2025; Building 1 Phase I (50 MW) Ready-for-Service 27 Oct 2025, Phase II completing 100 MW on 24 Nov 2025 "on time"; Building 2 Phase 1 added 75 MW in July 2026 (175 MW live, 400 MW contracted) — [APLD PR 27 Oct 2025](https://ir.applieddigital.com/news-events/press-releases/detail/133/applied-digital-achieves-ready-for-service-for-phase-1-at); [APLD PR 24 Nov 2025](https://ir.applieddigital.com/news-events/press-releases/detail/137/applied-digital-completes-phase-ii-ready-for-service-at); [Converge Digest](https://convergedigest.com/applied-digital-brings-75-mw-phase-online/?amp=1). APLD delayed its South Dakota site "as it evaluates long-term viability" (April 2026) and amended two CoreWeave leases in April 2026 (terms not found) — [Barchart](https://www.barchart.com/story/news/35393328/applied-digitals-earnings-call-expansion-amid-challenges); [Seeking Alpha](https://seekingalpha.com/news/4571176-applied-digital-amends-n-d-data-center-leases-with-coreweave)
- Cipher Barber Lake: 168 MW signed Sept 2025, "expected to deliver by September 2026" — [Cipher 8-K exhibit](https://www.sec.gov/Archives/edgar/data/1819989/000095010325012168/dp234624_ex9901.htm); analyst note (2026) said both data centers "targeting October 2026 energization" — [AOL/KBW](https://www.aol.com/articles/wall-street-cuts-cipher-mining-135628583.html). One-month slip, unconfirmed.
- TeraWulf Lake Mariner: Q1 2026 release — CB-3 "nearly complete, energization aligned to customer hardware deployment"; CB-4 and CB-5 "on schedule for 2026" — [WULF Q1 2026 8-K](https://www.sec.gov/Archives/edgar/data/0001083301/000108330126000083/a_wulfearningsreleaseq1202.htm); Anthropic lease at Justified Data: initial capacity H2 2027, full 401 MW early 2028 — [WULF 10-Q Q2 2026](https://www.sec.gov/Archives/edgar/data/0001083301/000108330126000166/wulf-20260630.htm)
- DGXX–Cerebras: signed 4 May 2026; Phase 1 (15 MW) targeted Dec 2026, Phase 2 by Q1 2027 (per press); facility "under construction, not ready for use" at 30 Jun 2026 — [DCD](https://www.datacenterdynamics.com/en/news/cerebras-signs-on-for-40mw-of-capacity-at-digi-power-x-data-center-in-alabama/); [DGXX 10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- AIB–Nebius: announced 30 Sep 2026; 50 MW in two halls, first "within 10 months", second "in 14 months" (press coverage); site has pre-existing 65 MW, 15-year Electric Service Agreement, "no significant additional electrical infrastructure upgrades required" — [AIB 8-K ex.99.1](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105865/ea030737801ex99-1.htm); [DCD](https://datacenterdynamics.com/en/news/nebius-signs-50mw-lease-with-aib-data-centers)
- Mawson (now Big Digital Energy, BGDE): 2024 20 MW AI/HPC colocation with BE Global; by 17 Apr 2026 Nasdaq delist determination (stockholders' equity < $2.5M at 31 Dec 2025), hearing requested — [Panabee](https://www.panabee.com/news/mawson-fails-1-00-bid-price-rule-faces-nasdaq-delisting-hearing); [Panabee rebrand](https://www.panabee.com/news/mawson-infrastructure-rebrands-to-big-digital-energy-amid-nasdaq-delisting-defense)
- Sphere 3D (ANY): Q2 2026 net loss $13.8M on $2.5M revenue; going-concern doubt; AI/HPC shift "theoretical until it secures non-mining counterparties" — [Panabee Sphere 3D](https://www.panabee.com/news/sphere-3d-earnings-q2-2026)
- Hut 8 River Bend: lease announced 17 Dec 2025; closing "subject to definitive agreements"; no delivery date found in results — [Hut 8 PR](https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion)

### Inferences
- Where utility power already exists at the fence (ex-mining sites, AIB's 65 MW ESA, DGXX's on-site substation), lease-to-first-hall is 5–14 months; where a new substation/transformer is needed, the 160-week transformer queue dominates and 2–4 years is realistic.
- Slippage in the sample is modest in months (CIFR ~1 month; CORZ "450 by end of summer" → 437 by mid-July) but has outsized stock impact when it lands on a big customer's guidance (CoreWeave −13% in a day; CORZ −10%).
- For a micro-cap, a 3–6-month slip is also a cash-burn and ATM event because rent only starts at Ready-for-Service.

### Gaps
- No primary PJM/ERCOT/TVA/NYISO queue reports fetched; NYISO and TVA not covered at all.
- Hut 8 River Bend delivery schedule and whether financing closed: not found.
- Soluna, Bitdeer, Mawson promised-vs-delivered MW by date: not found in the searches run.

---

## Key Question 3 — Financing realities: GPU loans, ABS, prepayments, converts, ATMs; dilution outcomes 2024→2026

### Takeaway
GPU-backed debt runs at 60–70% LTV and has repriced from ~SOFR+870 bps (2023) to ~SOFR+225 bps for investment-grade-contracted CoreWeave (2026), but that pricing exists only for IG counterparties; small operators financed 2024–26 chiefly with ATMs and converts, and cover-page share counts grew 38–207% at mid/large peers and 2–86x at micro-caps.

### Cited Findings
**Debt terms**
- Asset-backed loans on H100/B200 hardware cap at 60–70% LTV; operators fund 20–30% equity — [Spheron GPU financing](https://www.spheron.network/blog/gpu-financing-and-offtake-agreements-for-smaller-operators-2/); "LTV in the region of 60–70%" — [Wing VC "How the GPU became collateral"](https://www.wing.vc/content/how-the-gpu-became-collateral)
- CoreWeave Aug 2023 $2.3B DDTL at Term SOFR + 9.6196%; May 2024 facility at Term SOFR + 6.00% to 13.00% depending on customer credit rating — [amcompute largest GPU loans](https://www.amcompute.com/gpu-debt/largest-gpu-loans) (tracker); spread compressed from ~870 bps (2023) to 225 bps on the $8.5B DDTL 4.0 (Jan 2026), "first investment-grade GPU-backed financing, secured by HPC infrastructure + associated customer contract" — [pq-cybarg bubble-map](https://pq-cybarg.github.io/bubble-map/r-fin-coreweave-oracle.html) (secondary)
- Blackstone-led ~$7.5B facility May 2024 with Magnetar co-leading — [ABF Journal](https://www.abfjournal.com/magnetar-and-blackstone-provide-7-5b-in-debt-financing-facility-for-coreweave/)
- Lambda $926M senior secured Term Loan B (Sept 2026), Baa2 by Moody's, backed by GPU servers and cash flows for an investment-grade customer; $1B senior secured facility May 2026 — [StorageNewsletter](https://www.storagenewsletter.com/2026/09/22/lambda-closes-926-million-senior-secured-term-loan-b-facility-backing-gpu-deployment-for-an-investment-grade-customer/)
- First GPU-backed ABS ~$1.1B shelf in early 2025, AAA notes inside ~110 bps — [pq-cybarg](https://pq-cybarg.github.io/bubble-map/r-fin-coreweave-oracle.html) (secondary)
- NexGen Cloud: $34M 3-year non-recourse facility (June 2026) secured by GPUs and contracted cash flows — [Capacity](https://capacityglobal.com/?p=10010896) (indicative of small-operator deal size)
- Nvidia guaranteed $6.3B of CoreWeave unsold capacity through 2032; CoreWeave from 1 Jul 2026 offers to rent back unused capacity from neocloud partners at fixed rates — [Capacity](https://capacityglobal.com/news/nvidia-now-agrees-to-rent-back-unused-gpu-capacity-from-neocloud-operators-if-customer-demand-falls-short/)
- The Information (via aiweekly): industry execs expect only 7–10 of hundreds of neoclouds to survive; Nvidia backstops ~$20B in leases — [aiweekly](https://aiweekly.co/alerts/information-industry-execs-see-only-7-10-of-hundreds-of-neoclouds-surviving-as)
- Hut 8 River Bend: 85% loan-to-cost expected — [Hut 8 PR](https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion)
- Nebius: ~70% of Q2 2026 deals had customer prepayments covering 50–60% of associated capex; $4.34B converts (Mar 2026; 1.25% due 2031, 2.63% due 2033 per secondary) — [Nebius 6-K](https://www.sec.gov/Archives/edgar/data/0001513845/000110465926094568/tm2622968d1_ex99-2.htm); [TIKR](https://www.tikr.com/blog/nebius-stock-analysis-the-margin-miracle-with-a-250-billion-catch)
- IREN: $3.7B convertible notes across five series; TeraWulf: $5.7B total debt (converts + senior secured at compute sub) — [Yahoo/WULF bull case](https://finance.yahoo.com/news/terawulf-inc-wulf-bull-case-153523052.html)
- Cipher upsized private offering to $1.1B after Fluidstack deal (26 Sep 2025) — [The Block](https://www.theblock.co/news/business/2025-09-26-bitcoin-miner-cipher-upsizes-private-offering-to-1-billion-372511)

**Micro-cap financing**
- DGXX: H1 2026 ATM sold 27.95M shares for $163.2M gross (avg ≈ $5.84/share, kendi hesabım); +2.85M shares for $11.3M after quarter-end; cash $128.1M at 30 Jun 2026, no loans payable; operating cash burn −$10.6M (6 mo); prospectus supplement 8 May 2026 covers up to $175M of shares — [DGXX 10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- AIB: $55M public offering priced 5 Jun 2026 at $1.65/share (discount to $2.05 last sale on 4 Jun) — [Chartmill/GlobeNewswire](https://www.chartmill.com/news/external/34386/globenews-2026-6-5-blockchain-announces-pricing-of-55-million-public-offering-of-common-stock); listed via reverse merger with Signing Day Sports, trading on NYSE American from 17 Mar 2026 — [BriefGlance](https://briefglance.com/articles/blockchain-inc-debuts-on-nyse-fusing-ai-infrastructure-and-sports-tech); Nebius deal to be funded by customer prepayments + project-level debt + preferred equity "to limit potential shareholder dilution" — [AIB 8-K](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105865/ea030737801ex99-1.htm)
- Soluna Q2 2026: raised $159.4M equity in the quarter + $23.6M ATM after quarter-end; cash $113.4M, debt $33.1M; revenue $15.1M, net loss $22.6M — [The Energy Mag](https://www.theenergymag.com/news/market-news/soluna-holdings-reports-q2-2026-financial-results-and-debt-prepayment-agreement); [TipRanks](https://www.tipranks.com/news/company-announcements/soluna-posts-strong-q2-growth-amid-ai-pivot)
- Sphere 3D: $5.0M private placement after 90-day strategic review, divesting non-core assets to fund AI/HPC — [wallstreet-online](https://www.wallstreet-online.de/nachricht/21352118-sphere-3d-corp-concludes-90-day-strategic-review-announces-pricing-of-5-0-million-private-placement-and-divests-non-core-assets-to-fund-ai-and-high-performance-computing-development)

**Share-count growth (SEC XBRL dei:EntityCommonStockSharesOutstanding, cover-page dates; fetched 4 Nov 2026 from data.sec.gov companyconcept API)**
| Ticker | Early 2024 count (date) | Latest count (date) | Change | Note |
|---|---|---|---|---|
| APLD | 122.0M (10 Jan 2024) | 302.4M (6 Oct 2026) | +148% | |
| WULF | 302.2M (15 Mar 2024) | 499.0M (31 Jul 2026) | +65% | + $5.7B debt |
| CIFR | 296.5M (4 Mar 2024) | 456.4M (30 Oct 2026) | +54% | |
| CORZ | 177.6M (7 Mar 2024, post-Ch.11) | 321.3M (23 Jul 2026) | +81% | |
| HUT | 89.2M (27 Mar 2024) | 123.3M (31 Jul 2026) | +38% | |
| BTDR | 112.0M (31 Dec 2023) | 235.6M (31 Dec 2025) | +110% | FPI, annual only |
| IREN | 283.5M (31 Oct 2025) | 357.4M (30 Apr 2026) | +26% in 6 mo | FPI; earlier data not in API |
| DGXX | 33.0M (31 Dec 2024) | 101.4M (14 Aug 2026) | +207% | |
| AIB | 37.6M (30 Mar 2026) | 76.0M (13 Aug 2026) | +102% in 5 mo | |
| SLNH | 2.84M (28 Mar 2024; after 1:25 split Oct 2023) | 244.6M (10 Aug 2026) | ×86 | |
| MIGI/BGDE | 16.6M (26 Mar 2024) | 5.66M (7 Aug 2026) after ~1:5 reverse split (22.9M Nov 2025 → 5.49M Mar 2026) | ≈ +70% split-adjusted (tahmin) | delist notice Apr 2026 |
| GREE | n/a | n/a | — | not in API under CIK tried |
Source: [SEC XBRL companyconcept API](https://data.sec.gov/api/xbrl/companyconcept/CIK0001854368/dei/EntityCommonStockSharesOutstanding.json) (substitute CIK per company; CIKs: APLD 1144879, WULF 1083301, CIFR 1819989, CORZ 1839341, DGXX 1854368, SLNH 64463, MIGI 1218683, HUT 1964789, IREN 1878848, AIB 2070542, BTDR 1899123).

### Inferences
- IG-grade GPU debt (SOFR+225, 85% LTC) is a function of the tenant's rating, not the landlord's; a $100–250M company with a non-IG tenant should expect 60–70% LTV at 8–12% (secondary estimates) or must bring a Google/Nvidia-style backstop.
- Every micro-cap in the sample that announced an AI contract in 2025–26 followed it within weeks with an ATM or discounted offering (DGXX $175M shelf 4 days after the Cerebras signing; AIB $55M at a discount 11 weeks after listing; Soluna $159M in one quarter).
- Nebius-style prepayments (50–60% of capex) are the one mechanism that can replace equity for a micro-cap; AIB says it will use them, DGXX's 10-Q shows no Cerebras prepayment.

### Gaps
- No 2026 term sheets from Blackstone/Magnetar found; rate figures for small operators are secondary.
- IREN and BTDR share counts before late 2025 not available from the API (foreign private issuers).
- GREE and HIVE share counts not retrieved.

---

## Key Question 4 — Customer concentration and counterparty risk: Cerebras and Nebius as counterparties for DGXX and AIB

### Takeaway
No public default on a GPU-backed neocloud loan or a listed-landlord lease was found as of Oct 2026, but the sample's big leases were only financeable because Google backstopped Fluidstack ($1.73B at Cipher, $3.2B at TeraWulf, full base term at Hut 8); Cerebras (post-IPO, $3.3B cash Q1 2026, revenue ~$180–210M/quarter, historically 86% of 2025 revenue from two UAE-linked parties) and Nebius ($8–9B cash, $4.3B+ converts, $20–25B 2026 capex, ~80% of its 5 GW funding unsecured) are both mid-grade counterparties whose contracts carry no third-party backstop for DGXX or AIB.

### Cited Findings
**Backstop structures (what a creditworthy pyramid looks like)**
- TeraWulf–Fluidstack: Google backstopped $1.8B of Fluidstack lease obligations for warrants on ~41M WULF shares (~8%), later $3.2B for ~73M shares (~14%); warrant exercise price $0.01; on Fluidstack payment default or insolvency Google may pay the termination fee or assume the lease; "not a guarantee of TeraWulf's corporate debt" — [The Block](https://www.theblock.co/post/366959/bitcoin-miner-terawulf-shares-jump-50-after-google-secures-8-stake-as-part-of-3-7-billion-10-year-ai-compute-deal); [WULF 8-K](https://investors.terawulf.com/sec-filings/all-sec-filings/content/0001104659-25-078084/tm2523008d2_8k.htm); [Cointelegraph](https://regional-front.cointelegraph.com/news/google-largest-shareholder-terawulf-ai-data-center-fluidstack)
- Cipher–Fluidstack: Google backstop $1.4B for ~24M warrant shares (~5.4%), raised to $1.73B with the 39 MW expansion (Nov 2025) — [Cipher 8-K exhibit](https://www.sec.gov/Archives/edgar/data/1819989/000095010325012168/dp234624_ex9901.htm); [DCD](https://www.datacenterdynamics.com/en/news/fluidstack-signs-additional-39mw-lease-with-cipher-mining-in-texas-backed-by-google/)
- Hut 8–Fluidstack: Google guarantees lease payments and certain pass-throughs for the 15-year base term; Google neither leases nor operates — [Hut 8 PR](https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion)
- In most neocloud financings the customer contract is the repayment source, so lenders read the buyer's credit and termination rights first; reserved contracts usually take-or-pay; "no public default or foreclosure on a GPU-backed neocloud loan as of October 2026"; nearest precedents: 2022 bitcoin-miner equipment loans and AI customers that stopped paying for compute — [amcompute largest GPU loans](https://www.amcompute.com/gpu-debt/largest-gpu-loans)
- Historical "customer stopped paying" case: Stability AI (2024) ran ~$99M/yr of rented compute from AWS, GCP and CoreWeave and fell behind on bills — [Slashdot/The Register](https://slashdot.org/story/24/04/03/228209/stability-ai-reportedly-ran-out-of-cash-to-pay-its-bills-for-rented-cloud-gpus); [The Deep Dive](https://thedeepdive.ca/stability-ai-isnt-very-stable-defaults-on-aws-and-google-cloud-payments)
- Applied Digital's own GPU-cloud unit: board approved sale in April 2025 after revenue drop blamed on shift to multi-tenant on-demand GPU model with technical problems; FY2025 discontinued ops revenue ~$84.4M; Dec 2025 non-binding term sheet to combine with EKSO Bionics — [APLD 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1144879/000114487925000021/apld-20250531.htm); [Fidelity/CoinDesk](https://fidelity.com/news/article/technology/202504151111COINDESKCRYPTONW_a4baa256-54e1-47a4-a829-e1be24ccd6e2)
- CoreWeave concentration: "a meaningful demand reduction from any anchor customer could stress ability to service debt" — [Roundhill](https://blog.roundhillinvestments.com/neocloud-companies-explained)

**Cerebras (CBRS) as counterparty**
- IPO priced 14 May 2026 at $185 (above range), raised ~$5.5B, valuation ~$40B at pricing, +108% day one (~$66B) — [TechCrunch](https://techcrunch.com/2026/05/14/cerebras-raises-5-5b-kicking-off-2026s-ipo-season-with-a-bang); [Dealroom](https://dealroom.co/news/128936-cerebras-raises-5-55b-in-biggest-us-ipo-of-2026/); earlier $23B / $26.6B valuation targets in filings — [Pulse.bot](https://www.pulse.bot/investment-banking/news/cerebras-systems-launches-35-b-ipo-at-115125-per-share-targeting-266-b-valuation-e791acc1-68d0-48e9-8b5d-2fac7701dd9c/)
- Q1 2026: GAAP revenue $193.4M (+94% YoY), net loss $14.0M, cash + ST investments $3.3B — [Cerebras 8-K](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026044941/cbrsannouncesfinancialresu.htm)
- Q2 2026: "core" revenue $210M, GAAP ~$180M (below $194M est.), net loss $450.5M (SBC $386.6M), cloud revenue $126M, hardware $54M; RPO $25.4B; Q3 core revenue guide $214–216M — [Cerebras 8-K Q2](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026056186/cbrsannouncesfinancialresu.htm); [sec-api.io](https://sec-api.io/insights/cerebras-cbrs-first-public-quarters); [Webull](https://www.webull.com/news/15399426605589504)
- Concentration (per S-1 via secondary): ~86% of 2025 revenue from G42 (24%) and MBZUAI (62%), related parties; 2026 main names OpenAI and AWS — [INDmoney](https://www.indmoney.com/blog/us-stocks/cerebras-stock-cbrs-earnings-valuation-analysis)
- DGXX contract: $1.1B initial term, up to $2.5B with renewals, Cerebras expansion option +$1.4B; Phase 1 self-funded by DGXX; Phase 2 "conditional" — [Yahoo](https://finance.yahoo.com/sectors/technology/articles/digi-power-x-secures-1-132900027.html); [DGXX 10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)

**Nebius (NBIS) as counterparty**
- Q2 2026: cash ~$8B; capex $5.7B in the quarter; 2026 capex guidance raised to $20–25B; ATM $2.8B; converts $4.34B (Mar 2026) plus proposed $4.5B (Aug 2026, closing not confirmed); FCF ≈ −$3.41B in Q2 (TIKR); management "secured only ~20% of ~$250B needed for 5 GW pipeline" (secondary) — [Nebius 6-K](https://www.sec.gov/Archives/edgar/data/0001513845/000110465926094568/tm2622968d1_ex99-2.htm); [TIKR](https://www.tikr.com/blog/nebius-stock-analysis-the-margin-miracle-with-a-250-billion-catch); [TIKR Q1](https://www.tikr.com/blog/nebius-grew-revenue-684-in-q1-sold-out-its-entire-capacity-and-raised-its-capex-target-to-25-billion)
- Nebius itself depends on Microsoft and Meta: all Microsoft tranches delivered; second Meta agreement online early 2027; customer commitments >$40B; $2B NVIDIA equity investment — same 6-K; [TIKR](https://www.tikr.com/blog/nebius-stock-analysis-the-margin-miracle-with-a-250-billion-catch)
- AIB contract: 50 MW, 12-year initial term, two 5-year renewals, value undisclosed, Nebius prepayments (amounts undisclosed, escrowed) — [AIB 8-K](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105865/ea030737801ex99-1.htm)
- Market reaction: AIB closed $1.71 on 29 Sep 2026, $1.33 on 30 Sep (announcement day, −22%), $0.87 on 3 Nov 2026 — [stockanalysis AIB history](https://stockanalysis.com/stocks/aib/history/)

### Inferences
- Cerebras is a far better counterparty than a seed-stage AI startup (listed, ~$3B+ cash post-IPO, $25B RPO) but still a loss-making, two-customer-concentrated hardware vendor; its DGXX lease has no third-party backstop and Phase 2 is explicitly conditional — so DGXX's financeable capacity is 15 MW, not 40, until Phase 2 is firmed.
- Nebius is investment-grade-adjacent on cash but is funding a $20–25B/yr capex plan on converts, ATMs and prepayments; a 50 MW AIB lease is <1% of Nebius's 5 GW target, so Nebius will prioritize or drop it based on its own financing conditions. AIB's own disclosure that prepayments are "escrowed" is a positive, but amounts are unknown.
- The fact that the market marked AIB down 22% on the day of a 12-year 50 MW Nebius lease signals investors price the equity-funding gap and counterparty terms ahead of the headline value.

### Gaps
- No Nebius net loss / total debt figure in the 6-K letter; no rating-agency opinion on Cerebras or Nebius found.
- AIB–Nebius contract value and prepayment amounts are undisclosed.
- No identified case of a listed landlord's AI tenant defaulting (searched; none found) — absence of evidence, not evidence of safety; most leases have not yet commenced.

---

## Key Question 5 — Outcome base rates for small caps that announced AI/HPC contracts 2023–25

### Takeaway
Among 14 identifiable cases, no company that was $50–300M at announcement is up 10x per share by 4 Nov 2026; the 10x+ market-cap winners (IREN, WULF, CIFR, APLD, CORZ) reached it from 2022 crypto-winter lows and were already $0.6–3.9B when their AI contracts were signed, and their per-share gains since announcement are 1.5–4x after 38–148% dilution; micro-cap announcers (SLNH, MIGI, ANY, DGXX, AIB) are down 50–97% per share from their post-announcement highs or ATM prices.

### Cited Findings
Market caps: year-end values and 3 Nov 2026 values from stockanalysis.com market-cap pages (fetched 4 Nov 2026); shares from SEC XBRL (Q3 table). Per-share proxy = market cap ÷ cover-page share count nearest that date (kendi hesabım, ±10%).

| Company | AI/HPC announcement (date) | Mkt cap YE2022 | Mkt cap ~announcement | Mkt cap 3 Nov 2026 | Mkt-cap multiple from YE2022 | Per-share since announcement (tahmin) |
|---|---|---|---|---|---|---|
| IREN | Microsoft $9.7B, 3 Nov 2025 | $68.7M | $12.4B (YE2025) | $9.64B | 140x | −22% (mkt cap; shares +26% → ≈ −38% per share) |
| WULF | Fluidstack/Google, Aug 2025 | $96.8M | $2.18B (YE2024) → $4.81B (YE2025) | $6.25B | 65x | ≈ $5.65 (YE2024) → $12.53 = 2.2x |
| CIFR | Fluidstack/Google, Sep 2025 | $138.6M | $1.61B (YE2024); $5.83B (YE2025) | $3.37B | 24x | ≈ $4.63 (YE2024) → $8.12 = 1.75x; −42% from YE2025 |
| APLD | CoreWeave leases, Jun 2025 | $173.4M | $1.65B (YE2024); $6.86B (YE2025) | $5.39B | 31x | ≈ $7.40 (YE2024) → $17.81 = 2.4x; −21% from YE2025 |
| CORZ | CoreWeave 12-yr, Jun 2024 | n/a (Ch.11) | $606M (24 Jan 2024) | $4.58B | 7.6x from Jan 2024 | ≈ $3.41 → $14.24 = 4.2x |
| HUT | Fluidstack/Google, Dec 2025 | $63.6M | $3.92B (YE2024); $2.65B (YE2025) | $1.88B | 30x | ≈ $41.9 (YE2024)… NOTE stockanalysis HUT page shows $1.88B/ $6.92 — see gap; BTDR row below |
| BTDR | AI/HPC pivot 2024–25 | n/a (listed Apr 2023) | $1.19B (YE2023) | $7.86B | 6.6x from YE2023 | ≈ $10.6 (YE2023) → $63.75 = 6.0x |
| HIVE | HPC/GPU 2023–25 | $118.7M | $338M (YE2024) | $498M | 4.2x | n/a (shares not retrieved) |
| GREE | AI/HPC pivot 2024–25 | $12.9M | $17.7M (YE2024) | $42.0M | 3.3x | n/a (heavy dilution; shares not retrieved) |
| SLNH | modular AI/HPC 2024–26 | $4.6M | $17.6M (YE2024) | $138.9M | 30x (mkt cap) | shares 8.37M (Nov 2024) → 244.6M: per share ≈ $2.10 → $0.57 = −73% |
| MIGI/BGDE | 20 MW AI colocation 2024 | $18.8M | $15.6M (YE2024) | $17.8M | ~1x | ≈ −60% split-adjusted; delist notice |
| ANY (Sphere 3D) | AI/HPC pivot 2025–26 | n/a | n/a | n/a | — | going-concern doubt Q2 2026; high $5.65 on 3 Jun 2026 |
| DGXX | Cerebras $1.1B, 4 May 2026 | $10.3M | $168M (YE2025); ATM avg $5.84 in H1 2026 | $231.7M | 23x | $2.41 (YE2025) → $2.27 = −6%; ≈ −61% vs H1-2026 ATM avg; $4.10 (30 Sep) → $2.27 = −45% |
| AIB | Nebius 50 MW, 30 Sep 2026 | n/a (listed Mar 2026) | $1.71 × 37.6–76M sh ≈ $65–130M | $66.1M | — | $1.71 → $0.87 = −49% in 5 weeks; 52-wk high $17.25 → −95% |

Row sources: [APLD](https://stockanalysis.com/stocks/apld/market-cap/), [WULF](https://stockanalysis.com/stocks/wulf/market-cap/), [CIFR](https://stockanalysis.com/stocks/cifr/market-cap/), [IREN](https://stockanalysis.com/stocks/iren/market-cap/), [CORZ](https://stockanalysis.com/stocks/corz/market-cap/), [HUT](https://stockanalysis.com/stocks/hut/market-cap/), [BTDR](https://stockanalysis.com/stocks/btdr/market-cap/), [SLNH](https://stockanalysis.com/stocks/slnh/market-cap/), [MIGI](https://stockanalysis.com/stocks/migi/market-cap/), [GREE](https://stockanalysis.com/stocks/gree/market-cap/), [HIVE](https://stockanalysis.com/stocks/hive/market-cap/), [DGXX](https://stockanalysis.com/stocks/dgxx/market-cap/), [DGXX history](https://stockanalysis.com/stocks/dgxx/history/), [AIB](https://stockanalysis.com/stocks/aib/), [AIB history](https://stockanalysis.com/stocks/aib/history/); announcement dates: [IREN 8-K via Pulse2](https://pulse2.com/iren-secures-9-7-billion-ai-cloud-contract-with-microsoft/amp/), [WULF](https://www.theblock.co/post/366959/bitcoin-miner-terawulf-shares-jump-50-after-google-secures-8-stake-as-part-of-3-7-billion-10-year-ai-compute-deal), [CIFR](https://www.sec.gov/Archives/edgar/data/1819989/000095010325012168/dp234624_ex9901.htm), [HUT](https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion), [DGXX](https://www.datacenterdynamics.com/en/news/cerebras-signs-on-for-40mw-of-capacity-at-digi-power-x-data-center-in-alabama/), [AIB](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105865/ea030737801ex99-1.htm), [Sphere 3D](https://www.panabee.com/news/sphere-3d-earnings-q2-2026), [Mawson](https://www.panabee.com/news/mawson-fails-1-00-bid-price-rule-faces-nasdaq-delisting-hearing).

Correction to HUT row: stockanalysis HUT market-cap page gives $1.88B at $6.92 on 3 Nov 2026 and YE2024 $3.19B, YE2025 $2.65B, one-year change −60%; and BTDR page gives $7.86B at $63.75 with YE2024 $1.92B. The HUT/BTDR figures above should be read as: **HUT: YE2022 $63.6M → YE2024 $3.19B → YE2025 $2.65B → $1.88B now (−60% 1-yr; per share ≈ $34 YE2024 → $6.92?)** — these two pages' outputs may be mis-labelled (the $63.75 price and 123M implied shares match Hut 8's share count, while $6.92/272M shares match Bitdeer's profile). Treat the HUT and BTDR market-cap rows as swapped-uncertain; verify directly before use. (Gap recorded below.)

Other dated facts for the base-rate table
- Miners with secured HPC contracts trade at 12.3x NTM sales vs 5.9x for pure-play miners (S&P Global, Feb 2026) — [S&P Global](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/02/bitcoin-miners-pivot-to-ai-and-hpc-as-cryptocurrency-market-slumps)
- Five miners (WULF, CIFR, CORZ, HUT, Bitfarms) collectively signed >$30B in long-term AI/HPC agreements (CoinShares via VALR) — [VALR](https://blog.valr.com/blog/from-bitcoin-hashing-to-ai-computing-how-former-miners-are-repurposing-infrastructure-in-2026)
- Core Scientific shareholders rejected CoreWeave's ~$9B all-stock takeover on 30 Oct 2025 (proxy advisers and a large holder said it undervalued the company); stock +5% on rejection — [Bloomberg](https://www.bloomberg.com/news/articles/2025-10-30/core-scientific-investors-spurn-coreweave-takeover-bid-in-vote); [BusinessWire](https://www.businesswire.com/news/home/20251030641010/en/Core-Scientific-Announces-Termination-of-Merger-Agreement-with-CoreWeave)

### Inferences
- Tally (per share, since the AI announcement, n=12 with data): ≥10x: 0; 3–10x: 2 (CORZ ~4.2x since Jan 2024; BTDR ~6x from YE2023 if the BTDR row is correct); 1.5–3x: 3 (APLD, WULF, CIFR from YE2024); flat/−40%: 2 (IREN, DGXX vs YE2025); down >50%: 5 (SLNH, MIGI, ANY, AIB, DGXX vs ATM price). The 10x market-cap moves happened before the contracts, from distressed 2022 valuations.
- The winners shared four traits absent in the $100–250M group: (1) hundreds of MW of already-energized power from mining, (2) an IG-grade or Google-backstopped tenant, (3) access to $1B+ converts rather than ATMs, (4) a market cap already ≥$500M so that $100–300M raises were not >100% dilutive.
- For a micro-cap, market-cap growth and per-share growth decouple: SLNH market cap 8x (YE2024→now) while the share price fell ~73%.

### Gaps
- HUT vs BTDR market-cap rows possibly swapped in the fetch output; needs direct verification.
- GREE, HIVE, ANY, Gryphon, LM Funding: no share-count or dated-announcement data retrieved; Gryphon/LMFA not covered.
- Prices exactly on announcement dates were not pulled (only year-end caps and share counts); per-share returns are ±10–20% estimates.
- Jay Ritter small-IPO outcome data: not retrieved (AIB is a reverse-merger, not an IPO; Ritter data less applicable).

---

## Key Question 6 — The "10x math" template: what a $1–2B valuation requires at peer multiples, and the implied dilution

### Takeaway
At today's multiples a $1.5B EV needs roughly 115–185 MW of contracted (not planned) colocation capacity at the mid/large-peer $8–13M EV/MW, or ~45–75 MW energized at 18–20x EBITDA; that is $1.2–3.7B of construction capex, which at 60–85% debt means $180M–$1.5B of new equity against a $100–250M market cap — i.e. 1–6x the current share count unless prepayments/backstops replace equity.

### Cited Findings
**Multiples (dated)**
- Windsor Drake, priced 18 Sep 2026, TTM revenue, EV incl. leases: EV/Revenue — TeraWulf 67.2x, Cipher ~60x, Digital Realty 12.9x; layer medians: neocloud/GPU cloud 28.8x, accelerator silicon 21.9x, data-centre owners 18.8x, power/cooling equipment 5.0x; range across 27 names 2.7x–67.2x. EV per MW of contracted critical IT (30 Jun 2026 disclosures): Applied Digital $8.2M, TeraWulf $13.2M, Digital Realty $28.0M; EV per energised MW: Digital Realty $31.0M, TeraWulf $137.0M — [Windsor Drake Q3 2026](https://windsordrake.com/market-intelligence/reports/ai-infrastructure-valuations-q3-2026)
- M&A exits: Tier-1 AI-capable facilities $3.1–3.8M per MW at 18.2–20.1x EBITDA; traditional enterprise colo $1.4–1.8M/MW at 12.3–14.6x EBITDA (11 Aug 2026) — [datacentres.com](https://www.datacentres.com/news/data-centre-m-a-reaches-187b-peak-as-hyperscalers-consolidate-ai-infrastructure-slot1-2026-08-11); CyrusOne deal $26.8M/MW, 34% premium to $20.1M/MW listed-REIT VWAP (9 Jun 2026) — [datacentres.com](https://www.datacentres.com/news/data-centre-m-a-reaches-187b-in-2026-as-hyperscalers-fuel-consolidation-wave-slot1-2026-06-09) (the two datacentres.com bases are inconsistent; the $3.1–3.8M figure may be per gross MW or per-MW of EBITDA-bearing older assets — flag)
- Listed data center operators trade at ~10.8x Needham discounted 2028E EV/EBITDA vs 15–20x viewed appropriate over the prior 12–18 months — [SitusAMC](https://www.situsamc.com/resources-insights/articles/data-centers-ai-driven-era-key-trends-reshaping-valuation)
- Private platform deals 20–30x EV/EBITDA (advisory marketing piece) — [CT Acquisitions](https://www.ctacquisitions.com/how-to-sell-a-data-center-business/)
- Miners with HPC contracts 12.3x NTM sales (Feb 2026) — [S&P Global](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/02/bitcoin-miners-pivot-to-ai-and-hpc-as-cryptocurrency-market-slumps)
- "Contracted MW capacity drives valuation, not nameplate MW" — [Blockspace](https://blockspace.media/insight/ai-data-center-lease-valuation-2026/)

**What the market currently pays the micro-caps (kendi hesabım from the above)**
- DGXX: market cap $231.7M (3 Nov 2026), cash $128M, no debt (30 Jun 2026) → EV ≈ $105–110M against 40 MW contracted (15 MW firm) → ≈ $2.7M EV/MW contracted (≈ $7M per firm MW).
- AIB: market cap $66M, cash $52.8M (Q2 2026, per headline) → EV ≈ $15–20M against 50 MW Nebius lease → ≈ $0.3–0.4M EV/MW contracted; against 120 MW contracted power ≈ $0.15M/MW.
- Compare APLD $8.2M and WULF $13.2M EV/MW contracted: the micro-cap discount is 3–30x, which is the market's price for execution + financing risk.

**Template arithmetic (kendi hesabım; inputs cited above)**
Path A — Colocation landlord
- Revenue $1.8–2.3M/MW/yr; triple-net NOI ≈ 90–98% (Hut 8: $6.9B NOI on $7.0B rent).
- $1.5B EV at 18–20x EBITDA → ~$75–83M EBITDA → ~35–45 MW energized and billing at $2.0M/MW NOI; at public ~11x (Needham) → ~$135M EBITDA → ~65–75 MW.
- At the contracted-MW multiple ($8–13M/MW) → 115–185 MW of signed, financeable leases.
- Capex: AI-ready shell $15–25M/MW → 45 MW = $0.7–1.1B; 150 MW = $2.3–3.8B.
- Equity at 85% LTC (Google-backstopped) → $100–170M for 45 MW; at 65% LTV (non-IG tenant) → $240–390M for 45 MW; for 150 MW: $340–570M (85% LTC) to $0.8–1.3B (65%).
- Against a $150M market cap, that is +70% to +900% share-count growth unless prepayments (Nebius-style 50–60% of capex) or preferred equity carry the gap. Dilution-adjusted, a 10x market-cap outcome becomes 1.5–5x per share — matching the APLD/WULF/CIFR observed 1.75–2.4x since YE2024 despite 24–31x market-cap moves from 2022.

Path B — GPU-as-a-service
- Revenue ~$9.7–12M/MW/yr (IREN–MSFT; SemiAnalysis); EBITDA margin 40–60% (Nebius, CoreWeave) → $4–7M EBITDA/MW.
- $1.5B EV at ~6x forward contracted revenue (IREN: ~$12B+ EV on $1.94B/yr contract run-rate, kendi hesabım) → $250M/yr revenue → ~25 MW of GB300 → GPU capex ~$29–40M/MW → $0.7–1.0B of GPUs plus $0.4–0.6B of liquid-cooled halls.
- Equity at 30–40% (60–70% LTV) → $330–640M; against $150M market cap → 2–4x share count; and the asset re-prices with rental rates (±40% in 12 months) and a 3–6-year life.
- Nebius's own case: $0.58B quarterly revenue, $5.7B quarterly capex → each $1 of annualized revenue needs ~$2.5 of capex in the ramp year (6-K).

Time: 45 MW energized needs 10–14 months post-signing if power is at the fence (AIB, DGXX guidance) or 2–4 years if a substation is required (160-week transformers; PJM 7 years).

### Inferences
- A $1–2B valuation for a $100–250M company within 1–3 years is arithmetically possible only through Path A with ≥100 MW contracted to a backstopped/IG tenant and prepayment-heavy funding; Path B at micro-cap scale implies 2–4x dilution before the first GPU is energized and leaves the equity exposed to GPU price deflation.
- Per-share 10x has not occurred in this cohort since any 2024–26 contract announcement; the realistic upside case in comparable names is 2–4x per share, and the modal micro-cap outcome has been dilution and a lower share price.

### Gaps
- No primary EV/MW multiple for IREN, CORZ, HUT or Nebius from Windsor Drake; the IREN forward multiple is my estimate.
- No bank/sell-side NAV-per-MW models retrieved.
- AIB cash is from a news headline, not the 10-Q.

---

## Key Question 7 — Do small neoclouds convert backlog into cash and shareholder value, or into dilution?

### Takeaway
In the 2024–26 cohort, backlog converted into revenue and market cap at the mid/large miners (CORZ billing 437 MW ≈ $635M annualized; APLD 175 MW live) but into dilution at every micro-cap examined (SLNH ×86 shares, DGXX +207%, AIB +102% in five months, MIGI reverse split + delist notice, ANY going-concern).

### Cited Findings
- CORZ: billing 437 MW ≈ $635M annualized colocation revenue by mid-July 2026; adj. EBITDA $41.1M in Q2 2026 — [CORZ 8-K](https://www.sec.gov/Archives/edgar/data/0001839341/000183934126000013/q22026corescientificinc-ea.htm); shares +81% since Mar 2024 (SEC XBRL)
- APLD: 175 MW live Jul 2026, 400 MW contracted; FY2026 (May) revenue $611M, net loss −$250M; TTM (Aug 2026) revenue $872M, net loss −$469M — [stockanalysis APLD financials](https://stockanalysis.com/stocks/apld/financials/); shares +148% since Jan 2024 (SEC XBRL)
- WULF: FY2025 revenue $168M, net loss −$661M; TTM Jun 2026 net loss −$1.95B — [stockanalysis WULF financials](https://stockanalysis.com/stocks/wulf/financials/); CIFR TTM Sep 2026 revenue $146M, net loss −$1.08B — [stockanalysis CIFR](https://stockanalysis.com/stocks/cifr/financials/); IREN FY2026 (Jun) revenue $707M, net loss −$703M — [stockanalysis IREN](https://stockanalysis.com/stocks/iren/financials/) (losses largely non-cash warrant/convert marks per CORZ 8-K; not verified for others)
- SLNH: revenue $15.1M Q2 2026 (+145%), net loss −$22.6M, $183M equity raised in ~4 months — [Energy Mag](https://www.theenergymag.com/news/market-news/soluna-holdings-reports-q2-2026-financial-results-and-debt-prepayment-agreement); shares 2.84M → 244.6M (SEC XBRL)
- DGXX: TTM revenue $31.4M, net loss −$36.0M; $163M ATM at ≈$5.84 avg; price $2.27 on 3 Nov 2026 — [stockanalysis DGXX](https://stockanalysis.com/stocks/dgxx/financials/); [DGXX 10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm); [DGXX history](https://stockanalysis.com/stocks/dgxx/history/)
- AIB: TTM revenue $17.1M (−12.8%), net loss −$4.5M, 52-week range $0.81–17.25 — [stockanalysis AIB](https://stockanalysis.com/stocks/aib/)

### Inferences
- Backlog is converted to cash only at Ready-for-Service; every quarter before that is funded by equity at micro-cap scale. The cohort shows no case where a $100–250M company financed >15 MW without >100% share-count growth.

### Gaps
- No micro-cap in the cohort has yet reached rent commencement on its 2026 AI contract (DGXX Dec 2026 target; AIB mid-2027), so "conversion" for DGXX/AIB is not yet observable.

---

## Key Question 8 — Which single risk has most often killed the thesis in comparable small caps?

### Takeaway
For the $20–250M group the killer has been equity financing (ATMs/reverse splits at falling prices) rather than customer default or GPU deflation; for the $1B+ group the thesis-damaging events were delivery slippage (Core Scientific/Denton → CoreWeave guidance cut, lawsuits) and exposure to GPU repricing (APLD exited its own GPU cloud); no public AI-tenant default on a listed landlord has yet occurred.

### Cited Findings
- Financing/dilution: SLNH ×86 shares, DGXX +207%, AIB +102%, MIGI reverse split and Nasdaq delist determination 17 Apr 2026 on stockholders' equity <$2.5M — SEC XBRL; [Panabee](https://www.panabee.com/news/mawson-infrastructure-rebrands-to-big-digital-energy-amid-nasdaq-delisting-defense); ANY going-concern — [Panabee](https://www.panabee.com/news/sphere-3d-earnings-q2-2026)
- Delivery delay: CoreWeave 2025 guidance cut 10 Nov 2025 due to third-party developer power-shell delay; class actions Jan 2026 citing $14B market-cap loss — [Barchart/Hagens Berman](https://www.barchart.com/story/news/37083576/coreweave-inc-crwv-slapped-with-securities-class-action-amid-questions-over-denton-data-center-completion-transparency-14-billion-market-cap-loss-hagens-berman)
- GPU price deflation: H100 1-yr contract rate to ~$1.70/h Oct 2025 (secondary); APLD sold its GPU cloud unit after a revenue drop from the multi-tenant on-demand model (Apr 2025) — [Fidelity/CoinDesk](https://fidelity.com/news/article/technology/202504151111COINDESKCRYPTONW_a4baa256-54e1-47a4-a829-e1be24ccd6e2)
- Customer default: none public on GPU-backed neocloud loans as of Oct 2026 — [amcompute](https://www.amcompute.com/gpu-debt/largest-gpu-loans); Stability AI 2024 arrears is the cited precedent — [Slashdot](https://slashdot.org/story/24/04/03/228209/stability-ai-reportedly-ran-out-of-cash-to-pay-its-bills-for-rented-cloud-gpus)
- Counterparty fragility managed via Google backstops at WULF/CIFR/HUT — Q4 sources above; The Information: only 7–10 of hundreds of neoclouds expected to survive — [aiweekly](https://aiweekly.co/alerts/information-industry-execs-see-only-7-10-of-hundreds-of-neoclouds-surviving-as)

### Inferences
- Ranking by observed frequency in this cohort: (1) dilution/financing (5 of 5 micro-caps), (2) delivery delay (1 major, several minor), (3) GPU price deflation (hit GPU-renters, not landlords), (4) customer default (0 observed, but structurally the risk lenders price first). For QMLS/DGXX/AIB/VVPR the test should therefore be: cash on hand ÷ capex to Ready-for-Service, and whether the tenant contract is backstopped.

### Gaps
- QMLS and VVPR were not researched here (out of this note's assigned scope beyond sector context); no VVPR/QMLS-specific filings fetched.

---

## Source list (all accessed 4 Nov 2026)
Primary / filings
- CoreWeave Q2 2026 release — https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx
- Nebius Q2 2026 6-K shareholder letter — https://www.sec.gov/Archives/edgar/data/0001513845/000110465926094568/tm2622968d1_ex99-2.htm
- Core Scientific Q2 2026 8-K — https://www.sec.gov/Archives/edgar/data/0001839341/000183934126000013/q22026corescientificinc-ea.htm
- Digi Power X 10-Q (Q2 2026) — https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm
- AIB Data Centers 8-K ex.99.1 (30 Sep 2026) — https://www.sec.gov/Archives/edgar/data/0002070542/000121390026105865/ea030737801ex99-1.htm
- Cerebras 8-Ks (Q1, Q2 2026) — https://www.sec.gov/Archives/edgar/data/0002021728/000162828026044941/cbrsannouncesfinancialresu.htm ; https://www.sec.gov/Archives/edgar/data/0002021728/000162828026056186/cbrsannouncesfinancialresu.htm
- Cipher Mining 8-K exhibit (Fluidstack/Google) — https://www.sec.gov/Archives/edgar/data/1819989/000095010325012168/dp234624_ex9901.htm
- TeraWulf 8-K (Google warrants) — https://investors.terawulf.com/sec-filings/all-sec-filings/content/0001104659-25-078084/tm2523008d2_8k.htm ; WULF 10-Q Q2 2026 — https://www.sec.gov/Archives/edgar/data/0001083301/000108330126000166/wulf-20260630.htm ; WULF Q1 2026 8-K — https://www.sec.gov/Archives/edgar/data/0001083301/000108330126000083/a_wulfearningsreleaseq1202.htm
- Applied Digital Q1 FY2026 release — https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-25-000068/apldq126earningsrelease.htm ; FY2025 10-K — https://www.sec.gov/Archives/edgar/data/1144879/000114487925000021/apld-20250531.htm ; RFS PRs 27 Oct / 24 Nov 2025 — https://ir.applieddigital.com/news-events/press-releases/detail/133/ ; https://ir.applieddigital.com/news-events/press-releases/detail/137/
- Hut 8 River Bend PR (17 Dec 2025) — https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion
- SEC XBRL companyconcept API (shares outstanding) — https://data.sec.gov/api/xbrl/companyconcept/CIK{10-digit}/dei/EntityCommonStockSharesOutstanding.json
Industry data / analysis
- Windsor Drake AI Infrastructure Valuations Q3 2026 — https://windsordrake.com/market-intelligence/reports/ai-infrastructure-valuations-q3-2026
- Data Center Knowledge (Wood Mackenzie transformer data, PJM) 12 May 2026 — https://datacenterknowledge.com/energy-power-supply/why-ai-data-center-projects-face-years-of-delays-after-approval
- ESS News transformer lead times 12 May 2026 — https://www.ess-news.com/2026/05/12/us-transformer-market-faces-severe-supply-constraints-as-lead-times-extend-to-four-years/
- JLL/Goldman cost per MW via CoR Advisors — https://www.coradvisors.net/2026/06/ai-data-center-development-costs-2026.html
- datacentres.com M&A multiples — https://www.datacentres.com/news/data-centre-m-a-reaches-187b-peak-as-hyperscalers-consolidate-ai-infrastructure-slot1-2026-08-11 ; https://www.datacentres.com/news/data-centre-m-a-reaches-187b-in-2026-as-hyperscalers-fuel-consolidation-wave-slot1-2026-06-09
- SitusAMC (Needham multiples) — https://www.situsamc.com/resources-insights/articles/data-centers-ai-driven-era-key-trends-reshaping-valuation
- S&P Global miner pivot (Feb 2026) — https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/02/bitcoin-miners-pivot-to-ai-and-hpc-as-cryptocurrency-market-slumps
- Uvik GPU price index — https://uvik.net/blog/gpu-price-index/ ; getdeploying — https://getdeploying.com/gpu-price-trends ; Spheron — https://www.spheron.network/blog/nvidia-h100-price-2026/
- American Compute (GPU loans, H100 residuals) — https://www.amcompute.com/gpu-debt/largest-gpu-loans ; https://www.amcompute.com/appraisals/h100 ; https://www.amcompute.com/gpu-resale-index/residual-value/h100
- Wing VC "How the GPU became collateral" — https://www.wing.vc/content/how-the-gpu-became-collateral
- Lambda TLB — https://www.storagenewsletter.com/2026/09/22/lambda-closes-926-million-senior-secured-term-loan-b-facility-backing-gpu-deployment-for-an-investment-grade-customer/
- Capacity (CoreWeave debt, Nvidia/CoreWeave backstops) — https://capacityglobal.com/news/coreweaves-debt-hits-35bn/ ; https://capacityglobal.com/news/nvidia-now-agrees-to-rent-back-unused-gpu-capacity-from-neocloud-operators-if-customer-demand-falls-short/
- TIKR Nebius — https://www.tikr.com/blog/nebius-stock-analysis-the-margin-miracle-with-a-250-billion-catch
- Market caps/financials: stockanalysis.com pages listed inline (APLD, WULF, CIFR, IREN, CORZ, HUT, BTDR, SLNH, MIGI, GREE, HIVE, DGXX, AIB)
News
- CoreWeave guidance cut / Denton — https://www.streetinsider.com/Earnings/CoreWeave+flags+hit+from+data+center+delay%2C+shares+fall/25585703.html ; https://www.datacenterdynamics.com/en/news/coreweave-deploys-16000-gpus-at-delayed-data-center-in-denton-texas/
- Core Scientific merger rejection — https://www.bloomberg.com/news/articles/2025-10-30/core-scientific-investors-spurn-coreweave-takeover-bid-in-vote
- IREN–Microsoft — https://techinformed.com/microsoft-signs-9-7-billion-iren-deal-for-nvidia-gb300-capacity/
- Cerebras IPO — https://techcrunch.com/2026/05/14/cerebras-raises-5-5b-kicking-off-2026s-ipo-season-with-a-bang
- DGXX–Cerebras — https://www.datacenterdynamics.com/en/news/cerebras-signs-on-for-40mw-of-capacity-at-digi-power-x-data-center-in-alabama/
- AIB–Nebius — https://datacenterdynamics.com/en/news/nebius-signs-50mw-lease-with-aib-data-centers ; AIB offering — https://www.chartmill.com/news/external/34386/globenews-2026-6-5-blockchain-announces-pricing-of-55-million-public-offering-of-common-stock
- Mawson/BGDE delisting — https://www.panabee.com/news/mawson-infrastructure-rebrands-to-big-digital-energy-amid-nasdaq-delisting-defense
- Sphere 3D — https://www.panabee.com/news/sphere-3d-earnings-q2-2026
- Soluna Q2 2026 — https://www.theenergymag.com/news/market-news/soluna-holdings-reports-q2-2026-financial-results-and-debt-prepayment-agreement
- Depreciation debate — https://www.tomshardware.com/tech-industry/gpu-depreciation-could-be-the-next-big-crisis-coming-for-ai-hyperscalers-after-spending-billions-on-buildouts-next-gen-upgrades-may-amplify-cashflow-quirks ; https://www.nasdaq.com/articles/michael-burrys-latest-warning-could-be-bad-news-coreweave ; https://www.webull.com/news/13650205142680576
- The Information via aiweekly (neocloud survival) — https://aiweekly.co/alerts/information-industry-execs-see-only-7-10-of-hundreds-of-neoclouds-surviving-as
