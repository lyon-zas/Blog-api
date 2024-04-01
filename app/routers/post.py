from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import  List

from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import  get_db


router = APIRouter(prefix= "/posts", tags= ["Posts"])

@router.get("/",  response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    print(posts)
    return posts

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
   
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_posts = cursor.fetchone()
    # conn.commit() 
    new_posts =  models.Post(**post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return  new_posts


@router.get("/{id}",  response_model= schemas.PostResponse)
def get_post(id: int,  db: Session = Depends(get_db)):
    print(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id ==  id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
    return  post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    print(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id ==  id)

    if post.first() ==  None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@router.put("/{id}",  response_model= schemas.PostResponse)
def update_posts(id: int, new_post:schemas.PostCreate,  db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title =%s, content = %s, published=%s WHERE id =%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # updated_posts = cursor.fetchone()
    # print(updated_posts)
    # conn.commit()
    post_query =  db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post ==  None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()
