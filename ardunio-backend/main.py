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





