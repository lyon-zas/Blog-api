from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Body


from sqlalchemy.orm import Session
from .. import models, schemas, utils, oAuth2
from ..database import get_db

router = APIRouter(prefix= "/auth", tags= ["Auth"])

@router.post("/register", status_code= status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password = use.password
    hasshed_password = utils.hash(user.password)
    user.password = hasshed_password
    new_user =  models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", status_code= status.HTTP_201_CREATED, )
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # hash the password = use.password
    user =  db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Incorrect email or password")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Incorrect email or password")
    
    # create a token
    access_token = oAuth2.create_access_token(data= {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer", } 