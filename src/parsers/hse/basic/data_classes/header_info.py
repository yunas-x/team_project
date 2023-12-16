from dataclasses import dataclass, field


@dataclass
class HeaderInfo:
    speciality_codes: list[str] = field(default_factory=list)
    speciality_names: list[str] = field(default_factory=list)
    programme_name: str = ""
    faculty: str = ""
    enrollment_year: int = ""
    study_year_count: str = ""
    degree: str = ""

    def __repr__(self):
        result = ""

        result += "Speciality codes: " + repr(self.speciality_codes) + "\n"

        result += "Speciality names: " + repr(self.speciality_names) + "\n"

        result += "Programme name: " + repr(self.programme_name) + "\n"

        result += "Faculty: " + repr(self.faculty) + "\n"

        result += "Enrollment year: " + repr(self.enrollment_year) + "\n"

        result += "Study year count: " + repr(self.study_year_count) + "\n"

        return result + "Degree: " + repr(self.degree) + "\n"
