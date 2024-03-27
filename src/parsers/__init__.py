import json
from pathlib import Path
from parsers.JsonValidator import JsonValidator
from parsers.core.protocols.ParserProtocol import ParserProtocol
from typing import Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
from config import PARSING_PROCESS_COUNT, VALIDATION_PROCESS_COUNT
import logging


def parse(folder_with_pdf_files_path: str, folder_to_save_json_files_path: str, parser: ParserProtocol, process_count: int = PARSING_PROCESS_COUNT):
    """Parse pdf files and save resulting json files

    Args:
        folder_with_pdf_files_path (str): path to source folder
        folder_to_save_json_files_path (str): path to output folder
        parser (ParserProtocol): Parser that should be used
        process_count (int, optional): Amount of processes to be used when parsing. Defaults to config.PARSING_PROCESS_COUNT.
    """
    pdf_folder_path = Path(folder_with_pdf_files_path)
    all_file_names = [full_file_name.name for full_file_name in list(pdf_folder_path.iterdir())]
    
    if process_count == 1:
        __parse(all_file_names, folder_with_pdf_files_path, folder_to_save_json_files_path, parser)
    
    else:
        file_chunk_length = len(all_file_names) // process_count
        file_chunks = [all_file_names[file_chunk_length * i:file_chunk_length * (i+1)] for i in range(0, process_count)]
        
        if file_chunk_length * (process_count - 1) < len(all_file_names):
            file_chunks[-1].extend(all_file_names[file_chunk_length * (process_count):])

        with ProcessPoolExecutor(max_workers=process_count) as executor:
            futures = {executor.submit(__parse, file_chunk, folder_with_pdf_files_path, folder_to_save_json_files_path, parser): file_chunk for file_chunk in file_chunks}
    

def __parse(all_file_names: list[str], pdf_folder_path: str, folder_to_save_json_files_path: str, parser: ParserProtocol):
    """Parse pdf files and save resulting json files

    Args:
        folder_with_pdf_files_path (str): path to source folder
        folder_to_save_json_files_path (str): path to output folder
        parser (ParserProtocol): Parser that should be used
    """

    pdf_folder_path = Path(pdf_folder_path)
    json_folder_path = Path(folder_to_save_json_files_path)

    for i, file_name in enumerate(all_file_names):
        try:
            if file_name[-3:] != "pdf":
                continue

            logging.info("----")
            logging.info("started for: " + str(file_name))
            
            res = parser.parse(str(pdf_folder_path / file_name))
            
            with open(json_folder_path / (str(file_name) + ".json"), "w+", encoding="utf-8") as json_file:
                json.dump(res, json_file, ensure_ascii=False)
                
            logging.info(str((i + 1)) + " of " + str(len(all_file_names)) + " passed: " + str(file_name))

        except Exception as e:
            logging.exception(e)


def validate(folder_with_pdf_files_path: str, folder_to_save_json_files_path: str, json_schema_full_path: str, process_count: int = VALIDATION_PROCESS_COUNT):
    """Validate json files

    Args:
        folder_with_pdf_files_path (str): path to source folder
        folder_to_save_json_files_path (str): path to output folder with json files
        json_schema_full_path (str): Path to json schema that should be used for validation
        process_count (int, optional): Amount of processes to be used when validating. Defaults to config.PARSING_PROCESS_COUNT.
    """
    
    pdf_folder_path = Path(folder_with_pdf_files_path)
    all_file_names = [full_file_name.name for full_file_name in list(pdf_folder_path.iterdir())]
    
    if process_count == 1:
        logging.info(__validate(all_file_names, folder_to_save_json_files_path, json_schema_full_path))
    
    else:
        file_chunk_length = len(all_file_names) // process_count
        file_chunks = [all_file_names[file_chunk_length * i:file_chunk_length * (i+1)] for i in range(0, process_count)]
        
        if file_chunk_length * (process_count - 1) < len(all_file_names):
            file_chunks[-1].extend(all_file_names[file_chunk_length * (process_count):])


        with ProcessPoolExecutor(max_workers=process_count) as executor:
            futures = {executor.submit(__validate, file_chunk, folder_to_save_json_files_path, json_schema_full_path): file_chunk for file_chunk in file_chunks}
            res = []
            
            for future in as_completed(futures):
                try:
                    res.append(future.result())
                except Exception as exc:
                    logging.info("There was an error. {}".format(exc))
                    
            for item in res:
                logging.info(item)


def __validate(all_file_names: list[str], folder_to_save_json_files_path: str, json_schema_full_path: str) -> str:
    """Validate json files

    Args:
        folder_with_pdf_files_path (str): path to source folder
        folder_to_save_json_files_path (str): path to output folder with json files
        json_schema_full_path (str): Path to json schema that should be used for validation
    """
    output = ''
    counter = 0
    nonexist = 0
    json_folder_path = Path(folder_to_save_json_files_path)
    if json_schema_full_path:
        with open(json_schema_full_path, encoding="utf-8") as json_file:
            json_schema = json.load(json_file)

        for i, file_name in enumerate(all_file_names):
            result, err = __validate_scheme(str(json_folder_path / (str(file_name) + ".json")), json_schema)

            if result is None:
                logging.info(str((i + 1)) + " of " + str(len(all_file_names)) + ", does not exist: " + str(file_name))
                output += str((i + 1)) + " of " + str(len(all_file_names)) + ", does not exist: " + str(file_name) + '\n'
                nonexist += 1
            elif result:
                logging.info(str((i + 1)) + " of " + str(len(all_file_names)) + ", correct: " + str(file_name))
            else:
                logging.info(str((i + 1)) + " of " + str(len(all_file_names)) + ", NOT correct: " + str(file_name))
                output += str((i + 1)) + " of " + str(len(all_file_names)) + ", NOT correct: " + str(file_name) + '\n'
                output += err
                counter += 1
            
    output += '\n\nNot passed: ' + str(counter)
    output += "\nDon't exist: " + str(nonexist) + '\n\n'
    
    return output


def __validate_scheme(full_res_json_file_name: str, json_schema: dict) -> Tuple[Optional[bool], Optional[str]]:
    try:
        with open(full_res_json_file_name, encoding="utf-8") as json_file:
            data = json.load(json_file)
            validator = JsonValidator(json_schema)

            valid, errors = validator.validate(data)
            error_string = ''
            
            if not valid:
                for er in errors:
                    error_string += str(er) + '\n'
    
            return valid, error_string
    except Exception as e:
        logging.exception(e)
        return None, None
