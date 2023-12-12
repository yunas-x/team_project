from typing import override
import uuid
from parsers.core.protocols.ParserProtocol import ParserProtocol
from parsers.hse.basic.BasicParser import BasicParser
from parsers.hse.services_factory import get_temp_file_service
from parsers.services.http_service import get_html_page
from parsers.services.temp_file_service import TempFileService

temp_file_service: TempFileService = get_temp_file_service()


class BasicParserByLink(ParserProtocol):
    """Parser for basic HSE curricula"""

    @override
    def parse(self, payload: str) -> dict:
        """
        Parses basic HSE curricula pdf file
        :param payload: pdf file url
        """

        content = get_html_page(payload)

        pdf_file_name = uuid.uuid4().hex + ".pdf"
        pdf_file_full_path = temp_file_service.create_file(pdf_file_name, content)

        parser = BasicParser()
        result = parser.parse(pdf_file_full_path)

        temp_file_service.remove_file(pdf_file_full_path)

        # to be implemented
        return {}
