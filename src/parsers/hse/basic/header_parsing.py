from .data_classes.header_info import HeaderInfo
from ...core.utils.list_helpers import find_first_index
from ...core.utils.regex_helpers import get_speciality_code_list, get_speciality_list, remove_initials_from_text, \
    get_words_in_quotes, find_first_match


class Pointer:
    """Pointer indicates what index to continue reading rows from"""

    def __init__(self):
        self.__pointer = 0

    @property
    def pointer(self):
        return self.__pointer

    def increase_pointer(self, value=1):
        self.__pointer += value


def parse_header(header_text_list, header_info: HeaderInfo):
    """Parses data from a list of texts and places it into HeaderInfo"""

    pointer = Pointer()

    # to skip first unnecessary rows, start with the row that contains the word "Направление"
    start_index = find_first_index(header_text_list, "Направление ")
    pointer.increase_pointer(start_index)

    header_info.speciality_codes = get_speciality_codes(header_text_list, start_index)
    header_info.speciality_names = get_speciality_name_list(header_text_list, pointer)

    increase_pointer_for_programme_row(header_text_list, pointer)

    header_info.programme_name = get_programme_name(header_text_list, pointer)

    increase_pointer_for_faculty(header_text_list, pointer)

    header_info.faculty = get_faculty(header_text_list, pointer)

    header_info.enrollment_year = get_enrollment_year(header_text_list, pointer)
    header_info.study_year_count = get_study_year_count(header_text_list, pointer)

    # to skip 1 row
    pointer.increase_pointer()

    header_info.degree = get_degree(header_text_list, pointer)


def get_speciality_codes(entry_list, start_index):
    """Finds all the speciality codes in a list of texts"""

    entry = entry_list[start_index]
    code_list = []

    first_row_codes = get_speciality_code_list(entry)
    code_list.extend(first_row_codes)

    # the structure of header may consist of the following:
    # ...
    # Направление 01.02.03 Экономика,
    # trash sentence
    # 04.05.06 Менеджмент, ...
    # ...

    entry = entry_list[start_index + 2]
    code_list.extend(get_speciality_code_list(entry))

    return code_list


def get_speciality_name_list(entry_list, pointer: Pointer):
    """Finds all the speciality names in a list of texts"""

    entry = entry_list[pointer.pointer]
    entry = remove_initials_from_text(entry)

    speciality_rows = get_speciality_list(entry)

    speciality_names = []
    speciality_names.extend([get_clear_speciality_name(row[1]) for row in speciality_rows])

    pointer.increase_pointer()

    # check the string after next one
    entry = entry_list[pointer.pointer + 1]
    entry = remove_initials_from_text(entry)
    speciality_rows = get_speciality_list(entry)

    if len(speciality_rows) > 0:
        speciality_names.extend([get_clear_speciality_name(row[1]) for row in speciality_rows])

        # increase pointer because two rows were taken
        pointer.increase_pointer(2)

    return speciality_names


def get_clear_speciality_name(raw_speciality_name):
    return raw_speciality_name.replace("___________", "").strip(" \"")


def increase_pointer_for_programme_row(header_text_list, pointer: Pointer):
    continuation_index = find_first_index(header_text_list, "Образовательная программа")
    if not continuation_index:
        continuation_index = find_first_index(header_text_list, "Магистерская программа")

    pointer.increase_pointer(continuation_index - pointer.pointer)


def get_programme_name(entry_list, pointer: Pointer):
    programme_row = entry_list[pointer.pointer]
    programme = get_words_in_quotes(programme_row)

    pointer.increase_pointer()

    return programme.strip("\"")


def increase_pointer_for_faculty(header_text_list, pointer: Pointer):
    continuation_index = find_first_index(header_text_list, "Годы обучения:")

    pointer.increase_pointer(continuation_index - pointer.pointer - 1)


def get_faculty(entry_list, pointer: Pointer):
    faculty_row = entry_list[pointer.pointer]

    pointer.increase_pointer()

    return faculty_row.replace("Реализующее подразделение: ", "")


def get_enrollment_year(entry_list, pointer: Pointer):
    """
    Finds the enrollment year in the text.
    For a row "Годы обучения: 2022/2023 учебный год - 2025/2026 учебный год" 2022 will be returned.
    """

    enrollment_row = entry_list[pointer.pointer]
    year = find_first_match(r"\d{4}/", enrollment_row)

    pointer.increase_pointer()

    return year.replace("/", "")


def get_study_year_count(entry_list, pointer: Pointer):
    """
    Finds study years in the text.
    For a row "Срок обучения: 4 года" 4 will be returned.
    """

    study_years_row = entry_list[pointer.pointer]
    years = find_first_match(r"\d{1,2}", study_years_row)

    pointer.increase_pointer()

    return years


def get_degree(entry_list, pointer: Pointer):
    degree_row = entry_list[pointer.pointer]

    return degree_row.replace("Уровень образования: ", "")
