from typing import List
import pandas as pd
from parsers.core.utils.regex_helpers import get_words_in_quotes, get_speciality_list
from parsers.core.classifiers.degree_classifier import degree_classifier_dict
from parsers.core.classifiers.course_types import CourseType, course_classifier_dict
import re


def get_programme_info(header_list: List[str]) -> dict:
    """Returns programme info

    Args:
        header_list (List[str]): list of strings of the first page of the plan

    Returns:
        dict: return programme info like in json schema media/json_schemes/itmo_schema.json
    """
    name_ind = next((i for i, p in enumerate(header_list) if 'Наименование' in p))
    spec_ind = next((i for i, p in enumerate(header_list) if re.match(r'.*Направлени. подготовки', p)))
    year_ind = next((i for i, p in enumerate(header_list) if 'год начала подготовки' in p))
    
    name = header_list[name_ind]
    dquot_count = name.count('"')
    name_ind += 1
    
    while dquot_count != 2 and name_ind < spec_ind:
        name += ' ' + header_list[name_ind]
        dquot_count = name.count('"')
        name_ind += 1
        
    if dquot_count == 2:
        name = get_words_in_quotes(name)[1:-1]
    else:
        name = name[name.index('"')+1:]
        
    fields_of_study = []
    while spec_ind < year_ind:
        specialities = get_speciality_list(header_list[spec_ind])
        fields_of_study.extend([{
            'group': {
                'code': int(spec[0][:2]),
                'name': 'tbimpl'},
            'code': spec[0],
            'name': spec[1]} for spec in specialities])
        spec_ind += 1
    
    degree_code = int(fields_of_study[0]['code'][3:5])
    degree = {
        'code': degree_code,
        'degreeName': degree_classifier_dict[degree_code]
    }
    
    year = int(header_list[year_ind][-4:])
    
    return {
        'name': name,
        'yearEnrolled': year,
        'fields_of_study': fields_of_study,
        'degree': degree,
        'courses': [] 
    }


def get_courses(df: pd.DataFrame) -> dict:
    """Return courses

    Args:
        df (pd.DataFrame): dataframe with study plan courses

    Returns:
        dict: dict in the form {'courses': list_of_courses }
    """
    res = []
    
    hours_ind = None
    header_bottom = None
    
    for i in range(len(df)):
        try:
            hours_ind = list(df.iloc[i]).index('Лек')
            header_bottom = i
        except ValueError:
            continue
        break

    if hours_ind is None:
        for i in range(len(df)):
            try:
                # Устойчивое развитие и экологическое управление (2024, master).pdf
                hours_ind = list(df.iloc[i]).index('атобар\nяавосруК') + 2
                header_bottom = i
            except ValueError:
                continue
            break
    
    cdf = df[header_bottom+1:]
    current = None
    
    for i, row in cdf.iterrows():
        if current:
            item = __get_item_from_row(row, hours_ind)
            
            if item['color'] is not None:
                parent = current
                
                while True:
                    if item['color'] == parent['color']:
                        parent_parent = parent['parent']
                        if parent_parent is not None:
                            parent_parent['children'].append(item)
                            item['parent'] = parent_parent
                        else:
                            res.append(item)
                        break
                    
                    parent = parent['parent']
                    
                    if parent is None:
                        item['parent'] = current
                        current['children'].append(item)
                        break
            
            else:
                item['parent'] = current
                current['children'].append(item)
            
            current = item
            
        else:
            item = __get_item_from_row(row, hours_ind)
            res.append(item)
            current = item
    res = {'children': res}

    course_list = __course_tree_to_list(res)
    course_list = [course for course in course_list if course['year']]
    
    courses_to_add = []
    for course in course_list:
        if course['type'] == 'все':
            course['type'] = course_classifier_dict[CourseType.COMPULSORY_TYPE]
        elif course['type'] == 'все/0':
            course['type'] = course_classifier_dict[CourseType.FACULTATIVE_TYPE]
        else:
            course['type'] = course_classifier_dict[CourseType.ELECTIVE_TYPE]
            
        course['classroomHours'] = int(course['classroomHours'])
        course['credits'] = int(course['credits'])
        
        if course['year'].isdigit():
            course['year'] = (int(course['year']) + 1) // 2
        else:
            sems = course['year'].replace('\n', '').split(',')
            sems = list(set([(int(sem.strip()) + 1) // 2 for sem in sems if sem.strip() != '']))
            course['year'] = sems[0]
            
            for i in range(1, len(sems)):
                new_course = course.copy()
                new_course['year'] = sems[i]
                courses_to_add.append(new_course)
    
    course_list.extend(courses_to_add)
    
    course_dict = {}
    for item in course_list:
        course_dict.setdefault((item['name']), []).append(item)
    
    unique_courses = []

    for key, items in course_dict.items():
        if len(items) > 1:
            unique = [items[0]]
            for item in items[1:]:
                is_unique = True
                for u in unique:
                    if item['year'] == u['year']:
                        is_unique = False
                        
                        if item['type'] == course_classifier_dict[CourseType.COMPULSORY_TYPE]:
                            u['classroomHours'] += item['classroomHours']
                        break
                if is_unique:
                    unique.append(item)
            unique_courses.extend(unique)
        else:
            unique_courses.extend(items)
    
    return unique_courses


def __get_item_from_row(row, hours_ind):
    return {
            'parent': None,
            'name': row[5].replace('\n', ' '),
            'credits': row[6],
            'classroomHours': sum([int(item) for item in row[hours_ind:-3] if item and item.isdigit()]),
            'year': row[2],
            'type': row[0] if row[0] else '',
            'readBy': row[len(row)-3],
            'color': row[len(row)-1],
            'children': []}


def __course_tree_to_list(el: dict, override: str = '') -> list:
    res = []
    for child in el['children']:
        course_type = child['type'].lower()
        
        if override != '':
            if override == 'все' and course_type == '':
                child['type'] = override
            elif override != 'все':
                child['type'] = override
        
        res.append(__get_course_from_item(child))
        res.extend(__course_tree_to_list(child, child['type']))
    return res


def __get_course_from_item(item: dict) -> dict:
    return {key:item[key] for key in ['name', 'credits', 'classroomHours', 'year', 'type', 'readBy']}
