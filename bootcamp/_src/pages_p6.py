# -*- coding: utf-8 -*-
PAGES = []
G = "06 · Data Analysis (Wk 19–24)"

def page(**kw):
    kw.setdefault("group", G)
    PAGES.append(kw)

page(
    id="w19-thinking",
    title="W19 · Analytical Thinking & Metric Design",
    sub="Week 19, Day 1–3",
    eyebrow="WEEK 19 · DATA",
    subtitle="The part almost every analyst skips, and the reason most dashboards are ignored.",
    chips=["18 hours", "Metrics · framing · judgment"],
    body=r"""
## The job is not making charts

An analyst's product is a **decision**, not a dashboard. The distinction between a $40k analyst and a $140k analyst is almost never tooling — it is the ability to take a vague business question, sharpen it, answer it defensibly, and drive an action.

## From question to answer: the discipline

A stakeholder says: *"Sales are down. Can you look into it?"* An amateur opens a BI tool. A professional runs this sequence:

1. **Clarify the actual question.** Down versus what — last month, last year, plan? Which segment? Since when? What decision will you make with the answer? What would you do differently if the answer were A versus B? *(If no decision depends on it, deprioritize the request — politely.)*
2. **State the hypotheses before looking.** Fewer customers? Same customers buying less? Price change? A channel broke? Seasonality? Competitor entry? A data pipeline failure? Write them down — this prevents you from finding a story in noise.
3. **Decompose the metric.** `Revenue = Users × Conversion × Orders per converted user × Average order value`. Now you can locate *which factor* moved. Nearly every business metric decomposes like this, and the decomposition is the analysis.
4. **Check the data before trusting it.** Row counts by day, nulls, duplicates, a sudden schema change, a tracking release. A shocking number of "business crises" are broken instrumentation.
5. **Segment.** An aggregate is an average of different stories. Split by geography, channel, cohort, device, customer tier, new versus returning. The insight is almost always in a segment.
6. **Quantify and size.** "Conversion fell 4 points in the USSD channel, which is 62% of the total decline, worth ₦18M/month."
7. **Recommend, with a confidence level and a next step.**

:::edge The question behind the question
Stakeholders ask for outputs; they need outcomes. "Can you pull a list of churned customers?" usually means "we want to reduce churn." Give them the list *and* the analysis of who churns and why, and you become a partner rather than a query service. Always ask: **"What decision will this inform?"** It is the most valuable sentence in an analyst's vocabulary, and asking it in an interview case study is an instant credibility signal.
:::

## Metric design

**A good metric is:** actionable (a team can move it), comparable over time, hard to game, sensitive enough to detect real change, and clearly defined so two people compute it identically.

| Type | Purpose | Example |
|---|---|---|
| **North Star** | The one number reflecting delivered value | Weekly active paying merchants |
| **Input metrics** | Drivers you can directly influence | Signups, activation rate, time-to-first-transaction |
| **Output metrics** | Results | Revenue, retention, NPS |
| **Guardrail metrics** | What must not break while optimizing | Support tickets, refund rate, latency, fraud rate |
| **Counter-metrics** | Detect gaming | Push notifications sent vs unsubscribes |

**Definitions must be written down.** "Active user" — active in the last 7 days? Any event, or a meaningful one? Do internal accounts count? Is a bot excluded? Two teams with different definitions produce two different numbers and destroy trust in analytics. Maintain a **metrics dictionary** with the definition, SQL, owner, and known caveats for every metric. Doing this unprompted marks you as senior.

:::trap The metrics traps that mislead executives
- **Averages hide everything.** Report medians and percentiles too; one whale distorts a mean.
- **Vanity metrics.** Total registered users only ever goes up. Track actives and retention.
- **Survivorship bias.** Analyzing only current customers to understand churn.
- **Simpson's paradox.** A trend in every segment can reverse in the aggregate when segment mixes change. Always check whether a change is mix-shift.
- **Correlation as causation.** Ice cream and drowning. Ask what the confounder is, every time.
- **Ratio without denominator context.** "Conversion doubled!" from 1 to 2 out of 3 visitors.
- **Cherry-picked windows.** Always show enough history to see the trend and the seasonality.
:::

## The frameworks worth memorizing

- **AARRR (pirate metrics):** Acquisition → Activation → Retention → Revenue → Referral. A funnel for any product.
- **Unit economics:** CAC, LTV, LTV/CAC (aim > 3), payback period, contribution margin, gross margin. Learn to compute these from raw data — it makes you useful to founders and finance immediately.
- **Cohort analysis:** never judge retention on a blended number; always by acquisition cohort.
- **RFM segmentation:** Recency, Frequency, Monetary — a simple, powerful customer segmentation you can build in one SQL query.
- **Funnel + drop-off:** where do people leave, and what is each step worth?

## Communicating to executives

**Lead with the answer.** The Pyramid Principle: conclusion first, then the three supporting reasons, then the detail for anyone who wants it. Never build up to a reveal — executives read the first sentence and the chart title.

A good analysis memo has: **the recommendation (1 sentence)** → **the evidence (3 bullets with numbers)** → **the size of the opportunity or risk in money** → **what you propose to do next and by when** → **caveats and confidence** → appendix with methodology and SQL.

:::drill Analytical framing drill
Take five vague requests: "How is the business doing?", "Should we open a Kano branch?", "Is our marketing working?", "Why are customers complaining?", "Can we raise prices?" For each, write: the sharpened question, the decision it informs, the hypotheses, the data you would need, the analysis plan, and the failure mode of the analysis. Do not write a single query. **This exercise is worth more than a week of SQL practice** — and case interviews for analyst roles test exactly this.
:::
""",
)

