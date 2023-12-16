from typing import override
from parsers.core.utils.converters import get_pdf_page_text
from parsers.hse.basic.basic_helpers import concat_for_basic
from parsers.hse.basic.body_parsing import parse_body
from parsers.hse.basic.data_classes.header_info import HeaderInfo
from parsers.hse.basic.header_parsing import parse_header
from parsers.core.protocols.ParserProtocol import ParserProtocol
from parsers.hse.basic.json_converter import convert_to_json
from parsers.hse.utils import get_data_frame_by_pdf_path, prepare_table


class BasicParser(ParserProtocol):
    """Parser for basic HSE curricula"""

    @override
    def parse(self, payload: str) -> dict:
        """
        Parses basic HSE curricula pdf file
        :param payload: pdf file path
        """

        pdf_path = payload

        header_text_list = get_pdf_page_text(pdf_path, 0).split("\n")
        header_text_list = [text for text in header_text_list if text]

        df = get_data_frame_by_pdf_path(pdf_path,
                                        table_settings={"text_x_tolerance": 1, "vertical_strategy": "lines_strict"})
        df = prepare_table(df)
        df = concat_for_basic(df)

        header_info = HeaderInfo()
        parse_header(header_text_list, header_info)

        body_info_list = parse_body(df)

        return convert_to_json(header_info, body_info_list)
