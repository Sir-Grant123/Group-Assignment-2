"""
Group name: CAS15
Group member1: Atulya Subedi, Student ID: S394148
Group member2: Oliver Charles Cole, Student ID: S368184
Group member3: Megh RakeshKumar Brahmbhatt, Student ID: S394095
"""

import os
import glob
import pandas as pd
import numpy as np

# --- Constants ---
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# defining SEASON_MAP as a dictionary which contains each month and it's related season
SEASON_MAP = {
    "December": "Summer", "January": "Summer", "February": "Summer",
    "March": "Autumn", "April": "Autumn", "May": "Autumn",
    "June": "Winter", "July": "Winter", "August": "Winter",
    "September": "Spring", "October": "Spring", "November": "Spring",
}
SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]

# Where the CSV files live (temperatures subdirectory)
BASE_DIR = os.path.dirname(os.path.abspath(
    __file__)) if "__file__" in globals() else os.getcwd()
TEMPS_DIR = os.path.join(BASE_DIR, "temperatures")

# --- Functions ---


def _standardize_month_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean up column names, fix common misspellings/whitespace,
    and ensure month columns are numeric (NaN on bad parses).
    """
    fixed_cols = []
    for c in df.columns:
        name = str(c).strip()
        if name.lower() == "febuary":  # common typo
            name = "February"
        fixed_cols.append(name)
    df.columns = fixed_cols

    # Coerce month columns to numeric
    for m in MONTHS:
        if m in df.columns:
            df[m] = pd.to_numeric(df[m], errors="coerce")
    return df


def load_all_temperature_data() -> pd.DataFrame:
    """
    Reads ALL .csv files in the 'temperatures' directory and links them together.
    Expects a 'STATION_NAME' column plus the 12 month columns.
    Missing values are kept as NaN and ignored by later calculations.
    """
    csv_paths = glob.glob(os.path.join(TEMPS_DIR, "*.csv"))
    if not csv_paths:
        raise FileNotFoundError(f"No CSV files found in: {TEMPS_DIR}")

    dfs = []
    for path in csv_paths:
        df = pd.read_csv(path)
        if "STATION_NAME" not in df.columns:
            raise ValueError(
                f"'STATION_NAME' column not found in {os.path.basename(path)}")
        df = _standardize_month_columns(df)
        # Keep only station + months (ignore any extra columns)
        keep_cols = ["STATION_NAME"] + [m for m in MONTHS if m in df.columns]
        df = df[keep_cols]
        dfs.append(df)

    # Combine all years/files; keep all rows
    data = pd.concat(dfs, ignore_index=True)
    return data


def to_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the format of the data, from wide columns: (STATION_NAME, Jan, feb, march...)
    to "long rows" (Station_Name, Month, Temp) 
    """
    # identifies which month colums are present
    present_months = [m for m in MONTHS if m in df.columns]
    # reformats the table
    long_df = df.melt(
        id_vars=["STATION_NAME"],
        value_vars=present_months,
        var_name="Month",
        value_name="Temp"
    )
    # Ignore missing temperatures
    long_df = long_df.dropna(subset=["Temp"])
    return long_df


def _fmt_c(v: float) -> str:
    """Format a number as degrees Celsius with one decimal."""
    return f"{v:.1f}°C"


def calculate_seasonal_average(data: pd.DataFrame, out_path: str = "average_temp.txt") -> None:
    """
    Calculates the average temperature for each season across all
    stations and years, then writes the value to "average_temp.txt"
    """
    long = to_long(data)
    long["Season"] = long["Month"].map(SEASON_MAP)
    long = long.dropna(subset=["Season"])

    season_means = (
        long.groupby("Season", as_index=True)["Temp"]
            .mean()
            .reindex(SEASON_ORDER)
    )

    lines = [f"{season}: {_fmt_c(val)}" for season,
             val in season_means.items()]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def calculate_largest_temp_range(data: pd.DataFrame, out_path: str = "largest_temp_range_station.txt") -> None:
    """
    Finds the station/s with the largest temperature range across all months and years.
    then writes each relevant station to "largest_temp_range.txt
    """
    long = to_long(data)
    if long.empty:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("No data available.\n")
        return

    stats = long.groupby("STATION_NAME")["Temp"].agg(["min", "max"])
    stats["range"] = stats["max"] - stats["min"]

    max_range = stats["range"].max()
    winners = stats[stats["range"] == max_range]

    lines = []
    for station, row in winners.iterrows():
        line = (
            f"{station}: Range {_fmt_c(row['range'])} "
            f"(Max: {_fmt_c(row['max'])}, Min: {_fmt_c(row['min'])})"
        )
        lines.append(line)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def calculate_temperature_stability(data: pd.DataFrame, out_path: str = "temperature_stability_stations.txt") -> None:
    """
    Finds the station/s with the smallest and largest standard deviation of temperatures
    (across all months and years). then saves said outputs to "temperature_stability_stations.txt"
    """
    long = to_long(data)
    if long.empty:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("No data available.\n")
        return

    std_by_station = long.groupby("STATION_NAME")["Temp"].std().dropna()

    if std_by_station.empty:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("Insufficient data for standard deviation.\n")
        return

    min_std = std_by_station.min()
    max_std = std_by_station.max()
    most_stable = std_by_station[std_by_station == min_std].index.tolist()
    most_variable = std_by_station[std_by_station == max_std].index.tolist()

    stable_names = ", ".join(most_stable)
    variable_names = ", ".join(most_variable)

    lines = [
        f"Most Stable: {stable_names}: StdDev {_fmt_c(min_std)}",
        f"Most Variable: {variable_names}: StdDev {_fmt_c(max_std)}",
    ]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    # Load every CSV in the temperatures subfolder
    data = load_all_temperature_data()

    # 1) Seasonal averages
    calculate_seasonal_average(data, out_path="average_temp.txt")

    # 2) Largest temperature range station(s)
    calculate_largest_temp_range(
        data, out_path="largest_temp_range_station.txt")

    # 3) Temperature stability (most stable & most variable)
    calculate_temperature_stability(
        data, out_path="temperature_stability_stations.txt")

    print("Done. Wrote: average_temp.txt, largest_temp_range_station.txt, temperature_stability_stations.txt")