page(
    id="w19-pandas",
    title="W19 · pandas, Polars & Data Wrangling",
    sub="Week 19, Day 4–6",
    eyebrow="WEEK 19 · DATA",
    subtitle="Real data is filthy. Cleaning it correctly, reproducibly, and without silently corrupting it is most of the job.",
    chips=["18 hours", "pandas · Polars · cleaning"],
    body=r"""
## The reality

Analysts spend 60–80% of their time acquiring and cleaning data. The people who are fast and *rigorous* here produce trustworthy numbers; everyone else produces confident wrong answers.

## pandas essentials, professionally

```
import pandas as pd, numpy as np

df = pd.read_csv("transactions.csv",
    dtype={"customer_id": "string", "channel": "category"},
    parse_dates=["created_at"],
    na_values=["", "NA", "N/A", "null", "-", "#N/A"])

# ALWAYS profile before analyzing
df.info(memory_usage="deep")
df.describe(include="all").T
df.isna().mean().sort_values(ascending=False)      # missingness by column
df.duplicated(subset=["reference"]).sum()
df.nunique()
```

```
# Method chaining with assign/pipe - readable, no SettingWithCopyWarning
clean = (
    df
    .pipe(lambda d: d[d["status"].isin(["completed", "settled"])])
    .assign(
        amount_ngn = lambda d: d["amount_kobo"] / 100,
        month      = lambda d: d["created_at"].dt.to_period("M"),
        is_new     = lambda d: d.groupby("customer_id")["created_at"].transform("min").eq(d["created_at"]),
    )
    .drop_duplicates(subset=["reference"], keep="last")
    .reset_index(drop=True)
)

# Grouped aggregation with named outputs
summary = (
    clean.groupby(["month", "channel"], observed=True)
         .agg(revenue=("amount_ngn", "sum"),
              orders=("reference", "count"),
              customers=("customer_id", "nunique"),
              median_ticket=("amount_ngn", "median"))
         .reset_index()
         .assign(revenue_per_customer=lambda d: d.revenue / d.customers)
)

# Window-style operations
clean["running_total"] = clean.sort_values("created_at").groupby("customer_id")["amount_ngn"].cumsum()
clean["days_since_prev"] = clean.groupby("customer_id")["created_at"].diff().dt.days
summary["mom_growth"] = summary.groupby("channel")["revenue"].pct_change()

# Joins - and ALWAYS validate the cardinality
merged = clean.merge(customers, on="customer_id", how="left",
                     validate="many_to_one", indicator=True)
print(merged["_merge"].value_counts())     # catch unmatched rows instead of losing them silently
```

:::trap The pandas mistakes that produce wrong numbers
1. **Chained assignment** (`df[df.x > 1]["y"] = 5`) may silently do nothing. Use `.loc[mask, "y"] = 5`.
2. **Merging without `validate=`** — an unintended one-to-many join duplicates rows and inflates every sum. This is the most common cause of wrong revenue figures in the wild.
3. **`inplace=True`** — inconsistent, hurts chaining, being deprecated. Avoid it.
4. **Silent dtype coercion** — an ID column read as float becomes `1.0`, breaking joins. Set dtypes explicitly.
5. **Dropping NaN without thinking.** Missing is information: is it missing at random, or does missingness itself mean something (e.g. no delivery date = not delivered)?
6. **Ignoring timezones.** Mixing naive and aware datetimes produces off-by-hours errors in daily aggregates. Store UTC, convert to Africa/Lagos only for display.
:::

## Polars, for when pandas struggles

```
import polars as pl
q = (pl.scan_parquet("events/*.parquet")           # lazy: nothing loaded yet
       .filter(pl.col("event") == "purchase")
       .group_by_dynamic("ts", every="1d", group_by="channel")
       .agg([pl.col("amount").sum().alias("revenue"),
             pl.col("user_id").n_unique().alias("users")])
       .with_columns((pl.col("revenue") / pl.col("users")).alias("arpu")))
df = q.collect(streaming=True)                     # handles data larger than RAM
```

Polars is multi-threaded, has a query optimizer, and is typically several times faster than pandas with lower memory use. Learn pandas (ubiquitous, every job mentions it) and Polars (where the field is moving, and impressive to demonstrate).

## The cleaning checklist — run this on every dataset

1. **Shape and grain.** What does one row represent? State it explicitly. Half of all analytical errors come from confusion about grain.
2. **Uniqueness.** Is the key actually unique? Test it.
3. **Missingness.** Count per column; understand *why*; decide drop / impute / flag — and document which.
4. **Types.** Dates as dates, IDs as strings, categories as category. Never money as float.
5. **Ranges.** Negative quantities? Future dates? Ages of 200? Amounts of ₦0? Investigate before removing.
6. **Duplicates.** Exact and fuzzy (same customer with two spellings of a name).
7. **Consistency.** "Lagos", "lagos", "LAG", "Lagos State" are one place. Normalize with a mapping table.
8. **Outliers.** Look at them individually. They are often either the most interesting data or a data-entry bug — never blindly clip.
9. **Referential integrity.** Do all foreign keys resolve?
10. **Reconcile to a known truth.** Does your revenue total match finance's number? If not, find out why *before* presenting anything.

```
# Encode the checks as assertions so a broken pipeline fails loudly
assert clean["reference"].is_unique, "duplicate references"
assert clean["amount_ngn"].ge(0).all(), "negative amounts"
assert clean["created_at"].max() <= pd.Timestamp.now(tz="UTC"), "future timestamps"
assert clean["customer_id"].isin(customers["id"]).all(), "orphan customers"
```

Better: use **Great Expectations** or **pandera** to declare a schema with constraints and validate every run. Silent data corruption is the worst failure mode in analytics because nobody notices until a decision has been made on it.

:::drill The dirty data gauntlet
Find the messiest public dataset you can (Nigerian government open data, an NGO survey export, or a scraped e-commerce set). Clean it to analysis-ready state in a documented notebook: every decision justified in markdown, every assumption stated, assertions at each stage, and a "data quality report" summarizing what was wrong and what you did. **This notebook is a stronger portfolio item than three tutorial dashboards** — it shows judgment, which is what employers actually screen for.
:::
""",
)

