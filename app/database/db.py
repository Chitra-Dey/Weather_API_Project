from typing import Annotated 
from fastapi import Depends,FastAPI , HTTPException , Query
from sqlmodel import Field ,Session ,SQLModel,create_engine,select

sqlite_url = f'sqlite:///database.db'
connect_args = {"check_same_thread":False}
engine = create_engine(sqlite_url,connect_args=connect_args)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_db)]        




