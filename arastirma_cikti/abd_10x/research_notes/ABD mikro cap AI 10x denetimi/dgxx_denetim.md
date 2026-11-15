# Digi Power X (Nasdaq: DGXX; Cboe Canada: DGX) — independent audit of Cerebras contract, financing, capital structure, operations (as of 4 Nov 2026)

Source-type legend used below: **[8-K]** SEC current report (filed/furnished), **[10-Q]/[10-K]** SEC periodic report (official, audited only for 10-K), **[EX-10.1]** redacted contract filed with SEC, **[MCR]** Canadian Form 51-102F3 material change report (furnished as 8-K exhibit; it attaches the press release), **[DEF 14A]** proxy, **[S-3/A]** registration statement, **[Form 4]** insider filing, **[PR]** company press release (NOT independent), **[CBRS 10-Q]** Cerebras's own SEC filing, **[local]** local news/permit records, **[quote]** market-data provider. Company: formerly Digihost Technology Inc., SEC CIK 1854368, FYE 31 Dec, files on US domestic forms (10-K/10-Q/8-K) since 2026, not 40-F/6-K. Filing index: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1854368 (EDGAR submissions JSON read directly, 4 Nov 2026).

Important structural finding up front: **after 14 Aug 2026 the company has filed NO 8-K at all.** The 13 Oct 2026 "$200M debt financing commitment" exists only as a press release (and whatever was posted on SEDAR+, which I could not access); it was not filed or furnished on EDGAR. Every post-August operational figure (cash ~$135M, capex ~$153M YTD, "construction on schedule") rests on press releases only.

---

## KQ1. Cerebras agreement — what the primary documents actually say (TCV, term, pricing, payments, delay remedies, termination, binding?)

### Takeaway
The agreement is a **binding, signed, 10-year take-or-pay colocation contract** (not an LOI): "Data Center Colocation and Master Services Agreement" dated 4 May 2026, signed by Alec Amar (President, DGXX) and Andrew Feldman (CEO, Cerebras), filed as redacted Exhibit 10.1 to an 8-K. The ~$1.1B / ~$2.5B figures, the 15 MW / 15 Dec 2026 and 40 MW / end-Q1 2027 targets and the Phase 2 financing condition are all confirmed in the 8-K body; however the actual delivery dates, delay-credit percentages, prepayment size, one-time construction payments and termination day-counts are **redacted** or sit in omitted exhibits, so the economic protection for Cerebras (and the exposure for DGXX) cannot be quantified from public documents.

