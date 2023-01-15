import logging as logger
import xml.etree.ElementTree as ET

import xmltodict
from pydantic import ValidationError
from src.models.point import PointModel
from src.services.geocode import GeocodeService
from src.services.interfaces.import_interface import ImportInterface
from src.services.point import PointService


class XmlImporter(ImportInterface):
    input: str = (None,)
    collection: list = []
    __pointService: PointService
    __geocodeService: GeocodeService

    def __init__(self):
        self.__pointService = PointService()
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
        except (ValueError, TypeError, ValidationError) as e:
            logger.error("Import error. Can't parse data. Details %s", e)
            failed = True

        if failed is False:
            return self.collection

        raise Exception("Found errors. See logs for details.")

    async def import_data(self) -> None:
        if len(self.collection) == 0:
            raise Exception("Empty collection. Firstly parse data.")

        for item in self.collection:
            if not isinstance(item, PointModel):
                raise Exception("Cannot import data. Broken or bad payload.")

            geocoder = await self.__geocodeService.geocode(item)
            item.set_location(lat=geocoder["lat"], lon=geocoder["lon"])
            await self.__pointService.add_point(item)

    async def validate_data(self) -> bool:
        if self.input is None:
            logger.error("Import error. No input data found.")
            return False

        try:
            ET.fromstring(self.input)
            return True
        except ET.ParseError as e:
            logger.error("Import error. Problem with parsing input data. Details %s", e)
            return False

    async def __parse_to_dict(self) -> list:
        try:
            return xmltodict.parse(self.input)["collection"]["point"]
        except (ValueError, TypeError) as e:
            logger.error("Import error. Cannot parse xml to json. Details %s", e)
            raise Exception("Import error. Cannot parse xml to json.")
