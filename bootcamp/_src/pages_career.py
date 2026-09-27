# -*- coding: utf-8 -*-
PAGES = []
G = "08 · Capstone & Career (Wk 25–26)"

def page(**kw):
    kw.setdefault("group", G)
    PAGES.append(kw)

page(
    id="w25-capstone",
    title="W25 · The Flagship Capstone",
    sub="Week 25",
    eyebrow="WEEK 25 · LAUNCH",
    subtitle="One product that demonstrates everything: full-stack engineering, data analysis, and AI — solving a real sector problem.",
    chips=["35 hours", "The piece you lead with"],
    body=r"""
## What the flagship must prove

Your other projects each demonstrate a slice. This one demonstrates that you can **own a product end to end**. It must combine, in a single coherent system:

1. A **production-quality full-stack application** (Next.js + TypeScript, API, PostgreSQL, auth, multi-tenancy, payments or equivalent)
2. A **data layer** (dbt models, an analytics service, dashboards with real metrics)
3. An **AI feature** that solves a real problem, with evals proving it works
4. **Production engineering** (Docker, CI/CD, monitoring, tests, runbook)
5. **A real user or a real proxy for one** — even one actual business using it changes the conversation entirely

## Choosing well

Pick from the sector library, weighted by: (a) do you have access to someone with this problem? (b) does it naturally require all three layers? (c) can you explain its value in one sentence to a non-technical person? (d) would you be willing to keep working on it after the program?

**Strong archetypes:**

++ Clinic revenue system :: App: patient/billing workflow. Data: claim denial analytics, revenue leakage detection, payer performance. AI: extract structured data from HMO remittance PDFs, chat over clinical policy documents.
++ Agri cooperative platform :: App: member registry, produce aggregation, payments. Data: yield analytics, price forecasting, member profitability. AI: advisory chatbot in Hausa over agronomic guidance, disease identification from crop photos.
++ Logistics control tower :: App: dispatch, tracking, proof of delivery. Data: cost-per-km, on-time analytics, route profitability. AI: document extraction for waybills, natural-language querying of the operations data.
++ Microfinance loan platform :: App: origination, disbursement, repayment, collections. Data: portfolio at risk, vintage analysis, collections effectiveness. AI: alternative-data risk scoring with SHAP explanations, and a customer support assistant.

## The build plan

@@ Day 1 | Scope brutally. Define the ONE core workflow. Write the ADRs, data model, and API contract. Set up the repo, CI, and deploy pipeline before any features.
@@ Day 2 | Vertical slice: the core workflow working end to end in production, ugly but real. Deploy it today.
@@ Day 3 | Depth on the core: all states, edge cases, permissions, tests. Second workflow.
@@ Day 4 | Data layer: dbt models, metrics, analytics service, dashboard.
@@ Day 5 | AI feature with eval suite. Cost logging. Guardrails.
@@ Day 6 | Hardening, load test, monitoring, seed demo data, runbook, README, demo video.

:::trap Scope is the killer
Every ambitious capstone fails the same way: too many features, none finished. **Cut ruthlessly on Day 1.** One excellent workflow with real depth (permissions, edge cases, empty states, tests, performance) beats six half-built features. If you are behind on Day 4, cut features, never quality — a reviewer immediately sees the difference between "small and superb" and "big and broken."
:::

## The packaging (as important as the build)

Your capstone repo must contain:

- **README** — one-sentence problem, animated GIF, live demo link with credentials, feature list, architecture diagram, tech stack with justification, local setup in three commands, and a "trade-offs and what I'd do next" section
- **`/docs/adr/`** — at least six architecture decision records
- **`/docs/runbook.md`** — deploy, rollback, restore, incident procedures
- **`/docs/metrics.md`** — the metrics dictionary
- **`/evals/`** — the AI evaluation suite with a results table
- **A demo video** — 5 minutes, narrated, showing the problem then the solution. Host on YouTube unlisted and link it at the top.
- **A case-study blog post** — the story of building it, what broke, what you learned

:::edge Get one real user
The single highest-leverage thing you can do in Week 25 is get **one real business to use your product**, even free, even partially. It transforms every conversation: "I built a clinic billing system" becomes "I built a clinic billing system that St. Mary's in Kano has used to process ₦4M in billing over three weeks; here is what I learned about their workflow." That sentence beats any credential. Go to the businesses in the sector you chose, offer it free in exchange for feedback, and iterate on what they actually complain about.
:::
""",
)

