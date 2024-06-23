from unittest.mock import patch
import pytest

from areasofcontrol.get_data import get_history


@patch('requests.get')
def test_get_history(mock_get, get_history_mock_data):
    mock_get.return_value.json.return_value = get_history_mock_data
    ids = get_history()
    assert len(ids) > 0
    assert 1706735973 in ids


