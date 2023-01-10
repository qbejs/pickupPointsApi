import json
import uuid
from datetime import datetime
from urllib.request import Request

from fastapi import APIRouter, Depends, HTTPException

from src.db import User
from src.models.core import HealthcheckResponse
from src.models.dto.get_point_search_dto import GetSearchParamsDTO
from src.models.dto.patch_point_dto import PatchPointDTO
from src.models.point import PointModel
from src.models.users import current_active_user
from src.services.elastic import ESManager
from src.services.point import PointService
from src.services.geocode import GeocodeService
from src.models.dto.post_add_point_dto import PostAddPointDTO
from src.models.dto.get_geocode_nominatim_dto import GetGeocodeNominatimDTO
from src.models.responses.geocode_response import GeocodeResponse
from src.services.log import logger as log_service
from src.services.importers.xml_importer import XmlImporter
import xml.etree.ElementTree as ET

logger = log_service()

router = APIRouter(
    prefix="/api",
)


@router.post("/point", response_model=PointModel)
async def add_point(point: PostAddPointDTO, service: PointService = Depends(PointService),
                    user: User = Depends(current_active_user)):
    try:
        resp = await service.add_point(point=point)

        return resp
    except Exception as e:
        logger.error(f"Cannot add point. Payload: {point.json()} | Error details: {e}")
        raise HTTPException(500, "Cannot add new point. Contact with support.")


@router.patch("/point/{point}", response_model=PointModel)
async def patch_point(point: str, point_data: PatchPointDTO, service: ESManager = Depends(ESManager),
                      user: User = Depends(current_active_user)):
    try:
        data = PointModel.parse_raw(point_data.json())
        resp = await service.update(payload=data, resource_id=point)

        return resp
    except Exception as e:
        logger.error(f"Cannot update point. Details: {e}")
        raise HTTPException(500, "Cannot update point.")


@router.delete("/point/{point}", response_model=PointModel)
async def delete_point(point: str, service: ESManager = Depends(ESManager),
                       encoder: json.JSONEncoder = Depends(json.JSONEncoder),
                       user: User = Depends(current_active_user)):
    try:
        resp = await service.findOne(element_id=point)
        delete = await service.delete(payload=PointModel.parse_raw(encoder.encode(resp["hits"]["hits"][0]["_source"])))

        return delete
    except Exception as e:
        logger.error(f"Cannot delete point. Details: {e}")
        raise HTTPException(500, "Cannot delete point.")


@router.post("/point/import/{file_type}")
async def import_points(file: bytes, file_type: str, user: User = Depends(current_active_user)):
    payload = file.decode()

    if file_type == 'xml':
        service = XmlImporter()
        service.set_input(payload)
        await service.import_data()
        return {"status": "success"}

    raise HTTPException(400, "Unsupported file type")