page(
    id="w20-stats",
    title="W20 · Statistics & Experimentation",
    sub="Week 20",
    eyebrow="WEEK 20 · DATA",
    subtitle="Enough statistics to be right — and to know when you cannot be sure.",
    chips=["35 hours", "Inference · A/B testing · causality"],
    body=r"""
## Descriptive statistics, correctly

- **Center:** mean (sensitive to outliers), median (robust — usually the right default for money and durations), mode.
- **Spread:** standard deviation, IQR, range. *Always report spread with center.* "Average order ₦12,000" is meaningless without knowing whether the IQR is ₦11k–₦13k or ₦500–₦95k.
- **Shape:** skew and kurtosis. Business data is usually right-skewed (a few large values), which is precisely why the mean misleads.
- **Percentiles.** p50/p90/p95/p99 for latency, order values, session length. Executives understand "90% of customers wait less than X."
- **Distributions:** normal (heights, measurement error), log-normal (income, order values), Poisson (counts per interval), binomial (conversions), power law (network effects, city sizes, wealth).

## Inference: from sample to population

**Sampling error** is why you cannot trust a single number. A confidence interval quantifies it.

```
from scipy import stats
import numpy as np

# 95% CI for a mean
ci = stats.t.interval(0.95, len(x)-1, loc=np.mean(x), scale=stats.sem(x))

# 95% CI for a conversion rate (Wilson - correct for small samples and extreme rates)
from statsmodels.stats.proportion import proportion_confint
lo, hi = proportion_confint(count=successes, nobs=trials, method="wilson")
```

**Hypothesis testing in plain language:** assume nothing is happening (null hypothesis); calculate how surprising your data would be under that assumption (the p-value); if sufficiently surprising, reject it.

:::trap What a p-value is NOT
It is **not** the probability the hypothesis is true. It is **not** the probability the result was chance. It is: the probability of observing data at least this extreme *if the null hypothesis were true*. And **statistical significance is not business significance** — with 5 million users you can detect a 0.01% lift that is worth nothing. Always report the **effect size and its confidence interval**, not just "p < 0.05". Interviewers ask this precisely to see who memorized versus who understands.
:::

**Which test, when:**

| Situation | Test |
|---|---|
| Two group means, continuous | t-test (Welch's by default) |
| Two conversion rates | z-test for proportions, or chi-square |
| More than two groups | ANOVA, then post-hoc with correction |
| Non-normal / small samples | Mann-Whitney U, or bootstrap |
| Categorical association | Chi-square test of independence |
| Anything you cannot find a formula for | **Bootstrap it** — resample with replacement 10,000 times |

```
# Bootstrap: intuitive, assumption-light, works for medians, ratios, anything
boot = np.array([np.median(np.random.choice(x, len(x), replace=True)) for _ in range(10_000)])
print(np.percentile(boot, [2.5, 97.5]))
```

## A/B testing end to end

Experimentation ability is explicitly called out as a skill that raises analyst compensation. Own the whole cycle:

1. **Hypothesis:** "Showing bank-transfer as the default payment option will increase checkout completion for USSD-origin users, because card failure rates are high in that segment."
2. **Choose the metric** (primary: checkout completion rate) **and guardrails** (refund rate, support tickets, average order value).
3. **Power analysis — before running.** How many users do you need to detect the smallest effect worth acting on?

```
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize
n = NormalIndPower().solve_power(
      effect_size=proportion_effectsize(0.10, 0.115),   # 10% -> 11.5% (MDE)
      alpha=0.05, power=0.8, ratio=1)
print(f"{n:,.0f} users per arm")
```

4. **Randomize properly** at the right unit (user, not session, if the experience persists). Check that the split is actually 50/50 — a **sample ratio mismatch** invalidates the test and usually indicates a bug.
5. **Run for full weekly cycles** (behavior differs by weekday) and a pre-committed duration.
6. **Analyze once, at the end.** Report the lift, the CI, and the guardrails.
7. **Decide:** ship, iterate, or abandon. Document it either way — a well-documented negative result saves the company money.

:::trap The five ways A/B tests lie
1. **Peeking.** Checking daily and stopping when significant massively inflates false positives. Use sequential testing methods if you must monitor.
2. **Multiple comparisons.** Testing 20 metrics guarantees one "significant" result by chance. Correct for it (Bonferroni, or pre-register a single primary metric).
3. **Sample ratio mismatch.** 52/48 split is a red flag; investigate before believing anything.
4. **Novelty and primacy effects.** Users react to change itself. Short tests overestimate; check whether the effect persists.
5. **Simpson's paradox / segment mix shifts.** Always check whether the result holds across major segments.
:::

## Causality without experiments

Often you cannot randomize. Then you need quasi-experimental methods — and knowing these is unusual and valuable in an analyst:

- **Difference-in-differences:** compare the change in a treated group to the change in an untreated one (e.g. a feature launched in Lagos but not Kano). Requires the parallel-trends assumption.
- **Regression discontinuity:** a threshold rule (customers above ₦50k get a discount) creates a natural experiment at the cutoff.
- **Propensity score matching:** construct a comparable control group from observables.
- **Instrumental variables / synthetic control:** advanced, but know the names and the idea.
- **The absolute basics of confounding:** always ask "what third thing could cause both?" Draw a causal diagram before running a regression.

## Regression as an analytical tool

```
import statsmodels.formula.api as smf
m = smf.ols("np.log(revenue) ~ C(channel) + months_active + C(region) + promo", data=df).fit()
print(m.summary())
```

Interpret coefficients (with a log outcome, a coefficient ≈ a percentage effect), check the assumptions (linearity, independence, homoscedasticity, normal residuals), watch for multicollinearity, and **never present a coefficient as causal from observational data** without saying so. Logistic regression for binary outcomes — interpret odds ratios carefully.

:::ship Week 20 deliverable
Two artifacts. **(1)** A complete experiment analysis on a public dataset: hypothesis, power calculation, results with CIs, segment analysis, guardrails, and a one-page recommendation memo written for an executive. **(2)** A "statistics for business decisions" explainer post covering p-values, confidence intervals, and effect size in plain English with real examples. The second one, done well, gets shared widely and demonstrates the communication skill employers say is the most underestimated.
:::
""",
)

