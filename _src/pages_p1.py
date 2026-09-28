# -*- coding: utf-8 -*-
PAGES = []
G = "01 · Foundations (Wk 1–4)"

def page(**kw):
    kw.setdefault("group", G)
    PAGES.append(kw)

page(
    id="w1-machine",
    title="W1 · The Machine & The Terminal",
    sub="Day 1–2",
    eyebrow="WEEK 1 · FOUNDATIONS",
    subtitle="Before you write code, you need to command the computer the way professionals do.",
    chips=["12 hours", "Bash · Git · filesystem"],
    body=r"""
## Why this comes first

Every deployment, every server, every CI pipeline, every data job runs on Linux and is driven by a shell. GUI-only developers hit a hard ceiling around month six. You are clearing that ceiling in week one.

## Mental model: what a computer actually does

A program is bytes in memory that the CPU executes. The **operating system** manages three scarce things: CPU time (via processes and threads), memory (via virtual address spaces), and I/O (files, network, devices). Everything you will build sits on this. Key ideas to hold:

- **Process:** a running program with its own memory. Has a PID, a parent, an exit code (0 = success).
- **File descriptor:** processes talk to the world through numbered channels. 0 = stdin, 1 = stdout, 2 = stderr. Redirection and pipes are just rewiring these numbers.
- **Filesystem:** a tree from `/`. Paths are absolute (`/home/user/x`) or relative (`./x`, `../x`).
- **Environment variables:** key-value config inherited by child processes. This is how secrets reach your app in production.
- **Permissions:** `rwx` for user/group/other. `chmod 755` = owner can do everything, others can read+execute.

## The 40 commands that cover 95% of the work

```
# navigate
pwd  ls -la  cd  tree -L 2
# read
cat  less  head -n 20  tail -f app.log  wc -l
# manipulate
mkdir -p a/b/c   cp -r src dst   mv a b   rm -rf dir   touch f
# find
find . -name "*.ts" -not -path "*/node_modules/*"
grep -rn "TODO" src/            # recursive, line numbers
rg "useState" --type ts         # ripgrep: faster, learn it
# pipes and streams
cat access.log | grep 500 | awk '{print $7}' | sort | uniq -c | sort -rn | head
# processes
ps aux | grep node    kill -9 <pid>    lsof -i :3000    htop
# disk and network
df -h    du -sh *    curl -i https://api.github.com    ping    dig
# permissions and env
chmod +x script.sh   export API_KEY=abc   echo $PATH   which node
# archives and transfer
tar -czf out.tar.gz dir/   unzip f.zip   scp file user@host:/path
```

:::drill Terminal drill — the log forensics exercise
Download any web server access log (or generate one). Using only shell commands, answer: (1) the top 10 IP addresses by request count, (2) how many 5xx errors occurred, (3) which URL path produced the most errors, (4) the busiest hour of the day. This one exercise teaches pipes, `awk`, `sort`, `uniq`, and `grep` better than any tutorial. Write your commands into `forge-notes/week-01/log-forensics.md`.
:::

## Git: the mental model that prevents panic

Git is a **content-addressed database of snapshots**, not a diff tool. Three areas:

```
working directory  →  staging area (index)  →  repository (commits)
     (edit)              git add                  git commit
```

A **commit** is a snapshot + parent pointer + message. A **branch** is just a movable label pointing at a commit. `HEAD` is a pointer to your current branch. Once you see it as a graph of snapshots with labels, every command makes sense.

```
git status                      # read this constantly
git add -p                      # stage hunk by hunk - forces you to review your own diff
git commit -m "feat: add rate limiter"
git log --oneline --graph --all
git switch -c feature/auth      # modern replacement for checkout -b
git diff main...HEAD            # what my branch adds
git rebase -i main              # clean up commits before sharing
git restore --staged file       # unstage
git reset --hard HEAD~1         # DANGER: discard last commit + changes
git reflog                      # your undo history - this has saved careers
git stash / git stash pop
```

**Commit message convention** (Conventional Commits — used by most professional teams):
`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:` then a short imperative summary.

:::trap Three git mistakes juniors make
1. **Committing secrets.** Add `.env` to `.gitignore` before your first commit. Once pushed, a secret is compromised forever — rotate it, do not just delete it.
2. **Giant commits.** "Updated stuff" with 40 files. Commit one logical change at a time; use `git add -p`.
3. **Fear of `reflog`.** You almost never lose work in git. Before you panic, run `git reflog` and find the commit you were on.
:::

## The pull-request workflow (how teams actually work)

1. `git switch -c feat/thing` from an up-to-date `main`
2. Small commits as you work
3. `git push -u origin feat/thing`
4. Open a PR with: what changed, why, how you tested, screenshots if UI
5. Address review comments with new commits
6. Squash-merge into `main`; delete the branch

Practice this **solo** from week 1. Never commit directly to `main` again, even in your own repos. When you join a team, you will already be fluent.

@@ Day 1 | Install everything (if Week 0 incomplete). Terminal navigation, file ops, pipes. Do the log forensics drill.
@@ Day 2 | Git deep dive. Create 3 repos, branch, merge, deliberately create a merge conflict and resolve it. Open your first PR to yourself.

:::ship Deliverable
A repo `shell-toolkit` containing 5 bash scripts you wrote: a project scaffolder, a backup script, a log analyzer, a "find big files" script, and a git helper. Each with a `--help` flag and comments. Plus a README explaining pipes to a beginner.
:::
""",
)

