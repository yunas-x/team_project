from typing_extensions import Annotated
from annotated_types import Ge, Le, Len
from pydantic import BaseModel

from .Programs import Program

class InfographicsProgramIDs(BaseModel):
    first_program_id: int
    second_program_id: int
    
class CourseSimilarity(BaseModel):
    first_course_name: str
    second_course_name: str
    similarity: Annotated[int, Ge(0), Le(100)]
    
class PopularCompetence(BaseModel):
    competence: str
    share: Annotated[int, Ge(0), Le(100)]

class Infographics(BaseModel):
   first_program: Program
   second_program: Program
   similar_courses: Annotated[list[CourseSimilarity], Len(min_length=5, max_length=5)]
   first_program_popular_competences: Annotated[list[PopularCompetence], Len(min_length=4, max_length=6)]
   second_program_popular_competences: Annotated[list[PopularCompetence], Len(min_length=4, max_length=6)]
   first_program_lesson_hours_a_week: Annotated[list[int], Len(min_length=2, max_length=6)]
   second_program_lesson_hours_a_week: Annotated[list[int], Len(min_length=2, max_length=6)]