# -*- coding: utf-8 -*-
"""Graded exercise bank with collapsible answer keys, one page per phase."""
PAGES = []
G = "09 · Exercise Bank"

def page(**kw):
    kw.setdefault("group", G)
    kw.setdefault("eyebrow", "EXERCISE BANK")
    PAGES.append(kw)

# ---------------------------------------------------------------- foundations
page(
    id="ex-foundations",
    title="Exercise Bank · Foundations",
    sub="Weeks 1–4 · 12 graded problems",
    subtitle="Terminal, Git, HTTP, HTML/CSS, JavaScript and TypeScript. Do these without opening the answer key — the struggle is the exercise.",
    chips=["12 exercises", "Answer keys included", "Do them cold"],
    body=r"""
Use this page as your drill deck for Phase 1. Rules:

- Attempt each one **from a blank file** before reading anything below it.
- Time yourself. Record the time in `forge-notes/drills/phase-1.md`.
- If you get it wrong, write *why* you got it wrong in one sentence. That sentence is worth more than the correct answer.

Difficulty: **B** = should be fluent, **I** = should be hard, **A** = interview-level.

---

:::exercise 1 · File archaeology — B
**Task.** In a directory with ~5,000 files, find every `.log` file modified in the last 24 hours, sort them by size descending, and print the top 10 with human-readable sizes.

**Constraints.** One pipeline. No `find ... -exec ls`.

**Self-check.** Can you explain what each flag does without looking?

:::answer Show solution
~~~bash
find . -name "*.log" -mtime -1 -type f -print0 \
  | xargs -0 ls -lhS 2>/dev/null | head -n 10
~~~
Key points: `-print0` / `xargs -0` handles filenames with spaces. `-mtime -1` means "less than 1 day old". `-S` sorts by size. `2>/dev/null` hides permission errors so the pipeline still returns results.
:::

:::exercise 2 · The commit that went to the wrong branch — I
**Task.** You realise your last three commits landed on `main` instead of `feature/payments`. `main` has not been pushed. Move exactly those three commits to `feature/payments` and leave `main` where it was.

**Constraints.** Do not use `git reset --hard` in a way that could lose work. Do not cherry-pick.

**Self-check.** Can you explain why the order of the two commands matters?

:::answer Show solution
~~~bash
# 1. Point the feature branch at main, then rewind main by 3 commits
git branch -f feature/payments main
git reset --hard HEAD~3

# 2. Switch over; the commits are now on the feature branch
git checkout feature/payments
~~~
The order is the whole answer. If you rewind `main` first, the branch pointer creation still works because `git branch -f` captures the *current* position — but if you check out `feature/payments` first and then reset, you would rewind the wrong branch. The invariant: create the pointer **before** moving `main`.
:::

:::exercise 3 · Predict the output — I
**Task.** Without running it, write the exact console output of:

~~~js
console.log(1);
setTimeout(() => console.log(2), 0);
Promise.resolve().then(() => console.log(3));
console.log(4);
Promise.resolve().then(() => {
  console.log(5);
  return Promise.resolve();
}).then(() => console.log(6));
~~~

**Self-check.** Can you explain where microtasks sit relative to the timer queue?

:::answer Show solution
~~~text
1
4
3
5
6
2
~~~
Synchronous code runs first (`1`, `4`). Then the microtask queue drains completely before any macrotask: `3` was queued first, then the chained `.then` runs `5`, and its returned promise schedules `6` — still all microtasks, still before the timer. `2` fires last because `setTimeout(..., 0)` is clamped to a minimum delay and always waits for the microtask queue to empty.

The practical consequence: a `setTimeout` 0 is *not* "run immediately after this function". It is "run after everything currently queued as a microtask".
:::

:::exercise 4 · Type the unknown — I
**Task.** Write a TypeScript function `parseJson` that fetches a URL, parses JSON, and returns a typed value — without using `any` and without lying to the compiler with `as`. It must throw a descriptive error if the shape is wrong.

**Constraints.** No external validation library. Must narrow an unknown shape.

**Self-check.** Why is `as T` worse than a runtime check here?

:::answer Show solution
~~~ts
type User = { id: string; email: string; roles: string[] };

function isUser(v: unknown): v is User {
  if (typeof v !== "object" || v === null) return false;
  const o = v as Record<string, unknown>;
  return (
    typeof o.id === "string" &&
    typeof o.email === "string" &&
    Array.isArray(o.roles) &&
    o.roles.every((r) => typeof r === "string")
  );
}

async function parseUser(url: string): Promise<User> {
  const res = await fetch(url);
  if (!res.ok) throw new Error("HTTP " + res.status + " for " + url);
  const raw: unknown = await res.json();
  if (!isUser(raw)) throw new Error("payload did not match User shape");
  return raw;
}
~~~
`as T` asserts without checking, so a malformed API response produces a runtime crash three layers away from the cause. A type predicate converts the runtime check into compile-time narrowing *and* a real error at the boundary. The rule: trust nothing crossing a network boundary, validate once at the edge, then let the type system carry it inward.
:::

:::exercise 5 · The multi-tenant key bug — A
**Task.** This code is meant to cache per-user results, but users report seeing each other's data. Find the bug and fix it.

~~~js
const cache = new Map();
function getUserData(userId, fetcher) {
  if (cache.has(userId)) return cache.get(userId);
  const p = fetcher(userId);
  cache.set(userId, p);
  return p;
}
~~~

**Self-check.** What is the actual security property being violated?

:::answer Show solution
The cache itself is keyed correctly. The bug is **unbounded growth plus shared promise identity** — and the real vulnerability is that the cached value is a *promise that never expires*, so a stale or failed result is served forever, and there is no eviction, so the map grows until the process dies.

The fix has three parts: a TTL, a size cap, and never caching a rejected promise.

~~~js
const cache = new Map();
const TTL = 60_000;
const MAX = 500;

function getUserData(userId, fetcher) {
  const hit = cache.get(userId);
  if (hit && Date.now() - hit.at < TTL) return hit.promise;

  const promise = fetcher(userId).catch((e) => {
    cache.delete(userId);   // never serve a failure twice
    throw e;
  });
  cache.set(userId, { at: Date.now(), promise });

  if (cache.size > MAX) {
    const oldest = cache.keys().next().value;   // Map preserves insertion order
    cache.delete(oldest);
  }
  return promise;
}
~~~
The security framing matters: if `fetcher` ever receives a *trusted* caller's token, an unbounded shared cache becomes a cross-tenant leak. "Sees each other's data" almost always traces to a cache or memo boundary that is not keyed on the tenant — so the habit to build is: **every cache key includes the tenant id, and every cache entry has a TTL.**
:::

:::exercise 6 · Closure memoizer — I
**Task.** Write `memoize(fn)` that caches by *all* arguments, handles object arguments by identity, and exposes `cache.size`. Then write `memoizeByKey(fn, keyFn)` that caches by a derived key.

**Self-check.** Why is caching by `JSON.stringify(args)` a bad idea?

:::answer Show solution
~~~js
function memoize(fn) {
  const cache = new Map();
  const wrapped = (...args) => {
    if (cache.has(args[0]) && args.length === 1) return cache.get(args[0]);
    const key = args.length === 1 ? args[0] : args;
    if (cache.has(key)) return cache.get(key);
    const out = fn(...args);
    cache.set(key, out);
    return out;
  };
  wrapped.cache = cache;
  return wrapped;
}
~~~
Simpler and correct for the common case — a single primitive argument:

~~~js
function memoize(fn) {
  const cache = new Map();
  const wrapped = (x) => {
    if (cache.has(x)) return cache.get(x);
    const out = fn(x);
    cache.set(x, out);
    return out;
  };
  wrapped.cache = cache;
  return wrapped;
}
~~~
`JSON.stringify(args)` is wrong because key *order* changes the string (`{a,b}` vs `{b,a}` produce different keys for the same call), it is O(n) on every call, it throws on cycles and BigInt, and it silently conflates `undefined` with `"undefined"`. Identity-based `Map` keys are O(1) and correct. If you need structural equality, use a stable serialiser with sorted keys — and know why you are paying for it.
:::

:::exercise 7 · Semantic HTML and accessibility — B
**Task.** Build a nav bar, a main article with a heading hierarchy, and a form with a label, an error message, and a submit button — using no `<div>` where a semantic element exists. The error message must be announced by a screen reader.

**Self-check.** Which element carries the accessible name for the input?

:::answer Show solution
~~~html
<nav aria-label="Primary">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/pricing">Pricing</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Pricing</h1>
    <h2>Plans</h2>
    <section aria-labelledby="starter-h">
      <h3 id="starter-h">Starter</h3>
    </section>
  </article>
</main>

<form novalidate>
  <label for="email">Work email</label>
  <input id="email" name="email" type="email"
         aria-describedby="email-err" aria-invalid="true" required />
  <p id="email-err" role="alert">Enter a valid email address.</p>
  <button type="submit">Request access</button>
</form>
~~~
The `<label for>` carries the accessible name — that is the one line most beginners get wrong. `role="alert"` makes the error announced. `aria-describedby` links input to message. `aria-invalid` marks state. `aria-current="page"` tells a screen reader user where they are. Note `<h1>` → `<h2>` → `<h3>` never skips a level; skipping levels breaks the document outline that screen reader users navigate by.
:::

:::exercise 8 · Responsive layout without a framework — B
**Task.** With plain CSS, build a 3-column card grid on desktop, 2-column on tablet, 1-column on mobile, where cards in a row have equal height and the first card spans two columns.

**Self-check.** Why is `minmax` preferable to fixed `fr` units here?

:::answer Show solution
~~~css
.cards {
  display: grid;
  gap: 16px;
  grid-template-columns: 1fr;
}
@media (min-width: 640px) {
  .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (min-width: 1024px) {
  .cards { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .cards > .featured { grid-column: span 2; }
}
.card { display: flex; flex-direction: column; }
~~~
`minmax(0, 1fr)` instead of `1fr` because a bare `1fr` is `minmax(auto, 1fr)` — the `auto` minimum lets a long unbreakable string (a URL, a hash) force the column wider than its share and break the grid. `minmax(0, ...)` allows the item to shrink below its content size, so `overflow` and text wrapping handle it instead.
:::

:::exercise 9 · Debug by bisection — I
**Task.** A React list renders 200 rows but only the first 50 appear. No error is thrown. Describe your exact debugging sequence, in order, with the cheapest test at each step.

**Self-check.** What is the *first* thing you check, and why not the last?

:::answer Show solution
1. **Read the data, not the DOM.** `console.log(items.length)` before render. If it is 50, the bug is in the fetch or the slice — stop here; you just saved an hour. If it is 200, the bug is in rendering.
2. **Check for an explicit limit** — `.slice(0, 50)`, a pagination wrapper, a `take(50)` in the API, or a virtualised list that only mounts visible rows.
3. **Check for an exception swallowed by a boundary.** React error boundaries silently unmount subtrees. Look for `componentDidCatch` or a `key` collision that makes React reuse and hide nodes.
4. **Bisect.** Render only the first 100. Still truncated? The limit is in the data. All 100 show? Render 150. Each halving removes half the search space.
5. **Instrument.** Add a row-count assertion in a test so this class of bug cannot return silently.

Why the first step first: it costs 5 seconds and splits the problem space in half. Beginners check CSS first, which is expensive and usually irrelevant. The discipline is **always test the input before the output**.
:::

:::exercise 10 · Event delegation — I
**Task.** You have a list of 1,000 buttons. Attaching 1,000 listeners makes the page janky. Rewrite it with one listener, preserving which button was clicked and supporting buttons added later.

**Self-check.** Why does this also fix the "buttons added later don't work" bug?

:::answer Show solution
~~~js
document.getElementById("list").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-id]");
  if (!btn) return;                       // click was not on a button
  handleClick(btn.dataset.id);
});
~~~
One listener, O(1) memory, and it works for buttons inserted after the listener was attached because the listener is on the *ancestor* and events bubble. `closest` walks up from the actual click target, so clicks on an icon inside the button still resolve correctly. This is the single highest-leverage DOM pattern in the phase.
:::

:::exercise 11 · `this` and arrow functions — I
**Task.** Explain precisely why this logs `undefined` rather than the object, and fix it two different ways.

~~~js
const counter = {
  count: 0,
  tick: () => { this.count++; }
};
counter.tick();
~~~

**Self-check.** In which case does the arrow function *help*?

:::answer Show solution
Arrow functions have no own `this` — they capture it lexically from the enclosing scope, which at module top level is `undefined` in strict mode (and `globalThis` in sloppy mode). So `this.count++` throws or does nothing useful.

Fix 1 — regular function (method needs dynamic `this`):
~~~js
const counter = {
  count: 0,
  tick() { this.count++; }
};
~~~
Fix 2 — arrow capturing the object (when the callback must retain context):
~~~js
const counter = {
  count: 0,
  tick: function () {
    const self = this;
    setTimeout(() => { self.count++; }, 100);   // arrow keeps self
  }
};
~~~
Arrow functions *help* inside callbacks: `setTimeout(function(){ this.count++ })` would lose `this`, while the arrow inherits it. The rule of thumb: **methods use `function`, callbacks use arrows.**
:::

:::exercise 12 · Ship a portfolio page — B
**Task.** Take your Week 1 sector landing page and make it genuinely good: semantic HTML, responsive at 360px, one custom font, a real image, Lighthouse accessibility score above 95, and a deploy to a live URL.

**Constraints.** No framework. No CSS library. Under 40 KB total.

**Self-check.** Does it still look right with JavaScript disabled?

:::answer Show solution
The deliverable checklist, which matters more than the code:

- `<html lang="en">`, one `<h1>`, no skipped heading levels
- `<meta name="viewport">`, images with `width`/`height` attributes to prevent layout shift
- Text contrast at least 4.5:1 — check with a contrast checker, not by eye
- Tap targets at least 44×44 px
- Works with JS disabled: all content is in HTML, JS only adds enhancement
- Deployed on a real URL, with the URL in your `forge-notes` README

A page that passes these is already better than most freelance portfolios in the Nigerian market, because most are a single hero section with a broken mobile layout.
:::

:::ship Phase 1 drill target
Complete all 12 from a blank editor with no reference material, in under 90 minutes total, with at least 10 correct on the first attempt. Record your time and score. Re-run this set at the start of Week 5 and again at Week 13 — the delta is your real measure of progress.
:::
""",
)

