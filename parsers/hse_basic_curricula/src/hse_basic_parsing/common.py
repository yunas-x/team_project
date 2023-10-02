from converters import convert_pdf_to_data_frame, get_pdf_page_text
from parsing.parsing import parse


def parse_hse_basic_curricula(files_path):
    df = convert_pdf_to_data_frame(files_path.joinpath("2.pdf"))

    header_text_list = get_pdf_page_text(files_path.joinpath("2.pdf"), 0).split("\n")
    header_text_list = [text for text in header_text_list if text]

    parse(header_text_list, df)
    #print(get_pdf_page_text(files_path.joinpath("2.pdf"), 0))
    # print(df.iloc[5, :])
