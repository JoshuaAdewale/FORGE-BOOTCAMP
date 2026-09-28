# -*- coding: utf-8 -*-
PAGES = []
G = "03 · Backend (Wk 9–13)"

def page(**kw):
    kw.setdefault("group", G)
    PAGES.append(kw)

page(
    id="w9-node",
    title="W9 · Node, APIs & Contracts",
    sub="Week 9, Day 1–3",
    eyebrow="WEEK 9 · BACKEND",
    subtitle="Node powers roughly half of all backends. Build APIs that other engineers would be happy to consume.",
    chips=["18 hours", "Node · Hono/Express · REST"],
    body=r"""
## Node's model, and why it matters

Node is single-threaded JavaScript with an event loop and a thread pool for I/O. It is exceptional at handling many concurrent I/O-bound requests (DB queries, HTTP calls) and terrible at CPU-bound work (image processing, big loops) — those block every other user. When you need CPU work: worker threads, a queue with separate workers, or a different language for that service.

```
// This one function ruins your whole server under load
app.get("/report", (req, res) => {
  const rows = fs.readFileSync("huge.csv");     // BLOCKS the event loop
  const result = heavyParse(rows);              // BLOCKS harder
  res.json(result);
});
// Fix: stream it, offload to a worker, or push to a queue and return 202 Accepted.
```

## Framework choice in 2026

**Hono** — fast, tiny, TypeScript-first, runs on Node/Bun/Cloudflare Workers/Deno. **Fastify** — mature, fast, schema-driven. **Express** — everywhere, huge ecosystem, worth knowing because you will meet it in existing codebases. **NestJS** — opinionated, Angular-like, common in enterprise. Learn Hono or Fastify well; read enough Express to be dangerous.

```
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

const app = new Hono();

// Middleware runs in order: cross-cutting concerns live here
app.use("*", requestId(), logger(), cors({ origin: ALLOWED }), secureHeaders());
app.use("/api/*", rateLimit({ windowMs: 60_000, max: 100 }));
app.use("/api/private/*", requireAuth());

const CreateOrder = z.object({
  items: z.array(z.object({ sku: z.string(), qty: z.number().int().positive() })).min(1),
  deliveryAddress: z.string().min(10),
  idempotencyKey: z.string().uuid(),
});

app.post("/api/orders", zValidator("json", CreateOrder), async (c) => {
  const body = c.req.valid("json");
  const user = c.get("user");
  const order = await orderService.create(user.id, body);
  return c.json({ data: order }, 201, { Location: `/api/orders/${order.id}` });
});

export default app;
```

## API design that earns respect

```
GET    /api/orders?status=paid&cursor=eyJ...&limit=50   # list, filtered, paginated
POST   /api/orders                                       # create -> 201 + Location
GET    /api/orders/:id                                   # read
PATCH  /api/orders/:id                                   # partial update
DELETE /api/orders/:id                                   # -> 204
POST   /api/orders/:id/cancel                            # state transition as a verb resource
```

**Rules:**
- Plural nouns for collections; nest at most one level deep (`/orders/:id/items`, not four levels).
- **Cursor pagination**, not offset, for anything that grows. Offset gets slower the deeper you go and skips/duplicates rows when data changes mid-scroll.
- **Consistent envelope:** `{ "data": ..., "meta": { "nextCursor": ... } }` for success; a single error shape for failures.
- **Versioning:** `/api/v1/...` or a header. Decide before your first external consumer.
- **Idempotency keys** on any operation that creates money movement — the client sends a UUID; you store it and return the original response on retry. This is how Stripe and every serious payment API work.

```
// One error shape, everywhere. Clients can actually program against this.
{
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "Only 3 units of RICE-50KG remain",
    "details": { "sku": "RICE-50KG", "requested": 10, "available": 3 },
    "requestId": "req_01HX..."
  }
}
```

```
// Centralized error handling with typed application errors
export class AppError extends Error {
  constructor(
    public code: string, message: string,
    public status = 400, public details?: unknown
  ) { super(message); }
}
export const NotFound = (what: string) => new AppError("NOT_FOUND", `${what} not found`, 404);

app.onError((err, c) => {
  const id = c.get("requestId");
  if (err instanceof AppError) {
    logger.warn({ id, code: err.code }, err.message);
    return c.json({ error: { code: err.code, message: err.message, details: err.details, requestId: id } }, err.status);
  }
  logger.error({ id, err }, "unhandled");
  return c.json({ error: { code: "INTERNAL", message: "Something went wrong", requestId: id } }, 500);
});
```

:::trap Never leak internals in errors
Stack traces, SQL fragments, and raw exception messages in API responses are an information-disclosure vulnerability and look amateur. Log the detail server-side with a request ID; return a safe message plus that ID to the client. Then support can say "give me your request ID" and you can find the exact log line.
:::

## Layered architecture (keep this discipline from day one)

```
src/
  routes/        # HTTP concerns only: parse, validate, call service, format response
  services/      # business logic. No req/res objects here. Testable in isolation.
  repositories/  # data access. The only place SQL lives.
  domain/        # types, entities, pure business rules
  lib/           # cross-cutting: logger, config, errors, db client
  jobs/          # background workers
```

The test of a good backend: **your business logic should be callable from an HTTP route, a CLI script, a queue worker, or a test — with no changes.** If `req` and `res` appear in your service layer, you have coupled yourself to HTTP forever.

## Documentation and contracts

Generate an **OpenAPI** spec from your Zod schemas (`@hono/zod-openapi` or `zod-to-openapi`) so docs cannot drift from reality. Serve Swagger UI or Scalar at `/docs`. For internal TypeScript monorepos, **tRPC** gives end-to-end type safety with no codegen. Know when each fits: OpenAPI for public/multi-language consumers, tRPC for a TS-only product team.

:::drill API drill
Take a public API you use (Paystack, GitHub, Stripe) and write a critique: how do they paginate, version, handle errors, model idempotency, and document? Then design your own API for a domain of your choice as an OpenAPI document *before writing any code*. Design-first is a senior habit; most juniors code first and document never.
:::
""",
)

