from typing_extensions import Annotated
from annotated_types import Ge
from pydantic import BaseModel

from .University import University
from .FieldsOfStudy import FieldOfStudy

class Program(BaseModel):
    program_id: int
    program_name: str
    degree_id: int
    degree: str
    duration: int
    field: FieldOfStudy
    unverisity: University
    
class Programs(BaseModel):
    programs: list[Program]
    count: Annotated[int, Ge(0)]
    
    @staticmethod
    def from_rows(programs_rows):
        level_to_years = {
            3: 4,
            4: 2,
            5: 6
        }
            
        programs = [Program(
                        program_id=p.program_id,
                        program_name=p.program_name,
                        degree_id=p.degree_id,
                        degree=p.degree_name,
                        duration=level_to_years[p.degree_id],
                        field=FieldOfStudy(
                                           field_code=p.field_code,
                                           field_name=p.field_name,
                                           field_group_code=p.field_group_code,
                                           field_group_name=p.field_group_name
                                          ),
                        unverisity=University(
                                               university_id=1, # Убрать хардкод потом
                                               university_name="НИУ ВШЭ", # Убрать хардкод потом
                                               city="Пермь"
                                            )
                           )
                    for p
                    in programs_rows]
        
        return Programs(
                        programs=programs,
                        count=len(programs)
                       )