page(
    id="w21-ae",
    title="W21 · Analytics Engineering (dbt & Warehousing)",
    sub="Week 21",
    eyebrow="WEEK 21 · DATA",
    subtitle="The highest-paid analytics specialization: turning raw data into a trustworthy, documented, tested modeling layer.",
    chips=["35 hours", "dbt · dimensional modeling"],
    body=r"""
## The modern data stack

```
SOURCES              INGESTION        WAREHOUSE           TRANSFORM       CONSUME
app Postgres    →    Fivetran/     →  BigQuery /     →    dbt        →   BI tool
payment API          Airbyte/         Snowflake /         (SQL +          reverse ETL
CSV/Sheets           custom ELT       Postgres /          tests +         notebooks
event stream         Dagster          DuckDB              docs)           ML features
```

**ELT replaced ETL:** load raw data first, transform inside the warehouse with SQL. Storage is cheap, warehouses are fast, and keeping the raw layer means you can always re-derive everything when a definition changes.

## Dimensional modeling (still the foundation, 30 years on)

**Fact tables** record events/measurements — long, narrow, append-heavy: `fct_orders`, `fct_payments`, `fct_page_views`. **Dimension tables** describe entities — wide, descriptive: `dim_customers`, `dim_products`, `dim_dates`.

```
fct_orders
  order_key (pk) | customer_key (fk) | product_key (fk) | date_key (fk)
  quantity | unit_price_ngn | discount_ngn | revenue_ngn | cost_ngn | margin_ngn
```

**Grain is everything.** Declare it in one sentence before writing any SQL: "one row per order line item per order." Mixing grains in one table is the most damaging modeling error there is — it double-counts.

**Slowly changing dimensions (SCD Type 2):** when a customer moves from Kano to Abuja, do you overwrite (Type 1, loses history) or add a new row with validity dates (Type 2, preserves the ability to report "revenue by customer's region *at the time of purchase*")? Knowing when Type 2 is required is a senior modeling skill.

**A date dimension** with fiscal periods, public holidays, weekday flags, and week numbers is one of the highest-leverage tables you will ever build. Build it once, use it everywhere.

## dbt — the industry standard

```
-- models/staging/stg_orders.sql   (1:1 with source, light cleaning only)
with source as (select * from {{ source('app', 'orders') }}),
renamed as (
    select
        id                            as order_id,
        customer_id                   as customer_id,
        lower(trim(status))           as status,
        total_kobo / 100.0            as total_ngn,
        placed_at at time zone 'UTC'  as placed_at_utc
    from source
    where not _deleted
)
select * from renamed
```

```
-- models/marts/fct_orders.sql
{{ config(materialized='incremental', unique_key='order_id',
          on_schema_change='append_new_columns') }}

select
    o.order_id, o.customer_id, o.status, o.total_ngn, o.placed_at_utc,
    c.segment, c.acquisition_channel,
    row_number() over (partition by o.customer_id order by o.placed_at_utc) as customer_order_seq,
    o.total_ngn - coalesce(i.total_cost_ngn, 0) as gross_margin_ngn
from {{ ref('stg_orders') }} o
left join {{ ref('dim_customers') }} c on c.customer_id = o.customer_id
left join {{ ref('int_order_costs') }} i on i.order_id = o.order_id
{% if is_incremental() %}
  where o.placed_at_utc > (select coalesce(max(placed_at_utc), '1900-01-01') from {{ this }})
{% endif %}
```

```
# models/marts/schema.yml - tests and documentation live WITH the model
version: 2
models:
  - name: fct_orders
    description: "One row per order. Grain: order_id. Excludes soft-deleted rows."
    columns:
      - name: order_id
        description: "Primary key from the application database."
        tests: [unique, not_null]
      - name: customer_id
        tests:
          - not_null
          - relationships: { to: ref('dim_customers'), field: customer_id }
      - name: status
        tests:
          - accepted_values: { values: ['pending','paid','shipped','delivered','cancelled','refunded'] }
      - name: total_ngn
        tests:
          - dbt_utils.expression_is_true: { expression: ">= 0" }
```

**What dbt gives you that raw SQL scripts never will:**
- **A DAG** — dependencies are inferred from `ref()`, so build order is automatic
- **Tests** — uniqueness, nulls, referential integrity, accepted values, custom business assertions, run on every build
- **Documentation** — auto-generated site with column-level lineage graphs
- **Environments** — dev builds into your own schema; production is separate
- **Incremental models** — process only new rows
- **Macros** — reusable SQL (DRY), and `{{ ref() }}` makes refactoring safe
- **Snapshots** — automatic SCD Type 2 history

**Layering convention:** `staging/` (one model per source table, renamed and typed) → `intermediate/` (joins and business logic) → `marts/` (facts and dimensions grouped by business area: finance, marketing, ops). Never let a mart read directly from a source.

:::edge Why analytics engineering pays well
It sits exactly where software engineering discipline meets analytics. You are the person who makes numbers **trustworthy**: version-controlled, tested, documented, reproducible, and lineage-traceable. Companies that have been burned by conflicting dashboards pay a premium for this. Because you already have git, CI, testing, and code review from Phase 4, you will pick this up faster than an analyst coming from Excel — that combination is your competitive advantage. Lean into it.
:::

## Warehouse mechanics worth knowing

- **Columnar storage** is why warehouses are fast for analytics: they read only the columns you select.
- **Partitioning** (usually by date) and **clustering** (by frequently filtered columns) dramatically cut scanned bytes — and BigQuery bills you by bytes scanned. `SELECT *` on a large table is a literal waste of money.
- **Materialization strategy** in dbt: `view` (cheap, always fresh), `table` (fast reads, rebuilt each run), `incremental` (large, append-mostly), `ephemeral` (inlined CTE).
- **Cost control:** partition filters required, query result caching, scheduled rather than continuous refreshes, and monitoring the most expensive queries.

:::ship Week 21 deliverable
A full dbt project on your SaaS data: 15+ models across staging/intermediate/marts, 40+ tests, complete documentation with descriptions on every column, a date dimension, one SCD Type 2 snapshot, incremental fact tables, a metrics dictionary, and dbt running in CI on every PR with `dbt build`. Publish the generated docs site. **A public dbt project with green tests is one of the strongest possible signals for an analytics engineering role.**
:::
""",
)

