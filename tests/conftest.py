import json
from pathlib import Path

import pytest

BASE_DATA = Path(__file__).parent.joinpath("test_data")


@pytest.fixture
def get_history_mock_data():
    mock_history_json = BASE_DATA.joinpath("history.json")
    with open(mock_history_json, "r", encoding="utf-8") as f:
        yield json.load(f)


@pytest.fixture
def ids_mock_data(get_history_mock_data):
    response = get_history_mock_data
    ids = [x["id"] for x in response]
    yield ids


@pytest.fixture
def geojson_mock_positive():
    # Data is occupied
    mock_geojson = BASE_DATA.joinpath("positive_geojson.json")
    with open(mock_geojson, "r", encoding="utf-8") as f:
        mock_geojson = json.load(f)
    yield mock_geojson


@pytest.fixture
def geojson_mock_negative():
    # Data is not occupied
    mock_geojson_file = BASE_DATA.joinpath("negative_geojson.json")
    with open(mock_geojson_file, "r", encoding="utf-8") as f:
        mock_geojson = json.load(f)
    yield mock_geojson


@pytest.fixture
def geojson_mocks(geojson_mock_positive, geojson_mock_negative):
    return {"positive": geojson_mock_positive, "negative": geojson_mock_negative}
