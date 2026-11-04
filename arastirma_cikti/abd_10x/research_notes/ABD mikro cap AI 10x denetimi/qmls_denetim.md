# QumulusAI (Nasdaq: QMLS) — independent audit of financials, capital structure, contracts and financing, as of 4 November 2026

Scope note: all primary documents were pulled from SEC EDGAR (CIK 0002084026) on 4 Nov 2026 and read in full text. Company press releases are flagged "PR" and are NOT treated as independent proof. Secondary data providers (Yahoo Finance chart API, StockAnalysis, finviz news mirror) are flagged "secondary".

EDGAR filing index (official, complete as of 4 Nov 2026) — [EDGAR submissions JSON](https://data.sec.gov/submissions/CIK0002084026.json):
- 2025-12-31 S-1 (first public filing) … 2026-07-01 S-1/A; 2026-07-13 8-A12B; 2026-07-14 EFFECT; 2026-07-15 **424B4** (direct-listing resale prospectus); 2026-07-16 8-K (Items 3.03, 5.02, 5.03); 2026-07-21/27/29 Schedule 13G ×3; 2026-08-17 8-K (earnings date); 2026-08-25 8-K (Item 2.02, Q2 results) and **10-Q**; 2026-08-28 10-Q/A (XBRL only); 2026-08-31 S-8 ×2; 2026-09-22 8-K (Item 7.01, investor deck); 2026-10-20 Form 3/A; 2026-11-03 Schedule 13G; many Form 4s (2 Sept, 5 Oct, 13 Oct, 2 Nov 2026).
- **No S-3, no shelf, no ATM, no post-listing resale S-1, no 8-K for the 29 Sept contracts, the 15 Oct contract update or the 22 Oct equipment-financing expansion, no Item 3.01 (Nasdaq notice), no Item 5.02 after 16 July 2026.**

## Key question 1 — Q2 2026 and H1 2026 figures: verified or refuted?

### Takeaway
Every income-statement, balance-sheet and cash-flow number in the prior analysis is exact and official (10-Q filed 25 Aug 2026; identical figures in the 8-K Ex. 99.1 press release). The one item that exists ONLY in the press release is the GPU fleet count (952 → 3,088); it does not appear in the 10-Q.

### Cited Findings
- Q2 2026 total revenue $6,712,805 vs $3,085,439 in Q2 2025 (+118%); compute-power revenue $5,608,946 (84% of revenue) vs $1,311,700; crypto mining $410,081; mining hosting $693,778 — [10-Q, 25 Aug 2026, official, exact](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm); same numbers in [8-K Ex. 99.1 press release, 25 Aug 2026](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm)
- Gross profit $4,470k; gross margin 66.6% (Q1 2026: 37.5%; Q2 2025: 55.1%; H1 2026: 56.8%) — [8-K Ex. 99.1 summary table](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm) (cost of revenue $2,242,402 confirmed in [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm))
- Operating loss $(7,670,591) Q2; $(13,197,322) H1; D&A $6,882,154 in Q2 (vs $1,059,900) — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Net loss $(22,776,206) Q2; $(72,392,917) H1. Q2 includes "Loss on issuance of convertible note" $(19,241,000); H1 total of that line $(73,881,850). Also Q2 gains: change in FV of convertible note +$2,380,000; change in FV of additional-notes option +$3,850,850; interest expense, net $(2,045,748) — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Adjusted EBITDA (non-GAAP) $(782)k Q2; $(2,790)k Q1 2026; $(3,572)k H1 2026 — [8-K Ex. 99.1](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm) (company-defined non-GAAP; excludes finance-lease interest/amortization, which the company says will be ~$9.3M in rest of 2026 and ~$20.0M in 2027)
- EPS basic/diluted Q2 $(0.72); weighted-average basic shares 31,740,634 — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- H1 2026 cash flow: operating +$22,305,214; investing $(36,330,819) (PP&E purchases $(36,824,254), power-equipment deposits $(14,146,100), proceeds from sale of equity-method investment +$16,559,622); financing +$42,205,404 (convertible note proceeds $28,800,000; USD.AI loans net $20,268,245; common stock $5,980,834; finance-lease repayments $(6,518,746); debt issuance costs $(2,249,000)) — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Balance sheet 30 June 2026: cash $19,967,188; restricted cash $19,925,104; accounts receivable $11,058,423 (vs $57,889 at 31 Dec 2025); deferred revenue $30,460,939 (vs $0); total assets $215,002,216; total liabilities $215,783,480; total shareholders' deficit $(781,264) (attributable to QMLS shareholders $(3,567,675); NCI +$2,786,411); accumulated deficit $(109,788,460) — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- GPU fleet "grew from 952 to 3,088 (+224%)" and "8 MW of HPC capacity under executed lease and colocation agreements" — [8-K Ex. 99.1 press release only (furnished, not filed)](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm); the string "3,088" does not occur in the 10-Q — PR-only figure.
- 10-Q/A of 28 Aug 2026 only added inline XBRL; "No changes have been made to the registrant's Form 10-Q" — [10-Q/A](https://www.sec.gov/Archives/edgar/data/2084026/000162828026059295/qmls-20260630.htm)
- Remaining performance obligations (backlog) on direct compute contracts at 30 June 2026: $173,107,691, of which $34,368,785 to be recognised in 2026, remainder 2027-2029 — [10-Q Note 4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- "Cumulative signed customer contract value reaches $282.5 million" (as of 25 Aug 2026) — [PR in 8-K Ex. 99.1](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm) — PR metric, not a GAAP figure.

### Inferences
- The "non-cash loss tied to convertible notes" is accurately described: the $19.2M Q2 loss (and $54.6M in Q1) arises because the company elected fair-value accounting for the ATW notes and recorded the notes plus the "additional notes option" at fair values ($36.9M + $31.0M for the March tranche; $21.0M + $11.6M for the June tranche) far above the $15M cash received per tranche. The accounting loss is real in the sense that it measures how expensive the financing terms are.
- Negative equity ($-0.78M) is driven by $55.5M convertible-note fair value and $38.7M option liability; at face value ($30M principal) equity would be positive, but the liabilities reflect the instrument's variable conversion feature (see Q4).

### Gaps
- Q3 2026 (quarter ended 30 Sept 2026) financials are not yet filed; nothing after 30 June 2026 is audited or reviewed.

## Key question 2 — Is positive operating cash flow driven by customer prepayments (deferred revenue)? Quantify.

### Takeaway
Yes. H1 2026 operating cash flow of +$22.3M includes +$30.46M from deferred revenue (customer upfront payments); excluding that single working-capital item, operating cash flow was about −$8.2M. The company itself states the OCF was driven by customers "committing and paying ahead of delivery".

### Cited Findings
- Cash-flow statement line "Deferred revenue 30,460,939" within operating activities; net OCF $22,305,214; also AR growth $(11,302,778) and AP growth +$6,298,796 — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- CFO quote: "Customers are also committing and paying ahead of delivery — deferred revenue rose $30.5 million in the first half, contributing to $22.3 million of operating cash flow." — [PR in 8-K Ex. 99.1](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm)
- Upfront payments disclosed per contract: 11 May 2026 $99.6M/3-yr contract, upfront ~$16.9M; 28 May $19.8M/3-yr, upfront ~$4.9M; 29 June $18.0M/2-yr, upfront ~$3.7M; 22 July $32.0M/2-yr, upfront ~$6.5M; 25 July $71.9M/3-yr, upfront ~$14.4M — [10-Q MD&A and Note 26](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Going-concern note: "entered into multiple significant revenue contracts in July 2026 for approximately $103,900,000 in future revenue in which the Company received approximately $20,900,000 in cash deposits" — [10-Q Note 1](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)

### Inferences
- OCF ex-deferred-revenue ≈ $22.3M − $30.5M = −$8.2M (my arithmetic from the 10-Q lines). Cash paid for interest in H1 was $2,229,681. Upfront deposits run ~17-25% of contract value and are a structural feature of the model; they fund the ~10-15% equity portion of the TFC equipment leases (see Q5).
- Deferred revenue is a performance obligation (GPU hours to deliver), not free cash; it will unwind into revenue without cash.

### Gaps
- No Q3 deferred-revenue figure yet; the ~$20.9M July deposits suggest deferred revenue rose further in Q3, but this is unverified until the Q3 10-Q.

## Key question 3 — Going-concern or liquidity-risk language in filings?

### Takeaway
Yes, explicitly. The 10-Q (Note 1 and MD&A) states that conditions "raise substantial doubt about the Company's ability to continue as a going concern" and that management's plans (release of $19.9M restricted cash on listing, $15.3M USD.AI draw, July contract deposits) alleviate that doubt. The risk-factor summary also lists "The Company may be unable to continue as a going concern."

### Cited Findings
- "These factors raise substantial doubt about the Company's ability to continue as a going concern for a period of one year from the issuance of these unaudited condensed consolidated financial statements." Plans: access to $19,925,104 restricted cash upon listing; additional $15,300,000 USD.AI draw; ~$103.9M July contracts with ~$20.9M deposits; "management concluded these plans will alleviate the substantial doubt" — [10-Q Note 1 "Going Concern" and MD&A "Going Concern, Liquidity and Capital Resources"](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Risk-factor bullet: "The Company may be unable to continue as a going concern." — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Direct listing completed 16 July 2026 and "the Company has received access to $19,925,104 in previously restricted funds"; $15.3M USD.AI draw completed 7 Aug 2026 — [10-Q Note 26](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- ATW notes carry "financial covenants (including minimum liquidity requirements)", negative covenants restricting additional senior/secured debt and variable-rate transactions, first-priority lien on personal property and pledge of the three subsidiaries — [424B4, 15 July 2026](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm)
- Risk factor: "USD.AI financing arrangement may not provide any future funding, remains subject to various approvals and documentation" — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)

### Inferences
- Pro-forma liquidity after listing: ~$19.97M + $19.93M + $15.3M ≈ $55M (early Aug 2026) before Q3 capex; against finance-lease payments of ~$9.3M (rest of 2026) and ~$20.0M (2027) per the Adjusted-EBITDA disclosure, plus the $2.0M related-party note that matured 1 Oct 2026 (no 8-K on repayment/extension).

### Gaps
- Whether the $2.0M Trailhead Income LP note (12%, matured 1 Oct 2026) was repaid or extended is not disclosed anywhere yet.
- No Q3 cash balance disclosed; the 15 Oct and 22 Oct press releases give no cash figure.

## Key question 4 — Capital structure, share count, ALL dilutive instruments, lock-up, resale registration

### Takeaway
Latest official cover-page count is 33,458,515 shares (20 Aug 2026). The listing was a DIRECT LISTING (not an IPO): no shares sold by the company, no underwriters, no proceeds. The dominant dilution source is the $30M ATW senior secured convertible, which amortises monthly in shares at the lower of the fixed price and 93% of the lowest 8-day VWAP — at a ~$3.5 share price this is roughly 8M shares for the remaining ~$27M. Insider/affiliate lock-up (12.68M shares + 0.61M underlying) expires 180 days after 16 July 2026, i.e. ~12 January 2027; all other shares were already freely resalable under the 424B4.

### Cited Findings
- Cover page: "As of August 20, 2026, there were 33,458,515 shares of common stock of the registrant outstanding." Balance sheet: 31,727,001 shares at 30 June 2026 (31,367,559 at 31 Dec 2025); 500,000,000 authorised at 30 June; authorised raised to 1,000,000,000 common + 100,000,000 preferred on 14 July 2026 — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Bridge 31,727,001 → 33,458,515: 1,140,930 shares issued to Chardan Capital Markets LLC (financial adviser) immediately before effectiveness → 32,867,931 — [424B4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm); plus "As of August 20, 2026, $3.1 million of outstanding principal on the convertible notes were converted into 590,584 shares" — [10-Q Note 26](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm). 32,867,931 + 590,584 = 33,458,515 exactly (my arithmetic).
- Listing mechanics: "This prospectus relates to the registration of the resale of up to 39,472,531 shares of our common stock by ... the Registered Shareholders, in connection with our direct listing on the Nasdaq Global Market"; "Unlike an initial public offering, the resale by the Registered Shareholders is not being underwritten by any investment bank"; "There are no underwriters engaged on a firm-commitment basis"; Chardan Capital Markets LLC = financial adviser; company receives no proceeds — [424B4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm)
- Trading began 16 July 2026 on Nasdaq Global Market ("QMLS") — [10-Q Note 26](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm); first-day open $38.00, high $38.00, low $14.07, close $21.43, volume 128,300 — [Yahoo Finance chart API, secondary](https://query1.finance.yahoo.com/v8/finance/chart/QMLS?range=1y&interval=1d)
- Lock-up: "Our directors, officers and greater than 10% shareholders have entered into contractual lock-up agreements with respect to an aggregate of 12,678,323 shares of common stock, plus 610,376 shares of common stock underlying options and warrants ... until 180 days following the date the common stock is first listed"; "Substantially all of the remaining shares may be immediately sold either by the Registered Shareholders pursuant to this prospectus or by our other existing shareholders under Rule 144" — [424B4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm). 16 July 2026 + 180 days = 12 January 2027 (my arithmetic); 90-day Exchange Act reporting threshold for Rule 144 passed 14 Oct 2026.
- ATW convertible notes (holder: ATW AI Opportunities LLC): two $45M facilities (26 Mar 2026 and 3 Jun 2026), $15M first tranche funded under each (4% OID), 7% interest, "subsequent tranches in an aggregate principal amount of up to $60,000,000 ('Green Shoe'), which are callable by us subject to certain funding conditions"; maturity auto-extended to 2nd anniversary of listing (16 July 2028); fixed conversion $11.50 (March note) / $24.25 (June note), $17.00 / $30.00 for Green Shoe, with full-ratchet-style "price match if we issue equity at a lower price"; **"Beginning on the Public Listing Date, we will make equal monthly redemptions of the balance of the initial principal amount together with accrued interest in shares, subject to equity conditions, or in cash at our option at no premium. If monthly redemptions are made in shares, the conversion price shall be the lower of (i) the Fixed Conversion Price and (ii) 93% of the lowest daily VWAP during the eight trading days prior to each conversion. The Investor has the right to accelerate up to four payments ... in shares at any time per month."** Investor sale limit: higher of 15% of daily volume or $350,000/day; 4.99% beneficial-ownership cap; 24-month right to co-invest ≥15% of future financings; senior secured, first-priority lien — [424B4 "$90 Million Senior Secured Convertible Notes Facility"](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm); same terms repeated in [10-Q MD&A](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Carrying values at 30 June 2026: convertible note payable $55,481,000 (fair value option); "additional convertible notes option liability" $38,721,000; warrant liability $2,968,793 — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Anti-dilutive securities excluded from EPS (Q2 2026): warrants 722,671; stock options 1,182,034; convertible note 1,494,673 (at fixed conversion prices) — [10-Q Note 22](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Options: 1,182,034 outstanding at 30 June 2026, weighted-average exercise price $1.93, 8.2-yr remaining life, intrinsic value $27,103,204; 1,129,595 exercisable; no grants in H1 2026 — [10-Q Note 21](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Warrants: 851,079 outstanding at 30 June 2026 (763,558 at 31 Dec 2025 with WAEP $4.20; granted 91,688 in H1 at WAEP $23.15 incl. 86,393 issued 1 May 2026 "to a customer as consideration for entering into a contract"; 4,167 exercised); Type 1 "penny warrants" ($0.03 post-split) classified as liability, "961,256 of the warrants are pre-funded warrants" (historical count); 16,668 more warrants at $10.80 issued 5 Aug 2026 — [10-Q Notes 20 and 26](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- 2026 Equity Incentive Plan: 4,770,000-share initial pool, evergreen +5% of outstanding each 1 Jan 2027-2036; registered on Form S-8 (31 Aug 2026) — [10-Q Note 26](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm); [S-8](https://www.sec.gov/Archives/edgar/data/2084026/000143774926029249/quma20260717_s8.htm)
- RSU grants 1 Sept 2026 (Form 4s filed 2-3 Sept 2026, price $0, "Common Stock" acquisitions with RSU footnotes): CEO Maniscalco 127,768 + 303,406; CFO Krosnowski 85,179 + 103,934 + 122,400; Chatterjee 238,444; Gahan 275,479; Hunton 163,870; Gertz 195,289; DiRocco 189,229; Aderhold 85,690; Glickler 70,273; directors Mulica, Rench, Schwartz 19,166 each, Akbari 15,621, Kenworthy 15,572 — sum ≈ 2.05M RSUs (my arithmetic) — e.g. [Maniscalco Form 4](https://www.sec.gov/Archives/edgar/data/2084026/000198536726000002/), [Krosnowski Form 4](https://www.sec.gov/Archives/edgar/data/2084026/000209725926000002/)
- Insider option exercises 29 Oct–2 Nov 2026 (all code "M", no sales reported): Gahan 36,165 @ $3.00-3.30; Krosnowski 88,766 @ $0.36-3.00; Schwartz 479 @ $0.69; Hunton 2,998 @ $0.69. Aderhold gifted 15,000 shares 9 Oct 2026 (post: 5,651,909) — [Form 4s filed 2 Nov 2026](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002084026&type=4&owner=include&count=40). No open-market insider sales appear in any Form 4 to date.
- Preferred stock: none outstanding since 30 Sept 2025 conversion; no earnouts disclosed — [10-Q Note 19](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- SAFE: $1.0M SAFE issued 1 May 2026 to a supply/sales counterparty, converts at a 20% discount to the next equity financing — [424B4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm)
- Large holders (Schedule 13G): Michael Houston Aderhold 5,677,512 sole (27 Jul 2026); Robert C. Bissell 1,756,575 sole + 4,101,909 shared (21 Jul 2026); Alder Opportunity LP / Craig Heiser 1,856,079 shared (29 Jul 2026); Focus Partners Wealth (IA) 1,909,195.5 sole (filed 3 Nov 2026) — [EDGAR filing index](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002084026&owner=include&count=40)

### Inferences (fully diluted share count scenarios — my estimates)
- Base: 33.46M (official, 20 Aug 2026).
- LOW ≈ 39.2M: base + options 1.18M + warrants ~0.87M + Sept RSUs ~2.05M + ATW remaining ~$26.9M converted at fixed $11.50/$24.25 (~1.6M).
- MID ≈ 46M: as LOW but ATW remaining principal converted via monthly redemptions at 93% of VWAP around $3.5 (≈$3.29 → ~8.2M shares) + SAFE ~0.3M. The already-completed conversion ($3.1M → 590,584 shares = $5.25/share, below the $11.50 fixed price) proves the VWAP mechanism is in use.
- HIGH ≈ 75-80M: MID but with share price ~$2.50 (ATW ~11.6M shares), full 4.77M plan pool, and the $60M Green Shoe drawn and redeemed in shares at ~$2.3 (~26M). Green Shoe is at the company's call subject to conditions, so this is a contingent scenario; the $38.7M "additional notes option" liability on the balance sheet shows the auditors value that option highly.
- Monthly redemption schedule: $30M principal + 7% interest over 24 months from 16 July 2026 ≈ $1.3-1.4M/month; at $3.29 that is ~400k+ shares/month, i.e. ~1.2% of the float per month sold under the 15%-of-volume / $350k-per-day cap — continuous selling pressure through July 2028 unless the company pays cash.
- Nov 2026–Jan 2027 overhang: (i) continuous ATW redemptions; (ii) Rule 144 now open for affiliates since 14 Oct 2026 (except locked-up holders); (iii) lock-up expiry ~12 Jan 2027 frees 12.68M shares (~38% of outstanding) held by directors, officers and >10% holders (Aderhold, Bissell families, Alder). No new resale registration is needed because the 424B4 already registered 39.47M shares.

### Gaps
- Exact ATW outstanding principal after 20 Aug 2026 and conversions in Sept-Oct are undisclosed (no 8-K; Form 4 not required of ATW under 4.99% cap). Next data point: Q3 10-Q cover page.
- Whether the company elected cash instead of shares for any monthly redemption is undisclosed.
- Warrant WAEP at 30 June 2026 is truncated in the 10-Q table extraction; count (851,079) is reliable.

## Key question 5 — Debt instruments, equipment financing, net debt and EV

### Takeaway
At 30 June 2026 interest-bearing obligations at face were ≈$104M (notes $9.1M, USD.AI $18.9M, finance leases $45.8M, ATW principal $30M) against $39.9M cash+restricted → net debt ≈$64M (face basis), ≈$89M on carrying values. Post-quarter, USD.AI +$15.3M (cash-neutral) and the TFC lease expansion to ~$123.6M (PR only) add roughly $100M of lease obligations. EV at $3.54 is ≈$180M on June figures and plausibly ≈$280M pro forma — entirely estimate.

### Cited Findings
- Notes payable at 30 June 2026: commercial-bank equipment loan $4,850,282 (prime, 5% floor, monthly $129,552, matures Jan 2030); related-party Trailhead Income LP $2,000,000 (12%, interest-only, extended to 1 Oct 2026, secured by mining equipment); Caterpillar $19,464 (1.49%, Apr 2027); third-party term loan $2,209,930 (SOFR+3.0%, Apr 2028). Balance sheet: current $1,158,583 + related-party current $2,000,000 + long-term $5,917,155 — [10-Q Note 16](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- USD.AI protocol: "$500,000,000 USD.AI protocol ... borrow stablecoins against up to 70% of its approved GPU deployments"; draws $4,282,000 (13 Feb 2026, matures Feb 2029) and $16,400,000 (17 Apr 2026, matures Apr 2029); balance $18,913,377 at 30 June (current $6,892,685 + LT $12,020,692); Q2 interest $468,363; further $15.3M drawn 7 Aug 2026 — [10-Q Notes 14, 26](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm). (Implied rate ≈10% annualised on ~$19M — my estimate.)
- Finance lease liabilities $13,067,517 current + $32,708,652 LT = $45,776,169; finance ROU assets $47,919,004; "Acquisition of right-of-use asset in exchange for lease obligations $45,504,172" in H1 — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Master Lease Agreement 10 Apr 2026 with "a third party" for servers: 3-year terms, purchase option, initial payment ~$2.6M, remaining fixed payments $26.0M for leases entered by 1 May 2026 — [10-Q Note 25](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm); the $26M counterparty is named as Tech Finance Co. (TFC) only in [PR, 7 May 2026 (secondary mirror)](https://www.newswire.com/news/qumulusai-secures-26m-multi-year-lease-financing-for-50-node-nvidia-22776033)
- TFC expansion: "expanded its equipment lease financing with Tech Finance Co., LLC ('TFC') to approximately $123.6 million, up from the $26.0 million announced May 7, 2026"; 3-year leases; TFC financed 85-90% of equipment cost per schedule, customer deposits funded the balance; end-of-term buy-or-return option; "amortized lease payment schedules imply a high single-digit annualized interest rate"; no new equity issued; covers Blackwell GPUs bought May and July 2026 — [PR 22 Oct 2026, company PDF (image-only)](https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Expands-Closed-Lease-Financing-With-TFC-to-123-6-Million-Funding-Its-NVIDIA-Blackwell-GPUs-Without-New-Equity-2026.pdf); text via [finviz mirror, secondary](https://finviz.com/news/406325/qumulusai-expands-closed-lease-financing-with-tfc-to-1236-million-funding-its-nvidia-blackwell-gpus-without-new-equity). **No 8-K was filed for this; PR-only.**
- ATW notes: $30M principal funded (two $15M tranches), 7%, 4% OID, mature 16 July 2028 (2nd anniversary of listing), senior secured; carrying value $55,481,000 — [424B4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm), [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- "As of March 31, 2026, our total indebtedness, excluding warrant liability of $2,968,793, additional convertible note option liability of $30,991,850 and embedded features valued at $22,475,000 ... was $45,915,444" — [424B4 risk factor](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm)
- Operating lease liabilities $106,795 current + $1,459,005 LT; dividend payable $359,188 — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Market cap $118.44M at $3.54 close (3 Nov 2026), 33.46M shares — [StockAnalysis, secondary](https://stockanalysis.com/stocks/qmls/)

### Inferences
- Net debt (30 June 2026, face): 9.08 + 18.91 + 45.78 + 30.0 = $103.8M − cash $39.9M = ≈$63.9M. On carrying values (ATW at $55.5M fair value, excl. the $38.7M option and $3.0M warrant liabilities): ≈$89M. EV ≈ $118M + $64M = ≈$182M (June balance sheet) → EV/annualised Q2 revenue ≈ 6.8×; EV/"implied ARR $209M" ≈ 0.9× (ARR is a PR figure, mostly not yet billing).
- Pro forma for TFC expansion (+~$97.6M lease obligations, PR-only) and USD.AI (+$15.3M debt, +$15.3M cash): net debt ≈ $160M, EV ≈ $280M. This is an estimate; the Q3 10-Q will give the actual lease liability.
- Effective cost of capital is high across the stack: ATW 7% coupon + 4% OID + 7% VWAP discount + fair-value loss; USD.AI ≈10%; TFC "high single-digit"; legacy notes 12%.

### Gaps
- No official figure for total finance-lease obligations after the TFC expansion; the $123.6M figure is from a press release without an 8-K or exhibit.
- Status of the $2.0M related-party note that matured 1 Oct 2026 — undisclosed.

## Key question 6 — 15 Oct 2026 contract announcement ($523.4M etc.) and customers / creditworthiness

### Takeaway
All 15 Oct figures ($523.4M signed value, ~$209M implied initial-term ARR, 11.75 MW contracted, 7 MW billing, 1 MW end-October, 3.75 MW Atlanta early 2027, one customer $283.8M = 54.2%) are confirmed as stated in the company's press release — and ONLY there. No 8-K, no contract exhibit, no customer name. The filed record supports $173.1M of RPO at 30 June and the July contracts ($32.0M, $71.9M); the September $240.9M of contracts exists only in press releases. Four customers produced 90% of Q2 revenue; no evidence of the largest customer's identity or creditworthiness exists in any filing.

### Cited Findings
- 15 Oct 2026 PR: $71.9M three-year Blackwell agreement fully in production and billing "10 weeks after signing" (B200 delivered 8 Sept; B300 at Kansas City 1 Oct); 11.75 MW contracted across six colocation sites; 7 MW active and billing; 1 MW energised, final handoff end-October → 8 MW active; 3.75 MW metro Atlanta targeted early 2027; $211.9M three-year take-or-pay Atlanta agreement "sold in September"; $29.1M agreement at an additional site; September agreements total $240.9M; cumulative signed contract value $523.4M (+85% from $282.5M); ~$209M ARR on initial terms excl. extensions (~$128M from the 8 MW, ~$71M Atlanta, balance from $29.1M deal); largest customer's two agreements total $283.8M excl. extensions; no customer names — [company PR PDF, 15 Oct 2026 (image-only)](https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Puts-71-9-Million-Blackwell-Agreement-into-Production-Signed-Customer-Contracts-Surpass-500-Million-2026.pdf); text via [finviz mirror, secondary](https://finviz.com/news/402901/qumulusai-puts-719-million-blackwell-agreement-into-production-signed-customer-contracts-surpass-500-million). $283.8M / $523.4M = 54.2% (my arithmetic).
- 29 Sept 2026 PR: $240.9M across two agreements, >2,000 B300 GPUs in two dedicated clusters; $211.9M/3-yr for "an AI inference platform" (its second agreement; two one-year extension options of $70.6M each → up to $353.1M); $29.1M/3-yr for "a generative-AI inference platform" (capacity expected Dec 2026; extension $19.4M; that customer's commitments >$61M) — [company PR PDF, 29 Sept 2026](https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Signs-240-9-Million-in-New-AI-Inference-Customer-Contracts-for-NVIDIA-Blackwell-B300-Capacity-2026.pdf) (PR; summarised via web search, not independently verified)
- Filed contract disclosures (10-Q): 11 May $99.6M/3-yr (128 B300 nodes); 28 May $19.8M/3-yr (32 B200 nodes); 29 June $18.0M/2-yr (32 B300 nodes); 22 July $32.0M/2-yr (56 B300 nodes); 25 July $71.9M/3-yr; all with upfront payments; "Signed 21 new direct customer AI compute contracts during the quarter with aggregate expected take-or-pay contract value of $169.7 million" — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm); [PR 8-K Ex. 99.1](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm)
- Customer concentration: "During the three months ended June 30, 2026, the Company had four customers that accounted for approximately 90% of the Company's total revenues" (86% for H1) — [10-Q Note 2](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Named counterparties anywhere: DRW ("a diversified trading firm") GPU-as-a-Service agreement — [PR 8-K Ex. 99.1 only](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm); RunPod marketplace (80/20 revenue share) and colocation providers CoreSite, H5, NOCIX; Connected Nation IXP license (14 Jan 2026); Moonshot Energy JV — [10-Q MD&A](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm), [424B4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm)
- A customer was paid in warrants: "On May 1, 2026 the Company issued 86,393 warrants to a customer as consideration for entering into a contract"; "Issuance of warrants as consideration payable to customer $192,512" — [10-Q Note 20, cash-flow statement](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Allowance for credit losses rose from $2,263 to $365,133; bad-debt expense $302,244 in H1 2026 — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)
- Atlanta site: colocation agreement for up to 3.75 MW with right of first offer on up to 7 MW more (seven-year term per PR) — [PR 8-K Ex. 99.1](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm); 7-year term only in [PR, Aug 2026, secondary mirror](https://finviz.com/news/384152/qumulusai-secures-seven-year-atlanta-data-centre-deal-for-up-to-375-mw)

### Inferences
- "Implied ARR $209M" is a company construct: ~$81M of it (Atlanta $71M + part of $29.1M) is not billing before Dec 2026/early 2027 and depends on delivery of >2,000 B300 GPUs that need the TFC financing and 10-15% customer deposits. Only the ~$128M tied to 8 MW is near-term; even that is a run-rate, versus $6.7M actual Q2 revenue ($26.9M annualised).
- The $283.8M customer is an anonymous "AI inference platform"; its $71.9M contract required a ~$14.4M (20%) upfront payment, which is the only hard evidence of its ability to pay. No rating, no name, no guarantee, no audited financials disclosed. Contract value is "take-or-pay" per PR, but the filed 10-Q does not include the contracts as exhibits.
- Material-contract 8-Ks (Item 1.01) were not filed for the $211.9M or $29.1M agreements, nor for the TFC expansion — the company treats them as ordinary-course; investors have only press releases.

### Gaps
- Customer identity and creditworthiness: no primary evidence. Not answerable from public sources.
- The 22 Sept 2026 investor presentation (8-K Ex. 99.1) is image-only; not read.
- The Q2 call transcript (on IR site) was not retrievable; it may contain additional customer colour.

## Key question 7 — hosted.ai relationship

### Takeaway
It is a software LICENSE plus revenue-sharing collaboration, not a JV and not an equity investment; fees are paid BY QumulusAI TO hosted.ai ($10k-$168k per month depending on GPUs deployed). No revenue from hosted.ai is disclosed, and the 10-Q does not mention it.

### Cited Findings
- "We have entered into a license agreement with hosted.ai to provide software that manages GPU resource allocation, scheduling, scaling, and access ... The license has an initial two-year term with fees that scale based on the number of GPUs deployed on the hosted.ai platform. ... fees begin at $10,000 per month for up to 64 NVIDIA B200 level GPUs and increase in tiers up to $168,000 per month if 256 or more NVIDIA B200 level GPUs are deployed, or after 12 months from the effective date, whichever occurs first ... Renewal fees ... capped at no more than double the maximum fee from the prior term" — [424B4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm)
- "The exclusive partnership enables us to build a next-generation multi-tenant inference cloud ... GPU overcommitment"; "hosted.ai, whose software platform is currently in an early (alpha) stage of development"; "subject to agreed-upon governance, licensing, exclusivity, revenue-sharing, and intellectual property provisions" — [424B4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm)
- The string "hosted.ai" does not appear in the 10-Q; web search finds no press release on the partnership — [10-Q](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm)

### Inferences
- Alpha-stage software with a minimum fee ramp to $168k/month after 12 months regardless of deployment is a cost commitment (~$2M/yr) with unproven benefit; revenue-share terms are not quantified.

### Gaps
- Revenue-share percentage, effective date, and exclusivity scope are not disclosed.

## Key question 8 — Share price, market cap, performance; Q3 10-Q date; post-1 Sept 8-Ks; Nasdaq notices

### Takeaway
QMLS closed $3.54 on 3 Nov 2026 (market cap ≈$118M), down 46% over 30 days, 40% over 60 days, 41% over 90 days, 83.5% from the first-day close ($21.43) and 90.7% from the first print ($38.00). No company event explains the mid-October slide; it coincides with the ATW redemption period and the 14 Oct Rule 144 window opening. No Q3 results date has been announced; data providers estimate 25 Nov 2026. The only 8-K after 1 Sept is the 22 Sept investor deck; there are no Nasdaq notices or management-change filings.

### Cited Findings
- Close 3 Nov 2026 $3.54 (after-hours $3.49); market cap $118.44M; shares 33.46M; 52-week range $3.10-$38.00; "Est. Earnings Nov 25, 2026" — [StockAnalysis, secondary, checked 4 Nov 2026](https://stockanalysis.com/stocks/qmls/)
- Daily closes (Yahoo chart API, secondary): 16 Jul $21.43 (O 38.00, L 14.07); 17 Jul $14.28; 21 Jul $6.81; 5 Aug $6.04; 25 Aug $6.27 (Q2 results day); 4 Sep $5.90; 21 Sep $8.10 (highest close after July; intraday high $8.40 on 23 Sep); 2 Oct $6.53; 6 Oct $6.16; 14 Oct $3.74; 15 Oct $4.08 (contract-update day); 22 Oct $3.41 (TFC day); 26 Oct $3.14 (lowest close); 3 Nov $3.54 — [Yahoo Finance](https://query1.finance.yahoo.com/v8/finance/chart/QMLS?range=1y&interval=1d)
- Performance to 3 Nov 2026 (my arithmetic from the same series): 30-day (vs 2 Oct $6.53) −45.8%; 60-day (vs 4 Sep $5.90) −40.0%; 90-day (vs 5 Aug $6.04) −41.4%; since first close −83.5%; since first print −90.7%.
- Secondary commentary: stock "down 50.62% so far this month" with October high $6.93 / low $3.14 (as of 23-25 Oct) — [AAII, secondary](https://www.aaii.com/investingideas/article/551867-why-qumulusai-inc8217s-qmls-stock-is-down-1362); no news source identifies a cause.
- Only 8-K since 1 Sept 2026: 22 Sept 2026, Item 7.01, investor presentation furnished as Ex. 99.1 — [8-K](https://www.sec.gov/Archives/edgar/data/2084026/000143774926030947/quma20260911_8k.htm). No Item 1.01, 2.03, 3.01, 5.02 or 2.02 filings after 25 Aug 2026 — [EDGAR index](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002084026&owner=include&count=40)
- Q2 results date was announced by 8-K/PR eight days ahead (17 Aug for 25 Aug) — [8-K 17 Aug 2026](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028108/ex_1005855.htm); no equivalent 8-K for Q3 exists as of 4 Nov 2026; IR events page returned no events.
- Form 3/A filed 20 Oct 2026 (one insider correcting initial holdings) — [EDGAR index](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002084026&owner=include&count=40)

### Inferences
- As a non-accelerated filer in its first year, the Q3 10-Q deadline is 45 days after 30 Sept = 16 Nov 2026 (statutory), extendable 5 days by NT 10-Q to 23 Nov. The "25 Nov" date in data providers is an estimate and would be late relative to the 45-day rule unless an NT 10-Q is filed; treat as unconfirmed.
- Price fell from $6.53 to $3.14 (−52%) between 2 Oct and 26 Oct with no filing and two positive PRs; the consistent sellers permitted in that window are ATW (monthly redemption shares at 93% of lowest VWAP, capped at 15% of volume) and, from 14 Oct, affiliates under Rule 144. No short report was found. Causation is not established.
- Nasdaq listing-standard risk: price is well above $1 and no deficiency notice is on file; the main risk is the Nasdaq Global Market stockholders'-equity / market-value standards if equity stays negative — not yet flagged by the company.

### Gaps
- No confirmed Q3 2026 results date.
- Insider holdings: no Form 4 sales to date; whether affiliates sold under Rule 144 after 14 Oct is unknowable until Form 144/Form 4 filings appear (none filed).
- Short interest: only secondary (≈1.0M shares, 1.5 days to cover, per massive.com via search) — not verified.

## Source list (primary unless marked)
1. EDGAR submissions index (official): https://data.sec.gov/submissions/CIK0002084026.json
2. 10-Q for quarter ended 30 June 2026, filed 25 Aug 2026 (official, exact): https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm
3. 10-Q/A, 28 Aug 2026 (XBRL-only amendment): https://www.sec.gov/Archives/edgar/data/2084026/000162828026059295/qmls-20260630.htm
4. 8-K Item 2.02 + Ex. 99.1 Q2 press release, 25 Aug 2026 (furnished; PR): https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm
5. 8-K Ex. 99.1 results-date release, 17 Aug 2026 (PR): https://www.sec.gov/Archives/edgar/data/2084026/000143774926028108/ex_1005855.htm
6. 8-K Item 7.01, 22 Sept 2026 (investor deck, image-only): https://www.sec.gov/Archives/edgar/data/2084026/000143774926030947/quma20260911_8k.htm
7. 424B4 direct-listing prospectus, 15 July 2026 (official): https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm
8. S-8, 31 Aug 2026 (4,770,000 shares, 2026 Plan): https://www.sec.gov/Archives/edgar/data/2084026/000143774926029249/quma20260717_s8.htm
9. Schedule 13G filings (Aderhold 27 Jul; Bissell 21 Jul; Alder/Heiser 29 Jul; Focus Partners Wealth 3 Nov 2026) and Form 4s (2 Sept, 5 Oct, 13 Oct, 2 Nov 2026): https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002084026&owner=include&count=40
10. Company PR 15 Oct 2026 (image PDF; PR): https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Puts-71-9-Million-Blackwell-Agreement-into-Production-Signed-Customer-Contracts-Surpass-500-Million-2026.pdf — text mirror (secondary): https://finviz.com/news/402901/qumulusai-puts-719-million-blackwell-agreement-into-production-signed-customer-contracts-surpass-500-million
11. Company PR 22 Oct 2026 TFC expansion (image PDF; PR): https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Expands-Closed-Lease-Financing-With-TFC-to-123-6-Million-Funding-Its-NVIDIA-Blackwell-GPUs-Without-New-Equity-2026.pdf — text mirror (secondary): https://finviz.com/news/406325/qumulusai-expands-closed-lease-financing-with-tfc-to-1236-million-funding-its-nvidia-blackwell-gpus-without-new-equity
12. Company PR 29 Sept 2026 $240.9M contracts (PR): https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Signs-240-9-Million-in-New-AI-Inference-Customer-Contracts-for-NVIDIA-Blackwell-B300-Capacity-2026.pdf
13. Company PR 7 May 2026 $26M TFC lease (PR, secondary mirror): https://www.newswire.com/news/qumulusai-secures-26m-multi-year-lease-financing-for-50-node-nvidia-22776033
14. Yahoo Finance chart API, daily OHLC 16 Jul–3 Nov 2026 (secondary): https://query1.finance.yahoo.com/v8/finance/chart/QMLS?range=1y&interval=1d
15. StockAnalysis quote page, checked 4 Nov 2026 (secondary): https://stockanalysis.com/stocks/qmls/ and history: https://stockanalysis.com/stocks/qmls/history/
16. AAII note on October decline (secondary): https://www.aaii.com/investingideas/article/551867-why-qumulusai-inc8217s-qmls-stock-is-down-1362
