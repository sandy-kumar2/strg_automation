import pandas as pd

from loader import (
    load_mapping_sheet,
    load_storage_export
)

from compare import compare_luns
from capacity import compare_capacity
from dashboard import create_dashboard
from pathlib import Path

from report import (
    print_console_report,
    generate_excel_report
)

# System Generated Report
system_report = (
    "data/input/NCC DC Dell Unity.xlsx"
)

system_df = load_mapping_sheet(
    system_report
)

system_name = Path(
    system_report
).stem

# Your Techno Report
audit_report = "data/input/ACX_NCC-Dell-Strg-DC Dell Unity.xlsx"

audit_df = load_storage_export(
    audit_report
)

report_name = Path(
    audit_report
).stem

# ==================================================
# Compare Reports
# ==================================================

comparison_result = compare_luns(
    audit_df,
    system_df,
    report_name,
    system_name
)

capacity_result = compare_capacity(
    audit_df,
    system_df
)

print_console_report(
    comparison_result,
    capacity_result
)

summary_df = pd.DataFrame(
    {
        "Metric": [
            "Techno WWN Count",
            "System WWN Count",
            "Techno Capacity (TiB)",
            "System Capacity (TiB)",
            "Difference (TiB)"
        ],
        "Value": [
            comparison_result["wwn"]["human_count"],
            comparison_result["wwn"]["system_count"],
            capacity_result["human_capacity"],
            capacity_result["system_capacity"],
            capacity_result["difference"]
        ]
    }
)

generate_excel_report(
    summary_df,
    comparison_result,
    report_name
)

# Dashboard
create_dashboard(
    capacity_result["human_capacity"],
    capacity_result["system_capacity"],
    comparison_result["wwn"]["human_count"],
    comparison_result["wwn"]["system_count"]
)