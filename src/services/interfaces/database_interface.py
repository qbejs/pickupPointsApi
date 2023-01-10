import json
import string
from typing import Union

from src.models.dto.get_geocode_nominatim_dto import GetGeocodeNominatimDTO
from src.models.point import PointModel


class DatabaseInterface:
    async def getConnectionStatus(self) -> bool:
        pass

    async def getConnectionDetails(self) -> json:
        pass

    async def add(self, payload: object) -> PointModel:
        pass

    async def update(self, payload: object, resource_id: string) -> PointModel:
        pass

    async def delete(self, payload: object) -> PointModel:
        pass

    async def findOne(self, payload: object) -> json:
        pass

    async def findBy(self, payload: object) -> json:
        pass

    async def findAll(self) -> json:
        pass

    def __generateConnectionUrl(self) -> string:
        pass
