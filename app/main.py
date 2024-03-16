from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app =  FastAPI()

class PostModel(BaseModel):
    title:str
    content:str
    published: bool = True
    



my_posts = [{"title": "Blockchain and AI is the future", "content": "The futute can be scary", "id":1}, {"title": "Favorite Food", "content": "Meat is king", "id":2, "published": "false", "rating":5}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/user")
def user():
    return {"data":  {"user_nmae": "ted", "name": "Eyimofe"}}

@app.get("/posts")
def get_posts():
    return {"message": "successfully retrived", "data":my_posts}

@app.post("/posts")
def create_post(post: PostModel):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"message": "successfully created", "data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, respose:Response):
    print(id)
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"message": "success", "data": post}

@app.delete("/post/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    index = find_index_post(id)
    if index ==  None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="invalid post")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@app.put("/posts/{id}")
def update_posts(id: int, post:PostModel):
    index = find_index_post(id)
    if index ==  None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="invalid post")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": "success", "data": post}