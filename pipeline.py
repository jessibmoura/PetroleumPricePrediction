from petroleumpriceprediction.model import SARIMAXPredictor
from petroleumpriceprediction import data
from petroleumpriceprediction.config import load_config

from scripts.raw_data import generate
from scripts.process_data import organize_data

from loguru import logger

def main():
    # Carregando as configurações
    config = load_config("config.yaml")

    # Raw data
    create_rawdata = config["data"]["create_rawdata"]
    raw_filepath = config["data"]["raw_filepath"]
    if create_rawdata:
        size = config["data"]["size"]
        logger.info("Getting raw data")
        logger.info(f"Size: {size}")
        generate(size,raw_filepath)

    # Pre process raw data
    dataset_filepath = config["data"]["dataset_filepath"]
    logger.info("Preprocessing data...")
    organize_data(raw_filepath, dataset_filepath)
    logger.success("Dataset for model created!")

    # Prepare data for model
    dataset = data.load(dataset_filepath)
    dataset = data.preprocess(dataset)
    print(dataset.head())

    # Training model
    logger.info("Training model...")
    order = config["model"]["sarimax_order"]
    seasonal_order = config["model"]["seasonal_order"]
    sarimax = SARIMAXPredictor(order=order, 
                               seasonal_order=seasonal_order)
    sarimax.fit(dataset)

    # Testing forecast
    forecast = sarimax.forecast(steps=5)
    print(forecast)

    # Saving model file
    model_filepath = config["model"]["path"]
    sarimax.save(model_filepath)

if __name__ == "__main__":
    main()