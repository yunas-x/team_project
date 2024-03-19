from typing import override
import pandas as pd
from parsers.core.protocols.ParserProtocol import ParserProtocol
from parsers.core.utils.converters import get_pdf_page_text
from parsers.hse.annual.annual_helpers import get_programme_name, get_year_and_enrolled_in, get_hours, get_body_row_list_without_year
from parsers.hse.utils import get_data_frame_by_pdf_path
from parsers.hse.annual.json_converter import convert_to_json
from parsers.hse.annual.data_classes.header_info import HeaderInfo


class AnnualParser(ParserProtocol):
    """Parser for annual HSE curricula"""

    @override
    def parse(self, payload: str) -> dict:
        """
        Parses annual HSE curricula pdf file
        :param payload: pdf file path
        """

        pdf_path = payload

        header_text_list = get_pdf_page_text(pdf_path, 0, True).split("\n")
        header_text_list = [text.strip() for text in header_text_list if text]
        
        df = get_data_frame_by_pdf_path(pdf_path,
                                        table_settings={"text_x_tolerance": 1, "vertical_strategy": "lines_strict"})

        header_info = HeaderInfo()
        header_info.programme_name = get_programme_name(header_text_list)
        year, header_info.enrollment_year = get_year_and_enrolled_in(header_text_list)

        body_row_list = get_body_row_list_without_year(df)
        for row in body_row_list:
            row.course_year = year

        return convert_to_json(header_info, body_row_list)
