import pandas as pd
import re
import os


def parse(excel_file_name):
    df = pd.read_excel(excel_file_name, sheet_name='Sheet1', skiprows=1)

    speciality_code = get_speciality_code(df)

    speciality_name = get_speciality_name(df)

    programme_name = get_programme_name(df)

    (specialization_list, faculty) = get_specialization_and_faculty(df)

    enrollment_year = get_enrollment_year(df)

    study_year_count = get_study_year_count(df)

    print(study_year_count)


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


def get_specialization_and_faculty(df):
    current_row = df.iloc[2, 0]

    specialization_list = []

    # noinspection SpellCheckingInspection
    if current_row.contains("Специализ"):


        current_row = df.iloc[2, 0]

    return specialization_list, current_row.replace("Реализующее подразделение: ", "")


def get_enrollment_year(df):
    enrollment_row = df.iloc[3, 0]
    year_matching = re.search(r"\d{4}/", enrollment_row)

    return year_matching[0].replace("/", "")


def get_study_year_count(df):
    study_years_row = df.iloc[4, 0]
    years_matching = re.search(r"\d{1,2}", study_years_row)

    return years_matching[0]


if __name__ == '__main__':
    base_files_path = "..\\..\\curricula_examples\\basic"

    first_file_name = os.listdir(base_files_path)[0]
    parse(os.path.join(base_files_path, first_file_name))
