from fastapi import FastAPI , Query, APIRouter, Depends
from .authentication import get_current_user
from database.db import get_db
from sqlmodel import Session ,select
from models.user_model import User
from models.weather_model import WeatherHistory  
from datetime import datetime, timedelta
from cache import get_from_cache, set_in_cache
from dotenv import load_dotenv 
import os
import httpx
load_dotenv()

routers = APIRouter()

cache = {}

@routers.get("/")
def root():
    '''Showing a welcome message'''
    return {'message': 'Welcome to WeatherAPI Proxy Project!'}

API_KEY = os.getenv("API_KEY")

@routers.get('/get_weather')
async def get_weather(city: str = Query(description = "Enter the City Name"),
                      user:User=Depends(get_current_user),
                      session: Session = Depends(get_db)):
    '''Handling & Fetching the weather data from external api and checking cache memory'''
    if city in cache:
        cached_entry = cache[city]
        if cached_entry["expiry"] > datetime.utcnow():
            return {
                "source": "cache",
                **cached_entry["data"]
            }
        else:
            del cache[city]

    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        myweather = response.json()
        cod=myweather.get('cod')
        if cod and cod=="404":
            return{"invalid cityname":'city not found' }
        desc = myweather["weather"][0]["description"]
        temp = myweather["main"]["temp"]
        pres = myweather["main"]['pressure']
        humid = myweather["main"]['humidity']
        windy = myweather["wind"]['speed']
        
        result = {
            "city": city,
            "weather": desc,
            "temperature": temp,
            "pressure": pres,
            "humidity": humid,
            "wind_speed": windy,
        }

        cache[city] = {
            "data": result,
            "expiry": datetime.utcnow() + timedelta(minutes=5),
        }

        new_history = WeatherHistory(
            city=city,
            description=desc,
            temperature=temp,
            pressure=pres,
            humidity=humid,
            wind_speed=windy,
            user_id=str(user.id)
        )
        session.add(new_history)
        session.commit()
        session.refresh(new_history)
        return {"source": "api", **result}
       
@routers.get("/history_of_weather")
def get_history(session: Session = Depends(get_db)):
    '''showing the searched weather history'''
    history = session.exec(select(WeatherHistory).order_by(WeatherHistory.searched_at.desc())).all()
    return history
