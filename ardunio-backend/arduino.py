from fastapi import APIRouter,HTTPException,status
import models
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import database as db
import tokenfile as tf
import datetime
from datetime import datetime
from bson.objectid import ObjectId
import requests

index=0
liste=["egearslan","ozerarslan","sarparslan","dorukarslan"]

ard=APIRouter(
    prefix="/arduino",
    tags=["arduino"]
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

   