page(
    id="w26-portfolio",
    title="W26 · Portfolio, CV & Positioning",
    sub="Week 26, Day 1–3",
    eyebrow="WEEK 26 · MARKET ENTRY",
    subtitle="Turning 26 weeks of work into offers. Most people build skill and then market themselves badly.",
    chips=["18 hours", "Positioning · CV · profiles"],
    body=r"""
## Your positioning statement

Write one sentence you will use everywhere — CV headline, LinkedIn, X bio, email signature, first line of every application:

> **"Full-stack engineer (TypeScript/Next.js/Postgres) and analytics engineer (Python/SQL/dbt) — I build the systems and the analytics that prove they work. Focused on [your sector]."**

Specific beats generic. "Full-stack developer looking for opportunities" is invisible. A named combination plus a named sector is memorable and searchable.

## The portfolio site

Build it in a day with your own component library. Structure:

1. **Hero:** your positioning sentence, a photo, and two buttons — "See my work" and "Book a call".
2. **Three flagship projects**, each with: a one-line problem statement, a screenshot or GIF, the measurable outcome, the tech stack, and links to live/repo/case-study. **Never more than five projects** — quality signals get diluted.
3. **Case studies** for the top three: problem → constraints → approach → architecture → results with numbers → what I'd do differently. This is what separates a portfolio from a link dump.
4. **Writing:** your best 8 posts.
5. **About:** the honest story of the 26 weeks. Career-changers who tell this story well are compelling; a self-taught developer who shipped 12 products in six months is a signal of exactly the trait employers want.
6. **Contact:** email, calendar link, GitHub, LinkedIn, X.

## The CV that gets past screening

**One page** for under 5 years' experience. No photo (for international applications), no "references available on request", no skill bar charts.

**Structure:**
```
NAME | Full-Stack & Analytics Engineer
city, Nigeria (open to remote) | email | github | linkedin | portfolio

SUMMARY (2 lines)
Positioning sentence + the single most impressive concrete fact.

SELECTED PROJECTS  (yes, projects before employment if you have no relevant employment)
Project Name — one-line description                          live link | repo
• Built X using Y, achieving Z measurable result
• Reduced/increased [metric] from A to B by doing C
• Handled [technical challenge] with [approach]

SKILLS
Languages: TypeScript, Python, SQL
Frontend: React, Next.js (App Router, RSC), Tailwind, TanStack Query
Backend: Node (Hono/Fastify), FastAPI, PostgreSQL, Redis, BullMQ
Data: dbt, pandas/Polars, DuckDB, BigQuery, Power BI, Metabase
Infra: Docker, GitHub Actions, AWS/Fly/Vercel, OpenTelemetry, Sentry
AI: LLM APIs, RAG (pgvector), structured output, evaluation suites

EXPERIENCE / EDUCATION  (whatever you have — do not hide non-tech work,
frame it for transferable evidence: responsibility, customers, numbers)
```

**Every bullet follows: action verb + what you built + technology + measurable outcome.** "Worked on the frontend" is worthless. "Cut dashboard load time from 4.2s to 380ms by adding materialized rollups and cursor pagination over 8M rows" is an interview invitation.

:::trap CV mistakes that get you rejected in 6 seconds
Listing every technology you have ever touched (dilutes signal and invites questions you cannot answer); no links to live work; a wall of text; claiming "expert" in anything; typos; a generic objective statement; and PDF filenames like `cv_final_final2.pdf` — name it `Firstname-Lastname-CV.pdf`.
:::

## GitHub as a hiring surface

- **Profile README** with your positioning, top projects, and current focus
- **Pin your best six repos**; archive or delete abandoned experiments
- Every pinned repo has: a real README with screenshots, a live link, clear commits, and a green CI badge
- Contribute to **one open-source project** — even documentation fixes and small bug fixes. It proves you can work in someone else's codebase, which is what the job actually is.

## LinkedIn (the highest-ROI platform for Nigerian and remote hiring)

Headline = your positioning sentence. Banner = a clean graphic naming your stack. About section = the story plus specifics plus a call to action. **Featured section = your three flagship projects with images.**

**Post twice a week, permanently.** What works: a build story with a screenshot, a specific technical lesson with code, a sector insight ("what I learned about how HMO claims actually flow"), a project launch, and an honest "here is what I got wrong" post. What does not work: motivational quotes, "excited to announce" with no substance, and engagement bait.

Connect with: engineers at companies you want to join, engineering managers, recruiters in your sector, and people building in your chosen domain. Send a note, not a blank request.

:::edge The compounding asset you already built
By now you have ~150 public write-ups from your recall habit. That is the raw material for six months of content, a technical blog with genuine depth, and possibly a small book or course. Very few candidates have anything comparable. Turn the best 20 into polished posts, publish them on your own domain, and cross-post. **Being findable is the difference between applying for jobs and being approached for them.**
:::
""",
)

