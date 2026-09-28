# -*- coding: utf-8 -*-
PAGES = []
G = "07 · Real-World Problems"

def page(**kw):
    kw.setdefault("group", G)
    PAGES.append(kw)

page(
    id="sectors-intro",
    title="How to Use the Problem Library",
    sub="Sector playbook",
    eyebrow="REAL-WORLD PROBLEMS",
    subtitle="Sixty briefs across ten sectors. Each is a real, unsolved or badly-solved problem where your skills produce measurable value.",
    chips=["10 sectors", "60 briefs", "Build · pitch · sell"],
    track=False,
    body=r"""
## Why the sector matters more than the stack

Two developers know React. One says "I build web apps." The other says "I build claims-processing systems for HMOs and I understand NHIS reimbursement cycles." The second one is not competing on price with a thousand other developers. **Domain knowledge is the moat**, and it is the thing AI is worst at replacing, because it lives in messy human context, not in documentation.

Pick **one primary sector** by week 12 and go deep. Read its trade press, learn its regulations, understand its money flows, and talk to people who work in it. Build two projects in it. By week 26 you will be able to speak the language of buyers in that sector, which is worth more than another framework.

## How each brief is structured

Every problem below gives you: **the pain** (what is actually broken and who suffers), **the solution shape** (what you would build), **the skills exercised**, and **the value** (how you would justify the price). Use them as portfolio projects, freelance pitches, or startup ideas.

## How to validate before you build

1. **Find five people with the problem.** Not friends — actual practitioners. WhatsApp groups, trade associations, LinkedIn, market visits.
2. **Ask about their last week, not your idea.** "Walk me through how you handled X last Tuesday." Watch what they actually do; people describe their processes inaccurately but demonstrate them honestly.
3. **Find the spreadsheet.** Almost every business problem is currently held together by an Excel file, a WhatsApp group, and one overworked person. That file is your specification.
4. **Quantify the pain in money or hours.** If you cannot, they will not pay.
5. **Sell before you build.** A signed letter of intent or a small deposit validates far better than a survey.

:::edge The consulting positioning that changes your income
Do not sell "web development" — an hourly commodity. Sell **an outcome in a sector**: "I cut reconciliation time for microfinance banks from 3 days to 20 minutes." Same code, five times the rate, and clients who come to you. Every project in this library is framed as an outcome for exactly this reason. Write your case studies the same way: situation → what you built → measured result.
:::

## The sectors covered

++ Fintech & Banking :: Payments, lending, reconciliation, fraud, agency banking, compliance.
++ Healthcare :: Clinic operations, claims, supply chain, telemedicine, records, public health.
++ Agriculture :: Market prices, input finance, yield, cold chain, traceability, weather.
++ Logistics & Supply Chain :: Routing, fleet, last-mile, warehousing, freight matching, customs.
++ Education :: School operations, learning analytics, assessment, skills matching, EdTech.
++ Retail & E-commerce :: Inventory, POS, pricing, demand forecasting, customer analytics.
++ Energy & Utilities :: Metering, outage analytics, solar financing, fuel logistics, efficiency.
++ Government & Public Sector :: Procurement transparency, revenue, service delivery, open data.
++ Real Estate & Construction :: Listings integrity, project cost control, facility management.
++ NGO & Development :: M&E systems, beneficiary management, impact measurement, grant reporting.
""",
)

