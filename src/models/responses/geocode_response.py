from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Dict, Union


class GeocodeResponse(BaseModel):
    lat: float
    lon: float
