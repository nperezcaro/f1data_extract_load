from unittest.mock import patch
from src.extract import get_yearly_sessions_data

URL = "https://api.openf1.org/v1/sessions"


@patch("src.extract.requests.get")
def test_get_yearly_sessions_data(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "session_key": 9465,
            "session_name": "Practice 1",
            "date_start": "2024-02-29T11:30:00+00:00",
            "date_end": "2024-02-29T12:30:00+00:00",
            "gmt_offset": "03:00:00",
            "session_type": "Practice",
            "meeting_key": 1229,
            "location": "Sakhir",
            "country_key": 36,
            "country_code": "BRN",
            "country_name": "Bahrain",
            "circuit_key": 63,
            "circuit_short_name": "Sakhir",
            "year": 2024,
        },
        {
            "session_key": 9466,
            "session_name": "Practice 2",
            "date_start": "2024-02-29T15:00:00+00:00",
            "date_end": "2024-02-29T16:00:00+00:00",
            "gmt_offset": "03:00:00",
            "session_type": "Practice",
            "meeting_key": 1229,
            "location": "Sakhir",
            "country_key": 36,
            "country_code": "BRN",
            "country_name": "Bahrain",
            "circuit_key": 63,
            "circuit_short_name": "Sakhir",
            "year": 2024,
        },
    ]

    response = get_yearly_sessions_data(url=URL, year="2024")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "year" in response.json()[0]
