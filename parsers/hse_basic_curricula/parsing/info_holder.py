import pandas as pd


class InfoHolder:
    speciality_code = ""
    speciality_name = ""
    programme_name = ""
    faculty = ""
    enrollment_year = ""
    study_year_count = ""
    degree = ""

    result_df = pd.DataFrame(columns=["CourseName", "CompetenceCode", "Speciality", "SpecialityCode", "Programme",
                                      "CourseType", "Specialization", "Credits", "Year", "Faculty", "EnrolledIn",
                                      "Degree"])

    def add_row(self, row):
        self.result_df.loc[len(self.result_df)] = row

    def print(self):
        print(self.speciality_code, self.speciality_name, self.programme_name, self.faculty, self.enrollment_year,
              self.study_year_count, self.degree, sep=" ")
