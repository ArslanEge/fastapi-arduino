from fastapi import APIRouter,HTTPException,status,Request,FastAPI
import models
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import database as db
import tokenfile as tf
import datetime
from datetime import datetime
from bson.objectid import ObjectId
from jose import JWTError, jwt
import requests
from fastapi.middleware.cors import CORSMiddleware




index=0
liste=["egearslan","ozerarslan","sarparslan","dorukarslan"]

JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = "HS256"

app1=FastAPI()
origins = [
   "http:// 192.168.0.11.:8000",
   "http://localhost",
   "http://localhost:8080",
]

app1.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ard=APIRouter(
    prefix="/arduino",
    tags=["arduino"]
)
flutter=APIRouter(
    prefix="/flutter",
    tags=["flutter"]
)

@app1.middleware("http")
async def flutter_middleware(request: Request, call_next):
    headers = request.headers
    if "Authorization" in headers:
        token = request.headers["Authorization"]
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            request.state.username = data["username"]
            request.state.userID = data["user_id"]
        except:
            return JSONResponse(
                status_code=403,
                content={
                    "status": "failed",
                    "message": "Authentication Failed",
                },
            )
    else:
        return JSONResponse(
            status_code=403,
            content={
                "status": "failed",
                "message": "Authentication Failed",
            },
        )
    response = await call_next(request)
    return response


@app1.get("/getHeat/{date_time}")
async def get_user_courses(request: Request,data_time:str):
    try:
        user = db.user_col.find_one({"_id": ObjectId(request.state.userID)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        heat_ids = user["heat"]
        heats = []
        for heat_id in heat_ids:
            heat = db.heat_col.find_one({"_id": ObjectId(heat_id)})
            if heat:
                # convert ObjectId to string
                if(heat["date_time"]==data_time):
                    return{"heat":heat}
                

            return {"heat could not found"}
            
    except:
        return JSONResponse(
            status_code=403,
            content={
                "status": "failed",
                "message": "Couldn't get the courses!",
            },
        )

@ard.delete("/delete/{delete_id}")
async def delete_heat(username:str,delete_id:str):
    user = db.user_col.find_one({"username":username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    heat_obj_id = ObjectId(delete_id)
    if heat_obj_id not in user["heat"]:
            raise HTTPException(status_code=400, detail="Course not found for user")

        # Delete the course from the courses collection
    db.heat_col.delete_one({"_id":heat_obj_id})
    
    db.user_col.update_one(
            {"username":username},
            {"$pull": {"heat":heat_obj_id}},
        )
    return {"item was deleted"}
    

@ard.post("/heat")
async def add_heat(value:models.Arduino):
  global index
  
  heat_dicit = value.dict()
  
  result = db.heat_col.insert_one(heat_dicit)
  heat_id = result.inserted_id
  
  db.user_col.update_one(
            {"username": liste[index]}, {"$push": {"heat": heat_id}}
        )
  index = (index + 1) % len(liste)


  return {"SELAM"}


@ard.get("/get")
async def get_heat(temperature:str,humidity:str):
        url = 'https://fastapi-arduino.herokuapp.com/arduino/heat'
        now = datetime.now()

        current_month = str(now.month)
        current_day = str(now.day)
        current_hour = str(now.hour+3)
        current_minute = str(now.minute)

        date_time = str(current_month+"/"+current_day+"/"+current_hour+"/"+current_minute)

        # create the data to be sent in the HTTP POST request
        tvalue=str(temperature)
        hvalue=str(humidity)
        data = {
            'temperature': tvalue,
            'humidity': hvalue,
            'date_time': date_time
        }
        header = {
      'Content-Type': 'application/json',
    }

        # make the HTTP POST request
        try:
            response = requests.post(url,json=data,timeout=10,headers=header)
            response.raise_for_status()  # raise an exception for 4xx/5xx status codes
            print('Data successfully sent!')
        except requests.exceptions.HTTPError as e:
            print('Failed to send data: {}'.format(e))
        except requests.exceptions.RequestException as e:
            print('Request error: {}'.format(e))

        return "WORKED"

    





