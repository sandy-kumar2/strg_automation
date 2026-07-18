import pandas as pd

from pathlib import Path
from datetime import datetime


def print_console_report(
    comparison_result,
    capacity_result
):

    print("\n" + "=" * 70)
    print("STORAGE AUDIT REPORT")
    print("=" * 70)

    overall_status = (
        comparison_result["passed"]
        and
        capacity_result["passed"]
    )

    print(
        f"Overall Status : {'PASSED ✅' if overall_status else 'FAILED ❌'}"
    )

    print("\nValidation Summary")
    print("-" * 70)

    validations = [
        (
            "WWN",
            comparison_result["wwn"]["passed"]
        ),
        (
            "LDEV ID",
            comparison_result["ldev_id"]["passed"]
        ),
        (
            "LDEV Name",
            comparison_result["name"]["passed"]
        ),
        (
            "LDEV Size",
            comparison_result["size"]["passed"]
        ),
        (
            "Capacity",
            capacity_result["passed"]
        )
    ]

    for name, passed in validations:

        print(
            f"{'✓' if passed else '✗'} {name}"
        )

    print("\nWWN Count")

    print(
        f"Human Report  : {comparison_result['wwn']['human_count']}"
    )

    print(
        f"System Report : {comparison_result['wwn']['system_count']}"
    )

    print("\nCapacity")

    print(
        f"Human Report  : {capacity_result['human_capacity']} TiB"
    )

    print(
        f"System Report : {capacity_result['system_capacity']} TiB"
    )

    print(
        f"Difference    : {capacity_result['difference']} TiB"
    )

    print("=" * 70)

    # ==================================================
    # WWN DETAILS
    # ==================================================

    if not comparison_result["wwn"]["passed"]:

      print("\nWWN VALIDATION")
      print("=" * 70)

      print(
        comparison_result["wwn"]["data"]
        .to_string(index=False)
      )

    # ==================================================
    # LDEV ID DETAILS
    # ==================================================

    if not comparison_result["ldev_id"]["passed"]:

        print("\nLDEV ID MISMATCH")
        print("=" * 70)

        print(
            comparison_result["ldev_id"]["data"]
            .to_string(index=False)
        )

    # ==================================================
    # LDEV NAME DETAILS
    # ==================================================

    if not comparison_result["name"]["passed"]:

        print("\nLDEV NAME MISMATCH")
        print("=" * 70)

        print(
            comparison_result["name"]["data"]
            .to_string(index=False)
        )

    # ==================================================
    # LDEV SIZE DETAILS
    # ==================================================

    if not comparison_result["size"]["passed"]:

        print("\nLDEV SIZE MISMATCH")
        print("=" * 70)

        print(
            comparison_result["size"]["data"]
            .to_string(index=False)
        )

    print()


def generate_excel_report(
    summary_df,
    comparison_result,
    report_name
):

    report_short = report_name

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    output_dir = (
        Path("output")
        /
        today
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%H-%M-%S"
    )

    output_file = (
        output_dir
        /
        f"{report_name}_{timestamp}.xlsx"
    )

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        # Missing LUNs
        if not comparison_result["wwn"]["data"].empty:
           comparison_result["wwn"]["data"].to_excel(
           writer,
           sheet_name=f"Missing in {report_short}"[:31],
           index=False
        ) 

        # LDEV ID Mismatch
        if not comparison_result["ldev_id"]["data"].empty:
           comparison_result["ldev_id"]["data"].to_excel(
           writer,
           sheet_name="LDEV_ID_Mismatch",
           index=False
        )

        # LDEV Name Mismatch
        if not comparison_result["name"]["data"].empty:
           comparison_result["name"]["data"].to_excel(
           writer,
           sheet_name="LDEV_Name_Mismatch",
           index=False
        )

        # LDEV Size Mismatch
        if not comparison_result["size"]["data"].empty:
           comparison_result["size"]["data"].to_excel(
           writer,
           sheet_name="LDEV_Size_Mismatch",
           index=False
        )

    print(
        f"Report Generated : {output_file}"
    )