from converters import convert_pdf_to_data_frame, get_pdf_page_text
from parsing.parsing import parse_all


def parse_hse_basic_curricula(files_path):
    file_name = "2.pdf"
    full_path = files_path.joinpath(file_name)

    header_text_list = get_pdf_page_text(full_path, 0).split("\n")
    header_text_list = [text for text in header_text_list if text]

    df = get_data_frame_by_pdf_path(full_path)
    parse_all(header_text_list, df)


def get_data_frame_by_pdf_path(full_path):
    df = convert_pdf_to_data_frame(full_path)
    if "Федеральное" in df.iloc[0, 0]:
        df = df.drop([0])

    return df
