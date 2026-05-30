# ekon-analyza

Macroeconomic comparison: Czech Republic vs Slovakia vs EU (2015–2025).  
Real data from Eurostat API. Built with Python, Pandas, and Plotly.

## Charts

| Metric | Preview |
|--------|---------|
| Inflácia (HICP) | [Open](dashboard/inflation.html) |
| Rast HDP | [Open](dashboard/gdp.html) |
| Nezamestnanosť | [Open](dashboard/unemployment.html) |
| **Dashboard** | [Open](dashboard/dashboard.html) |

## Key Findings

### Inflation
- **Česko**: maximálna inflácia **17.5%** v Januári 2023
- **Slovensko**: maximálna inflácia **14.8%** v Februári 2023

### Unemployment  
- **Česko**: najnižšia nezamestnanosť **2.0%** (najnižšia v EÚ)
- **Slovensko**: najnižšia nezamestnanosť **5.7%**

### Observations
1. Czech inflation exceeded EU average by 2-4pp during the 2022-2023 energy crisis
2. Czech unemployment consistently 3-5pp below EU average — tightest labor market in EU
3. Both CZ and SK GDP contracted sharply in Q2 2020 (COVID) and recovered by Q3 2021
4. Slovakia's unemployment remains structurally higher than Czech levels by 2-4pp

## Tech Stack

- **Python 3.9+**: pandas, plotly, csv
- **Eurostat API**: official EU statistical data
- **Plotly**: interactive charts (zoom, hover, export)
- **Jupyter Notebook**: step-by-step analysis in `notebooks/`

## Data Sources

All data from [Eurostat](https://ec.europa.eu/eurostat) public API:
- Inflation: `prc_hicp_manr` (HICP monthly annual rate of change)
- GDP: `namq_10_gdp` (GDP and main components)
- Unemployment: `une_rt_m` (unemployment by sex and age — monthly)

Data fetched on: **2026-05-29**

## Quick Start

```bash
# Install dependencies
pip install pandas plotly kaleido

# Fetch fresh data from Eurostat
python scripts/fetch_data.py

# Generate charts
python scripts/analyze.py

# Open dashboard
open dashboard/dashboard.html
```

## Project Structure

```
ekon-analyza/
├── scripts/
│   ├── fetch_data.py      # Fetch from Eurostat API
│   └── analyze.py         # Process & visualize
├── data/
│   └── processed/         # Cleaned CSVs
├── dashboard/             # Interactive HTML charts
├── notebooks/             # Jupyter analysis
└── report/
    └── findings.md        # Automatic findings
```

## Why This Project?

Demonstrates: Python data analysis, working with real economic APIs, data visualization, and applying VŠE economics education in practice. All code is reproducible — anyone can run `fetch_data.py` and get the same results.

---