# ---------------------------------------------------------------- frontend
page(
    id="ex-frontend",
    title="Exercise Bank · Frontend",
    sub="Weeks 5–8 · 12 graded problems",
    subtitle="React, Next.js, state, data fetching, forms, performance and accessibility. These are the patterns that show up in real frontend interviews.",
    chips=["12 exercises", "Answer keys included", "React + Next.js"],
    body=r"""
Each exercise assumes React 19 / Next.js App Router. Do them in a real project with a real backend endpoint — mock data hides the bugs that matter.

---

:::exercise 1 · State vs derived — B
**Task.** This component stores `fullName` in state alongside `first` and `last`. Identify the bug and rewrite it correctly.

~~~tsx
const [first, setFirst] = useState("");
const [last, setLast] = useState("");
const [fullName, setFullName] = useState("");
useEffect(() => { setFullName(first + " " + last); }, [first, last]);
~~~

**Self-check.** What is the cost of the `useEffect` beyond the extra render?

:::answer Show solution
`fullName` is *derived* state — it is fully determined by `first` and `last`. Storing it creates two sources of truth that can disagree, plus a render pass where `fullName` is stale (a flash of wrong content), plus an effect that runs on every keystroke.

~~~tsx
const [first, setFirst] = useState("");
const [last, setLast] = useState("");
const fullName = first + " " + last;   // derived, not stored
~~~
The rule: **if you can compute it from existing state or props, compute it.** State is only for values that cannot be derived — things that change independently, or that come from outside React.
:::

:::exercise 2 · The stale closure — A
**Task.** Why does the counter only ever increment by 1, no matter how fast you click? Fix it without adding a dependency.

~~~tsx
const [count, setCount] = useState(0);
useEffect(() => {
  const id = setInterval(() => setCount(count + 1), 1000);
  return () => clearInterval(id);
}, []);
~~~

**Self-check.** Why is `[count]` as the dependency also wrong?

:::answer Show solution
The effect captures `count` from the first render and never re-runs (empty deps), so every tick sets state to `0 + 1`. Adding `[count]` "fixes" the value but destroys the interval every second — it clears and recreates the timer on each tick, so the timing drifts and it is fragile.

The correct fix is the updater form, which reads the latest state from React's queue:

~~~tsx
useEffect(() => {
  const id = setInterval(() => setCount((c) => c + 1), 1000);
  return () => clearInterval(id);
}, []);
~~~
This is the general pattern: **whenever new state depends on old state, use the updater function.** The stale-closure bug is the single most common React correctness bug in production code.
:::

:::exercise 3 · Form with validation — B
**Task.** Build a signup form with client-side validation (email format, password ≥ 12 chars, confirm-match), server-side error display, disabled submit while pending, and no full-page reload.

**Constraints.** No form library. Errors must be announced to screen readers.

**Self-check.** What stops a double-submit?

:::answer Show solution
~~~tsx
type Errors = { email?: string; password?: string; confirm?: string; form?: string };

function validate(v: { email: string; password: string; confirm: string }): Errors {
  const e: Errors = {};
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) e.email = "Enter a valid email address.";
  if (v.password.length < 12) e.password = "Use at least 12 characters.";
  if (v.password !== v.confirm) e.confirm = "Passwords do not match.";
  return e;
}

export function SignupForm() {
  const [values, setValues] = useState({ email: "", password: "", confirm: "" });
  const [errors, setErrors] = useState<Errors>({});
  const [pending, setPending] = useState(false);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    const found = validate(values);
    setErrors(found);
    if (Object.keys(found).length) return;
    setPending(true);
    try {
      await fetch("/api/signup", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(values),
      });
    } catch {
      setErrors({ form: "Something went wrong. Try again." });
    } finally {
      setPending(false);        // runs on success AND failure
    }
  }
  // render: each input gets aria-invalid and aria-describedby
}
~~~
`pending` in the `disabled` attribute is what prevents double-submit — and the `finally` block guarantees the button re-enables even if the request throws, which is where naive implementations leave a permanently disabled form.
:::

:::exercise 4 · Server vs client components — A
**Task.** In Next.js App Router, this page fetches data on the client with a loading spinner. Refactor it so data is fetched on the server, keeping a button that mutates the data as a client component.

**Self-check.** What is the rule for deciding where a component runs?

:::answer Show solution
The rule: **a component is a Server Component by default; it becomes a Client Component only when it needs state, effects, event handlers, or browser APIs.**

~~~tsx
// app/products/page.tsx  — Server Component (default)
export default async function ProductsPage() {
  const products = await db.product.findMany();   // direct DB access, no API round-trip
  return (
    <section>
      <h1>Products</h1>
      <AddToCart products={products} />   {/* client island */}
    </section>
  );
}
~~~
~~~tsx
"use client";                        // only the interactive leaf
export function AddToCart({ products }: { products: Product[] }) {
  const [cart, setCart] = useState<string[]>([]);
  return products.map((p) => (
    <button key={p.id} onClick={() => setCart((c) => [...c, p.id])}>
      Add {p.name}
    </button>
  ));
}
~~~
The performance win is real: the product list ships zero JavaScript and renders before hydration, and only the button is a client island. The architectural rule is to push `"use client"` as far *down* the tree as possible — putting it on the page makes the entire subtree client-rendered and you lose the benefit entirely.
:::

:::exercise 5 · Loading and error states — I
**Task.** Fetch a resource and handle all four states: loading, success, error, and empty. A blank screen or an infinite spinner is a fail.

**Self-check.** What distinguishes "error" from "empty" in the UI?

:::answer Show solution
~~~tsx
type State<T> =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; data: T };

export function useResource<T>(fn: () => Promise<T>): State<T> {
  const [state, setState] = useState<State<T>>({ status: "loading" });
  useEffect(() => {
    let live = true;                    // guards against setState after unmount
    fn()
      .then((data) => { if (live) setState({ status: "ready", data }); })
      .catch((e) => { if (live) setState({ status: "error", message: String(e) }); });
    return () => { live = false; };
  }, []);
  return state;
}
~~~
Four distinct states, discriminated union so the compiler forces you to handle each one. The `live` flag prevents the classic "setState on unmounted component" warning and the race where a slow first request resolves after a fast second one.

Error means "we tried and failed" — show a retry button. Empty means "we tried and there is genuinely nothing" — show a call to action. Conflating them is why users distrust dashboards.
:::

:::exercise 6 · Keyboard accessibility — I
**Task.** Build a dropdown menu that opens on click, closes on Escape, closes when clicking outside, moves focus with arrow keys, and traps nothing but restores focus to the trigger on close.

**Self-check.** Which single ARIA attribute do most implementations get wrong?

:::answer Show solution
The commonly-wrong attribute is `aria-expanded` on the trigger — it must reflect open state and be on the *trigger*, not the menu.

~~~tsx
export function Menu({ items }: { items: string[] }) {
  const [open, setOpen] = useState(false);
  const [i, setI] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const onDoc = (e: MouseEvent) => {
      if (!ref.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, [open]);

  return (
    <div ref={ref}>
      <button
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={() => setOpen((o) => !o)}
        onKeyDown={(e) => {
          if (e.key === "Escape") setOpen(false);
          if (e.key === "ArrowDown") { setOpen(true); setI(0); }
        }}
      >
        Actions
      </button>
      {open && (
        <ul role="menu" onKeyDown={(e) => {
          if (e.key === "Escape") setOpen(false);
          if (e.key === "ArrowDown") setI((n) => (n + 1) % items.length);
          if (e.key === "ArrowUp") setI((n) => (n - 1 + items.length) % items.length);
        }}>
          {items.map((it, n) => (
            <li key={it} role="menuitem" tabIndex={n === i ? 0 : -1}>{it}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
~~~
The cleanup function in the effect is what makes outside-click work without leaking listeners — and it is the part people forget, producing a menu that stays open because five old listeners are still attached.
:::

:::exercise 7 · Performance: the slow list — A
**Task.** A list of 5,000 rows re-renders on every keystroke in a search box, dropping to 8 fps. Diagnose and fix. The list must stay scrollable at 60 fps.

**Self-check.** Which fix gives the biggest win, and why is `memo` alone insufficient?

:::answer Show solution
Three problems, in order of impact:

1. **Every row re-renders on every keystroke.** `React.memo` on the row component stops this — but only if props are stable, which requires (2).
2. **Inline callbacks and objects are new every render.** `onClick={() => ...}` and `style={{...}}` defeat `memo` entirely. Hoist with `useCallback` / module-level constants.
3. **5,000 DOM nodes exist at once.** Memoising does not reduce node count. Window the list.

~~~tsx
const Row = memo(function Row({ item, onPick }: { item: Item; onPick: (id: string) => void }) {
  return <li onClick={() => onPick(item.id)}>{item.name}</li>;
});

export function List({ items }: { items: Item[] }) {
  const [q, setQ] = useState("");
  const onPick = useCallback((id: string) => { /* ... */ }, []);
  const filtered = useMemo(() => items.filter((i) => i.name.includes(q)), [items, q]);

  const [start, setStart] = useState(0);          // simple windowing
  const visible = filtered.slice(start, start + 50);

  return (
    <>
      <input value={q} onChange={(e) => setQ(e.target.value)} />
      <ul onScroll={(e) => setStart(Math.floor(e.currentTarget.scrollTop / 32))}>
        {visible.map((it) => <Row key={it.id} item={it} onPick={onPick} />)}
      </ul>
    </>
  );
}
~~~
The biggest win is windowing — it cuts DOM nodes by 100×. `memo` alone leaves you with 5,000 memoised components still being diffed every keystroke, which is why "just add React.memo" is usually the wrong answer to a slow-list problem. And without stable props, `memo` does nothing at all.
:::

:::exercise 8 · Design system component — I
**Task.** Build a `<Button>` with variants (primary/secondary/ghost/danger), sizes, loading state, disabled state, and icon support — such that a consumer cannot use it incorrectly.

**Self-check.** How do you make the type system prevent `<Button loading>` plus `<Button disabled>` conflicts?

:::answer Show solution
~~~tsx
type Variant = "primary" | "secondary" | "ghost" | "danger";
type Size = "sm" | "md" | "lg";

type ButtonProps =
  | { loading?: false; disabled?: boolean }
  | { loading: true; disabled?: never };     // mutually exclusive

export function Button({
  variant = "primary",
  size = "md",
  loading,
  disabled,
  children,
  ...rest
}: ButtonProps & React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant; size?: Size }) {
  return (
    <button
      className={"btn btn-" + variant + " btn-" + size}
      disabled={disabled || loading}
      aria-busy={loading || undefined}
      {...rest}
    >
      {loading ? <Spinner /> : children}
    </button>
  );
}
~~~
The discriminated union is the trick: if `loading: true` is passed, `disabled` becomes `never`, so `<Button loading disabled>` is a **compile error**. That is the difference between a component library and a pile of divs — the types encode the rules so misuse is impossible rather than merely discouraged.
:::

:::exercise 9 · URL as state — I
**Task.** Filters, sort order, and page number must survive refresh, back button, and sharing the link. Implement without a router library.

**Self-check.** Why is `useState` the wrong tool here?

:::answer Show solution
~~~tsx
function useQueryParam(key: string, fallback: string) {
  const [value, setValue] = useState(
    () => new URLSearchParams(location.search).get(key) ?? fallback
  );
  useEffect(() => {
    const p = new URLSearchParams(location.search);
    if (value === fallback) p.delete(key); else p.set(key, value);
    history.replaceState(null, "", "?" + p.toString());
  }, [key, value, fallback]);
  return [value, setValue] as const;
}
~~~
`useState` is wrong because it is ephemeral and private — a refresh destroys it, the back button does not restore it, and a shared link carries none of the context. Anything a user might want to *bookmark or share* belongs in the URL. Anything purely transient (a hover state, an animation flag) belongs in state.
:::

:::exercise 10 · Error boundary — I
**Task.** One broken component currently blanks the entire app. Add error boundaries so a failure in a widget shows a local fallback while the rest of the page keeps working.

**Self-check.** What does an error boundary *not* catch?

:::answer Show solution
~~~tsx
class Boundary extends React.Component<
  { fallback: React.ReactNode; children: React.ReactNode },
  { error: Error | null }
> {
  state = { error: null };
  static getDerivedStateFromError(error: Error) { return { error }; }
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("boundary caught", error, info.componentStack);   // send to Sentry
  }
  render() {
    return this.state.error ? this.props.fallback : this.props.children;
  }
}
~~~
Wrap each independent widget, not the whole app. Place boundaries at the seams of your UI where a failure is survivable.

What boundaries do **not** catch: errors in event handlers (use try/catch), async errors such as a rejected `fetch` (handle with `.catch`), server-side rendering errors, and errors thrown inside the boundary's own render. This gap is why a complete error strategy needs all three layers: boundaries for render, try/catch for handlers, and `.catch` for promises.
:::

:::exercise 11 · Optimistic UI — A
**Task.** Implement a like button that updates instantly, reverts if the server rejects, and does not flicker when the response is slow.

**Self-check.** What is the failure mode if you forget the revert?

:::answer Show solution
~~~tsx
async function onLike() {
  const previous = liked;
  setLiked(!liked);                     // optimistic
  try {
    await fetch("/api/like", { method: "POST", body: JSON.stringify({ id }) });
  } catch {
    setLiked(previous);                 // revert
    toast("Could not save your like");
  }
}
~~~
Without the revert, the UI lies to the user permanently — they see a like that was never persisted, and the inconsistency only surfaces on the next page load. Optimistic UI is a promise you make to the user; the revert is you keeping it. Note `previous` must be captured *before* the optimistic update, or rapid double-clicks revert to the wrong value.
:::

:::exercise 12 · The Week 8 capstone bar — B
**Task.** Ship a frontend capstone that: renders real data from an API, has loading/error/empty states, passes keyboard-only navigation, scores above 90 on Lighthouse performance and accessibility, has tests covering the trickiest logic, and is deployed with a URL.

**Self-check.** Could a stranger use it without reading instructions?

:::answer Show solution
The acceptance checklist is the deliverable. If any line fails, the capstone is not done:

- Real data from a real API, not a local JSON file
- Four states handled: loading, error, empty, populated
- Every interactive element reachable and operable by keyboard alone
- Lighthouse: performance ≥ 90, accessibility ≥ 90, best practices ≥ 90
- At least one test for logic that is easy to get subtly wrong (a date calculation, a currency format, a filter combination)
- Live URL, plus the repo linked from your `forge-notes` README
- A README with a screenshot, the stack, and how to run it locally

The "stranger test" is the real one. If someone has to ask you how to use it, the design has failed regardless of the code quality.
:::

:::ship Phase 2 drill target
Rebuild the Week 2 Naira Expense Tracker in Next.js with server components, then rebuild the Week 3 Kano Market Price Tracker as a second app. Both must be deployed. Two deployed frontends by end of Week 8 is the portfolio minimum for a frontend-leaning application.
:::
""",
)

