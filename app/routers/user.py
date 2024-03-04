from fastapi import APIRouter, HTTPException

from services import UserService
from models import User
from enums import SearchUserBy
router = APIRouter()


@router.post("/")
async def create_user(user_data: User):
    api_key = await UserService().create_user(user_data)
    return {"api_key": api_key}


# @router.get("/")
# async def get_all_users():
#     users = await UserService().get_all_users()
#     return {"users": users}


@router.get("/")
async def get_user(value: str, by: SearchUserBy):
    if by not in SearchUserBy.__members__.values():
        raise HTTPException(status_code=404, detail=f"Invalid value for 'by': {by}")

    user = await UserService().get_user(value, by)
    if user:
        return {"user": user}

    raise HTTPException(status_code=404, detail="User not found")


@router.put("/{user_id}")
async def update_user(user_id: str, user_data: User):
    updated_user = await UserService().update_user(user_id, user_data)
    if updated_user:
        return updated_user

    raise HTTPException(status_code=404, detail="User not Update or found")


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    deleted_count = await UserService().delete_user(user_id)
    if deleted_count == 1:
        return {"message": "User deleted successfully"}

    raise HTTPException(status_code=404, detail="User not found")
