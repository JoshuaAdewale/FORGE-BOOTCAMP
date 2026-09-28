# -*- coding: utf-8 -*-
PAGES = []

def page(**kw):
    PAGES.append(kw)

page(
    id="start",
    group="00 · Orientation",
    title="Read This First",
    sub="The contract",
    eyebrow="FORGE BOOTCAMP · 26 WEEKS",
    subtitle="A full-time, zero-to-top-1% program in full-stack engineering and data analysis. Built for someone starting from nothing and finishing employable at a global standard.",
    chips=["26 weeks · 35 hrs/week", "Zero experience assumed", "Ships 12 real products"],
    track=False,
    body=r"""
## What this is

This is not a list of tutorials. It is a **training system** with four properties that separate people who get hired from people who collect certificates:

1. **Everything is built, nothing is watched.** Each week ends with a deliverable in a public repo with a live URL.
2. **You learn the layer below.** Most bootcamp graduates know a framework. You will know HTTP, the event loop, query planners, and index B-trees. That is the difference between "React developer" and "engineer".
3. **You are trained as a problem-solver in a domain, not a tool operator.** Every project comes from a real sector: fintech, agriculture, health, logistics, energy, public data.
4. **AI is treated as a power tool, not a threat.** The 2026 market does not pay for code typing. It pays for judgment, system design, data modeling, and the ability to verify what a model produced. You will use AI aggressively *and* be able to work without it.
5. **You start earning in Week 2, not Week 26.** Waiting six months to make money is a luxury most people do not have, and unpaid learning has no feedback loop — a client who will not pay tells you the truth about your skill in a way no tutorial can. Every phase upgrades what you sell, at a price that respects your ability.
6. **You build for the world market from day one.** Earning in dollars while spending in naira is a 5–10× lever on the same hours of work. Your stack is already global-standard; what most Nigerian developers never build is the *go-to-market* — international payment rails, professional communication, and public proof. The Global Track group covers all three, and you should start it in Week 1, not Week 26.

## The top 0.1% reality

Twenty-six weeks will not make you world-class — nothing will. What it can do is start the machine that compounds for the next ten years.

| Percentile | What it means | Timeline |
|---|---|---|
| Top 25% | Can build working software | 3–6 months |
| Top 10% | Can ship production software unsupervised | 1–2 years |
| Top 1% | Can design, operate, and explain systems | 3–5 years |
| Top 0.1% | Recognized expertise — people seek you out | 8–15 years of public compounding |

The 0.1% is not the most gifted. It is the group that picked one narrow thing, went absurdly deep, did it **publicly**, and did not quit. Almost nobody does all three — which is exactly why the percentile is so sparsely populated.

So measure yourself in **assets accumulated, not lessons completed**: public writing, an open-source project people use, a documented specialization, USD income rails, an audience. All six are available to you in Week 1 at your current skill level. Read *The Top 0.1% Path* in the Global Track group before Week 2.

## The market you are training for

| Role you can take at week 26 | What it needs | Where it pays |
|---|---|---|
| Full-Stack Engineer | TypeScript, React/Next.js, Node, PostgreSQL, Docker, CI/CD, cloud | Product startups, agencies, remote contracts |
| AI-Integrated Engineer | The above + LLM APIs, RAG, evals, vector search | Fastest-growing 2026 category, highest premium |
| Data / Analytics Engineer | SQL (window functions, CTEs), Python, dbt, warehouse modeling, BI | Fintech, telco, banks, NGOs, e-commerce |
| Product / Business Analyst | SQL + statistics + experimentation + storytelling | Any company with users and revenue |

Research across 2026 hiring data converges on the same core: **TypeScript everywhere, React/Next.js frontend, Node or Python backend, PostgreSQL, Docker, CI/CD, one cloud** for engineering; and **advanced SQL, Python/pandas, one BI tool, statistics, and business communication** for analytics. This program covers all of it and then goes two levels deeper than a typical bootcamp.

## The 26 weeks at a glance

++ Phase 1 · Weeks 1–4 :: Foundations. Terminal, Git, how the web actually works, HTML/CSS, JavaScript, TypeScript, algorithmic thinking.
++ Phase 2 · Weeks 5–8 :: Frontend engineering. React, Next.js App Router, data fetching, forms, design systems, accessibility, performance, testing.
++ Phase 3 · Weeks 9–13 :: Backend and data layer. Node APIs, PostgreSQL and data modeling, auth and security, payments, queues, caching, realtime, FastAPI.
++ Phase 4 · Weeks 14–16 :: Production engineering. Testing strategy, Docker, CI/CD, cloud deployment, observability, system design, incident response.
++ Phase 5 · Weeks 17–18 :: AI-native engineering. LLM APIs, structured output, RAG with pgvector, evals, guardrails, agents, cost control.
++ Phase 6 · Weeks 19–24 :: Data analysis. Metric design, analytical SQL, pandas/Polars, statistics and experimentation, dbt and analytics engineering, BI and executive storytelling, forecasting.
++ Phase 7 · Weeks 25–26 :: Capstone and market entry. One flagship product, portfolio, interviews, freelancing, pricing, offers.

## The weekly rhythm (35 hours)

You are running **two tracks in parallel** from Week 1: the curriculum, and paid client work. They are not in competition — the client work is where the learning compounds fastest.

@@ Mon–Thu | 6 hrs/day: 1 hr concept and notes, 2.5 hrs building the curriculum project, 2 hrs client/project work, 30 min written recall.
@@ Friday | 6 hrs: integration and delivery day. Deploy the curriculum project, deliver client work, invoice anything finished.
@@ Saturday | 5 hrs: 2 hrs drills, 1.5 hrs prospecting and outreach, 1.5 hrs public output.
@@ Sunday | Rest, or 2 hrs of light review. Burnout kills more careers than difficulty does.

The ratio shifts as you climb the **income ladder** (roughly 70/30 learning-to-earning in Weeks 1–4, reaching 40/60 by Week 18, when clients start paying you to learn things you would have learned anyway). The full schedule and the escalation pattern are in *The Paid Learning Rhythm*, and the week-by-week money map is in *The Income Map* — both in the Income Track group. **Read those two before Week 3.**

:::edge Build once, sell many times
Every weekly project is not just a portfolio piece — it is a **template you can sell repeatedly**. Build a restaurant site in Week 2 and you can sell restaurant sites for the next two years. Build an inventory system in Week 12 and every retailer in your city is a prospect.

This is why the curriculum is sequenced the way it is. Each phase produces a product, and each product has a market. Your first paid project should come from Week 2 material — see *Your First Client in 14 Days*.
:::

:::edge The top-1% multiplier
Ordinary students finish a lesson and move on. You will finish each lesson by writing a 150-word explanation of it **from memory, in your own words**, and posting it publicly. This does three things at once: it converts recognition into recall, it builds a searchable body of proof that you understand things, and it compounds into an audience before you ever apply for a job. Twenty-six weeks of this is ~150 public artifacts. Almost nobody does it. That is exactly why it works.
:::

## Rules of the program

1. **No copy-paste you cannot explain.** If AI or Stack Overflow gives you code, you must be able to delete a line and predict what breaks.
2. **Ship broken over perfect.** A deployed ugly app beats a beautiful local one. Always.
3. **Public by default.** Every repo public, every write-up public, every dashboard shareable.
4. **Time-box debugging to 45 minutes**, then write the question out fully. Half the time you will solve it while writing.
5. **Never skip a Friday deploy.** The habit of shipping is the actual skill.

## What you need

- A laptop (8 GB RAM minimum, 16 GB comfortable), reliable-enough internet, and power backup planning if you are in Nigeria — schedule heavy installs and deploys for stable-power windows.
- Free-tier accounts only: GitHub, Vercel, Neon or Supabase (Postgres), Cloudflare, Render or Fly.io, Google Cloud free tier / BigQuery sandbox, Power BI Desktop or Metabase, one LLM API with a spend cap.
- Zero paid courses required. Every tool in this program has a free tier that is enough.

Start with the next page: your environment. Do not read ahead until your terminal works.
""",
)

