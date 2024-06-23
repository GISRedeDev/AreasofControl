from unittest.mock import patch

import pytest

from areasofcontrol.get_data import filter_ids, get_geojson, get_history


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
