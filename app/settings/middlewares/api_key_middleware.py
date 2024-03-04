from fastapi import Request, HTTPException

from services.user_service import UserService
from enums.search_user_by import SearchUserBy


async def verify_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key is missing")
    elif not await UserService.authenticate_by_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")


async def check_api_key(request: Request, call_next):
    await verify_api_key(request)
    response = await call_next(request)
    return response