# ---------------------------------------------------------------- backend
page(
    id="ex-backend",
    title="Exercise Bank · Backend & Data",
    sub="Weeks 9–13 · 12 graded problems",
    subtitle="Schema design, SQL, auth, idempotency, transactions, queues and API design. These are the questions senior engineers actually ask.",
    chips=["12 exercises", "Answer keys included", "Node · PostgreSQL"],
    body=r"""
Backend exercises reward precision over speed. A schema that is 10% wrong costs months.

---

:::exercise 1 · Multi-tenant schema — A
**Task.** Design a schema for a B2B SaaS where each organisation has users, projects, and invoices. Users may belong to several organisations with different roles. Invoices must be uniquely numbered *per organisation*, not globally.

**Constraints.** Enforce the numbering rule at the database level, not in application code.

**Self-check.** Why is a global `SERIAL` on invoice number wrong here?

:::answer Show solution
~~~sql
CREATE TABLE organisations (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  slug        text NOT NULL UNIQUE,
  name        text NOT NULL,
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE users (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email      text NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Membership with a role, not a role column on users
CREATE TABLE memberships (
  org_id  uuid NOT NULL REFERENCES organisations(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role    text NOT NULL CHECK (role IN ('owner','admin','member','viewer')),
  PRIMARY KEY (org_id, user_id)
);

CREATE TABLE invoices (
  id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id   uuid NOT NULL REFERENCES organisations(id) ON DELETE CASCADE,
  number   integer NOT NULL,
  total    numeric(12,2) NOT NULL CHECK (total >= 0),
  status   text NOT NULL DEFAULT 'draft'
             CHECK (status IN ('draft','sent','paid','void')),
  issued_on date NOT NULL DEFAULT current_date,
  -- the constraint that makes per-org numbering real:
  UNIQUE (org_id, number)
);

CREATE INDEX invoices_org_issued_idx ON invoices (org_id, issued_on DESC);
~~~
The composite `UNIQUE (org_id, number)` is the load-bearing line: it makes "invoice #7" mean something *within* an organisation and impossible to duplicate. A global sequence would hand every organisation the same numbers, and worse, it would leak volume information between tenants — a competitor could infer your customer count.

`memberships` as a join table rather than a `role` column on `users` is the second decision: users belong to many orgs with different roles, and collapsing that into one column forces a migration the first time a real customer asks for it.
:::

:::exercise 2 · The N+1 query — A
**Task.** This endpoint takes 4 seconds for 50 organisations. Rewrite it to run in one query.

~~~ts
const orgs = await db.organisation.findMany({ take: 50 });
for (const org of orgs) {
  org.invoiceCount = await db.invoice.count({ where: { orgId: org.id } });
  org.users = await db.user.findMany({ where: { orgId: org.id } });
}
~~~

**Self-check.** How do you *prove* it is fixed rather than assume it?

:::answer Show solution
~~~sql
SELECT o.id, o.name,
       COUNT(DISTINCT i.id)      AS invoice_count,
       COUNT(DISTINCT m.user_id) AS user_count
FROM organisations o
LEFT JOIN invoices i ON i.org_id = o.id
LEFT JOIN memberships m ON m.org_id = o.id
GROUP BY o.id, o.name
ORDER BY o.name
LIMIT 50;
~~~
One round trip instead of 101. The `LEFT JOIN` (not `INNER`) keeps organisations with zero invoices — a common and invisible bug where empty orgs silently vanish from the list.

Prove it, don't assume it: run `EXPLAIN (ANALYZE, BUFFERS)` before and after, and assert on the *query count* in a test. Most teams add an assertion that a request performs at most N queries, which turns this class of regression into a red build instead of a slow production page.
:::

:::exercise 3 · Index selection — A
**Task.** This query takes 900 ms on 5 million rows. Which index fixes it, and what would you check before adding it?

~~~sql
SELECT * FROM events
WHERE org_id = '...' AND created_at > now() - interval '7 days'
ORDER BY created_at DESC
LIMIT 20;
~~~

**Self-check.** Why might a single-column index on `org_id` be enough — or not?

:::answer Show solution
~~~sql
CREATE INDEX events_org_created_idx ON events (org_id, created_at DESC);
~~~
A composite index with the **equality column first and the range column second**, ordered `DESC` to match the `ORDER BY` so the database can walk the index and stop after 20 rows instead of sorting everything.

Before adding it, check:
1. `EXPLAIN ANALYZE` — is it actually a sequential scan, or is the plan fine and the slowness elsewhere (a lock, a network hop, a slow disk)?
2. **Selectivity.** If one org owns 4.9 of the 5 million rows, the index helps far less than you would hope, and a partitioned or time-bucketed table is the real answer.
3. **Write cost.** Every index slows inserts. A table with heavy write traffic cannot carry a dozen indexes.
4. **Existing redundancy.** An index on `(org_id)` alone may already cover this if `org_id` is selective; `(org_id, created_at)` may be a strictly better replacement for it.

A single-column index on `org_id` can be enough *if* one org has few rows — then the index finds the handful and sorting 20 rows is free. The composite index is the answer when the org is large. You cannot know which without the data, which is why `EXPLAIN ANALYZE` comes first and index-adding comes second.
:::

:::exercise 4 · Payment idempotency — A
**Task.** A client retries a charge request after a network timeout. Without protection, the customer is charged twice. Design the endpoint so retries are safe.

**Constraints.** Must work even if the first request's response was lost.

**Self-check.** What is stored, and when?

:::answer Show solution
~~~ts
app.post("/charges", async (req, res) => {
  const key = req.header("Idempotency-Key");
  if (!key) return res.status(400).json({ error: "Idempotency-Key required" });

  // 1. Have we seen this exact request before?
  const seen = await db.idempotency.findUnique({ where: { key } });
  if (seen) {
    if (seen.status === "done") return res.json(seen.response);      // replay
    return res.status(409).json({ error: "request already in flight" });
  }

  // 2. Claim the key BEFORE doing the work
  await db.idempotency.create({ data: { key, status: "pending" } });

  try {
    const charge = await paystack.charge(req.body);   // the side effect
    await db.idempotency.update({
      where: { key },
      data: { status: "done", response: charge },
    });
    res.json(charge);
  } catch (e) {
    await db.idempotency.update({ where: { key }, data: { status: "failed" } });
    res.status(502).json({ error: "upstream failure" });
  }
});
~~~
The critical detail is step 2: you **claim the key before performing the side effect**. If you record it afterwards and the process dies mid-charge, the retry has no record that a charge happened and the customer pays twice. A pending row is what makes concurrent retries safe — the second request gets a 409 instead of a second charge.

This is the exact pattern Paystack, Stripe and Flutterwave expose, and it is the single most important thing to get right in any Nigerian fintech integration.
:::

:::exercise 5 · Transaction isolation — A
**Task.** Two concurrent requests both read a wallet balance of ₦10,000 and each withdraw ₦8,000, succeeding both times and leaving the balance at ₦2,000 when it should have rejected the second. Fix it.

**Self-check.** Why is `SELECT` then `UPDATE` in application code insufficient?

:::answer Show solution
~~~sql
BEGIN;

-- Lock the row so no other transaction can read it for update
SELECT balance FROM wallets WHERE user_id = $1 FOR UPDATE;

-- Now the check is safe
-- (application asserts balance >= 8000, else ROLLBACK)

UPDATE wallets SET balance = balance - 8000 WHERE user_id = $1;

COMMIT;
~~~
`FOR UPDATE` takes a row lock, so the second transaction blocks at the `SELECT` until the first commits, then reads the *new* balance of ₦2,000 and correctly fails.

Application-level read-then-write is insufficient because the gap between the two statements is where the race lives — both transactions read ₦10,000 before either writes. The database is the only component that can serialise that, because it is the only one that sees both transactions. The habit: **any check-then-act on shared mutable state must happen inside a lock or a constraint.** A `CHECK (balance >= 0)` constraint is an even better backstop, because it makes the invariant true even if the application logic has a bug.
:::

:::exercise 6 · JWT auth with refresh — A
**Task.** Implement login issuing a short-lived access token and a long-lived refresh token. Refresh tokens must be revocable. Explain where each is stored and why.

**Self-check.** Why can the access token not be revoked?

:::answer Show solution
~~~ts
// Access token: 15 minutes, stateless, holds claims
const access = jwt.sign({ sub: user.id, org: user.orgId, role: user.role },
                        process.env.JWT_SECRET, { expiresIn: "15m" });

// Refresh token: 30 days, opaque, stored server-side so it can be revoked
const refresh = crypto.randomBytes(32).toString("hex");
await db.refreshToken.create({
  data: {
    token: sha256(refresh),          // store a hash, never the raw token
    userId: user.id,
    expiresAt: new Date(Date.now() + 30 * 864e5),
  },
});
~~~
Storage: access token in memory (a JS variable), refresh token in an `HttpOnly; Secure; SameSite=Strict` cookie. Never `localStorage` for either — any XSS reads it wholesale.

The access token cannot be revoked because the whole point is that the server verifies it *without a database lookup* — that is what makes it fast and stateless. The consequence is a 15-minute window where a leaked token still works. That is the deliberate trade: short expiry bounds the damage, and the refresh token is the revocable half. If you need instant revocation (a stolen laptop, a fired employee), you need a token blocklist or server-side sessions, and you pay a lookup on every request.
:::

:::exercise 7 · Webhook signature verification — I
**Task.** A payment provider POSTs to `/webhooks/paystack`. Verify the payload is genuinely from them and has not been tampered with.

**Constraints.** Do not trust any header except the signature. Do not parse JSON before verifying.

**Self-check.** What breaks if you verify after `JSON.parse`?

:::answer Show solution
~~~ts
import crypto from "node:crypto";

app.post("/webhooks/paystack", express.raw({ type: "application/json" }), (req, res) => {
  const signature = req.header("x-paystack-signature");
  if (!signature) return res.status(400).send("missing signature");

  // HMAC over the RAW body bytes - before any parsing
  const expected = crypto
    .createHmac("sha512", process.env.PAYSTACK_SECRET_KEY)
    .update(req.body)               // Buffer, not a string
    .digest("hex");

  const ok = signature.length === expected.length &&
             crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
  if (!ok) return res.status(401).send("invalid signature");

  const event = JSON.parse(req.body.toString());   // safe to parse now
  handleEvent(event);
  res.sendStatus(200);               // always 200 fast, process async if slow
});
~~~
If you `JSON.parse` first and re-serialise, the byte sequence changes — whitespace, key order, number formatting, unicode escapes — and the HMAC no longer matches. Verification must operate on the exact bytes received, which is why `express.raw` is used instead of `express.json`.

`timingSafeEqual` prevents a timing attack that could otherwise let someone forge a signature byte by byte. And the endpoint must respond 200 quickly: providers retry aggressively on timeouts, and a slow handler means duplicate deliveries.
:::

:::exercise 8 · Queue with retry and backoff — I
**Task.** A job calls an external API that fails intermittently. Build a retry mechanism with exponential backoff, jitter, a dead-letter queue, and a maximum attempt count.

**Self-check.** Why is jitter necessary?

:::answer Show solution
~~~ts
const MAX_ATTEMPTS = 5;

async function processWithRetry(job: Job) {
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    try {
      return await callExternalApi(job.payload);
    } catch (err) {
      if (attempt === MAX_ATTEMPTS) {
        await deadLetter(job, err);            // give up, but never lose it
        throw err;
      }
      // Exponential backoff WITH jitter: 1s, 2s, 4s, 8s... plus randomness
      const base = 2 ** (attempt - 1) * 1000;
      const delay = base + Math.random() * 1000;      // jitter breaks synchrony
      await sleep(delay);
    }
  }
}
~~~
Jitter exists because without it, every job that failed at the same moment retries at the same moment. A provider outage causes a thousand simultaneous failures; on recovery, a thousand identical retries arrive simultaneously and knock the provider over again — a thundering herd that re-creates the outage. Randomising the delay spreads the load.

The dead-letter queue is not optional: it is the difference between "a job failed and we know about it" and "a job silently vanished". Every message that exhausts retries must land somewhere inspectable.
:::

:::exercise 9 · Rate limiting — I
**Task.** Limit each API key to 100 requests per minute, returning correct `429` responses with retry guidance, without a single point of failure.

**Self-check.** Why is an in-memory counter wrong for a multi-instance deployment?

:::answer Show solution
~~~ts
// Sliding window in Redis - shared across every instance
const WINDOW = 60;
const LIMIT = 100;

async function rateLimit(key: string) {
  const now = Date.now();
  const id = crypto.randomUUID();
  const pipe = redis.multi();
  pipe.zRemRangeByScore(key, 0, now - WINDOW * 1000);   // drop old entries
  pipe.zAdd(key, [{ score: now, member: id }]);
  pipe.zCard(key);
  pipe.expire(key, WINDOW);
  const count = (await pipe.exec())[2] as number;

  if (count > LIMIT) {
    const oldest = await redis.zRangeWithScores(key, 0, 0);
    const retryAfter = Math.ceil((oldest[0].score + WINDOW * 1000 - now) / 1000);
    return { allowed: false, retryAfter };
  }
  return { allowed: true, remaining: LIMIT - count };
}
~~~
An in-memory counter is wrong with more than one instance because each process sees only its own traffic. Deploy four instances and your effective limit is 400/min, and it changes whenever you scale — so the limit is not a limit. Redis gives a single shared counter every instance agrees on.

The sliding window (not a fixed window) matters too: a fixed window lets a client send 100 requests at 11:59:59 and 100 more at 12:00:01, doubling the burst. And a correct `429` always includes `Retry-After` — without it, well-behaved clients hammer you instead of waiting.
:::

:::exercise 10 · API design review — I
**Task.** Critique this endpoint signature and propose a better design.

~~~ts
POST /api/getUserData
{ "userId": 123, "includeOrders": true, "includeAddresses": false, "format": "json" }
~~~

**Self-check.** What is wrong with the verb in the path?

:::answer Show solution
Problems, in order of severity:

| Problem | Why it matters | Fix |
|---|---|---|
| `GET` semantics on a `POST` | Caches, proxies and browsers assume POST is unsafe and non-idempotent; you lose caching and break retries | `GET /api/users/123` |
| Verb in the path (`getUserData`) | The HTTP method already carries the verb; the path should identify the *resource* | `GET /api/users/123` |
| `userId` in the body | Identifiers belong in the path for GET | path parameter |
| `format: "json"` | Content negotiation is a header's job, and hardcoding it prevents other formats | `Accept` header |
| Booleans for related resources | Combinatorial explosion; every new relation needs a new flag, and the response shape is unpredictable | `?include=orders,addresses` or separate requests |

Better:
~~~http
GET /api/users/123?include=orders,addresses
Accept: application/json
~~~
The deeper principle: **a REST endpoint is a resource, not a function.** `getUserData` describes an operation; `/users/123` describes a thing. Things have stable URLs you can cache, link, version and authorise against. Function-style APIs make every one of those harder.
:::

:::exercise 11 · The missing `WHERE` — A
**Task.** This update runs in a migration and silently changes 200,000 rows instead of 3. What was missing, and what would have caught it?

~~~sql
UPDATE users SET status = 'active';
~~~

**Self-check.** How do you make this class of mistake impossible in production?

:::answer Show solution
The missing `WHERE` clause. The fix for the intended operation:

~~~sql
UPDATE users SET status = 'active'
WHERE status = 'pending' AND created_at < now() - interval '90 days';
~~~
How to make the class impossible:
1. **Wrap every migration in a transaction** and run the `SELECT` with the same predicate first to see the row count.
2. **Add a guard assertion** in the migration: `-- expect exactly 3 rows`.
3. **Test migrations against a production-shaped copy** before running them.
4. **Use a linter / CI check** that flags `UPDATE`/`DELETE` without `WHERE`.
5. **Take a backup immediately before** any data migration. Non-negotiable.

The professional habit: run the `SELECT` version of every destructive statement first, *always*, and read the count before you execute the write. It costs ten seconds and it is the difference between a routine deploy and a career-defining incident.
:::

:::exercise 12 · Week 13 integration — B
**Task.** Ship a backend with: a multi-tenant schema, JWT auth, at least one idempotent write endpoint, a rate limiter, an integration test suite, and a deployed URL.

**Self-check.** Can you delete your database and restore it from migrations alone?

:::answer Show solution
Acceptance checklist:

- Multi-tenant schema with the per-org uniqueness constraint enforced in the database
- Auth: access + refresh tokens, revocable refresh, `HttpOnly` cookies
- One idempotent write endpoint with a claimed key before the side effect
- Rate limiting backed by a shared store, with `Retry-After` on 429
- Integration tests that run against a real database (a test container), not mocks
- `npx prisma migrate deploy` (or equivalent) rebuilds the schema from nothing
- Deployed with a health check endpoint and structured logs

The restore-from-migrations test is the real bar. If you cannot rebuild your database from source control, you do not have a database — you have a file on someone's laptop.
:::

:::ship Phase 3 deliverable
A deployed multi-tenant B2B API. The Week 16 version must include containerisation, CI, and observability. This is the project most likely to be discussed in an interview, so be able to draw its architecture on a whiteboard from memory.
:::
""",
)

