from fastapi import HTTPException
from unittest.mock import patch
from requests.exceptions import HTTPError
import pytest

from app.services.delivery_fee_service import get_static_venue_data

@pytest.fixture
def mock_response():
    with patch('requests.get') as mock_get:
        yield mock_get

def test_get_static_venue_data(mock_response):
    mock_response = mock_response.return_value

def test_get_static_venue_data_handles_404(mock_response):
    mock_response = mock_response.return_value
    mock_response.status_code = 404
    mock_response.json.return_value = {"message": "Venue not found"}
    mock_response.raise_for_status.side_effect = HTTPError

    with pytest.raises(HTTPException) as exc_info:
        get_static_venue_data("invalid-slug")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "HTTP error occurred: Venue not found"