page(
    id="w26-interview",
    title="W26 · Interviews & Getting Hired",
    sub="Week 26, Day 4–5",
    eyebrow="WEEK 26 · MARKET ENTRY",
    subtitle="The full process, from application strategy to negotiating the offer.",
    chips=["12 hours", "Process · practice · offers"],
    body=r"""
## Application strategy

**Do not mass-apply.** A hundred generic applications produce fewer interviews than fifteen targeted ones. For each target company: read their product, find their engineering blog, identify a specific problem they have, and reference it.

**The four channels, in order of conversion rate:**
1. **Warm referrals** (~50% interview rate) — an engineer inside forwards your CV. Build these relationships *before* you need them.
2. **Direct outreach to hiring managers** (~15%) — a short, specific email with a link to relevant work.
3. **Inbound from your public work** (highest quality) — this is what the writing habit buys you.
4. **Cold applications** (~2–5%) — worth doing, but never your primary strategy.

**The outreach email that works:**
```
Subject: Full-stack + analytics engineer — built a [thing] relevant to [their problem]

Hi [Name],

I saw [specific thing about their product/blog/announcement]. I recently built
[project] which solves a similar problem — [one-line description with a number].

Live: [link]  ·  Code: [link]  ·  Write-up: [link]

I'm looking for [role type] work. If you have anything open, I'd love to talk.
If not, is there someone on your team I should follow instead?

[Name]
```
Short, specific, gives them an easy out, and asks for a small favor. Send 10 a week.

## The interview stages and what each tests

| Stage | Tests | How to win |
|---|---|---|
| **Recruiter screen** | Communication, motivation, salary fit | Have your 90-second story rehearsed; give a salary range, not a number |
| **Technical screen / take-home** | Can you code | Treat it as production work: tests, README, clean commits. Timebox honestly and say what you cut |
| **Live coding / pairing** | Thinking process, collaboration | Narrate your thinking; clarify before coding; write the test first if allowed |
| **System design** | Seniority, trade-offs | Use the 7-step framework from Week 15. Ask about scale before designing |
| **Domain / SQL round** | Real analytical skill | Window functions, careful about NULLs and joins, state your assumptions |
| **Behavioural** | Will we want to work with you | STAR stories, prepared and specific |
| **Hiring manager** | Judgment, ownership, fit | Ask about their biggest technical problem and discuss it seriously |

## The 90-second story

Rehearse until it is natural, not memorized:
> "I came from [background]. Six months ago I committed full-time to becoming an engineer who can both build products and analyze them. I've shipped [N] projects — the one I'm proudest of is [flagship], which [does what] for [whom] and [measurable result]. I specialize in TypeScript full-stack and Python/SQL analytics, focused on [sector], and I'm looking for a role where I can own features end to end."

## Behavioural answers with STAR

Prepare **eight** stories, each with Situation → Task → Action → Result (with numbers), covering: a hard technical problem, a failure and what you learned, a disagreement, tight deadline trade-offs, learning something fast, taking initiative, handling ambiguous requirements, and a time you were wrong.

:::edge The candidate who asks great questions wins
Most candidates ask about culture and growth. Ask instead: "What is the most painful part of your current codebase?" · "How do you decide what to build?" · "What does the on-call rotation look like?" · "Walk me through what happens between a commit and production." · "What has someone in this role done in their first six months that made you glad you hired them?" · "What is the biggest risk to this team hitting its goals this year?" These signal that you are evaluating them as a peer, which reframes the entire dynamic.
:::

## Salary and negotiation

**Never give the first number if you can avoid it.** "I'd like to understand the role better first — what range is budgeted for this position?" If pressed, give a researched range with your target at the bottom third.

**Know the market:** research on Levels.fyi, Glassdoor, and community salary surveys. For Nigerian roles, local mid-level full-stack compensation varies enormously between local companies and internationally-funded startups — the gap can be 3–5x, so target accordingly. For remote international contracts, rates are typically quoted in USD and are a different market entirely; do not let local anchoring cap you.

**Always negotiate.** A single conversation is worth more than months of raises, and reasonable negotiation does not lose offers. Negotiate on: base, equity, signing bonus, remote flexibility, learning budget, and title. Get everything in writing.

**Evaluate offers on:** the work itself, who you will learn from, growth trajectory, compensation, stability, and optionality. Early career, **who you learn from matters more than salary** — one year with a strong senior engineer is worth three years alone.

## Freelance and consulting (the parallel track)

Do this alongside job hunting; it produces income and case studies immediately.

- **Price on value, never hourly.** A reconciliation system that saves ₦4M a year is not a "40 hours × rate" job. Quote a project fee tied to the outcome.
- **Ladder up:** first project cheap for the case study → second at market → third at premium with a named result.
- **Always use a contract:** scope, deliverables, milestones, payment schedule (50% upfront minimum), change-request process, and IP terms.
- **Where to find work:** Upwork/Contra for the first case studies; then direct outreach to businesses in your sector; then inbound from your content. The third channel is where the real money is.
- **The upsell that builds a business:** every project you build generates data. Offer an ongoing analytics retainer on top of the build. Recurring revenue beats project work.

:::ship Week 26 final deliverables
(1) Portfolio site live on your own domain. (2) One-page CV as a PDF. (3) LinkedIn and GitHub fully optimized. (4) 20 target companies researched with named contacts. (5) 10 outreach emails sent. (6) Three mock interviews recorded and reviewed — technical, system design, and behavioural. (7) A freelance service page with three productized offers and prices.
:::
""",
)

