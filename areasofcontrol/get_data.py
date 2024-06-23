import requests

def get_history() -> list[int]:
    url = "https://deepstatemap.live/api/history/"
    response = requests.get(url)
    ids = [x["id"] for x in response.json()]
    return ids