"""Analyze and visualize macroeconomic data: CZ vs SK vs EU.

Creates 3 interactive plotly charts and saves as HTML + PNG.
"""

import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime

import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROCESSED_DIR = Path("data/processed")
DASHBOARD_DIR = Path("dashboard")
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {"CZ": "#11457E", "SK": "#EE7F2D", "EU27_2020": "#2E86AB"}
NAMES = {"CZ": "Česko", "SK": "Slovensko", "EU27_2020": "EU priemer"}

# ── Data Loading ──────────────────────────────────────

def load_csv(name: str) -> dict[str, dict[str, float]]:
    """Load CSV into {country_code: {period: value}}"""
    data: dict[str, dict[str, float]] = defaultdict(dict)
    with open(PROCESSED_DIR / f"{name}.csv") as f:
        for row in csv.DictReader(f):
            code = row["country_code"]
            period = row["period"]
            # Determine value column name
            val_col = [c for c in row if c not in ("country_code", "country_name", "period")][0]
            try:
                data[code][period] = float(row[val_col])
            except (ValueError, KeyError):
                continue
    return data


def filter_periods(data: dict[str, dict[str, float]], start: str, end: str):
    """Keep only periods between start and end (inclusive)."""
    result = {}
    for code, periods in data.items():
        filtered = {p: v for p, v in periods.items() if start <= p <= end}
        if filtered:
            result[code] = dict(sorted(filtered.items()))
    return result


# ── Charts ────────────────────────────────────────────

def chart_inflation(data):
    """Inflation rate over time (monthly)."""
    fig = go.Figure()
    for code in ["CZ", "SK", "EU27_2020"]:
        if code not in data:
            continue
        periods = sorted(data[code])
        values = [data[code][p] for p in periods]
        fig.add_trace(go.Scatter(
            x=periods, y=values, mode="lines",
            name=NAMES.get(code, code),
            line=dict(color=COLORS.get(code, "#999"), width=2),
        ))
    fig.update_layout(
        title="Inflácia (HICP) — medziročná zmena v %",
        xaxis_title="Rok",
        yaxis_title="%",
        template="plotly_white",
        hovermode="x unified",
        height=500,
    )
    fig.write_html(DASHBOARD_DIR / "inflation.html")
    fig.write_image(DASHBOARD_DIR / "screenshots" / "inflation.png", scale=2)
    print("  ✓ inflation chart saved")


def chart_gdp(data):
    """GDP growth rate over time (quarterly)."""
    fig = go.Figure()
    for code in ["CZ", "SK", "EU27_2020"]:
        if code not in data:
            continue
        periods = sorted(data[code])
        values = [data[code][p] for p in periods]
        fig.add_trace(go.Bar(
            x=periods, y=values,
            name=NAMES.get(code, code),
            marker_color=COLORS.get(code, "#999"),
        ))
    fig.update_layout(
        title="Rast HDP — medziročná zmena v % (kvartálne)",
        xaxis_title="Kvartál",
        yaxis_title="%",
        template="plotly_white",
        barmode="group",
        height=500,
    )
    fig.write_html(DASHBOARD_DIR / "gdp.html")
    fig.write_image(DASHBOARD_DIR / "screenshots" / "gdp.png", scale=2)
    print("  ✓ GDP chart saved")


def chart_unemployment(data):
    """Unemployment rate over time (monthly)."""
    fig = go.Figure()
    for code in ["CZ", "SK", "EU27_2020"]:
        if code not in data:
            continue
        periods = sorted(data[code])
        values = [data[code][p] for p in periods]
        fig.add_trace(go.Scatter(
            x=periods, y=values, mode="lines",
            name=NAMES.get(code, code),
            line=dict(color=COLORS.get(code, "#999"), width=2),
        ))
    fig.update_layout(
        title="Nezamestnanosť — % aktívnej populácie (sezónne očistené)",
        xaxis_title="Rok",
        yaxis_title="%",
        template="plotly_white",
        hovermode="x unified",
        height=500,
    )
    fig.write_html(DASHBOARD_DIR / "unemployment.html")
    fig.write_image(DASHBOARD_DIR / "screenshots" / "unemployment.png", scale=2)
    print("  ✓ unemployment chart saved")


