import json
from typing import Union

from src.models.requests.get_geocode_nominatim_request import GetGeocodeNominatimRequest
from src.models.point import PointModel


class GeocoderInterface:
    async def geocode(
        self,
        payload: Union[GetGeocodeNominatimRequest, PointModel],
        reverse: bool = False,
    ) -> json:
        pass

    async def make_request(
        self, url: str, data: str, resp_format: str = "json"
    ) -> json:
        pass
