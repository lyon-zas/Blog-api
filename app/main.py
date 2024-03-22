from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
# from psycopg2.extras import RealDictCursor
import time


app =  FastAPI()

class PostModel(BaseModel):
    title:str
    content:str
    published: bool = True
    
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



my_posts = [{"title": "Blockchain and AI is the future", "content": "The futute can be scary", "id":1}, {"title": "Favorite Food", "content": "Meat is king", "id":2, "published": "false", "rating":5}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 
        

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print("is it working") 
    print(posts)
    return {"message": "successfully retrived", "data":posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post(post: PostModel):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_posts = cursor.fetchone()
    conn.commit()
    
    return {"message": "successfully created", "data": new_posts}


@app.get("/posts/{id}")
def get_post(id: int, respose:Response):
    print(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
    return {"message": "success", "data": post}

@app.delete("/post/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    print(id)
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post ==  None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
   
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@app.put("/posts/{id}")
def update_posts(id: int, post:PostModel):
    cursor.execute("""UPDATE posts SET title =%s, content = %s, published=%s WHERE id =%s RETURNING *""",(post.title, post.content, post.published, str(id)))
    updated_posts = cursor.fetchone()
    print(updated_posts)
    conn.commit()
    if updated_posts ==  None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"posts with the id: {id} does not exist")
   
    return {"message": "success", "data": updated_posts}