# FORGE — Full-Stack & Data Bootcamp (26 weeks)

An interactive, self-paced bootcamp site: **67 pages, 68 graded exercises with
answer keys, ~470,000 characters of curriculum, 60 real-world sector problem
briefs, a full income track, and a global track**, offline support, and progress
tracking with backup/restore.

## Run it

```bash
python3 -m http.server 8080 --directory .
# open http://localhost:8080
```

No build step, no dependencies, no framework. Progress is saved to browser
`localStorage`.

## What's in the app

| Feature | Where |
|---|---|
| 56 lessons across 10 sidebar groups | `data/*.js` |
| Full-text search across every lesson | press `/` anywhere to focus |
| Progress tracking with % complete | sidebar, auto-advances to next lesson |
| **Save backup / Restore** | sidebar footer — export progress to JSON, restore later |
| **Works offline** | service worker precaches everything; installable as a PWA |
| **Copy button on every code block** | hover any code block |
| Print / Save as PDF | sidebar footer |
| Keyboard shortcuts | `/` search, `Esc` close sidebar |
| Accessibility | skip link, focus rings, `aria-current`, reduced-motion support |

## Structure

```
index.html          app shell
css/style.css       styling (dark, print-friendly, accessible)
js/md.js            markdown renderer (callouts, cards, day plans, tables,
                    collapsible answers, exercise blocks)
js/app.js           router, search, progress, backup/restore, offline
sw.js               service worker (offline support)
data/*.js           compiled curriculum (7 bundles)
_src/               Python source for the curriculum + build.py
```

## Editing the curriculum

Edit the `_src/pages_*.py` files, then:

```bash
cd _src && python3 build.py
```

Refresh the browser. If you add a new source module, register it in the
`BUNDLES` list in `build.py` **and** add a `<script>` tag in `index.html`.

### Authoring syntax

Page bodies are raw strings (`r"""..."""`). Supported blocks:

| Syntax | Renders as |
|---|---|
| ` ```lang ... ``` ` | code block with copy button |
| `:::edge Title ... :::` | green callout (insight) |
| `:::trap Title ... :::` | red callout (mistake to avoid) |
| `:::ship Title ... :::` | blue callout (deliverable) |
| `:::drill Title ... :::` | amber callout (practice) |
| `:::exercise Title ... :::` | bordered exercise block |
| `:::answer Title ... :::` | collapsible `<details>` solution |
| `++ Title :: body` | card grid |
| `@@ Day N \| text` | day-plan rows |
| `\| a \| b \|` + `\|---\|---\|` | table |

> **Rule:** never use `"""` inside a page body — it terminates the raw string.
> Use `'''` or `#` comments in code samples. Use `~~~` in source; `build.py`
> converts it to ` ``` `.

## Phases

| Phase | Weeks | Focus |
|---|---|---|
| 0 | Wk 0 | Environment setup + learning method |
| 1 | 1–4 | Foundations: shell, git, web, HTML/CSS, JS, TS, CS, Python/SQL |
| 2 | 5–8 | Frontend: React, Next.js App Router, state, design systems, perf, testing |
| 3 | 9–13 | Backend: Node APIs, PostgreSQL, advanced SQL, auth/security, payments, queues, FastAPI |
| 4 | 14–16 | Production: Docker, CI/CD, observability, system design |
| 5 | 17–18 | AI engineering: LLM apps, RAG, evals |
| 6 | 19–24 | Data analysis: metrics, pandas/Polars, statistics, dbt, BI, ML |
| 7 | — | 60 sector problem briefs across 10 industries |
| 8 | 25–26 | Capstone, portfolio, interviews, freelancing, job search |
| 9 | — | Exercise bank: 68 graded problems with answer keys |
| 10 | — | Income track: what to sell week by week, first client, pricing, delivery |
| 11 | — | Global track: the 0.1% path, professional English, USD rails, world market, public proof |

## Deployment

See [DEPLOY.md](DEPLOY.md). The site is 100% static — drag the folder to
[app.netlify.com/drop](https://app.netlify.com/drop), or connect a GitHub repo
for auto-deploy on push.

## Tests

```bash
node /tmp/domtest/run.js    # DOM behaviour (30 assertions)
node /tmp/domtest/income.js  # income track (8 assertions)
node /tmp/domtest/global.js  # global track (21 assertions)
node /tmp/domtest/run2.js   # progress backup/restore round-trip (9 assertions)
node /tmp/domtest/act.js    # service worker cache lifecycle
```
