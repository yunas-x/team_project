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

def select_programs(session_maker: sessionmaker[Session]=SessionMaker):

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


        programs = programs_pre_query.all()

    return programs
