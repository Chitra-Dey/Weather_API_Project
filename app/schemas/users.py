from pydantic import BaseModel
from typing import Optional


class TokenData(BaseModel):
    username: str    


class UserIn(BaseModel):
    username: str
    email: str
    password: str
   
class LoginData(BaseModel):
    username: str
    password: str