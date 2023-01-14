import json

from src.models.point import PointModel
from src.services.elastic import ESManager
from src.services.geocode import GeocodeService
from src.services.interfaces.import_interface import ImportInterface
from src.services.log import logger as log_service
from src.services.point import PointService
import xml.etree.ElementTree as ET
import xmltodict
import logging as logger


class XmlImporter(ImportInterface):
    input: str = None,
    collection: list = []
    __pointService: PointService
    __dataSource: ESManager
    __geocodeService: GeocodeService

    def __init__(self):
        self.__pointService = PointService()
        self.__dataSource = ESManager()
        self.__geocodeService = GeocodeService()

    def set_input(self, input_data: str):
        self.input = input_data

    async def parse(self) -> list:
        failed = False
        if await self.validate_data() is False:
            raise Exception("Failed to validate given data.")

        try:
            importDict = await self.__parse_to_dict()
            point = PointModel.parse_obj(importDict)

            self.collection.append(point)
        except Exception as e:
            logger.error(f"Import error. Can't parse data. Details {e}")
            failed = True

        if failed is False:
            return self.collection
        else:
            raise Exception("Found errors. See logs for details.")

    async def import_data(self) -> None:
        if len(self.collection) == 0:
            raise Exception("Empty collection. Firstly parse data.")

        for item in self.collection:
            if not isinstance(item, PointModel):
                raise Exception("Cannot import data. Broken or bad payload.")

            geocoder = await self.__geocodeService.geocode(item)
            item.set_location(lat=geocoder["lat"], lon=geocoder["lon"])
            await self.__dataSource.add(item)

    async def validate_data(self) -> bool:
        if self.input is None:
            logger.error(f"Import error. No input data found.")
            return False

        try:
            ET.fromstring(self.input)
            return True
        except ET.ParseError as e:
            logger.error(f"Import error. Problem with parsing input data. Details {e}")
            return False

    async def __parse_to_dict(self) -> list:
        try:
            return xmltodict.parse(self.input)["collection"]["point"]
        except Exception as e:
            logger.error(f"Import error. Cannot parse xml to json. Details {e}")
            raise Exception("Import error. Cannot parse xml to json.")
