from fastapi import status, HTTPException, Depends, APIRouter



from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix= "/users", tags= ["Users"])



@router.get("/{id}", response_model= schemas.UserResponse)
def get_user(id: int,  db: Session = Depends(get_db)):
   user = db.query(models.User).filter(models.User.id ==  id).first()
   if not user:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist")
   return user
    