import requests
from loguru import logger
from dotenv import load_dotenv
import os
import pendulum
import json

# API key is accessed using environment variables
load_dotenv()

def generate(number_years: int, file_path: str):
    """ Generates the raw_data json file 
    
    Parameters
    ----------
    number_years: int
        number of years to get of data
    file_path: str
        path to save raw data file
    """
    data = []
    years = gap_years(number_years)
    for year in years:
        json_data = ipeadata(date_start=f"{year}-01-01",
                             date_end=f"{year}-12-31")
        data.append(json_data)
    with open(file_path,"w") as file:
        json.dump(data,file)
        logger.success("Succefully created raw data file!")

def ipeadata(date_start: str, date_end: str):
    """ API call to the U.S. Energy Information Administration 
    
    The api_key used on the call is disponibilized by the organization site 
    itself. To get it, just register yourself on the website.

    Parameters
    ----------
    date_start: str
        start date to get data
    date_end: str
        end date to get data
    """
    api_key = os.getenv('API_KEY')
    url = f"https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={api_key}&frequency=daily&data[0]=value&start={date_start}&end={date_end}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    logger.error("API's response was not ok: please check the parameters passed.")
    return None

def gap_years(x: int) -> list[pendulum.DateTime]:
    """ Gets the last x years of data 
    
    Parameters
    ----------
    x: int
        number of years to get of data
    """
    dates = []
    date_now = pendulum.now()
    for i in range(1,x+1):
        sub_year = date_now.subtract(years=i)
        dates.append(sub_year.format("YYYY"))
    return dates