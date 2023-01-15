from pydantic import BaseModel


class PostAddPointRequest(BaseModel):
    name: str
    code: str
    city: str
    country: str
    voivodeship: str
    province: str
    street: str
    buildingNumber: str
