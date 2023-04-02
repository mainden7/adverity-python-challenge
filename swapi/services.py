import asyncio
from datetime import datetime

import petl as etl
from typing import Any

import aiohttp
from django.conf import settings

from swapi.models import FilesCollection


class SWAPIDataJSONReader:
    @staticmethod
    async def _fetch_paginated(url: str) -> list[dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            data = []
            page = 1
            while True:
                # make HTTP request to the API endpoint
                params = {"page": page}
                async with session.get(url, params=params) as response:
                    response_json = await response.json()

                    # add results to data list
                    data.extend(response_json["results"])

                    # check if there are more pages to fetch
                    next_url = response_json["next"]
                    if not next_url:
                        break

                    # increment the page number and fetch the next page
                    page += 1

            return data

    async def _load_data(self, url: str) -> list[dict[str, Any]]:
        data = await self._fetch_paginated(url)
        return data

    def load_data(self) -> list[dict[str, Any]]:
        fetch_endpoint = f"{settings.SWAPI_BASE_URL}/people"
        data = asyncio.run(self._load_data(fetch_endpoint))
        return data


class SWAPIDataCSVWriter:
    @staticmethod
    def save_data(data: list[dict[str, Any]]) -> None:
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S.csv")
        file_source = settings.FILES_BASE_DIR / filename
        etl.tocsv(table=data, source=file_source)
        collection = FilesCollection(file=filename)
        collection.save()


class SWAPIDataCollector(SWAPIDataJSONReader, SWAPIDataCSVWriter):
    def collect_all(self) -> None:
        data = self.load_data()
        self.save_data(data)
