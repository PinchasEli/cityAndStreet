from fastapi import Request, HTTPException

from services.user_service import UserService
from enums.search_user_by import SearchUserBy


class VerifyPermission:

    @staticmethod
    async def verify_superuser_key(request: Request):
        api_key = request.headers.get("x-api-key")
        if api_key:
            user = await UserService().get_user(api_key, SearchUserBy.api_key)
            if user and not user.get("is_superuser"):
                raise HTTPException(status_code=403, detail="Forbidden: Invalid superuser")

            return

        raise HTTPException(status_code=401, detail="Unauthorized: API key is missing or invalid")

    @staticmethod
    async def verify_read_only(request: Request):
        api_key = request.headers.get("x-api-key")
        if api_key:
            user = await UserService().get_user(api_key, SearchUserBy.api_key)
            if user:
                if user.get("is_superuser"):
                    return
                elif request.method in ["PUT", "DELETE", "POST"]:
                    raise HTTPException(status_code=403, detail="Forbidden: Insufficient permissions")

                return

        raise HTTPException(status_code=401, detail="Unauthorized: API key is missing or invalid")
