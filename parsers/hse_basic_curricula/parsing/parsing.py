import pandas as pd
import re
from info_holder import InfoHolder


COMPULSORY_TYPE = "О"
ELECTIVE_TYPE = "В"

info_holder = InfoHolder()


def parse(data_frame):
    info_holder.speciality_code = get_speciality_code(data_frame)

    info_holder.speciality_name = get_speciality_name(data_frame)

    info_holder.programme_name = get_programme_name(data_frame)

    info_holder.faculty = get_faculty(data_frame)

    info_holder.enrollment_year = get_enrollment_year(data_frame)

    info_holder.study_year_count = get_study_year_count(data_frame)

    info_holder.degree = get_degree(data_frame)

    info_holder.print()


def get_speciality_code(df):
    speciality_row = df.iloc[0, 0]
    code_matching = re.search(r"\b(?:\d{2}.){2}\d{2}\b", speciality_row)

    return code_matching[0]


def get_speciality_name(df):
    speciality_row = df.iloc[0, 0]
    name_matching = find_word_in_quotes(speciality_row)

    return name_matching[0].replace("\"", "")


def find_word_in_quotes(row):
    return re.search(r"\"(?:[\da-zА-я\-]+[^\S\f\t\r\n]?)+\"", row)


def get_programme_name(df):
    programme_row = df.iloc[1, 0]
    programme_matching = find_word_in_quotes(programme_row)

    return programme_matching[0].replace("\"", "")


def get_faculty(df):
    faculty_row = df.iloc[2, 0]

    return faculty_row.replace("Реализующее подразделение: ", "")


def get_enrollment_year(df):
    enrollment_row = df.iloc[3, 0]
    year_matching = re.search(r"\d{4}/", enrollment_row)

    return year_matching[0].replace("/", "")


def get_study_year_count(df):
    study_years_row = df.iloc[4, 0]
    years_matching = re.search(r"\d{1,2}", study_years_row)

    return years_matching[0]


def get_degree(df):
    degree_row = df.iloc[6, 0]

    return degree_row.replace("Уровень образования: ", "")


def read_table_rows(df):
    specialization = ""
    course_type = ""

    for index in range(10, len(df)):
        row = df.iloc[index, :]

        if row[0] is None and not row[1].contains("Специализация"):
            continue

        if row[1].contains("Специализация"):
            specialization = find_word_in_quotes(row[1])

            continue
        else:
            specialization = ""

        if row[1].contains("Блок дисциплин по выбору"):
            course_type = ELECTIVE_TYPE

            continue
        else:
            course_type = COMPULSORY_TYPE

        if row[0] is not None:
            #course_name = row[]

            new_df_row = []