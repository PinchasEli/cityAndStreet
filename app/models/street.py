from pydantic import BaseModel


class Street(BaseModel):
    name: str
    city: str
    # state: str
    # zipcode: str
