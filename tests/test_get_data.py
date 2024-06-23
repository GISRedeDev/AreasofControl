from unittest.mock import patch

import pytest

from areasofcontrol.get_data import filter_ids, get_history


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
