import pdfplumber
import pandas as pd


def convert_pdf_to_data_frame(pdf_file_name):
    with pdfplumber.open(pdf_file_name) as pdf:
        column_count = len(pdf.pages[0].extract_table()[1])
        df = pd.DataFrame(columns=[i for i in range(0, column_count)])

        for i, page in enumerate(pdf.pages):
            table = page.extract_table()

            for row in table:
                df.loc[len(df)] = row

    return df


def get_pdf_text(pdf_file_name):
    with pdfplumber.open(pdf_file_name) as pdf:
        page_text_list = [page.extract_text(x_tolerance=1) for page in pdf.pages]

    return "\n".join(page_text_list)


def get_pdf_page_text(pdf_file_name, page_index):
    with pdfplumber.open(pdf_file_name) as pdf:
        page_text = pdf.pages[page_index].extract_text(x_tolerance=1)

    return page_text
