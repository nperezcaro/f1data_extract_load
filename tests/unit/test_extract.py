from unittest.mock import patch, Mock
from hypothesis import given, settings, strategies as st
from src.extract import get_yearly_sessions_data, get_df_from_response

import polars as pl

URL = "https://api.openf1.org/v1/sessions"


def create_mock_response_data(year=2024):
    """Helper function to create mock response data."""
    return [
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
            "year": year,
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
            "year": year,
        },
    ]


@patch("src.extract.requests.get")
def test_get_yearly_sessions_data(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = create_mock_response_data()

    response = get_yearly_sessions_data(url=URL, year="2024")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "year" in response.json()[0]


@patch("src.extract.requests.get")
@settings(deadline=1000, max_examples=2)
@given(year=st.sampled_from(["2023", "2024"]))
def test_get_yearly_sessions_data_with_parameter(mock_get, year):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = create_mock_response_data(year=year)

    response = get_yearly_sessions_data(url=URL, year=year)
    assert response.status_code == 200


def test_get_df_from_response():
    mock_data = create_mock_response_data()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data

    df = get_df_from_response(response=mock_response)
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (2, 14)
    assert df["session_key"].to_list() == [9465, 9466]
    assert df["year"].to_list() == [2024, 2024]
