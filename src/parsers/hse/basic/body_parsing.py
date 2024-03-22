import re
from typing import Any
from .data_classes.body_info import BodyRowInfo
from ...core.classifiers.course_types import CourseType
from ...core.utils.list_helpers import find_first_index


def parse_body(document_df) -> list[BodyRowInfo]:
    first_row = document_df.iloc[0, :]

    has_course_type_column = find_first_index(first_row, "Вид") is not None
    credits_col_index = find_first_index(first_row, "Трудоемкость")
    last_col_index = len(document_df.columns) - 1

    body_info_list = []

    specialization = ""
    previous_course_type = CourseType.ELECTIVE_TYPE

    # row_number initially equals to 1
    for row_index, row in document_df.iterrows():
        row_values = row.tolist()
        first_value = row_values[0]

        if not isinstance(first_value, str) or not first_value.isdigit():
            continue

        # if row's "Код цикла" isn't "1", not change specialization name
        # otherwise, try to find name in previous rows
        possible_specialization = try_define_specialization(document_df, row_index, first_value)
        if possible_specialization is not None:
            specialization = possible_specialization

        body_info = BodyRowInfo()
        body_info.specialization = specialization
        body_info.course_name = row_values[1]

        if has_course_type_column:
            body_info.course_type = CourseType(row_values[2])
        else:
            previous_course_type = define_course_type(document_df, row_index, previous_course_type)
            body_info.course_type = previous_course_type

        credits_list, years = __get_credits_and_years(row_values, credits_col_index, last_col_index)
        body_info.credits.extend(credits_list)
        body_info.course_years.extend(years)

        last_value = row_values[last_col_index]

        # value might be undefined
        if isinstance(last_value, str):
            body_info.competence_codes = [code.strip() for code in last_value.split(",") if code.strip() != ""]

        body_info_list.append(body_info)

    return body_info_list


def try_define_specialization(document_df, row_index, row_first_value) -> str | None:
    if row_first_value == "1":
        specialization_pattern = r'\"([А-яA-z,\- ]+)\"?'

        # noinspection SpellCheckingInspection
        pattern = r'Дисц(?:[A-zА-я\" ])*?специализации ' + specialization_pattern

        possible_name = try_get_specialization_name(document_df, row_index - 2, pattern)

        if possible_name is not None:
            return possible_name

        pattern = 'Специализация ' + specialization_pattern

        possible_name = try_get_specialization_name(document_df, row_index - 2, pattern)

        if possible_name is not None:
            return possible_name

        return ""

    return None


def try_get_specialization_name(df, row_index, row_specialization_name_pattern) -> str | None:
    previous_row_course_name = df.iloc[row_index, 1]

    if previous_row_course_name is None:
        specialization_match = None
    else:
        # Specialization name might be written in rows like this
        specialization_match = re.search(row_specialization_name_pattern, previous_row_course_name)

    if specialization_match is not None:
        return specialization_match.group(1)

    return None


def define_course_type(document_df, row_index, previous_course_type) -> CourseType:
    previous_row = get_df_row(document_df, row_index - 1)

    # document structure:
    # 4 previous data...
    # Базовый профессиональный         - block header
    #   Дисциплины предметных областей - block subhead
    # 1     Анализ данных на Python    - block content row
    # 2     etc.

    # if previous row isn't the block subhead,
    # course type equals to previous one (was defined before)
    if isinstance(previous_row[0], str):
        return previous_course_type

    # noinspection SpellCheckingInspection
    subhead_names = [
        "Дисциплины *по *выбору",
        r"Научно[ -]*исследовательская",
        r"Дополнительные *дисциплины",
        "Корзина",
        r"Научно[ -]*исследовательский *семинар *по *выбору",
        r"Дополнительные *факультативные"
    ]

    previous_row_second_value = previous_row[1]  # contains course name

    for subhead_name in subhead_names:
        course_type_match = re.search(subhead_name, previous_row_second_value)
        if course_type_match is not None:
            return CourseType.ELECTIVE_TYPE

    block_header_name = find_block_header_name(document_df, row_index)

    if block_header_name is None:
        return CourseType.COMPULSORY_TYPE

    # noinspection SpellCheckingInspection
    header_names = [
        r"Дисц(?:[A-zА-я\" ])*?специализации ",
        r"Семинары *и *профориентационные *дисциплины",
        "ДОЦ"
    ]

    subhead_names = [
        r"Обязательные *дисциплины",
        r"Обязательные *семинары",
        r"Обязательные *дисциплины"
    ]

    # for example:
    # if block header = "ДОЦ" and block subhead = "Обязательные дисциплины",
    # course type is elective one

    for index, header_name in enumerate(header_names):
        course_type_match = re.search(header_name, block_header_name)
        if course_type_match is not None:
            course_type_match = re.search(subhead_names[index], previous_row_second_value)

            if course_type_match is None:
                return CourseType.ELECTIVE_TYPE

    return CourseType.COMPULSORY_TYPE


# noinspection GrazieInspection
def find_block_header_name(document_df, cur_row_index):
    """
    :param document_df: DataFrame with pdf table
    :param cur_row_index: Index of the first block content row
    """

    row_index = cur_row_index

    # (block header always goes before block subhead,
    # both can be defined if first column value in the row doesn't contain a number)
    previous_row = get_df_row(document_df, row_index - 1)
    possible_block_header = get_df_row(document_df, row_index - 2)

    # if first column value of previous row doesn't contain a number (is block subhead)
    # and first column value of row before previous one also doesn't contain a number (is block header)
    # or row index < 2, leave loop
    while (isinstance(previous_row[0], str) or isinstance(possible_block_header[0], str)) and row_index > 1:
        row_index -= 1

        previous_row = get_df_row(document_df, row_index - 1)
        possible_block_header = get_df_row(document_df, row_index - 2)

    return possible_block_header[1]


def get_df_row(df, row_index) -> list[Any]:
    return df.iloc[row_index, :]


def __get_credits_and_years(cur_row_values, credits_col_index, last_col_index):
    credits_list = []
    years = []

    for col_index in range(credits_col_index + 1, last_col_index):
        credits_value = cur_row_values[col_index]

        credits_match = re.search(r"\d+", str(credits_value))
        if credits_match is not None:
            credits_list.append(int(credits_match.group(0)))
            years.append(col_index - credits_col_index)

    return credits_list, years
