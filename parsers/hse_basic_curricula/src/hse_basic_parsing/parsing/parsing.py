from .header_parsing import parse_header
from .header_info import HeaderInfo

COMPULSORY_TYPE = "О"
ELECTIVE_TYPE = "В"


def parse_all(header_text_list, data_frame):
    header_info = HeaderInfo()
    parse_header(header_text_list, header_info)

    print(header_info, sep=" ")


def read_table_rows(df):
    specialization = ""
    course_type = ""

    for index in range(10, len(df)):
        row = df.iloc[index, :]

        if row[0] is None and not row[1].contains("Специализация"):
            continue

        if row[1].contains("Специализация"):
            # specialization = find_word_in_quotes(row[1])

            continue
        else:
            specialization = ""

        if row[1].contains("Блок дисциплин по выбору"):
            course_type = ELECTIVE_TYPE

            continue
        else:
            course_type = COMPULSORY_TYPE

        if row[0] is not None:
            #course_name = row[]

            new_df_row = []