from pydantic import BaseModel

class HTTPAuthError(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
        
class ValidationModel(BaseModel):
    detail: str
    status_code: int