### Cited Findings
- 8-K (Item 1.01), date of report 4 May 2026, filed 8 May 2026: company "entered into a Data Center Colocation and Master Services Agreement with Cerebras Systems Inc." for "approximately 40 MW" at the Columbiana, Alabama campus; "exclusive license"; initial term "ten (10) years" from the later of the two phase commencement dates; Cerebras may extend "for one or more periods of 1, 3, 5, or 7 years"; value "approximately $1.1 billion over the initial term" and "approximately $2.5 billion" with one 7-year extension, "subject to the Company meeting its obligations"; Cerebras makes "one-time payments" for Phase 1 and Phase 2 construction plus a monthly colocation fee per kW delivered, "a portion of the monthly fee is prepaid"; Phase 1 = 15 MW ready-for-service "targeted December 15, 2026"; Phase 2 to 40 MW "targeted by the end of the first fiscal quarter of 2027", the additional 25 MW "conditioned on the Company securing adequate financing for Phase 2 operations". Amounts of construction payments, prepayment, penalties and termination terms are not given in the 8-K body. — [8-K, official, exact](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026053566/ea0289585-8k_digi.htm)
- Exhibit 10.1 (redacted agreement, EX-10.1, official): Phase 1 defined as "fifteen megawatts (15 MW) of IT Load"; Phase 2 adds 25 MW only if Section 2.2(b) conditions met; Target Delivery Dates sit in **Exhibit A (omitted)**; colocation fee per kW/month **[***] redacted**; Section 6.2 "Prepaid Colocation Fee" **entirely redacted**, letter of credit referenced (6.2(f), redacted); one-time NRCs "$[***] per kW" per phase, payable only after a funding condition (Phase 1: approval of general contractor; Phase 2: approval of final plans/specs); escalation [***]% p.a. compounding from each Phase Commencement Date; **Section 6.1(c): fee "is a take-or-pay obligation payable in full" on contracted IT load regardless of usage**; delay remedy: "Daily RFS Credits" per day of delay as a share of MRC Base (percentages/thresholds redacted), Section 4.4 treats them as liquidated damages; if RFS not achieved by the "Final Outside Delivery Date" (day-count redacted) Customer may terminate the Service Order without fee, prepaid fees and unapplied NRCs are returned, accrued credits remain payable; Phase 2 (2.2(b)): Operator must use commercially reasonable efforts to secure Phase 2 financing within a redacted "Financing Period", **Cerebras must approve the financing**, and "Operator shall have no obligation to deliver Phase 2" if Cerebras disapproves or stays silent; no termination-for-convenience found; force-majeure termination after redacted consecutive days with pro-rated refund; Operator (DGXX) change-of-control: Customer change of control (>50%) lets Operator terminate or continue; Operator may not assign to a "Customer Competitor" (Exhibit H, up to 12 names); exclusivity 24/7/365 and Section 13.8 bars Operator from granting occupancy to any new customer without Customer consent (conditioned on a redacted third party's consent); Customer has ROFR on certain future capacity; power is included in the fee as of Effective Date, later taxes/demand charges pass through; Section 5.4(b) requires firm non-interruptible power up to full contracted IT load; Customer procures its own racks, IT hardware and liquid cooling (CDUs); Delaware law. Omitted: Exhibits A–J incl. Phased Delivery Schedule, RFS Criteria, SLA/Service Credits, Escrow Agreement, Appendix A Cost Breakdown. Signatures: Alec Amar (President) and Andrew Feldman ("ceo"), both 5/4/2026. — [EX-10.1, official, redacted](https://www.sec.gov/Archives/edgar/data/1854368/000121390026053566/ea028958501ex10-1.htm)
- MCR (Form 51-102F3, dated 8 May 2026, attaching PR of 5 May 2026): initial term ~$1.1B, "up to $2.5 billion including renewal terms", also mentions an "additional $1.4 billion" expansion as "upside"; Tier III design, high-density accelerator cooling; "construction start: immediate"; Phase 1 RFS target 15 Dec 2026; full deployment end Q1 2027; revenue commencement "late 2026"; "on-site substation serving Phase 1 is complete", "grid interconnection is finalized", "power delivery agreement with Alabama Power in place"; Phase 1 "self-funded"; no unit pricing disclosed. — [MCR/PR via 8-K Ex. 99.1, furnished, company statements](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026053566/ea028958501ex99-1.htm)
- Q2 2026 10-Q (note on the Cerebras agreement, as extracted): "fixed, take-or-pay colocation fee of **$195.00 per kW per month**", escalating **3.0% annually**; facility "remained under construction and not ready for use" at 30 Jun 2026; Phase 2 "conditioned on the Corporation securing adequate financing"; "the Corporation is currently seeking out project-level financing for the Columbiana, Alabama data center facility". — [10-Q, official](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- Cerebras's own Q2 2026 10-Q (filed 12 Aug 2026) does **not name Digi Power X, Columbiana or Alabama** anywhere (full-text search, 0 hits). It does state: "In the three months ended June 30, 2026, the Company executed non-cancelable lease agreements for additional data center capacity with lease commencement dates in 2026 ... Aggregate undiscounted future minimum lease payments under these agreements total approximately $1.5 billion over the lease term." This is consistent with (but not specific to) the DGXX contract; it covers more than one agreement. — [CBRS 10-Q, official](https://www.sec.gov/Archives/edgar/data/2021728/000162828026056357/cbrs-20260630.htm)
- Cerebras IPO prospectus (424B4, 14 May 2026): 0 hits for Digi Power/Columbiana/Alabama; lists its colocation facilities as "California, Oklahoma, and Canada". — [CBRS 424B4, official](https://www.sec.gov/Archives/edgar/data/2021728/000162828026035214/cerebras-424b4.htm)
- Aug 14 2026 results PR: "contracted run-rate expected in 2027: ~$140M annualized"; Cerebras-related colocation revenue FY2027 "~$80–100M" (Jul 7 PR). — [PR via 8-K Ex. 99.1, 14 Aug 2026](https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea030173001ex99-1.htm); [PR via 8-K Ex. 99.1, 7 Jul 2026](https://www.sec.gov/Archives/edgar/data/1854368/000121390026075755/ea029720301ex99-1.htm)

### Inferences
- Arithmetic check of TCV with the 10-Q fee: $195/kW/mo × 40,000 kW = $7.8M/mo = $93.6M/yr; 10 years at 3% escalation ≈ $1.07B → matches "~$1.1B". Phase 1 alone (15 MW) = $2.925M/mo ≈ $35M/yr. A 7-year extension at the same escalated rate adds only ≈ $0.96B (total ≈ $2.0B), so the "$2.5B" headline implies either repriced renewal rates or additional capacity; it is not reproducible from disclosed terms. Treat $2.5B as a company figure, not a contractual number.
- "Contracted run-rate ~$140M annualized in 2027" (Aug PR) exceeds the ≈$94M/yr that 40 MW at $195/kW yields; the difference is unexplained (SubQ adds ≈$9.8M/yr). Flag as company target, not reconciled.
- Because the NRCs are per kW and payable only after milestone approvals, and the prepaid fee size is redacted, Cerebras's cash contribution to construction is **unknown**; the 10-Q balance sheet shows only $1.69M non-current "deposits payable" and $2.51M "unearned lease revenue" (the latter matches SubQ's $2.95M upfront less amortisation), i.e. **no material Cerebras prepayment had been received by 30 Jun 2026**.
- The delay regime (daily credits → termination without fee after a redacted outside date, with refund of prepaid fees) means a slip of the 15 Dec 2026 date is not fatal per se, but a prolonged slip gives Cerebras a walk-away right. The day-count is the single most important undisclosed number.
- Phase 2 is doubly conditional: DGXX must find financing **and Cerebras must approve it**. The $200M commitment letter (KQ4) has not been described as Cerebras-approved.

### Gaps
- Actual contracted delivery dates (Exhibit A), Final Outside Delivery Date day-count, RFS credit percentages, prepayment amount, NRC $/kW, escrow terms — all redacted/omitted. SEDAR+ copy not checked (site not accessible from this environment); it would be the same redacted exhibit.
- Whether Cerebras has paid anything to date: not disclosed in any filing through 14 Aug 2026; Q3 10-Q (due ~13 Nov 2026) is the next place to look (deposits payable / contract liabilities).

---

## KQ2. SubQ AI contract

### Takeaway
Verified in the 10-Q: ~$19.6M, 24-month bare-metal GPU rental with Subquadratic Inc. ("SubQ AI"), signed 18 Apr 2026, effective 15 May 2026, 15% ($2.95M) upfront; first GPU revenue ($1.08M) recognised in Q2 2026.

### Cited Findings
- 8-K of 20 Apr 2026 Ex. 99.1 (PR): "first AI revenue contract", $19.6M expected TCV, 24 months, NVIDIA Blackwell, NeoCloudz bare metal at the Alabama AI data center. — [PR via 8-K, company](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026045361/ea028691301ex99-1.htm)
- 10-Q Q2 2026: agreement signed 18 Apr 2026, effective 15 May 2026; upfront $2.95M = 15% of TCV, remainder monthly Net-15; "recognized its first AI-related revenues in May 2026"; Q2 2026 revenue line "Tier III AI project / GPU rental" **$1,082,592**; unearned lease revenue $2,513,111 at 30 Jun 2026; separately DGXX invested $250,000 in a SAFE in Subquadratic Inc. on 23 Apr 2026 (i.e., DGXX is a small investor in its own customer). — [10-Q, official](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- Aug 14 PR: GPU bare-metal "~0.6 MW deployed"; ~$30M invested in GPU infrastructure; company claims 10 pods / ~4,000 B300 capacity "up to ~$120M potential annualized revenue" (company estimate, not contracted). — [PR, 14 Aug 2026](https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea030173001ex99-1.htm)

### Inferences
- $19.6M/24 ≈ $0.82M/month; 1.5 months in Q2 ≈ $1.2M vs $1.08M booked — consistent. SubQ is a small private AI startup; counterparty credit is unverified (gap).

### Gaps
- SubQ's financial capacity to pay ~$0.8M/month for 24 months: no public data.

---

## KQ3. Power & sites — how much is AI-ready vs. mining-grade; where Cerebras is hosted; construction status

### Takeaway
Cerebras is hosted **only at Columbiana, Alabama** (130 Industrial Parkway, a former Grede foundry / bitcoin-mining site DGXX has owned since 2022). Of the "201.7 MW" portfolio, essentially **none was Tier III AI-ready at 30 Jun 2026** apart from one ~1 MW ARMS 200 modular pod (~0.6 MW of GPUs running since 15 May 2026); the 40 MW Tier III hall was "under construction and not ready for use". New York (141.7 MW) is still a gas peaker + mining/hosting portfolio "in the planning phase" for AI conversion (target Q3–Q4 2027); North Carolina 200 MW is raw land targeted 2028–2030. Independent evidence of construction progress is thin: a $7.0M building permit (22 Jun 2026, Dunn Building Company) and a July 2026 city abatement vote.

### Cited Findings
- 10-K FY2025 (Properties): Columbiana AL, 130 Industrial Parkway, acquired 14 Jun 2022, "initial access to 28 MW of power with a total capacity of up to 55 MW"; North Tonawanda NY (1070 Erie Ave, ~13.5 acres, acquired 8 Feb 2023) "is a 60 MW power plant" (gas-fired peaker) plus a 5 MW community solar project; Buffalo NY (1001 East Delavan, leased, 99-year lease) bitcoin mining facility; North Carolina ~40 acres owned, "to accommodate a 200 MW power", planned Tier 1 and Tier 3, phased AI deployment 2028–2029; secured power cited as 123 MW North Tonawanda + 18.7 MW Buffalo (=141.7 MW NY) + "70 MW secured for a Tier 3 AI data-center site"; active miners at YE2025 "approximately nil" self-mining, "9,700" under colocation (hosting) agreements; FY2025 capex only ~$11M. — [10-K, official](https://www.sec.gov/Archives/edgar/data/1854368/000121390026037677/ea0283764-10k_digipower.htm)
- 10-Q Q2 2026 MD&A: Alabama 60 MW; New York 141.7 MW; total 201.7 MW; North Carolina 200 MW "anticipated by 2028"; AI roadmap "Q4 2026 total of 55 MW, with 40 MW critical load"; Phase 1 substation completed, grid interconnection finalized, power delivery agreement in place; "approximately $50 million of Tier III AI data center assets were placed into service"; load study for an additional 60 MW at one NY location; ~$35M NVIDIA Vera Rubin commitment (3 Jun 2026) from cash. — [10-Q, official](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- Aug 14 2026 PR: GPU bare-metal ~0.6 MW deployed; New York "conversion to AI data center operations targeted for Q3–Q4 2027"; North Carolina ~75 MW in 2029 and ~75 MW in 2030; West Virginia 1.3 GW "under an LOI, still being assessed". — [PR, 14 Aug 2026](https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea030173001ex99-1.htm)
- Oct 13 2026 PR: "construction at the 40 MW Alabama campus remains on target, Phase 1 expected December 2026, Phase 2 March 2027"; first ARMS 200 operating since May 2026; "New York State sites are in the planning phase for conversion to AI token factories"; Silicon Valley office/lab acquired. — [PR, 13 Oct 2026, company only](https://via.tt.se/pressmeddelande/4594325/digi-power-x-announces-dollar200-million-debt-financing-commitment-to-support-completion-of-alabama-ai-data-center-and-provides-expansion-update?lang=en)
- Jul 7 2026 PR: ARMS 200 pod operating at Alabama since 15 May 2026; YTD capex at Columbiana ~$95M as of 3 Jul 2026; ARMS 200 is a 1 MW modular unit for up to 256 B200/B300 GPUs (company description). — [PR, 7 Jul 2026](https://www.sec.gov/Archives/edgar/data/1854368/000121390026075755/ea029720301ex99-1.htm); [PR ARMS 200 commissioning](https://www.accessnewswire.com/newsroom/en/computers-technology-and-internet/digi-power-x-announces-arms-200-commissioning-and-timetable-for-g-1142570)
- Local: Shelby County building permit issued 22 Jun 2026 for 130 Industrial Parkway, owner "Digihost Technology Inc", contractor Dunn Building Company LLC, valuation **$7,024,000**; article describes an older 55 MW / two-phase plan (Phase 1 22 MW ~$176M, total ~$440M, "financed primarily through debt"). — [local, Bama Buzz, ~29–30 Jun 2026](https://thebamabuzz.com/digi-power-x-data-center-shelby-building-permits/)
- Local: Columbiana City Council (vote "Tuesday", ~21 Jul 2026) granted a 12-month construction-period sales & use tax abatement in exchange for a $3.5M "community impact payment"; mayor says company aims to have the completed data center operating "by 2027"; council had earlier passed an ordinance restricting future data-center expansion. — [local, WBRC 24 Jul 2026](https://www.wbrc.com/2026/07/24/columbiana-receive-35m-data-center-deal-heres-how-it-could-change-your-neighborhood/)
- Local (via Compute Atlas summarising Shelby County Reporter, 29 May 2026 — original article returned HTTP 403): site already had a 22 MW substation from the foundry era; construction "set to begin in May 2026", "completed by March 2027 for service to begin in April 2027"; council had "unanimously rejected a tax abatement proposal" in May 2026 (later approved in July per WBRC); abatement filing says "the site will utilize water for liquid cooling"; Compute Atlas lists investment $371.5M (unsourced). — [secondary aggregator](https://www.compute-atlas.com/facilities/digi-power-x-columbiana-al); [Shelby County Reporter (403)](https://www.shelbycountyreporter.com/news/columbiana-data-center-signs-1b-agreement-future-plans-revealed-f520ff1b/)
- DCD trade press on earlier plan: 22 MW in 2026, 55 MW by 2027. — [DCD, secondary](https://www.datacenterdynamics.com/en/news/cerebras-signs-on-for-40mw-of-capacity-at-digi-power-x-data-center-in-alabama/)

### Inferences
- "AI-ready" today ≈ 1 MW (one ARMS pod). The 15 MW Phase 1 hall must go from "not ready for use" (30 Jun) to RFS in ~5.5 months. The only independent datapoint on physical progress is a $7.0M building permit in June — small relative to a $150M+ phase, consistent with the heavy spend being on long-lead electrical/cooling equipment and modular/prefab elements rather than conventional building work, but it does not prove transformer/chiller delivery. No contractor announcement, utility (Alabama Power) filing, or photo evidence found.
- Plausibility of 15 Dec 2026: the site has an existing ~22–28 MW grid feed (foundry substation) and the company says the Phase 1 substation is complete, so **power for 15 MW is plausible**; the open question is the Tier III hall (dual-path, liquid-cooling CDU/CFNI piping, which Cerebras itself installs per Section 5.2). Local reporting from May said "service to begin in April 2027" — later than the 15 Dec 2026 contract target — but the company reiterated December as of 13 Oct 2026 (PR only).
- "60 MW Alabama" (10-Q) vs "up to 55 MW" (10-K) vs "Q4 2026 55 MW incl. 40 MW critical load": the 40 MW Cerebras IT load implies ≈55 MW facility load at PUE ~1.35; figures are not contradictory but the extra 5 MW of "Alabama 60 MW" is not explained.
- New York 141.7 MW is mining-grade / peaker power with hosting of 9,700 third-party miners; it is **not** AI capacity and carries no 2026 AI revenue.

### Gaps
- No independent construction-progress evidence after June 2026 (no utility filings, contractor PRs, or photos found); Shelby County Reporter article (29 May 2026) not readable (403).
- Breakdown of the 60 MW Alabama figure and transformer/switchgear delivery status: not disclosed.

---

## KQ4. The 13 Oct 2026 US$200M project financing commitment letter

### Takeaway
Press-release-only. Lender unnamed ("a major lending institution"), **Goldman Sachs syndicating**, SPV-level debt with an **unsecured parent guarantee through project completion**, closing targeted "within 90 days" (≈ mid-January 2027, i.e. **after** the 15 Dec 2026 Phase 1 target) subject to definitive documentation, lender due diligence and conditions. No 8-K, no definitive agreement announced as of 4 Nov 2026.

### Cited Findings
- PR 13 Oct 2026: commitment letter from "a major lending institution" for US$200M; "structured at a project special purpose vehicle level, with an unsecured company guarantee through project completion and other limited matters"; conditions: definitive documentation, satisfaction of various conditions, lender due diligence; "expected closing within 90 days"; use: completion of Alabama project and related costs, "preserving corporate liquidity, limiting shareholder dilution"; cash ~US$135M; capex ~US$153M YTD 2026; **no ATM shares issued in Q3 2026**; forward-looking risk that "conditions to closing ... are not satisfied or waived" or the commitment "terminates or is modified". — [PR, company only](https://via.tt.se/pressmeddelande/4594325/digi-power-x-announces-dollar200-million-debt-financing-commitment-to-support-completion-of-alabama-ai-data-center-and-provides-expansion-update?lang=en); mirrors: [NatLawReview](https://natlawreview.com/press-releases/digi-power-x-announces-200-million-debt-financing-commitment-support), [DCD](https://datacenterdynamics.com/en/news/digi-power-x-secures-200m-in-debt-financing-for-alabama-data-center-project)
- Aug 14 2026 PR: "in advanced discussions with lenders for Alabama project debt and has engaged Goldman Sachs to syndicate it". — [PR](https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea030173001ex99-1.htm)
- EDGAR index: last 8-K is 14 Aug 2026; filings after 1 Sep 2026 are S-3/A (11 Sep), EFFECT (15 Sep), Form 4 (15 Oct), PRE 14A (16 Oct), DEF 14A / ARS / DEFA14A (2 Nov). **No 8-K for the commitment letter.** — [EDGAR submissions, official](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1854368&type=8-K)

### Inferences
- A commitment letter with due-diligence and documentation conditions is customary pre-closing paper; it is not funded capital. The absence of an 8-K (Item 1.01 would normally be triggered by a definitive credit agreement, not by a commitment letter) is consistent with nothing definitive having been signed by 4 Nov 2026.
- The "unsecured company guarantee through project completion" means the parent carries completion risk; project-level debt will be structurally senior to equity on the Alabama asset, which is the company's only contracted revenue asset.
- Phase 2 requires Cerebras's approval of the financing (EX-10.1 §2.2(b)); no statement that Cerebras has approved.

### Gaps
- Lender identity, interest rate, tenor, covenants, conditions precedent (e.g., Phase 1 RFS, Cerebras consent, equity contribution), whether SEDAR+ carries a material change report: not found.

---

## KQ5. Share count, ATM, dilution (low / mid / high)

### Takeaway
Latest official basic count: **101,396,689 SV shares + 3,333 PV shares (= 666,600 SV-equivalent) as of record date 27 Oct 2026** (DEF 14A). The company's own fully diluted total in the proxy is **111,540,742** (options 3,635,000; RSUs 4,761,978; warrants 1,080,475). The prior analysis's 108.48M used the 10-Q MD&A numbers (2.92M options / 2.95M RSUs / 1.22M warrants), which conflict with both the 10-Q financial-statement note (3.485M / 4.675M / 1.08M) and the proxy; the proxy figure should be used. No equity raise, convertible or ATM sale after 14 Aug 2026 is disclosed (company says zero ATM shares in Q3 2026); two proposals at the 21 Dec 2026 AGM would lift RSU and option plan caps to 10,139,668 shares each with a 10%/yr evergreen from 2028.

### Cited Findings
- DEF 14A (filed 2 Nov 2026): record date 27 Oct 2026; 101,396,689 SV shares (147 holders of record) and 3,333 PV shares (one holder, entity controlled by a director/officer; 200 votes each; total votes 102,063,289); options outstanding 3,635,000 (WAEP C$4.90); warrants 1,080,475 (WAEP $2.98); RSUs 4,761,978; RSU shares available 1,443,319 now / 5,377,690 after meeting; "fully diluted total: 111,540,742"; proposals: consolidate SV+PV into one class (PV→200 common each), raise quorum to 33⅓%, amend RSU Plan to fixed max 10,139,668 (prior max 6,205,297) with evergreen up to 10% annually from 1 Jan 2028, amend Option Plan to fixed max 10,139,668 with same evergreen; Michel Amar (Chairman/CEO) 6,005,480 SV + 3,333 PV; Alec Amar 1,368,949 SV; meeting 21 Dec 2026 (virtual). — [DEF 14A, official](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026114925/ea0310068-def14a_digi.htm)
- 10-Q Q2 2026: cover 101,393,355 SV + 3,333 PV as of 14 Aug 2026; FS note at 30 Jun 2026: options 3,485,000 (3,447,500 vested), RSUs 4,675,312, liability-classified warrants 1,080,475; MD&A table as of 14 Aug 2026: options 2,920,635, RSUs 2,945,312, warrants 1,219,461 (incl. 240,385 broker warrants) — **internal inconsistency**; ATM: May 8 2026 prospectus supplement up to $175,000,000 (including $75M under prior supplement); H1 2026 ATM sales 27,950,000 shares, net proceeds $159,547,599; from inception through 30 Jun 2026: 52,028,450 shares, gross $254,758,203; after 30 Jun 2026: 2,850,000 shares for $11,256,693; 2025 ATM had been upsized to US$200M. — [10-Q, official](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- 10-K cover: 69,807,449 SV shares at 30 Mar 2026 → ~101.4M by 14 Aug 2026 (+45% in 4.5 months, essentially all ATM). — [10-K, official](https://www.sec.gov/Archives/edgar/data/1854368/000121390026037677/ea0283764-10k_digipower.htm)
- S-3/A (11 Sep 2026, effective 15 Sep 2026): resale registration only, 380,590 SV shares underlying Feb-2025 private-placement warrants ($3.66 strike, expire 7 Feb 2028) for 19 selling holders; no new primary shelf; Nasdaq price 10 Sep 2026 $3.70. — [S-3/A, official](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026099261/ea0304511-s3a1_digi.htm)
- 13 Oct 2026 PR: "no shares were issued under the ATM program in Q3 2026". — [PR](https://via.tt.se/pressmeddelande/4594325/digi-power-x-announces-dollar200-million-debt-financing-commitment-to-support-completion-of-alabama-ai-data-center-and-provides-expansion-update?lang=en)
- Form 4 (filed 15 Oct 2026): CEO Michel Amar **bought** 20,000 SV shares on 14 Oct 2026 at $2.7628 (open-market, code P). — [Form 4, official](https://www.sec.gov/Archives/edgar/data/1854368/000121390026109819/ownership.xml)
- H.C. Wainwright settlement (Jan 2026): $840,000.12 cash + warrant for up to 269,231 shares (PR; likely inside the 1.08M warrant count). — [secondary summary](https://quantisnow.com/i/digipower-x-announces-closing-of-settlement-6405350)

### Inferences
- Basic SV-equivalent today ≈ 102.06M (101.40M SV + 0.667M PV-equivalent). Fully diluted scenarios (my calculation): **Low** = basic 102.06M (options at C$4.90 and warrants at $2.98 are out of the money at $2.27; RSUs 4.76M vest regardless → 106.8M "economic low"). **Mid** = proxy 111.5M. **High** = 111.5M + new plan headroom (RSU cap +~5.4M available, option cap to 10.1M → ~+6.5M) ≈ 123M, before any equity raise. Each $50M raised via ATM at ~$2.27 ≈ 22M shares (+22% of basic); if the $200M debt does not close and Phase 2 (+ GPU plans) is funded with equity instead, dilution of 50–100% is arithmetically possible at current prices.
- ATM remaining capacity: the $175M (May 2026) supplement had ≈$163M gross drawn in H1 plus $11.3M in July → ~$0–1M left if the $175M cap includes the $75M prior supplement as stated; i.e. **a new prospectus supplement/shelf would be needed to raise meaningful equity**, which would itself be a visible signal (none filed as of 4 Nov 2026).

### Gaps
- Exact remaining ATM capacity is not stated in any filing; the 2025 US$200M ATM vs the 2026 $175M supplement relationship is ambiguous.
- Shares issued after 27 Oct 2026: none disclosed; Q3 10-Q cover (≈13 Nov) will give the next official count.

---

## KQ6. Cash, debt, going concern, burn, legacy bitcoin share

### Takeaway
At 30 Jun 2026: cash $128.1M (official 10-Q; the "$142.4M" in the PR appears to include digital assets $14.3M), **no debt**, total liabilities $14.5M, working capital $131.8M. Going-concern-dependency language exists in the 10-Q notes ("ability to continue as a going concern is dependent on" executing Tier III initiatives and raising financing) but no auditor going-concern qualification. Operating cash burn H1 2026 $10.6M; capex H1 $96.3M. Bitcoin-related revenue (self-mining $0.16M + miner hosting $3.43M) was ~54% of Q2 revenue; self-mining alone 2.4%.

### Cited Findings
- 10-Q Q2 2026: cash $128,121,977 (vs $78.5M at 31 Dec 2025, rise "mainly from share issuances"); digital currencies $14,303,261 (BTC $12,705,648 ≈ 217 BTC; ETH $1,597,613); total liabilities $14,547,035; no loans/debt; deposits payable (non-current) $1,692,526; unearned lease revenue $2,513,111; working capital $131,781,707; Q2 revenue $6,628,607 (mining/staking $161,422; AI/GPU $1,082,592; energy sales $1,958,285; colocation $3,426,308); H1 revenue $14,595,820 (mining $209,149; GPU $1,082,592; energy $6,850,863; colocation $6,453,216); net loss Q2 $(14,360,509), H1 $(19,012,854); operating cash flow H1 $(10,607,198); capex H1 $(96,308,574); Q2 BTC mined ~3 (−79% y/y); going-concern-dependency sentence as quoted; "not currently a party to any actual or pending legal proceedings" of material effect. — [10-Q, official](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- Aug 14 2026 PR: cash "$142.4M as of June 30, 2026" and "~$150M as of August 14, 2026"; adjusted EBITDA ~$3.3M (adds back SBC $5.8M, warrant FV loss $5.0M, crypto loss $2.8M, D&A $4.1M); total assets $279.6M; equity $265.0M; capex + equipment deposits YTD ~$110M; "no debt". — [PR](https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea030173001ex99-1.htm)
- Jul 7 2026 PR: cash ~$155M at 3 Jul 2026; Columbiana YTD capex ~$95M. — [PR](https://www.sec.gov/Archives/edgar/data/1854368/000121390026075755/ea029720301ex99-1.htm)
- Oct 13 2026 PR: cash ~$135M; capex ~$153M YTD. — [PR](https://via.tt.se/pressmeddelande/4594325/digi-power-x-announces-dollar200-million-debt-financing-commitment-to-support-completion-of-alabama-ai-data-center-and-provides-expansion-update?lang=en)
- Market data: revenue TTM $31.40M; net income TTM −$36.03M. — [quote, StockAnalysis](https://stockanalysis.com/stocks/DGXX/)

### Inferences
- Cash walk (company figures): $155M (3 Jul) → ~$150M (14 Aug) → ~$135M (13 Oct) while stated capex YTD rose $95M → $110M → $153M; a $43M capex increase against a $15M cash decline between mid-Aug and mid-Oct does not reconcile unless "capex invested" includes non-cash commitments/deposits or the ~$11M July ATM proceeds and Q3 receipts (possibly Cerebras NRC/prepayment) offset it. **Flag for Q3 10-Q verification.**
- Quarterly cash burn: operating ≈ $5M/quarter; the real drain is capex (~$50M/quarter H1). With ~$135M cash and the 15 MW hall still to finish, cash covers Phase 1 completion only if remaining Phase 1 spend is well under ~$100M; Phase 2 (25 MW) is explicitly dependent on the $200M debt.
- "Adjusted EBITDA $3.3M" is after adding back $5.8M SBC on a $6.6M revenue base — low-quality metric.

### Gaps
- Capex remaining to complete Phase 1 and the total Phase 2 budget are not disclosed (only older local reporting: ~$176M Phase 1 / ~$440M total for the earlier 55 MW plan; Compute Atlas $371.5M unsourced).

---

## KQ7. Q3 2026 results date

### Takeaway
Confirmed: **13 Nov 2026**, conference call 8:30 AM ET (press release of 28 Oct 2026). No 8-K yet.

### Cited Findings
- PR 28 Oct 2026 (ACCESS Newswire, Miami): results for the quarter ended 30 Sep 2026 on 13 Nov 2026; call 8:30 AM ET, dial-in 1-877-407-9039 / 1-201-689-8470. — [PR mirror](https://www.valuethemarkets.com/news/press-releases/digi-power-x-to-announce-2026-q3-financial-results-and-provi); [Yahoo mirror](https://finance.yahoo.com/markets/stocks/articles/digi-power-x-announce-2026-113000375.html)
- StockAnalysis lists next earnings 13 Nov 2026. — [quote](https://stockanalysis.com/stocks/DGXX/)

### Gaps
- None.

---

## KQ8. Filings / news after 1 Sep 2026

### Takeaway
Only: S-3/A resale registration (11 Sep) and effectiveness (15 Sep); $200M commitment-letter PR (13 Oct, no 8-K); CEO open-market purchase of 20,000 shares at $2.76 (14 Oct, Form 4); PRE 14A (16 Oct); Q3 date PR (28 Oct); DEF 14A / annual report / notice (2 Nov) with share-class consolidation and equity-plan expansion proposals for the 21 Dec 2026 AGM. No Nasdaq notices, no lawsuits, no management changes, no new customer contracts found. The Pleasants (WV) 1.3 GW item is a **non-binding LOI from 7 Jan 2026** with no definitive agreement reported.

### Cited Findings
- EDGAR index (as listed in KQ4). — [EDGAR](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1854368)
- Form 4 CEO purchase 20,000 @ $2.7628 on 14 Oct 2026. — [Form 4](https://www.sec.gov/Archives/edgar/data/1854368/000121390026109819/ownership.xml)
- DEF 14A proposals (see KQ5). — [DEF 14A](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026114925/ea0310068-def14a_digi.htm); notice of availability. — [DEFA14A](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026114927/ea0310283-defa14a_digi.htm)
- Pleasants Power Station: non-binding LOI with Omnis Pleasants LLC announced 7 Jan 2026, load/interconnection study up to 1.3 GW, definitive agreements targeted within 90 days — no follow-up found; Aug 14 PR still calls it "under an LOI, still being assessed". — [secondary](https://www.newsquantified.com/dgxx/stock-report/digi-power-x-common-subordinate-voting-shares-enters-nonbinding-loi-with-omnis-0fh072); [PR 14 Aug](https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea030173001ex99-1.htm)
- Analyst items (secondary, via StockAnalysis news feed): "Jones" (JonesTrading) initiated Buy, $8 PT ~early Oct 2026; Alliance Global cut PT $12→$9 (Buy) in Aug 2026. — [quote/news feed](https://stockanalysis.com/stocks/DGXX/)
- Litigation search: no DGXX class action or Nasdaq deficiency found (hits were for Diginex / Digi International, different companies); 10-Q states no material legal proceedings. — [search summary; 10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- Listing: TSXV listing moved to Cboe Canada (DGX) effective 27 Feb 2026 — the ticker "TSXV: DGX" in the brief is outdated. — [secondary](https://rallies.ai/news/digipower-x-to-uplist-shares-to-cboe-canada-feb-27-after-tsxv-delisting)

### Inferences
- Cerebras's own Q3 10-Q (due ~mid-Nov 2026) could independently confirm whether a lease with 2026 commencement is still on track (watch "Leases Not Yet Commenced").

### Gaps
- SEDAR+ could not be queried; Canadian-only filings (e.g., MCR for the commitment letter) unverified. Company IR news page could not be parsed (image-heavy).

---

## KQ9. Share price, market cap, EV, range, performance; price action around the Cerebras announcement

### Takeaway
Close 3 Nov 2026 **$2.27** (52-week range $1.86–$9.20); market cap ≈ **$232M**; with ~$135M cash (Oct PR) and no debt, EV ≈ **$95–100M** (≈ $89M using 30 Jun cash + crypto). Down ~41% over 30 days, ~40% over 60 and 90 days, ~63% over 180 days and ~73% from the 13 May 2026 closing high ($8.46). The Cerebras news was **not** priced in: +29% on 5 May 2026 on 115.8M shares (≈60× normal volume) after a modest +19% run-up the prior week; the stock then peaked a week later and has since given back the entire deal premium and more (now 43% below the pre-announcement close of $3.95). The $200M financing PR (13 Oct) was met with continued selling (−2%, −8% next day).

### Cited Findings
- Price/market data: close $2.27 on 3 Nov 2026 (+6.8%); market cap $231.68M; shares outstanding 102.06M; 52-week range $1.860–$9.200; next earnings 13 Nov 2026. — [quote, StockAnalysis](https://stockanalysis.com/stocks/DGXX/)
- Daily history (Yahoo Finance chart API, 1-year daily, retrieved 4 Nov 2026): 27 Apr $3.33; 4 May $3.95 (vol 5.0M); **5 May $5.11 (vol 115.8M)**; 6 May $6.24 (31.0M); 8 May $6.63; 11 May $7.43; 13 May $8.46 (52-wk closing high; intraday high $9.20 on 14 May); 15 May $7.54; 3 Jun $7.62; 30 Jun $5.45; 7 Jul $4.42; 5 Aug $3.75; 14 Aug $3.97; 4 Sep $3.75; 25 Sep $4.59 (local high); 2 Oct $3.84; 6 Oct $3.63; 13 Oct $2.96 (vol 2.4M); 14 Oct $2.71 (4.4M); 2 Nov $2.13 (lowest close since March); 3 Nov $2.27; 52-wk low close $1.89 on 30 Mar 2026 (intraday $1.86). — [quote, Yahoo Finance chart data](https://finance.yahoo.com/quote/DGXX/history/); cross-checked Aug 25–Nov 3 closes on [StockAnalysis history](https://stockanalysis.com/stocks/DGXX/history/)
- Contemporaneous press: shares +27–29% on 5 May 2026 after the announcement. — [Stocktwits, secondary](https://stocktwits.com/news-articles/markets/equity/dgxx-stock-soars-22-today-everything-to-know-about-the-data-center-agreement-with-nvidia-rival-cerebras/cZQDcbdRe9X); [Invezz, secondary](https://invezz.com/en-ae/news/2026/05/05/penny-stock-dgxx-is-soaring-and-it-has-ai-firm-cerebras-to-thank/)

### Inferences
- Performance (my calculation from the Yahoo closes): 30d (vs 2 Oct $3.84) **−40.9%**; 60d (vs 4 Sep $3.75) **−39.5%**; 90d (vs 5 Aug $3.75) **−39.5%**; 180d (vs 7 May $6.19) **−63.3%**; vs 52-wk closing high **−73%**; vs pre-announcement close 4 May $3.95 **−42.5%**; YTD-ish vs 4 Nov 2025 close $6.03 **−62%**.
- Pre-announcement leak signal: 1 May +11.6% and 4 May +5.1% on 1.9M/5.0M volume (vs ~1.2–1.4M typical) — mild run-up, possibly rumor/positioning; the dominant reaction came on the public release day, so the deal was not meaningfully priced in beforehand. Since mid-May the market has fully discounted the deal; at ~$95–100M EV the stock prices in substantial execution/financing risk on a contract whose Phase 1 alone would yield ≈$35M/yr of take-or-pay revenue if delivered.
- EV calc: $231.7M − $135M cash (PR, 13 Oct) ≈ $97M; or − ($128.1M + $14.3M crypto, 10-Q 30 Jun) ≈ $89M. Debt zero per 10-Q.

### Gaps
- Day-by-day news catalysts for the Sept 25 → Nov 2 slide (−54%) are not identified (no company filings in that window beyond the proxy); likely sector/Cerebras-stock sympathy and financing-dilution fears, but unverified.

---

## KQ10. Is 15 MW by 15 Dec 2026 physically plausible? How much capital to deliver 40 MW, secured vs not? Realistic dilution?

### Takeaway
Plausible-but-unverified: power for Phase 1 exists (foundry-era 22–28 MW feed, Phase 1 substation "complete" per 8-K/MCR), ~$95–153M has reportedly been spent at the site, and the company reiterated December as of 13 Oct; but the only independent artefacts are a $7.0M June permit and a July abatement vote, local reporting had pointed to April 2027 service, and the facility was "not ready for use" at 30 Jun. Capital: company has never disclosed a total budget; third-party/local figures range $370–440M for the full site. Secured: ~$135M cash (PR) + $200M commitment letter (non-binding until documented, closing after the Phase 1 target date). Unsecured: Phase 2 if the debt fails, plus the GPU build-out ($35M Vera Rubin commitment, ~10 MW NeoCloudz plan). Realistic dilution from equity-plan expansion alone ≈ +10%; from an equity-funded Phase 2 at ~$2–3/share, +30–70%.

### Cited Findings
- Power/infrastructure claims (substation complete, interconnection finalized, PDA with Alabama Power) — company statements in 8-K/MCR and 10-Q, not independently verified. — [8-K](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026053566/ea0289585-8k_digi.htm); [10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- Facility "remained under construction and not ready for use" at 30 Jun 2026; ~$50M Tier III assets placed in service. — [10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)
- Capex spent at Columbiana ~$95M by 3 Jul; ~$110M incl. deposits by 14 Aug; ~$153M company-wide by 13 Oct (all PRs). — [PR 7 Jul](https://www.sec.gov/Archives/edgar/data/1854368/000121390026075755/ea029720301ex99-1.htm); [PR 14 Aug](https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea030173001ex99-1.htm); [PR 13 Oct](https://via.tt.se/pressmeddelande/4594325/digi-power-x-announces-dollar200-million-debt-financing-commitment-to-support-completion-of-alabama-ai-data-center-and-provides-expansion-update?lang=en)
- Local plan figures (older 55 MW plan): Phase 1 ~$176M, total ~$440M, "financed primarily through debt"; permit $7.0M (22 Jun 2026). — [local](https://thebamabuzz.com/digi-power-x-data-center-shelby-building-permits/)
- Cerebras supplies and installs its own racks and liquid-cooling CDUs (EX-10.1 §5.2) — part of the critical path sits with the customer. — [EX-10.1](https://www.sec.gov/Archives/edgar/data/1854368/000121390026053566/ea028958501ex10-1.htm)
- $200M commitment: closing "within 90 days" of 13 Oct 2026 (≈ 11 Jan 2027). — [PR 13 Oct](https://via.tt.se/pressmeddelande/4594325/digi-power-x-announces-dollar200-million-debt-financing-commitment-to-support-completion-of-alabama-ai-data-center-and-provides-expansion-update?lang=en)
- Equity-plan expansion to 10,139,668 RSUs + 10,139,668 options with 10%/yr evergreen from 2028. — [DEF 14A](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026114925/ea0310068-def14a_digi.htm)

### Inferences
- Capital math (estimates): if the older $176M Phase-1 figure is roughly right and ~$95–120M had gone into Columbiana by Aug/Oct, remaining Phase 1 spend is on the order of $50–80M — coverable from the ~$135M cash. Phase 2 (25 MW, est. $150–260M) depends on the $200M debt; if it closes, 40 MW is fundable with little new equity; if not, Phase 2 requires ~$150M+ equity ≈ 65M+ shares at $2.27 (≈ +65%), or Phase 2 is not delivered (contract allows this without default, but TCV shrinks to ≈$0.4B for 15 MW).
- Timeline risk indicators: facility not usable at 30 Jun; permit for "part of" the project only in late June; the company's own earlier ARMS pod slipped from Nov 2025 → Mar 2026 → May 2026 (track record of 5–6 month slips on a 1 MW unit); contract protects Cerebras via daily credits and an outside-date termination. A slip into Q1 2027 would look consistent with local reporting (April 2027 service) and with the debt closing date.
- Realistic dilution ladder (my estimate): base 102M → ~112M (existing awards) → ~123M (plan headroom) → 150–190M if Phase 2/GPU growth is equity-funded at $2–3.

### Gaps
- No disclosed total project budget, remaining-to-spend, transformer/chiller delivery dates, or GC name beyond the permit's Dunn Building Company; no independent site inspection evidence; SEDAR+ and the Shelby County Reporter article inaccessible from this environment.

---

## Source list (primary first)
1. 8-K, 4 May 2026 (Cerebras agreement): https://www.sec.gov/Archives/edgar/data/0001854368/000121390026053566/ea0289585-8k_digi.htm
2. EX-10.1 redacted Cerebras MSA: https://www.sec.gov/Archives/edgar/data/1854368/000121390026053566/ea028958501ex10-1.htm
3. EX-99.1 MCR + PR 5 May 2026: https://www.sec.gov/Archives/edgar/data/0001854368/000121390026053566/ea028958501ex99-1.htm
4. 10-Q Q2 2026 (filed 14 Aug 2026): https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm
5. 8-K + Ex. 99.1 Q2 results PR, 14 Aug 2026: https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea0301730-8k_digi.htm ; https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea030173001ex99-1.htm
6. 8-K Ex. 99.1 operations update, 7 Jul 2026: https://www.sec.gov/Archives/edgar/data/1854368/000121390026075755/ea029720301ex99-1.htm
7. 8-K Ex. 99.1 SubQ PR, 20 Apr 2026: https://www.sec.gov/Archives/edgar/data/0001854368/000121390026045361/ea028691301ex99-1.htm
8. 10-K FY2025 (filed 31 Mar 2026): https://www.sec.gov/Archives/edgar/data/1854368/000121390026037677/ea0283764-10k_digipower.htm
9. S-3/A, 11 Sep 2026: https://www.sec.gov/Archives/edgar/data/0001854368/000121390026099261/ea0304511-s3a1_digi.htm
10. Form 4 CEO purchase, 15 Oct 2026: https://www.sec.gov/Archives/edgar/data/1854368/000121390026109819/ownership.xml
11. DEF 14A, 2 Nov 2026: https://www.sec.gov/Archives/edgar/data/0001854368/000121390026114925/ea0310068-def14a_digi.htm ; DEFA14A: https://www.sec.gov/Archives/edgar/data/0001854368/000121390026114927/ea0310283-defa14a_digi.htm
12. EDGAR filing index CIK 1854368: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1854368
13. Cerebras 10-Q Q2 2026: https://www.sec.gov/Archives/edgar/data/2021728/000162828026056357/cbrs-20260630.htm ; Cerebras 424B4: https://www.sec.gov/Archives/edgar/data/2021728/000162828026035214/cerebras-424b4.htm
14. PR 13 Oct 2026 ($200M commitment): https://via.tt.se/pressmeddelande/4594325/digi-power-x-announces-dollar200-million-debt-financing-commitment-to-support-completion-of-alabama-ai-data-center-and-provides-expansion-update?lang=en
15. PR 28 Oct 2026 (Q3 date): https://www.valuethemarkets.com/news/press-releases/digi-power-x-to-announce-2026-q3-financial-results-and-provi
16. Local: Bama Buzz permit: https://thebamabuzz.com/digi-power-x-data-center-shelby-building-permits/ ; WBRC abatement: https://www.wbrc.com/2026/07/24/columbiana-receive-35m-data-center-deal-heres-how-it-could-change-your-neighborhood/ ; Compute Atlas: https://www.compute-atlas.com/facilities/digi-power-x-columbiana-al ; Shelby County Reporter (403): https://www.shelbycountyreporter.com/news/columbiana-data-center-signs-1b-agreement-future-plans-revealed-f520ff1b/
17. Quotes: StockAnalysis https://stockanalysis.com/stocks/DGXX/ ; history https://stockanalysis.com/stocks/DGXX/history/ ; Yahoo https://finance.yahoo.com/quote/DGXX/history/
18. Secondary: DCD https://www.datacenterdynamics.com/en/news/cerebras-signs-on-for-40mw-of-capacity-at-digi-power-x-data-center-in-alabama/ ; Stocktwits 5 May https://stocktwits.com/news-articles/markets/equity/dgxx-stock-soars-22-today-everything-to-know-about-the-data-center-agreement-with-nvidia-rival-cerebras/cZQDcbdRe9X ; Pleasants LOI https://www.newsquantified.com/dgxx/stock-report/digi-power-x-common-subordinate-voting-shares-enters-nonbinding-loi-with-omnis-0fh072
