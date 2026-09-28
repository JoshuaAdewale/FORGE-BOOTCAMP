# -*- coding: utf-8 -*-
PAGES = []
G = "02 · Frontend (Wk 5–8)"

def page(**kw):
    kw.setdefault("group", G)
    PAGES.append(kw)

page(
    id="w5-react",
    title="W5 · React — The Mental Model",
    sub="Week 5, Day 1–3",
    eyebrow="WEEK 5 · FRONTEND",
    subtitle="React powers ~45% of professional frontend work. Learn the model, not the API surface.",
    chips=["18 hours", "Components · state · effects"],
    body=r"""
## The one idea

**UI is a pure function of state.** `view = f(state)`. You never touch the DOM; you change state and describe what the UI should look like for that state. React computes the difference and applies it. Everything else — hooks, keys, memoization — is machinery serving that idea.

You already built this by hand in Week 2. React is your reducer + render loop, optimized and generalized.

## Components and props

```
type Props = {
  title: string;
  amount: number;
  currency?: "NGN" | "USD";
  onSelect?: (id: string) => void;
  children?: React.ReactNode;
};

export function StatCard({ title, amount, currency = "NGN", children }: Props) {
  const formatted = new Intl.NumberFormat("en-NG", {
    style: "currency", currency, maximumFractionDigits: 0,
  }).format(amount);
  return (
    <div className="card">
      <h5>{title}</h5>
      <p className="value">{formatted}</p>
      {children}
    </div>
  );
}
```

Props flow **down**, events flow **up**. Components should be small, named for what they represent, and ideally pure.

## State: the rules that prevent 90% of React bugs

```
const [count, setCount] = useState(0);

// 1. Never mutate. Create new objects/arrays.
setItems([...items, newItem]);                       // add
setItems(items.filter(i => i.id !== id));            // remove
setItems(items.map(i => i.id === id ? { ...i, done: true } : i));  // update
setUser({ ...user, address: { ...user.address, city } });          // nested

// 2. Use the updater form when the new value depends on the old
setCount(c => c + 1);      // safe in batches, closures, async

// 3. State updates are asynchronous and batched
setCount(count + 1);
console.log(count);        // still the OLD value - this trips up everyone

// 4. Derive, do not duplicate. This is the biggest one.
const [items, setItems] = useState([]);
const total = items.reduce((s, i) => s + i.price, 0);   // computed, NOT state
const visible = items.filter(i => i.category === filter); // computed, NOT state
```

:::trap The #1 React beginner mistake
Storing derived data in state. If a value can be calculated from existing state or props, **calculate it during render**. Every piece of duplicated state is a bug waiting to happen (the two copies drift out of sync). Only store what you cannot derive.
:::

## Rendering, keys, and lists

```
{orders.map(order => <OrderRow key={order.id} order={order} />)}
```

`key` must be a **stable, unique ID** — never the array index if the list can reorder, filter, or have items inserted. Index keys cause wrong data appearing in wrong rows, lost input focus, and broken animations. This is a favorite interview question because it reveals whether you understand reconciliation.

## Effects: the escape hatch, not the tool

`useEffect` is for **synchronizing with systems outside React** — subscriptions, timers, browser APIs, analytics, non-React libraries. It is *not* for transforming data or responding to user events.

```
// CORRECT: subscribing to an external system, with cleanup
useEffect(() => {
  const ws = new WebSocket(url);
  ws.onmessage = e => setPrice(JSON.parse(e.data));
  return () => ws.close();          // cleanup prevents leaks and duplicate connections
}, [url]);

// WRONG: this should just be an event handler
useEffect(() => { if (submitted) sendAnalytics(); }, [submitted]);

// WRONG: derived state via effect - causes an extra render and can desync
useEffect(() => { setTotal(items.reduce(...)); }, [items]);   // just compute it inline
```

**The dependency array is not a suggestion.** Every reactive value used inside must be listed. If that causes an infinite loop, your design is wrong — move the function inside the effect, or use `useCallback`/`useRef` appropriately. Enable `eslint-plugin-react-hooks` and never silence it.

:::edge When you do NOT need an effect
Ask these in order: (1) Is it derived from props/state? → compute during render. (2) Does it happen in response to a user action? → put it in the event handler. (3) Does it fetch data? → use the framework's data layer or TanStack Query, not a raw effect. (4) Does it reset state when a prop changes? → use a `key` on the component instead. Only what remains needs `useEffect`. Senior React code has strikingly few effects.
:::

## The complete hook set (what each is actually for)

| Hook | Use it when |
|---|---|
| `useState` | Local, independent values |
| `useReducer` | Multiple values that change together / complex transitions |
| `useEffect` | Synchronizing with an external system |
| `useRef` | A mutable value that should NOT trigger re-render; DOM node access |
| `useMemo` | Caching an expensive computation (measure first) |
| `useCallback` | Stabilizing a function identity passed to memoized children |
| `useContext` | Reading values from a provider (theme, auth, locale) |
| `useId` | Generating stable IDs for label/input pairs (SSR-safe) |
| `useTransition` | Marking a state update as non-urgent to keep UI responsive |
| `useOptimistic` | Showing the expected result before the server confirms |

```
// useReducer shines for real forms and workflows
type Action =
  | { type: "field"; name: string; value: string }
  | { type: "submit" }
  | { type: "error"; errors: Record<string, string> }
  | { type: "success" };

function reducer(state: FormState, action: Action): FormState {
  switch (action.type) {
    case "field":   return { ...state, values: { ...state.values, [action.name]: action.value } };
    case "submit":  return { ...state, status: "submitting", errors: {} };
    case "error":   return { ...state, status: "idle", errors: action.errors };
    case "success": return { ...state, status: "done" };
  }
}
```

@@ Day 1 | Components, props, JSX, lists, conditional rendering, events. Rebuild your Week 3 UI in React.
@@ Day 2 | State, lifting state, useReducer, context, controlled inputs.
@@ Day 3 | Effects done right, custom hooks, refs, cleanup, StrictMode double-invocation.

```
// Custom hooks: extract stateful logic, name it for the behaviour
function useDebounced<T>(value: T, ms = 300): T {
  const [v, setV] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setV(value), ms);
    return () => clearTimeout(t);
  }, [value, ms]);
  return v;
}
```
""",
)

