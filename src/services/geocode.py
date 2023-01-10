import asyncio
import json
import os
import aiohttp
from typing import Union

from src.services.interfaces.geocode_interface import GeocoderInterface
from src.models.dto.get_geocode_nominatim_dto import GetGeocodeNominatimDTO
from dotenv import load_dotenv
from fastapi import HTTPException

from src.models.point import PointModel

load_dotenv()


class GeocodeService(GeocoderInterface):
    async def geocode(self, payload: Union[GetGeocodeNominatimDTO, PointModel], reverse: bool = False) -> json:

        if reverse is True:
            if isinstance(payload, GetGeocodeNominatimDTO) and (payload.lat is None or payload.lon is None):
                raise HTTPException(400, "Lat and Lon is required in payload")

            if isinstance(payload, PointModel) and (payload.location["lat"] is None or payload.location["lon"] is None):
                raise HTTPException(400, "Lat and Lon is required in payload")

        resp = await self.make_request(url=os.getenv('NOMINATIM_URL'), data=payload.__str__())

        return resp[0]

    async def make_request(self, url: str, data: str, resp_format: str = "json") -> json:
        async with aiohttp.ClientSession() as session:
            async with session.get(os.getenv('NOMINATIM_URL'),
                                   params={"q": data, "format": resp_format}) as resp:
                return await resp.json()
