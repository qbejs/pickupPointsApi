from typing import Union
from pydantic import BaseModel


class GetSearchParamsRequest(BaseModel):
    lat: Union[float, None] = None
    lon: Union[float, None] = None
    distance: int = None
    addressStreet: str = None
    addressBuildingNumber: str = None
    addressVoivodeship: str = None
    addressProvince: str = None
    addressCity: str = None
    addressCountry: str = "Poland"