page(
    id="sec-fintech",
    title="Fintech & Banking",
    sub="8 problem briefs",
    eyebrow="SECTOR 01",
    subtitle="The largest tech employer and highest-paying sector in Nigeria, and a global remote market. Payment correctness skills are directly monetizable.",
    chips=["High pay", "High regulation", "Immediate freelance demand"],
    body=r"""
## 1 · Reconciliation automation for microfinance banks and fintechs

**The pain:** Finance teams reconcile provider settlement files against internal records manually in Excel — often 2–3 days per month, error-prone, and discrepancies get discovered weeks late. Missing money is found by accident.
**Build:** An ingestion service for provider settlement files (CSV/Excel/API) and internal ledger extracts, a matching engine (exact on reference, then fuzzy on amount+date+counterparty), an exception queue with assignment and resolution notes, an audit trail, and a daily summary email. Add a dashboard for unmatched value by age.
**Skills:** Node/Python ingestion, matching algorithms, Postgres, background jobs, ledger modeling, dashboards.
**Value:** "3 days → 20 minutes, with discrepancies caught same-day instead of month-end." Easily justifies ₦2–8M for a build, or a monthly SaaS fee.

## 2 · Agency banking commission and float management

**The pain:** Agent networks (POS operators) struggle with float allocation, commission disputes, and knowing which agents are underperforming or committing fraud. Super-agents manage hundreds of agents on WhatsApp and spreadsheets.
**Build:** An agent portal with real-time float balance, transaction history, commission calculation with a transparent rule engine, float request/approval workflow, and an anomaly detector for suspicious patterns (round-number transactions, same-customer repeats, unusual hours).
**Skills:** Multi-tenant SaaS, ledgers, realtime, rule engines, anomaly detection, mobile-first UI.
**Value:** Commission disputes are a major operational cost; fraud losses are larger. This is a sellable product, not just a project.

## 3 · Credit scoring for thin-file borrowers

**The pain:** Most Nigerian borrowers have no credit bureau history. Lenders either reject them or lend blindly at punishing rates.
**Build:** An alternative-data scoring service using transaction history (with consent), airtime top-up patterns, device signals, and repayment history. Feature engineering, a gradient-boosted model, SHAP explanations (regulatorily required), a threshold chosen by expected-value rather than accuracy, and a monitoring dashboard for drift and fairness across segments.
**Skills:** Feature engineering, ML, calibration, cost-weighted thresholds, interpretability, FastAPI, monitoring.
**Value:** A 2-point reduction in default rate on a ₦500M book is ₦10M/year. Frame the pitch that way.

## 4 · Merchant cash-flow forecasting

**The pain:** SMEs cannot predict cash position, so they take expensive emergency loans or miss supplier payments.
**Build:** Bank/POS transaction ingestion (Mono/Okra/Stitch APIs), categorization of inflows and outflows, a 30/60/90-day cash-flow forecast with intervals, scenario modeling ("what if this receivable is 2 weeks late?"), and an alert when projected balance goes negative.
**Skills:** Open banking APIs, time series forecasting, categorization (rules + ML), scenario modeling, clear visualization.

## 5 · Transaction fraud detection in real time

**The pain:** Card and transfer fraud, SIM-swap account takeover, and social-engineering scams. Rules-based systems either block legitimate customers or miss new patterns.
**Build:** A streaming scoring service: velocity features (transactions per hour, amount vs personal baseline, new beneficiary, device change, geo-improbability), a rules layer plus a model layer, a case-management UI for analysts, and feedback capture to retrain.
**Skills:** Realtime processing, feature stores, rules engines, ML, low-latency APIs, analyst tooling.
**Value:** Directly measurable in prevented losses versus false-positive cost. The best kind of project to have numbers for.

## 6 · Regulatory reporting automation

**The pain:** CBN, NDIC, and NFIU returns are assembled manually from multiple systems each month. Late or incorrect filings carry penalties.
**Build:** A reporting engine that pulls from core systems, applies the regulator's schema and validation rules, flags exceptions before submission, versions each filing, and keeps an evidence trail.
**Skills:** Data modeling, validation frameworks, dbt, PDF/Excel generation, audit logging.
**Value:** Penalty avoidance plus dozens of analyst-hours monthly. Compliance budgets are large and defensible.

## 7 · Savings and thrift (ajo/esusu) digitization

**The pain:** Rotating savings groups run on paper and trust. Collectors abscond; members dispute contributions; there is no record for credit history.
**Build:** A group savings platform: group creation, contribution schedules, automated reminders (SMS/WhatsApp), a transparent ledger every member can see, payout rotation, default handling, and an exportable contribution history usable as credit evidence.
**Skills:** Ledgers, scheduling, notifications, offline-tolerant mobile UX, low-literacy design.

## 8 · Treasury and FX exposure dashboard

**The pain:** Businesses with USD costs and NGN revenue have no visibility into FX exposure and get surprised by devaluation.
**Build:** Multi-currency position tracking, exposure by tenor, scenario analysis on rate movements, hedging cost comparison, and alerting on threshold breaches.
**Skills:** Multi-currency modeling (rate-at-transaction-time), scenario analysis, financial visualization.

:::drill Sector immersion assignment
Choose one brief. Then: (1) find and read the relevant CBN regulation or guideline (they are public), (2) interview two people who work in that function, (3) find the actual spreadsheet they use today, (4) write a one-page proposal with the problem, the solution, the implementation timeline, and the price. Do this before writing a line of code. **The proposal is the deliverable that gets you paid; the code is what you do afterwards.**
:::
""",
)

