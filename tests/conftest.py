import json
import pytest
from pathlib import Path

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

