from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username:str
    password:str


class Arduino(BaseModel):
    temperature:str
    humidity:str
    date_time1:str
    