page(
    id="sec-health-agri",
    title="Healthcare & Agriculture",
    sub="12 problem briefs",
    eyebrow="SECTORS 02–03",
    subtitle="Two sectors with enormous unmet need, growing donor and private funding, and very little competent software.",
    chips=["High impact", "Grant-funded budgets"],
    body=r"""
# Healthcare

## 1 · Clinic operations system for private practices
**Pain:** Small clinics run on paper registers. Patient histories are lost, follow-ups are missed, and billing leaks revenue.
**Build:** Patient registry with search and duplicate detection, appointment scheduling with SMS reminders, consultation notes with templates, prescriptions with interaction checks, lab order tracking, billing split by cash/HMO/NHIS, and an operations dashboard. Must work offline and sync.
**Value:** Reduced no-shows (SMS reminders alone typically cut them 20–30%) and recovered billing leakage pay for the system quickly.

## 2 · HMO claims processing and denial analytics
**Pain:** Providers submit claims and wait 60–120 days; denials are frequent and poorly explained; nobody analyzes *why* claims are rejected.
**Build:** Claim capture with pre-submission validation against payer rules, batch submission, status tracking, denial-reason analytics, aging reports, and a reconciliation view of expected versus received payment.
**Skills:** Workflow engines, rules validation, document generation, analytics.
**Value:** Cutting denial rate from 18% to 8% on a ₦200M claim book is ₦20M recovered.

## 3 · Drug supply chain and stockout prediction
**Pain:** Essential medicine stockouts at PHCs; expiry waste elsewhere; no visibility across facilities.
**Build:** Facility-level stock tracking, consumption-based reorder forecasting, expiry alerting, redistribution recommendations between facilities, and a supply-chain dashboard for the state ministry.
**Skills:** Forecasting, optimization, multi-tenant, mapping, offline-first data capture.

## 4 · Telemedicine triage and referral routing
**Pain:** Patients travel long distances for conditions manageable remotely; specialists are concentrated in a few cities.
**Build:** Structured symptom intake, triage scoring, teleconsultation (WebRTC), e-prescription, and referral routing to the nearest capable facility with capacity data.
**Skills:** WebRTC, clinical decision rules, geospatial routing, secure records.

## 5 · Immunization and antenatal follow-up tracking
**Pain:** Defaulters in vaccination and antenatal schedules are found late or never; community health workers track on paper.
**Build:** Enrollment with schedule generation, SMS/voice reminders in local languages, defaulter lists for health workers with offline mobile capture, and coverage dashboards by ward.
**Value:** Directly fundable by donors; coverage improvements are measurable and reportable.

## 6 · Health facility geospatial access analysis
**Pain:** New facilities are sited politically rather than analytically, leaving access gaps.
**Build:** An analysis combining facility locations, population rasters, and road networks to compute travel-time coverage, identify underserved populations, and recommend optimal new sites.
**Skills:** PostGIS, isochrone analysis, population data, choropleth visualization, policy-grade reporting.

---

# Agriculture

## 7 · Market price intelligence and arbitrage
**Pain:** Farmers sell at the farmgate price offered because they do not know prices 30 km away. Information asymmetry costs them 20–40% of value.
**Build:** Crowd-sourced and scraped price collection with verification, a price index per commodity per market, arbitrage recommendations net of transport cost, USSD and WhatsApp delivery for feature-phone users, and price trend forecasts.
**Skills:** Data collection at scale, verification/anti-gaming, USSD/WhatsApp integration, forecasting, low-bandwidth UX.

## 8 · Input financing and repayment tracking
**Pain:** Smallholders need seed and fertilizer on credit; lenders cannot assess or monitor them at scale.
**Build:** Farmer registration with plot geo-tagging, input loan disbursement in kind, harvest-linked repayment scheduling, agent field-visit logging, and a portfolio dashboard with satellite-derived crop health as a monitoring signal.
**Skills:** Geospatial, offline mobile, credit workflows, remote sensing basics (NDVI), portfolio analytics.

## 9 · Cold chain monitoring for perishables
**Pain:** Post-harvest losses of 40%+ in tomatoes, fish, and dairy; nobody knows where in the chain it happens.
**Build:** IoT temperature logger ingestion (or manual checkpoint logging), excursion alerting, batch traceability from farm to market, and loss-attribution analytics by route and handler.
**Skills:** Time-series ingestion, alerting, traceability modeling, root-cause analytics.

## 10 · Yield prediction and advisory
**Pain:** Planting decisions are made on tradition; rainfall patterns are shifting.
**Build:** Combine NIMET rainfall data, soil data, historical yields, and satellite vegetation indices to forecast yield and issue planting/spraying advisories via SMS in local languages.
**Skills:** Time series, geospatial, ML, multilingual delivery, agronomic domain reading.

## 11 · Produce traceability for export compliance
**Pain:** Nigerian agricultural exports get rejected over pesticide residue and documentation failures, costing millions.
**Build:** A traceability chain from farm plot through aggregation, processing, and export, with input records, test certificates, QR-verifiable batch records, and an exporter compliance dashboard against destination-market requirements.
**Value:** Rejection avoidance is directly quantifiable; export bodies and donors fund this work.

## 12 · Cooperative management platform
**Pain:** Farmer cooperatives manage membership, contributions, aggregation, and distribution on paper, causing disputes and enabling leakage.
**Build:** Membership registry, contribution ledger, produce aggregation tracking with grading, bulk sale proceeds distribution with transparent per-member calculation, and member-facing SMS statements.

:::edge Why these sectors are strategically smart for you
Two reasons. **Funding:** health and agriculture attract donor, government, and impact-investor money — budgets exist even where consumers cannot pay. **Competition:** almost nobody with real engineering skill works on these problems, so the bar is low and the gratitude is high. A strong health or agri portfolio makes you a candidate for roles at organizations like the Gates Foundation's partners, eHealth Africa, Babban Gona, Thrive Agric, and dozens of well-funded NGOs — plus it is genuinely meaningful work.
:::
""",
)