page(
    id="beyond",
    title="After Week 26 — The Next 5 Years",
    sub="Compounding",
    eyebrow="BEYOND THE PROGRAM",
    subtitle="What actually separates the top 1% is not the first 26 weeks. It is what you do in the 260 weeks after.",
    chips=["Long game"],
    track=False,
    body=r"""
## The honest truth about "top 1%"

Twenty-six weeks of intense, well-structured work puts you ahead of most bootcamp graduates and many working developers — genuinely. But top 1% is not a certificate you earn; it is a **position you hold by continuing to compound** while others plateau. Most developers stop learning deliberately around year two and coast on the same skills for a decade. That is the opening.

Here is what the next five years look like if you want to hold that position.

## The four compounding assets

++ Depth :: Every year, go one level deeper on something fundamental — the query planner, the browser rendering pipeline, distributed consensus, statistical inference. Depth is what makes you the person others come to.
++ Range :: Deliberately learn adjacent things: a systems language (Go or Rust), infrastructure-as-code, data engineering at scale, mobile, security. Range is what makes you able to lead.
++ Reputation :: Keep writing and shipping publicly. Speak at meetups, then conferences. A reputation means opportunities arrive without applications.
++ Relationships :: The engineers you meet now become CTOs and founders in eight years. Be the person people want to work with again. Nearly every great job comes through someone who knows your work.

## The year-by-year arc

**Year 1 — Ship and absorb.** Get hired or get paying clients. Optimize entirely for **who you learn from**. Read every code review comment as free tutoring. Volunteer for the unglamorous work — migrations, on-call, debugging production — because that is where real skill forms. Goal: become genuinely reliable.

**Year 2 — Own things.** Take ownership of a system, not just tickets. Lead a project end to end including the ambiguity, the stakeholder conversations, and the trade-off decisions. Start mentoring someone. Deepen your sector expertise. Goal: be trusted with scope.

**Year 3 — Multiply.** Your value shifts from what you build to what you enable. Design systems others build on. Improve how your team works. Write the documentation and tooling that saves everyone time. Start speaking publicly. Goal: raise the output of people around you.

**Year 4–5 — Choose your lane.** By now the fork appears: **staff/principal engineer** (deep technical leadership, architecture, hard problems), **engineering management** (people, delivery, organization), **founder** (your own product, using everything), or **independent consultant** (premium rates, chosen problems, maximum autonomy). All four are legitimate. Choose intentionally rather than drifting.

## Habits to keep permanently

- **10 minutes daily of spaced repetition** on whatever you are currently learning
- **One public write-up per week.** Non-negotiable. It is the highest-return hour of your week.
- **One system design per month**, written out
- **Five algorithm/SQL problems per week**, tagged by pattern
- **One deep book per quarter** — *Designing Data-Intensive Applications*, *The Pragmatic Programmer*, *Storytelling with Data*, *Trustworthy Online Controlled Experiments*, *Database Internals*, *Thinking in Systems*
- **One sabbatical project per year** — something unreasonable that teaches you a new domain
- **A quarterly review** of your skills, income, network, and direction against where you said you wanted to be

## The three multipliers most engineers never develop

1. **Writing.** The best engineers write well. Design documents, postmortems, proposals, and explanations are how influence travels in an organization larger than five people. Practice it deliberately.
2. **Commercial literacy.** Learn to read a P&L, understand unit economics, and know how your company actually makes money. The engineer who can say "this feature costs ₦2M to build and will generate ₦8M" makes decisions instead of receiving them.
3. **Judgment under uncertainty.** Knowing what *not* to build, when "good enough" is correct, when to take on debt deliberately and when to pay it down. This is the rarest skill and the one that compounds most steeply. It comes from shipping many things and honestly reviewing the outcomes.

## Ten things worth remembering

1. Shipping beats perfecting. Always.
2. Boring technology, chosen deliberately, wins most of the time.
3. Read more code than you write.
4. The bug is almost always in your assumptions, not the framework.
5. Simple systems that work beat elegant systems that mostly work.
6. Ask the question you are afraid will make you look stupid — it is usually the question everyone else has.
7. Your first version of anything will be wrong. Ship it and learn.
8. Optimize for feedback loops: fast tests, fast deploys, real users, honest reviewers.
9. The person who understands the business problem best usually writes the most valuable code.
10. Consistency over intensity. Twenty-six weeks was a sprint. The career is not.

:::edge The final instruction
Go back to Week 0 and read what you wrote in that first README. Then open a new file: `year-1-goals.md`. Write down where you intend to be in 52 weeks — role, income, skills, one thing built, one thing published. Be specific and be ambitious. Then close this site and go build something nobody asked you to build.
:::
""",
)