# ---------------------------------------------------------------- production + AI
page(
    id="ex-production",
    title="Exercise Bank · Production & AI",
    sub="Weeks 14–18 · 10 graded problems",
    subtitle="Docker, CI/CD, observability, system design, and the AI-engineering patterns that separate demos from products.",
    chips=["10 exercises", "Answer keys included", "Docker · LLMs · RAG"],
    body=r"""
This phase is where most self-taught developers stop, and exactly where the 2026 market pays a premium.

---

:::exercise 1 · Multi-stage Dockerfile — I
**Task.** This image is 1.4 GB. Get it under 150 MB without changing application behaviour.

~~~dockerfile
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
CMD ["node", "dist/server.js"]
~~~

**Self-check.** Which layer is the biggest, and why does the naive `COPY . .` hurt rebuilds?

:::answer Show solution
~~~dockerfile
# ---- build stage: has the toolchain, never ships ----
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci                              # cached unless deps change
COPY tsconfig.json ./
COPY src ./src
RUN npm run build && npm prune --omit=dev

# ---- runtime stage: only what runs ----
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
USER node                              # never run as root
EXPOSE 3000
CMD ["node", "dist/server.js"]
~~~
Why each line exists:
- **`alpine`** instead of full `node:20` cuts the base from ~1 GB to ~130 MB.
- **Multi-stage** means the compiler, TypeScript, and dev dependencies never reach the final image.
- **`COPY package*.json` then `npm ci` before `COPY src`** is the caching trick: source changes do not invalidate the dependency layer, so rebuilds take seconds instead of minutes.
- **`npm prune --omit=dev`** removes dev dependencies from the shipped `node_modules`.
- **`USER node`** because a container running as root is a privilege-escalation path.

The naive `COPY . .` before installing deps means *any* file change — even a README edit — invalidates the cache and forces a full `npm install` on every build.
:::

:::exercise 2 · CI pipeline design — I
**Task.** Design a pipeline for a TypeScript monorepo with a web app, an API, and shared packages. Push to `main` deploys to production; PRs get a preview. Total feedback under 6 minutes.

**Self-check.** Which checks run on every push, and which only on `main`?

:::answer Show solution
~~~yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality:                        # fast, runs on everything
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm typecheck            # tsc --noEmit
      - run: pnpm lint
      - run: pnpm test --coverage      # unit, parallel

  build:                          # only after quality passes
    needs: quality
    strategy:
      matrix:
        package: [web, api]
    steps:
      - run: pnpm --filter ${{ matrix.package }} build
      - uses: docker/build-push-action@v6
        with:
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ghcr.io/${{ github.repository }}/${{ matrix.package }}:sha-${{ github.sha }}

  deploy-preview:
    needs: build
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - run: echo "deploy preview from PR branch"

  deploy-prod:
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production         # requires manual approval
    runs-on: ubuntu-latest
    steps:
      - run: echo "deploy to prod"
~~~
The design decisions: **typecheck and lint are cheap and run first** because they fail fastest; the build matrix parallelises independent packages; `--frozen-lockfile` makes the build reproducible; `environment: production` gives you an approval gate so a bad merge cannot auto-deploy. The 6-minute budget is met by running `quality` before anything heavy and never rebuilding unchanged packages.
:::

:::exercise 3 · Observability — I
**Task.** You are paged: "checkout latency spiked at 02:00". You have logs only. What four things do you instrument so this never happens again, and what do you look at first?

**Self-check.** Why are logs alone insufficient?

:::answer Show solution
Instrument the four signals:

1. **Metrics** — RED for services: Rate, Errors, Duration. Percentiles, not averages. `p50`, `p95`, `p99` latency on the checkout endpoint.
2. **Traces** — distributed traces with spans, so you can see *which* downstream call (payment provider, database, cache) is slow rather than just that checkout is slow.
3. **Structured logs** — JSON with `request_id`, `user_id`, `org_id`, so you can pivot from a slow trace to the exact requests.
4. **Alerts on symptoms, not causes** — page on "checkout p99 > 800 ms for 5 minutes", not on "CPU > 70%", which fires constantly and means nothing.

What to look at first: the **p99, not the mean**. A mean of 200 ms with a p99 of 8 seconds means a small subset of requests are pathologically slow — usually one tenant, one region, or one cold cache path. The mean hides it completely.

Logs alone are insufficient because they tell you what happened to *one* request. They cannot tell you that 3% of requests are slow, when it started, or which dependency is responsible. Logs answer "why"; metrics answer "how much, and is it getting worse". You need both, and you need traces to connect them.
:::

:::exercise 4 · Structured LLM output — I
**Task.** Extract structured data from messy support emails into `{ intent, urgency, product, amount }`. The model returns invalid JSON 15% of the time. Make it reliable.

**Self-check.** Why is a regex on the raw text worse than a schema?

:::answer Show solution
~~~ts
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const Ticket = z.object({
  intent: z.enum(["billing", "bug", "refund", "question"]),
  urgency: z.enum(["low", "medium", "high"]),
  product: z.string(),
  amount: z.number().nullable(),
});

const res = await openai.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [
    { role: "system", content: "Extract a support ticket. Output JSON only." },
    { role: "user", content: email },
  ],
  response_format: {
    type: "json_schema",
    json_schema: { name: "ticket", schema: zodToJsonSchema(Ticket), strict: true },
  },
  temperature: 0,                      // extraction is deterministic work
});

const ticket = Ticket.parse(JSON.parse(res.choices[0].message.content!));
~~~
Three reliability layers: **constrained decoding** (`json_schema` with `strict: true` makes invalid JSON structurally impossible), **runtime validation** with Zod (catches semantically wrong but syntactically valid output), and **`temperature: 0`** because extraction should not be creative.

Regex on raw text is worse because it fails silently on paraphrase — "I was charged twice" and "double billing on my card" both need semantic understanding, and no regex survives that variety. A schema also gives you a compile-time type downstream, so the consumer cannot accidentally read a field that does not exist.
:::

:::exercise 5 · RAG retrieval evaluation — A
**Task.** Your RAG chatbot answers well in demos and badly in production. Design an evaluation to find out whether the problem is retrieval or generation.

**Self-check.** How do you separate "wrong chunk retrieved" from "right chunk, bad answer"?

:::answer Show solution
Build a golden set and measure the two stages separately:

~~~text
1. Curate 50 real question/answer pairs from actual user traffic.
2. For each, record the top-5 retrieved chunks.

RETRIEVAL METRICS (is the right chunk even in the top 5?)
  - Recall@5:      % of questions where a gold chunk appears
  - MRR:           rank of the first relevant chunk
  - Context precision: signal-to-noise in what you sent the model

GENERATION METRICS (given the right chunk, is the answer good?)
  - Faithfulness:  every claim traceable to the retrieved context
  - Answer relevance: does it actually address the question
  - Citation accuracy: do the cited chunks support the claims
~~~
The diagnostic split: **run retrieval with generation disabled** and inspect the chunks. If the gold chunk is missing from the top 5, you have a retrieval problem — fix chunking, embeddings, or the query rewrite. If the gold chunk is present but the answer is wrong, you have a generation problem — fix the prompt, the model, or the context window.

Almost everyone skips this and tunes the prompt, which is why RAG demos impress and RAG products disappoint. The evaluation harness is the difference between guessing and engineering. Without numbers you are changing things and hoping.
:::

:::exercise 6 · System design: URL shortener — A
**Task.** Design a URL shortener handling 100M new URLs/month and 10:1 read:write ratio. Cover storage, ID generation, caching, and the redirect.

**Self-check.** Where does the write bottleneck appear, and how do you remove it?

:::answer Show solution
**Storage.** Two tables: `urls(short_code PK, long_url, created_at, owner_id)` and `analytics(short_code, ts, country, referrer)`. The analytics table is the write-heavy one and should be append-only, partitioned by day, and written asynchronously through a queue — never on the request path, because a redirect must be fast and analytics is not allowed to make it slow.

**ID generation.** Base62-encode a monotonically increasing integer, so short codes are dense and index-friendly. Do not hash the long URL: collisions require a re-hash and re-check loop, and you lose the ability to detect duplicate submissions cheaply. A single counter is a write bottleneck, so use a **ticket server** or a time-ordered ID (ULID/KSUID) that can be generated without coordination.

**Caching.** The read path is 90% of traffic and heavily skewed toward recent URLs. Put a CDN in front for the hot 1%, and Redis for the long tail with a TTL. A 301 redirect is cacheable by browsers; a 302 is not but lets you count clicks — the trade is caching versus analytics fidelity.

**The bottleneck and its fix.** The write bottleneck is the counter: every insert contends on the same sequence. Removing it with distributed ID generation (or a range-allocating ticket server that hands out blocks of 1,000 IDs per instance) turns a serial dependency into parallel work.

**What to mention unprompted:** abuse prevention (this is a phishing vector — check against a blocklist), deletion/expiry, and the fact that `short_code` as a primary key means lookups are a single B-tree probe with no secondary index.
:::

:::exercise 7 · LLM cost control — I
**Task.** Your AI feature costs $4,000/day and is growing. Users are sending 8,000-token documents to get a one-line answer. Design a cost control strategy that does not degrade quality.

**Self-check.** Which single change gives the largest saving?

:::answer Show solution
Ranked by impact:

1. **Prompt caching.** Anthropic and OpenAI both cache the static prefix of a prompt. If your system prompt and few-shot examples are 2,000 tokens and identical across calls, caching them cuts their cost by ~90% and latency substantially. This is usually the single biggest win and costs one code change.
2. **Model routing.** Not every request needs the flagship model. Classify difficulty cheaply (a small model, or a heuristic on input length) and route easy requests to a small model. In practice 70–80% of traffic is simple.
3. **Truncate and chunk.** Do not send 8,000 tokens to answer a one-line question. Retrieve only relevant chunks, and cap input length per request.
4. **Output caps.** Set `max_tokens` to what the answer actually needs. An unbounded response is an unbounded bill.
5. **Per-tenant budgets with hard caps.** A single abusive tenant should not be able to run up your bill. Enforce quotas at the API gateway, not in application code.
6. **Batch where latency allows.** Batch APIs are typically 50% cheaper for non-interactive work.

The largest single change is almost always prompt caching, because the static prefix is the bulk of most production prompts and it is repeated on every call.
:::

:::exercise 8 · Secrets management — I
**Task.** An API key was committed to a public repo and pushed. What do you do, in what order, and what do you change so it cannot recur?

**Self-check.** Why is deleting the commit insufficient?

:::answer Show solution
Order of operations:

1. **Rotate the key immediately.** Before anything else. Assume compromise from the moment of push — bots scrape public GitHub commits within seconds.
2. **Audit usage** of the old key in the provider's logs for unauthorised calls.
3. **Revoke** the old key, do not merely delete it from the code.
4. **Purge history** (`git filter-repo`, not `filter-branch`) and force-push — but understand this is cleanup, not remediation.
5. **Notify** anyone affected per your incident process.
6. **Prevent recurrence:** pre-commit secret scanning (`gitleaks`), a `.gitignore` entry, and CI scanning on every push.

Deleting the commit is insufficient because the key is already cloned into every fork and mirror, archived by third-party crawlers, and present in your local reflog. Rotation is the only real fix — history rewriting is theatre that makes you *feel* better. The professional rule: **a committed secret is a compromised secret. Rotate first, ask questions later.**
:::

:::exercise 9 • Deploy and rollback — I
**Task.** A bad deploy takes checkout down. Describe the fastest safe recovery, and the change that would have caught it before release.

**Self-check.** Why is "fix forward" usually wrong under pressure?

:::answer Show solution
Fastest safe recovery, in order:
1. **Roll back to the last known-good artifact.** One command, one immutable image tag, under a minute. This is why you deploy immutable, versioned images rather than mutable `latest`.
2. **Verify health** — not just "the pod is running", but the actual health check hitting the database and returning 200.
3. **Only then** debug. On a copy of production data, not on the live system.

"Fix forward" is wrong under pressure because you are writing untested code with the site down, adrenaline high, and no ability to verify the fix before shipping it. Rollback restores service; fixing forward gambles service on a second deploy. The two are not equivalent.

What catches it earlier: a **canary or blue-green deployment** that sends 5% of traffic to the new version and automatically rolls back on error-rate regression, plus a staging environment that is production-shaped rather than a toy. And crucially — a deploy pipeline that takes minutes, because a slow pipeline is what tempts people to fix forward in the first place.
:::

:::exercise 10 · Phase 5 capstone — B
**Task.** Ship an AI feature with: structured output validated by a schema, retrieval over a real document corpus, an evaluation harness with at least 30 test cases, cost tracking per tenant, and graceful degradation when the model API is down.

**Self-check.** What happens to your product when the LLM API has an outage?

:::answer Show solution
Acceptance checklist:

- Structured output with constrained decoding *and* runtime validation
- Retrieval over at least 200 real documents, with chunking you can justify
- An eval harness: 30+ cases, retrieval and generation metrics reported separately
- Per-tenant cost tracking with a hard budget cap
- A fallback path when the API is unavailable — a cached answer, a degraded mode, or a clear error. Never a spinner that hangs forever.

The last item is the one most AI demos fail. Your product has an availability target, and a third-party API you do not control is a dependency with its own failure modes. Design for it being down, because it will be.
:::

:::ship Phase 4–5 deliverable
A containerised, CI-deployed multi-tenant SaaS with an evaluated AI feature. By the end of Week 18 you should have three deployed products and an eval harness — the harness is the artifact almost no other candidate will have, and it is the one senior interviewers ask about.
:::
""",
)

