import re
import pandas as pd

from config import COLUMN_MAPPINGS


# ==================================================
# Column Utilities
# ==================================================

def clean_columns(*dataframes):
    """
    Remove leading/trailing spaces
    from every dataframe column.
    """

    for df in dataframes:
        df.columns = df.columns.str.strip()


def find_column(df, logical_name):
    """
    Finds the actual column name from
    the configured aliases.
    """

    available_columns = {
        col.strip().lower(): col
        for col in df.columns
    }

    for alias in COLUMN_MAPPINGS[logical_name]:

        alias = alias.strip().lower()

        if alias in available_columns:
            return available_columns[alias]

    raise ValueError(
        f"Unable to find column for '{logical_name}'"
    )


def get_required_columns(df):
    """
    Returns all required columns.
    """

    return {

        "ldev_id": find_column(df, "ldev_id"),

        "wwn": find_column(df, "wwn"),

        "name": find_column(df, "name"),

        "size": find_column(df, "size")

    }


# ==================================================
# WWN Utilities
# ==================================================

def normalize_wwn(value):
    """
    Normalizes WWN values by removing
    prefixes and separators.
    """

    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    value = value.replace("naa.", "")
    value = value.replace("naa:", "")
    value = value.replace("naa", "")

    value = value.replace(":", "")
    value = value.replace("-", "")

    return value


def normalize_wwn_columns(
    audit_df,
    system_df,
    audit_cols,
    system_cols
):
    """
    Creates normalized WWN columns
    and returns both WWN sets.
    """

    audit_df["_WWN"] = (
        audit_df[
            audit_cols["wwn"]
        ].apply(normalize_wwn)
    )

    system_df["_WWN"] = (
        system_df[
            system_cols["wwn"]
        ].apply(normalize_wwn)
    )

    audit_wwns = set(
        audit_df["_WWN"].dropna()
    )

    system_wwns = set(
        system_df["_WWN"].dropna()
    )

    audit_wwns.discard("")
    system_wwns.discard("")

    return audit_wwns, system_wwns


# ==================================================
# Capacity Utilities
# ==================================================

def convert_to_gib(value):
    """
    Converts GiB/TiB values into GiB.
    """

    if pd.isna(value):
        return 0

    value = str(value).strip()

    value = value.replace(",", "")

    match = re.search(
        r"([\d\.]+)\s*(GiB|TiB)?",
        value,
        re.IGNORECASE
    )

    if not match:
        return 0

    number = float(match.group(1))

    unit = match.group(2)

    if unit is None:
        return number

    unit = unit.upper()

    if unit == "TIB":
        return number * 1024

    return number

