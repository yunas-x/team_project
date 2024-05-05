from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Query,
)


from fastapi.middleware.cors import CORSMiddleware

'''
for validation
'''
from typing import Optional
from typing_extensions import Annotated
from pydantic import PositiveInt, StringConstraints

'''
for work with data models
'''
from validators import validate_inforaphics
from models.University import Universities, University
from models.Infographics import Infographics, InfographicsProgramIDs
from models.Programs import Programs
from models.FieldsOfStudy import FieldsOfStudy
from models.HTTPAuthError import HTTPAuthError
from auth.auth import api_key_auth

'''
DB Queries
'''
from orm.queries.FieldsQueries import select_fields
from orm.queries.ProgramsQueries import select_programs
from orm.queries.InfographicsQueries import select_infographics

import response_de_jour as rsp

app = FastAPI(title="BI Curricula", 
              summary="""API для дипломного проекта""",
              description="""АПИ к хранилищу данных
                             Для облегчения поиска 
                             образовательных программ""",
              version="0.1.3"
      )

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

fields_alias = Annotated[str, StringConstraints(pattern=r"^[0-5][0-9]\.0[3-5]\.[0-1][1-9]$")]

@app.get("/programs",
         dependencies=[Depends(api_key_auth)],
         summary="Список образовательных программ",
         description="""Список образовательных программ""",
         status_code=status.HTTP_200_OK,
         tags=["programs"],
         responses={
             status.HTTP_200_OK: {
                   "model": Programs,
                   "description": "List of programms"
             },
             status.HTTP_401_UNAUTHORIZED: {
                   "model": HTTPAuthError,
                   "description": "Invalid Token (or not provided)"
             }
         }
)
def get_programmes(offset: Optional[PositiveInt]=None,
                   limit: Optional[PositiveInt]=None,
                   fields: Annotated[Optional[list[fields_alias]], Query()] = None) -> Programs:
    programs_rows = select_programs(offset, limit, fields)
    return Programs.from_rows(programs_rows)

@app.get("/fields",
         dependencies=[Depends(api_key_auth)],
         summary="Список направлений подготовки",
         description="""Список направлений подготовки""",
         status_code=status.HTTP_200_OK,
         tags=["fields of study"],
         responses={
             status.HTTP_200_OK: {
                   "model": FieldsOfStudy,
                   "description": "List of fields of study"
             },
             status.HTTP_401_UNAUTHORIZED: {
                   "model": HTTPAuthError,
                   "description": "Invalid Token (or not provided)"
             }
         }
)
def get_fields() -> FieldsOfStudy:
    fields_rows = select_fields()
    return FieldsOfStudy.from_rows(fields_rows)

@app.get("/universities",
         dependencies=[Depends(api_key_auth)],
         summary="Список университетов",
         description="""Список университетов""",
         status_code=status.HTTP_200_OK,
         tags=["university"],
         responses={
             status.HTTP_200_OK: {
                   "model": Universities,
                   "description": "List of fields of study"
             },
             status.HTTP_401_UNAUTHORIZED: {
                   "model": HTTPAuthError,
                   "description": "Invalid Token (or not provided)"
             }
         }
)
def get_universities() -> Universities:
    return Universities(universities=[University(
                                               university_id=1,
                                               university_name="НИУ ВШЭ",
                                               city="Пермь"
                                              )])

@app.get("/infographics",
         dependencies=[Depends(api_key_auth)],
         summary="Инфографика по двум выбранным программам",
         description="""Инфографика по двум выбранным программам""",
         status_code=status.HTTP_200_OK,
         tags=["infographics"],
                  responses={
             status.HTTP_200_OK: {
                   "model": Infographics,
                   "description": "Data for Infographics"
             },
             status.HTTP_400_BAD_REQUEST: {
                   "model": HTTPAuthError,
                   "description": "No programs with such ids"
             },
             status.HTTP_401_UNAUTHORIZED: {
                   "model": HTTPAuthError,
                   "description": "Invalid Token (or not provided)"
             }
         })
def get_infographics(ids: InfographicsProgramIDs=Depends()):
    programs_rows = select_infographics(
                                        ids.first_program_id, 
                                        ids.second_program_id
                                       )
    programs_info = Programs.from_rows(programs_rows)
    
    validation_result = validate_inforaphics(programs_info)
    if validation_result.status_code // 100 != 2:
        raise HTTPException(
                            status_code=validation_result.status_code, 
                            detail=validation_result.detail
                           )
    
    first_program_n_years = programs_info.programs[0].duration
    second_program_n_years = programs_info.programs[1].duration
    
    return Infographics(
                first_program = programs_info.programs[0],
                second_program = programs_info.programs[1],
                similar_courses = rsp.similar_courses,
                first_program_popular_competences = rsp.first_program_popular_competences,
                second_program_popular_competences = rsp.second_program_popular_competences,
                first_program_lesson_hours_a_week = rsp.first_program_lesson_hours_a_week[0:first_program_n_years],
                second_program_lesson_hours_a_week = rsp.second_program_lesson_hours_a_week[0:second_program_n_years])
