from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg
from sqlalchemy.orm import Session
import time
from . import models, schemas
from .database import engine, SessionLocal, get_db


models.Base.metadata.create_all(bind=engine)

app =  FastAPI()


    
while True:
    try:
        conn =  psycopg.connect(host= 'localhost', dbname= 'fastapi', user='postgres', 
                                password= 'Okikiola',)
        cursor = conn.cursor()
        print("Database connection was succesfull!!")
        break
    except Exception as error:
        print("Connecting to database failed ")
        print("Error", error)
        time.sleep(2)



# my_posts = [{"title": "Blockchain and AI is the future", "content": "The futute can be scary", "id":1}, {"title": "Favorite Food", "content": "Meat is king", "id":2, "published": "false", "rating":5}]

# def find_posts(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i 
     

@app.get("/posts",  response_model= List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    print(posts)
    return posts

@app.post("/posts", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
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


@app.get("/posts/{id}",  response_model= schemas.PostResponse)
def get_post(id: int,  db: Session = Depends(get_db)):
    print(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id ==  id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
    return  post

@app.delete("/post/{id}", status_code= status.HTTP_204_NO_CONTENT)
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

@app.put("/posts/{id}",  response_model= schemas.PostResponse)
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