page(
    id="sec-logistics-retail",
    title="Logistics, Retail & Energy",
    sub="18 problem briefs",
    eyebrow="SECTORS 04–05–07",
    subtitle="Operations-heavy sectors where software directly converts into margin, which makes the sale easy.",
    chips=["Clear ROI", "Operational buyers"],
    body=r"""
# Logistics & Supply Chain

## 1 · Route optimization with real constraints
**Pain:** Dispatchers plan routes by intuition; fuel and time are wasted; deliveries miss windows.
**Build:** Multi-stop route optimization accounting for vehicle capacity, delivery time windows, traffic patterns, and road quality. Compare planned versus actual, and quantify savings.
**Skills:** Graph algorithms, VRP heuristics/OR-Tools, geospatial, mapping UI.
**Value:** 10–15% fuel reduction on a 30-vehicle fleet is millions annually. Easy pitch.

## 2 · Fleet telematics and driver behaviour analytics
**Build:** GPS ingestion, harsh-braking/speeding/idling detection, fuel-efficiency scoring per driver, maintenance scheduling based on usage, and a cost-per-km dashboard by vehicle.
**Skills:** High-frequency time series, event detection, scoring, cost analytics.

## 3 · Last-mile delivery with proof and exceptions
**Build:** Driver mobile app with offline manifest, delivery proof (photo, signature, OTP), failure-reason capture, live customer tracking link, and exception analytics by area and driver.

## 4 · Freight matching marketplace
**Pain:** Trucks return empty ~40% of the time; shippers cannot find capacity.
**Build:** Load posting, capacity matching by route and vehicle type, price discovery, escrow payment, and rating. Focus on the trust and payment layer — that is the hard part.

## 5 · Warehouse inventory and picking optimization
**Build:** Bin-level inventory, receiving and putaway workflows, pick-path optimization, cycle counting, and shrinkage analytics.

## 6 · Customs and clearing document workflow
**Pain:** Clearing agents juggle documents across email and WhatsApp; delays incur demurrage charges of real magnitude.
**Build:** Shipment workflow with document checklists per cargo type, deadline tracking with demurrage risk alerts, LLM-based document extraction and validation, and a client portal.
**Skills:** Workflow engines, document AI (Phase 5), deadline logic, client portals.

---

# Retail & E-commerce

## 7 · Inventory and POS for multi-location retail
**Build:** Offline-capable POS, real-time stock across branches, transfer workflows, supplier orders with lead-time tracking, and shrinkage detection by comparing expected versus counted stock.

## 8 · Demand forecasting and reorder automation
**Pain:** Stockouts lose sales; overstock ties up cash and expires.
**Build:** Per-SKU per-location demand forecasting with seasonality and promotions, safety stock calculation from service-level targets, automated reorder suggestions, and a dashboard of stockout cost versus holding cost.
**Value:** This is the highest-ROI analytics project in retail. Quantify it as recovered lost sales plus reduced working capital.

## 9 · Dynamic pricing and margin analytics
**Build:** Price elasticity estimation from historical data, competitor price scraping, margin-by-SKU analysis including hidden costs (delivery, returns, payment fees), and pricing recommendations with guardrails.

## 10 · Customer segmentation and retention engine
**Build:** RFM segmentation, cohort retention analysis, churn prediction, and automated lifecycle campaigns (welcome, replenishment reminder, win-back) with holdout groups to measure actual incremental impact.
**Edge:** Insist on holdout groups. Most marketing analytics overstates impact because nobody measures the counterfactual — saying this in an interview is a strong signal.

## 11 · Returns and reverse logistics analytics
**Build:** Return reason capture, cost-of-returns by SKU and by customer, fraud detection on serial returners, and product-quality feedback loops to procurement.

## 12 · WhatsApp commerce automation
**Pain:** Enormous volumes of Nigerian commerce happen in WhatsApp DMs with no catalogue, no order record, and no analytics.
**Build:** WhatsApp Business API integration with catalogue, order capture into a structured system, payment link generation, delivery status updates, and sales analytics on conversations. Add an LLM assistant for FAQ handling with human handoff.
**Skills:** WhatsApp API, conversation state machines, payments, LLM with guardrails.

---

# Energy & Utilities

## 13 · Prepaid meter and billing analytics for DisCos
**Build:** Consumption pattern analysis, estimated-billing dispute detection, revenue leakage identification (feeder input versus billed output), and collection efficiency by area.
**Value:** Aggregate technical, commercial and collection (ATC&C) losses are the industry's central problem. Analytics that localize losses are extremely valuable.

## 14 · Outage tracking and reliability reporting
**Build:** Crowd-sourced plus sensor outage reporting, duration and frequency metrics per feeder (SAIDI/SAIFI), restoration-time analytics, and public transparency dashboards.

## 15 · Solar system sizing and financing
**Build:** A load-profile calculator from appliance inventory, system sizing with battery autonomy, payback calculation against current generator and grid spend, financing plan comparison, and post-install monitoring integration.
**Value:** A sizing tool is a lead-generation asset for solar companies — sellable as a white-label product.

## 16 · Generator fleet fuel management
**Pain:** Diesel theft and inefficiency in businesses running generators; nobody reconciles fuel purchased against runtime.
**Build:** Runtime logging, fuel purchase records, consumption-per-hour analytics with anomaly detection, and cost-per-kWh comparison against alternatives.

## 17 · Energy efficiency audit tooling
**Build:** Structured audit data capture, benchmark comparison by facility type, savings opportunity ranking with payback periods, and report generation.

## 18 · Mini-grid customer and payment management
**Build:** Customer registry, prepaid token or mobile-money payment integration, consumption monitoring, disconnection/reconnection automation, and financial reporting for mini-grid operators and their funders.

:::ship Pick-one-and-build assignment
By Week 12, choose one brief from this library and make it your **secondary portfolio track**: research it properly, talk to three practitioners, and build a working version alongside the main curriculum. By Week 26 you will have both a general-purpose SaaS capstone and a sector-specific product with genuine domain credibility behind it. That pairing is what turns a job search into inbound interest.
:::
""",
)