page(
    id="w9-postgres",
    title="W9 · PostgreSQL & Data Modeling",
    sub="Week 9, Day 4–6",
    eyebrow="WEEK 9 · BACKEND",
    subtitle="The most consequential skill in backend work. A bad schema outlives every framework decision you make.",
    chips=["18 hours", "Schema · indexes · transactions"],
    body=r"""
## Why the schema matters most

You can rewrite your frontend in a month and swap your API framework in a week. A bad data model haunts a company for years — it corrupts data, blocks features, and forces expensive migrations. Learn to model well and you are immediately more valuable than most developers with twice your experience.

## Modeling process

1. **List the nouns** in the domain (order, customer, product, shipment).
2. **Define relationships and cardinality** (a customer has many orders; an order has many items; a product appears in many orders → join table).
3. **Find the natural keys and constraints** (an email is unique; a quantity must be > 0; an order cannot ship before it is paid).
4. **Normalize to 3NF first** — every fact stored once. Denormalize later, deliberately, with measurements to justify it.
5. **Decide what history you need.** Mutable rows lose the past. For anything financial or regulated, append-only event tables beat `UPDATE`.

```
CREATE TABLE customers (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email       citext NOT NULL UNIQUE,
  full_name   text   NOT NULL CHECK (length(trim(full_name)) > 1),
  phone       text   CHECK (phone ~ '^\+?[0-9]{10,15}$'),
  created_at  timestamptz NOT NULL DEFAULT now(),
  deleted_at  timestamptz
);

CREATE TYPE order_status AS ENUM ('pending','paid','shipped','delivered','cancelled','refunded');

CREATE TABLE orders (
  id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id   uuid NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  status        order_status NOT NULL DEFAULT 'pending',
  -- store money as integer minor units. NEVER float.
  total_kobo    bigint NOT NULL CHECK (total_kobo >= 0),
  currency      char(3) NOT NULL DEFAULT 'NGN',
  placed_at     timestamptz NOT NULL DEFAULT now(),
  metadata      jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE order_items (
  order_id      uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  sku           text NOT NULL,
  qty           integer NOT NULL CHECK (qty > 0),
  unit_kobo     bigint  NOT NULL CHECK (unit_kobo >= 0),
  PRIMARY KEY (order_id, sku)
);

CREATE INDEX orders_customer_placed_idx ON orders (customer_id, placed_at DESC);
CREATE INDEX orders_status_idx ON orders (status) WHERE status IN ('pending','paid');
```

:::trap Money in floating point
`0.1 + 0.2 !== 0.3` in binary floating point. Storing currency as `float`/`double` will produce accounting discrepancies that are extremely painful to unwind. Use `bigint` minor units (kobo, cents) or `numeric(19,4)`. This is a real question in fintech interviews and a real bug in production systems.
:::

:::edge Six schema decisions that mark a professional
1. **`timestamptz`, never `timestamp`.** Always store UTC; convert at the edge.
2. **UUIDv7 or ULID for public IDs.** Sequential integers leak business volume ("I am customer #43") and enable enumeration attacks. UUIDv7 keeps index locality that random UUIDv4 destroys.
3. **Constraints in the database, not only in application code.** Applications have bugs and multiple writers; the database is the last line of defense. `CHECK`, `NOT NULL`, `UNIQUE`, and foreign keys are free correctness.
4. **Soft delete deliberately.** `deleted_at` preserves history but every query must filter it — use a view. Sometimes hard delete plus an audit log is cleaner (and GDPR/NDPR may require real deletion).
5. **`jsonb` for genuinely variable data only.** It is not an excuse to avoid modeling. Index it with GIN when you query into it.
6. **Migrations, always.** Never change production schema by hand. Every change is a versioned, reviewed, reversible file.
:::

## Indexes: how the database actually finds rows

A B-tree index is a sorted structure giving O(log n) lookup instead of O(n) scanning. Without one, a query on 10 million rows reads all 10 million.

```
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = $1 ORDER BY placed_at DESC LIMIT 20;
```

Read the plan: **Seq Scan** on a large table in a filtered query is your warning sign. You want **Index Scan** or **Index Only Scan**. Watch the difference between estimated and actual rows — big gaps mean stale statistics (`ANALYZE`).

Index rules:
- Index columns used in `WHERE`, `JOIN`, and `ORDER BY`.
- **Composite index column order matters**: `(customer_id, placed_at)` serves `WHERE customer_id = ?` and `WHERE customer_id = ? ORDER BY placed_at` — but not `WHERE placed_at > ?` alone. Leftmost prefix rule.
- **Covering indexes** (`INCLUDE`) let Postgres answer entirely from the index.
- **Partial indexes** (`WHERE status = 'pending'`) are small and fast for hot subsets.
- Indexes cost write throughput and disk. Do not index everything; index what you query.
- Use `pg_stat_user_indexes` to find indexes nobody uses, and `pg_stat_statements` to find your slowest queries.

## Transactions and concurrency

**ACID:** Atomicity (all or nothing), Consistency (constraints hold), Isolation (concurrent transactions do not corrupt each other), Durability (committed means committed).

```
BEGIN;
  UPDATE accounts SET balance_kobo = balance_kobo - 500000 WHERE id = $1 AND balance_kobo >= 500000;
  -- if 0 rows affected -> insufficient funds -> ROLLBACK
  UPDATE accounts SET balance_kobo = balance_kobo + 500000 WHERE id = $2;
  INSERT INTO ledger (from_id, to_id, amount_kobo, ref) VALUES ($1, $2, 500000, $3);
COMMIT;
```

**Isolation levels:** `READ COMMITTED` (Postgres default) prevents dirty reads. `REPEATABLE READ` prevents non-repeatable reads. `SERIALIZABLE` prevents everything but can fail with serialization errors that your code must retry.

**The lost-update race** — critical to understand:
```
-- WRONG: read-modify-write in application code
const s = await db.one("SELECT stock FROM products WHERE id=$1");
await db.none("UPDATE products SET stock=$1 WHERE id=$2", [s.stock - 1, id]);
-- Two concurrent requests both read 10, both write 9. You just oversold.

-- RIGHT: atomic, conditional
UPDATE products SET stock = stock - 1 WHERE id = $1 AND stock > 0 RETURNING stock;
-- Or lock explicitly:  SELECT ... FOR UPDATE
```

**Deadlocks** happen when transactions lock resources in different orders. Prevent them by always acquiring locks in a consistent order (e.g. sort account IDs before locking).

## Query layer: Drizzle, Prisma, or raw SQL

**Drizzle** — SQL-like TypeScript, thin, excellent types, no hidden queries. Recommended default in 2026. **Prisma** — great DX and migrations, heavier, can generate surprising SQL. **Raw SQL + a query builder** — maximum control; always parameterize.

```
// Drizzle: types flow from your schema
const rows = await db.select({
    id: orders.id, total: orders.totalKobo, customer: customers.fullName,
  })
  .from(orders)
  .innerJoin(customers, eq(customers.id, orders.customerId))
  .where(and(eq(orders.status, "paid"), gte(orders.placedAt, since)))
  .orderBy(desc(orders.placedAt))
  .limit(50);
```

:::trap The N+1 query problem
Fetching 50 orders then looping to fetch each customer = 51 queries. In production that turns a 20ms endpoint into 2 seconds. Fix with a `JOIN`, a single `WHERE id = ANY($1)` batch, or a dataloader. **Log your query count per request in development** — it is the fastest way to catch this. Every ORM makes this easy to do accidentally.
:::

:::drill Postgres drill
Generate 2 million rows of synthetic order data (`generate_series`). Write a dashboard query joining three tables with aggregation. Time it. Then: add the right indexes, rewrite with a CTE, examine `EXPLAIN ANALYZE` at each step, and record the improvement. Getting a query from 4,000ms to 40ms and being able to explain exactly why is a story you will tell in interviews.
:::
""",
)

