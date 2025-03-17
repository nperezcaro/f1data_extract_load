import requests


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
