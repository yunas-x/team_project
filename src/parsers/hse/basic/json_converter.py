from parsers.core.classifiers.degree_classifier import degree_classifier_dict
from parsers.hse.basic.data_classes.body_info import BodyRowInfo
from parsers.hse.basic.data_classes.course_types import CourseType
from parsers.hse.basic.data_classes.header_info import HeaderInfo


def convert_to_json(header_info: HeaderInfo, body_info_list: list[BodyRowInfo]) -> dict:
    json_dict = {"ProgramInfo": {
        "name": header_info.programme_name,
        "fields_of_study": __get_fields_of_study(header_info),
        "degree": __get_degree(header_info),
        "yearEnrolled": header_info.enrollment_year,
        "courses": __get_courses(body_info_list)
    }}

    return json_dict


def __get_fields_of_study(header_info: HeaderInfo) -> list[dict]:
    return [
        {"group": {"code": int(speciality_code[:2]), "name": "tbimpl"},
         "code": speciality_code,
         "name": header_info.speciality_names[i]
         }
        for i, speciality_code in enumerate(header_info.speciality_codes)]


def __get_degree(header_info: HeaderInfo) -> dict:
    if header_info.degree == "Бакалавриат":
        code = 3
    elif header_info.degree == "Магистратура":
        code = 4
    elif header_info.degree == "Специалитет":
        code = 5
    else:
        # to be implemented
        code = 1

    return {"code": code, "degreeName": degree_classifier_dict[code]}


def __get_courses(body_info_list: list[BodyRowInfo]) -> list[dict]:
    result = []

    for body_info in body_info_list:
        for i, credits_count in enumerate(body_info.credits):
            course = __get_course(body_info.course_name, body_info.course_type, credits_count,
                                  body_info.course_years[i], body_info.competence_codes)
            result.append(course)

    return result


def __get_course(course_name: str, course_type: CourseType, credits_count: int,
                 course_year: int, competences: list[str]) -> dict:
    return {
        "name": course_name,
        "type": __get_course_type(course_type),
        "credits": credits_count,
        "year": course_year,
        "competences": __get_competences(competences)
    }


def __get_course_type(course_type: CourseType) -> str:
    if course_type == CourseType.COMPULSORY_TYPE:
        return "Обязательный"
    elif course_type == CourseType.ELECTIVE_TYPE:
        return "По выбору"
    elif course_type == CourseType.FACULTATIVE_TYPE:
        return "Факультативный"


def __get_competences(competences: list[str]) -> list[dict]:
    return [
        {"code": competence, "type": __get_competence_type(competence)}
        for competence in competences
    ]


def __get_competence_type(competence_code: str) -> str:
    if "УК-" in competence_code:
        return "Универсальные"
    elif "ОП" in competence_code:
        return "Общепрофессиональные"

    return "Профессиональные"