page(
    id="w1-web",
    title="W1 · How the Web Actually Works",
    sub="Day 3",
    eyebrow="WEEK 1 · FOUNDATIONS",
    subtitle="The single most under-taught topic in bootcamps, and the one senior interviewers probe first.",
    chips=["6 hours", "DNS · TCP · TLS · HTTP"],
    body=r"""
## The interview question you will be able to answer

*"You type `flutterwave.com` into a browser and press Enter. Walk me through everything that happens."*

Most bootcamp graduates say "it sends a request to the server." Here is the answer that gets you hired.

### 1. Name resolution (DNS)
The browser checks its own cache, then the OS cache, then asks a **resolver** (your ISP's or 1.1.1.1). The resolver walks the hierarchy: root servers → `.com` TLD servers → the domain's authoritative nameservers → returns an **A record** (IPv4) or **AAAA** (IPv6). Results are cached according to **TTL**. Record types you must know: `A`, `AAAA`, `CNAME` (alias), `MX` (mail), `TXT` (verification/SPF), `NS`.

### 2. Transport (TCP)
A three-way handshake: `SYN → SYN-ACK → ACK`. Now there is a reliable, ordered byte stream. TCP handles retransmission and congestion control. One round trip is spent before any data flows — which is why latency matters more than bandwidth for most web performance.

### 3. Security (TLS)
Certificate exchange, the server proves it owns the domain via a certificate signed by a trusted CA, keys are agreed, and everything after is encrypted. TLS 1.3 does this in one round trip. **HTTPS is not optional** — browsers block many APIs (geolocation, service workers, camera) on plain HTTP.

### 4. The HTTP request
```
GET /dashboard HTTP/1.1
Host: flutterwave.com
User-Agent: Mozilla/5.0 ...
Accept: text/html
Cookie: session=abc123
```
The server responds with a **status line**, **headers**, and a **body**.

### 5. The browser renders
HTML is parsed into the **DOM**; CSS into the **CSSOM**; together they form the render tree → **layout** (geometry) → **paint** (pixels) → **composite** (layers to screen). JavaScript can block parsing, which is why `defer`/`async` on script tags matters. Every image, stylesheet, and font triggers more requests.

## HTTP: the vocabulary of the whole industry

**Methods and their contracts:**

| Method | Purpose | Safe? | Idempotent? |
|---|---|---|---|
| GET | Read a resource | Yes | Yes |
| POST | Create / trigger action | No | No |
| PUT | Replace a resource wholesale | No | Yes |
| PATCH | Partial update | No | No (usually) |
| DELETE | Remove a resource | No | Yes |

*Idempotent* means calling it 5 times has the same effect as once. This matters enormously for retries and payment systems — you will use it in Week 12.

**Status codes worth memorizing:**
- `200` OK · `201` Created · `204` No Content
- `301` Moved Permanently (cached forever — be careful) · `302` Found · `304` Not Modified
- `400` Bad Request · `401` Unauthenticated · `403` Authenticated but not allowed · `404` Not Found · `409` Conflict · `422` Unprocessable · `429` Too Many Requests
- `500` Server Error · `502` Bad Gateway · `503` Unavailable · `504` Gateway Timeout

:::edge 401 vs 403 — the classic filter question
`401` means "I do not know who you are" (missing/invalid credentials). `403` means "I know who you are and you still cannot do this" (insufficient permission). Getting this right in an interview signals you have actually built auth.
:::

**Headers that carry real weight:** `Content-Type`, `Authorization`, `Cache-Control`, `ETag`, `Set-Cookie`, `Access-Control-Allow-Origin`, `X-Forwarded-For`, `Retry-After`.

## CORS, explained properly

The browser's **same-origin policy** blocks JavaScript on `a.com` from reading responses from `b.com`. An origin = scheme + host + port. CORS is the server's way of saying "this other origin is allowed." For non-simple requests the browser sends a **preflight** `OPTIONS` request first.

```
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET,POST,PATCH,DELETE
Access-Control-Allow-Headers: Content-Type,Authorization
```

:::trap The CORS misunderstanding
CORS is enforced **by the browser**, not by the server, and it protects *users*, not your API. A `curl` request or another server ignores CORS entirely. So CORS is never a security control for your data — authentication and authorization are. Fixing CORS by setting `*` with credentials is both broken and a bad habit.
:::

## Cookies, sessions, and tokens

- **Cookie:** small key-value sent automatically with every request to its domain. Flags that matter: `HttpOnly` (JS cannot read it — blocks XSS theft), `Secure` (HTTPS only), `SameSite=Lax|Strict|None` (CSRF defense), `Max-Age`.
- **Session:** server stores state, cookie holds an opaque ID. Easy to revoke, needs shared storage across servers.
- **JWT:** signed token containing claims, stored client-side. Stateless and scalable but **hard to revoke** — keep them short-lived and pair with a refresh token.

You will implement both in Week 11.

:::drill Web forensics drill
Open DevTools → Network on three sites you use (a bank, a news site, an e-commerce store). For each, record: number of requests, total transferred bytes, time to first byte, the status codes present, whether they use HTTP/2 or HTTP/3, and three interesting response headers. Then run `dig yourbank.com` and `curl -I https://yourbank.com`. Write a 300-word comparison. You will learn more about the web here than from ten hours of video.
:::
""",
)

