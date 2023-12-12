from pathlib import Path

from parsers.services.temp_file_service import TempFileService


def get_temp_file_service() -> TempFileService:
    return TempFileService(str(Path(__file__).parent.joinpath("temp_files")))
