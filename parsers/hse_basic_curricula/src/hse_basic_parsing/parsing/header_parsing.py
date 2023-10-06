from .regex_helpers import get_words_in_quotes, get_speciality_code_list, remove_initials_from_text,\
    get_speciality_list, find_first_match
from .list_helpers import find_first_index


__pointer = 0


def __get_pointer():
    global __pointer

    return __pointer


def __increase_pointer(value=1):
    global __pointer
    __pointer += value


def parse_header(header_text_list, header_info):
    """Parses data from a list of texts and places it into HeaderInfo"""

    start_index = find_first_index(header_text_list, "Направление ")
    __increase_pointer(start_index)

    header_info.speciality_codes = __get_speciality_code_list(header_text_list)
    header_info.speciality_names = __get_speciality_name_list(header_text_list)

    __increase_pointer_for_programme_row(header_text_list)
    header_info.programme_name = __get_programme_name(header_text_list)

    __increase_pointer_for_faculty(header_text_list)
    header_info.faculty = __get_faculty(header_text_list)

    header_info.enrollment_year = __get_enrollment_year(header_text_list)
    header_info.study_year_count = __get_study_year_count(header_text_list)

    __increase_pointer()

    header_info.degree = __get_degree(header_text_list)


def __get_speciality_code_list(entry_list):
    """Finds all the speciality codes in a list of texts"""

    entry_index = __get_pointer()

    entry = entry_list[entry_index]
    code_list = []

    first_row_codes = get_speciality_code_list(entry)
    code_list.extend(first_row_codes)

    # the structure of header may consist of the following:
    # ...
    # Направление 01.02.03 Экономика,
    # trash sentence
    # 04.05.06 Менеджмент, ...
    # ...

    entry = entry_list[entry_index + 2]
    code_list.extend(get_speciality_code_list(entry))

    return code_list


def __get_speciality_name_list(entry_list):
    """Finds all the speciality names in a list of texts"""

    entry = entry_list[__get_pointer()]
    entry = remove_initials_from_text(entry)

    speciality_rows = get_speciality_list(entry)

    speciality_names = []
    speciality_names.extend([__get_clear_speciality_name(row[1]) for row in speciality_rows])

    __increase_pointer()

    # check the string after next one
    entry = entry_list[__get_pointer() + 1]
    entry = remove_initials_from_text(entry)
    speciality_rows = get_speciality_list(entry)

    if len(speciality_rows) > 0:
        speciality_names.extend([__get_clear_speciality_name(row[1]) for row in speciality_rows])

        __increase_pointer(2)

    return speciality_names


def __get_clear_speciality_name(raw_speciality_name):
    return raw_speciality_name.replace("___________", "").strip(" \"")


def __increase_pointer_for_programme_row(header_text_list):
    continuation_index = find_first_index(header_text_list, "Образовательная программа")
    if not continuation_index:
        continuation_index = find_first_index(header_text_list, "Магистерская программа")

    __increase_pointer(continuation_index - __get_pointer())


def __get_programme_name(entry_list):
    programme_row = entry_list[__get_pointer()]
    programme = get_words_in_quotes(programme_row)

    __increase_pointer()

    return programme.strip("\"")


def __increase_pointer_for_faculty(header_text_list):
    continuation_index = find_first_index(header_text_list, "Годы обучения:")
    __increase_pointer(continuation_index - __get_pointer() - 1)


def __get_faculty(entry_list):
    faculty_row = entry_list[__get_pointer()]

    __increase_pointer()

    return faculty_row.replace("Реализующее подразделение: ", "")


def __get_enrollment_year(entry_list):
    """
    Finds the enrollment year in the text.
    For a row "Годы обучения: 2022/2023 учебный год - 2025/2026 учебный год" 2022 will be returned.
    """

    enrollment_row = entry_list[__get_pointer()]
    year = find_first_match(r"\d{4}/", enrollment_row)

    __increase_pointer()

    return year.replace("/", "")


def __get_study_year_count(entry_list):
    """
    Finds study years in the text.
    For a row "Срок обучения: 4 года" 4 will be returned.
    """

    study_years_row = entry_list[__get_pointer()]
    years = find_first_match(r"\d{1,2}", study_years_row)

    __increase_pointer()

    return years


def __get_degree(entry_list):
    degree_row = entry_list[__get_pointer()]

    return degree_row.replace("Уровень образования: ", "")
