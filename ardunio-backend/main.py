from typing import Union
import database as db
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from user import user
from arduino import ard,flu
import models
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.include_router(user)
app.include_router(ard)
app.include_router(flu)

origins = [
   "http:// 192.168.0.11.:8000",
   "http://localhost",
   "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



