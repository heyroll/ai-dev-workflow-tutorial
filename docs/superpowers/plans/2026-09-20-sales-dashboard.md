# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ShopSmart e-commerce sales dashboard (Streamlit app with KPI cards, a monthly sales trend chart, and category/region breakdowns) from `data/sales-data.csv`.

**Architecture:** A pure-Python data module (`sales_data.py`, no Streamlit imports) holds loading and aggregation logic and is covered by pytest. `app.py` imports that module and handles only Streamlit layout and Plotly chart rendering.

**Tech Stack:** Python 3.14.7, Streamlit, Pandas, Plotly, pytest.

**Spec:** `docs/superpowers/specs/2026-09-20-sales-dashboard-design.md`

## Global Constraints

- Work on the current branch, `feature/sales-dashboard` — do not create a git worktree.
- Use a plain Python virtual environment in `venv/` with dependencies listed in `requirements.txt`. Do not use `uv` or `conda`.
- Python version: 3.14.7 (the only version installed on this machine; satisfies the PRD's 3.11+ floor).
- All data calculations live in `sales_data.py`, covered by pytest tests in `tests/test_sales_data.py`. `app.py` contains no calculation logic.
- CSV validation is minimal and fail-fast: check required columns exist; otherwise let pandas raise naturally. No per-row data cleaning.
- The sales trend chart aggregates by month, not by day.
- Styling uses Streamlit defaults (`st.metric()`, wide layout) and Plotly's default theme — no custom CSS or theming.
- Code should stay simple and readable — no abstractions beyond what each task needs.
- TASK-7 (deployment) is executed manually by the user from `main` after merge. It is not implemented by the agent; the plan hands off there.

## File Structure

```
app.py                  # Streamlit UI: page config, layout, chart rendering (built incrementally)
sales_data.py           # Data loading + calculation functions (built incrementally)
tests/
  test_sales_data.py    # pytest tests for sales_data.py (built incrementally)
requirements.txt        # streamlit, pandas, plotly, pytest
venv/                   # local virtual environment (gitignored, not committed)
data/sales-data.csv     # existing sample data (not modified)
```

`sales_data.py` and `tests/test_sales_data.py` are each modified across multiple tasks below, adding one function (and its tests) per task rather than growing in one large step. `app.py` is likewise extended incrementally: layout scaffolding in Task 1, then one dashboard element added per task as its underlying data function becomes available.

---

### Task 1: Environment setup and project skeleton (Milestone: TASK-1)

**Files:**
- Create: `requirements.txt`
- Create: `app.py`

**Interfaces:**
- Consumes: nothing (first task)
- Produces: a runnable Streamlit entry point at `app.py`; `venv/` with dependencies installed, used by every later task

- [ ] **Step 1: Create the virtual environment**

Run: `python -m venv venv`

- [ ] **Step 2: Activate it and create `requirements.txt`**

Activate (PowerShell): `venv\Scripts\Activate.ps1`
Activate (bash): `source venv/Scripts/activate`

Create `requirements.txt`:

```
streamlit
pandas
plotly
pytest
```

- [ ] **Step 3: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: all four packages (and their dependencies) install with no errors.

- [ ] **Step 4: Create a minimal `app.py`**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 5: Run the app and verify it loads**

Run: `streamlit run app.py`
Expected: browser opens to `http://localhost:8501` showing the page title "ShopSmart Sales Dashboard" with no errors in the terminal. Stop the server (Ctrl+C) once confirmed.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt app.py
git commit -m "TASK-1: set up environment and project skeleton"
```

---

### Task 2: Data loading with validation (Milestone: TASK-2)

**Files:**
- Create: `sales_data.py`
- Create: `tests/test_sales_data.py`

**Interfaces:**
- Consumes: nothing new
- Produces: `load_sales_data(path: str) -> pd.DataFrame`, raising `ValueError` if required columns are missing; module-level constant `REQUIRED_COLUMNS`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_sales_data.py`:

```python
import pandas as pd
import pytest

from sales_data import load_sales_data

CSV_CONTENT = """date,order_id,product,category,region,quantity,unit_price,total_amount
2024-01-15,ORD-1,Widget,Electronics,North,1,100.0,100.0
2024-02-10,ORD-2,Widget,Electronics,North,1,200.0,200.0
"""


def test_load_sales_data_reads_csv(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(CSV_CONTENT)

    df = load_sales_data(str(csv_path))

    assert len(df) == 2
    assert list(df.columns) == [
        "date", "order_id", "product", "category",
        "region", "quantity", "unit_price", "total_amount",
    ]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_sales_data_raises_on_missing_column(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text("date,order_id\n2024-01-15,ORD-1\n")

    with pytest.raises(ValueError):
        load_sales_data(str(csv_path))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_sales_data.py -v`
Expected: both tests FAIL with `ModuleNotFoundError: No module named 'sales_data'` (the file doesn't exist yet).

- [ ] **Step 3: Implement `sales_data.py`**

```python
import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def load_sales_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"sales data is missing required columns: {missing}")
    df["date"] = pd.to_datetime(df["date"])
    return df
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_sales_data.py -v`
Expected: both tests PASS.

- [ ] **Step 5: Commit**

```bash
git add sales_data.py tests/test_sales_data.py
git commit -m "TASK-2: add sales data loading with column validation"
```

---

### Task 3: KPI cards — Total Sales and Total Orders (Milestone: TASK-3)

**Files:**
- Modify: `sales_data.py`
- Modify: `tests/test_sales_data.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_sales_data(path: str) -> pd.DataFrame` (Task 2)
- Produces: `total_sales(df: pd.DataFrame) -> float`, `total_orders(df: pd.DataFrame) -> int`; pytest fixture `sample_df` in `tests/test_sales_data.py`, reused by Tasks 4 and 5:

```python
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date": pd.to_datetime([
            "2024-01-15", "2024-01-20", "2024-02-10", "2024-02-15", "2024-03-05",
        ]),
        "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4", "ORD-5"],
        "product": ["A", "B", "C", "D", "E"],
        "category": ["Electronics", "Audio", "Electronics", "Wearables", "Audio"],
        "region": ["North", "South", "North", "East", "West"],
        "quantity": [1, 2, 1, 3, 2],
        "unit_price": [100.0, 50.0, 200.0, 30.0, 25.0],
        "total_amount": [100.0, 100.0, 200.0, 90.0, 50.0],
    })
```

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_sales_data.py` (keep the existing imports and tests, add `pytest` fixture above and these tests below, and add `total_sales, total_orders` to the `from sales_data import ...` line):

```python
def test_total_sales(sample_df):
    assert total_sales(sample_df) == 540.0


def test_total_orders(sample_df):
    assert total_orders(sample_df) == 5
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_sales_data.py -v`
Expected: `test_total_sales` and `test_total_orders` FAIL with `ImportError: cannot import name 'total_sales'`.

- [ ] **Step 3: Implement the functions**

Add to `sales_data.py`:

```python
def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_sales_data.py -v`
Expected: all 4 tests PASS.

- [ ] **Step 5: Add the KPI cards to `app.py`**

Replace the contents of `app.py` with:

```python
import streamlit as st

from sales_data import load_sales_data, total_sales, total_orders

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

try:
    df = load_sales_data("data/sales-data.csv")
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

st.title("ShopSmart Sales Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")
```

- [ ] **Step 6: Run the app and verify the KPIs**

Run: `streamlit run app.py`
Expected: page shows "Total Sales" as **$116,500** and "Total Orders" as **482**, with no errors. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add sales_data.py tests/test_sales_data.py app.py
git commit -m "TASK-3: add KPI cards for total sales and total orders"
```

---

### Task 4: Sales trend chart (Milestone: TASK-4)

**Files:**
- Modify: `sales_data.py`
- Modify: `tests/test_sales_data.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `sample_df` fixture (Task 3); `load_sales_data`, `total_sales`, `total_orders` (Tasks 2-3, unchanged)
- Produces: `monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame` with columns `["month", "total_amount"]`, sorted chronologically, where `month` is a string like `"2024-01"`

- [ ] **Step 1: Write the failing test**

Add to `tests/test_sales_data.py` (add `monthly_sales_trend` to the import line):

```python
def test_monthly_sales_trend(sample_df):
    result = monthly_sales_trend(sample_df)

    assert list(result["month"]) == ["2024-01", "2024-02", "2024-03"]
    assert list(result["total_amount"]) == [200.0, 290.0, 50.0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_sales_data.py -v`
Expected: `test_monthly_sales_trend` FAILS with `ImportError: cannot import name 'monthly_sales_trend'`.

- [ ] **Step 3: Implement the function**

Add to `sales_data.py`:

```python
def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .sort_values("month")
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_sales_data.py -v`
Expected: all 5 tests PASS.

- [ ] **Step 5: Add the trend chart to `app.py`**

Update the imports and add the chart below the KPI columns:

```python
import plotly.express as px
import streamlit as st

from sales_data import load_sales_data, total_sales, total_orders, monthly_sales_trend
```

```python
trend = monthly_sales_trend(df)
fig_trend = px.line(
    trend, x="month", y="total_amount", markers=True,
    labels={"month": "Month", "total_amount": "Sales ($)"},
    title="Sales Trend Over Time",
)
st.plotly_chart(fig_trend, use_container_width=True)
```

- [ ] **Step 6: Run the app and verify the trend chart**

Run: `streamlit run app.py`
Expected: a line chart appears below the KPIs spanning 12 points, "2024-01" through "2024-12", generally trending upward toward the end of the year, with no errors. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add sales_data.py tests/test_sales_data.py app.py
git commit -m "TASK-4: add monthly sales trend chart"
```

---

### Task 5: Category and region breakdowns (Milestone: TASK-5)

**Files:**
- Modify: `sales_data.py`
- Modify: `tests/test_sales_data.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `sample_df` fixture (Task 3); all functions from Tasks 2-4, unchanged
- Produces: `sales_by_category(df: pd.DataFrame) -> pd.DataFrame` and `sales_by_region(df: pd.DataFrame) -> pd.DataFrame`, each with columns `[<category|region>, "total_amount"]`, sorted descending by `total_amount`

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_sales_data.py` (add `sales_by_category, sales_by_region` to the import line):

```python
def test_sales_by_category(sample_df):
    result = sales_by_category(sample_df)

    assert list(result["category"]) == ["Electronics", "Audio", "Wearables"]
    assert list(result["total_amount"]) == [300.0, 150.0, 90.0]


def test_sales_by_region(sample_df):
    result = sales_by_region(sample_df)

    assert list(result["region"]) == ["North", "South", "East", "West"]
    assert list(result["total_amount"]) == [300.0, 100.0, 90.0, 50.0]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_sales_data.py -v`
Expected: both new tests FAIL with `ImportError: cannot import name 'sales_by_category'`.

- [ ] **Step 3: Implement the functions**

Add to `sales_data.py`:

```python
def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("region", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_sales_data.py -v`
Expected: all 7 tests PASS.

- [ ] **Step 5: Add the breakdown charts to `app.py`**

Update the imports and add two columns with bar charts below the trend chart:

```python
from sales_data import (
    load_sales_data,
    total_sales,
    total_orders,
    monthly_sales_trend,
    sales_by_category,
    sales_by_region,
)
```

```python
col3, col4 = st.columns(2)

category = sales_by_category(df)
fig_category = px.bar(
    category, x="category", y="total_amount",
    labels={"category": "Category", "total_amount": "Sales ($)"},
    title="Sales by Category",
)
col3.plotly_chart(fig_category, use_container_width=True)

region = sales_by_region(df)
fig_region = px.bar(
    region, x="region", y="total_amount",
    labels={"region": "Region", "total_amount": "Sales ($)"},
    title="Sales by Region",
)
col4.plotly_chart(fig_region, use_container_width=True)
```

- [ ] **Step 6: Run the app and verify both charts**

Run: `streamlit run app.py`
Expected: two bar charts appear side by side below the trend chart. Category chart shows Electronics as the tallest bar, followed by Wearables, Audio, Smart Home, Accessories. Region chart shows North as the tallest bar, followed by West, East, South. No errors. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add sales_data.py tests/test_sales_data.py app.py
git commit -m "TASK-5: add category and region breakdown charts"
```

---

### Task 6: Testing and refinement (Milestone: TASK-6)

**Files:** none created or modified unless an issue is found during verification (see Step 4).

**Interfaces:**
- Consumes: the complete `app.py` and `sales_data.py` from Tasks 1-5
- Produces: nothing new; this task verifies the existing implementation against the PRD's acceptance criteria

- [ ] **Step 1: Run the full test suite**

Run: `pytest -v`
Expected: `7 passed` (2 loading tests, 2 KPI tests, 1 trend test, 2 breakdown tests), no failures or warnings.

- [ ] **Step 2: Run the app and check it against the PRD's expected output**

Run: `streamlit run app.py`, open `http://localhost:8501`, and confirm:
- Total Sales reads **$116,500**
- Total Orders reads **482**
- The trend line covers all 12 months of 2024
- The category chart's bar order (tallest to shortest) is Electronics, Wearables, Audio, Smart Home, Accessories
- The region chart's bar order (tallest to shortest) is North, West, East, South
- No errors or warnings appear in the browser or the terminal running Streamlit

- [ ] **Step 3: Check the PRD's acceptance criteria list**

Confirm each item in the PRD's "Acceptance Criteria" section (`prd/ecommerce-analytics.md`) is satisfied: KPIs visible, trend chart works, category chart works, region chart works, data loads correctly, no errors, professional appearance. All should already be true from Steps 1-2 — this is a final cross-check, not new work.

- [ ] **Step 4: Fix anything that didn't check out**

If any check in Step 2 or 3 failed, fix the specific issue in `app.py` or `sales_data.py`, re-run the affected verification, and commit the fix separately:

```bash
git add <fixed files>
git commit -m "TASK-6: fix <short description of the issue>"
```

If everything passed, no code changes or commit are needed for this task — stop here.

---

### Task 7: Deployment (Milestone: TASK-7) — executed by you, not the agent

**This task is not implemented as part of this plan.** Per your instructions, deployment is your responsibility, done manually from `main` after the feature branch is reviewed and merged. Stop plan execution at the end of Task 6 and hand off here.

When you're ready, the steps are:

- [ ] Push `feature/sales-dashboard` to GitHub and open a pull request.
- [ ] Review the diff yourself, optionally run `/code-review` on the branch.
- [ ] Merge the pull request into `main`.
- [ ] From `main`, deploy to Streamlit Community Cloud (per the PRD's NFR-5) and obtain the public shareable URL.
- [ ] Confirm the deployed app matches local behavior (KPIs, trend chart, category/region charts all render correctly).
- [ ] Record the public URL somewhere in the repo (e.g., the README) for stakeholder access.