page(
    id="w10-sql",
    title="W10 · Advanced SQL",
    sub="Week 10, Day 1–3",
    eyebrow="WEEK 10 · BACKEND",
    subtitle="Window functions and CTEs are the explicit 2026 benchmark for competitive data roles. This is the highest-leverage lesson in the program.",
    chips=["18 hours", "Windows · CTEs · optimization"],
    body=r"""
## Common Table Expressions — readable, composable SQL

```
WITH monthly AS (
  SELECT date_trunc('month', placed_at) AS month,
         customer_id,
         SUM(total_kobo) / 100.0 AS revenue
  FROM orders
  WHERE status IN ('paid','delivered')
  GROUP BY 1, 2
),
ranked AS (
  SELECT *, RANK() OVER (PARTITION BY month ORDER BY revenue DESC) AS rnk
  FROM monthly
)
SELECT month, customer_id, revenue
FROM ranked
WHERE rnk <= 10
ORDER BY month DESC, revenue DESC;
```

CTEs turn one unreadable 80-line query into named steps you can reason about and test individually. **Recursive CTEs** handle hierarchies:

```
WITH RECURSIVE org AS (
  SELECT id, name, manager_id, 1 AS depth FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, org.depth + 1
  FROM employees e JOIN org ON e.manager_id = org.id
)
SELECT * FROM org ORDER BY depth;
```

## Window functions — the skill that separates levels

A window function computes across a set of rows **related to the current row** without collapsing them into one row (unlike `GROUP BY`).

```
SELECT
  order_id, customer_id, placed_at, amount,

  -- ranking
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY placed_at)       AS order_seq,
  RANK()       OVER (ORDER BY amount DESC)                              AS amount_rank,
  DENSE_RANK() OVER (ORDER BY amount DESC)                              AS dense_rank,
  NTILE(4)     OVER (ORDER BY amount)                                   AS quartile,

  -- offsets: compare to previous/next row
  LAG(amount)  OVER (PARTITION BY customer_id ORDER BY placed_at)       AS prev_amount,
  LEAD(placed_at) OVER (PARTITION BY customer_id ORDER BY placed_at)    AS next_order_at,

  -- running totals and moving averages
  SUM(amount) OVER (PARTITION BY customer_id ORDER BY placed_at
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)   AS running_total,
  AVG(amount) OVER (ORDER BY placed_at
                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)           AS ma7,

  -- share of a group total
  ROUND(100.0 * amount / SUM(amount) OVER (PARTITION BY date_trunc('month', placed_at)), 2)
                                                                        AS pct_of_month,

  -- first/last within a partition
  FIRST_VALUE(amount) OVER (PARTITION BY customer_id ORDER BY placed_at) AS first_order_value
FROM orders;
```

**The five business questions window functions answer, that nothing else does cleanly:**

1. **Growth:** month-over-month change → `LAG`
2. **Ranking within groups:** top 3 products per category → `ROW_NUMBER` + filter
3. **Running/cumulative:** revenue to date, cumulative users → `SUM OVER`
4. **Smoothing:** 7-day moving average → `AVG OVER ROWS BETWEEN`
5. **Deduplication:** keep the latest record per entity → `ROW_NUMBER() = 1`

```
-- Deduplicate: keep the most recent row per customer
WITH d AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY email ORDER BY updated_at DESC) AS rn
  FROM customer_imports
)
SELECT * FROM d WHERE rn = 1;

-- Month-over-month growth
WITH m AS (SELECT date_trunc('month', placed_at) mo, SUM(total_kobo)/100.0 rev FROM orders GROUP BY 1)
SELECT mo, rev, LAG(rev) OVER (ORDER BY mo) AS prev,
       ROUND(100.0 * (rev - LAG(rev) OVER (ORDER BY mo)) / NULLIF(LAG(rev) OVER (ORDER BY mo), 0), 1) AS growth_pct
FROM m ORDER BY mo;
```

:::edge The interview question that filters everyone
"Find the second-highest salary per department." Weak candidates write subqueries with `MAX` and get stuck on ties. Strong candidates write:
`SELECT * FROM (SELECT *, DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) r FROM emp) x WHERE r = 2;`
and then **explain why `DENSE_RANK` rather than `RANK` or `ROW_NUMBER`** given how ties should be treated. That explanation is the actual answer.
:::

## Analytical patterns you will reuse constantly

```
-- 1. Cohort retention (the classic analytics deliverable)
WITH first_order AS (
  SELECT customer_id, date_trunc('month', MIN(placed_at)) AS cohort FROM orders GROUP BY 1
),
activity AS (
  SELECT o.customer_id, f.cohort,
         (EXTRACT(YEAR FROM age(date_trunc('month', o.placed_at), f.cohort)) * 12
          + EXTRACT(MONTH FROM age(date_trunc('month', o.placed_at), f.cohort)))::int AS month_n
  FROM orders o JOIN first_order f USING (customer_id)
)
SELECT cohort, month_n, COUNT(DISTINCT customer_id) AS active,
       ROUND(100.0 * COUNT(DISTINCT customer_id)
             / FIRST_VALUE(COUNT(DISTINCT customer_id)) OVER (PARTITION BY cohort ORDER BY month_n), 1) AS retention_pct
FROM activity GROUP BY cohort, month_n ORDER BY cohort, month_n;

-- 2. Date spine: never let missing days silently disappear from a chart
WITH days AS (SELECT generate_series(date '2026-01-01', date '2026-12-31', '1 day')::date AS d)
SELECT days.d, COALESCE(SUM(o.total_kobo)/100.0, 0) AS revenue
FROM days LEFT JOIN orders o ON o.placed_at::date = days.d
GROUP BY days.d ORDER BY days.d;

-- 3. Conditional aggregation (pivot without a pivot)
SELECT market,
  COUNT(*) FILTER (WHERE status = 'paid')      AS paid,
  COUNT(*) FILTER (WHERE status = 'cancelled') AS cancelled,
  SUM(total_kobo) FILTER (WHERE channel = 'ussd')/100.0 AS ussd_revenue
FROM orders GROUP BY market;

-- 4. Funnel with conditional counts
SELECT
  COUNT(DISTINCT session_id)                                        AS visited,
  COUNT(DISTINCT session_id) FILTER (WHERE event = 'add_to_cart')   AS carted,
  COUNT(DISTINCT session_id) FILTER (WHERE event = 'checkout')      AS checked_out,
  COUNT(DISTINCT session_id) FILTER (WHERE event = 'purchase')      AS purchased
FROM events WHERE occurred_at >= now() - interval '30 days';

-- 5. Gaps and islands: find consecutive-day streaks
WITH d AS (SELECT DISTINCT user_id, activity_date FROM logins),
     g AS (SELECT *, activity_date - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY activity_date))::int AS grp FROM d)
SELECT user_id, MIN(activity_date) AS streak_start, COUNT(*) AS streak_len
FROM g GROUP BY user_id, grp HAVING COUNT(*) >= 3;
```

## Making slow queries fast

1. `EXPLAIN (ANALYZE, BUFFERS)` — always start with the actual plan, never a guess.
2. Look for: Seq Scan on big tables, Nested Loop with huge row counts, Sort spilling to disk, and estimate-vs-actual mismatches.
3. Fix in this order: **add the right index** → **rewrite the query** (avoid functions on indexed columns, avoid `SELECT *`, avoid `OR` on different columns — use `UNION ALL`) → **restructure the data** (materialized view, summary table, partitioning).
4. `CREATE MATERIALIZED VIEW` for expensive dashboard aggregates; refresh on a schedule with `REFRESH MATERIALIZED VIEW CONCURRENTLY`.
5. Partition tables that exceed ~50–100M rows by time range.

:::drill The 50-query gauntlet
Load a large public dataset (NYC taxi, Brazilian e-commerce/Olist, or Nigerian trade statistics). Write 50 queries progressing from simple filters to cohort retention, funnels, gaps-and-islands, and a full executive summary in one query. Optimize the five slowest and document the before/after with plans. Publish it as a repo: **an annotated SQL portfolio is one of the most persuasive artifacts for a data role**, and almost nobody has one.
:::
""",
)

