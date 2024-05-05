from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased

from ..Context import SessionMaker
from ..models.FieldOfStudy import FieldOfStudy
from ..models.Degree import Degree
from ..models.MVP_API import MVP_API

__fos1 = aliased(FieldOfStudy)
__fos2 = aliased(FieldOfStudy)

def select_programs(offset: int|None, 
                    limit: int, 
                    fields: list[str], 
                    session_maker: sessionmaker[Session]=SessionMaker):
    '''
    Selects all programs info required for frontend depiction
    
    Arguments:
    
    offset -- offset of Database
    
    limit -- how many rows to take
    
    fields -- filters rows only matching the specified filters
    
    session_maker -- a factory for building session with Database
    '''

    with session_maker() as session:
        programs_pre_query = session \
                                    .query(
                                           MVP_API.program_id,
                                           MVP_API.program_name,
                                           MVP_API.field_code,
                                           __fos1.field_name,
                                           __fos2.field_code.label("field_group_code"),
                                           __fos2.field_name.label("field_group_name"),
                                           MVP_API.degree_id,
			                               Degree.name.label("degree_name")
			                        ) \
                                    .filter(MVP_API.degree_id==Degree.id) \
                                    .filter(MVP_API.field_code==__fos1.field_code) \
                                    .filter(__fos1.field_group_code==__fos2.field_code)

        if fields:
            programs_pre_query = programs_pre_query.filter(MVP_API.field_code.in_(fields))

        if offset:
            programs_pre_query = programs_pre_query.offset(offset=offset)
        
        if limit:
            programs_pre_query = programs_pre_query.limit(limit=limit)
       
        programs = programs_pre_query.all()

    return programs
