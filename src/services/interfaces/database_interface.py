import json
import string

from src.models.point import PointModel


class DatabaseInterface:
    async def get_connection_status(self) -> bool:
        pass

    async def get_connection_details(self) -> json:
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

    def __generate_connection_url(self) -> string:
        pass
