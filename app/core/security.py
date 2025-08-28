from fastapi import Depends,HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from models.user_model import User
from database.db import get_db
from sqlalchemy.orm import Session
from schemas.users import TokenData
import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

context = CryptContext(schemes=["bcrypt"],deprecated="auto")

oauth2=OAuth2PasswordBearer(tokenUrl='auth/login')

def check_password(simple_password,hashed_password):
    return context.verify(simple_password,hashed_password)

def hash_password(password:str):
    return context.hash(password)

def create_token(data:dict,expire:timedelta|None=None):
    to_encode=data.copy()
    if expire:
        expiree=datetime.now(timezone.utc)+expire
    else:
        expiree=datetime.now(timezone.utc)+timedelta(minutes=5)
    to_encode.update({"exp":expiree})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db:Session,username:str):
    try:
        user=db.query(User).filter(User.username==username).first()
    except Exception as e:
        print(e)
        user=None
    return user

def get_current_user(token:str=Depends(oauth2),session:Session=Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    token_data = TokenData(username=username)
    user = session.query(User).filter(User.username == token_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user