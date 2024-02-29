from fastapi import APIRouter, HTTPException

from services import CityService
from models import City

router = APIRouter()


@router.post("/")
async def create_city(city_data: City):
    print(city_data)
    city_id = await CityService().create_city(city_data)
    return {"city_id": city_id}


@router.get("/")
async def get_all_cities():
    cities = await CityService().get_all_cities()
    return {"cities": cities}


@router.get("/{city_id}")
async def get_city(city_id: str):
    city = await CityService().get_city(city_id)
    if city:
        return {"city": city}

    raise HTTPException(status_code=404, detail="City not found")


@router.put("/{city_id}")
async def update_city(city_id: str, city_data: City):
    updated_city = await CityService().update_city(city_id, city_data)
    if updated_city:
        return updated_city

    raise HTTPException(status_code=404, detail="City not Update or found")


@router.delete("/{city_id}")
async def delete_city(city_id: str):
    deleted_count = await CityService().delete_city(city_id)
    if deleted_count == 1:
        return {"message": "City deleted successfully"}

    raise HTTPException(status_code=404, detail="City not found")
