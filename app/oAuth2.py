from typing import Annotated
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

#SECRET_KEY
#Algorithm
# Expiration time

SECRET_KEY = "cb7ee919fcc5a34b9d4508ed3bfb114e705f355b1ce46e98297a198d59c5619b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM])
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
   try: 
       payload =  jwt.decode(token, SECRET_KEY, ALGORITHM)
       payload.get("user_id")

       if id is None:
            raise credentials_exception
       toke_data = schemas.TokenData(id=id)
   except JWTError: 
       raise credentials_exception
   return toke_data
       

def get_current_user(toke: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return  verify_access_token(toke, credentials_exception)
