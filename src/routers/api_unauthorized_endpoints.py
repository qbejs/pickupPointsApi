import uuid
from datetime import datetime
import logging as logger
from typing import List

from aiohttp import ClientError as NominatimRequestError
from elastic_transport import ApiError, TransportError
from fastapi import APIRouter, Depends, HTTPException

from src.models.core import HealthcheckResponse
from src.models.requests.get_geocode_nominatim_request import GetGeocodeNominatimRequest
from src.models.requests.get_point_search_request import GetSearchParamsRequest
from src.models.point import PointModel
from src.models.responses.geocode_response import GeocodeResponse
from src.services.elastic import ESManager
from src.services.geocode import GeocodeService
from src.services.point import PointService


router = APIRouter(
    prefix="/api",
)


@router.get("/health", response_model=HealthcheckResponse)
async def healthcheck(es: ESManager = Depends(ESManager)):
    health_check = {
        "id": uuid.uuid4(),
        "timestamp": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        "system_status": "FAILURE",
    }

    try:
        if await es.getConnectionStatus():
            health_check["system_status"] = "SUCCESS"
            health_check["connection_details"] = await es.getConnectionDetails()
            return health_check
        return health_check
    except (ValueError, ApiError, TransportError) as e:
        logger.error("Health check failed. Details: %s", e)


@router.get("/geocode", response_model=GeocodeResponse)
async def geocode_point(
    payload: GetGeocodeNominatimRequest,
    service: GeocodeService = Depends(GeocodeService),
):
    try:
        return await service.geocode(payload=payload, reverse=False)
    except (ValueError, NominatimRequestError) as e:
        logger.error(
            "Problem with geocoding. Payload: %s | Error details: %s", payload.json(), e
        )
        return {"lat": 0.0, "lon": 0.0}


@router.get("/point/{point}", response_model=PointModel)
async def get_point(point: str, service: ESManager = Depends(ESManager)):
    try:
        resp = await service.findOne(element_id=point)

        if len(resp["hits"]["hits"]) == 0:
            raise HTTPException(404, "Point not found")

        if len(resp["hits"]["hits"]) > 1:
            logger.error(
                "More than one record found for given point id. Point ID: %s", point
            )
            raise HTTPException(
                409, "Cannot process given point. Contact with support."
            )

        return resp["hits"]["hits"][0]["_source"]
    except (ValueError, ApiError, TransportError) as e:
        logger.error(
            "Cannot get point data. Point ID: %s | Error details: %s", point, e
        )
        raise HTTPException(500, "Cannot get point data. Contact with support.")


@router.get("/point", response_model=List[PointModel])
async def get_points(service: ESManager = Depends(ESManager)):
    try:
        collection = []
        resp = await service.findAll()

        for item in resp["hits"]["hits"]:
            collection.append(item["_source"])

        return collection
    except (ValueError, ApiError, TransportError) as e:
        logger.error("Cannot get point collection. Details: %s", e)


@router.get("/point/search/{search_type}", response_model=List[PointModel])
async def point_search(
    search_type: str,
    params: GetSearchParamsRequest,
    service: PointService = Depends(PointService),
):
    try:
        collection = []
        resp = await service.point_search(search_type, params)

        for item in resp["hits"]["hits"]:
            collection.append(item["_source"])

        return collection
    except (ValueError, ApiError, TransportError) as e:
        logger.error(
            "Problem with search engine. Search type: %s | Payload: %s} | Error details: %s",
            search_type,
            params.json(),
            e,
        )

        if e.args[0] == 400 or e.args[0] == 404:
            print(e.args[0])
            raise HTTPException(e.args[0], str(e))

        return []
