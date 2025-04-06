import polars as pl
import requests

BASE_URL = "https://api.openf1.org/v1/"


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
