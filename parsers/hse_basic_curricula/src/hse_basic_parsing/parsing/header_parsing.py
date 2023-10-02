import re
from .helpers import get_speciality_code_matching, get_words_in_quotes, get_speciality_code_list


def parse_header(header_text_list, header_info):
    text_with_speciality = list(filter(lambda text: "Направление " in text, header_text_list))[0]
    text_index = header_text_list.index(text_with_speciality)

    header_info.speciality_codes = _get_speciality_code_list(header_text_list, text_index)
    text_index, header_info.speciality_names = _get_speciality_name(header_text_list, text_index)

    text_index, header_info.programme_name = _get_programme_name(header_text_list, text_index)


def _get_speciality_code_list(entry_list, start_index):
    """Finds all speciality codes in list of texts"""

    entry = entry_list[start_index]
    code_list = []

    first_row_codes = get_speciality_code_list(entry)
    code_list.extend(first_row_codes)

    entry = entry_list[start_index + 2]
    code_list.extend(get_speciality_code_list(entry))

    return code_list


def _get_speciality_name(entry_list, start_index):
    entry_index = start_index
    name_list = []

    while True:
        entry = entry_list[entry_index]

        code_matching = get_speciality_code_matching(entry)
        first_index, last_index = code_matching.span()

        speciality_name = entry[last_index + 1:].replace(",", "")
        name_list.append(speciality_name)

        entry_index += 1

        if not entry.endswith(","):
            break

        entry_index += 1

    return entry_index, name_list


def _get_programme_name(entry_list, start_index):
    programme_row = entry_list[start_index]
    programme_matching = get_words_in_quotes(programme_row)

    return start_index + 1, programme_matching[0].replace("\"", "")


def _get_faculty(df):
    faculty_row = df.iloc[2, 0]

    return faculty_row.replace("Реализующее подразделение: ", "")


def _get_enrollment_year(df):
    enrollment_row = df.iloc[3, 0]
    year_matching = re.search(r"\d{4}/", enrollment_row)

    return year_matching[0].replace("/", "")


def _get_study_year_count(df):
    study_years_row = df.iloc[4, 0]
    years_matching = re.search(r"\d{1,2}", study_years_row)

    return years_matching[0]


def _get_degree(df):
    degree_row = df.iloc[6, 0]

    return degree_row.replace("Уровень образования: ", "")