page(
    id="w1-html-css",
    title="W1 · HTML & CSS That Doesn't Embarrass You",
    sub="Day 4–6",
    eyebrow="WEEK 1 · FOUNDATIONS",
    subtitle="Semantic structure, modern layout, responsive design, and accessibility — the parts that separate developer-looking sites from professional ones.",
    chips=["18 hours", "Flexbox · Grid · a11y · design"],
    body=r"""
## HTML is an accessibility and semantics API, not decoration

Every element you choose is a promise to screen readers, search engines, and browsers about *meaning*. A `<div onclick>` is invisible to a keyboard user; a `<button>` is focusable, announceable, and keyboard-activated for free.

```
<article>
  <header>
    <h1>Quarterly revenue report</h1>
    <p><time datetime="2026-08-11">11 August 2026</time></p>
  </header>
  <nav aria-label="Sections"> ... </nav>
  <section aria-labelledby="rev">
    <h2 id="rev">Revenue</h2>
    <figure>
      <img src="chart.png" alt="Revenue rose 23% from Q1 to Q2, driven by mobile" />
      <figcaption>Q2 2026 revenue by channel</figcaption>
    </figure>
  </section>
  <footer>...</footer>
</article>
```

**Rules that matter:**
- One `<h1>` per page; never skip heading levels (they are the document outline a blind user navigates by).
- `alt` text describes *the information the image conveys*, not the image. Decorative image? `alt=""`.
- Forms: every input has a `<label for>`. Use `<fieldset>`/`<legend>` for groups. Use correct `type` (`email`, `tel`, `number`, `date`) — it changes the mobile keyboard.
- Use `<button type="button">` inside forms unless you want submission.

## CSS: the four things that actually cause confusion

### 1. The box model
`content → padding → border → margin`. Always set `box-sizing: border-box` globally so `width` means what you think it means.

### 2. The cascade and specificity
Specificity: inline (1000) > id (100) > class/attribute/pseudo-class (10) > element (1). `!important` overrides everything and is a sign you lost control. Modern escape hatches: `:where()` (zero specificity) and `@layer` for ordering.

### 3. Layout: Flexbox for one dimension, Grid for two

```
/* Flexbox: a row of items that wraps */
.toolbar { display: flex; gap: 12px; align-items: center; justify-content: space-between; flex-wrap: wrap; }

/* Grid: a real 2D layout, responsive with no media queries */
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }

/* App shell */
.app { display: grid; grid-template-areas: "side head" "side main"; grid-template-columns: 260px 1fr; grid-template-rows: 60px 1fr; min-height: 100dvh; }
.app > nav { grid-area: side } .app > header { grid-area: head } .app > main { grid-area: main }
```

### 4. Stacking and positioning
`position: relative | absolute | fixed | sticky`. `z-index` only works on positioned elements and is scoped to a **stacking context** — which `transform`, `opacity < 1`, and `filter` silently create. This is the source of the classic "my z-index: 9999 does not work" bug.

## Modern CSS you should use in 2026

```
:root {
  --space: 8px;
  --brand: oklch(72% 0.15 160);       /* perceptually uniform color */
  --radius: 12px;
}
.card {
  padding: calc(var(--space) * 2);
  border-radius: var(--radius);
  container-type: inline-size;         /* container queries */
}
@container (min-width: 400px) { .card { display: grid; grid-template-columns: 100px 1fr } }

/* fluid typography, no breakpoints */
h1 { font-size: clamp(1.75rem, 1rem + 3vw, 3rem); }

/* respect user preferences */
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important } }
@media (prefers-color-scheme: dark) { :root { --bg: #0b0f14 } }

/* nesting is now native */
.nav { & a { color: var(--brand); &:hover { text-decoration: underline } } }
```

**Responsive strategy:** mobile-first. Write the small-screen layout as the default, then add `@media (min-width: 48rem)` for larger. Use `dvh` not `vh` on mobile (address bar). Test at 320px width — if it works there, it works everywhere.

## Design competence in 90 minutes

Developers who can make things look decent get hired faster. Five rules that do most of the work:

1. **Spacing scale.** Pick 4/8/12/16/24/32/48/64 and never use arbitrary values. Inconsistent spacing is the #1 giveaway of amateur work.
2. **Two fonts maximum.** One for headings, one for body. Inter, Geist, or system fonts are safe.
3. **Type scale and line length.** Body text 16–18px, line-height 1.5–1.7, max 65–75 characters per line.
4. **Restrained color.** One brand color, one accent, a neutral gray ramp. Use color to mean something (success/warning/danger), not to decorate.
5. **Contrast.** Text must hit WCAG AA: 4.5:1 for body, 3:1 for large text. Check it — this is a legal requirement in many markets.

:::edge Accessibility is a hiring differentiator
Most junior candidates cannot discuss a11y at all. Learn these five and you will stand out: (1) keyboard navigability — tab through your whole app, can you reach and activate everything? (2) visible focus states — never `outline: none` without a replacement, (3) semantic landmarks, (4) `aria-live` regions for dynamic updates, (5) form errors linked to inputs with `aria-describedby`. Run Lighthouse and axe DevTools on every project. Public-sector and enterprise clients often *require* WCAG compliance, so this skill is directly billable.
:::

@@ Day 4 | Semantic HTML, forms, accessibility fundamentals. Build a complex multi-step form, keyboard-only.
@@ Day 5 | CSS layout: rebuild three real product pages from screenshots using Flexbox + Grid. No frameworks.
@@ Day 6 | Responsive + design polish + Lighthouse. Get a 100 accessibility score.

:::ship Week 1 project — "Sector Landing Page"
Build and deploy a one-page site for a real Nigerian SME (a clinic, a logistics firm, a school, a farm co-op). Requirements: semantic HTML, responsive from 320px to 2560px, dark mode, Lighthouse ≥ 95 on Performance/Accessibility/Best Practices/SEO, no CSS framework, deployed to Vercel with a custom domain path. Write a 400-word post on what "semantic HTML" means and why it is not just style.
:::
""",
)

