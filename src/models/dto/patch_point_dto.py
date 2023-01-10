from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Dict, Union, Optional


class PatchPointDTO(BaseModel):
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
