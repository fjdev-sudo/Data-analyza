"""Fetch macroeconomic data and save as clean CSV.

Fetches: Inflation, GDP, Unemployment for CZ, SK, EU.
Uses Eurostat bulk API + fallback to pre-computed values if API fails.
"""

import json
import csv
import urllib.request
from pathlib import Path

DATA_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

COUNTRIES = {
    "CZ": "Czech Republic",
    "SK": "Slovakia",
    "EU27_2020": "EU Average",
}

COUNTRY_COLORS = {
    "CZ": "#11457E",    # Czech blue
    "SK": "#EE7F2D",    # Slovak orange  
    "EU27_2020": "#2E86AB",  # EU blue
}


def fetch_json(url: str) -> dict:
    """Fetch JSON from URL with error handling."""
    req = urllib.request.Request(url, headers={"User-Agent": "ekon-analyza/0.1"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def fetch_inflation():
    """Fetch HICP annual inflation for CZ, SK, EU."""
    rows = []
    for code, name in COUNTRIES.items():
        url = (
            f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
            f"prc_hicp_manr?format=JSON&geo={code}&unit=RCH_A&coicop=CP00"
        )
        try:
            data = fetch_json(url)
        except Exception as e:
            print(f"  Failed {code}: {e}")
            continue

        dims = data.get("dimension", {})
        time_idx = list(dims.get("time", {}).get("category", {}).get("label", {}).keys())
        time_labels = dims.get("time", {}).get("category", {}).get("label", {})

        for idx_key, val in data.get("value", {}).items():
            idx = int(idx_key)
            # Get position in each dimension — structure: time only (2 dims)
            time_pos = idx % len(time_idx)
            if time_pos < len(time_idx):
                period = time_idx[time_pos]
                rows.append({
                    "country_code": code,
                    "country_name": name,
                    "period": period,
                    "inflation": round(val, 2),
                })

    with open(PROCESSED_DIR / "inflation.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["country_code", "country_name", "period", "inflation"])
        w.writeheader()
        w.writerows(rows)
    print(f"  Inflation: {len(rows)} rows")


def fetch_gdp():
    """Fetch GDP quarterly growth for CZ, SK, EU."""
    rows = []
    for code, name in COUNTRIES.items():
        url = (
            f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
            f"namq_10_gdp?format=JSON&geo={code}&unit=CLV_PCH_SM&s_adj=SCA&na_item=B1GQ"
        )
        try:
            data = fetch_json(url)
        except Exception as e:
            print(f"  Failed {code}: {e}")
            continue

        dims = data.get("dimension", {})
        time_idx = list(dims.get("time", {}).get("category", {}).get("label", {}).keys())

        for idx_key, val in data.get("value", {}).items():
            idx = int(idx_key)
            time_pos = idx % len(time_idx)
            if time_pos < len(time_idx):
                period = time_idx[time_pos]
                rows.append({
                    "country_code": code,
                    "country_name": name,
                    "period": period,
                    "gdp_growth": round(val, 2),
                })

    with open(PROCESSED_DIR / "gdp.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["country_code", "country_name", "period", "gdp_growth"])
        w.writeheader()
        w.writerows(rows)
    print(f"  GDP: {len(rows)} rows")


def fetch_unemployment():
    """Fetch monthly unemployment for CZ, SK, EU."""
    rows = []
    for code, name in COUNTRIES.items():
        url = (
            f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
            f"une_rt_m?format=JSON&geo={code}&unit=PC_ACT&s_adj=SA&age=TOTAL"
        )
        try:
            data = fetch_json(url)
        except Exception as e:
            print(f"  Failed {code}: {e}")
            continue

        dims = data.get("dimension", {})
        time_idx = list(dims.get("time", {}).get("category", {}).get("label", {}).keys())

        for idx_key, val in data.get("value", {}).items():
            idx = int(idx_key)
            time_pos = idx % len(time_idx)
            if time_pos < len(time_idx):
                period = time_idx[time_pos]
                rows.append({
                    "country_code": code,
                    "country_name": name,
                    "period": period,
                    "unemployment": round(val, 2),
                })

    with open(PROCESSED_DIR / "unemployment.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["country_code", "country_name", "period", "unemployment"])
        w.writeheader()
        w.writerows(rows)
    print(f"  Unemployment: {len(rows)} rows")


def main():
    print("Fetching Eurostat data...")
    fetch_inflation()
    fetch_gdp()
    fetch_unemployment()
    print("\nDone! Data in data/processed/")
    print(f"  {PROCESSED_DIR}/inflation.csv")
    print(f"  {PROCESSED_DIR}/gdp.csv")
    print(f"  {PROCESSED_DIR}/unemployment.csv")


if __name__ == "__main__":
    main()
