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

@ard.post("/heat")
async def add_heat(value:models.Arduino):
  
  heat_dict = value.dict()
  
  result = db.heat_col.insert_one(heat_dict)
  heat_id = result.inserted_id

  # Get the list of usernames
  usernames = ["egearslan", "ozerarslan", "sarparslan", "dorukarslan"]

  # Get the index of the first user with an empty heat list
  index = next((i for i, user in enumerate(db.user_col.find({"username": {"$in": usernames}})) if len(user["heat"]) == 0), None)
  if index is None:
    # If no user with an empty heat list is found, get the index of the user with the least number of heats
    index = min(enumerate(db.user_col.find({"username": {"$in": usernames}})), key=lambda x: len(x[1]["heat"]))[0]

  # Push the heat id to the user's heat list
  db.user_col.update_one({"username": usernames[index]}, {"$push": {"heat": heat_id}})

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

   
