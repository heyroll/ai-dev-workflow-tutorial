# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

- `sales_data.py` — all data loading and calculation logic. No Streamlit imports. Covered by `tests/test_sales_data.py`.
- `app.py` — Streamlit UI only (page config, layout, `st.metric()` cards, Plotly chart rendering). Contains no calculation logic; imports everything it needs from `sales_data.py`.
- `data/sales-data.csv` — source data. Required columns (see `REQUIRED_COLUMNS` in `sales_data.py`): `date, order_id, product, category, region, quantity, unit_price, total_amount`. `load_sales_data()` raises `ValueError` if any are missing.
- `prd/ecommerce-analytics.md` — the PRD. `docs/superpowers/plans/2026-09-20-sales-dashboard.md` — the implementation plan (task-by-task, TDD steps). `docs/superpowers/specs/2026-09-20-sales-dashboard-design.md` — the design spec.
- `TASKS.md` — the task board (`To Do` / `In Progress` / `Done`), mirroring the PRD's milestones. Each entry has acceptance-criteria checkboxes, a `Commit:` line, and a `Notes:` line.

Keep new calculation logic in `sales_data.py`, tested there — never in `app.py`.

## Running

- Activate the venv first: PowerShell `venv\Scripts\Activate.ps1`, bash `source venv/Scripts/activate`.
- Tests: use `python -m pytest`, not bare `pytest` — there's no `conftest.py`/`pytest.ini`, so nothing puts the project root on `sys.path`. Bare `pytest` fails with `ModuleNotFoundError: No module named 'sales_data'` even though the module is fine; `python -m pytest` works because `-m` itself prepends cwd to `sys.path`.
- Running the app in the background or non-interactively: use `streamlit run app.py --server.headless true`. Without `--server.headless true`, Streamlit's first-run onboarding prompt blocks on stdin and the process exits 127 when no input is attached.
- Expected reference values against the real dataset: Total Sales ≈ $116,500.21, Total Orders = 482, top category = Electronics, all 4 regions present (North, South, East, West), 5 categories.
- Streamlit renders client-side over a WebSocket — fetching the page URL only proves the server is up, not that displayed values are correct. Verify computed values by calling the `sales_data.py` functions directly against `data/sales-data.csv`.

## Project constraints (from the implementation plan's Global Constraints)

- Python 3.14.7, plain venv in `venv/` (gitignored) with deps in `requirements.txt` (unpinned — installs may drift to newer versions; watch for API differences, e.g. pandas has resolved to 3.0.x here). Do not use `uv` or `conda`.
- CSV validation is minimal and fail-fast: check required columns exist, otherwise let pandas raise naturally. No per-row data cleaning.
- The sales trend chart aggregates by month, not by day.
- No abstractions beyond what each task needs — keep code simple and readable.
- Styling uses Streamlit defaults and Plotly's default theme — no custom CSS or theming, **except** a single chart accent color (currently purple, `#7C3AED`, set via `color_discrete_sequence`/`CHART_COLOR` in `app.py`).
  - This color deviation is explicitly approved by Rolland Lopez; treat further accent-color changes the same way (config-level Plotly styling is fine, custom CSS/theming is not) unless told otherwise.
- TASK-7 (deployment to Streamlit Community Cloud) is done manually by the user from `main` after merge — do not attempt to deploy.

## Git and task-board workflow

Commits follow `TASK-N: <lowercase, imperative description>`. Moving a milestone between `TASKS.md` sections (In Progress, Done) is its own commit, separate from the code commit that implements it — e.g. `TASK-4: mark in progress on the board`, then `TASK-4: add monthly sales trend chart`, then `TASK-4: mark done on the board`. Fixes or tweaks requested after a task is already marked Done still cite that task's ID (e.g. `TASK-3: show cents in the Total Sales KPI`).

When moving a milestone to Done, its `Notes:` line should stay scoped to deviations: what Claude got wrong, or what the user explicitly changed/corrected. If neither happened, write `Clean` (optionally with a short reason). Don't use `Notes:` as a general implementation summary — verification detail belongs in commit messages, not the board.

## Lessons

Distilled from `TASKS.md` Notes lines across TASK-1 through TASK-6:

- `requirements.txt` is intentionally unpinned. Expect a fresh `pip install` to resolve dependencies (e.g. pandas) to newer majors than whatever's in the current venv, and watch for API differences rather than assuming a pinned version.
- Running Streamlit non-interactively (background processes, agents) requires `--server.headless true`. Without it, the first-run onboarding prompt blocks on stdin with no input attached and the process exits 127.
- If a board acceptance criterion isn't covered by the implementation plan, don't silently add scope or drop the criterion — flag the gap and get explicit sign-off before marking the milestone Done. Record a waived criterion with a struck-through (`~~...~~`), unchecked checkbox and a note naming who approved it and why.
- Verify computed dashboard values by calling `sales_data.py` functions directly against the real CSV, not by fetching the rendered page — Streamlit renders client-side over a WebSocket, so a plain HTTP fetch never shows the actual numbers.
- After a milestone is marked Done, small follow-up refinements (number formatting, chart styling, colors, axis ranges) are common. Make the change, show the running app, and wait for explicit confirmation before committing — then commit citing the original task's ID (e.g. `TASK-3: show cents in the Total Sales KPI`), not as new scope.
