from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import  List, Optional
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy import func


from .. import models, schemas, oAuth2
from ..database import  get_db


router = APIRouter(
    prefix= "/posts", 
    tags= ["Posts"],
    dependencies=[Depends(oAuth2.oauth2_scheme)]
)

@router.get("/",  response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user), limit: int = 10,skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts""") 
    # posts = cursor.fetchall()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return posts 

@router.get("/user/",  response_model= List[schemas.PostOut])
def get_user_posts(db: Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user)):
   
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.user_id == current_user.id).all()
    return posts

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oAuth2.get_current_user)):
   
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_posts = cursor.fetchone()
    # conn.commit() 
    new_posts =  models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return  new_posts


@router.get("/{id}",  response_model= schemas.PostOut)
def get_post(id: int,  db: Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user)):
    print(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id ==  id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
    return  post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id ==  id)
    post = post_query.first()

    if post ==  None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@router.put("/{id}",  response_model= schemas.PostResponse)
def update_posts(id: int, new_post:schemas.PostCreate,  db: Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title =%s, content = %s, published=%s WHERE id =%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # updated_posts = cursor.fetchone()
    # print(updated_posts)
    # conn.commit()
    post_query =  db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post ==  None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(new_post.model_dump(), synchronize_session=False)
    db.commit()
    return  post_query.first()
