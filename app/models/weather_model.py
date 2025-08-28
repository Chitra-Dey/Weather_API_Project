from sqlmodel import Field,SQLModel 
from datetime import datetime, timedelta , timezone

class WeatherHistory(SQLModel,table = True):
    id: int= Field(primary_key = True,default = None)
    city: str
    description:str
    temperature:str
    pressure: int
    humidity : int
    wind_speed : float
    searched_at : datetime = Field(default_factory = datetime.utcnow)
    user_id : str = Field(default = None , foreign_key = "user.id")