page(
    id="w22-bi",
    title="W22 · BI, Dashboards & Storytelling",
    sub="Week 22",
    eyebrow="WEEK 22 · DATA",
    subtitle="Dashboard maturity — designing for decisions, not decoration — is explicitly named as a top salary-raising skill.",
    chips=["35 hours", "Power BI · viz design · narrative"],
    body=r"""
## Choosing a tool

| Tool | Strengths | Learn it if |
|---|---|---|
| **Power BI** | Dominant in enterprise/banking/government; DAX is powerful; cheap | You want maximum job coverage — especially in Nigerian corporates |
| **Tableau** | Best-in-class exploratory visualization | Targeting international/consulting roles |
| **Looker / Looker Studio** | Governed metrics layer (LookML); Studio is free | Working with a modern data stack |
| **Metabase / Superset** | Open source, self-hostable, SQL-native | Startups, and you want to own the stack |
| **Streamlit / Evidence / Observable** | Code-native, versionable, custom | You are an engineer — this is your unfair advantage |

**Recommendation for you:** Power BI (job coverage) + Metabase (self-host on your own projects) + Streamlit or Evidence (leverage your engineering skills to build things a pure analyst cannot).

## Visualization: choose by question, not by aesthetics

| Question | Chart |
|---|---|
| How has X changed over time? | Line chart (time on x-axis, always) |
| How do categories compare? | Horizontal bar, sorted by value |
| What is the composition? | Stacked bar, or a treemap. **Avoid pie charts** beyond 2–3 slices |
| How are two variables related? | Scatter plot, with a trend line if justified |
| What is the distribution? | Histogram or box plot — never just an average |
| Where do users drop off? | Funnel |
| How does retention behave? | Cohort heatmap |
| Where is it happening? | Choropleth map (only if geography is the actual insight) |
| What is one key number? | Big number with a comparison and a sparkline |

**The rules that make charts credible:**
1. Bar charts **must** start at zero. Line charts need not, but label the axis clearly.
2. Sort bars by value, not alphabetically, unless the order is meaningful.
3. Label directly instead of forcing eye movement to a legend.
4. Maximize data-ink: delete gridlines, borders, 3D effects, and background fills.
5. Use color to encode meaning, and use at most 5–7 categories. Check colorblind safety (avoid red/green as the sole distinction).
6. Always show the comparison: versus last period, versus target, versus segment. A number alone is not information.
7. Annotate the "why" — a note on the chart saying "price change launched" turns a graph into an explanation.
8. Include units and the time window in the title. The title should state the **insight**, not the dimensions: "Mobile revenue overtook web in May" beats "Revenue by channel".

## Dashboard design that gets used

**The three-layer structure:**
1. **Top: the headline.** 4–6 KPI cards with value, change versus comparison period, and a sparkline. Answers "is anything wrong?" in five seconds.
2. **Middle: the drivers.** Trends and breakdowns explaining the headline. Answers "why?"
3. **Bottom: the detail.** Filterable table for the analyst who wants to dig in and export.

**Rules:** one dashboard, one audience, one purpose. Load in under 3 seconds. Every filter defaults to something sensible. State the refresh time and the data source visibly. Design mobile layouts for executives (they check on phones). And **remove anything nobody looks at** — instrument your dashboards and retire unused ones.

```
-- Power BI DAX: the patterns you will use constantly
Revenue = SUM(fct_orders[revenue_ngn])
Revenue LY = CALCULATE([Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
YoY % = DIVIDE([Revenue] - [Revenue LY], [Revenue LY])
Rolling 30d = CALCULATE([Revenue], DATESINPERIOD(dim_date[date], MAX(dim_date[date]), -30, DAY))
Active Customers = DISTINCTCOUNT(fct_orders[customer_id])
ARPU = DIVIDE([Revenue], [Active Customers])
-- CALCULATE modifies filter context. Understanding filter context IS understanding DAX.
```

## Storytelling with data

The structure that persuades, every time:

1. **Context** — the situation everyone agrees on. ("Checkout completion has averaged 62% all year.")
2. **Conflict** — what changed or what is at stake. ("In June it fell to 48%, costing about ₦31M/month.")
3. **Resolution** — your finding and recommendation. ("94% of the drop is card payments on Android in the 3 affected banks; enabling bank transfer as default for that segment recovers an estimated ₦24M/month.")

Deliver it as: the recommendation first, three supporting evidence points with numbers, the money at stake, the proposed action with an owner and a date, then the caveats. Keep methodology in an appendix.

:::edge Presentation skills are the compounding multiplier
The analyst who presents well gets their recommendations implemented; the one who does not gets ignored regardless of analytical quality. Practical rules: never read your slides; one message per slide with the message as the title; anticipate the three questions your audience will ask and prepare those slides for the appendix; know your numbers cold (if you cannot explain how a figure was calculated, do not show it); and **say what you do not know** — stating uncertainty honestly builds far more trust than false confidence, and executives can tell the difference.
:::

:::drill Dashboard critique drill
Find five public dashboards (COVID trackers, government open data portals, company investor pages). For each write: who is the audience, what decision it supports, three design flaws, and how you would redesign it. Then rebuild one of them better. Critique-then-rebuild teaches faster than building from scratch, and the write-up is excellent portfolio material.
:::

:::ship Week 22 deliverable
Three dashboards for three audiences on the same data: an **executive** view (5 KPIs, monthly, mobile-friendly, one screen), an **operational** view (daily, alerting, drill-down to individual records), and a **self-serve exploratory** tool. Plus a 10-minute recorded presentation of an analysis to an imagined executive team. Record yourself, watch it back, redo it. This is uncomfortable and it is exactly why most people never do it.
:::
""",
)

