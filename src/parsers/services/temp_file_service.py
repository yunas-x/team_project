from pathlib import Path
from typing import Any


class TempFileService:

    def __init__(self, temp_folder_path: str):
        self.__temp_folder_path = temp_folder_path

    def create_file(self, file_name: str, file_content: Any):
        """
        Creates a new file with the specified name and content in temp directory
        :param file_name: string like 'example.pdf'
        :param file_content: something to write into a creating file
        :returns: Full path of a created file
        """

        file_path = self.get_full_temp_file_path(file_name)

        with open(file_path, 'wb') as f:
            f.write(file_content)

        return file_path

    def remove_file(self, file_name: str):
        """
        Removes a file with the specified name from temp directory
        :param file_name: string like 'example.pdf'
        """

        Path.unlink(Path(self.get_full_temp_file_path(file_name)))

    def get_full_temp_file_path(self, file_name: str) -> str:
        """
        Concatenates temp folder directory and input file name
        :param file_name: string like 'example.pdf'
        :returns: string like '/temp_folder/example.pdf'
        """

        return str(Path(self.__temp_folder_path).joinpath(file_name))