page(
    id="setup",
    group="00 · Orientation",
    title="Week 0 · Environment Setup",
    sub="Before day one",
    eyebrow="ORIENTATION",
    subtitle="Two days. Get a professional development machine running before the clock starts.",
    chips=["2 days", "Deliverable: green checkmark on a CI run"],
    body=r"""
## Objective

End Week 0 with a machine that a senior engineer could sit down at and work on, and a GitHub profile that already has one green-lit repository.

## Step 1 — The operating layer

**Windows users:** install WSL2 (Windows Subsystem for Linux) with Ubuntu. Do all your development *inside* Linux, not in Windows paths. This eliminates 80% of "works on my machine" pain later.

~~~
wsl --install -d Ubuntu
~~~

**macOS users:** install Homebrew. **Linux users:** you are already set.

## Step 2 — Core toolchain

~~~
# version manager for Node (never install Node directly)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
nvm install --lts && nvm use --lts

# Python via uv - the modern, fast Python manager
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12

# Git, and a package manager
sudo apt update && sudo apt install -y git build-essential curl unzip
corepack enable && corepack prepare pnpm@latest --activate
~~~

Install **VS Code** (or Cursor, which is VS Code plus AI). Extensions to add on day one: ESLint, Prettier, Error Lens, GitLens, Tailwind CSS IntelliSense, Python, Jupyter, and the Docker extension. Also install **Docker Desktop** — you will not use it until Week 14 but installing it early saves a bad day later.

## Step 3 — Identity

~~~
git config --global user.name "Your Real Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
ssh-keygen -t ed25519 -C "you@example.com"
cat ~/.ssh/id_ed25519.pub    # paste into GitHub > Settings > SSH keys
~~~

Create your GitHub account with a **professional username** — this is a career asset you will use for a decade. `chidi-okafor` beats `xXdarkcoderXx`. Add a real photo, a one-line bio, and your location.

## Step 4 — Accounts to open now

- **GitHub** (code + portfolio), **Vercel** (frontend hosting), **Neon** or **Supabase** (free PostgreSQL)
- **Render** or **Fly.io** (backend hosting), **Cloudflare** (DNS, R2 storage, Workers)
- **Google account** → BigQuery sandbox (free 1 TB/month querying) and Looker Studio
- **Kaggle** (datasets), **Hugging Face** (models/datasets), one LLM provider with a hard spend cap set
- A **domain name** (~$10/yr). `yourname.dev` or `.com`. This is the single highest-leverage $10 in your career.

## Step 5 — The hello-world that proves the pipeline

~~~
mkdir -p ~/dev/forge-hello && cd ~/dev/forge-hello
npm init -y && git init
mkdir -p .github/workflows
~~~

Create `index.js`:

~~~
export function greet(name) {
  if (!name) throw new Error("name is required");
  return `Hello, ${name}. Week 0 complete.`;
}
console.log(greet("Forge"));
~~~

Create `.github/workflows/ci.yml`:

~~~
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: node --experimental-vm-modules index.js
~~~

Push it. When you see the green checkmark on GitHub, you have just used version control, a remote, and a continuous integration pipeline — three things most beginners do not touch for months.

:::ship Week 0 deliverable
A public repo named `forge-hello` with a passing GitHub Actions badge in its README, plus a `README.md` stating: your name, the 26-week goal, and the date you started. You will link back to this on graduation day.
:::

## Step 6 — Set up your learning system

Create a second repo, `forge-notes`, with this structure. Every lesson's 150-word recall goes here, and it doubles as your public blog later.

~~~
forge-notes/
  README.md          # index with links, updated weekly
  week-01/
    day-1.md
    ...
  projects/          # one folder per shipped project, with screenshots
  drills/            # SQL and algorithm practice logs
~~~

:::drill Setup drill
Time yourself: from a fresh terminal, create a new folder, init git, create a file, commit, create a GitHub repo from the CLI (`gh repo create`), and push. Target: under 90 seconds without looking anything up. Repeat daily during Week 1 until it is muscle memory.
:::
""",
)