page(
    id="w2-js",
    title="W2 · JavaScript to Real Depth",
    sub="Day 1–4",
    eyebrow="WEEK 2 · FOUNDATIONS",
    subtitle="Not syntax tour. The runtime model, async, closures, and the patterns you will use every day for the next decade.",
    chips=["24 hours", "Event loop · closures · async"],
    body=r"""
## Part 1 — The language core

```
// Declarations: use const by default, let when reassigning, never var.
const rate = 0.075;
let attempts = 0;

// Primitives: string number boolean null undefined symbol bigint
// Everything else is an object (arrays, functions, dates, maps...)

// Equality: always ===  (== does type coercion with insane rules)
0 == "";        // true   <- chaos
0 === "";       // false  <- use this

// Truthiness: falsy values are  false 0 -0 0n "" null undefined NaN
// Everything else is truthy - including [] and {}

// Nullish coalescing vs OR - a real bug source
const limit1 = input || 10;    // 0 becomes 10  (wrong for numbers!)
const limit2 = input ?? 10;    // only null/undefined become 10  (correct)

// Optional chaining
const city = user?.address?.city ?? "unknown";

// Destructuring + defaults + rest
const { name, role = "member", ...rest } = user;
const [first, ...others] = list;

// Spread: shallow copies
const updated = { ...user, role: "admin" };
```

:::trap Shallow vs deep copy
`{...obj}` copies only the top level. Nested objects are still shared references — mutate one and you mutate both. For real copies use `structuredClone(obj)`. This bug appears constantly in React state.
:::

## Part 2 — Functions, closures, and `this`

A **closure** is a function that remembers the variables from where it was *defined*, not where it is called. This is the mechanism behind hooks, private state, memoization, and most middleware.

```
function makeRateLimiter(maxPerMinute) {
  const hits = [];                                  // captured by closure
  return function allow() {
    const now = Date.now();
    while (hits.length && now - hits[0] > 60_000) hits.shift();
    if (hits.length >= maxPerMinute) return false;
    hits.push(now);
    return true;
  };
}
const allow = makeRateLimiter(5);
```

`this` is determined by **how a function is called**, not where it is defined — except in arrow functions, which capture `this` lexically. Rule of thumb: use arrow functions for callbacks, regular functions for object methods and constructors.

## Part 3 — Arrays: the functional toolkit you will use daily

```
const orders = [
  { id: 1, customer: "Ada",  amount: 45000, status: "paid",    channel: "web" },
  { id: 2, customer: "Bola", amount: 12000, status: "pending", channel: "ussd" },
  { id: 3, customer: "Ada",  amount: 89000, status: "paid",    channel: "web" },
];

const paid      = orders.filter(o => o.status === "paid");
const totals    = orders.map(o => o.amount);
const revenue   = paid.reduce((sum, o) => sum + o.amount, 0);
const anyUssd   = orders.some(o => o.channel === "ussd");
const allPaid   = orders.every(o => o.status === "paid");
const big       = orders.find(o => o.amount > 50_000);

// group-by with reduce - the single most useful data pattern in JS
const byCustomer = orders.reduce((acc, o) => {
  (acc[o.customer] ??= []).push(o);
  return acc;
}, {});

// modern built-in (2024+): does the same thing
const grouped = Object.groupBy(orders, o => o.customer);

// sort DOES mutate - copy first
const sorted = [...orders].sort((a, b) => b.amount - a.amount);
```

## Part 4 — The event loop (the concept that unlocks async)

JavaScript is **single-threaded** with an event loop. The call stack runs synchronous code. Async work (timers, network, file I/O) is handed to the host (browser/Node), which pushes callbacks into queues when done. The loop takes from the **microtask queue** (promises) until empty, *then* one **macrotask** (timers, I/O), then repeats.

```
console.log("1");
setTimeout(() => console.log("2"), 0);       // macrotask
Promise.resolve().then(() => console.log("3")); // microtask
console.log("4");
// Output: 1 4 3 2
```

If you can explain that output, you understand more than most candidates. **Blocking the loop is the cardinal sin** — a heavy `for` loop or synchronous file read freezes everything, including other users' requests on your server.

## Part 5 — Async patterns done right

```
// Sequential when there IS a dependency
const user  = await getUser(id);
const orders = await getOrders(user.id);

// Parallel when there is NOT - this is a huge, common performance win
const [profile, settings, notifications] = await Promise.all([
  getProfile(id), getSettings(id), getNotifications(id),
]);

// Partial failure tolerated
const results = await Promise.allSettled(tasks);
const ok = results.filter(r => r.status === "fulfilled").map(r => r.value);

// Timeouts and cancellation - the professional touch
const ctrl = new AbortController();
const t = setTimeout(() => ctrl.abort(), 5000);
try {
  const res = await fetch(url, { signal: ctrl.signal });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
} catch (err) {
  if (err.name === "AbortError") throw new Error("Request timed out");
  throw err;
} finally {
  clearTimeout(t);
}

// Retry with exponential backoff + jitter - you will reuse this forever
async function retry(fn, { attempts = 4, base = 300 } = {}) {
  let lastErr;
  for (let i = 0; i < attempts; i++) {
    try { return await fn(); }
    catch (e) {
      lastErr = e;
      const wait = base * 2 ** i + Math.random() * 100;
      await new Promise(r => setTimeout(r, wait));
    }
  }
  throw lastErr;
}
```

:::trap Three async traps
1. **`forEach` with `async`** does not await. Use `for...of` for sequential, `Promise.all(map(...))` for parallel.
2. **Unhandled rejections** crash Node processes. Every `await` belongs in a `try/catch` or has a `.catch()`.
3. **`await` inside a loop** when calls are independent turns 100ms into 10 seconds. Look for this in every code review.
:::

## Part 6 — Modules, errors, and the browser APIs

```
// ES modules
export function calc() {}         // named
export default class Api {}       // default
import Api, { calc } from "./api.js";
const heavy = await import("./chart.js");   // dynamic, code-splitting

// Custom errors carry context
class ValidationError extends Error {
  constructor(field, message) { super(message); this.name = "ValidationError"; this.field = field; }
}

// DOM essentials
document.querySelector("#app");
el.addEventListener("click", handler, { once: true });
el.closest("[data-row]");                   // event delegation
new IntersectionObserver(cb).observe(el);   // lazy loading, infinite scroll
localStorage.setItem("k", JSON.stringify(v));
```

@@ Day 1 | Core language, types, functions, closures. 30 small exercises.
@@ Day 2 | Arrays, objects, data transformation. Build a pure-JS data pipeline over a CSV.
@@ Day 3 | Event loop, promises, async/await, fetch, error handling, retries.
@@ Day 4 | DOM, events, storage, and a no-framework interactive app.

:::ship Week 2 project — "Naira Expense Tracker (vanilla JS)"
No frameworks. Features: add/edit/delete transactions, categories, monthly summary, chart drawn with Canvas or SVG, filter and search, data persisted to `localStorage`, CSV export, offline-capable. Constraints: all state in one object with pure update functions (you are hand-building what React does — this makes React trivial next week), zero libraries, keyboard accessible, deployed. Write up "What the event loop is, in 300 words."
:::
""",
)

