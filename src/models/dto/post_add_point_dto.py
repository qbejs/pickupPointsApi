from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Dict, Union


class PostAddPointDTO(BaseModel):
    name: str
    code: str
    city: str
    country: str
    voivodeship: str
    province: str
    street: str
    buildingNumber: str
