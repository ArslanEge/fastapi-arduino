from fastapi import APIRouter,HTTPException,status
import models
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import database as db
import tokenfile as tf
import datetime
from datetime import datetime
import requests
import pytz



ard=APIRouter(
    prefix="/arduino",
    tags=["arduino"]
)

def get_current_date_time():
    # set the timezone to 'Europe/Istanbul'
    tz = pytz.timezone('Europe/Istanbul')

    # get the current time in Istanbul's local time
    now = datetime.datetime.now(tz)

    # extract the month, day, hour, and minute from the current time
    current_month = now.month
    current_day = now.day
    current_hour = now.hour
    current_minute = now.minute

    # convert the values to strings
    current_month_str = str(current_month).zfill(2) # adds a leading zero if necessary
    current_day_str = str(current_day).zfill(2)
    current_hour_str = str(current_hour).zfill(2)
    current_minute_str = str(current_minute).zfill(2)

    # create a date/time string in the format: "MM/DD HH:MM"
    date_time = current_month_str + '/' + current_day_str + ' ' + current_hour_str + ':' + current_minute_str

    # return the date/time string
    return date_time


@ard.post("/heat")
async def add_heat(value:models.Arduino):
  
  heat_dicit=value.dict()
  
  result=db.heat_col.insert_one(heat_dicit)

  return {"SELAM"}



@ard.get("/get")
async def get_heat(temperature:str,humidity:str):
        url = 'https://fastapi-arduino.herokuapp.com/arduino/heat'
        

        # create the data to be sent in the HTTP POST request
        tvalue=str(temperature)
        hvalue=str(humidity)
        data = {
            'temperature': tvalue,
            'humidity': hvalue,
            'date_time': get_current_date_time()
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

   
