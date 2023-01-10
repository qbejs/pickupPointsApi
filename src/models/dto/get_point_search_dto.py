from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Dict, Union


class GetSearchParamsDTO(BaseModel):
    lat: Union[float, None] = None
    lon: Union[float, None] = None
    distance: int = None
    addressStreet: str = None
    addressBuildingNumber: str = None
    addressVoivodeship: str = None
    addressProvince: str = None
    addressCity: str = None
    addressCountry: str = "Poland"