page(
    id="w11-auth",
    title="W11 · Auth, Security & Multi-Tenancy",
    sub="Week 11, Day 1–3",
    eyebrow="WEEK 11 · BACKEND",
    subtitle="The area where mistakes are catastrophic and where most self-taught developers are weakest.",
    chips=["18 hours", "OWASP · sessions · RBAC"],
    body=r"""
## Authentication vs authorization

**Authentication** = who are you. **Authorization** = what may you do. They are separate systems and conflating them causes breaches.

### Password handling (if you build it yourself)

```
import argon2 from "argon2";
const hash = await argon2.hash(password, { type: argon2.argon2id });
const ok   = await argon2.verify(hash, submitted);
```

- **Argon2id** (or bcrypt/scrypt). Never MD5, SHA-256, or anything fast — fast hashes are the enemy here.
- Never store, log, or email plaintext passwords. Never send a password in a reset email; send a single-use, expiring token.
- Enforce minimum length (12+) over composition rules, and check against known-breached password lists.
- Rate limit login attempts **per account and per IP**; add exponential backoff and CAPTCHA after repeated failures.
- **Always return the same message** for "wrong password" and "no such user" — otherwise you have an account-enumeration oracle. Same for signup and password reset flows.

### Sessions vs JWTs — choose deliberately

| | Sessions (opaque ID + server store) | JWT (signed, self-contained) |
|---|---|---|
| Revoke immediately | Yes | No (that is the whole problem) |
| Scales across services | Needs shared store (Redis) | Yes, stateless |
| Payload visible to client | No | Yes — base64, not encrypted |
| Best for | Most web apps | Service-to-service, short-lived access tokens |

**The practical pattern:** short-lived access token (10–15 min) + long-lived refresh token stored in an `HttpOnly; Secure; SameSite=Lax` cookie, with refresh-token rotation and reuse detection (if an old refresh token is presented, revoke the entire family — that indicates theft).

:::trap Never store tokens in localStorage
Any XSS on your site can read `localStorage` and exfiltrate every token. Use `HttpOnly` cookies so JavaScript cannot touch them, and pair with `SameSite` plus CSRF tokens for state-changing requests. "Where do you store the JWT and why?" is a standard senior interview question — and the answer "localStorage" ends the conversation.
:::

### Use a provider unless you have a reason not to

Auth.js (NextAuth), Clerk, Supabase Auth, WorkOS, or Keycloak. They give you OAuth, magic links, MFA, and session management correctly. **Build it from scratch once as a learning exercise, then use a provider in real products.** Knowing what is under the hood is why you can debug it.

## Authorization: RBAC and multi-tenancy

```
// Central policy, not scattered if-statements
type Action = "read" | "create" | "update" | "delete" | "export";
const policy: Record<Role, Partial<Record<Resource, Action[]>>> = {
  owner:   { invoice: ["read","create","update","delete","export"], user: ["read","create","update","delete"] },
  analyst: { invoice: ["read","export"], user: ["read"] },
  viewer:  { invoice: ["read"] },
};
export function can(user: User, action: Action, resource: Resource, record?: { orgId: string }) {
  if (record && record.orgId !== user.orgId) return false;   // tenant isolation FIRST
  return policy[user.role]?.[resource]?.includes(action) ?? false;
}
```

:::trap IDOR — the most common real-world vulnerability
`GET /api/invoices/9f2c...` and your handler fetches by ID and returns it. An authenticated user from another company changes the ID and reads your customer's invoice. **Every single query must be scoped to the tenant**: `WHERE id = $1 AND org_id = $2`. Do not rely on unguessable IDs. Better: enforce it structurally with Postgres Row-Level Security so a missing filter cannot leak data.
:::

```
-- Row-Level Security: defense that survives application bugs
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON invoices
  USING (org_id = current_setting('app.current_org', true)::uuid);
-- then per request:  SET LOCAL app.current_org = '...';
```

## The OWASP essentials, with fixes

| Risk | Fix |
|---|---|
| **Broken access control** | Check authorization on every request server-side; RLS; deny by default |
| **Injection (SQL/command)** | Parameterized queries always. Never string-concatenate user input into SQL |
| **XSS** | Escape output (React does by default); avoid `dangerouslySetInnerHTML`; sanitize with DOMPurify; set a Content-Security-Policy |
| **CSRF** | `SameSite` cookies + CSRF tokens on state-changing requests |
| **SSRF** | Validate and allowlist any URL your server fetches; block internal IP ranges |
| **Insecure deserialization / mass assignment** | Never spread request bodies into DB writes; use an explicit allowlist of fields |
| **Secrets exposure** | Env vars + a secret manager; scan repos with gitleaks; rotate on any exposure |
| **Vulnerable dependencies** | `npm audit`, Dependabot/Renovate, lockfiles, minimal dependencies |
| **Security misconfiguration** | Security headers, disable directory listing, no debug mode in prod |
| **Insufficient logging** | Log auth events, permission denials, and admin actions with request IDs |

```
// Security headers, one middleware
app.use("*", secureHeaders({
  contentSecurityPolicy: { defaultSrc: ["'self'"], scriptSrc: ["'self'"], imgSrc: ["'self'", "data:", "https:"] },
  strictTransportSecurity: "max-age=63072000; includeSubDomains; preload",
  xFrameOptions: "DENY",
  referrerPolicy: "strict-origin-when-cross-origin",
}));
```

## File uploads (a frequently botched surface)

Validate type by **magic bytes**, not the extension or client-supplied MIME. Enforce a size limit. Store outside the web root — object storage (S3/R2) with **presigned URLs** so files never pass through your server. Generate new filenames; never trust user-supplied names. Serve user content from a separate domain to contain XSS. Scan for malware if users share files with each other.

:::drill Security drill — break your own app
Take your Week 8 capstone and attack it: (1) try IDOR on every endpoint by changing IDs, (2) submit `'; DROP TABLE--` and `<img src=x onerror=alert(1)>` in every field, (3) call your Server Actions directly with curl while logged out, (4) upload a `.php` file renamed to `.jpg`, (5) hammer login 1,000 times, (6) inspect the JS bundle for leaked keys. Fix everything you find and write it up. Security write-ups get attention because so few juniors can produce them.
:::
""",
)

