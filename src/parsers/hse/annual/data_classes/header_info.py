from dataclasses import dataclass, field


@dataclass
class HeaderInfo:
    programme_name: str = ""
    enrollment_year: int = ""
    
    def __repr__(self):
        result = ""

        result += "Programme name: " + repr(self.programme_name) + "\n"

        result += "Enrollment year: " + repr(self.enrollment_year) + "\n"

        return result
