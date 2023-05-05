from fastapi import APIRouter,HTTPException,status
import models
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import database as db
import tokenfile as tf




user=APIRouter(
    prefix="/user",
    tags=["user"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify(hashed_password,plain_password):

    return pwd_context.verify(plain_password,hashed_password)


@user.post("/register")
async def register(user:models.User):
   
   check={"username":user.username}
   hashed_password=pwd_context.hash(user.password)

   if(db.user_col.count_documents(check)):
       return JSONResponse(
            status_code=409,
            content={"status": "failed", "message": "Username already exists!"},
        )
   
   data ={
      "username":user.username,
      "password":hashed_password
    }
   
   db.user_col.insert_one(data)
   
   token=tf.generate_token(user)

   return {"status":"success","token":token}

   
@user.post("/login")
async def login(user:models.User):
    data=db.user_col.find_one({"username":user.username})

    if not data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username ")
    
    if not verify(data["password"],user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
    
    token=tf.generate_token(user)

    return {"status": "success", "token": token}





    


