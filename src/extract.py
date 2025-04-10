import polars as pl
import requests

from src.config import BASE_URL


def get_yearly_sessions_data(url: str, year: str) -> requests.Response:
    """
    This function takes an API's URL and a year to use in the query, it returns a Response object.

    Args:
        url: The API's URL to make the call.
        year: The year to use as param in the API query.

    Returns:
        requests.Response: A Response with the API's answer.
    """
    response = requests.get(url=url, params={"year": year})

    return response


def get_dimension_data_from_session_key(
    dimension: str, sesion_key: int
) -> requests.Request:
    """
    This function takes a dimension and a session key to use in the query, it returns a Response object.

    Args:
        dimension (str): The dimension to which data will be extracted. Needs to be a dimension that can be filtered by session key.
        session_key (int): The session_key to use as param in the API query.

    Returns:
        requests.Response: A Response with the API's answer.

    Raises:
        ValueError: if API's answer has a status code different to 200.
    """
    url = BASE_URL + dimension
    request = requests.get(url=url, params={"session_key": sesion_key})

    if request.status_code != 200:
        raise ValueError(f"Request failed with code: {request.status_code}.")
    return request


def get_df_from_response(response: requests.Response) -> pl.DataFrame:
    """
    This function takes a Response object, it returns a Polars DataFrame.

    Args:
        response (requests.Response): Response object from an API call.

    Returns:
        df (pl.DataFrame): Polars DataFrame with the content of the Response object.

    Raises:
        ValueError: if the Polars DataFrame to return is empty.
    """
    df = pl.DataFrame(data=response.json())

    if not df.is_empty():
        return df
    else:
        raise ValueError("DF created from response is empty!")
