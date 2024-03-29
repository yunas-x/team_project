from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated

class FieldOfStudy(BaseModel):
    field_code: Annotated[str, StringConstraints(pattern=r"^[0-5][0-9]\.0[3-5]\.[0-1][1-9]$")]
    field_name: str
    field_group_code: Annotated[str, StringConstraints(pattern=r"^[0-5][0-9]\.0{2}\.0{2}$")]
    field_group_name: str
    
    
class FieldsOfStudy(BaseModel):
    fields_of_study: list[FieldOfStudy]

    @staticmethod
    def from_rows(fields_rows):
        fields = [FieldOfStudy(
                                field_code=f.field_code,
                                field_name=f.field_name,
                                field_group_code=f.field_group_code,
                                field_group_name=f.field_group_name
                              )
                  for f
                  in fields_rows]
        
        return FieldsOfStudy(fields_of_study=fields)
