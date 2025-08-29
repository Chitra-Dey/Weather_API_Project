Project: Weather API Proxy
Stack: FastAPI 
Requirements:
Build an API that fetches weather data from an external API (e.g., OpenWeatherMap).
Cache responses (in-memory or Redis) for 5 minutes to reduce API calls.
in cache TTL means Time to Live  here i take 300 sec
Endpoints:
GET /weather?city=London → returns current weather.
Store a history of user searches in DB.

(We will use httpx module in python to make the asynchronous API call.)

Emailstr is a special kind of email-validator

default is static but default_factory is dynamic it will update everytime in runtime,so operation like UUID genaration,date.utc() its better to use default_factory


The InMemoryBackend stores cache data in memory and only deletes when an expired key is accessed. This means that if you don't access a function after data has been cached, the data will not be removed automatically.that mean i need to write a else condition for delete a expiry data




Run with uvicorn main:app --reload