page(
    id="w5-next",
    title="W5 · Next.js App Router & Server Components",
    sub="Week 5, Day 4–6",
    eyebrow="WEEK 5 · FRONTEND",
    subtitle="The single most valuable frontend skill in 2026 — and the one most candidates fake.",
    chips=["18 hours", "RSC · routing · caching"],
    body=r"""
## Why this matters commercially

Recruiters report a recurring pattern: candidates list Next.js first on their CV but cannot explain the difference between server and client components under pressure. Being genuinely fluent here is a direct, immediate differentiator.

## The core distinction

**Server Components (default in App Router)** render on the server. They can query a database directly, read secrets, and send **zero JavaScript** to the browser. They cannot use state, effects, or browser APIs.

**Client Components (`"use client"`)** are what you know from classic React: state, effects, event handlers, browser APIs. They ship JS to the browser.

```
// app/dashboard/page.tsx  — a Server Component (no directive needed)
import { db } from "@/lib/db";
import { RevenueChart } from "./revenue-chart";

export default async function DashboardPage() {
  const rows = await db.query(                     // direct DB access, runs on server only
    "SELECT month, SUM(amount) AS revenue FROM sales GROUP BY month ORDER BY month"
  );
  return (
    <main>
      <h1>Revenue</h1>
      <RevenueChart data={rows} />   {/* interactive island */}
    </main>
  );
}
```

```
// app/dashboard/revenue-chart.tsx
"use client";
import { useState } from "react";
export function RevenueChart({ data }: { data: Row[] }) {
  const [view, setView] = useState<"bar" | "line">("bar");
  ...
}
```

**The architecture rule:** keep `"use client"` as *low in the tree as possible*. Fetch and compose on the server; make only the interactive leaves client components. This is what "islands architecture" means and it is why Next.js apps can be fast.

:::trap Server/client boundary rules
- A Server Component can render a Client Component, but **not the reverse** (except as `children` passed through).
- Props crossing the boundary must be **serializable** — no functions, class instances, or Dates-with-methods.
- The moment you add `"use client"`, everything it imports becomes client code too. Watch your bundle.
- Secrets are safe in Server Components but **any variable used in a Client Component can be read by users**. Only `NEXT_PUBLIC_*` env vars reach the browser — and assume everything there is public.
:::

## File-based routing

```
app/
  layout.tsx              # root layout, wraps everything (html/body)
  page.tsx                # /
  loading.tsx             # instant loading UI via Suspense
  error.tsx               # error boundary ("use client" required)
  not-found.tsx
  (marketing)/            # route group - organizes without affecting URL
    pricing/page.tsx      # /pricing
  dashboard/
    layout.tsx            # nested layout, persists across child navigations
    page.tsx              # /dashboard
    [projectId]/
      page.tsx            # /dashboard/123   -> params.projectId
      settings/page.tsx
  api/
    webhooks/route.ts     # route handler: GET/POST exports
```

```
// app/dashboard/[projectId]/page.tsx
export default async function Page({
  params, searchParams,
}: {
  params: Promise<{ projectId: string }>;
  searchParams: Promise<{ range?: string }>;
}) {
  const { projectId } = await params;         // async in Next 15+
  const { range = "30d" } = await searchParams;
  ...
}
```

## Data fetching and caching

```
// Static-ish: revalidate on an interval (ISR)
const res = await fetch(url, { next: { revalidate: 3600 } });

// Always fresh
const res = await fetch(url, { cache: "no-store" });

// Tag-based invalidation - the professional pattern
const res = await fetch(url, { next: { tags: ["projects"] } });
// ...later, after a mutation:
import { revalidateTag } from "next/cache";
revalidateTag("projects");
```

## Server Actions — mutations without writing an API

```
// app/actions.ts
"use server";
import { z } from "zod";
import { revalidatePath } from "next/cache";
import { auth } from "@/lib/auth";

const Schema = z.object({ name: z.string().min(2), budget: z.coerce.number().positive() });

export async function createProject(prev: State, formData: FormData): Promise<State> {
  const session = await auth();                          // ALWAYS re-check auth here
  if (!session) return { error: "Not authenticated" };

  const parsed = Schema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { fieldErrors: parsed.error.flatten().fieldErrors };

  await db.project.create({ data: { ...parsed.data, ownerId: session.userId } });
  revalidatePath("/dashboard");
  return { ok: true };
}
```

```
// app/dashboard/new-project-form.tsx
"use client";
import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { createProject } from "../actions";

function Submit() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? "Creating…" : "Create project"}</button>;
}

export function NewProjectForm() {
  const [state, action] = useActionState(createProject, {});
  return (
    <form action={action}>
      <label htmlFor="name">Name</label>
      <input id="name" name="name" required />
      {state.fieldErrors?.name && <p role="alert">{state.fieldErrors.name[0]}</p>}
      <Submit />
    </form>
  );
}
```

:::trap Server Actions are public HTTP endpoints
A Server Action is a POST endpoint that anyone can call directly, regardless of what your UI shows. **Authenticate and authorize inside every action.** Hiding a button is not access control. This is the single most common security hole in new Next.js codebases.
:::

## Streaming and Suspense

```
export default function Page() {
  return (
    <>
      <Header />                                 {/* instant */}
      <Suspense fallback={<StatsSkeleton />}>
        <SlowStats />                            {/* streams in when ready */}
      </Suspense>
      <Suspense fallback={<TableSkeleton />}>
        <SlowTable />
      </Suspense>
    </>
  );
}
```

Slow data no longer blocks the whole page. This is the modern answer to loading spinners and a major perceived-performance win.

## Other essentials

- **Metadata / SEO:** export `metadata` or `generateMetadata()`; add `sitemap.ts`, `robots.ts`, and Open Graph images (`opengraph-image.tsx`).
- **Middleware:** `middleware.ts` runs at the edge before requests — auth gating, redirects, A/B splits, locale routing.
- **Images:** `next/image` handles resizing, modern formats, and lazy loading. Always set `width`/`height` or `fill` to prevent layout shift.
- **Fonts:** `next/font` self-hosts and eliminates font-swap flashes.

:::ship Week 5 deliverable
Port the Market Price Tracker to Next.js App Router: server-rendered data, a client island for the interactive chart, a Server Action for the "submit a price" form (with Zod validation and revalidation), streaming with Suspense, dynamic routes per commodity, generated metadata and OG images. Deploy to Vercel. Then write "Server vs Client Components explained with a diagram" — this post alone will get you interviews.
:::
""",
)

