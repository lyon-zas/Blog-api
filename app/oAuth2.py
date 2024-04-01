from jose import JWTError, jwt
from datetime import datetime, timedelta

#SECRET_KEY
#Algorithm
# Expiration time

SECRET_KEY = "cb7ee919fcc5a34b9d4508ed3bfb114e705f355b1ce46e98297a198d59c5619b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt