import json
import os
import string
from datetime import datetime

from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException

from src.models.point import PointModel
from src.services.geocode import GeocodeService
from src.services.interfaces.database_interface import DatabaseInterface

load_dotenv()


class ESManager(DatabaseInterface):
    es: AsyncElasticsearch = None
    geocoderService: GeocodeService = None

    def __init__(self):
        try:
            self.es = AsyncElasticsearch([self.generate_connection_url()])
            self.geocoderService = GeocodeService()
        except Exception as e:
            raise HTTPException(
                500, f"Cannot initialize connection with elasticsearch. Details: {e}"
            )

    async def getConnectionStatus(self):
        return await self.es.ping(pretty=True, human=True)

    async def getConnectionDetails(self):
        return await self.es.info(pretty=True, human=True)

    async def add(self, payload: object) -> PointModel:
        if isinstance(payload, PointModel):
            await self.es.create(
                index="points", id=str(payload.id), document=payload.json()
            )
            return payload

        raise HTTPException(400, "Unsupported payload")

    async def update(self, payload: object, resource_id: str) -> PointModel:
        if isinstance(payload, PointModel):
            if payload.id != resource_id:
                raise HTTPException(400, "Invalid payload")
            geocode = await self.geocoderService.geocode(payload=payload)
            payload.set_location(lat=geocode["lat"], lon=geocode["lon"])
            payload.updated_at = datetime.now()
            await self.es.update(index="points", id=str(payload.id), doc=payload.dict())
            return payload

        raise HTTPException(400, "Unsupported payload")

    async def delete(self, payload: object) -> PointModel:
        if isinstance(payload, PointModel):
            payload.updated_at = datetime.now()
            payload.deleted_at = datetime.now()
            await self.es.update(index="points", id=str(payload.id), doc=payload.dict())
            return payload

        raise HTTPException(400, "Unsupported payload")

    async def findOne(self, element_id: str) -> json:
        return await self.es.search(
            index="points", query={"query": {"match": {"id": element_id}}}
        )

    async def findBy(self, payload: object) -> json:
        """
        TO DO
        """

    async def rangeSearch(self, lat: float, lon: float, search_range: int = 10):
        return await self.es.search(
            index="points",
            query={
                "bool": {
                    "must": {"match_all": {}},
                    "filter": {
                        "geo_distance": {
                            "distance": f"{search_range}km",
                            "location": {"lat": lat, "lon": lon},
                        }
                    },
                }
            },
        )

    async def findAll(self) -> json:
        return await self.es.search(index="points", query={"match_all": {}})

    def generate_connection_url(self) -> string:
        return (
            f"{'https://' if os.getenv('ES_SSL') == 'True' else 'http://'}"
            f"{os.getenv('ES_USER')}:{os.getenv('ES_PASS')}"
            f"@{os.getenv('ES_HOST')}:{os.getenv('ES_PORT')}"
        )
