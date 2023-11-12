import pdfplumber
import pandas as pd


def convert_pdf_to_data_frame(pdf_file_name) -> pd.DataFrame:
    """Extracts all the tables from pdf file and places them into one DataFrame"""

    with pdfplumber.open(pdf_file_name) as pdf:
        column_count = len(pdf.pages[0].extract_table()[1])
        df = pd.DataFrame(columns=[i for i in range(0, column_count)])

        for i, page in enumerate(pdf.pages):
            table = page.extract_table()

            for row in table:
                df.loc[len(df)] = row

    return df


def get_pdf_text(pdf_file_name) -> str:
    """Collects all the text from pdf file"""

    with pdfplumber.open(pdf_file_name) as pdf:
        page_text_list = [__get_page_text(page) for page in pdf.pages]

    return "\n".join(page_text_list)


def get_pdf_page_text(pdf_file_name, page_index) -> str:
    """Collects all the text from a page of pdf file"""

    with pdfplumber.open(pdf_file_name) as pdf:
        return __get_page_text(pdf.pages[page_index])


def __get_page_text(page):
    return page.extract_text(x_tolerance=1)
