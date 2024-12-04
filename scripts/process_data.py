import json
import polars as pl
import pandas as pd
import pendulum
from loguru import logger

def organize_data(raw_filepath: str, save_filepath: str) -> None:
    """
    Processes raw data and saves it as a CSV file.

    This function loads a JSON file containing raw petroleum price data, filters for the specific petroleum
    type "Europe Brent Spot Price FOB (Dollars per Barrel)", and organizes it into a DataFrame. The processed 
    data is then saved to a CSV file.

    Parameters
    ----------
    raw_filepath : str
        The file path to the raw data JSON file.
    save_filepath : str
        The file path where the organized data will be saved as a CSV.

    Returns
    -------
    None
    """
    dataframe = pl.DataFrame(schema={"id": pl.String, "date": pl.Date, "price": pl.Float64})

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
