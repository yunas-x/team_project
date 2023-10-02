import pandas as pd


class InfoHolderToDataFrameSaver:
    result_df = pd.DataFrame(columns=["CourseName", "CompetenceCode", "Speciality", "SpecialityCode", "Programme",
                                      "CourseType", "Specialization", "Credits", "Year", "Faculty", "EnrolledIn",
                                      "Degree"])

    def add_row(self, row):
        self.result_df.loc[len(self.result_df)] = row
