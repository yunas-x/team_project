from dataclasses import dataclass, field


@dataclass
class BodyRowInfo:
    course_name: str = ""
    course_type: str = ""
    credits: int = 0
    course_year: int = 0
    classroom_hours: int = 0
    comments: list[str] = field(default_factory=list)
    read_by: str = ""