page(
    id="w6-state",
    title="W6 · Data, Forms & Client State",
    sub="Week 6, Day 1–3",
    eyebrow="WEEK 6 · FRONTEND",
    subtitle="Where real apps get hard: server cache vs client state, complex forms, and optimistic UI.",
    chips=["18 hours", "TanStack Query · RHF · Zod"],
    body=r"""
## The distinction that organizes all frontend state

Most state confusion disappears once you separate these four categories:

| Category | Examples | Right tool |
|---|---|---|
| **Server cache** | Users, orders, products — data that lives in a DB | TanStack Query, or RSC + `revalidateTag` |
| **URL state** | Filters, page number, sort, search, tab | `searchParams` — shareable and back-button-safe |
| **Form state** | Field values, validation, submission | React Hook Form + Zod |
| **UI state** | Modal open, sidebar collapsed, theme | `useState` / Context / Zustand |

:::edge The judgment that marks a senior frontend dev
Putting server data into Redux/Zustand and hand-managing loading, errors, refetching, and staleness. That is thousands of lines of bug-prone code reimplementing a cache. Server data belongs in a **server-state library** (TanStack Query) or in **server components**. Global client stores should hold almost nothing. Say this in an interview and you will sound years ahead.
:::

## TanStack Query — the server-cache workhorse

```
const { data, isPending, isError, error, refetch } = useQuery({
  queryKey: ["orders", { status, page }],      // the cache key = dependency array
  queryFn: () => api.getOrders({ status, page }),
  staleTime: 60_000,                            // do not refetch for 60s
  placeholderData: keepPreviousData,            // no flash when paginating
});

// Mutations with optimistic update + rollback
const qc = useQueryClient();
const mutation = useMutation({
  mutationFn: (patch: OrderPatch) => api.updateOrder(patch),
  onMutate: async patch => {
    await qc.cancelQueries({ queryKey: ["orders"] });
    const prev = qc.getQueryData(["orders"]);
    qc.setQueryData(["orders"], (old: Order[]) =>
      old.map(o => (o.id === patch.id ? { ...o, ...patch } : o)));
    return { prev };                               // context for rollback
  },
  onError: (_e, _v, ctx) => qc.setQueryData(["orders"], ctx?.prev),
  onSettled: () => qc.invalidateQueries({ queryKey: ["orders"] }),
});
```

You get caching, deduplication, background refetch, retries, pagination, and offline handling — behavior users expect and hand-rolled code never fully delivers.

## Forms that do not fall apart

Real forms have: multi-step flows, conditional fields, async validation (is this email taken?), file uploads, array fields, autosave, and unsaved-changes warnings. Do not hand-roll this.

```
const Schema = z.object({
  businessName: z.string().min(2, "Required"),
  rcNumber: z.string().regex(/^RC\d{6,8}$/, "Format: RC1234567"),
  bvn: z.string().length(11, "BVN must be 11 digits"),
  monthlyRevenue: z.coerce.number().positive(),
  sector: z.enum(["agriculture", "retail", "logistics", "services"]),
  directors: z.array(z.object({
    name: z.string().min(2),
    share: z.coerce.number().min(0).max(100),
  })).min(1),
}).refine(d => d.directors.reduce((s, x) => s + x.share, 0) === 100,
          { message: "Shares must total 100%", path: ["directors"] });

type Form = z.infer<typeof Schema>;

const { register, handleSubmit, control, formState: { errors, isSubmitting } } =
  useForm<Form>({ resolver: zodResolver(Schema), mode: "onBlur" });
const { fields, append, remove } = useFieldArray({ control, name: "directors" });
```

**Accessible error handling** — most developers get this wrong:
```
<input
  id="bvn" {...register("bvn")}
  aria-invalid={!!errors.bvn}
  aria-describedby={errors.bvn ? "bvn-err" : undefined}
/>
{errors.bvn && <p id="bvn-err" role="alert">{errors.bvn.message}</p>}
```

## URL as state

```
"use client";
const router = useRouter(); const params = useSearchParams(); const pathname = usePathname();

function setFilter(key: string, value: string | null) {
  const p = new URLSearchParams(params);
  value ? p.set(key, value) : p.delete(key);
  p.delete("page");                                    // reset pagination on filter change
  router.push(`${pathname}?${p.toString()}`, { scroll: false });
}
```

Filters in the URL means users can bookmark, share, and use the back button. It is a small change that makes an app feel professional.

## Light global state, when you truly need it

```
import { create } from "zustand";
type UI = { sidebarOpen: boolean; toggle: () => void };
export const useUI = create<UI>(set => ({
  sidebarOpen: true,
  toggle: () => set(s => ({ sidebarOpen: !s.sidebarOpen })),
}));
```
That is the entire API. If your Zustand store starts filling up with server data, stop and reconsider.

:::drill Forms drill
Build a 4-step loan application wizard: business details → directors (dynamic array) → financials with computed debt-service ratio → document upload with drag-and-drop and progress. Requirements: state survives refresh (persist to sessionStorage), back/forward works via URL, per-step validation, async check on RC number, full keyboard accessibility, warning on navigating away with unsaved changes. This single component demonstrates more skill than five CRUD apps.
:::
""",
)

