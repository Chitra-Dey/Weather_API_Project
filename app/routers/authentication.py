from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlmodel import select
from database.db import get_db
from core.security import hash_password, check_password, get_current_user, create_token
from models.user_model import User
from schemas.users import UserIn, TokenData
from datetime import timedelta, datetime

router = APIRouter()

@router.post("/register", response_model=User) 
def register_user(user_data:UserIn,db:Session=Depends(get_db)):
    '''register a user'''
    hashed_password=hash_password(user_data.password)
    user_data=user_data.model_dump(exclude='password')
    user_data.update({'hashed_password':hashed_password,'created_at':datetime.now()})
    user=User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''login a user'''

    username=form_data.username
    password=form_data.password

    user=db.exec(select(User).where(User.username==username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    if not check_password(password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid password'
        )

    access_token=create_token({"sub": str(user.username)})
    return {'access_token':access_token,"token_type": "bearer"}

@router.get('/check_me')
def get_recent_user(user:User=Depends(get_current_user)):
    '''Check currently authenticated user'''
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }   