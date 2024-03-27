import pdfplumber
import pandas as pd
import time
from config import PDF_COLOR_SNAP_TOLERANCE
from pdfplumber.table import Table

def convert_pdf_to_data_frame(pdf_file_name: str, table_settings: dict = {}) -> pd.DataFrame:
    """Extracts all the tables from pdf file and places them into one DataFrame"""

    with pdfplumber.open(pdf_file_name) as pdf:
        tables = pdf.pages[1].extract_table(table_settings=table_settings)
        column_count = len(tables[1])
        df = pd.DataFrame(columns=[i for i in range(0, column_count)])

        for i, page in enumerate(pdf.pages):
            table = page.extract_table(table_settings=table_settings)
            
            if table:
                for row in table:
                    # When table starts on one page and ends on another, sometimes the part that is on the second page
                    # does not have programme rows and because of this it has reduced count of columns
                    # Those rows can be skipped, since they don't carry any important info
                    if len(row) == len(df.columns):
                        df.loc[len(df)] = row

    return df


def convert_pdf_to_data_frame_with_row_colors(pdf_file_name: str, starting_page: int = 0, table_settings: dict = {}) -> pd.DataFrame:
    """Extracts all the tables from pdf file and places them into one DataFrame with colors in the last column

    Args:
        pdf_file_name (str): Path to pdf
        start_page (int, optional): Page where table is expected to start. If value is equal to -1, page will be automatically selected. Defaults to -1.
        table_settings (dict, optional): Settings for PdfPlumber. Defaults to {}.

    Returns:
        pd.DataFrame: Pandas dataframe with table + last column contains the float rgb color of rows
    """
    with pdfplumber.open(pdf_file_name) as pdf:      
        if starting_table := pdf.pages[starting_page].find_table(table_settings=table_settings):
            column_count = len(starting_table.rows[0].cells) + 1
            df = pd.DataFrame(columns=[i for i in range(0, column_count)])
        
            __append_df_from_table(df, starting_table)
            for i in range(starting_page+1, len(pdf.pages)):
                if table := pdf.pages[i].find_table(table_settings=table_settings):
                    __append_df_from_table(df, table)
    
    return df


def __append_df_from_table(df: pd.DataFrame, table: Table):
    texts = table.extract()
    
    for row in texts:
        row.append(None)
    
    colors = __get_colored_rows(table)
    for row_n in colors.keys():
        texts[row_n][-1] = colors[row_n]
        
    # Skip table headers
    non_header_ind = 0
    if len(df) > 0:
        for i, row in enumerate(texts):
            if list(df.iloc[i]) != row:
                non_header_ind = i
                break
    
    for row in texts[non_header_ind:]:
        # When table starts on one page and ends on another, sometimes the part that is on the second page
        # does not have programme rows and because of this it has reduced count of columns
        # Those rows can be skipped, since they don't carry any important info
        if len(row) == len(df.columns):
            df.loc[len(df)] = row


def __get_colored_rects(rects: dict):
    return [r for r in rects if r['non_stroking_color'] != (1,) and r['non_stroking_color'] != (0,)]


def __get_colored_rows(table: Table):
    rects = __get_colored_rects(table.page.rects)
    colors = {}
    for rect in rects:
        for i, row in enumerate(table.rows):
            if abs(row.bbox[1]-rect['top']) < PDF_COLOR_SNAP_TOLERANCE:
                colors[i] = rect['non_stroking_color']
    return colors


def get_pdf_page_text(pdf_file_name, page_index, layout=False, x_density=7.25) -> str:
    """Collects all the text from a page of pdf file"""
    with pdfplumber.open(pdf_file_name) as pdf:
        return __get_page_text(pdf.pages[page_index], layout, x_density)


def __get_page_text(page, layout=False, x_density=1.0):
    return page.extract_text(x_tolerance=1, layout=layout, x_density=x_density)