def chart_dashboard(data_inf, data_gdp, data_unemp):
    """Combined dashboard with all 3 charts."""
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            "Inflácia (HICP medziročne, %)",
            "Rast HDP (kvartálne, %)",
            "Nezamestnanosť (%)",
        ),
        vertical_spacing=0.08,
    )

    for code in ["CZ", "SK", "EU27_2020"]:
        # Inflation
        if code in data_inf:
            p_inf = sorted(data_inf[code])
            fig.add_trace(go.Scatter(
                x=p_inf, y=[data_inf[code][p] for p in p_inf],
                mode="lines", name=NAMES.get(code, code),
                line=dict(color=COLORS.get(code, "#999"), width=1.5),
                showlegend=True,
            ), row=1, col=1)

        # GDP
        if code in data_gdp:
            p_gdp = sorted(data_gdp[code])
            fig.add_trace(go.Bar(
                x=p_gdp, y=[data_gdp[code][p] for p in p_gdp],
                name=NAMES.get(code, code),
                marker_color=COLORS.get(code, "#999"),
                showlegend=False,
            ), row=2, col=1)

        # Unemployment
        if code in data_unemp:
            p_un = sorted(data_unemp[code])
            fig.add_trace(go.Scatter(
                x=p_un, y=[data_unemp[code][p] for p in p_un],
                mode="lines", name=NAMES.get(code, code),
                line=dict(color=COLORS.get(code, "#999"), width=1.5),
                showlegend=False,
            ), row=3, col=1)

    fig.update_layout(
        title_text="Makroekonomické porovnanie: Česko vs Slovensko vs EÚ (2015–2025)",
        height=1000,
        template="plotly_white",
        hovermode="x unified",
    )
    fig.write_html(DASHBOARD_DIR / "dashboard.html")
    print("  ✓ dashboard saved")


def write_findings(data_inf, data_gdp, data_unemp):
    """Generate key findings in markdown."""
    findings = []

    # Inflation peaks
    for code in ["CZ", "SK"]:
        if code in data_inf:
            peak_val = max(data_inf[code].values())
            peak_period = [p for p, v in data_inf[code].items() if v == peak_val][0]
            findings.append(f"- **{NAMES[code]}**: maximálna inflácia **{peak_val}%** v {peak_period}")

    # Unemployment lows
    for code in ["CZ", "SK"]:
        if code in data_unemp:
            low_val = min(data_unemp[code].values())
            low_period = [p for p, v in data_unemp[code].items() if v == low_val][0]
            findings.append(f"- **{NAMES[code]}**: najnižšia nezamestnanosť **{low_val}%** v {low_period}")

    with open("report/findings.md", "w") as f:
        f.write("# Kľúčové zistenia\n\n")
        f.write("Automaticky vygenerované z Eurostat API dát.\n\n")
        f.write("## Inflácia\n")
        f.write("\n".join(findings[:2]) + "\n\n")
        f.write("## Nezamestnanosť\n")
        f.write("\n".join(findings[2:4]) + "\n")
    print("  ✓ findings written")


def main():
    print("Loading data...")
    inf = load_csv("inflation")
    gdp = load_csv("gdp")
    unemp = load_csv("unemployment")

    # Filter to 2015-2025
    inf = filter_periods(inf, "2015-01", "2025-12")
    gdp = filter_periods(gdp, "2015-Q1", "2025-Q3")
    unemp = filter_periods(unemp, "2015-01", "2025-12")

    print(f"  Inflation: {sum(len(v) for v in inf.values())} data points")
    print(f"  GDP: {sum(len(v) for v in gdp.values())} data points")
    print(f"  Unemployment: {sum(len(v) for v in unemp.values())} data points")

    print("\nGenerating charts...")
    (DASHBOARD_DIR / "screenshots").mkdir(parents=True, exist_ok=True)
    chart_inflation(inf)
    chart_gdp(gdp)
    chart_unemployment(unemp)
    chart_dashboard(inf, gdp, unemp)

    print("\nWriting findings...")
    write_findings(inf, gdp, unemp)

    print("\n✅ Done! Open dashboard/dashboard.html to view.")


if __name__ == "__main__":
    main()