page(
    id="w23-ml",
    title="W23 · Forecasting & Practical ML",
    sub="Week 23",
    eyebrow="WEEK 23 · DATA",
    subtitle="Prediction that a business can act on — plus the judgment to know when a model is the wrong answer.",
    chips=["35 hours", "Time series · sklearn · deployment"],
    body=r"""
## Time series forecasting

Business forecasting questions: how much inventory to hold, how many agents to staff, what cash flow to expect, when to reorder.

**Decompose first:** trend + seasonality (weekly, monthly, annual) + holidays/events + noise. Plot the data before modeling — most forecasting failures come from not looking.

```
# Baselines FIRST. Always. You cannot claim a model is good without one.
naive      = y[-1]                       # tomorrow = today
seasonal   = y[-7]                       # this Monday = last Monday
moving_avg = y[-28:].mean()

# Then a real model
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, SeasonalNaive
sf = StatsForecast(models=[AutoARIMA(season_length=7), AutoETS(season_length=7), SeasonalNaive(season_length=7)],
                   freq="D", n_jobs=-1)
sf.fit(df)                              # df: unique_id, ds, y
fc = sf.forecast(h=30, level=[80, 95])  # ALWAYS produce prediction intervals
```

:::trap Time series validation is not random splitting
Never use `train_test_split` with shuffling on time series — you leak the future into training and get a beautiful, worthless model. Use **rolling-origin / expanding-window cross-validation**: train on data up to T, predict T+1..T+h, roll forward, repeat. Also beware **target leakage** generally: any feature that would not exist at prediction time (like "total order value" when predicting whether an order completes) makes your model look brilliant in testing and useless in production.
:::

**Evaluation metrics:** MAE (interpretable, in original units), RMSE (penalizes large errors), MAPE (percentage, but breaks near zero and punishes over-forecasting asymmetrically), and **MASE** (scaled against the naive baseline — the honest one). Report intervals, not just point forecasts: "we expect 1,200 units, 80% likely between 950 and 1,480" is far more useful for planning than a single number.

## Supervised ML for business problems

The realistic tasks: **churn prediction**, **credit default risk**, **lead scoring**, **demand forecasting**, **fraud detection**, **customer segmentation**, **recommendation**.

```
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold, cross_val_score
import lightgbm as lgb

pre = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), num_cols),
    ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                      ("oh", OneHotEncoder(handle_unknown="ignore", min_frequency=20))]), cat_cols),
])
pipe = Pipeline([("pre", pre), ("clf", lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05))])

scores = cross_val_score(pipe, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=42), scoring="roc_auc")
```

**Use a Pipeline always** — it prevents the classic leakage of fitting a scaler or imputer on the full dataset before splitting.

**For tabular business data, gradient boosting (LightGBM/XGBoost/CatBoost) beats deep learning almost always.** Do not reach for neural networks on a spreadsheet.

**Metrics that match the decision:**
- Accuracy is nearly useless on imbalanced data (99% accuracy predicting "no fraud" on 1% fraud).
- **Precision** — of those flagged, how many were right? (Matters when acting is costly.)
- **Recall** — of the actual positives, how many did we catch? (Matters when missing is costly.)
- **PR-AUC** for imbalanced problems; ROC-AUC for balanced.
- **Calibration** — if the model says 30%, does it happen 30% of the time? Essential when the score feeds a monetary decision (credit limits, expected value).
- **Cost-weighted evaluation** — translate the confusion matrix into naira. This is what makes an ML project a *business* project: "at this threshold we prevent ₦4.2M of fraud per month and wrongly block 180 legitimate transactions worth ₦900k."

**Feature engineering** beats model choice, nearly always: recency/frequency/monetary aggregates, ratios, time-since-last-event, rolling windows, day-of-week, and categorical target encoding (with care). Domain knowledge is your edge here.

**Interpretability:** SHAP values for global and per-prediction explanation. In credit and insurance this is a **regulatory requirement**, not a nicety — you must be able to say why an applicant was declined.

## Deployment and monitoring

```
# Serve it with FastAPI - you already know how
@app.post("/score/churn", response_model=ChurnScore)
async def score(req: ChurnRequest):
    features = build_features(req.customer_id)          # SAME code path as training
    proba = model.predict_proba(features)[0, 1]
    return ChurnScore(customer_id=req.customer_id, risk=float(proba),
                      band=band(proba), top_factors=explain(features)[:3],
                      model_version=MODEL_VERSION)
```

Track in production: **input drift** (has the population changed?), **prediction drift**, **actual outcomes** versus predictions once labels arrive, and business impact. Version models and data together. Have a documented rollback. Retrain on a schedule and re-validate before promoting.

:::edge The question that separates a professional from a Kaggle hobbyist
"What is the business action, and what does the model cost when it is wrong?" A churn model with 0.85 AUC is useless if nobody acts on it, or if the retention offer costs more than the customers saved. Always work backwards: decision → required precision/recall trade-off → threshold → model → features. And be willing to conclude "you do not need ML here — a rule that flags customers with no login in 30 days captures 80% of the value, costs nothing, and everyone understands it." That recommendation demonstrates more seniority than a fancy model.
:::

:::ship Week 23 deliverable
An end-to-end ML project deployed as a service: a real business problem, baseline first, feature engineering documented, proper validation, cost-weighted threshold selection, SHAP explanations, FastAPI endpoint, a monitoring dashboard, and a written business case in naira. Integrate it into your SaaS as a live feature (a risk score on a customer page). Include a section titled **"Why the simple version was almost good enough"** — reviewers love that honesty.
:::
""",
)

