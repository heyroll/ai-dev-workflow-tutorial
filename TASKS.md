# Tasks

This file tracks all work for the ShopSmart e-commerce analytics dashboard, as defined in `prd/ecommerce-analytics.md`.

## Definition of Done

A milestone can only move to Done when:

- Its acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

### TASK-7: Deployment to Streamlit Community Cloud
Publish the dashboard so stakeholders can access it via a public URL.
- [ ] App is deployed to Streamlit Community Cloud
- [ ] Deployed app is reachable via a shareable public URL and matches local behavior
- [ ] Public URL is recorded (e.g., in the README) for stakeholder access

Commit:

## In Progress

## Done

### TASK-6: Testing and refinement
Verify the dashboard is correct, performant, and presentable.
- [x] Dashboard runs with no errors or warnings, and loads within 5 seconds
- [x] Displayed values match expected results (~$116,500 total sales, 482 total orders, Electronics as top category)
- [x] Layout and styling are polished enough for an executive presentation

Commit: N/A — verification only, no code changes required
Notes: Clean — verification only, everything already met the acceptance criteria, nothing to fix.

### TASK-5: Category and region breakdowns
Show sales broken down by product category and by region.
- [x] Bar chart shows sales by category, sorted highest to lowest, with all 5 categories present
- [x] Bar chart shows sales by region, sorted highest to lowest, with all 4 regions present
- [x] Both charts include interactive tooltips with exact values

Commit: fea2c5c
Notes: Clean — implementation matched the plan exactly (TDD RED then GREEN, 7 tests passing), nothing Rolland had to correct.

### TASK-4: Sales trend chart
Show how sales change over time.
- [x] Line chart plots sales over time (daily or monthly granularity)
- [x] Chart includes interactive tooltips showing exact values
- [x] Chart renders within 2 seconds of data load

Commit: 46309a2
Notes: Clean — implementation matched the plan exactly (TDD RED then GREEN, 5 tests passing), nothing Rolland had to correct.

### TASK-3: KPI cards implementation
Display the headline Total Sales and Total Orders metrics.
- [x] Total Sales (sum of `total_amount`) and Total Orders (transaction count) are calculated correctly
- [x] Currency and large numbers are formatted appropriately (e.g., `$116,500`)
- [x] KPIs are displayed prominently near the top of the dashboard

Commit: 66716aa
Notes: Clean — implementation matched the plan exactly (TDD RED then GREEN, 4 tests passing), nothing Rolland had to correct.

### TASK-2: Data loading and basic structure
Load and validate the sales data so it's ready for analysis.
- [x] `sales-data.csv` loads into a Pandas DataFrame without errors
- [x] Date, numeric, and categorical columns are parsed with correct types
- [ ] ~~A basic data preview/summary is displayed in the app for sanity checking~~

  Note: Rolland Lopez approved moving TASK-2 to Done without this item. The implementation plan's Task 2 never adds a preview to `app.py`, and Task 3 overwrites `app.py`'s contents wholesale (adding the KPI cards) before a preview would ever be seen, so it was dropped as redundant.

Commit: f094d5b
Notes: Implementation matched the plan exactly — TDD RED then GREEN verified, tests passed on first try, no rework needed. One discrepancy surfaced: the board's third acceptance criterion (data preview in app) wasn't covered by the implementation plan at all; flagged to Rolland, who approved dropping it (see struck-through item and note above) rather than adding scope outside the plan. Rolland also asked for a formatting fix (blank line after the struck-through criterion), applied after the initial board update.

### TASK-1: Environment setup and project initialization
Set up the project skeleton and dependencies needed to build the dashboard.
- [x] `app.py` and `requirements.txt` exist, with `streamlit`, `pandas`, and `plotly` listed as dependencies
- [x] Project structure includes a `data/` folder containing `sales-data.csv`
- [x] A minimal Streamlit app runs locally with `streamlit run app.py`

Commit: 9e2afbd
Notes: First background run of `streamlit run app.py` failed (exit 127) because Streamlit's interactive first-run onboarding prompt blocks on stdin with no input attached; fixed by adding `--server.headless true`. `requirements.txt` is unpinned, so `pip install` resolved pandas to 3.0.6 (a very recent major version) — flagging to watch for API differences once later tasks use it for real data work.