page(
    id="resources",
    title="Resource Vault",
    sub="Curated only",
    eyebrow="APPENDIX",
    subtitle="A deliberately short list. Depth over volume — everything here is worth your full attention.",
    chips=["Free unless noted"],
    track=False,
    body=r"""
## Documentation (read the primary source, always)

- **MDN Web Docs** — the definitive reference for HTML, CSS, JavaScript, and browser APIs
- **React docs (react.dev)** — genuinely excellent; the "You Might Not Need an Effect" and "Thinking in React" pages are essential
- **Next.js docs** — read the App Router and caching sections twice
- **PostgreSQL manual** — dense but authoritative; the indexes and query-planning chapters repay effort
- **TypeScript Handbook** + Matt Pocock's free TypeScript resources
- **dbt docs** — including their "How we structure our dbt projects" guide, which is a modeling course in itself
- **OWASP Top 10 and the OWASP Cheat Sheet Series** — read all of it once, revisit annually

## Books that repay the time

| Book | Why |
|---|---|
| *Designing Data-Intensive Applications* — Kleppmann | The single best systems book. Read it in year 1 and again in year 3 |
| *The Pragmatic Programmer* | Craft and professional judgment |
| *Refactoring* — Fowler | How to change code safely |
| *Storytelling with Data* — Knaflic | Visualization and communication |
| *Trustworthy Online Controlled Experiments* — Kohavi et al. | The definitive A/B testing text |
| *The Art of PostgreSQL* — Fontaine | SQL as a first-class skill |
| *Fundamentals of Data Engineering* — Reis & Housley | The modern data stack, explained properly |
| *Thinking, Fast and Slow* — Kahneman | Why your analysis will fool you |
| *The Mom Test* — Fitzpatrick | How to talk to users without getting lied to. Short and essential |

## Practice platforms

- **SQL:** DataLemur, StrataScratch, PostgreSQL Exercises, Advent of SQL
- **Algorithms:** LeetCode (patterns, not volume), Neetcode.io's structured roadmap
- **Frontend:** Frontend Mentor (real designs to implement), CSS Battle
- **Data:** Kaggle (datasets more than competitions), Maven Analytics challenges, TidyTuesday
- **System design:** ByteByteGo, the Grokking system design material, and real engineering blogs

## Data sources for portfolio projects

**Nigeria:** National Bureau of Statistics, CBN Statistical Bulletin, NGX, Nigeria Open Data portal, NIMET, NBS LSMS household surveys, Open Contracting (Budeshi, BudgIT).
**Global:** World Bank Open Data, IMF, WHO GHO, FAOSTAT, Our World in Data, OpenStreetMap, GDELT, Kaggle, Hugging Face Datasets, data.gov.

## Communities worth joining

Nigerian/African: Forloop Africa, Data Science Nigeria, Google Developer Groups (Kano/Kaduna/Abuja/Lagos chapters), She Code Africa, local tech hub communities.
Global: relevant Discords for your stack, Locally Optimistic (analytics), the dbt Community Slack, Hacker News (read, do not argue), and Lobsters.

## Newsletters and blogs

Engineering blogs from companies that write well: Stripe, Figma, Cloudflare, Netflix, Airbnb, Paystack, Uber. Newsletters: JavaScript Weekly, Node Weekly, TLDR, Benn Stancil's *Substack* (analytics thinking), Data Engineering Weekly, Simon Willison's blog (the best source on practical LLM engineering).

## Tools to have accounts for

GitHub · Vercel · Neon or Supabase · Fly.io or Render · Cloudflare · Sentry · Axiom or Better Stack · BigQuery sandbox · Metabase or Power BI Desktop · Figma · Excalidraw (diagrams) · Obsidian or Notion (notes) · one LLM API with a spend cap.

:::edge How to read documentation like a professional
Do not read linearly. (1) Skim the table of contents to build a map of what exists. (2) Read the conceptual overview properly. (3) Build something small. (4) Return to the reference for the specific thing you need. (5) Once you are comfortable, **read the "advanced", "caveats", and "gotchas" sections cover to cover** — that is where the knowledge that makes you look experienced actually lives, and where almost nobody goes.
:::
""",
)

