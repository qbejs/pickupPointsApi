import uuid
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Dict, Union


class PointModel(BaseModel):
    id: UUID = uuid.uuid4()
    created_at: datetime = datetime.now()
    updated_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None
    name: str
    code: str
    country: str
    city: str
    voivodeship: str
    province: str
    street: str
    buildingNumber: str
    location: Union[dict, None] = None

    def is_deleted(self) -> bool:
        if self.deleted_at is None:
            return False
        else:
            return True

    def set_location(self, lat: float, lon: float) -> object:
        self.location = {
            "lat": lat,
            "lon": lon
        }

        return self

    def __str__(self):
        return f"{self.country},{self.voivodeship},{self.province},{self.city},{self.street} {self.buildingNumber}"
