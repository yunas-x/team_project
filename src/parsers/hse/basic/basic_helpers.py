import numpy as np
import pandas as pd
from pandas import DataFrame

from parsers.core.utils.list_helpers import find_first_index


def merge_info(header_info, body_info_list) -> DataFrame:
    result_df = pd.DataFrame(columns=["CourseName", "CompetenceCode", "Speciality", "SpecialityCode", "Programme",
                                      "CourseType", "Specialization", "Credits", "CourseYear", "Year", "Faculty",
                                      "EnrolledIn", "Degree"])

    for code_index, code_name in enumerate(header_info.speciality_codes):
        for body_info in body_info_list:
            if len(body_info.competence_codes) == 0:
                __add_rows(result_df, header_info, "", body_info, code_name, header_info.speciality_names[code_index])
            else:
                for competence_code in body_info.competence_codes:
                    __add_rows(result_df, header_info, competence_code, body_info, code_name,
                               header_info.speciality_names[code_index])

    return result_df


def __add_rows(result_df, header_info, competence_code, body_info, code_name, speciality_name):
    for i, credits_value in enumerate(body_info.credits):
        new_row = create_row(header_info, competence_code, body_info, code_name, speciality_name, credits_value,
                             body_info.course_years[i])

        add_new_row(result_df, new_row)


def create_row(header_info, competence_code, body_info, code_name, speciality_name, credits_value, course_year):
    # credits_value is count of credits that is gaining in course_year
    # one course can last for several years

    return [
        body_info.course_name,
        competence_code,
        speciality_name,
        code_name,
        header_info.programme_name,
        body_info.course_type.value,
        body_info.specialization,
        credits_value,
        course_year,
        header_info.study_year_count,
        header_info.faculty,
        header_info.enrollment_year,
        header_info.degree
    ]


def add_new_row(df, row):
    df.loc[len(df.index)] = row


def concat_for_basic(df):
    index = find_first_index(df.iloc[0, :], "Вид")
    if index is None:
        index = find_first_index(df.iloc[0, :], "Трудоемкость")

    # if there are columns between colum with index 1 and "Вид" or "Трудоемкость" column,
    # it's necessary to concatenate these columns because of some error
    # example:
    # 1,  2,    3,   4          - column names
    # Dat a cul ture О          - data

    if index - 1 != 1:
        new_column_values = []

        for row_index in range(len(df)):
            new_row_value = ""

            for col_index in range(1, index):
                value = df.iloc[row_index, col_index]
                if isinstance(value, str):
                    new_row_value += value

            new_column_values.append(new_row_value)

        df.drop(np.arange(1, index), axis=1, inplace=True)
        df.insert(1, column="1", value=new_column_values)

    return df