page(
    id="w2-ts",
    title="W2 · TypeScript, Properly",
    sub="Day 5–6",
    eyebrow="WEEK 2 · FOUNDATIONS",
    subtitle="TypeScript is the industry default in 2026. Learn it as a design tool, not as annotations you sprinkle on afterward.",
    chips=["12 hours", "Types as documentation"],
    body=r"""
## Why it dominates

TypeScript adoption exceeds 80% for new professional projects. It catches a large class of bugs before runtime, makes refactoring safe, and — most importantly — turns your editor into a live specification of your system. Job postings now list "TypeScript" more often than "JavaScript."

## Configuration first

```
// tsconfig.json - the strict baseline you should always start from
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true
  }
}
```

`strict: true` is non-negotiable. `noUncheckedIndexedAccess` is the one most people miss: it makes `arr[0]` typed as `T | undefined`, which is *the truth* and prevents a whole family of crashes.

## The type system in one page

```
// Primitives and literals
let id: string;
type Status = "draft" | "active" | "archived";   // union of literals - use these constantly

// Objects: interface for shapes you may extend, type for everything else
interface User { id: string; email: string; role: Role; createdAt: Date }
type Role = "admin" | "analyst" | "viewer";

// Optional, readonly, index signatures
interface Config { readonly apiUrl: string; timeout?: number; [key: string]: unknown }

// Functions
type Handler = (req: Request) => Promise<Response>;
function first<T>(xs: readonly T[]): T | undefined { return xs[0]; }

// Generics with constraints - the real power
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map(i => i[key]);
}

// Utility types you will use weekly
type PublicUser  = Omit<User, "passwordHash">;
type UserPatch   = Partial<User>;
type Required1   = Required<Config>;
type ById        = Record<string, User>;
type Args        = Parameters<typeof pluck>;
type Ret         = ReturnType<typeof pluck>;
type Awaited1    = Awaited<Promise<User>>;
```

## Discriminated unions — the pattern that eliminates entire bug classes

```
type Result<T> =
  | { ok: true;  data: T }
  | { ok: false; error: string; code: number };

function render(r: Result<User>) {
  if (r.ok) {
    console.log(r.data.email);   // TS knows data exists here
  } else {
    console.log(r.code);         // and error/code exist here
  }
}

// Exhaustiveness checking - compiler error if you add a case and forget to handle it
function label(s: Status): string {
  switch (s) {
    case "draft": return "Draft";
    case "active": return "Active";
    case "archived": return "Archived";
    default: { const _never: never = s; return _never; }
  }
}
```

This models loading/success/error UI states, API responses, and state machines. Adopt it early and your code becomes provably complete.

## `unknown` over `any`, and validating at the boundary

`any` disables type checking and silently spreads. `unknown` forces you to narrow before use. **The critical realization: TypeScript types vanish at runtime.** Data from an API, a form, or a database is *not* verified by TS. Validate it at the edge with Zod:

```
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().min(13).max(120),
  role: z.enum(["admin", "analyst", "viewer"]),
  createdAt: z.coerce.date(),
});
type User = z.infer<typeof UserSchema>;   // one source of truth: schema AND type

const parsed = UserSchema.safeParse(await res.json());
if (!parsed.success) throw new ValidationError(parsed.error.format());
const user = parsed.data;   // fully typed AND actually verified
```

:::edge The senior habit
Define your types **before** you write the implementation. Sketch the data shapes and function signatures first; the implementation often becomes obvious, and impossible states become unrepresentable. "Make illegal states unrepresentable" is the phrase — e.g. instead of `{ isLoading: boolean; data?: T; error?: E }` (which allows loading *and* error simultaneously), use a discriminated union where only valid combinations exist.
:::

:::drill TypeScript drill
Take your Week 2 vanilla-JS expense tracker and convert it to TypeScript with `strict: true` and zero `any`. Model the transaction state as a discriminated union. Validate `localStorage` reads with Zod (they are untrusted input!). Note every bug the compiler finds — there will be several, and that is the point.
:::
""",
)