page(
    id="w6-ui",
    title="W6 · Design Systems & Component Craft",
    sub="Week 6, Day 4–6",
    eyebrow="WEEK 6 · FRONTEND",
    subtitle="Building an interface library that scales — Tailwind, shadcn/ui, tokens, and the composition patterns senior devs use.",
    chips=["18 hours", "Tailwind · Radix · tokens"],
    body=r"""
## Tailwind: why professionals adopted it

Utility classes eliminate the naming problem, keep styles co-located with markup, produce tiny CSS bundles (unused classes are purged), and enforce a design scale by default. The "it looks ugly in the markup" objection disappears once components encapsulate the classes.

```
// tailwind config as design tokens - your system's single source of truth
export default {
  theme: {
    extend: {
      colors: {
        brand: { 50:"#eefdf5", 500:"#3ddc97", 900:"#0d4a30" },
        surface: { DEFAULT:"#0b0f14", raised:"#141c27" },
      },
      spacing: { 18: "4.5rem" },
      borderRadius: { xl2: "1rem" },
      fontFamily: { sans: ["var(--font-inter)", "system-ui"] },
    },
  },
};
```

```
// A variant-driven component with cva - the professional pattern
import { cva, type VariantProps } from "class-variance-authority";

const button = cva(
  "inline-flex items-center justify-center rounded-lg font-medium transition-colors " +
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 " +
  "disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      intent: {
        primary:   "bg-brand-500 text-surface hover:bg-brand-600",
        secondary: "bg-surface-raised text-white border border-white/10 hover:bg-white/5",
        danger:    "bg-red-600 text-white hover:bg-red-700",
        ghost:     "hover:bg-white/5",
      },
      size: { sm: "h-8 px-3 text-sm", md: "h-10 px-4", lg: "h-12 px-6 text-lg" },
    },
    defaultVariants: { intent: "primary", size: "md" },
  }
);

export type ButtonProps = React.ComponentProps<"button"> & VariantProps<typeof button>;
export function Button({ className, intent, size, ...props }: ButtonProps) {
  return <button className={cn(button({ intent, size }), className)} {...props} />;
}
```

## shadcn/ui — the 2026 default

Not a dependency: a set of accessible components (built on **Radix UI** primitives) that you **copy into your repo** and own. You get correct focus management, keyboard interaction, and ARIA out of the box, with full freedom to restyle.

```
npx shadcn@latest init
npx shadcn@latest add button dialog dropdown-menu form table toast tabs command
```

Build these yourself at least once, though — a dialog with focus trap, a combobox with type-ahead and ARIA, a data table with sorting/filtering/pagination. Understanding what Radix does for you is what lets you debug it.

## Composition patterns worth knowing

```
// 1. Compound components - shared implicit state, flexible layout
<Tabs defaultValue="overview">
  <Tabs.List>
    <Tabs.Trigger value="overview">Overview</Tabs.Trigger>
    <Tabs.Trigger value="tx">Transactions</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Panel value="overview"><Overview /></Tabs.Panel>
</Tabs>

// 2. asChild / slot - render as any element without wrapper divs
<Button asChild><Link href="/pricing">See pricing</Link></Button>

// 3. Render props / headless hooks - logic without imposed markup
const { getRowProps, sortBy, rows } = useDataTable({ data, columns });

// 4. Polymorphic + forwardRef so libraries can attach to your components
export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  function Input(props, ref) { return <input ref={ref} {...props} />; }
);
```

## The component checklist (apply to every component you build)

1. Keyboard operable end to end; visible focus ring
2. Correct ARIA role/state; tested with a screen reader at least once
3. Loading, empty, error, and "too much data" states designed — not just the happy path
4. Responsive from 320px; touch targets ≥ 44px
5. Dark mode
6. `forwardRef` and `className` pass-through so it is composable
7. Documented in Storybook with all variants
8. Reduced-motion respected

:::edge Empty states and error states are a portfolio signal
Ninety percent of junior portfolios show only the happy path with perfect data. Design the empty state ("No transactions yet — here is how to add one"), the error state (with a retry action and a human explanation), the loading skeleton, and the overflow case (a name 200 characters long, an amount of ₦1,000,000,000). Reviewers notice this immediately because it is what real product work consists of.
:::

## Charts and data visualization in React

Use **Recharts** or **visx** for standard charts; **D3** when you need something custom. Rules for charts that actually communicate: label axes with units, start bar-chart y-axes at zero, use color meaningfully, add a text summary for screen readers, and always handle the "no data" case.

:::ship Week 6 deliverable
Publish `@yourname/ui` — a component library with Button, Input, Select, Combobox, Dialog, Drawer, Table (sortable/filterable/paginated), Toast, Tabs, Card, Skeleton, and EmptyState. Requirements: TypeScript, variants via cva, dark mode, full a11y, Storybook deployed publicly, and a documentation site. This is portfolio piece #2 and it is unusually impressive for a self-taught developer.
:::
""",
)

