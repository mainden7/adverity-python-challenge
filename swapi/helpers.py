from typing import Any
from datetime import datetime


def convert_timezone_aware_datetime_string(dt_string: str) -> str:
    dt = datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S.%f%z")
    return dt.strftime("%Y-%m-%d")


def transform(
    peoples_list: list[dict[str, Any]], planets_list: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    planets = {planet["url"]: planet["name"] for planet in planets_list}
    for row in peoples_list:
        row["homeworld_name"] = planets[row["homeworld"]]
        row["date"] = convert_timezone_aware_datetime_string(row["edited"])
    return peoples_list