page(
    id="jobmarket",
    title="Where the Work Actually Is",
    sub="The Nigerian + remote hiring map",
    eyebrow="CAREER",
    subtitle="Concrete sources, a weekly cadence, and the funnel metrics that tell you what to fix. Read this before you send a single application.",
    chips=["Nigeria + remote", "Concrete sources", "Weekly cadence"],
    body=r"""
## Why most job searches fail

It is almost never a shortage of jobs. It is a broken funnel that nobody measures. If you send 60 applications and get 3 replies, sending 120 will not help — the CV or the targeting is wrong, and doubling a wrong input doubles nothing.

Fix the funnel by measuring it, then fix the broken stage only.

## Where Nigerian employers actually post

| Source | What it is good for | How to use it |
|---|---|---|
| **LinkedIn Jobs** | The largest volume of formal tech roles in Nigeria; most startups and banks post here first | Set alerts for 4–6 titles, filter "past week", apply within 48 hours of posting |
| **LinkedIn direct outreach** | Referred candidates are interviewed at a far higher rate than cold applicants | Message an engineer at the company, not HR |
| **Company career pages** | Where serious companies post before aggregators pick it up | Make a list of 30 target companies; check weekly |
| **Jobberman, Ngcareers, MyJobMag** | Volume, but heavy with low-quality and mislabelled listings | Useful for breadth; expect a low signal rate |
| **Otta, Wellfound (AngelList Talent)** | Startup roles, often with salary ranges published upfront | Best source for early-stage startups |
| **Paystack, Flutterwave, Moniepoint, Kuda, Interswitch, Andela, AltSchool, TeamApt** career pages | The fintech and edtech employers who pay best | Check monthly; roles fill fast and often unadvertised |
| **Slack/Discord communities** | Where contract and freelance work circulates before it reaches job boards | Be a useful member for months before you need anything |
| **Twitter/X tech Nigeria** | Founders hiring, contract gigs, and referrals | Post your work publicly; this is where being visible pays |

### The fintech cluster

If you are optimising for Nigerian salary, **fintech is the centre of gravity**. The companies that pay above market — Paystack, Flutterwave, Moniepoint, Kuda, OPay, PalmPay, Interswitch, TeamApt, Brass, Sparrow — all hire TypeScript/React frontend engineers, Node or Python backend engineers, and increasingly analytics engineers.

Your Week 12 sector choice should probably be **fintech & banking** if your goal is the Nigerian market, because that is where both the jobs and the highest pay are. If your goal is remote/global work, pick the sector where you have genuine domain knowledge, because that is your differentiator against candidates from anywhere in the world.

## Where remote work actually is

| Source | Notes |
|---|---|
| **RemoteOK, We Work Remotely, Remotive** | High volume, high competition, mostly global-facing companies |
| **Hacker News "Who is hiring"** | Posted the 1st of each month; a remarkable signal-to-noise ratio and far less competition than the big boards |
| **Wellfound / Y Combinator jobs** | Startup roles, often with equity; strong for first remote job |
| **Toptal, Gun.io, Arc.dev** | Vetted marketplaces; the screening is hard but the rates are good |
| **Upwork, Fiverr** | Best for building a track record fast, worst for building a career; use deliberately, not by default |
| **Contra, Braintrust** | Newer, lower-fee alternatives worth checking |
| **Direct outreach to agencies** | Nigerian and European agencies hire contractors constantly and rarely post |

### The remote reality check

Remote roles from global companies are the most competitive market on earth: you are competing against everyone. Your realistic first remote role is more likely to come from:
- A **Nigerian company with international clients** (agencies, consultancies)
- A **contract role** you found through a community or a referral
- A **freelance client** who became a retainer, then a job
- A **global company that specifically hires in Africa** (there are more of these every year, and being in WAT is sometimes an advantage for coverage)

Do not wait for the perfect global remote job. Build income from what is available, and let the global role be the thing that happens while you are already working.

## The weekly cadence

@@ Monday | Refresh CV and LinkedIn. Update the tracker. Review last week's funnel numbers.
@@ Tuesday | 3–4 tailored applications. Each one gets a CV edited for that specific role.
@@ Wednesday | 3–4 tailored applications.
@@ Thursday | 3–4 tailored applications.
@@ Friday | 2–3 outreach messages to engineers at target companies. This is the highest-yield hour of the week.
@@ Saturday | Ship one portfolio improvement. A better README, one more test, a performance fix.
@@ Sunday | 30 minutes: review the funnel, decide which stage to fix, plan next week.

Total: about **8–12 applications and 2–3 outreach messages per week**, sustained. Sustained matters far more than intense — a burst of 40 applications in one week followed by nothing is worth less than 10 per week for ten weeks.

## The funnel: measure it, then fix the broken stage

| Stage | Healthy rate | If you are below it |
|---|---|---|
| Application → screening call | 15–25% | Your CV is not matching the role. Rewrite the top third around the job title and its keywords |
| Screening call → technical | 40–60% | Your communication or your project story is weak. Practice out loud |
| Technical → offer | 20–33% | Your interview communication is the gap, not your code. Do recorded mock interviews weekly |
| Offer → accepted | 60%+ | You are negotiating badly, or applying to roles you do not actually want |

**Read this table before sending one more application.** If your application-to-call rate is 5%, the fix is the CV. If it is 25% but your call-to-technical rate is 15%, the fix is how you talk about your work. Doubling application volume never fixes a broken stage.

## The tracker

One row per application, in a spreadsheet. Non-negotiable — without it you are guessing.

~~~text
Company | Role | Source | Salary | Date applied | Stage | Next action | Due | Contact | Notes
~~~

The columns that matter most: **Next action** and **Due**. An application with no next action and no date is an application you have forgotten about. Most people lose offers to disorganisation, not to competition.

## What to do in the first 30 days

1. **Week 1:** Build the tracker. List 30 target companies. Rewrite your CV against 5 real job postings — not against what you wish they said, but against the actual words they use.
2. **Week 2:** Start the cadence. 8–10 applications. First outreach messages.
3. **Week 3:** Keep the cadence. Ship one portfolio improvement. Book one mock interview.
4. **Week 4:** Review the funnel honestly. Fix the worst stage. Do not add volume.

## The one thing that changes everything

Apply through a **referral** wherever you can get one. A referred candidate is interviewed at a dramatically higher rate than a cold applicant — often several times higher. This is why Friday outreach is the highest-yield hour of your week: one ten-minute message to an engineer at a company you want to work for is worth more than twenty cold applications.

The message that works is short, specific, and asks for one small thing:

~~~text
Subject: Quick question about [team] at [company]

Hi [Name] - I saw your post about [specific thing]. I'm a
full-stack engineer in Lagos who recently shipped [relevant
thing], and I'm applying for the [role] opening.

Would you be open to a 15-minute call about what the team is
working on? Happy to work around your schedule.

Either way, thanks for the post - [specific thing you learned].
~~~

It works because it is specific, it offers something before asking, and it asks for a small commitment. Do not send this to fifty people. Send it to three, properly.
""",
)