page(
    id="w7-perf",
    title="W7 · Performance, Testing & Quality",
    sub="Week 7",
    eyebrow="WEEK 7 · FRONTEND",
    subtitle="The engineering discipline layer: measuring, optimizing, and proving your UI works.",
    chips=["35 hours", "Core Web Vitals · Vitest · Playwright"],
    body=r"""
## Performance: measure, then optimize

The metrics Google and users care about (Core Web Vitals):

| Metric | Measures | Good |
|---|---|---|
| **LCP** Largest Contentful Paint | Loading — when the main content appears | < 2.5s |
| **INP** Interaction to Next Paint | Responsiveness — replaced FID in 2024 | < 200ms |
| **CLS** Cumulative Layout Shift | Visual stability — things jumping around | < 0.1 |
| **TTFB** | Server response time | < 800ms |

**In a market like Nigeria this is not cosmetic.** Users on 3G with metered data and mid-range Android devices will abandon a 4 MB bundle. Building fast is a competitive and commercial advantage, and it is a genuinely differentiating skill to demonstrate.

### The optimization playbook, in order of impact

1. **Ship less JavaScript.** Server components, dynamic `import()`, remove heavy dependencies. Check with `@next/bundle-analyzer`. Moment.js → `Intl`. Lodash → native. A charting library → an SVG you draw.
2. **Optimize images.** Usually 60–80% of page weight. Modern formats (AVIF/WebP), correct dimensions, lazy-load below the fold, `priority` on the LCP image, always set width/height.
3. **Fix the critical path.** Preconnect to third-party origins, `next/font` for fonts, inline critical CSS, defer non-essential scripts.
4. **Cache aggressively.** CDN, ISR, `stale-while-revalidate`, immutable hashed assets.
5. **Then micro-optimize React.** `memo`, `useMemo`, virtualization for long lists (`@tanstack/react-virtual`), `useTransition` for expensive updates.

:::trap Premature memoization
Wrapping everything in `useMemo`/`memo` adds complexity and its own cost. Profile first with React DevTools Profiler. Most re-renders are cheap. Optimize the ones that measurably are not — usually large lists, charts, and heavy computations. "I profiled and found X" is a sentence that gets people hired.
:::

```
// Virtualize long lists - 10,000 rows rendering only ~20 DOM nodes
const parentRef = useRef<HTMLDivElement>(null);
const v = useVirtualizer({ count: rows.length, getScrollElement: () => parentRef.current, estimateSize: () => 44, overscan: 8 });
```

## Testing: the pyramid that fits real projects

++ Unit (many, fast) :: Pure functions, business logic, utilities, reducers. Vitest. Milliseconds.
++ Component (a good number) :: React Testing Library. Test what the user sees and does, never internal state.
++ Integration (some) :: Multiple components + mocked network via MSW. The best value-per-test.
++ E2E (few, critical paths only) :: Playwright. Signup, login, checkout, the one flow that loses money if broken.

```
// Component test - notice it queries the way a user perceives the UI
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("shows validation error for invalid BVN", async () => {
  const user = userEvent.setup();
  render(<LoanForm />);
  await user.type(screen.getByLabelText(/bvn/i), "123");
  await user.click(screen.getByRole("button", { name: /continue/i }));
  expect(await screen.findByRole("alert")).toHaveTextContent(/11 digits/i);
});
```

```
// Mock the network, not your own modules
import { http, HttpResponse } from "msw";
export const handlers = [
  http.get("/api/orders", () => HttpResponse.json([{ id: "1", amount: 5000 }])),
  http.post("/api/orders", () => new HttpResponse(null, { status: 500 })),  // test the error path!
];
```

```
// E2E: the money path
test("user can complete checkout", async ({ page }) => {
  await page.goto("/products/rice-50kg");
  await page.getByRole("button", { name: "Add to cart" }).click();
  await page.getByRole("link", { name: "Cart" }).click();
  await page.getByLabel("Delivery address").fill("12 Zoo Road, Kano");
  await page.getByRole("button", { name: "Pay" }).click();
  await expect(page.getByText(/order confirmed/i)).toBeVisible();
});
```

:::edge What to test (the rule that saves time)
Test **behavior and contracts**, not implementation. If a refactor that changes no user-visible behavior breaks your tests, your tests are wrong. Prioritize: money paths, auth, data integrity, anything that has broken before, and complex pure logic. Do not chase 100% coverage — chase confidence in the paths that matter. Also add accessibility assertions with `axe-core` in your component tests; it catches real bugs and signals maturity.
:::

## Quality automation

```
# The standard professional setup
pnpm add -D eslint prettier typescript vitest @testing-library/react playwright husky lint-staged @axe-core/playwright
npx husky init
echo "pnpm lint-staged" > .husky/pre-commit
```

Pre-commit: format + lint changed files. Pre-push or CI: typecheck, unit tests, build. **Never let broken code reach `main`.**

:::ship Week 7 deliverable
Take your Week 6 component library and Week 5 app to production quality: ≥ 80% coverage on logic, component tests for every interactive component, 3 Playwright E2E flows, Lighthouse ≥ 95 on mobile, bundle under budget with a documented before/after, and a CI pipeline that blocks merges on failure. Write "How I cut my bundle 62%" with real numbers — performance write-ups get read and shared.
:::
""",
)

