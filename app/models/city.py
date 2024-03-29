from pydantic import BaseModel


class City(BaseModel):
    name: str
    population: int
    country: str