page(
    id="w3-cs",
    title="W3 · Computer Science That Pays",
    sub="Week 3, Day 1–3",
    eyebrow="WEEK 3 · FOUNDATIONS",
    subtitle="Only the CS that shows up in real work and real interviews: complexity, the six data structures that matter, and the patterns behind 80% of coding challenges.",
    chips=["18 hours", "Big-O · structures · patterns"],
    body=r"""
## Why a self-taught developer needs this

Two reasons, both practical. First, **interviews**: most companies still screen with algorithmic problems. Second, and more important, **judgment**: knowing that a hash lookup is O(1) and a nested loop over 100k rows is 10 billion operations is what makes you choose the right approach instinctively. Without it you write code that works on 100 rows and dies on 100,000.

## Big-O in the way that actually matters

You are counting how work grows as input grows.

| Complexity | Name | 1k items | 1M items | Typical source |
|---|---|---|---|---|
| O(1) | Constant | 1 | 1 | Hash/object lookup, array index |
| O(log n) | Logarithmic | 10 | 20 | Binary search, balanced tree, DB index |
| O(n) | Linear | 1k | 1M | Single loop, `map`, `filter` |
| O(n log n) | Linearithmic | 10k | 20M | Good sorting |
| O(n²) | Quadratic | 1M | 1 trillion | Nested loop over same data |
| O(2ⁿ) | Exponential | — | — | Naive recursion over subsets |

**The rule of thumb:** if you see a loop inside a loop over the same dataset, ask whether a hash map can remove the inner one. That single transformation — O(n²) → O(n) — is the most common optimization in real code and in interviews.

## The six structures you must own

++ Array :: Contiguous, index O(1), search O(n), insert/delete at front O(n). Default choice.
++ Hash Map :: `Map`/object/dict. Insert, lookup, delete all O(1) average. The workhorse — reach for it whenever you think "have I seen this before?"
++ Set :: Uniqueness and membership in O(1). Deduplication, "seen" tracking, intersection logic.
++ Stack / Queue :: LIFO / FIFO. Undo, DFS, parsing, BFS, task queues, rate limiters.
++ Tree :: Hierarchies, the DOM, file systems, JSON, database indexes (B-trees). Traverse with recursion or an explicit stack.
++ Graph :: Anything with relationships — social networks, road routes, dependency graphs, supply chains. Store as an adjacency map; traverse with BFS (shortest path in unweighted) or DFS.

## The eight patterns behind most problems

```
// 1. Two pointers - sorted arrays, pair sums, palindromes
function pairSum(sorted, target) {
  let l = 0, r = sorted.length - 1;
  while (l < r) {
    const s = sorted[l] + sorted[r];
    if (s === target) return [l, r];
    s < target ? l++ : r--;
  }
  return null;
}

// 2. Sliding window - "longest/max subarray of size k or with property P"
function maxSum(nums, k) {
  let sum = 0, best = -Infinity;
  for (let i = 0; i < nums.length; i++) {
    sum += nums[i];
    if (i >= k) sum -= nums[i - k];
    if (i >= k - 1) best = Math.max(best, sum);
  }
  return best;
}

// 3. Hash map for frequency / seen  - kills most O(n^2) solutions
function firstDuplicate(xs) {
  const seen = new Set();
  for (const x of xs) { if (seen.has(x)) return x; seen.add(x); }
  return null;
}

// 4. Binary search - sorted data, or "search the answer space"
function bsearch(arr, t) {
  let lo = 0, hi = arr.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (arr[mid] === t) return mid;
    arr[mid] < t ? lo = mid + 1 : hi = mid - 1;
  }
  return -1;
}

// 5. BFS on a graph - shortest path, level order
function bfs(graph, start) {
  const seen = new Set([start]); const q = [start]; const order = [];
  while (q.length) {
    const node = q.shift(); order.push(node);
    for (const nb of graph[node] ?? []) if (!seen.has(nb)) { seen.add(nb); q.push(nb); }
  }
  return order;
}

// 6. Recursion + memoization  (dynamic programming, the practical form)
const memo = new Map();
function ways(n) {
  if (n <= 2) return n;
  if (memo.has(n)) return memo.get(n);
  const r = ways(n - 1) + ways(n - 2);
  memo.set(n, r); return r;
}

// 7. Sorting with a custom comparator + then a linear scan  (interval merging)
function mergeIntervals(iv) {
  const s = [...iv].sort((a, b) => a[0] - b[0]); const out = [s[0]];
  for (const [a, b] of s.slice(1)) {
    const last = out[out.length - 1];
    if (a <= last[1]) last[1] = Math.max(last[1], b); else out.push([a, b]);
  }
  return out;
}

// 8. Prefix sums - fast range queries
function prefix(nums) { const p = [0]; for (const n of nums) p.push(p.at(-1) + n); return p; }
```

:::edge How to practice so it transfers
Do **60 problems, not 600** — but do them properly. For each: (1) solve it brute force first and state the complexity, (2) improve it and state why, (3) code it without running until you believe it is right, (4) after solving, write the *pattern name* and a one-line trigger ("saw sorted array + pair → two pointers"). Volume without pattern-labeling is why people grind 300 problems and still freeze in interviews. Target: 5 problems a week for the rest of the program, forever.
:::

## Applied CS: where this shows up in your actual job

- **Pagination** = offset/limit vs cursor (a binary-search-like index seek). Offset pagination degrades to O(n) on deep pages — a real production bug.
- **Deduplicating a 2M-row import** = Set, not nested loop.
- **Autocomplete** = prefix tree or an index; debounce = closures + timers.
- **Recommendation "people you may know"** = BFS to depth 2 on a graph.
- **Delivery route optimization** = weighted graph, Dijkstra.
- **Database indexes** = B-trees; understanding this is why you will write fast SQL in Week 10.
""",
)

