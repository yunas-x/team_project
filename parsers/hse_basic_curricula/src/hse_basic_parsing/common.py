import numpy as np
import pandas as pd

from converters import convert_pdf_to_data_frame, get_pdf_page_text
from parsing.parsing import parse_all
from src.hse_basic_parsing.parsing.list_helpers import find_first_index
from src.hse_basic_parsing.parsing.savers import save_df_to_excel


def parse_hse_basic_curricula(files_path):
    file_name = "3.pdf"
    full_path = files_path.joinpath(file_name)

    header_text_list = get_pdf_page_text(full_path, 0).split("\n")
    header_text_list = [text for text in header_text_list if text]

    df = get_data_frame_by_pdf_path(full_path)
    df = prepare_table(df)

    #print(df)#.iloc[:, 6:16])
    result_df = parse_all(header_text_list, df)

    save_df_to_excel(result_df, files_path.joinpath("sdf.xlsx"))


def get_data_frame_by_pdf_path(full_path):
    df = convert_pdf_to_data_frame(full_path)
    if "Федеральное" in df.iloc[0, 0]:
        df = df.drop([0])

    return df


# noinspection GrazieInspection
def prepare_table(df):
    """Changes input df to correct some issues"""

    # replace all the empty or white space strings with NaN
    df = df.apply(lambda x: x.str.strip()).replace('', np.nan)

    df.replace('\n', ' ', regex=True, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    pd.set_option('display.max_rows', 13)
    pd.set_option('display.max_columns', 12)
    pd.set_option('display.width', 1000)

    index = find_first_index(df.iloc[0, :], "Вид")
    if index is None:
        index = find_first_index(df.iloc[0, :], "Трудоемкость")

    # if there are columns between colum with index 1 and "Вид" or "Трудоемкость" column,
    # it's necessary to concatenate these columns because of some error
    # example:
    # 1,  2,    3,   4          - column names
    # Dat a cul ture О          - data

    if index - 1 != 1:
        new_column_values = []

        for row_index in range(len(df)):
            new_row_value = ""

            for col_index in range(1, index):
                value = df.iloc[row_index, col_index]
                if isinstance(value, str):
                    new_row_value += value

            new_column_values.append(new_row_value)

        df.drop(np.arange(1, index), axis=1, inplace=True)
        df.insert(1, column="1", value=new_column_values)

    return df
