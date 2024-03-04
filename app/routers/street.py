from fastapi import APIRouter, HTTPException

from models import Street
from services import StreetService

router = APIRouter()


@router.post("/")
async def create_street(street: Street):
    return await StreetService().create_street(street)


@router.get("/")
async def get_all_streets():
    return await StreetService().get_all_streets()


@router.get("/{street_name}")
async def get_street(street_name: str): 
    street = await StreetService().get_street(street_name)
    if street:
        return street

    raise HTTPException(status_code=404, detail="Street not found")


@router.put("/{street_id}")
async def update_street(street_id: str, street_data: Street):
    updated_street = await StreetService().update_street(street_id, street_data)
    print(updated_street)
    if updated_street:
        return updated_street

    raise HTTPException(status_code=404, detail="Street not Update or found")


@router.delete("/{street_id}")
async def delete_street(street_id: str):
    deleted_count = await StreetService().delete_city(street_id)
    if deleted_count == 1:
        return {"message": "Street deleted successfully"}

    raise HTTPException(status_code=404, detail="Street not found")