# ---------------------------------------------------------------- data analysis
page(
    id="ex-data",
    title="Exercise Bank · Data Analysis",
    sub="Weeks 19–24 · 14 graded problems",
    subtitle="SQL, pandas, statistics, experimentation, analytics engineering and dashboard design. The analyst skill stack, graded.",
    chips=["14 exercises", "Answer keys included", "SQL · pandas · stats"],
    body=r"""
The 2026 analyst bar is window functions, CTEs, and a performance mindset — not `SELECT * FROM t WHERE x = 1`. These exercises are set at that level.

All SQL exercises assume PostgreSQL. Data is described inline so you can build the fixtures yourself.

---

:::exercise 1 · Window functions — B
**Task.** For each customer, rank their orders by amount descending and show only each customer's top 2 orders.

~~~sql
CREATE TABLE orders (id int, customer_id int, amount numeric, created_at date);
~~~

**Self-check.** Why does a `GROUP BY` approach fail here?

:::answer Show solution
~~~sql
SELECT customer_id, id, amount, rn
FROM (
  SELECT customer_id, id, amount,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rn
  FROM orders
) t
WHERE rn <= 2;
~~~
`GROUP BY` fails because it collapses rows to one per group — you physically cannot return the top *2* orders from a grouped result without a join back to the original table, which is both slower and more code. The window function keeps every row while attaching a rank computed within each partition, so filtering happens after ranking.

Use `ROW_NUMBER()` for a strict top-N. Use `RANK()` if you want ties to share a position (and therefore potentially return more than N rows), and `DENSE_RANK()` if you do not want gaps. Interviewers specifically test whether you know the difference.
:::

:::exercise 2 · Running totals and cohorts — I
**Task.** Produce a monthly cohort retention table: rows are signup months, columns are months since signup, values are the percentage of the cohort still active.

**Self-check.** What makes this query slow at scale, and how do you fix it?

:::answer Show solution
~~~sql
WITH cohorts AS (
  SELECT user_id,
         date_trunc('month', signed_up_at)::date AS cohort_month,
         (date_trunc('month', last_active_at)::date
          - date_trunc('month', signed_up_at)::date) / 30 AS period
  FROM users
  WHERE last_active_at IS NOT NULL
),
sizes AS (
  SELECT cohort_month, COUNT(*) AS cohort_size
  FROM cohorts GROUP BY cohort_month
)
SELECT c.cohort_month,
       c.period,
       COUNT(*) AS active_users,
       ROUND(100.0 * COUNT(*) / s.cohort_size, 1) AS retention_pct
FROM cohorts c
JOIN sizes s USING (cohort_month)
GROUP BY c.cohort_month, c.period, s.cohort_size
ORDER BY c.cohort_month, c.period;
~~~
The `period` arithmetic uses date subtraction in days divided by 30 — crude but adequate for a first pass. The performance issue at scale is the self-join on `sizes`, which recomputes cohort sizes for every row. Fix it with a materialised view refreshed nightly, or a `WINDOW` clause that computes the size in the same pass. Retention queries are the canonical "correct but too slow" query, and knowing when to materialise is the senior skill.
:::

:::exercise 3 · Query optimisation — A
**Task.** This takes 40 seconds on 50M rows. Rewrite it, and say what you would check first.

~~~sql
SELECT DATE_TRUNC('day', created_at) AS d, COUNT(*)
FROM events
WHERE EXTRACT(YEAR FROM created_at) = 2025
GROUP BY 1;
~~~

**Self-check.** Why does the function on `created_at` defeat the index?

:::answer Show solution
~~~sql
SELECT created_at::date AS d, COUNT(*)
FROM events
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'
GROUP BY 1;
~~~
The original wraps `created_at` in `EXTRACT(YEAR FROM ...)`, which makes the predicate **non-sargable** — the database must evaluate the function on every one of the 50M rows because it cannot reason about the index. Rewriting it as a range comparison lets a B-tree index on `created_at` seek directly to the start of 2025 and scan only the matching rows. This is the single most common performance bug in analytical SQL.

Check first: `EXPLAIN (ANALYZE, BUFFERS)` to confirm it is a sequential scan, and confirm an index on `created_at` actually exists. If the table is partitioned by month, the range predicate also enables partition pruning, which is an order-of-magnitude win on its own.
:::

:::exercise 4 · pandas: the groupby trap — I
**Task.** Compute each customer's spend as a share of their own total, then each customer's share of overall revenue. Do it without a Python loop.

**Self-check.** Why does `groupby().sum()` then a plain division give the wrong answer?

:::answer Show solution
~~~python
import pandas as pd

df = pd.DataFrame({
    "customer": ["a", "a", "b", "b", "c"],
    "amount":   [100, 200, 50, 150, 300],
})

# 1. Share within each customer's own total
df["cust_total"] = df.groupby("customer")["amount"].transform("sum")
df["share_of_cust"] = df["amount"] / df["cust_total"]

# 2. Share of overall revenue
grand = df["amount"].sum()
df["share_of_total"] = df["amount"] / grand
~~~
`transform` is the key: it returns a Series **aligned to the original index**, so you can divide element-wise and keep every row. `groupby().sum()` alone returns a *reduced* Series indexed by customer — dividing by it either raises a shape error or silently broadcasts incorrectly depending on alignment, which is worse because it looks like it worked.

The habit to build: **`transform` when you need the aggregate back on the original rows; `agg` when you want a summary table.** Confusing the two is the most common pandas correctness bug in real analysis code.
:::

:::exercise 5 · Cleaning a messy Nigerian dataset — I
**Task.** A market price CSV has: amounts as `"₦1,200.50"` and `"1200"`, dates in `DD/MM/YYYY` and `YYYY-MM-DD`, state names with inconsistent casing and trailing spaces, and 12% null prices. Produce a clean, analysis-ready frame.

**Self-check.** Which cleaning step, done in the wrong order, silently corrupts data?

:::answer Show solution
~~~python
import pandas as pd
import numpy as np

df = pd.read_csv("prices.csv", dtype=str)          # read as str: no premature coercion

# 1. Normalise currency strings BEFORE numeric conversion
df["price"] = (
    df["price"].str.replace("₦", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
)
df["price"] = pd.to_numeric(df["price"], errors="coerce")   # bad values become NaN

# 2. Parse mixed date formats - dayfirst handles DD/MM/YYYY
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce", format="mixed")

# 3. Normalise categorical text
df["state"] = df["state"].str.strip().str.title()

# 4. Handle nulls deliberately, never silently
n_null = df["price"].isna().sum()
print(f"unparseable prices: {n_null} ({100*n_null/len(df):.1f}%)")
df = df.dropna(subset=["price", "date"])           # or impute, but decide explicitly

df = df.drop_duplicates()
~~~
The step that corrupts data if done in the wrong order is **date parsing before string cleaning** — or worse, numeric conversion before stripping `₦` and commas. `pd.to_numeric("₦1,200.50")` returns `NaN` with no error by default when `errors="coerce"` is set, so 12% of your data vanishes and every downstream average is computed on the survivors. That is a bias, not a cleanup.

Always print the loss rate. If 12% of your prices failed to parse, the right response is to fix the parser, not to proceed with 88% and quietly wrong aggregates.
:::

:::exercise 6 · A/B test significance — A
**Task.** Control: 10,000 visitors, 500 conversions. Variant: 10,000 visitors, 570 conversions. Is the variant better? Give the lift, the p-value, and your recommendation.

**Self-check.** What does "statistically significant" not tell you?

:::answer Show solution
~~~python
from scipy import stats
import numpy as np

n_c, x_c = 10000, 500
n_v, x_v = 10000, 570

p_c, p_v = x_c/n_c, x_v/n_v
p_pool = (x_c + x_v) / (n_c + n_v)
se = np.sqrt(p_pool * (1 - p_pool) * (1/n_c + 1/n_v))
z = (p_v - p_c) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z)))

print(f"control:  {p_c:.2%}")
print(f"variant:  {p_v:.2%}")
print(f"lift:     {(p_v/p_c - 1):+.1%}")
print(f"z:        {z:.2f}   p-value: {p_value:.4f}")
~~~
Output: control 5.00%, variant 5.70%, lift +14.0%, p ≈ 0.013.

Interpretation: the lift is **statistically significant** at α = 0.05 — there is roughly a 1.3% probability of seeing a difference this large if the two variants were truly identical.

What significance does **not** tell you:
- **Practical importance.** A 0.7 percentage-point lift on a metric worth ₦50 per conversion is a very different decision than the same lift on a metric worth ₦50,000.
- **That it will replicate.** With p = 0.013 you are near the threshold; a second test would plausibly show less.
- **Who it worked for.** An aggregate lift can hide a large win in one segment offset by a loss in another. Always segment before shipping.
- **That you ran it correctly.** Check for peeking, sample ratio mismatch, and whether the metric is even the one that matters.
:::

:::exercise 7 · Metric definition — A
**Task.** Define "active user" precisely enough that two engineers would compute the same number. Then define it for a mobile money app where a user can transact, check balance, or just open the app.

**Self-check.** What makes a metric definition *wrong* rather than merely different?

:::answer Show solution
~~~text
METRIC: monthly_active_users (MAU)

Definition: the count of distinct user_id values with at least one
            event of type in ('session_start', 'transaction')
            where event_ts falls in the calendar month,
            and user.account_status = 'active',
            and user.is_test_account = false.

Grain:       one row per user per month
Timezone:    Africa/Lagos (WAT) - business operates in Nigeria
Exclusions: internal staff accounts, seeded demo data,
            accounts created and deleted within the same month
Owner:       analytics engineering
Refresh:     daily by 06:00 WAT
```
A definition is *wrong* — not merely different — when it is **ambiguous**: when two competent people reading it would compute different numbers, or when it silently changes meaning between reports. The failure modes that make definitions wrong:

- **No timezone.** "This month" for a user in Lagos and an engineer in San Francisco are different months for 8 hours a day.
- **No exclusions.** Test accounts and staff inflate the number, and the inflation grows as your team grows.
- **No event list.** "Did something" is not a definition. Opening the app and completing a transaction are different products.
- **No grain.** Counting events instead of distinct users changes the number by an order of magnitude.
- **No owner.** Nobody notices when the underlying event schema changes and the metric silently breaks.

The professional habit: **every dashboard tile links to its definition, and the definition names a timezone.** A metric without a definition is a rumour with a number attached.
:::

:::exercise 8 · dbt model design — I
**Task.** Model an e-commerce warehouse from raw `orders`, `order_items`, `products`, and `customers` into a mart that finance can query for monthly revenue by product category.

**Self-check.** Where do you put the currency conversion, and why not in the BI tool?

:::answer Show solution
~~~sql
-- models/staging/stg_orders.sql
-- One row per order, cleaned, typed, renamed. No business logic.
with source as (
    select * from {{ source('raw', 'orders') }}
)
select
    id as order_id,
    customer_id,
    created_at,
    status,
    total_amount,
    currency,
    updated_at
from source
where id is not null

-- models/marts/fct_revenue.sql
-- One row per order line, with the grain made explicit.
with items as (
    select * from {{ ref('stg_order_items') }}
),
products as (
    select * from {{ ref('dim_products') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
)
select
    o.order_id,
    o.created_at,
    date_trunc('month', o.created_at) as revenue_month,
    p.category,
    i.quantity,
    i.unit_price,
    i.quantity * i.unit_price as line_revenue,
    o.currency
from items i
join orders o   on o.order_id = i.order_id
join products p on p.product_id = i.product_id
where o.status not in ('cancelled', 'refunded')
~~~
Currency conversion goes in a **dedicated dbt model**, not the BI tool, because it must be applied consistently everywhere and audited in version control. Putting it in the BI layer means every dashboard reimplements it, and the first person who uses the wrong rate for a month is invisible until an audit.

The layering rule: staging models clean and rename with no business logic; marts encode the business logic and are the only thing analysts query. When finance asks "why is this number different from that number", the answer must be findable in a reviewed, tested model — not in a spreadsheet formula.
:::

:::exercise 9 · Dashboard design — I
**Task.** Design an executive dashboard for a Nigerian logistics company. State the five tiles, the drill-down path, and the one number the CEO should see first.

**Self-check.** What makes executives stop trusting a dashboard?

:::answer Show solution
~~~text
TILE 1 (hero number): On-time delivery rate, last 7 days, with a
        7-day trend sparkline and the delta vs the prior week.
        This is the number the business exists to move.

TILE 2: Active shipments, split by lane, with a count of
        delayed shipments over 48 hours highlighted in red.

TILE 3: Cost per delivery by lane, trended, with the
        three most expensive lanes called out.

TILE 4: Failed delivery attempts, by reason code
        (customer unavailable, wrong address, vehicle issue).

TILE 5: Fleet utilisation - vehicles dispatched vs available.

DRILL-DOWN PATH:
  CEO view (5 tiles) -> regional manager (tiles by state)
  -> operations (individual shipments, filterable by lane and date)
  -> analyst (row-level export, every shipment with all attributes)

RULES APPLIED:
  - Every tile shows its definition on hover, with the owner and
    the timezone. Africa/Lagos, always.
  - Comparisons are always vs a prior period, never a bare number.
  - No tile without an action attached. If nobody would change
    their behaviour based on it, delete it.
```
Executives stop trusting a dashboard for three reasons, all of which are design failures rather than data failures:

1. **The number changes and nobody can explain why.** No definition link, no owner, no changelog.
2. **Two tiles disagree.** Two definitions of "delivery" computed two ways in two tools.
3. **It is never wrong — until it is.** A dashboard that has always looked plausible and then is off by 30% destroys more trust than one that openly shows data-quality warnings.

The CEO number is the one that changes decisions. If the answer is "all of them", the dashboard has no point of view and will be ignored.
:::

:::exercise 10 · Anomaly detection — I
**Task.** Daily transaction volume for a payments platform suddenly drops 40%. Build a check that flags it within an hour, and explain how you avoid alert fatigue.

**Self-check.** Why does a fixed threshold produce false alarms?

:::answer Show solution
~~~sql
-- Robust anomaly detection: median + MAD instead of mean + stddev
WITH daily AS (
    SELECT day, volume,
           -- rolling median and MAD over the trailing 28 days
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY volume)
             OVER (ORDER BY day ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING) AS med,
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY abs_dev)
             OVER (ORDER BY day ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING) AS mad
    FROM (
        SELECT day, volume,
               ABS(volume - LAG(volume) OVER (ORDER BY day)) AS abs_dev
        FROM daily_volumes
    ) t
)
SELECT day, volume, med,
       (volume - med) / NULLIF(1.4826 * mad, 0) AS robust_z
FROM daily
WHERE ABS((volume - med) / NULLIF(1.4826 * mad, 0)) > 3.5
ORDER BY day;
~~~
Median and MAD (median absolute deviation) are **robust** — a single wild outlier barely moves them, whereas one 10× spike destroys a mean and standard deviation so completely that the following normal days all look anomalous.

A fixed threshold ("alert if volume < 1,000") produces false alarms because transaction volume is seasonal: it drops every Sunday, every public holiday, and every month-end. The alert fires weekly, everyone mutes it, and then the real 40% drop goes unnoticed. **An alert nobody trusts is worse than no alert**, because it consumes the attention you need for the real incident.

To avoid fatigue: alert on the *robust* z-score rather than an absolute level, require the anomaly to persist across two consecutive windows, and suppress alerts on known seasonal patterns (Sundays, holidays) using a calendar table.
:::

:::exercise 11 · Cohort LTV — A
**Task.** Estimate 12-month customer LTV from 6 months of cohort data, for a subscription product with monthly churn.

**Self-check.** Why is averaging all customers' lifetime value biased?

:::answer Show solution
~~~text
Method: fit a retention curve to observed cohorts, extrapolate, multiply by ARPU.

1. Observed retention by month-since-signup, pooled across cohorts
   (pooling is valid because retention by period is stable across
   cohorts in a mature product - verify this before pooling).

   period:  0     1     2     3     4     5
   retained: 100%  72%   58%   49%   43%   39%

2. Fit a decay model. Exponential gives r where 0.39/1.00 = (1-r)^5
   => r ≈ 0.21% monthly churn... but real curves are usually
   better fit by a power law (Weibull) because churn decelerates.

3. Integrate the fitted curve to month 12 -> expected retained-months
   per acquired customer. Say the fit gives 4.1 retained-months.

4. LTV = 4.1 × ARPU (₦2,500) = ₦10,250 per customer.

5. Report as a RANGE with the cohort spread, not a point estimate.
```
Averaging observed customers' lifetime value is **survivorship-biased**: customers who churned in month 1 have a short observed lifetime and customers still active at month 6 have an artificially truncated one. The average of those two is a number that describes no real customer. You must model the retention curve and integrate it, not average realised history.

This is the same bias that makes "average tenure of current employees" meaningless, and it is worth being able to explain out loud — it is a favourite interview question precisely because it separates people who have done the work from people who have only run `AVG()`.
:::

:::exercise 12 · Public-data project — B
**Task.** Take one Nigerian public dataset (NBS, NPC, NDIC, or a state open-data portal), clean it, model it, build a dashboard, and publish the methodology.

**Self-check.** Would your numbers survive a journalist's fact-check?

:::answer Show solution
Acceptance checklist:

- Source cited with the retrieval date and the exact URL
- Every transformation documented in a version-controlled repo, reproducible from raw
- Data-quality issues disclosed prominently, not hidden — missing states, known under-reporting, definitional changes between years
- Confidence intervals or at minimum a sensitivity note on any headline figure
- A methodology page a non-technical reader can follow
- A public-good framing: the dashboard answers a question a decision-maker actually has

The journalist test is the real bar. Nigerian public data has well-documented problems — coverage gaps, definitional breaks between survey vintages, and figures that do not reconcile across agencies. A dashboard that quietly smooths over those will be wrong, and a dashboard that discloses them will be trusted. Disclosure is not a disclaimer you add at the end; it is the reason anyone should believe your number.
:::

:::exercise 13 · Statistics for analysts — I
**Task.** A product manager says "conversion went up 3%, ship it". Your data shows p = 0.31 on 40,000 users per arm. Explain, in language a PM will accept, why you are not shipping.

**Self-check.** What is the *right* next question to ask?

:::answer Show solution
~~~text
"With 40,000 users per arm, a 3% relative lift is within the range
we would expect from random noise alone - there is roughly a 1 in 3
chance of seeing a difference this large even if the change does
nothing at all. To detect a 3% lift reliably at our baseline, we
would need about 190,000 users per arm.

So the question is not 'is it significant' - it is 'is a 3% lift
worth six weeks of engineering time?' If yes, let us run it longer.
If no, let us test something with a bigger expected effect, because
this experiment cannot answer the question in the time we have."
~~~
The right next question is **not** "can we get more traffic?" — it is "what effect size would make this worth shipping?" That reframes the conversation from statistics to product, which is where it belongs and where you will be credible. Power analysis in reverse: given the sample you can realistically get, what is the smallest effect you could detect, and is that effect worth acting on?

The skill being tested is communication, not computation. An analyst who says "p = 0.31, not significant" has given the PM nothing. An analyst who converts that into a decision about experiment duration and expected effect size has done the job.
:::

:::exercise 14 · Week 24 data capstone — B
**Task.** Ship an end-to-end analytics project: raw ingestion, cleaning, dbt models with tests, a dashboard, and a written insight with a recommendation.

**Self-check.** Does your recommendation name a decision and an owner?

:::answer Show solution
Acceptance checklist:

- Raw data ingested from a real source, not hand-typed
- Cleaning reproducible from source in version control
- dbt models with tests: not-null, unique, accepted values, and at least one relationship test
- A dashboard with a defined metric dictionary
- A written insight: **one paragraph, naming the finding, the decision it implies, and who should make it**
- The recommendation is falsifiable — you state what evidence would change your mind

The last two items are what separate an analytics project from a data exercise. "Revenue is flat" is an observation. "Revenue is flat because repeat purchase rate fell 8 points in the South-West after the March price change; the pricing team should test a regional price before the Q3 rollout" is an analysis. It names a finding, a decision, and an owner — and it can be proven wrong, which is what makes it worth reading.
:::

:::ship Phase 6 deliverable
Three deployed dashboards, one dbt project with tests, one public-data analysis with published methodology, and one deployed ML scoring endpoint. The public-data project is your differentiator: almost no junior analyst has one, and it demonstrates judgment rather than tool familiarity.
:::
""",
)

