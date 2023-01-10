import json
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from src.models.core import HealthcheckResponse
from src.models.dto.get_point_search_dto import GetSearchParamsDTO
from src.models.dto.patch_point_dto import PatchPointDTO
from src.models.point import PointModel
from src.services.elastic import ESManager
from src.services.point import PointService
from src.services.geocode import GeocodeService
from src.models.dto.post_add_point_dto import PostAddPointDTO
from src.models.dto.get_geocode_nominatim_dto import GetGeocodeNominatimDTO
from src.models.responses.geocode_response import GeocodeResponse
from src.services.log import logger as log_service
from src.services.importers.xml_importer import XmlImporter

logger = log_service()

router = APIRouter(
    prefix="/api",
)


@router.get("/health", response_model=HealthcheckResponse)
async def healthcheck(es: ESManager = Depends(ESManager)):
    health_check = {
        "id": uuid.uuid4(),
        "timestamp": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        "system_status": "FAILURE"
    }

    try:
        if await es.getConnectionStatus():
            health_check["system_status"] = "SUCCESS"
            health_check["connection_details"] = await es.getConnectionDetails()
    except Exception as e:
        logger.error(f"Health check failed. Details: {e}")

    return health_check


'''
GEOCODING
'''


@router.get("/geocode", response_model=GeocodeResponse)
async def geocode_point(payload: GetGeocodeNominatimDTO, service: GeocodeService = Depends(GeocodeService)):
    try:
        return await service.geocode(payload=payload, reverse=False)
    except Exception as e:
        logger.error(f"Problem with geocoding. Payload: {payload.json()} | Error details: {e}")
        return {
            "lat": 0.0,
            "lon": 0.0
        }


'''
POINT
'''


@router.get("/point/{point}", response_model=PointModel)
async def get_point(point: str, service: ESManager = Depends(ESManager)):
    try:
        resp = await service.findOne(element_id=point)

        if len(resp["hits"]["hits"]) == 0:
            raise HTTPException(404, "Point not found")

        if len(resp["hits"]["hits"]) > 1:
            logger.error(f"More than one record found for given point id. Point ID: {point}")
            raise HTTPException(409, "Cannot process given point. Contact with support.")

        return resp["hits"]["hits"][0]["_source"]
    except Exception as e:
        logger.error(f"Cannot get point data. Point ID: {point} | Error details: {e}")
        raise HTTPException(500, "Cannot get point data. Contact with support.")


@router.get("/point", response_model=list[PointModel])
async def get_points(service: ESManager = Depends(ESManager)):
    try:
        collection = []
        resp = await service.findAll()

        for item in resp["hits"]["hits"]:
            collection.append(item["_source"])

        return collection
    except Exception as e:
        logger.error(f"Cannot get point collection. Details: {e}")


'''
POINT SEARCH ENGINE
'''


@router.get("/point/search/{search_type}", response_model=list[PointModel])
async def get_point(search_type: str, params: GetSearchParamsDTO, service: PointService = Depends(PointService)):
    try:
        collection = []
        resp = await service.point_search(search_type, params)

        for item in resp["hits"]["hits"]:
            collection.append(item["_source"])

        return collection
    except Exception as e:
        logger.error(
            f"Problem with search engine. Search type: {search_type} | Payload: {params.json()} | Error details: {e}")

        if e.args[0] == 400 or e.args[0] == 404:
            print(e.args[0])
            raise HTTPException(e.args[0], e.__str__())

        return []