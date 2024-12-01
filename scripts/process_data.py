import json
import polars as pl
import pandas as pd
import pendulum
from loguru import logger

def organize_data(raw_filepath: str, save_filepath: str):
    """ Takes the raw_data and process it """
    dataframe = pl.DataFrame(schema = {"id": pl.String, "date": pl.Date,"price": pl.Float64})

    # Open and read the JSON file
    with open(raw_filepath, 'r') as file:
        data = json.load(file)
    
    # Process each year at a time
    for response in data:
        daily_registers = response["response"]["data"]
        for register in daily_registers:
        # Gets the specific kind of petroleum we want to study
            if register["series-description"] == "Europe Brent Spot Price FOB (Dollars per Barrel)":
                new_row = pl.DataFrame({
                    "id": [register["series-description"]],
                    "date": [pendulum.parse(register["period"]).date()],
                    "price": [float(register["value"])]
                })
                dataframe = pl.concat([dataframe, new_row], how="vertical")
    
    dataframe.write_csv(save_filepath)
    logger.success("Successfully organized data and saved it!")
