from datetime import datetime, timedelta

import requests


def get_history() -> list[int]:
    url = "https://deepstatemap.live/api/history/"
    response = requests.get(url)
    ids = [x["id"] for x in response.json()]
    return ids


def filter_ids(ids: list[int], start_date: str, end_date: str) -> list[int]:
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1, seconds=-1)
    filtered_timestamps = [
        ts for ts in ids if start_dt <= datetime.fromtimestamp(ts) <= end_dt
    ]

    return filtered_timestamps
