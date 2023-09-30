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
