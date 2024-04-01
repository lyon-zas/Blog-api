from fastapi import FastAPI, APIRouter
from fastapi.params import Body
from pydantic import BaseModel

from typing import Optional, List
from random import randrange
import psycopg
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post, users, auth

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

app.include_router(users.router)
app.include_router(post.router)
app.include_router(auth.router) 


