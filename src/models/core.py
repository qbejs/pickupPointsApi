from datetime import datetime
from typing import Union
from uuid import UUID
from pydantic import BaseModel


class HealthcheckResponse(BaseModel):
    id: UUID
    timestamp: datetime
    system_status: str
    connection_details: Union[dict, None] = None