page(
    id="w11-payments",
    title="W11 · Payments, Webhooks & Money Logic",
    sub="Week 11, Day 4–6",
    eyebrow="WEEK 11 · BACKEND",
    subtitle="Payment integration is the single most commercially valuable backend skill, and correctness here is unforgiving.",
    chips=["18 hours", "Paystack/Stripe · idempotency · ledgers"],
    body=r"""
## Why this is worth an entire block

Any developer who can *correctly* integrate payments — with idempotency, webhook verification, reconciliation, and a proper ledger — is immediately employable and can charge premium freelance rates. Most cannot. This lesson uses Paystack/Flutterwave (dominant in Nigeria) and Stripe (global); the concepts are identical.

## The correct payment flow

```
1. Client requests to pay          -> your server creates a payment intent/transaction
2. Your server stores it as        -> status: 'pending', with an idempotency key
3. Client is redirected / uses SDK -> user pays on the provider's page (you never touch card data)
4. Provider redirects back         -> DO NOT trust this for fulfilment. It is a UX signal only.
5. Provider sends a webhook        -> verify signature -> this is the source of truth
6. Your server verifies via API    -> re-fetch the transaction; confirm amount AND currency
7. Fulfil once, idempotently       -> mark paid, grant access, ship goods, write ledger entries
```

:::trap Three payment bugs that cost real money
1. **Trusting the redirect.** A user can hit your success URL manually. Only a verified webhook or a server-side verification call may trigger fulfilment.
2. **Not verifying the amount.** Always confirm the charged amount and currency match your order. Never trust a client-supplied amount at any point — compute totals server-side from your own price data.
3. **Non-idempotent webhook handling.** Providers retry webhooks, often several times, sometimes out of order. Without deduplication you will ship goods twice or double-credit a wallet.
:::

```
// Webhook handler done properly
app.post("/webhooks/paystack", async (c) => {
  const raw = await c.req.text();                       // RAW body - parsing first breaks the signature
  const sig = c.req.header("x-paystack-signature");
  const expected = crypto.createHmac("sha512", process.env.PAYSTACK_SECRET!).update(raw).digest("hex");
  if (!sig || !crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) {
    return c.json({ error: "invalid signature" }, 401);  // timing-safe compare, not ===
  }

  const event = JSON.parse(raw);

  // Idempotency: unique index on provider_event_id makes replay a no-op
  const inserted = await db.insert(webhookEvents)
    .values({ providerEventId: event.id, type: event.event, payload: event })
    .onConflictDoNothing().returning();
  if (inserted.length === 0) return c.json({ ok: true });   // already processed

  // Return 200 fast; do the work in a queue. Providers time out and retry.
  await queue.add("process-payment-event", { eventId: event.id });
  return c.json({ ok: true });
});
```

## The double-entry ledger

For anything holding balances — wallets, escrow, marketplace payouts, savings — do not keep a mutable `balance` column as the source of truth. Use an **append-only double-entry ledger** where every transaction writes balanced debit and credit entries.

```
CREATE TABLE ledger_entries (
  id            bigserial PRIMARY KEY,
  transaction_id uuid NOT NULL,             -- groups the two+ sides
  account_id    uuid NOT NULL REFERENCES accounts(id),
  direction     char(2) NOT NULL CHECK (direction IN ('DR','CR')),
  amount_kobo   bigint NOT NULL CHECK (amount_kobo > 0),
  currency      char(3) NOT NULL,
  occurred_at   timestamptz NOT NULL DEFAULT now(),
  description   text NOT NULL,
  metadata      jsonb NOT NULL DEFAULT '{}'
);
-- Invariant that must ALWAYS hold, and that you should test in CI:
-- SUM(CASE WHEN direction='DR' THEN amount ELSE -amount END) = 0  per transaction_id
```

Balance = a sum over entries (materialized or cached, but always derivable). Benefits: complete audit trail, provable correctness, no lost updates, and you can reconstruct any historical balance. This is how banks work and it is how your fintech project should work.

## Reconciliation

Every day, compare your ledger to the provider's settlement report. Flag: transactions in your system not in theirs, in theirs not in yours, and amount mismatches. Build this as a scheduled job with an alert. **Reconciliation is what separates a payment integration from a payment system**, and the ability to say you built one is a strong signal in any fintech interview.

## Other money mechanics you should be able to implement

- **Refunds and partial refunds**, and their ledger entries
- **Subscriptions:** billing cycles, proration, dunning (retrying failed charges), grace periods, cancellation at period end
- **Split payments / marketplace payouts:** platform fee, vendor balance, payout scheduling
- **Multi-currency:** store the rate used at transaction time; never re-derive historical values with today's rate
- **Chargebacks and disputes:** evidence submission, provisional reversal in the ledger

:::ship Week 11 deliverable
A working payments service: checkout initialization, webhook handling with signature verification and idempotency, a double-entry ledger with balance queries, refund support, a daily reconciliation job, an admin view of transactions, and a test suite that includes replayed webhooks, out-of-order events, and concurrent purchase attempts on limited stock. Use Paystack test mode. **This project alone can get you freelance work.**
:::
""",
)

