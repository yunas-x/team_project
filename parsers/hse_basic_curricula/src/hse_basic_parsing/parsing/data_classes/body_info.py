from dataclasses import dataclass, field
from src.hse_basic_parsing.parsing.data_classes.course_types import CourseType


@dataclass
class BodyInfo:
    course_name: str = ""
    course_type: CourseType = CourseType.COMPULSORY_TYPE
    specialization: str = ""
    credits: int = 0
    competence_codes: list[str] = field(default_factory=list)