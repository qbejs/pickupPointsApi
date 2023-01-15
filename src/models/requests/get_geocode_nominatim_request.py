from typing import Union
from pydantic import BaseModel


class GetGeocodeNominatimRequest(BaseModel):
    lat: Union[float, None] = None
    lon: Union[float, None] = None
    addressStreet: str
    addressBuildingNumber: str
    addressVoivodeship: str
    addressProvince: str
    addressCity: str
    addressCountry: str = "Poland"

    def __str__(self):
        return (
            f"{self.addressCountry},"
            f"{self.addressVoivodeship}"
            f",{self.addressProvince},"
            f"{self.addressCity},"
            f"{self.addressStreet} {self.addressBuildingNumber}"
        )
