from typing import override
import pandas as pd
from parsers.core.protocols.ParserProtocol import ParserProtocol
from parsers.core.utils.converters import get_pdf_page_text
from parsers.hse.utils import get_data_frame_by_pdf_path
from parsers.core.utils.converters import convert_pdf_to_data_frame_with_row_colors
from parsers.itmo.itmo_helpers import get_courses, get_programme_info
import time


class ItmoParser(ParserProtocol):
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
        
        df = convert_pdf_to_data_frame_with_row_colors(pdf_path, 1, table_settings={})
        
        programme_info = get_programme_info(header_text_list)
        programme_info['courses'] = get_courses(df)
        
        return {'ProgramInfo': programme_info}
