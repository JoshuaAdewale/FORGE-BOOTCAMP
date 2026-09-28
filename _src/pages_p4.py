# -*- coding: utf-8 -*-
PAGES = []
G = "04 · Production (Wk 14–16)"

def page(**kw):
    kw.setdefault("group", G)
    PAGES.append(kw)

page(
    id="w14-docker",
    title="W14 · Docker, CI/CD & Deployment",
    sub="Week 14",
    eyebrow="WEEK 14 · PRODUCTION",
    subtitle="Getting code from your laptop to the internet reliably, repeatedly, and without fear.",
    chips=["35 hours", "Docker · Actions · cloud"],
    body=r"""
## Docker: the mental model

A **container** is a process running with an isolated filesystem, network, and process namespace. An **image** is the immutable filesystem template. Not a VM — no guest OS, so startup is milliseconds. Its value: the same image runs identically on your laptop, in CI, and in production. "Works on my machine" becomes a non-issue.

```
# Multi-stage build: small, secure production images
FROM node:20-slim AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

FROM node:20-slim AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

FROM node:20-slim AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN useradd -m -u 1001 app                      # never run as root
COPY --from=build --chown=app /app/dist ./dist
COPY --from=deps  --chown=app /app/node_modules ./node_modules
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD node dist/health.js || exit 1
CMD ["node", "dist/server.js"]
```

**Image discipline:** pin base image versions, order layers from least to most frequently changing (dependencies before source) so caching works, use `.dockerignore` (`node_modules`, `.git`, `.env`), run as non-root, never bake secrets into images, and scan with `docker scout` or Trivy.

```
# docker-compose.yml - your entire stack, one command
services:
  api:
    build: .
    ports: ["3000:3000"]
    environment:
      DATABASE_URL: postgres://dev:dev@db:5432/app
      REDIS_URL: redis://cache:6379
    depends_on:
      db: { condition: service_healthy }
  db:
    image: postgres:16
    environment: { POSTGRES_USER: dev, POSTGRES_PASSWORD: dev, POSTGRES_DB: app }
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 5s
  cache:
    image: redis:7-alpine
volumes: { pgdata: }
```

New team member onboarding becomes `git clone && docker compose up`. That is the goal.

## CI/CD

**CI** = every push is automatically built and tested. **CD** = passing code is automatically deployed. This is a top-10 requirement in current job listings, because it is the mechanism that catches bugs and security issues early.

```
name: CI/CD
on:
  push: { branches: [main] }
  pull_request:

jobs:
  quality:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: test }
        options: >-
          --health-cmd pg_isready --health-interval 5s --health-retries 10
        ports: ["5432:5432"]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test:unit --coverage
      - run: pnpm db:migrate
        env: { DATABASE_URL: postgres://postgres:test@localhost:5432/postgres }
      - run: pnpm test:integration
      - run: pnpm build
      - uses: actions/upload-artifact@v4
        with: { name: build, path: dist }

  e2e:
    needs: quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx playwright install --with-deps chromium
      - run: pnpm test:e2e

  deploy:
    needs: [quality, e2e]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/deploy.sh
        env: { DEPLOY_TOKEN: "${{ secrets.DEPLOY_TOKEN }}" }
```

**Branch protection on `main`:** require PR review, require CI to pass, no direct pushes. Set this on your own repos — it builds the habit and signals professionalism to anyone browsing.

## Database migrations in a pipeline

The rule: **migrations must be backward compatible with the currently running code**, because during a deploy both versions run simultaneously.

The **expand/contract pattern** for a breaking change (e.g. renaming a column):
1. **Expand:** add the new column, write to both, deploy.
2. **Backfill:** copy historical data in batches (never one giant `UPDATE` — it locks the table).
3. **Migrate reads:** deploy code reading the new column.
4. **Contract:** stop writing the old column, then drop it in a later release.

Never: `DROP COLUMN` in the same deploy as the code change; add a `NOT NULL` column without a default to a big table; create an index without `CONCURRENTLY` in production.

## Deployment targets, and what to pick

| Platform | Best for | Notes |
|---|---|---|
| **Vercel** | Next.js frontends | Effortless; watch function costs at scale |
| **Fly.io / Render / Railway** | Node/Python APIs, workers | Containers, easy Postgres/Redis, sane pricing |
| **Cloudflare Workers/Pages** | Edge APIs, static, R2 storage | Very cheap, huge free tier, some runtime limits |
| **AWS (ECS/Fargate, RDS, S3)** | Enterprise, compliance | Steepest curve, most job listings mention it |
| **VPS (Hetzner/DigitalOcean) + Docker + Caddy** | Cost control, learning | You manage everything — do this once, it teaches you a lot |

Learn one managed platform for shipping speed, and do **one manual VPS deployment** (provision a server, install Docker, set up Caddy for TLS, configure a systemd unit, set up backups and a firewall). That exercise teaches more about production than any tutorial.

## Environments and configuration

Three environments: **development** (local), **staging** (production-like, real data shape, fake data), **production**. Twelve-factor principles: config in environment variables, never in code; strict separation of build and run; treat logs as event streams; stateless processes.

**Secrets:** never in git. Use the platform's secret store or Doppler/Infisical/AWS Secrets Manager. Rotate on any suspicion. Add `gitleaks` to your pre-commit hook.

**Feature flags** (a senior habit): deploy code dark, enable per user or percentage, roll back instantly without a redeploy. This decouples "deploy" from "release" and is how mature teams ship safely.

:::ship Week 14 deliverable
Your capstone, fully containerized: multi-stage Dockerfiles for web/api/worker, `docker compose up` runs the whole stack locally with seeded data, a CI pipeline running lint + typecheck + unit + integration + E2E, automated migrations, staging and production environments, and one **documented rollback** you actually performed. Write "From laptop to production: my deployment pipeline" with a diagram.
:::
""",
)

