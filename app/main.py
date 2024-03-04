from fastapi import Depends, FastAPI

from settings.middlewares.api_key_middleware import check_api_key
from settings.middlewares.verify_permission_middleware import VerifyPermission
from settings.middlewares.custom_response_middleware import custom_response_middleware

from routers import street, city, user

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["user"], dependencies=[Depends(VerifyPermission.verify_superuser_key)])
app.include_router(street.router, prefix="/street", tags=["street"], dependencies=[Depends(VerifyPermission.verify_read_only)])
app.include_router(city.router, prefix="/city", tags=["city"], dependencies=[Depends(VerifyPermission.verify_read_only)])

app.middleware("http")(check_api_key)
app.middleware("http")(custom_response_middleware)