page(
    id="takehome",
    title="Take-Home Tests & Interviews",
    sub="The part that decides the offer",
    eyebrow="CAREER",
    subtitle="Take-homes and technical interviews are where most capable people lose roles they should win. Here is what is actually being evaluated.",
    chips=["Take-homes", "System design", "Live coding"],
    body=r"""
## The uncomfortable truth

Take-home tests and technical interviews are not primarily tests of whether you can write code. They are tests of whether you can **work the way the team works** — communicate, scope, prioritise, and finish. Most candidates lose on process, not on ability.

Everything below is about process.

## Take-home tests

### The first 20 minutes: read, do not code

The most common failure is starting to code before understanding the brief. Spend the first 20 minutes on:

1. **List every explicit requirement.** If the brief says "include overdue detection", that is a requirement, and forgetting it is fatal regardless of code quality.
2. **List every ambiguous term** and decide how you will interpret it. Write the decision down.
3. **Decide the schema first.** The data model is the part reviewers look at hardest and the part that is expensive to change later.
4. **Write a short plan in the README before any code.** This is the first thing a reviewer reads, and it frames everything after it.

### The build order

~~~text
1. Schema and migrations, with real constraints
2. Core endpoints, tested as you go
3. The one genuinely hard piece, isolated as a pure function
4. Tests for the tricky logic only
5. README: what it does, how to run it, decisions, next steps
~~~

Tests for the tricky logic — not everything. A take-home with 100% coverage and a wrong schema scores worse than one with four tests around the genuinely hard calculation.

### The last 20 minutes: the part everyone skips

- **Clone it fresh and run it.** `git clone`, install, start, hit the endpoint. Roughly half of broken take-homes fail exactly here, in the candidate's own environment, and would have been caught by ten minutes of checking.
- **Re-read the brief line by line against your implementation.** Tick every requirement off explicitly.
- **Write the "what I would do with more time" section.** This signals seniority more than any feature you could add, because it shows you can see the limits of your own work.

### What reviewers actually score, in order

| Rank | What they check | Why |
|---|---|---|
| 1 | Does it run | Nothing else matters if it does not |
| 2 | Is the schema sound | Schema mistakes are the most expensive to fix |
| 3 | Is the hard logic correct | This is the actual test |
| 4 | Is the README clear | Communication is a job requirement, not a bonus |
| 5 | Are there tests | Shows you know what is risky |
| 6 | Is the architecture sensible | Impressive architecture on a broken app scores zero |

Fancy architecture, a beautiful UI, or an elaborate test pyramid will not rescue a take-home that fails at rank 1.

### The traps

- **Over-engineering.** A microservices take-home for a CRUD brief reads as a junior who has read about microservices. Build the simplest thing that satisfies the brief, well.
- **Under-testing the edge cases.** Empty input, a missing record, concurrent writes, a very long string. The edge cases are the interview.
- **Silent assumptions.** If you assumed single-tenant, say so in the README. An undocumented assumption looks like an oversight; a documented one looks like a decision.
- **Submitting late.** A late submission signals that you cannot manage a deadline, which is a bigger red flag than a smaller scope.

## Live coding interviews

### Say your thinking out loud

Silence is the single most common reason capable candidates fail live coding. The interviewer cannot see your reasoning, and an interviewer who cannot follow you cannot score you. Narrate:

~~~text
"So the input is a list of intervals. Let me start with the
brute-force approach to make sure I understand the problem,
then optimise. Brute force is O(n^2) - for each interval,
compare against every other one. That is correct but slow.

The optimisation: sort by start time first, which is O(n log n),
then a single pass comparing adjacent intervals. That is O(n)
after the sort, so O(n log n) overall.

Let me code the sorted version. Edge cases: empty list, a
single interval, and overlapping at the boundary - does [1,2]
and [2,3] count as overlapping? I will assume yes, since the
endpoints touch."
~~~
That last sentence — asking about an ambiguity — is worth more than solving it silently and correctly. Interviewers are evaluating whether you will clarify requirements on the job.

### The structure that works

1. **Restate the problem** in your own words. Confirms understanding and buys thinking time.
2. **Ask 2–3 clarifying questions.** Input size, edge cases, expected output format, what "valid" means.
3. **Talk through a brute-force solution first.** It proves you can produce a correct answer, and it is the base case for optimisation.
4. **Optimise out loud**, stating the complexity before and after.
5. **Code it**, talking as you go.
6. **Test it** with a normal case, an empty case, and a boundary case — out loud, by hand, before declaring done.

### When you get stuck

Say so, then think out loud: "I am stuck on the off-by-one here. Let me trace through with a two-element input." Interviewers explicitly score how you handle being stuck, because everyone gets stuck at work. Freezing silently and typing nothing is the worst possible response. Thinking out loud while stuck is a good one.

### What they are actually evaluating

Not whether you have seen this exact problem. They are evaluating: can you decompose a problem, can you communicate, do you know when your solution is wrong, and can you accept a hint without falling apart. All four are learnable, and all four improve with practice — which is why recorded mock interviews weekly are worth more than any amount of reading.

## System design interviews

### Questions before diagrams

Spend the first five minutes asking, not drawing:

- What is the scale — requests per second, data volume, growth rate?
- What is the latency requirement?
- Is this read-heavy or write-heavy?
- What happens on failure — retry, drop, degrade?
- Are there consistency requirements, or is eventual acceptable?

Then say the scale back: "So about 12 writes per second on average, maybe 60 at peak. That is a small system — the interesting problems here are reliability and correctness, not throughput." **Naming what is *not* hard is a senior signal.**

### The shape of a good answer

~~~text
1. Requirements and scale (5 min)
2. High-level diagram: client -> API -> service -> store (5 min)
3. Data model and access patterns (5 min)
4. The hard part, in depth (10 min) - this is where you earn the offer
5. Failure modes, monitoring, and what you would change at 10x scale (5 min)
~~~

Step 4 is the whole interview. Every system has one genuinely hard component — for a URL shortener it is ID generation, for a notification system it is not double-sending, for a feed it is fan-out. Find it, go deep, and talk about the trade-offs rather than presenting one answer as obviously correct.

### The four things to mention unprompted

1. **Idempotency** on any write path that can be retried.
2. **A queue** anywhere an external dependency can be slow or down.
3. **Monitoring and alerting** on symptoms, not causes.
4. **What breaks first at 10× scale**, and what you would change then.

These four separate candidates who have operated systems from candidates who have only designed them.

## The 48-hour rule

After any interview, send a short thank-you that adds something — a link to a relevant project, a thought on a problem they mentioned. Not a generic thank-you. Two sentences, within 24 hours.

And log it in the tracker with the next action and the date. An interview you do not follow up on is an interview you have silently withdrawn from.
""",
)
