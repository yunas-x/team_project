from parsers.core.classifiers.degree_classifier import degree_classifier_dict
from parsers.hse.annual.data_classes.header_info import HeaderInfo
from parsers.hse.annual.data_classes.body_info import BodyRowInfo


def convert_to_json(header_info: HeaderInfo, body_info_list: list[BodyRowInfo]) -> dict:
    json_dict = {"ProgramInfo": {
        "name": header_info.programme_name,
        "yearEnrolled": header_info.enrollment_year,
        "courses": __get_courses(body_info_list)
    }}

    return json_dict


def __get_courses(body_info_list: list[BodyRowInfo]) -> list[dict]:
    result = []

    for body_info in body_info_list:
        course = {
            "name": body_info.course_name,
            "credits": body_info.credits,
            "classroomHours": body_info.classroom_hours,
            "year": body_info.course_year,
            "readBy": body_info.read_by
        }
        result.append(course)

    return result
