from typing import override
import pandas as pd
from parsers.core.protocols.ParserProtocol import ParserProtocol
from parsers.core.utils.converters import get_pdf_page_text
from parsers.hse.annual.annual_helpers import get_programme_name, get_year_and_enrolled_in, get_hours
from parsers.hse.utils import get_data_frame_by_pdf_path, prepare_table


class AnnualParser(ParserProtocol):
    """Parser for annual HSE curricula"""

    @override
    def parse(self, payload: str):
        """
        Parses annual HSE curricula pdf file
        :param payload: pdf file path
        """

        pdf_path = payload

        header_text_list = get_pdf_page_text(pdf_path, 0, True).split("\n")
        header_text_list = [text.strip() for text in header_text_list if text]

        df = get_data_frame_by_pdf_path(pdf_path)
        df = prepare_table(df)
        df.columns = ['n_row', 'dscpl', 'podr', 'cred', 'hours_total', 'hours_contact', 'hours_mod1', 'hours_mod2',
                      'hours_mod3', 'hours_mod4', 'info']
        df = df.iloc[2:, :]
        df[['hours_mod1', 'hours_mod2', 'hours_mod3', 'hours_mod4']] =\
            df[['hours_mod1', 'hours_mod2', 'hours_mod3', 'hours_mod4']].fillna(0)

        programme = get_programme_name(header_text_list)
        year, enrolled_in = get_year_and_enrolled_in(header_text_list)

        result_table = []
        table = df.dropna(subset=['podr'])

        for row_index, row in table.iterrows():
            course_name = row['dscpl']
            department = row['podr']
            credits = row['cred']
            first_sem_hours = get_hours(row['hours_mod1']) + get_hours(row['hours_mod2'])
            second_sem_hours = get_hours(row['hours_mod3']) + get_hours(row['hours_mod4'])

            result_table.append(
                [course_name, programme, credits, year, department, enrolled_in, first_sem_hours, second_sem_hours])

        return pd.DataFrame(result_table, columns=[
            'CourseName',
            'Programme',
            'Credits',
            'Year',
            'Department',
            'EnrolledIn',
            'FirstSemesterContactHours',
            'SecondSemesterContactHours'
        ])