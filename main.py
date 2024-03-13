from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app =  FastAPI()

class PostModel(BaseModel):
    title:str
    content:str
    published: bool = True
    rating: Optional[int] = None



my_posts = [{"title": "Blockchain and AI is the future", "content": "The futute can be scary", "id":1}, {"title": "Favorite Food", "content": "Meat is king", "id":2, "published": "false", "rating":5}]

def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
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
def get_post(id: int):
    print(id)
    post = find_posts(id)
    return {"message": "success", "data": post}