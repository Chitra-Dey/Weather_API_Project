from fastapi import Depends,HTTPException, status ,Request
from passlib.context import CryptContext
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from datetime import datetime,timedelta,timezone
from models.user_model import User
from database.db import get_db
from sqlalchemy.orm import Session
from schemas.users import TokenData
from settings import settings
import jwt
import uuid
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def check_password(simple_password,hashed_password):
    return context.verify(simple_password,hashed_password)

def hash_password(password:str):
    return context.hash(password)

def create_token(data:uuid.UUID,refresh=False)->str:
    payload={}
    payload.update({'sub':str(data),'refresh':refresh})

    if not refresh:
        exp=int((datetime.now()+timedelta(minutes=5)).timestamp())
    else:
        exp=int((datetime.now()+timedelta(days=5)).timestamp())
    payload.update({'exp':exp})
    token=jwt.encode(payload,settings.JWT_SECRET,settings.JWT_ALGO)
    return token

def decode_access_token(token:str)->uuid.UUID:
    try:
        payload = jwt.decode(token,settings.JWT_SECRET,algorithms=[settings.JWT_ALGO])
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={'message':'Invalid Token','data':str(e)})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={'message':'Error while decoding the token','data':str(e)})    
    if payload['refresh']:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail={'message':'This is not an access token'})
    return uuid.UUID(payload['sub'])

class DecodeToken(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__ (auto_error=auto_error)

    async def __call__(self, request:Request):
        data:HTTPAuthorizationCredentials=await super().__call__(request)
        token=data.credentials
        user_id=decode_access_token(token)
        return user_id

def get_user(id:uuid.UUID=Depends(DecodeToken()),db:Session=Depends(get_db)):
    user=db.get(User,id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')
    return user
