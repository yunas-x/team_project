import json
from pathlib import Path
from parsers.JsonValidator import JsonValidator
from parsers.hse.basic.BasicParser import BasicParser


def start_stress_testing(folder_with_pdf_files_path: str, folder_to_save_json_files_path: str,
                         json_schema_full_path: str):
    parser = BasicParser()
    # pd.set_option('display.max_rows', 13)
    # pd.set_option('display.max_columns', 12)
    # pd.set_option('display.width', 1000)

    pdf_folder_path = Path(folder_with_pdf_files_path)
    json_folder_path = Path(folder_to_save_json_files_path)
    all_file_names = [full_file_name.name for full_file_name in list(pdf_folder_path.iterdir())]

    # for i, file_name in enumerate(all_file_names):
    #     try:
    #         print("----")
    #         print("started for: " + str(file_name))
    #         res = parser.parse(str(pdf_folder_path / file_name))
    #         with open(json_folder_path / (str(file_name) + ".json"), "w", encoding="utf-8") as json_file:
    #             json.dump(res, json_file, ensure_ascii=False)
    #         print(str((i + 1)) + " of " + str(len(all_file_names)) + " passed: " + str(file_name))
    #     except Exception as e:
    #         print(e)
    #         print("failed: " + str(file_name))
    #         break

    with open(json_schema_full_path, encoding="utf-8") as json_file:
        json_schema = json.load(json_file)

    for i, file_name in enumerate(all_file_names):
        result = validate_scheme(str(json_folder_path / (str(file_name) + ".json")), json_schema)

        if result:
            print(str((i + 1)) + " of " + str(len(all_file_names)) + ", correct: " + str(file_name))
        else:
            print(str((i + 1)) + " of " + str(len(all_file_names)) + ", NOT correct: " + str(file_name))

    for file_name in all_file_names:
        (json_folder_path / (str(file_name) + ".json")).unlink()


def validate_scheme(full_res_json_file_name: str, json_schema: dict) -> bool:
    with open(full_res_json_file_name, encoding="utf-8") as json_file:
        data = json.load(json_file)
        validator = JsonValidator(json_schema)

        return validator.validate(data)
