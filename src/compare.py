import pandas as pd

from utils import (
    clean_columns,
    normalize_wwn_columns,
    convert_to_gib,
    get_required_columns,
)

# ==================================================
# Merge Reports
# ==================================================

def merge_reports(
    audit_df,
    system_df
):

    return audit_df.merge(
        system_df,
        on="_WWN",
        how="inner",
        suffixes=(
            "_audit",
            "_system"
        )
    )

# ==================================================
# WWN Validation
# ==================================================

def compare_wwn(
    audit_df,
    system_df,
    audit_cols,
    system_cols,
    audit_wwns,
    system_wwns,
    report_name,
    system_name
):

    missing_in_audit = (
        system_wwns - audit_wwns
    )

    missing_in_system = (
        audit_wwns - system_wwns
    )

    missing_lun_details = system_df[
        system_df["_WWN"].isin(
            missing_in_audit
        )
    ][
        [
            system_cols["ldev_id"],
            system_cols["name"],
            system_cols["size"],
            "_WWN"
        ]
    ].copy()

    missing_lun_details.columns = [
        "LUN-ID",
        "LUN-NAME",
        "SIZE",
        "WWN"
    ]


    extra_lun_details = audit_df[
        audit_df["_WWN"].isin(
            missing_in_system
        )
    ][
        [
            audit_cols["ldev_id"],
            audit_cols["name"],
            audit_cols["size"],
            "_WWN"
        ]
    ].copy()

    extra_lun_details.columns = [
        "LUN-ID",
        "LUN-NAME",
        "SIZE",
        "WWN"
    ]


    audit_count = len(audit_wwns)
    system_count = len(system_wwns)

    if audit_count == system_count:

        wwn_report = pd.concat(
            [
                extra_lun_details.assign(
                   Status=f"WWN Mismatch in {report_name}"
                ),
                missing_lun_details.assign(
                   Status=f"WWN Mismatch in {system_name}"
                )
            ],
            ignore_index=True
        )

    elif audit_count > system_count:

        wwn_report = extra_lun_details.assign(
           Status=f"Extra in {report_name}"
        )

    else:
  
        wwn_report = missing_lun_details.assign(
           Status=f"Missing from {report_name}"
        )

    return {

        "passed": (
            not missing_in_audit
            and
            not missing_in_system
        ),

        "human_count": len(
            audit_wwns
        ),

        "system_count": len(
            system_wwns
        ),

        "count": len(
            wwn_report
        ),

        "data": wwn_report

    }


# ==================================================
# LDEV ID Validation
# ==================================================

def compare_ldev_id(
    merged_df,
    audit_cols,
    system_cols,
    audit_name,
    system_name
):

    id_mismatch = merged_df[

        merged_df[
            audit_cols["ldev_id"]
        ]

        !=

        merged_df[
            system_cols["ldev_id"]
        ]

    ][

        [

            "_WWN",

            audit_cols["ldev_id"],

            audit_cols["name"],

            audit_cols["size"],

            system_cols["ldev_id"]

        ]

    ]


    id_mismatch.columns = [

        "WWN",

        f"LUN-ID ({audit_name})",

        "LUN-NAME",

        "SIZE",

        f"LUN-ID ({system_name})"

    ]


    return {

        "passed": id_mismatch.empty,

        "count": len(
            id_mismatch
        ),

        "data": id_mismatch

    }


# ==================================================
# LDEV Name Validation
# ==================================================

def compare_ldev_name(
    merged_df,
    audit_cols,
    system_cols,
    audit_name,
    system_name
):

    name_mismatch = merged_df[

        merged_df[
            audit_cols["name"]
        ]
        .astype(str)
        .str.strip()
        .str.lower()

        !=

        merged_df[
            system_cols["name"]
        ]
        .astype(str)
        .str.strip()
        .str.lower()

    ][

        [

            "_WWN",

            audit_cols["ldev_id"],

            audit_cols["name"],

            system_cols["name"],

            audit_cols["size"]

        ]

    ]


    name_mismatch.columns = [

        "WWN",

        "LUN-ID",

        f"LUN Name ({audit_name})",

        f"LUN Name ({system_name})",

        "SIZE"

    ]


    return {

        "passed": name_mismatch.empty,

        "count": len(
            name_mismatch
        ),

        "data": name_mismatch

    }

# ==================================================
# LDEV Size Validation
# ==================================================

def compare_ldev_size(
    merged_df,
    audit_cols,
    system_cols,
    audit_name,
    system_name
):

    merged_df["AUDIT_SIZE_GIB"] = (
        merged_df[
            audit_cols["size"]
        ].apply(convert_to_gib)
    )

    merged_df["SYSTEM_SIZE_GIB"] = (
        merged_df[
            system_cols["size"]
        ].apply(convert_to_gib)
    )

    size_mismatch = merged_df[

        merged_df["AUDIT_SIZE_GIB"]

        !=

        merged_df["SYSTEM_SIZE_GIB"]

    ][

        [

            "_WWN",

            audit_cols["ldev_id"],

            audit_cols["name"],

            audit_cols["size"],

            system_cols["size"]

        ]

    ]

    size_mismatch.columns = [

        "WWN",

        "LUN-ID",

        "LUN-NAME",

        f"LUN Size ({audit_name})",

        f"LUN Size ({system_name})"

    ]

    return {

        "passed": size_mismatch.empty,

        "count": len(size_mismatch),

        "data": size_mismatch

    }


# ==================================================
# Main Comparison Function
# ==================================================

def compare_luns(
    audit_df,
    system_df,
    report_name,
    system_name
):

    # ----------------------------------------------
    # Clean Columns
    # ----------------------------------------------

    clean_columns(
        audit_df,
        system_df
    )

    # ----------------------------------------------
    # Detect Required Columns
    # ----------------------------------------------

    audit_cols = get_required_columns(
        audit_df
    )

    system_cols = get_required_columns(
        system_df
    )

    # ----------------------------------------------
    # Normalize WWN
    # ----------------------------------------------

    audit_wwns, system_wwns = (
        normalize_wwn_columns(
            audit_df,
            system_df,
            audit_cols,
            system_cols
        )
    )

    # ----------------------------------------------
    # Merge Reports
    # ----------------------------------------------

    merged_df = merge_reports(
        audit_df,
        system_df
    )

    # ----------------------------------------------
    # Run Validations
    # ----------------------------------------------

    wwn_result = compare_wwn(
        audit_df,
        system_df,
        audit_cols,
        system_cols,
        audit_wwns,
        system_wwns,
        report_name,
        system_name
    )

    id_result = compare_ldev_id(
        merged_df,
        audit_cols,
        system_cols,
        report_name,
        system_name
    )

    name_result = compare_ldev_name(
        merged_df,
        audit_cols,
        system_cols,
        report_name,
        system_name
    )

    size_result = compare_ldev_size(
        merged_df,
        audit_cols,
        system_cols,
        report_name,
        system_name
    )

    # ----------------------------------------------
    # Overall Status
    # ----------------------------------------------

    overall_pass = (

        wwn_result["passed"]

        and

        id_result["passed"]

        and

        name_result["passed"]

        and

        size_result["passed"]

    )

    # ----------------------------------------------
    # Final Result
    # ----------------------------------------------

    return {

        "passed": overall_pass,

        "wwn": wwn_result,

        "ldev_id": id_result,

        "name": name_result,

        "size": size_result

    }