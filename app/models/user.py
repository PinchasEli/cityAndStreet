import secrets

from pydantic import BaseModel, validator


class User(BaseModel):
    username: str
    api_key: str = None
    is_superuser: bool = False
    is_staff: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        if not self.api_key:
            self.generate_api_key()

    def generate_api_key(self):
        self.api_key = secrets.token_urlsafe(16)

    @validator("username")
    def check_username(cls, username_value):
        assert username_value, "username is required"
        return username_value
