# Design: E-Commerce Sales Dashboard

Source PRD: `prd/ecommerce-analytics.md`
Tracked milestones: `TASKS.md` (TASK-1 through TASK-7)

## Overview

A single-page Streamlit dashboard reading `data/sales-data.csv` (482 transaction
rows, Jan–Dec 2024, 5 categories, 4 regions) and showing: two KPI cards (Total
Sales, Total Orders), a monthly sales trend line chart, and bar charts for sales
by category and by region. This covers Phase 1 of the PRD; Phase 2 items
(auth, filtering, export, etc.) are explicitly out of scope.

## Decisions

These were confirmed during brainstorming and drive the design below:

- **Trend granularity: monthly.** Daily would be noisy — 482 orders over 12
  months averages ~1.3/day. Monthly aggregation gives a smooth, presentable
  line.
- **Test depth: core calculations only.** One or two tests per data function
  against a small in-memory fixture DataFrame. No edge-case suite (empty data,
  ties, etc.) — the real dataset has none of these conditions (verified by
  direct inspection: no nulls, no duplicate order IDs, no non-positive
  quantities/prices, `total_amount` matches `quantity * unit_price` on all 482
  rows, all categories/regions match the PRD's lists exactly, all dates parse).
- **CSV validation: minimal, fail-fast.** Check required columns are present;
  otherwise let `pandas` raise naturally on a malformed file. No per-row
  cleaning or coercion, since the actual data doesn't need it.
- **Styling: Streamlit defaults + light touches.** `st.metric()` for KPI
  cards, Plotly's default theme for charts, wide page layout. No custom CSS
  or theming.
- **Python version: 3.14.7** (the only version installed locally; satisfies
  the PRD's 3.11+ requirement).

## Project structure

```
app.py                  # Streamlit UI: layout, widgets, chart building
sales_data.py           # Pure data functions: load + calculations (no Streamlit imports)
tests/
  test_sales_data.py    # pytest tests for sales_data.py
requirements.txt
venv/                   # local virtual environment (already gitignored)
data/sales-data.csv     # existing sample data
```

`sales_data.py` has no Streamlit dependency, so it's testable with plain
pytest. `app.py` imports it and handles only presentation. This mirrors the
PRD's own architecture diagram, which draws "Data Processing (Pandas)" as a
box separate from the Streamlit app.

## Data module (`sales_data.py`)

```python
def load_sales_data(path: str) -> pd.DataFrame:
    """Load CSV, parse the date column, and validate required columns exist.
    Raises FileNotFoundError / ValueError with a clear message on failure."""

def total_sales(df: pd.DataFrame) -> float: ...
def total_orders(df: pd.DataFrame) -> int: ...

def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Returns columns [month, total_amount], sorted chronologically."""

def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Returns columns [category, total_amount], sorted descending."""

def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Returns columns [region, total_amount], sorted descending."""
```

Each aggregation function takes an already-loaded DataFrame, not a file path,
so tests build a tiny in-memory DataFrame directly rather than needing CSV
fixture files.

## App layout (`app.py`)

```python
st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

df = load_sales_data("data/sales-data.csv")   # wrapped in try/except -> st.error on failure

st.title("ShopSmart Sales Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")

st.plotly_chart(line_chart(monthly_sales_trend(df)))

col3, col4 = st.columns(2)
col3.plotly_chart(bar_chart(sales_by_category(df)))
col4.plotly_chart(bar_chart(sales_by_region(df)))
```

This matches the PRD's dashboard layout diagram: KPIs on top, trend chart
full-width beneath, category/region bar charts side by side at the bottom.
`line_chart`/`bar_chart` helper functions live in `app.py` (not
`sales_data.py`) — they take already-aggregated DataFrames and return Plotly
figure objects, keeping data and presentation separated. A single top-level
`try/except` around `load_sales_data` shows a short `st.error(...)` message
instead of a raw traceback if the CSV is ever missing or malformed.

## Testing

`tests/test_sales_data.py`: one small in-memory sample DataFrame (5-6 rows
spanning multiple categories, regions, and months) as a pytest fixture, then
one test per function — `test_total_sales`, `test_total_orders`,
`test_monthly_sales_trend`, `test_sales_by_category`, `test_sales_by_region`
— each asserting the computed numbers match hand-calculated expectations from
the fixture. No file I/O in tests.

## Dependencies & environment

`requirements.txt` (unpinned, major packages only):
```
streamlit
pandas
plotly
pytest
```

Environment: `venv/` created with `python -m venv venv` (Python 3.14.7),
activated, then `pip install -r requirements.txt`. `venv/` is already covered
by the repo's `.gitignore`.

## Out of scope

Per the PRD's Phase 2 list: authentication, real-time database integration,
export functionality, email alerts, filtering/date range selection,
drill-down, mobile-responsive design. Also out of scope for this design:
custom CSS theming, defensive row-level data cleaning, edge-case test
coverage — none of these are needed for the actual dataset or the PRD's
Phase 1 acceptance criteria.

## Deployment

Deployment to Streamlit Community Cloud (TASK-7) is executed by the user
manually from `main` after this branch is reviewed and merged. It is not
part of the implementation plan's automated steps.
