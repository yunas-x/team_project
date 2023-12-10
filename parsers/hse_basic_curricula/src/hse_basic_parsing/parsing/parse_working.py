from .data_classes.header_info import HeaderInfo
from .regex_helpers import get_words_in_quotes, get_speciality_code_list, remove_initials_from_text,\
    get_speciality_list, find_first_match
from .list_helpers import find_first_index
import re
import pandas as pd


def parse(text_list, table) -> pd.DataFrame:
    # Header
    programme = _get_programme_name(text_list)
    year, enrolled_in = _get_year_and_enrolled_in(text_list)
    
    print(programme)
    print(year)
    print(enrolled_in)

    result_table = []
    table = table.dropna(subset=['podr'])

    for row_index, row in table.iterrows():
        course_name = row['dscpl']
        department = row['podr']
        credits = row['cred']  
        first_sem_hours = _get_hours(row['hours_mod1']) + _get_hours(row['hours_mod2'])
        second_sem_hours = _get_hours(row['hours_mod3']) + _get_hours(row['hours_mod4'])
        
        result_table.append([course_name, programme, credits, year, department, enrolled_in, first_sem_hours, second_sem_hours])
        
    return pd.DataFrame(result_table, columns=['CourseName', 'Programme', 'Credits', 'Year', 'Department', 'EnrolledIn', 'FirstSemesterContactHours', 'SecondSemesterContactHours'])
        
    
def _get_programme_name(text_list: list[str]) -> str:
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
                
                for j in range(i+1, len(text_list)):
                    row = text_list[j]
                    
                    if '"' in row:
                        quote_ind = row.index('"')
                        
                        programme_name += ' ' + row[:quote_ind]
                        break
                    
                    elif '  ' in row:
                        gap_ind = row.index('  ')
                        
                        programme_name += ' ' + row[:gap_ind]
                break
    
    return programme_name


def _get_year_and_enrolled_in(text_list) -> (int, int):
    for row in text_list:
        match = re.search('\d ?курс, ?\d{4}\/\d{4} ?учебный ?год', row)
        
        if match:
            res_string = match.group(0)
            slash_ind = res_string.index('/')
            
            year = int(res_string[0])
            enrolled_in = int(res_string[slash_ind-4:slash_ind]) + 1 - year
            break
            
    return year, enrolled_in
            
            
def _get_hours(val) -> int:
    if type(val) is str:
        match = re.search('\d+', val)
        if match:
            return int(match.group(0))
        else:
            return 0
    else:
        return int(val)