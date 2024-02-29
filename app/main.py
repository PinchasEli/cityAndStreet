from fastapi import FastAPI
from routers import street

from routers import city

app = FastAPI()

app.include_router(street.router, prefix="/street", tags=["street"])
app.include_router(city.router, prefix="/city", tags=["city"])
