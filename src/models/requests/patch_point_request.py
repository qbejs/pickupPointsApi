from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class PatchPointRequest(BaseModel):
    id: UUID
    created_at: datetime
    deleted: Optional[bool]
    name: str
    code: str
    city: str
    country: str
    voivodeship: str
    province: str
    street: str
    buildingNumber: str
