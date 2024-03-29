from pydantic import BaseModel

class University(BaseModel):
    university_id: int
    university_name: str
    city: str
    
class Universities(BaseModel):
    universities: list[University]