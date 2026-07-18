import pandas as pd

from utils import (
    convert_to_gib,
    get_required_columns
)

def compare_capacity(techno_df, system_df):

    techno_cols = get_required_columns(techno_df)
    system_cols = get_required_columns(system_df)

    techno_clean = techno_df[
        pd.to_numeric(
          techno_df[techno_cols["ldev_id"]],
          errors="coerce"
        ).notna() 
    ].copy()

    unique_techno = techno_clean.drop_duplicates(
        subset=[techno_cols["wwn"]]
    )

    unique_system = system_df.drop_duplicates(
        subset=[system_cols["wwn"]]
    )

    techno_total_gib = (
        unique_techno[techno_cols["size"]]
        .apply(convert_to_gib)
        .sum()
    )

    system_total_gib = (
        unique_system[system_cols["size"]]
        .apply(convert_to_gib)
        .sum()
    )

    difference_gib = techno_total_gib - system_total_gib

    techno_total_tib = techno_total_gib / 1024
    system_total_tib = system_total_gib / 1024
    difference_tib = difference_gib / 1024

    return {
    "passed": abs(difference_tib) < 0.01,
    "human_capacity": round(techno_total_tib, 2),
    "system_capacity": round(system_total_tib, 2),
    "difference": round(difference_tib, 2),
    "human_wwn": len(unique_techno),
    "system_wwn": len(unique_system)
    }