page(
    id="method",
    group="00 · Orientation",
    title="How to Learn 4x Faster",
    sub="The meta-skill",
    eyebrow="ORIENTATION",
    subtitle="The study protocol that separates people who finish from people who fade at week 9.",
    chips=["Read once, use forever"],
    body=r"""
## The failure pattern

Most self-taught developers fail in one of four ways, and all four are preventable:

| Failure | What it looks like | The fix built into this program |
|---|---|---|
| Tutorial hell | Endless courses, no original work | Every week ends in a deliverable you designed |
| Passive consumption | Watching, nodding, forgetting | Written recall after every lesson |
| Breadth without depth | Knows 9 frameworks, masters none | One stack, driven to production depth |
| Isolation | No feedback, no network | Public output + code review habits from week 1 |

## The five techniques

### 1. Active recall over re-reading
After each lesson, close everything and write what you learned from memory. Then check. The gap you find *is* the learning. Re-reading feels productive and is nearly worthless.

### 2. Spaced repetition on the small, hard facts
Some things must be instant: SQL join semantics, HTTP status codes, Git commands, `useEffect` dependency rules, pandas indexing, big-O of common operations. Put these in Anki or a simple `drills.md` and review 10 minutes daily. Ten minutes a day for 26 weeks is 75 hours of retrieval practice.

### 3. The Feynman loop
Explain the concept as if to a smart 12-year-old. Where you reach for jargon, you do not understand it yet. Post the explanation. This is your recall habit and your portfolio in one action.

### 4. Deliberate difficulty
Practice at the edge of your ability, not in your comfort zone. Concretely: rebuild yesterday's feature without looking at your notes; break your own code deliberately and predict the error; implement something twice, the second time from scratch.

### 5. Debug like an engineer, not a gambler
Beginners change random things and re-run. Do this instead:

1. **Read the actual error.** All of it. Bottom of the stack trace up.
2. **Reproduce it reliably.** Intermittent bugs are just bugs whose trigger you have not found.
3. **Form one hypothesis** and state it out loud: "I believe X is undefined because the fetch resolves after render."
4. **Design the cheapest test** of that hypothesis (a log, a breakpoint, a smaller input).
5. **Bisect.** Delete half the code. Still broken? The bug is in the remaining half.
6. **Record the fix** in your notes with the error message as the heading — searchable next time.

:::trap The AI trap that will cap your ceiling
Using AI to produce code you cannot read makes you fast this month and unemployable next year. The rule for this program: **AI may explain, review, generate tests, and draft boilerplate. You must be able to rewrite anything it produced without it.** Before week 17 you should regularly do "cold sessions" — 2 hours coding with all assistants off. The market pays for people who can judge output, and you cannot judge what you cannot write.
:::

:::edge How to use AI like the top 1%
- **Rubber duck with pressure:** "Here is my mental model of React server components. What is wrong with it?"
- **Adversarial review:** "Critique this schema like a staff engineer in a design review. Find three failure modes."
- **Explain the unfamiliar codebase:** paste a file, ask for a call-graph summary, then verify by reading.
- **Generate tests, not implementations.** Tests encode understanding; letting AI write them forces you to specify behavior.
- **Never** paste secrets, customer data, or employer proprietary code into a public model.
:::

## The weekly review (30 minutes every Sunday)

Answer these five questions in `forge-notes/week-XX/review.md`:
1. What did I ship this week that did not exist before?
2. What concept did I *think* I understood but did not?
3. What did I spend more than 45 minutes stuck on, and what was the actual root cause?
4. What will I do differently next week?
5. What is one thing I can now explain that I could not last Sunday?

This single file, kept honestly for 26 weeks, becomes the most persuasive artifact in your job search.
""",
)