page(
    id="sec-public-edu",
    title="Education, Government, Property & NGO",
    sub="22 problem briefs",
    eyebrow="SECTORS 06–08–09–10",
    subtitle="Institutional buyers with real budgets, plus the highest-visibility work for building a public reputation.",
    chips=["Institutional budgets", "Public impact"],
    body=r"""
# Education

## 1 · School management for private schools
**Build:** Student records, attendance, continuous assessment and report-card generation to WAEC/NECO grading conventions, fee invoicing with payment tracking and reminders, parent portal with SMS, and a dashboard of collection rate and enrollment trends.
**Value:** Fee collection improvement alone typically justifies the cost. Thousands of private schools; a genuine SaaS market.

## 2 · Learning analytics and early warning
**Build:** Per-student performance trajectories, identification of at-risk students before they fail (attendance + assessment trends), topic-level weakness detection from question-level data, and teacher-facing intervention suggestions.

## 3 · Computer-based test platform
**Build:** Question banks with difficulty tagging, randomized exam generation, secure delivery with lockdown behavior, auto-marking with item analysis, and psychometrics (discrimination index, reliability) to identify bad questions.
**Skills:** Anti-cheating design, offline-tolerant delivery, psychometric statistics.

## 4 · Skills-to-jobs matching for training programs
**Build:** Trainee skill profiles, employer requirement parsing, matching and recommendation, placement tracking, and outcome analytics that funders require.

## 5 · Adaptive learning for foundational literacy/numeracy
**Build:** Diagnostic assessment, an adaptive item-selection engine, spaced repetition scheduling, and progress reporting. Design for low-end Android and offline use.

---

# Government & Public Sector

## 6 · Procurement transparency and anomaly detection
**Build:** Ingest open contracting data, detect anomalies (single-bidder awards, price outliers versus comparable contracts, supplier concentration, split contracts avoiding thresholds), and publish an explorable public dashboard.
**Value:** Anti-corruption analytics is funded by international donors and gets significant media attention — excellent for reputation.

## 7 · Internally generated revenue (IGR) analytics
**Build:** Revenue stream analysis by source and LGA, leakage detection by comparing assessed versus collected, taxpayer registry deduplication, and collection efficiency dashboards.

## 8 · Citizen service request and resolution tracking
**Build:** Multi-channel intake (web, SMS, WhatsApp, USSD), routing to responsible agency, SLA tracking, resolution verification, and public performance dashboards by agency and LGA.

## 9 · Budget execution transparency
**Build:** Parse published budget documents (usually terrible PDFs), model budget versus actual by line item, track capital project execution against milestones, and visualize for public consumption.
**Skills:** PDF extraction (a genuinely hard, valuable skill), data modeling, public-facing visualization.

## 10 · Land registry and title verification
**Build:** Digitized parcel records with geospatial boundaries, ownership history chain, encumbrance flags, and a verification interface for buyers and lenders. Fraud prevention is the value.

## 11 · Public health surveillance dashboard
**Build:** Case reporting from facilities, outbreak detection through statistical anomaly monitoring, geographic spread visualization, and resource allocation recommendations.

---

# Real Estate & Construction

## 12 · Listing verification and fraud prevention
**Pain:** Property fraud is endemic; the same property is listed by five agents, some fictitious.
**Build:** Listing deduplication via image hashing and geospatial clustering, agent verification workflow, document verification checklist, and a fraud-report system with pattern analysis.

## 13 · Construction project cost control
**Build:** Bill-of-quantities tracking, material price escalation monitoring (a serious issue in inflationary markets), progress versus payment certification, variation-order management, and cost-overrun early warning.

## 14 · Facility management and maintenance
**Build:** Asset registry, preventive maintenance scheduling, work-order workflow with vendor management, cost-per-asset analytics, and a tenant request portal.

## 15 · Rental property and service charge management
**Build:** Tenancy tracking with renewal alerts, rent invoicing and receipting, service-charge allocation and reconciliation with transparent statements, and arrears analytics.

## 16 · Property valuation model
**Build:** A hedonic pricing model using location, size, features, and comparable transactions, with confidence intervals and explanation of drivers. Honesty about data limitations is essential here.

---

# NGO & Development

## 17 · Monitoring & evaluation (M&E) platform
**Pain:** NGOs report to donors using spreadsheets consolidated by hand across dozens of field sites; errors and delays are constant.
**Build:** Indicator framework configuration, offline field data collection, automatic aggregation against targets, disaggregation by the dimensions donors require (sex, age, location, disability), and donor-format report generation.
**Value:** Every funded NGO must do this. It is a repeatable product with a defined buyer.

## 18 · Beneficiary registry with deduplication
**Build:** Registration with biometric or document identifiers, fuzzy deduplication across programs, eligibility verification, distribution tracking, and grievance handling.
**Skills:** Record linkage/fuzzy matching (a genuinely valuable specialty), privacy-preserving design, offline capture.

## 19 · Cash transfer program management
**Build:** Beneficiary enrollment, payment instruction generation to providers, reconciliation of confirmed payments, exception handling for failed transfers, and outcome tracking.

## 20 · Impact measurement and evidence synthesis
**Build:** Baseline/endline survey management, treatment versus comparison analysis with proper statistics, cost-per-outcome computation, and evidence dashboards for funders.
**Skills:** Survey methodology, causal inference (Phase 6), honest uncertainty reporting.

## 21 · Grant compliance and reporting automation
**Build:** Multi-donor requirement tracking, expenditure categorization against budget lines, burn-rate monitoring with alerts, and automated narrative and financial report drafting.

## 22 · Community feedback and accountability
**Build:** Anonymous multi-channel feedback intake, categorization (LLM-assisted), routing to responsible teams, resolution tracking, and trend analysis to spot systemic issues.

:::edge The reputation play
Public-interest projects generate disproportionate visibility. A well-built procurement transparency dashboard or an open health-access analysis can get covered in the press, cited by researchers, and shared by people with large audiences. That visibility converts into job offers, consulting inquiries, and conference invitations far more efficiently than another CRUD app. **Build one public-good project during this program and publish it loudly.** Use open data so you do not need anyone's permission.
:::
""",
)
