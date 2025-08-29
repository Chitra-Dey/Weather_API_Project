from sqlmodel import Field, SQLModel 
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr
from uuid import UUID
import uuid


class User(SQLModel,table=True):
    id :uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True,primary_key=True) 
    email: EmailStr = Field(index=True)
    hashed_password: str=Field(index=True)
   