page(
    id="w15-obs",
    title="W15 · Observability & Reliability",
    sub="Week 15, Day 1–3",
    eyebrow="WEEK 15 · PRODUCTION",
    subtitle="Running software you did not just write, at 2am, when it is broken and users are complaining.",
    chips=["18 hours", "Logs · metrics · traces · SLOs"],
    body=r"""
## The three pillars

**Logs** — discrete events with context. **Metrics** — numeric time series, cheap to store and aggregate. **Traces** — the path of one request across services with timing at each hop. You need all three; each answers a different question.

### Structured logging (the single highest-value change)

```
import pino from "pino";
export const log = pino({
  level: process.env.LOG_LEVEL ?? "info",
  redact: ["req.headers.authorization", "req.headers.cookie", "*.password", "*.bvn", "*.card"],
});

// Bad:  log.info(`User ${id} paid ${amount}`)        <- unqueryable text
// Good: structured fields you can filter and aggregate
log.info({ event: "payment.completed", userId, orderId, amountKobo, provider: "paystack", durationMs }, "payment completed");
```

Every log line should carry a **request ID / trace ID** propagated through every service and job, so you can reconstruct one user's journey from a single identifier. Log at boundaries (request in/out, external calls, job start/end) and on every error with full context. Never log secrets, tokens, card data, BVN, or full personal records — this is both a security and a regulatory issue (NDPR in Nigeria, GDPR in the EU).

### Metrics that matter

The **RED method** for services: **R**ate (requests/sec), **E**rrors (failure %), **D**uration (latency distribution). The **USE method** for resources: **U**tilization, **S**aturation, **E**rrors.

**Always look at percentiles, never averages.** An average of 200ms hides that 5% of users wait 4 seconds. Track p50, p95, p99. Business metrics belong here too: signups, orders, payment success rate, queue depth — an alert on "payment success rate dropped below 95%" catches problems that infrastructure metrics never will.

```
// OpenTelemetry - the vendor-neutral standard. Instrument once, export anywhere.
import { NodeSDK } from "@opentelemetry/sdk-node";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
new NodeSDK({ instrumentations: [getNodeAutoInstrumentations()] }).start();

// Custom span for the part you care about
await tracer.startActiveSpan("reconcile.daily", async span => {
  span.setAttribute("provider", "paystack");
  const result = await reconcile();
  span.setAttribute("mismatches", result.mismatches.length);
  span.end();
});
```

Tooling: **Sentry** (errors — set this up on day one of any project, free tier is generous), **Grafana + Prometheus** or **Grafana Cloud**, **Axiom** or **Better Stack** for logs, **Uptime monitoring** with an external checker.

## SLIs, SLOs, and error budgets

- **SLI** (indicator): the measurement, e.g. "% of requests served < 500ms".
- **SLO** (objective): the target, e.g. "99.5% over 30 days".
- **Error budget:** 100% − SLO. At 99.5%, you may be down ~3.6 hours per month. If you have budget left, ship fast. If you have burned it, stop feature work and fix reliability.

This framework turns "is it reliable enough?" from an argument into a number. Being able to discuss it puts you ahead of most mid-level engineers.

**Alert on symptoms, not causes.** "Checkout error rate > 2% for 5 minutes" is actionable. "CPU > 80%" is noise. Every alert must be urgent, actionable, and have a runbook — otherwise you train yourself to ignore alerts, which is worse than having none.

## Resilience patterns

```
// Timeouts on EVERY external call. A hanging dependency takes your service down with it.
const res = await fetch(url, { signal: AbortSignal.timeout(3000) });

// Circuit breaker: stop hammering a service that is already down
class CircuitBreaker {
  private failures = 0; private openedAt = 0;
  constructor(private threshold = 5, private cooldownMs = 30_000) {}
  async call<T>(fn: () => Promise<T>, fallback?: () => T): Promise<T> {
    if (this.failures >= this.threshold) {
      if (Date.now() - this.openedAt < this.cooldownMs) {
        if (fallback) return fallback();
        throw new AppError("CIRCUIT_OPEN", "Service temporarily unavailable", 503);
      }
      this.failures = 0;                          // half-open: allow one trial
    }
    try { const r = await fn(); this.failures = 0; return r; }
    catch (e) { this.failures++; this.openedAt = Date.now(); throw e; }
  }
}
```

Also: **graceful degradation** (show cached data when the recommendation service is down rather than erroring the whole page), **bulkheads** (separate connection pools so one slow dependency cannot exhaust all resources), **graceful shutdown** (stop accepting new requests, finish in-flight work, close connections — otherwise every deploy drops requests), and **health checks** distinguishing liveness (am I alive?) from readiness (can I serve traffic?).

## Backups and disaster recovery

Define your **RPO** (how much data you can afford to lose) and **RTO** (how long you can be down). Then:
- Automated daily backups plus point-in-time recovery.
- **Test the restore.** An untested backup is a hope, not a backup. Restore into a scratch environment quarterly and time it.
- Store backups in a different region/provider than production.
- Document the recovery runbook so someone else could execute it.

## Incident response

1. **Acknowledge** — someone owns it.
2. **Mitigate first, diagnose second.** Roll back, disable the feature flag, scale up. Restore service before understanding the root cause.
3. **Communicate** — status page, honest and frequent updates.
4. **Blameless postmortem** — timeline, impact, root cause (use "5 whys"), and action items with owners and dates. Blame produces hiding; hiding produces repeat outages.

:::edge Write a postmortem for a self-inflicted incident
Deliberately break your staging environment (drop an index, exhaust the connection pool, deploy a bad migration), then run the full incident process on yourself: detect via your own alerts, mitigate, and write a real postmortem. Publishing one thoughtful postmortem signals operational maturity that almost no junior candidate can demonstrate.
:::
""",
)

