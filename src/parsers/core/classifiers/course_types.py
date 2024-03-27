from enum import Enum


class CourseType(Enum):
    COMPULSORY_TYPE = "О"
    ELECTIVE_TYPE = "В"
    FACULTATIVE_TYPE = "Ф"


# TODO: Combine enum and dict
course_classifier_dict = {
    CourseType.COMPULSORY_TYPE: "Обязательный",
    CourseType.ELECTIVE_TYPE: "По выбору",
    CourseType.FACULTATIVE_TYPE: "Факультативный"
}