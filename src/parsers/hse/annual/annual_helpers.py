import re
from pandas import DataFrame


def get_corrected_df(df: DataFrame) -> DataFrame:
    
    if len(df.columns) != 11:
        df = _remove_redundant_columns(df)
    
    df.columns = ['n_row', 'dscpl', 'podr', 'cred', 'hours_total', 'hours_contact', 'hours_mod1', 'hours_mod2',
                      'hours_mod3', 'hours_mod4', 'info']
    df = df.iloc[2:, :]
    df[['hours_mod1', 'hours_mod2', 'hours_mod3', 'hours_mod4']] =\
        df[['hours_mod1', 'hours_mod2', 'hours_mod3', 'hours_mod4']].fillna(0)
        
    # If № is not a number, replace with None
    df['n_row'] = df['n_row'].apply(lambda x: x if bool(re.search(r'\d+', str(x))) else None)
    df = df.dropna(subset=['n_row'])
    return df
        
        
def _remove_redundant_columns(df: DataFrame) -> DataFrame:
    used_column_names = []
    
    for col_name in df.columns:
        cell_value = df.iloc[0, col_name]
        
        print(cell_value)
        if cell_value == None:
            cell_value = df.iloc[1, col_name]
        
        if _determine_if_column_is_used(cell_value):
            used_column_names.append(col_name)
            
    return df.loc[:,used_column_names]
            


def _determine_if_column_is_used(header_name: str) -> bool:
    return bool(re.search('(код блока)|(наименование)|(реализующее)|(зачетные)|(всего)|' +
                          '(в том числе)|(распределение)|(дополнительная)|([1-4])', header_name.lower()))


def get_programme_name(text_list: list[str]) -> str:
    programme_name = ''

    for i in range(0, len(text_list)):
        row = text_list[i]
        print(row)

        if 'программа' in row and '"' in row:
            start_ind = row.index('"') + 1
            potential_name = row[start_ind:]
            print('Potential name: ' + potential_name)

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
                    print('Potential name: ' + programme_name)

                for j in range(i + 1, len(text_list)):
                    row = text_list[j]
                    print(row)

                    if '"' in row:
                        quote_ind = row.index('"')

                        programme_name += ' ' + row[:quote_ind]
                        break

                    elif '  ' in row:
                        gap_ind = row.index('  ')

                        programme_name += ' ' + row[:gap_ind]
                break

    return programme_name


def get_year_and_enrolled_in(text_list) -> (int, int):
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