page(
    id="w15-sysdesign",
    title="W15 · System Design",
    sub="Week 15, Day 4–6",
    eyebrow="WEEK 15 · PRODUCTION",
    subtitle="The skill that determines your seniority, your salary band, and whether you pass the final interview round.",
    chips=["18 hours", "Architecture · trade-offs"],
    body=r"""
## The framework for any design question

Interviewers are testing structured thinking and trade-off awareness, not memorized architectures. Use this in every design discussion, in interviews and at work:

1. **Clarify requirements** (5 min). Functional: what must it do? Non-functional: how many users, read/write ratio, latency target, consistency needs, budget? **Never start drawing before this.** The candidates who fail are the ones who start designing immediately.
2. **Estimate scale** (5 min). Back-of-envelope: 1M daily active users × 20 requests = 20M/day ≈ 230/sec average, maybe 1,000/sec peak. Storage: 1M orders/month × 2 KB = 2 GB/month. These numbers determine the architecture.
3. **Define the API and data model** (10 min). Endpoints and the core tables. Most systems live or die here.
4. **High-level architecture** (10 min). Client → CDN → load balancer → API → cache → database, plus queues and workers. Draw it.
5. **Deep dive** (15 min) on whatever the interviewer probes — usually the hardest part.
6. **Identify bottlenecks and scale** (10 min). Where does it break at 10x? What is the fix?
7. **Discuss trade-offs.** Every choice has a cost. Saying so out loud is the mark of seniority.

## The concept vocabulary

++ Vertical vs horizontal scaling :: Bigger machine vs more machines. Vertical is simpler and often correct until surprisingly late; horizontal needs statelessness.
++ Load balancing :: Round-robin, least-connections, consistent hashing. Health checks remove dead instances.
++ Caching layers :: Browser, CDN, application (Redis), database. Cache closest to the user that is safe.
++ Database replication :: One primary for writes, read replicas for reads. Beware replication lag — a user may not see their own write.
++ Sharding / partitioning :: Split data across machines by key or time. Powerful, painful. Delay it as long as possible.
++ CAP theorem :: Under a network partition, choose consistency or availability. Most systems are partition-tolerant, so it is CP or AP per operation.
++ Consistency models :: Strong (banking balances) vs eventual (view counts, feeds). Choose per feature, not per system.
++ Async decoupling :: Queues absorb spikes and isolate failure. The default answer to "the request is too slow."
++ Idempotency :: Retries are inevitable at scale. Design every write to tolerate them.
++ Monolith vs services :: Start with a well-structured modular monolith. Extract a service only when a real constraint (team scaling, independent scaling, isolation) demands it.

:::edge The trap in every system design interview
Over-engineering. A candidate asked to design a URL shortener who immediately proposes Kubernetes, Kafka, and five microservices has failed — they showed they cannot match solution to problem. The strong answer starts simple ("a single Postgres and an API handles 1,000 writes/sec comfortably"), then adds complexity **only where the stated requirements force it**, and names the cost each time. "We could shard, but that adds operational burden and cross-shard queries; at your stated 10M rows we do not need it yet" is a senior sentence.
:::

## Three worked designs

### 1. A ride-hailing dispatch (matching + geo)
Requirements: 50k drivers, 200k riders/day, match in < 5 seconds, live location. Core issues: **geospatial indexing** (PostGIS or geohash/H3 cells in Redis to find nearby drivers in O(1)), **high-frequency location writes** (do not write every ping to Postgres — Redis with periodic persistence), **matching as a queue** with a state machine per trip, **realtime** via WebSocket with a Redis backplane, **idempotency** so a duplicate accept does not double-assign. Discuss: what happens when two drivers accept simultaneously? (Atomic conditional update or a lock.)

### 2. A payments/wallet system
Requirements: exact correctness, audit trail, provider webhooks, reconciliation. Core issues: **double-entry ledger** (append-only), **idempotency keys**, **transactional consistency** for balance changes, **webhook deduplication and ordering**, **reconciliation jobs**, **PCI scope minimization** (never touch card data — tokenize with the provider). Discuss: how do you handle a webhook that arrives before the transaction record exists? (Store and reprocess, or create-on-demand.)

### 3. An analytics dashboard over 500M events
Requirements: sub-second queries over a year of data, 50 concurrent analysts. Core issues: **OLTP vs OLAP separation** (never run analytics on your production database), **columnar storage** (BigQuery, ClickHouse, DuckDB, or Postgres with partitioning), **pre-aggregation** (materialized rollups by hour/day), **incremental models** (dbt), **caching by query fingerprint**. Discuss: the trade-off between query freshness and cost.

## Practice protocol

Do one design per week for the rest of the program, written in a doc with a diagram, timeboxed to 45 minutes: URL shortener, chat app, news feed, notification service, rate limiter, file storage, ticket booking with no double-selling, food delivery, video streaming, distributed job scheduler.

For each, write: requirements, estimates, API, schema, diagram, bottlenecks, and **three trade-offs you made and why**. Keep them in `forge-notes/design/`. This becomes both interview preparation and public evidence of architectural thinking.

:::drill Reverse-engineer a real system
Pick a product you use (Paystack, Jumia, Bolt, WhatsApp). Write how you believe it is architected, then find their engineering blog posts and compare. The gap between your guess and reality is precisely the learning. Publish the comparison — these posts perform very well and demonstrate exactly the thinking employers screen for.
:::
""",
)

