import numpy as np
from pandas import DataFrame

from parsers.core.utils.converters import convert_pdf_to_data_frame


def get_data_frame_by_pdf_path(full_path: str, table_settings: dict = {}):
    df = convert_pdf_to_data_frame(full_path, table_settings=table_settings)
    if "Федеральное" in df.iloc[0, 0]:
        df = df.drop([0])

    return df


def prepare_table(df: DataFrame) -> DataFrame:
    """
    Changes input DataFrame to correct some issues
    :return: New DataFrame
    """

    # replace all the empty or white space strings with NaN
    df = df.apply(lambda x: x.str.strip()).replace('', np.nan)

    df.replace('\n', ' ', regex=True, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    return df
