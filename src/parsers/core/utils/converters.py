import pdfplumber
import pandas as pd


def convert_pdf_to_data_frame(pdf_file_name) -> pd.DataFrame:
    """Extracts all the tables from pdf file and places them into one DataFrame"""

    with pdfplumber.open(pdf_file_name) as pdf:
        column_count = len(pdf.pages[0].extract_table(table_settings={"text_x_tolerance": 1, "vertical_strategy": "lines_strict"})[1])
        df = pd.DataFrame(columns=[i for i in range(0, column_count)])

        for i, page in enumerate(pdf.pages):
            table = page.extract_table(table_settings={"text_x_tolerance": 1, "vertical_strategy": "lines_strict"})
            
            if table:
                for row in table:
                    df.loc[len(df)] = row

    return df


def get_pdf_page_text(pdf_file_name, page_index, layout=False, x_density=7.25) -> str:
    """Collects all the text from a page of pdf file"""

    with pdfplumber.open(pdf_file_name) as pdf:
        return __get_page_text(pdf.pages[page_index], layout, x_density)


def __get_page_text(page, layout=False, x_density=1.0):
    return page.extract_text(x_tolerance=1, layout=layout, x_density=x_density)