page(
    id="w16-integration",
    title="W16 · Full-Stack Integration Sprint",
    sub="Week 16",
    eyebrow="WEEK 16 · PRODUCTION",
    subtitle="Everything from Phases 1–4 assembled into one production system you operate, not just build.",
    chips=["35 hours", "Portfolio piece #4"],
    body=r"""
## The brief: a complete SaaS product

Build a **multi-tenant B2B SaaS** end to end. Choose the domain (school management, clinic billing, freight brokerage, inventory + POS for retail, field-service dispatch, or microfinance loan management). Requirements are the same regardless:

### Functional
- Organization signup, team invitations, role-based access (owner/admin/member/viewer)
- The core domain workflow, complete, with at least three entity types and a real state machine
- Search, filtering, sorting, pagination across the main list views
- File uploads with previews
- An analytics dashboard with at least six meaningful metrics and two charts
- Notifications: in-app, email, and one realtime channel
- Subscription billing with a free tier and usage limits (Paystack/Stripe test mode)
- Data export (CSV and PDF), and a public read-only share link
- Audit log of who did what, when
- A settings area: profile, org, billing, API keys, notification preferences

### Technical (non-negotiable)
- Next.js App Router + TypeScript strict; server components by default
- Node/Hono API (or Next route handlers) + a Python analytics service
- PostgreSQL with migrations, proper indexes, and **row-level security for tenant isolation**
- Redis for caching, rate limiting, and queues; BullMQ workers in a separate process
- Object storage with presigned uploads
- Auth with sessions/refresh rotation, MFA optional, and audit logging
- Docker Compose for local; deployed to production with CI/CD
- Sentry + structured logs + a `/metrics` endpoint + uptime monitoring
- Tests: unit, integration (with a real test DB), and E2E on the three critical paths
- Load tested: report p95 latency at 100 concurrent users, and the fix for whatever broke first

### Operational (this is what makes it stand out)
- A **runbook**: how to deploy, roll back, restore a backup, rotate a secret, and respond to the top three likely incidents
- An **architecture decision record** (ADR) folder with at least five decisions documented in the format: context → options considered → decision → consequences
- A **seeded demo environment** with a public login so anyone can try it in 10 seconds without signing up
- A 5-minute narrated demo video

## Suggested week structure

@@ Day 1 | Requirements, data model, ADRs, API contract, wireframes. Nothing else. Resist coding.
@@ Day 2 | Auth, tenancy, RLS, base layout, CI pipeline running from the first commit.
@@ Day 3 | Core domain: full vertical slice of the primary workflow, tested.
@@ Day 4 | Secondary features, billing, notifications, background jobs.
@@ Day 5 | Analytics service, dashboard, exports, realtime.
@@ Day 6 | Hardening: security pass, performance pass, load test, observability, runbook, demo, deploy.

:::edge Make one thing genuinely excellent
Reviewers cannot evaluate everything, so they sample. Choose one dimension and make it exceptional: a beautiful, fast UI; a bulletproof payments ledger; a sub-100ms dashboard over 10M rows; or best-in-class accessibility. Then lead with it in your README and in interviews. Depth in one visible area reads as competence everywhere; uniform mediocrity reads as a tutorial project.
:::

:::ship Phase 4 exit criteria
You can design, build, secure, deploy, monitor, and operate a real multi-tenant system. At this point you are employable as a full-stack engineer — mid-level in capability, junior only in job title. The remaining ten weeks add the two things that push you into the top percentile: AI-native engineering, and genuine data analysis depth.
:::
""",
)
