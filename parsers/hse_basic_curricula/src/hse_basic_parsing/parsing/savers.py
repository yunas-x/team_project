import pandas as pd


def save_df_to_excel(df, excel_full_path):
    df.to_excel(excel_full_path)
