import requests
from loguru import logger
from dotenv import load_dotenv
import os
import pendulum
import json

# API key is accessed using environment variables
load_dotenv()

def generate(number_years: int, file_path: str) -> None:
    """
    Generates a raw data JSON file by fetching data from the U.S. Energy Information Administration (EIA) API.

    This function fetches petroleum data for a specified number of years and saves it as a JSON file.

    Parameters
    ----------
    number_years : int
        The number of years of data to fetch.
    file_path : str
        The file path where the raw data will be saved.

    Returns
    -------
    None
    """
    data = []
    years = gap_years(number_years)
    for year in years:
        json_data = ipeadata(date_start=f"{year}-01-01",
                             date_end=f"{year}-12-31")
        data.append(json_data)
    with open(file_path, "w") as file:
        json.dump(data, file)
        logger.success("Successfully created raw data file!")

def ipeadata(date_start: str, date_end: str) -> dict:
    """
    Makes an API call to the U.S. Energy Information Administration (EIA) to fetch petroleum data.

    The API key used for the call is obtained from the EIA website after registering for access.

    Parameters
    ----------
    date_start : str
        The start date for fetching data (format: YYYY-MM-DD).
    date_end : str
        The end date for fetching data (format: YYYY-MM-DD).

    Returns
    -------
    dict
        The response JSON from the API call if successful, otherwise `None`.
    """
    api_key = os.getenv('API_KEY')
    url = (
        f"https://api.eia.gov/v2/petroleum/pri/spt/data/"
        f"?api_key={api_key}&frequency=daily&data[0]=value&start={date_start}"
        f"&end={date_end}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    
    logger.error("API's response was not ok: please check the parameters passed.")
    return None


def gap_years(x: int) -> list[str]:
    """
    Generates a list of the last x years as strings.
    
    Parameters
    ----------
    x : int
        Number of years to include in the list, counting backwards from the current year.
    
    Returns
    -------
    list[str]
        A list of years in string format, representing the last x years.
    """
    dates = []
    date_now = pendulum.now()
    for i in range(1, x + 1):
        sub_year = date_now.subtract(years=i)
        dates.append(sub_year.format("YYYY"))
    return dates