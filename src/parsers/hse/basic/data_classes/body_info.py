from dataclasses import dataclass, field
from .course_types import CourseType


@dataclass
class BodyRowInfo:
    course_name: str = ""
    course_type: CourseType = CourseType.COMPULSORY_TYPE
    specialization: str = ""
    credits: list[int] = field(default_factory=list)
    course_years: list[int] = field(default_factory=list)
    competence_codes: list[str] = field(default_factory=list)
