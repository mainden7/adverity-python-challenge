import asyncio
import math
from datetime import datetime

import petl as etl
from typing import Any

from aiohttp import ClientSession
from django.conf import settings

from swapi.helpers import transform
from swapi.models import FilesCollection


class APIDataReader:
    @staticmethod
    async def _fetch(sess: ClientSession, url: str) -> dict[str, Any]:
        response = await sess.get(url)
        response_json = await response.json()
        return response_json

    async def fetch_paginated(self, base_url: str) -> list[dict[str, Any]]:
        async with ClientSession() as session:
            response_json = await self._fetch(session, base_url)
            total_count = response_json.get("count", 0)
            first_page_result = response_json.get("results", [])
            last_page = int(
                math.ceil(total_count / len(response_json.get("results")))
            )
            tasks = []
            for page_num in range(2, last_page + 1):
                url = f"{base_url}/?page={page_num}"
                tasks.append(asyncio.create_task(self._fetch(session, url)))

            results = await asyncio.gather(*tasks)

            return sum(
                [r.get("results", []) for r in results], first_page_result
            )


class SWAPIPeopleDataReader(APIDataReader):
    def load_data(self) -> list[dict[str, Any]]:
        fetch_endpoint = f"{settings.SWAPI_BASE_URL}/people"
        data = asyncio.run(self.fetch_paginated(fetch_endpoint))
        return data


class SWAPIPlanetsDataReader(APIDataReader):
    def load_data(self) -> list[dict[str, Any]]:
        fetch_endpoint = f"{settings.SWAPI_BASE_URL}/planets"
        data = asyncio.run(self.fetch_paginated(fetch_endpoint))
        return data


class SWAPIDataWriter:
    @staticmethod
    def save_data(data: list[dict[str, Any]]) -> None:
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.csv")
        file_source = settings.FILES_BASE_DIR / filename
        etl.tocsv(table=etl.fromdicts(data), source=file_source)
        collection = FilesCollection(file=filename)
        collection.save()


class SWAPIDataCSVReader:
    @staticmethod
    def load_data(
        filename: str, headers: list[str], start: int = 0, limit: int = 0
    ):
        file_source = settings.FILES_BASE_DIR / filename
        data = etl.fromcsv(file_source)
        data = etl.cut(data, *headers)
        if limit > 0:
            data = etl.rowslice(data, start, limit)
        return data

    def get_value_count(
        self, filename: str, headers: list[str], columns: list[str]
    ):
        data = self.load_data(filename, headers)
        data_aggregated = etl.aggregate(
            data, key=columns, aggregation=len
        ).sort("value", reverse=True)
        return data_aggregated


class SWAPIDataAPICollector:
    def collect_all(self) -> None:
        people_data = SWAPIPeopleDataReader().load_data()
        planets_data = SWAPIPlanetsDataReader().load_data()
        data = transform(people_data, planets_data)
        SWAPIDataWriter().save_data(data)
