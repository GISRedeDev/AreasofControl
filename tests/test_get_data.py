from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import fiona
import pytest

from areasofcontrol.get_data import (
    filter_and_save,
    filter_ids,
    get_geojson,
    get_history,
)

TEST_DIR = Path(__file__).parent.joinpath("test_data")


@patch("requests.get")
def test_get_history(mock_get, get_history_mock_data):
    mock_get.return_value.json.return_value = get_history_mock_data
    ids = get_history()
    assert len(ids) > 0
    assert 1706735973 in ids


@pytest.mark.parametrize(
    "start_date, end_date, expected_len",
    [
        ("2024-01-22", "2024-01-31", 10),
        ("2024-01-26", "2024-01-29", 5),
        ("2024-01-01", "2024-01-21", 0),
        ("2024-01-31", "2024-01-31", 1),
    ],
)
def test_filter_ids(ids_mock_data, start_date, end_date, expected_len):
    filtered_ids = filter_ids(ids_mock_data, start_date, end_date)
    assert len(filtered_ids) == expected_len


@pytest.mark.parametrize("geojson_key", ["positive", "negative"])
@patch("requests.get")
def test_get_geojson(mock_get, geojson_key, geojson_mocks):
    mock_get.return_value.json.return_value = geojson_mocks[geojson_key]
    geojson = get_geojson(1)
    assert geojson["type"] == "FeatureCollection"
    assert "Point" not in [x["geometry"]["type"] for x in geojson["features"]]
    assert all(
        x["geometry"]["type"] in ["Polygon", "MultiPolygon"]
        for x in geojson["features"]
    )


@pytest.mark.parametrize("geojson_key", ["positive", "negative"])
@patch("requests.get")
def test_filter_and_save(mock_get, geojson_key, geojson_mocks):
    mock_get.return_value.json.return_value = geojson_mocks[geojson_key]
    geojson = get_geojson(1)
    filter_and_save(geojson, 1706735973, TEST_DIR.joinpath("test.gpkg"))
    if geojson_key == "positive":
        assert TEST_DIR.joinpath("test.gpkg").exists()
        layer = datetime.fromtimestamp(1706735973).strftime("%Y-%m-%d")
        assert layer in fiona.listlayers(TEST_DIR.joinpath("test.gpkg"))
        TEST_DIR.joinpath("test.gpkg").unlink()
    else:
        assert not TEST_DIR.joinpath("test.gpkg").exists()
