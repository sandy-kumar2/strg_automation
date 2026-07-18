import pandas as pd


def load_mapping_sheet(file_path):

    df = pd.read_excel(file_path)

    # Remove Unnamed columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    return df


def load_storage_export(file_path):

    df = pd.read_excel(file_path)

    # Remove Unnamed columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    return df
    