page(
    id="w12-scale",
    title="W12 · Queues, Caching, Realtime & Files",
    sub="Week 12",
    eyebrow="WEEK 12 · BACKEND",
    subtitle="The infrastructure patterns that turn a demo into a system that survives real traffic.",
    chips=["35 hours", "Redis · BullMQ · WebSockets"],
    body=r"""
## Background jobs — the first thing to add when requests get slow

Anything slow, unreliable, or non-essential to the response belongs in a queue: sending emails and SMS, generating PDFs and reports, image processing, third-party API calls, data imports, and scheduled tasks.

```
import { Queue, Worker } from "bullmq";
const connection = { host: process.env.REDIS_HOST, port: 6379 };

export const emails = new Queue("emails", { connection });

// Producer: return to the user immediately
await emails.add("invoice", { invoiceId }, {
  attempts: 5,
  backoff: { type: "exponential", delay: 2000 },
  removeOnComplete: 1000,
  jobId: `invoice:${invoiceId}`,        // dedupe key
});

// Consumer: a separate process, scaled independently
new Worker("emails", async job => {
  const invoice = await getInvoice(job.data.invoiceId);
  await mailer.send(renderInvoice(invoice));
}, { connection, concurrency: 10 });
```

**Job design rules:** jobs must be **idempotent** (they will be retried), **small** (pass an ID, not a payload — the record may change), and **observable** (log start/finish/failure with the job ID). Always configure a **dead-letter queue** and actually check it. Add a scheduled job (`repeat: { pattern: "0 2 * * *" }`) for nightly work like reconciliation.

## Caching — the biggest performance lever, and the biggest footgun

Layers, from cheapest to most expensive to get wrong:
1. **CDN / edge** — static assets and cacheable pages. Nearly free performance.
2. **HTTP caching** — `Cache-Control`, `ETag`, `stale-while-revalidate`.
3. **Application cache (Redis)** — computed results, session data, rate-limit counters.
4. **Database** — materialized views, summary tables.

```
// Cache-aside, the standard pattern
async function getDashboard(orgId: string) {
  const key = `dash:${orgId}:v3`;                 // version in the key = instant invalidation
  const hit = await redis.get(key);
  if (hit) return JSON.parse(hit);
  const data = await computeDashboard(orgId);      // expensive
  await redis.set(key, JSON.stringify(data), "EX", 300);
  return data;
}
```

:::trap Cache invalidation and the stampede
Two hard problems. (1) **Stale data**: prefer short TTLs and event-based invalidation on write; put a version in the key so you can bump it on deploy. (2) **Thundering herd**: when a popular key expires, 500 requests all recompute simultaneously and take down your database. Fix with a lock (only one recomputes, others wait or serve stale) or probabilistic early expiry. Also **never cache per-user data under a shared key** — the classic bug that shows one customer another customer's dashboard.
:::

**Rate limiting** with Redis (protects you from abuse and from your own retry loops):
```
const key = `rl:${userId}:${Math.floor(Date.now() / 60000)}`;
const n = await redis.incr(key);
if (n === 1) await redis.expire(key, 60);
if (n > 100) throw new AppError("RATE_LIMITED", "Too many requests", 429);
```

## Realtime

| Technology | Direction | Use when |
|---|---|---|
| **Polling** | Client pulls | Simple, infrequent updates. Do not dismiss it — often the right answer |
| **SSE** (Server-Sent Events) | Server → client | Notifications, live dashboards, LLM token streaming. Simple, auto-reconnects |
| **WebSocket** | Bidirectional | Chat, collaborative editing, live tracking, multiplayer |
| **WebRTC** | Peer-to-peer | Audio/video calls |

```
// SSE - underrated and far simpler than WebSockets for one-way updates
app.get("/api/stream", c => {
  return streamSSE(c, async stream => {
    const unsub = bus.subscribe(c.get("user").orgId, async evt => {
      await stream.writeSSE({ event: evt.type, data: JSON.stringify(evt) });
    });
    c.req.raw.signal.addEventListener("abort", unsub);
  });
});
```

Scaling WebSockets: connections are stateful, so you need a **pub/sub backplane** (Redis) so a message published on server A reaches clients connected to server B. Also handle: authentication on connect, heartbeats, reconnection with backoff, and message ordering/replay after reconnect.

## Files and storage

Use object storage (S3, Cloudflare R2, Supabase Storage) — never your application's filesystem, which disappears on redeploy. **Presigned uploads** are the correct pattern:

```
// 1. Client asks your server for permission
const { url, fields, key } = await s3.createPresignedPost({
  Bucket, Key: `uploads/${orgId}/${crypto.randomUUID()}.jpg`,
  Conditions: [["content-length-range", 0, 5_000_000], ["starts-with", "$Content-Type", "image/"]],
  Expires: 300,
});
// 2. Client uploads DIRECTLY to storage - your server never handles the bytes
// 3. Client notifies your server; you verify the object exists and record it
```

Then: generate thumbnails in a queue worker, serve through a CDN, use presigned GET URLs for private files, and set lifecycle rules to expire old data.

## Email, SMS and notifications

Transactional email (Resend, Postmark, SES): configure **SPF, DKIM, and DMARC** or you land in spam. Always provide a plain-text alternative and an unsubscribe link for anything non-transactional. For SMS/WhatsApp in Nigeria: Termii, Africa's Talking, or Twilio. Build a **notification preference system** early — users must be able to control channels, and regulators increasingly require it.

:::ship Week 12 deliverable
Add to your capstone: a job queue with retries and a dead-letter queue, Redis caching with measured hit rates, rate limiting, a realtime feed via SSE or WebSocket, presigned direct-to-storage uploads with thumbnailing, and transactional email. Then **load test it** with k6 or Artillery: report p50/p95/p99 latency and throughput before and after your caching layer. Numbers in a README are enormously persuasive.
:::
""",
)