page(
    id="w24-capstone-data",
    title="W24 · Data Capstone",
    sub="Week 24",
    eyebrow="WEEK 24 · DATA",
    subtitle="A complete, sector-grounded analytics project — the piece that gets you data interviews.",
    chips=["35 hours", "Portfolio piece #5"],
    body=r"""
## The brief

Take a **real, messy, public dataset** in a sector you care about, and deliver a full analytics project as if you were a consultant being paid ₦2M for it.

### Data sources worth using
- **Nigeria:** NBS (National Bureau of Statistics) — CPI, GDP, trade, labour force; CBN statistical bulletin; NGX market data; NNPC/NUPRC petroleum data; NPHCDA health data; Nigeria Open Data portal; NIMET weather.
- **Africa/global:** World Bank Open Data, IMF, WHO GHO, FAOSTAT, GDELT, OpenStreetMap, Our World in Data.
- **Commercial-style:** Olist Brazilian e-commerce, NYC taxi, Instacart, telco churn datasets — good if you want a business-metrics flavor.

### Required deliverables

1. **A written analysis** (2,000–3,000 words) structured as: executive summary with the recommendation → context → methodology → findings with charts → limitations → recommendations with estimated impact → appendix with full methodology.
2. **A reproducible pipeline:** raw data ingestion → cleaning with documented decisions and validation → a dbt or SQL modeling layer → outputs. Anyone should be able to clone and run it.
3. **A dashboard** (Metabase/Power BI/Streamlit/Evidence) that is publicly viewable.
4. **A statistical or predictive component:** a hypothesis test, a causal estimate, or a forecast — with uncertainty quantified.
5. **A 10-minute recorded presentation** to a non-technical audience.
6. **A data quality report:** what was wrong with the source data and how you handled it.

### Strong project ideas by sector

++ Food inflation transmission :: Using NBS CPI and market price data, quantify how quickly fuel price changes transmit into food prices across states, and which states are most exposed. Policy-relevant, publishable.
++ Healthcare access gaps :: Combine facility locations, population density, and road networks to compute the share of each LGA's population beyond 5 km of a primary health centre. Recommend five optimal new sites.
++ Financial inclusion :: Analyze EFInA/World Bank Findex data to model which factors predict account ownership, and quantify the addressable market for agency banking by state.
++ Energy and outages :: Model the relationship between grid supply data, generator fuel costs, and SME operating costs; size the market for solar alternatives by sector.
++ Agricultural yield :: Combine rainfall (NIMET), planting calendars, and yield data to build an early-warning indicator for harvest shortfalls.
++ Public procurement :: Analyze open contracting data for anomalies — single-bidder contracts, unusual price variance, supplier concentration. Anti-corruption analytics is a real, funded field.

## The standard to hit

:::edge What makes a data portfolio project stand out
Almost every data portfolio contains a Titanic notebook and an Iris classifier. Yours must instead show: **(1)** you found and cleaned genuinely dirty real-world data, **(2)** you asked a question that matters to someone specific, **(3)** you quantified the answer in money or lives or hours, **(4)** you stated your uncertainty and limitations honestly, **(5)** you made a concrete recommendation, and **(6)** it is reproducible. Six things. Most portfolios have zero of them. Doing all six once beats doing ten tutorials.
:::

:::trap Three ways data portfolios fail
1. **No question.** A notebook of unrelated charts with no conclusion. Every project needs one sentence: "This analysis answers X so that Y can decide Z."
2. **Clean data.** Using a pre-cleaned Kaggle CSV proves nothing about the 70% of the job that is cleaning.
3. **No stated limitations.** Every dataset has bias, gaps, and definitional problems. Naming them shows maturity; ignoring them shows inexperience. Reviewers specifically look for this.
:::

## Week structure

@@ Day 1 | Choose the question and the stakeholder. Find and assess data. Write the analysis plan BEFORE touching the data.
@@ Day 2 | Ingest, profile, clean, validate. Write the data quality report as you go.
@@ Day 3 | Model the data (dbt/SQL). Build the metric definitions. Exploratory analysis.
@@ Day 4 | The core analysis: statistics, segmentation, causal reasoning or forecast.
@@ Day 5 | Dashboard and visualizations. Iterate on chart clarity ruthlessly.
@@ Day 6 | Write the report, record the presentation, publish everything, post it publicly.

:::ship Phase 6 exit criteria
You can take an ambiguous business question, find and clean the data, model it properly, apply appropriate statistics, build a dashboard people use, and present a recommendation that drives a decision. Combined with Phases 1–5, you are now in a very small group: engineers who can build the system *and* prove what it is doing. That combination is what the top 1% of this field actually looks like.
:::
""",
)
