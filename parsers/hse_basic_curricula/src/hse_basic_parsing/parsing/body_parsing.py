import re

from src.hse_basic_parsing.parsing.data_classes.body_info import BodyInfo
from src.hse_basic_parsing.parsing.list_helpers import find_first_index


pattern = r'\"([А-яA-z,\- ]+)\"?'


def parse_body(document_df) -> list[BodyInfo]:
    first_row = document_df.iloc[0, :]

    is_course_type_exist = find_first_index(first_row, "Вид") is not None
    credits_col_index = find_first_index(first_row, "Трудоемкость")

    body_info_list = []

    specialization = ""

    for index, row in document_df.iterrows():
        row_values = row.tolist()
        first_value = row_values[0]

        if not isinstance(first_value, str) or not first_value.isdigit():
            continue

        if "Обеспечение качества" in row_values[1]:
            t = True

        if first_value == "1":
            n = document_df.iloc[index - 3, :].tolist()
            previous_row = document_df.iloc[index - 3, 1]
            if previous_row is None:
                specialization_match = None
            else:
                specialization_match = re.search(r'Дисц(?:[A-zА-я\" ])*?специализации ' + pattern, previous_row)

            if specialization_match is not None:
                specialization = specialization_match.group(1)
            else:
                previous_row = document_df.iloc[index - 2, 1]
                if previous_row is None:
                    specialization_match = None
                else:
                    specialization_match = re.search('Специализация ' + pattern, previous_row)

                if specialization_match is not None:
                    specialization = specialization_match.group(1)
                else:
                    specialization = ""

        body_info = BodyInfo()
        body_info.specialization = specialization
        body_info.course_name = row_values[1]

        if is_course_type_exist:
            body_info.course_type = row_values[2]
        else:
            pass

        body_info.credits = row_values[credits_col_index]

        last_value = row_values[len(row_values) - 1]

        # if value is not NaN
        if not isinstance(last_value, float):
            body_info.competence_codes = last_value.split(", ")

        body_info_list.append(body_info)

    return body_info_list
