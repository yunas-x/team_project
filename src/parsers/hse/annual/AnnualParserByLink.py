import uuid
from typing import override
from parsers.core.protocols.ParserProtocol import ParserProtocol
from parsers.hse.annual.AnnualParser import AnnualParser
from parsers.hse.services_factory import get_temp_file_service
from parsers.services.http_service import get_html_page
from parsers.services.temp_file_service import TempFileService

temp_file_service: TempFileService = get_temp_file_service()


class AnnualParserByLink(ParserProtocol):
    """Parser for annual HSE curricula"""

    @override
    def parse(self, payload: str) -> dict:
        """
        Parses annual HSE curricula pdf file
        :param payload: pdf file url
        """

        content = get_html_page(payload)

        pdf_file_name = uuid.uuid4().hex + ".pdf"
        pdf_file_full_path = temp_file_service.create_file(pdf_file_name, content)

        parser = AnnualParser()

        try:
            result = parser.parse(pdf_file_full_path)
        finally:
            temp_file_service.remove_file(pdf_file_full_path)

        print(result)
        # to be implemented
        return {}
