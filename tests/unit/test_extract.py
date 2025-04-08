from unittest.mock import Mock, patch

import polars as pl
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from src.config import SESSIONS_URL, SESSIONS_DIMENSIONS
from src.extract import (
    get_df_from_response,
    get_yearly_sessions_data,
    get_dimension_data_from_session_key,
)


def create_mock_sessions_response_data(year=2024):
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
    mock_response.json.return_value = create_mock_sessions_response_data()

    response = get_yearly_sessions_data(url=SESSIONS_URL, year="2024")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "year" in response.json()[0]


@patch("src.extract.requests.get")
@settings(deadline=1000, max_examples=2)
@given(year=st.sampled_from(["2023", "2024"]))
def test_get_yearly_sessions_data_with_parameter(mock_get, year):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = create_mock_sessions_response_data(year=year)

    response = get_yearly_sessions_data(url=SESSIONS_URL, year=year)
    assert response.status_code == 200


def create_mock_drivers_response_data() -> list[dict[str, any]]:
    """Helper function to create mock response data."""
    return [
        {
            "session_key": 9673,
            "meeting_key": 1233,
            "broadcast_name": "M VERSTAPPEN",
            "country_code": "NED",
            "first_name": "Max",
            "full_name": "Max VERSTAPPEN",
            "headshot_url": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/1col/image.png",
            "last_name": "Verstappen",
            "driver_number": 1,
            "team_colour": "3671C6",
            "team_name": "Red Bull Racing",
            "name_acronym": "VER",
        },
        {
            "session_key": 9673,
            "meeting_key": 1233,
            "broadcast_name": "O PIASTRI",
            "country_code": "AUS",
            "first_name": "Oscar",
            "full_name": "Oscar PIASTRI",
            "headshot_url": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/O/OSCPIA01_Oscar_Piastri/oscpia01.png.transform/1col/image.png",
            "last_name": "Piastri",
            "driver_number": 81,
            "team_colour": "FF8000",
            "team_name": "McLaren",
            "name_acronym": "PIA",
        },
    ]


@patch("src.extract.requests.get")
def test_get_dimension_data_from_session_key_drivers(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = create_mock_drivers_response_data()

    session_key = 9673
    response = get_dimension_data_from_session_key(
        dimension=SESSIONS_DIMENSIONS[0], sesion_key=session_key
    )

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert "session_key" in data[0]
    assert data[0]["session_key"] == session_key
    assert data[1]["session_key"] == session_key
    assert data[0]["full_name"] == "Max VERSTAPPEN"
    assert data[1]["full_name"] == "Oscar PIASTRI"


@patch("src.extract.requests.get")
def test_get_dimension_data_from_session_key_wrong_status_code(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 500

    session_key = 9673

    with pytest.raises(ValueError, match="Request failed with code: 500."):
        get_dimension_data_from_session_key(
            dimension=SESSIONS_DIMENSIONS[0], sesion_key=session_key
        )


def test_get_df_from_response():
    mock_data = create_mock_sessions_response_data()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data

    df = get_df_from_response(response=mock_response)
    assert isinstance(df, pl.DataFrame)
    assert df.shape == (2, 14)
    assert df["session_key"].to_list() == [9465, 9466]
    assert df["year"].to_list() == [2024, 2024]


def test_get_df_from_response_empty_response():
    mock_data = []
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data

    with pytest.raises(ValueError):
        get_df_from_response(response=mock_response)
