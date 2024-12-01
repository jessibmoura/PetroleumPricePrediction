from petroleumpriceprediction.model import SARIMAXPredictor
from petroleumpriceprediction import data

from scripts.raw_data import generate
from scripts.process_data import organize_data

import yaml
from loguru import logger

def load_config(filepath: str) -> dict:
    """Carrega as configurações do arquivo .yaml."""
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)
    return config

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
    process_filepath = config["data"]["process_filepath"]
    dataset_filepath = config["data"]["dataset_filepath"]
    logger.info("Preprocessing data...")
    organize_data(raw_filepath, process_filepath)
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
    model_filepath = config["model"]["save_path"]
    sarimax.save(model_filepath)

if __name__ == "__main__":
    main()