page(
    id="w13-python-be",
    title="W13 · Python Backends & Data Services",
    sub="Week 13",
    eyebrow="WEEK 13 · BACKEND",
    subtitle="FastAPI, async Python, and the data-service layer where engineering meets analytics.",
    chips=["35 hours", "FastAPI · pydantic · pipelines"],
    body=r"""
## Why add Python when you already have Node

Because the highest-value work in 2026 sits where products meet data and AI, and that layer is Python. Job data consistently shows Python/FastAPI rising in importance for mid and senior full-stack roles. You will use Node for the product API and Python for data processing, ML/LLM services, and analytics pipelines — a combination that makes you useful on both sides of a company.

## FastAPI essentials

```
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Annotated

app = FastAPI(title="Analytics Service", version="1.0.0")

class ForecastRequest(BaseModel):
    sku: str = Field(min_length=3)
    horizon_days: int = Field(ge=1, le=365, default=30)
    confidence: float = Field(ge=0.5, le=0.99, default=0.95)

class ForecastPoint(BaseModel):
    day: date
    predicted: float
    lower: float
    upper: float

@app.post("/forecast", response_model=list[ForecastPoint])
async def forecast(req: ForecastRequest, db=Depends(get_db)) -> list[ForecastPoint]:
    history = await db.fetch_history(req.sku)
    if len(history) < 30:
        raise HTTPException(422, detail="Need at least 30 days of history")
    return run_forecast(history, req.horizon_days, req.confidence)
```

You get automatic validation, OpenAPI docs at `/docs`, and typed responses for free. Pydantic is Python's Zod: the validation boundary between the messy outside world and your clean internal types.

**Async Python:** `async def` + `await` work like JavaScript, with the same blocking rule — a synchronous CPU-heavy call inside an async handler blocks the loop. Use `asyncio.to_thread()` or a process pool for CPU work. Use `httpx.AsyncClient` (not `requests`) and `asyncpg`/SQLAlchemy async for the database.

## Production-grade Python practice

```
# pyproject.toml essentials
[tool.ruff]              # linter + formatter, replaces black/flake8/isort. Extremely fast.
line-length = 100
[tool.mypy]
strict = true            # yes, Python can be strictly typed. Do it.
[tool.pytest.ini_options]
addopts = "-q --cov=app --cov-report=term-missing"
```

Structure services the same way as your Node app: `routers/`, `services/`, `repositories/`, `schemas/`, `core/`. Configuration through `pydantic-settings`. Structured JSON logging with `structlog`. Tests with `pytest` + `httpx.AsyncClient`.

## Data pipelines — the ETL/ELT skill

```
import polars as pl

# Polars: faster than pandas, lazy execution, better memory behaviour on big files
lf = (
    pl.scan_csv("transactions_*.csv")                      # lazy - nothing read yet
      .filter(pl.col("status") == "completed")
      .with_columns([
          (pl.col("amount_kobo") / 100).alias("amount_ngn"),
          pl.col("created_at").str.to_datetime().alias("ts"),
      ])
      .group_by([pl.col("ts").dt.truncate("1d"), "channel"])
      .agg([
          pl.len().alias("txn_count"),
          pl.col("amount_ngn").sum().alias("revenue"),
          pl.col("amount_ngn").median().alias("median_ticket"),
          pl.col("customer_id").n_unique().alias("unique_customers"),
      ])
      .sort("ts")
)
df = lf.collect()          # the query optimizer plans the whole thing, then executes
```

**The ETL checklist for any pipeline you build:**
1. **Idempotent** — running twice produces the same result, never duplicates.
2. **Incremental** — process only new/changed data (watermark on `updated_at` or an event ID).
3. **Validated** — schema and business-rule checks at ingestion; quarantine bad rows rather than silently dropping them.
4. **Observable** — log rows in / rows out / rows rejected, plus duration. Alert on anomalies.
5. **Recoverable** — restartable from the last checkpoint; never leaves partial state.
6. **Documented lineage** — where did this number come from?

```
# DuckDB: an analytics database in a single file. Absurdly useful.
import duckdb
con = duckdb.connect("analytics.db")
con.sql('''
  CREATE OR REPLACE TABLE daily AS
  SELECT date_trunc('day', ts) d, channel, sum(amount) rev, count(*) n
  FROM read_parquet('s3://bucket/events/*.parquet')
  GROUP BY 1, 2
''')
# Query 50 GB of parquet on a laptop, with full SQL, no cluster required.
```

## Orchestration

For scheduled, dependent pipelines use **Dagster** or **Prefect** (both far friendlier than Airflow for new projects) — you get retries, dependency graphs, backfills, alerting, and lineage. Small jobs can start as cron plus a queue. Learn the concepts: DAG, task, sensor, backfill, idempotent partition.

:::edge The bridge role that pays
The engineer who can build the product API in TypeScript, the data pipeline in Python, and the SQL model that feeds the dashboard is far rarer than a specialist in any one of them — and is the person a startup CTO or a bank's innovation lab most wants to hire. Position yourself explicitly as this. In your CV headline: "Full-stack engineer (TypeScript) + analytics engineer (Python/SQL) — I build the product and the systems that measure it."
:::

:::ship Week 13 deliverable
A Python analytics service beside your Node API: FastAPI with typed endpoints, an incremental ETL job pulling from your app's Postgres into a DuckDB or Postgres analytics schema, data-quality validation with quarantine, a forecasting endpoint, scheduled orchestration, and a `/metrics` endpoint. Your Next.js frontend calls it for the analytics tab. **You now have a genuine two-language, multi-service architecture** — that is a mid-level portfolio, not a junior one.
:::
""",
)
