from fastapi import FastAPI
import models
import bcrypt, time
from jose import JWTError, jwt
import database as db


def generate_token(user:models.User):
    ts=time.time()
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    payload= {
        "user_id":str(db.user_col.find_one({"username":user.username})["_id"]),
        "username":user.username,
        "timestamp":ts
    }
    token=jwt.encode(payload,SECRET_KEY,ALGORITHM)
    return token;