page(
    id="w3-project",
    title="W3 · First Real Application",
    sub="Week 3, Day 4–6",
    eyebrow="WEEK 3 · FOUNDATIONS",
    subtitle="Integration week. You have HTML, CSS, JS, TS, and CS fundamentals — now build something a stranger would actually use.",
    chips=["18 hours", "Project", "Public deploy"],
    body=r"""
## The brief: "Kano Market Price Tracker"

A real problem: smallholder farmers and traders lack price transparency across markets. Prices for the same commodity can differ 30–40% between markets 20 km apart, and traders exploit the information gap.

**Build a web app that:**
1. Displays current prices for 10 commodities across 6 markets (seed with realistic data in a JSON file).
2. Lets a user filter by commodity and market, and sort by price or change.
3. Shows a 30-day price trend chart per commodity (SVG or Canvas — draw it yourself).
4. Computes and highlights **arbitrage opportunities**: same commodity, cheapest market vs most expensive, with the spread as a percentage and a naira-per-bag figure.
5. Works offline after first load, and is fully usable on a 320px screen over a slow connection.
6. Has a "submit a price" form with full validation (a stub — no backend until Week 9).

## Engineering requirements (this is what makes it a portfolio piece)

- **TypeScript, strict mode, zero `any`.** Zod-validate the JSON data on load.
- **Architecture:** separate `data/`, `logic/` (pure functions, no DOM), `ui/` (rendering only). Your business logic must be testable without a browser.
- **State:** one immutable state object; a `dispatch(action)` reducer; re-render from state. You are hand-rolling Redux — next week React will make total sense.
- **Performance budget:** JS bundle < 50 KB gzipped, LCP < 1.5s on simulated 3G, Lighthouse ≥ 95 across the board.
- **Accessibility:** keyboard-operable, screen-reader-tested with headings and live regions for filter results.
- **Tests:** at least 10 unit tests on the logic layer using Vitest (arbitrage calc, filtering, sorting, percentage change, empty-data edge cases).
- **Deployed** on Vercel with a real URL, and a README with screenshots, architecture notes, and "what I would do next."

## Suggested structure

```
market-tracker/
  src/
    data/prices.json
    data/schema.ts          # zod schemas + inferred types
    logic/arbitrage.ts      # pure: (prices) => opportunities[]
    logic/filters.ts
    logic/stats.ts          # moving average, % change
    logic/__tests__/
    ui/render.ts
    ui/chart.ts             # hand-drawn SVG sparkline
    state.ts                # reducer + store
    main.ts
  index.html
  vite.config.ts
```

```
// logic/arbitrage.ts - the kind of pure function that is a joy to test
export interface Price { commodity: string; market: string; pricePerBag: number; date: string }
export interface Opportunity {
  commodity: string; buyMarket: string; sellMarket: string;
  buyPrice: number; sellPrice: number; spread: number; spreadPct: number;
}

export function findOpportunities(prices: Price[], minSpreadPct = 5): Opportunity[] {
  const byCommodity = Object.groupBy(prices, p => p.commodity);
  const out: Opportunity[] = [];
  for (const [commodity, rows] of Object.entries(byCommodity)) {
    if (!rows || rows.length < 2) continue;
    const sorted = [...rows].sort((a, b) => a.pricePerBag - b.pricePerBag);
    const low = sorted[0]!, high = sorted[sorted.length - 1]!;
    const spread = high.pricePerBag - low.pricePerBag;
    const spreadPct = (spread / low.pricePerBag) * 100;
    if (spreadPct >= minSpreadPct) {
      out.push({ commodity, buyMarket: low.market, sellMarket: high.market,
                 buyPrice: low.pricePerBag, sellPrice: high.pricePerBag, spread, spreadPct });
    }
  }
  return out.sort((a, b) => b.spreadPct - a.spreadPct);
}
```

:::drill Extension challenges (do at least two)
1. Add a **transport cost** input so arbitrage is net of logistics — now the recommendation is actually actionable.
2. Add a **price alert** feature using `Notification` API + `localStorage`.
3. Add **Hausa language toggle** with an i18n object. Real localization is a marketable skill in this region.
4. Add a **share** button that encodes current filters into the URL (`URLSearchParams`) so a trader can WhatsApp a specific view.
:::

:::ship Week 3 deliverable
Deployed app + repo + a 700-word write-up: the problem, your data model, why you chose pure functions for logic, one performance decision with before/after numbers, and one thing that was harder than expected. Post it publicly. This is portfolio piece #1.
:::
""",
)

page(
    id="w4-python",
    title="W4 · Python & SQL — First Contact",
    sub="Week 4, Day 1–3",
    eyebrow="WEEK 4 · FOUNDATIONS",
    subtitle="Your second language and the most durable skill in the entire program. Everything in Phase 6 depends on this week.",
    chips=["18 hours", "Python · SQL · data thinking"],
    body=r"""
## Why both languages

TypeScript builds products. Python and SQL extract truth from data. The engineers who command the highest rates in 2026 are the ones who can do both — build the system *and* answer "so what is actually happening in it?" You start SQL in week 4 rather than week 19 deliberately: 15 weeks of low-intensity practice beats 6 weeks of cramming.

## Python for a JavaScript speaker

```
# Types, but readable. Use type hints from day one - professional Python is typed.
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Loan:
    id: str
    principal: float
    rate: float          # annual, e.g. 0.28
    months: int
    issued: date

def monthly_payment(loan: Loan) -> float:
    # Amortized monthly payment.
    r = loan.rate / 12
    if r == 0:
        return loan.principal / loan.months
    return loan.principal * r / (1 - (1 + r) ** -loan.months)

# Comprehensions - Python's map/filter, and its signature feature
paid = [l for l in loans if l.status == "paid"]
totals = {l.id: monthly_payment(l) for l in loans}
big = {l.customer for l in loans if l.principal > 500_000}   # a set

# Unpacking, defaults, kwargs
def report(rows, *, currency: str = "NGN", limit: int | None = None) -> str: ...

# Context managers - guaranteed cleanup
with open("data.csv") as f:
    header = next(f)

# Error handling
try:
    value = int(raw)
except ValueError as e:
    raise ValidationError(f"bad number: {raw}") from e
finally:
    cleanup()

# The standard library is the superpower
import csv, json, itertools, collections, statistics, pathlib, datetime, re
counts = collections.Counter(row["market"] for row in rows)
top3 = counts.most_common(3)
```

**Environment discipline:** always use `uv`.
```
uv init price-analysis && cd price-analysis
uv add pandas polars matplotlib jupyterlab duckdb
uv run jupyter lab
```
Never `pip install` into your system Python. Every project gets its own environment, always.

## SQL: the highest-ROI skill in this entire program

SQL is 50 years old and will outlive every framework you learn. It appears in nearly every data job posting and most backend ones. **Advanced SQL — window functions and CTEs — is the explicit 2026 benchmark separating entry-level from competitive candidates.** You start now.

Set up local Postgres via Docker (one command, works everywhere):
```
docker run --name forge-pg -e POSTGRES_PASSWORD=dev -p 5432:5432 -d postgres:16
```
Or use a free Neon/Supabase database. Connect with `psql`, DBeaver, or the VS Code Postgres extension.

### The mental model
SQL is **declarative**: you describe the result set you want, and the query planner figures out how. Logical evaluation order is *not* the written order — this is the key insight:

```
FROM / JOIN   →  WHERE  →  GROUP BY  →  HAVING  →  SELECT  →  DISTINCT  →  ORDER BY  →  LIMIT
```

That is why you cannot use a `SELECT` alias in `WHERE` (it does not exist yet) but can in `ORDER BY`.

```
-- The shape of nearly every analytical query you will ever write
SELECT
  m.name                              AS market,
  DATE_TRUNC('month', s.sold_at)      AS month,
  COUNT(*)                            AS transactions,
  SUM(s.amount)                       AS revenue,
  ROUND(AVG(s.amount), 2)             AS avg_ticket,
  COUNT(DISTINCT s.trader_id)         AS active_traders
FROM sales s
JOIN markets m ON m.id = s.market_id
WHERE s.sold_at >= DATE '2026-01-01'
  AND s.status = 'completed'
GROUP BY m.name, DATE_TRUNC('month', s.sold_at)
HAVING SUM(s.amount) > 1000000
ORDER BY month DESC, revenue DESC
LIMIT 100;
```

### Joins — internalize these now

| Join | Returns |
|---|---|
| `INNER JOIN` | Only rows matching in both tables |
| `LEFT JOIN` | All left rows; NULLs where no right match |
| `RIGHT JOIN` | Mirror of left (rarely used — rewrite as LEFT) |
| `FULL OUTER` | Everything from both sides |
| `CROSS JOIN` | Cartesian product (used for date spines) |

:::trap The LEFT JOIN + WHERE bug
`LEFT JOIN orders o ... WHERE o.status = 'paid'` silently converts your LEFT JOIN into an INNER JOIN, because NULL rows fail the WHERE test. Put the condition in the `ON` clause instead: `LEFT JOIN orders o ON o.user_id = u.id AND o.status = 'paid'`. This bug has produced wrong numbers in real board reports. Know it cold.
:::

:::trap NULL is not a value
`NULL = NULL` is not true — it is unknown. Use `IS NULL`. `COUNT(column)` skips NULLs while `COUNT(*)` does not. `SUM` of all NULLs is NULL, not 0 — wrap with `COALESCE(SUM(x), 0)`. Any arithmetic with NULL yields NULL, which silently poisons calculations.
:::

## Your daily SQL habit (10 minutes, every day, for 22 weeks)

Load a real dataset into your local Postgres — Nigerian trade data, a Kaggle e-commerce set, or the NYC taxi dataset. Every single day, write **one query that answers a business question**, and log it in `forge-notes/drills/sql.md` with the question, the query, and the result. By week 26 you will have 150 queries and genuine fluency. This one habit is the difference between "knows SQL" and "is fast in SQL."

@@ Day 1 | Python syntax, data structures, comprehensions, functions, files, stdlib. Rewrite three of your JS exercises in Python.
@@ Day 2 | SQL: SELECT, WHERE, JOIN, GROUP BY, aggregate functions. 40 queries against a real dataset.
@@ Day 3 | Subqueries, CTEs, CASE, date functions, set operations. Load a CSV into Postgres yourself.

:::ship Deliverable
A Jupyter notebook that loads a public Nigerian dataset (NBS, CBN, or World Bank), cleans it in pandas, and answers five questions with charts — plus a `queries.sql` file answering the same five questions in SQL. Compare the two approaches in writing: when is SQL better, when is Python?
:::
""",
)

