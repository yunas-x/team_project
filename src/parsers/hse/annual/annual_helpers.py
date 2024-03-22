import re
from typing import Tuple
from pandas import DataFrame
from parsers.hse.annual.data_classes.body_info import BodyRowInfo
from parsers.hse.utils import get_data_frame_by_pdf_path, prepare_table


def get_body_row_list_without_year(df: DataFrame) -> list[BodyRowInfo]:
    df = prepare_table(df)
    df = __get_corrected_df(df)

    result_table = []

    for row_index, row in df.iterrows():
        row_info = BodyRowInfo()
        row_info.course_name = row['dscpl']
        # TODO: Add course type evaluation
        row_info.course_type = "Обязательный"
        row_info.course_year = 0
        row_info.credits = row['cred']
        row_info.read_by = row['podr']
        #row_info.classroom_hours = get_hours(row['hours_mod1']) + get_hours(row['hours_mod2']) + get_hours(row['hours_mod3']) + get_hours(row['hours_mod4'])
        row_info.classroom_hours = row['hours_contact']
        row_info.comments = row['info']
        result_table.append(row_info)

    return result_table



def __get_corrected_df(df: DataFrame) -> DataFrame:

    mod_cols = __get_module_cols(df)

    if len(df.columns) - len(mod_cols) != 11 - 4:
        df = __remove_redundant_columns(df)

    # TODO: Add support for pdfs with module count less than 4

    df = df.drop(mod_cols, axis=1)

    df.columns = ['n_row', 'dscpl', 'podr', 'cred', 'hours_total', 'hours_contact', 'info']
    df = df.iloc[2:, :]
    # df.loc[:,['hours_mod1', 'hours_mod2', 'hours_mod3', 'hours_mod4']] =\
    #     df.loc[:,['hours_mod1', 'hours_mod2', 'hours_mod3', 'hours_mod4']].fillna(0)

    df.loc[:,'n_row'] = df['n_row'].apply(lambda x: x if bool(re.search(r'\d+', str(x))) else None)
    df.loc[:,'dscpl'] = df['dscpl'].apply(lambda x: None if bool(re.search(r'Блок \d+', str(x))) else x)
    df = df.dropna(subset=['n_row', 'dscpl'])
    df.loc[:,'hours_contact'] = df.loc[:,'hours_contact'].fillna(0).astype(int)

    df.loc[:,'cred'] = df.loc[:,'cred'].fillna(0).astype(int)
    df.loc[:,'info'] = df.loc[:,'info'].fillna("")
    df.loc[:,'podr'] = df.loc[:,'podr'].fillna("")
    return df


def __get_module_cols(df: DataFrame) -> list[int]:
    # TODO: There is probably a better way to do this
    cols = []
    for i in range(0, len(df.columns)):
        if df.iloc[1,i] is not None:
            cols.append(df.columns[i])
    return cols


def __remove_redundant_columns(df: DataFrame) -> DataFrame:
    used_column_names = []
    
    for col_name in df.columns:
        cell_value = df.iloc[0, col_name]
        
        print(cell_value)
        if cell_value == None:
            cell_value = df.iloc[1, col_name]
        
        if __determine_if_column_is_used(cell_value):
            used_column_names.append(col_name)
            
    return df.loc[:,used_column_names]
        


def __determine_if_column_is_used(header_name: str) -> bool:
    # Need to figure a better way to determine which columns are useful
    return bool(re.search('(код блока)|(наименование)|(реализующее)|(зачетные)|(всего)|' +
                          '(в том числе)|(распределение)|(дополнительная)|([1-4])', header_name.lower()))


def get_programme_name(text_list: list[str]) -> str:
    programme_name = ''

    for i in range(0, len(text_list)):
        row = text_list[i]

        if 'программа' in row and '"' in row:
            start_ind = row.index('"') + 1
            potential_name = row[start_ind:]

            # if both quotes are in the row then programme name should be between them
            if '"' in potential_name:
                end_ind = potential_name.index('"')

                programme_name = potential_name[:end_ind]
                break

            # if just one quote is in the row then find next row with end quote
            else:
                if '  ' in potential_name:
                    gap_ind = potential_name.index('  ')

                    programme_name = potential_name[:gap_ind]
                else:
                    programme_name = potential_name

                for j in range(i + 1, len(text_list)):
                    row = text_list[j]

                    if '"' in row:
                        quote_ind = row.index('"')

                        programme_name += ' ' + row[:quote_ind]
                        break

                    elif '  ' in row:
                        gap_ind = row.index('  ')

                        programme_name += ' ' + row[:gap_ind]
                break

    programme_name = programme_name.replace('_ ', '').replace('_', '')

    return programme_name


def get_year_and_enrolled_in(text_list) -> Tuple[int, int]:
    for row in text_list:
        match = re.search(r'\d ?курс, ?\d{4}/\d{4} ?учебный ?год', row)

        if match:
            res_string = match.group(0)
            slash_ind = res_string.index('/')

            year = int(res_string[0])
            enrolled_in = int(res_string[slash_ind - 4:slash_ind]) + 1 - year
            break

    return year, enrolled_in


def get_hours(val) -> int:
    if type(val) is str:
        match = re.search(r'\d+', val)
        if match:
            return int(match.group(0))
        else:
            return 0
    else:
        return int(val)