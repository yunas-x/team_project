import pandas as pd
from pandas import DataFrame
from .body_parsing import parse_body
from .header_parsing import parse_header
from .data_classes.header_info import HeaderInfo


def parse_all(header_text_list, data_frame) -> DataFrame:
    header_info = HeaderInfo()
    parse_header(header_text_list, header_info)

    body_info_list = parse_body(data_frame)
    print(body_info_list)

    result_df = merge_info(header_info, body_info_list)

    return result_df


def merge_info(header_info, body_info_list) -> DataFrame:
    result_df = pd.DataFrame(columns=["CourseName", "CompetenceCode", "Speciality", "SpecialityCode", "Programme",
                                      "CourseType", "Specialization", "Credits", "Year", "Faculty", "EnrolledIn",
                                      "Degree"])

    for code_index, code_name in enumerate(header_info.speciality_codes):
        for body_info in body_info_list:
            if len(body_info.competence_codes) == 0:
                result_row = create_row(header_info, "", body_info, code_name, header_info.speciality_names[code_index])

                add_new_row(result_df, result_row)
            else:
                for competence_code in body_info.competence_codes:
                    result_row = create_row(header_info, competence_code, body_info, code_name,
                                            header_info.speciality_names[code_index])

                    add_new_row(result_df, result_row)

    return result_df


def add_new_row(df, row):
    df.loc[len(df.index)] = row


def create_row(header_info, competence_code, body_info, code_name, speciality_name):
    return [
        body_info.course_name,
        competence_code,
        speciality_name,
        code_name,
        header_info.programme_name,
        body_info.course_type.value,
        body_info.specialization,
        body_info.credits,
        header_info.study_year_count,
        header_info.faculty,
        header_info.enrollment_year,
        header_info.degree
    ]