# ---------------------------------------------------------------- capstone + career
page(
    id="ex-capstone",
    title="Exercise Bank · Capstone & Career",
    sub="Weeks 25–26 · 8 graded problems",
    subtitle="The exercises that convert skill into an offer. Portfolio review, take-home simulation, system design, pricing, and negotiation.",
    chips=["8 exercises", "Answer keys included", "Simulated"],
    body=r"""
Everything before this page builds capability. This page converts it into income.

---

:::exercise 1 · Portfolio teardown — B
**Task.** Review your own portfolio as a hiring manager with 90 seconds and 40 other applicants. Cut anything that does not survive that.

**Self-check.** Which project would you delete, and why does deleting it make you stronger?

:::answer Show solution
A hiring manager spends about 90 seconds on a portfolio. In that window they answer three questions: **can this person build, can this person finish, and can this person communicate?** Every element that does not help answer one of those is noise.

The teardown checklist:

| Element | Keep? | Why |
|---|---|---|
| A deployed project with a live URL | Always | Proves finishing, not just starting |
| A README with a screenshot and setup steps | Always | Proves communication |
| A project with real users or real data | Always | Proves it survived contact with reality |
| A tutorial-clone (todo app, Netflix clone) | Delete | Answers none of the three questions |
| A project with no README | Fix or delete | An undocumented repo reads as abandoned |
| Six half-finished projects | Delete five | One finished thing beats six started things |
| A certificate screenshot | Delete | Nobody hires certificates |

The project to delete is the one you are most attached to and least proud of — usually an early tutorial follow-along. Deleting it is not loss, it is removing the evidence that you once could not build.

The counterintuitive rule: **a portfolio of three deep projects beats a portfolio of ten shallow ones**, because depth is the only thing that survives a technical interview, where the conversation will go three levels below whatever you put on the page.
:::

:::exercise 2 · Take-home simulation — A
**Task.** A 4-hour take-home: "Build an API for a library with books, members, and loans. Include overdue detection." Produce the plan and the deliverable.

**Self-check.** What do you do in the first 20 minutes, and what in the last 20?

:::answer Show solution
**First 20 minutes — read and plan, do not code.**
- Re-read the brief and list every explicit requirement and every ambiguous term.
- Decide the schema first. Loans are the join table: `(book_id, member_id, loaned_at, due_at, returned_at)`.
- Identify the one genuinely interesting problem — overdue calculation across timezones — and note it.
- Write a 6-line plan in the README before any code exists. This is what the reviewer reads first.

**Hours 1–3 — build in this order:**
1. Schema and migrations, with constraints (`CHECK (due_at > loaned_at)`, a partial index on open loans).
2. The three core endpoints, tested.
3. Overdue logic, with a pure function you can unit test — not a query buried in a controller.
4. Tests for the tricky logic only. Not 100% coverage; coverage of the parts that are easy to get wrong.
5. A README: what it does, how to run it, decisions made, what you would do with more time.

**Last 20 minutes — the part everyone skips:**
- Run it from scratch on a clean clone. Half of all broken take-homes fail here.
- Re-read the brief line by line against your implementation.
- Add the "what I would do with more time" section. It signals seniority more than any feature.

What actually gets evaluated, in order: **does it run, is it tested, is the schema sound, is the README clear, is the overdue logic correct.** Fancy architecture scores nothing if `npm install && npm start` fails.
:::

:::exercise 3 · System design interview — A
**Task.** "Design a system that sends 1 million SMS notifications per day, with delivery receipts and retry." Talk through it out loud for 30 minutes.

**Self-check.** What do you ask before drawing anything?

:::answer Show solution
**Questions first (5 minutes) — this is what separates seniors from juniors:**
- What is the latency requirement — seconds or minutes acceptable?
- Is this transactional (OTP, must arrive in seconds) or bulk (marketing)?
- What happens on failure — retry forever, or drop after N attempts?
- Do we need per-recipient delivery receipts, or aggregate?
- Which provider, and is multi-provider failover required?

**Then the design:**
~~~text
API → validate → queue (durable) → worker pool → provider → receipts webhook
~~~
- **Queue, not direct calls.** Provider outages are normal; a durable queue absorbs bursts and lets you retry without losing messages. This is the single most important decision.
- **Separate transactional and bulk traffic.** OTP traffic must never queue behind a 500k marketing blast. Two queues, two worker pools, priority for transactional.
- **Idempotency key per message** so a retry cannot double-send. A user receiving the same OTP twice is a bug; a user receiving the same marketing SMS twice is a complaint.
- **Provider abstraction with failover** — primary and secondary, with circuit breaking so a failing provider stops consuming workers.
- **Receipts are a separate async path.** Providers deliver them late and sometimes twice; treat them as events, keyed by message id, idempotently applied.
- **Store the message, not the rendering.** Keep the template and the parameters so you can re-render for audit and debugging.

**Scale numbers to state out loud:** 1M/day ≈ 12/second average, with peaks maybe 5× that. That is a small system. The interesting part is not throughput — it is **reliability, ordering, and not double-sending**. Saying that out loud is the senior signal.
:::

:::exercise 4 · Pricing a client project — A
**Task.** A Lagos retailer wants an inventory system with a POS frontend and a reporting dashboard. Quote it.

**Self-check.** Why is a day rate the wrong way to price this?

:::answer Show solution
Do not quote a day rate. A day rate prices your *time*, which is the one thing that does not scale and the one thing the client is trying to minimise. Price the **outcome**.

~~~text
SCOPE
  - Inventory master with barcode/QR scanning
  - POS frontend, offline-tolerant, single-store
  - Sales + stock reporting dashboard
  - Staff accounts with role-based access
  - 30 days post-launch support

PHASE 1 — Discovery & design (fixed, paid up front)      ₦350,000
  Schema, wireframes, technical plan. Deliverable: a
  document. If the client stops here, they keep the plan.

PHASE 2 — Build (fixed price, milestone-based)           ₦2,400,000
  M1: inventory + auth            ₦600,000
  M2: POS + offline sync          ₦900,000
  M3: dashboard + reports         ₦500,000
  M4: deploy + training + handover ₦400,000

PHASE 3 — Support retainer (monthly, optional)           ₦120,000/mo
  Bug fixes, hosting, minor changes. Cancel any time.

TOTAL PHASE 1+2: ₦2,750,000

TERMS
  - 50% on signature, 50% on final acceptance
  - Two rounds of revisions per milestone included
  - Out-of-scope work quoted separately, never absorbed
  - Source code and infrastructure transfer to client on
    final payment. Client owns everything.
~~~
Why this beats a day rate: it pays for your *judgment* rather than your hours, it rewards you for getting faster (a day rate punishes improvement), and it makes scope explicit so the "just one more small thing" conversation has a price instead of being an argument.

The clauses that matter most: **paid discovery** (filters out clients who will not commit), **milestone payments** (you are never more than one milestone underwater), and **code transfer on final payment** (the single most important protection you have — without it, you have no leverage if payment stops).
:::

:::exercise 5 · Salary negotiation — A
**Task.** A company offers ₦450,000/month for a mid-level role. You were hoping for ₦600,000. Negotiate.

**Self-check.** What is your leverage if you have no competing offer?

:::answer Show solution
~~~text
"Thank you - I'm excited about the role and the team. Before I
accept, I'd like to talk about the offer.

The responsibilities as we discussed them include owning the
payments integration end to end, which is the area I've shipped
in production twice. Based on that scope and on market rates
for this level, I was expecting something closer to ₦600,000.

Is there flexibility on the base, or would it help to look at
the total package - sign-on, or a review at six months instead
of twelve?"

Then stop talking. Let them respond.
~~~
The rules that make this work:

1. **Never give a number first.** If they ask your expectation early, say "I'd like to understand the scope first — what range did you have budgeted for this level?"
2. **Anchor to scope, not need.** "I need ₦600k for rent" is not a negotiation. "This role owns payments, which is the thing I have shipped twice" is.
3. **Negotiate the package, not just the number.** Sign-on, a six-month review, extra leave, equipment budget, and learning budget are all cheaper for the company than base salary and are often easier to approve.
4. **Your leverage without a competing offer is a credible walk-away.** It comes from having other options in progress — which is why you apply to many roles, not one. If you genuinely have no alternative, your leverage is the cost to them of re-running the search, which is real but smaller. Say so honestly and negotiate on scope instead.
5. **Get it in writing.** A verbal yes is not an offer.

And the meta-rule: **never accept on the call.** "I'm very interested — could you send the details in writing so I can review it properly?" buys you time and moves you from reactive to considered.
:::

:::exercise 6 · The Nigerian job search — B
**Task.** Build a 6-week application system targeting both Nigerian employers and remote roles.

**Self-check.** How many applications per week, and what makes you stop applying and start fixing something?

:::answer Show solution
~~~text
WEEKLY CADENCE
  Mon     Refresh CV/LinkedIn, update the tracker
  Tue-Thu 8-10 tailored applications (not mass-applied)
  Fri     2-3 outreach messages to engineers at target companies
  Sat     1 portfolio improvement shipped
  Sun     Review funnel metrics, adjust

THE TRACKER (a spreadsheet, one row per application)
  Company | Role | Source | Date applied | Stage | Next action | Date | Notes

FUNNEL BENCHMARKS (if you are below these, fix the input, not the volume)
  Applications → screening call:  15-25%
  Screening → technical:          40-60%
  Technical → offer:              20-33%

DIAGNOSTIC
  Low application → call rate?
    Your CV is not matching the role. Rewrite the top third
    around the specific job title and keywords.
  Good call rate, low technical rate?
    Your portfolio is under-selling you. Ship one more
    substantial project, or deepen the README of your best one.
  Good technical rate, no offers?
    Your interview communication is the gap. Do mock
    interviews out loud, recorded, weekly.
~~~
The counterintuitive insight: **volume is almost never the problem.** Most people at 50 applications with no calls do not need 100 applications — they need a different CV. Read the funnel, find the broken stage, fix that stage specifically.

And the highest-yield single activity is the Friday outreach message to an engineer at a target company. A referred candidate is interviewed at a dramatically higher rate than a cold applicant, and one thoughtful message to a stranger takes ten minutes.
:::

:::exercise 7 · Explaining a gap — I
**Task.** You spent 6 months in this bootcamp after 4 years in an unrelated field. Answer "why should we hire you over a CS graduate?"

**Self-check.** What is the *honest* advantage, stated without defensiveness?

:::answer Show solution
~~~text
"A CS graduate has four years of breadth - algorithms, systems,
theory. I have four years of [previous field] plus six months of
building and shipping production code, every week, with a public
record of it.

The specific advantage is that I have already solved problems in
[domain]. When you need someone who understands both the
engineering and how [logistics/payments/agriculture] actually
works, that combination is rare and hard to train. I can also
show you 12 shipped projects and a public write-up for every
lesson I learned - you can verify my thinking, not just take my
word for it.

Where I am weaker is computer science fundamentals. I am
actively closing that - I have worked through [specific
material] and I can tell you exactly what I do not know yet."
~~~
The three things that make this land:

1. **Do not apologise for the gap and do not over-compensate.** State it once, factually, and move to what you built.
2. **Name the domain advantage concretely.** "I understand how a Nigerian supply chain actually works" is worth more to a logistics company than another algorithms course.
3. **Admit a specific weakness with a specific plan.** Naming what you do not know is the strongest credibility signal available, because it proves you have an accurate model of your own competence — which is exactly what a senior engineer needs and what a bootcamp certificate cannot demonstrate.

The worst answer is a defensive one. The best is short, specific, and ends with a question about their actual problem.
:::

:::exercise 8 · The graduation artifact — B
**Task.** Produce the single document that summarises 26 weeks: one page, linked from everywhere.

**Self-check.** If this page were the only thing a stranger saw, would they book a call?

:::answer Show solution
The one-page structure:

~~~text
[Name] — Full-Stack Engineer / Analytics Engineer
One sentence on the outcome you produce, for whom.
Live at yourname.dev · GitHub · LinkedIn · hello@yourname.dev

WHAT I SHIPPED (3 items, each: name, one line, live URL, repo)
  1. [Flagship] — multi-tenant B2B SaaS, TypeScript/Next/Postgres
  2. [Sector project] — solves X for [industry], with real users/data
  3. [Public-good] — open-data analysis of [Nigerian dataset]

HOW I THINK (3 links to public write-ups)
  The three posts that best show your reasoning, not your tooling.

PROOF OF PRACTICE
  26 weeks, 48 lessons, ~150 public write-ups. Every claim
  above is verifiable in public repositories.

WHAT I AM LOOKING FOR
  One line. Specific beats broad.
```
The design principle: **the page is an argument, not a list.** Every element exists to support the claim in your opening sentence, and anything that does not is cut. Three projects, not ten. Three write-ups, not thirty.

And the final test is the one that matters: if a stranger read only this page, would they believe you can solve *their* problem? If not, the fix is almost never more content — it is a sharper claim and better proof for the claim you already made.
:::

:::ship The capstone bar
One flagship product you can discuss for an hour without notes, one sector product with a real user, one public-good analysis with published methodology, a one-page portfolio, a CV tailored per application, and a funnel you are actively managing. That is the complete package. Ship it before Week 26 ends.
:::
""",
)
