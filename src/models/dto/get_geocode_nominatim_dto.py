from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Dict, Union


class GetGeocodeNominatimDTO(BaseModel):
    lat: Union[float, None] = None
    lon: Union[float, None] = None
    addressStreet: str
    addressBuildingNumber: str
    addressVoivodeship: str
    addressProvince: str
    addressCity: str
    addressCountry: str = "Poland"

    def __str__(self):
        return f"{self.addressCountry},{self.addressVoivodeship},{self.addressProvince},{self.addressCity},{self.addressStreet} {self.addressBuildingNumber}"