page(
    id="w4-review",
    title="W4 · Phase 1 Checkpoint",
    sub="Week 4, Day 4–6",
    eyebrow="WEEK 4 · FOUNDATIONS",
    subtitle="Consolidate, self-assess honestly, and fix gaps before they compound.",
    chips=["18 hours", "Assessment"],
    body=r"""
## Self-assessment: can you do these without help?

Score yourself 1–5 on each. Anything under 4 gets remediation time this week — gaps here become disasters in Phase 3.

| # | Competency | Proof it is real |
|---|---|---|
| 1 | Navigate and manipulate a filesystem from the shell | Did the log forensics drill without lookups |
| 2 | Git branch/merge/rebase/recover | Recovered a "lost" commit with reflog |
| 3 | Explain DNS → TCP → TLS → HTTP → render | Wrote it out from memory, correctly |
| 4 | Build a responsive, accessible page with no framework | Lighthouse ≥ 95 on your Week 1 site |
| 5 | Predict event-loop output | Got the sync/micro/macro ordering right |
| 6 | Transform data with map/filter/reduce fluently | Wrote a group-by from scratch |
| 7 | Handle async errors, timeouts, retries | Your fetch code has abort + backoff |
| 8 | Model a domain with TypeScript unions | Zero `any` in the Week 3 project |
| 9 | State the complexity of code you wrote | Can name where your app is O(n²) |
| 10 | Write a multi-join, grouped SQL query | 40+ queries logged |

## Remediation protocol

For any score below 4: spend one focused half-day. Rebuild the smallest possible example from scratch, with no reference, then write the explainer. Do not "re-read" — rebuild.

## The Phase 1 exam (do this in one 4-hour sitting, no AI)

1. **(45 min)** Given a raw CSV of 5,000 transactions, write a TypeScript script that outputs: monthly revenue, top 10 customers, the churn list (customers with no order in 60 days), and flags duplicate transactions. Pure functions, tested.
2. **(45 min)** Build a responsive, accessible pricing-table component with three tiers, a monthly/annual toggle, and keyboard navigation. No framework.
3. **(45 min)** Write 8 SQL queries of increasing difficulty against the dataset you loaded, ending with a self-join and a CTE.
4. **(45 min)** Debug a broken repo (write one yourself first with 5 deliberate bugs, wait a day, then fix it) — a closure bug, an async ordering bug, a CSS stacking-context bug, a NULL-handling SQL bug, and a git conflict.
5. **(60 min)** Write the "what happens when you type a URL" essay, 1,000 words, from memory.

:::edge Compounding move: start your public presence now
You now have three shipped projects and ~20 written explainers. Do these four things this week: (1) turn `forge-notes` into a real blog — GitHub Pages or a simple Next.js site later; (2) write a pinned "I am doing a 26-week build-in-public program" post on LinkedIn and X; (3) update your GitHub profile README with your projects; (4) start posting one build note per week. Recruiters and clients in 2026 find people through public work far more often than through applications. Twenty-two weeks of visible progress before you even start applying is an enormous unfair advantage.
:::

## What is coming

Phase 2 turns you into a frontend engineer: React's mental model, Next.js App Router with server components, data fetching, forms, design systems, and performance. The vanilla-JS state machine you hand-built in Week 2 will make React click in about a day, which is roughly two weeks faster than most learners.
""",
)
