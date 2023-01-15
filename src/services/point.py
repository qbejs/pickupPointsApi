import json
from typing import Union

from dotenv import load_dotenv
from fastapi import HTTPException

from src.models.requests.get_point_search_request import GetSearchParamsRequest
from src.models.requests.patch_point_request import PatchPointRequest
from src.models.requests.post_add_point_request import PostAddPointRequest
from src.models.point import PointModel
from src.services.elastic import ESManager
from src.services.geocode import GeocodeService

load_dotenv()


class PointService:
    __geocodeService: GeocodeService
    __dataSource: ESManager

    def __init__(self):
        self.__geocodeService = GeocodeService()
        self.__dataSource = ESManager()

    async def add_point(
        self, point: Union[PostAddPointRequest, PointModel]
    ) -> PointModel:
        newPoint = PointModel(
            name=point.name,
            code=point.code,
            country=point.country,
            voivodeship=point.voivodeship,
            province=point.province,
            city=point.city,
            street=point.street,
            buildingNumber=point.buildingNumber,
        )
        geocode = await self.__geocodeService.geocode(newPoint)
        newPoint.set_location(lat=geocode["lat"], lon=geocode["lon"])

        await self.__dataSource.add(newPoint)

        return newPoint

    async def update_point(
        self, point: str, point_data: Union[PatchPointRequest, PointModel]
    ) -> PointModel:
        data = PointModel.parse_raw(point_data.json())
        resp = await self.__dataSource.update(payload=data, resource_id=point)

        return resp

    async def delete_point(self, point_id: str) -> PointModel:
        encoder = json.JSONEncoder()
        resp = await self.__dataSource.findOne(element_id=point_id)
        delete = await self.__dataSource.delete(
            payload=PointModel.parse_raw(
                encoder.encode(resp["hits"]["hits"][0]["_source"])
            )
        )

        return delete

    async def point_search(
        self, search_type: str, params: Union[GetSearchParamsRequest, PointModel]
    ) -> json:
        if search_type == "address":
            pass

        if search_type == "range":
            try:
                return await self.__dataSource.rangeSearch(
                    lat=params.lat, lon=params.lon, search_range=params.distance
                )
            except Exception as e:
                raise HTTPException(500, f"Range search error. Details: {e}")

        raise HTTPException(400, "Not enough params or wrong search type")
