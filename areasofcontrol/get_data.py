from datetime import datetime, timedelta
from pathlib import Path

import geopandas as gpd
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


def get_geojson(id: int) -> dict:
    url = f"https://deepstatemap.live/api/history/{id}/geojson/"
    response = requests.get(url)
    polygon_features = []
    for feature in response.json()["features"]:
        if feature["geometry"]["type"] in ["Polygon", "MultiPolygon"]:
            polygon_features.append(feature)
    filtered_geojson = {"type": "FeatureCollection", "features": polygon_features}
    return filtered_geojson


def filter_and_save(geojson: dict, id: int, gpkg_dir: Path | str) -> None:
    assert Path(gpkg_dir).is_dir()
    if not Path(gpkg_dir).exists():
        Path(gpkg_dir).mkdir(parents=True)
    gdf = gpd.GeoDataFrame.from_features(geojson)
    gdf = gdf[gdf["name"].str.contains("уп|ОРДЛО|Крим", case=False)]
    if not gdf.empty:
        layer = datetime.fromtimestamp(id).strftime("%Y-%m-%d")
        gdf = gdf.dissolve(by=None)
        gdf["date"] = layer
        gdf.to_file(
            Path(gpkg_dir).joinpath(f"{layer}.gpkg"), layer=layer, driver="GPKG"
        )
