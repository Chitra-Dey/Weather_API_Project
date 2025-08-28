from fastapi import FastAPI
from routers import authentication,weather
from database.db import create_db


app = FastAPI(title = 'Weather API Proxy')
@app.on_event('startup')
def create_db_and_tables():
    create_db() 

app.include_router(authentication.router, prefix="/auth")
app.include_router(weather.routers,prefix="/weather")