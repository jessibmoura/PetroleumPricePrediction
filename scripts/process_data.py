import json
import polars as pl
import pendulum

def organize_data():
    """ Takes the raw_data and process it """
    dataframe = pl.DataFrame(schema = {"id": pl.String, "date": pl.Date,"price": pl.Float64})

    # Open and read the JSON file
    with open('data/raw/raw_data.json', 'r') as file:
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
    
    dataframe.write_csv("data/processed/petroleum_price.csv")
    print("\nCSV file saved succefully!\n")

if __name__ == "__main__":
    organize_data()
