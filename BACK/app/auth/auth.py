from fastapi import (
    Depends, 
    status, 
    HTTPException
)

from fastapi.security import OAuth2PasswordBearer
import os

api_key = os.environ['API_TOKEN']
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def api_key_auth(key: str = Depends(oauth2_scheme)):
    if key != api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden. Invalid Token"
        )
