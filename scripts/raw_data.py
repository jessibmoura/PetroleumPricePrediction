import requests
from loguru import logger
from dotenv import load_dotenv
import os
from utils import gap_years
import json

load_dotenv()

def generate():
    """ Generates the raw_data file """
    data = []
    years = gap_years(3)
    for year in years:
        json_data = ipeadata(date_start=f"{year}-01-01",
                             date_end=f"{year}-12-31")
        data.append(json_data)
    with open("data/raw/raw_data.json","w") as file:
        json.dump(data,file)
    return data

def ipeadata(date_start: str, date_end: str):
    """ API call to the U.S. Energy Information Administration 
    
    The api_key used on the call is disponibilized by the organization site 
    itself. To get it, just register yourself on the website. """
    api_key = os.getenv('API_KEY')
    url = f"https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={api_key}&frequency=daily&data[0]=value&start={date_start}&end={date_end}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    logger.error("API's response was not ok: please check the parameters passed.")
    return None

if __name__ == "__main__":
    generate()