page(
    id="w8-project",
    title="W8 · Frontend Capstone",
    sub="Week 8",
    eyebrow="WEEK 8 · FRONTEND",
    subtitle="One large, realistic frontend built to professional standards. This is the piece you will show for frontend roles.",
    chips=["35 hours", "Portfolio piece #3"],
    body=r"""
## Choose one brief (pick the sector closest to work you want)

### Brief A — "Clinic OS" (health tech)
A patient-management frontend for a small Nigerian private clinic. Patient registry with search; appointment calendar with drag-to-reschedule; consultation notes with autosave; prescription builder with drug-interaction warnings; a billing module with NHIS/HMO vs cash split; and an analytics tab showing patient volume, top diagnoses, and revenue. Must work on a tablet, tolerate intermittent connectivity (offline queue for notes), and be usable one-handed.

### Brief B — "Fleet Command" (logistics)
Dispatch and tracking for a haulage company. Live map with vehicle positions (mock WebSocket feed); job assignment with driver availability; route cost calculator including fuel, tolls, and driver allowance; delivery proof upload; SLA breach alerts; and a dashboard for on-time rate, cost per km, and idle time. Must handle 200 vehicles updating every 5 seconds without dropping frames.

### Brief C — "Agri Yield" (agriculture)
Farm management for a cooperative. Plot registry with map polygons; input tracking (seed, fertilizer, labour cost per plot); a weather feed with a spray-window advisory; a harvest log; a yield-per-hectare comparison across plots and seasons; and a market-price feed linking to your Week 3 tracker. Must work offline in the field and sync when back online.

### Brief D — "Cash Ledger" (fintech / SME)
Bookkeeping for informal traders. Multi-currency transaction entry; a customer credit ledger ("book") with reminders; inventory with low-stock alerts; profit calculation per product; a cash-flow projection; and a WhatsApp-shareable statement. Must be usable by someone with limited formal education — extreme clarity, minimal text, iconography, Hausa/Yoruba/Igbo toggle.

## Non-negotiable requirements

- **Next.js App Router + TypeScript strict.** Server components for data, client islands for interactivity.
- **Real data layer.** Mock API with MSW or a small JSON server; TanStack Query or RSC caching; realistic latency and failure injection.
- **Every state designed:** loading skeletons, empty states, error states with retry, offline banner, permission-denied.
- **Full accessibility:** keyboard-only walkthrough recorded as a video; axe clean; screen-reader labels on all interactive elements.
- **Performance:** Lighthouse mobile ≥ 95; LCP < 2s on simulated 3G; bundle budget documented.
- **Tests:** unit for logic, component for interactions, 3+ Playwright E2E flows, all running in CI.
- **Polish:** dark mode, responsive 320px → 4K, meaningful animation (respecting reduced-motion), real content not lorem ipsum.
- **Deployed** with a custom domain and a README containing: problem statement, screenshots/GIF, architecture diagram, key decisions and trade-offs, and known limitations.

## How to run the week like a professional

@@ Day 1 | Requirements + user flows + wireframes (paper is fine) + data model + component inventory. Do NOT open an editor before this exists.
@@ Day 2 | Scaffold, design tokens, layout shell, routing, mock API contracts.
@@ Day 3 | Core feature vertical slice — one complete flow end to end before starting a second.
@@ Day 4 | Remaining features, all UI states.
@@ Day 5 | Accessibility pass, performance pass, tests.
@@ Day 6 | Deploy, README, demo video (3 minutes, narrated), public post.

:::edge Make the README do the selling
Hiring managers spend 90 seconds on your repo. Your README should open with a one-sentence problem statement, an animated GIF of the app working, a live link, then the architecture and decisions. Include a short **"Trade-offs I made"** section — e.g. "I chose optimistic updates for note-saving because clinics have unstable internet; the cost is reconciliation complexity, handled in `sync.ts`." That one paragraph tells a reviewer more about your seniority than the entire codebase.
:::

:::ship Phase 2 exit criteria
You can: build any interface from a design, choose the correct rendering strategy per route, manage server vs client state correctly, make it accessible and fast, test it meaningfully, and deploy it. You now have three portfolio pieces and roughly 40 public write-ups. That is already stronger than most bootcamp graduates. Next: the backend, where the real engineering depth lives.
:::
""",
)
