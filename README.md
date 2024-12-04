# PetroleumPricePrediction

This project aims to create a time series model capable of predicting the price value of Petroleum, specifically the price per barrel of Brent crude oil. Produced in the North Sea (Europe), Brent is a class of crude oil that serves as a benchmark for the international price of different types of oil.

The data used for this project is available at the [U.S. Energy Information Administration](https://www.eia.gov/).

## Requirements

Before running the project, ensure that you have the following:

1. **Create a `.env` file** with your personal API key for the U.S. Energy Information Administration (EIA). You can obtain this key by registering on their website. Add the following line to the `.env` file:
    ```
    API_KEY=your_personal_api_key
    ```

2. Install the necessary Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Project Structure

The project directory structure is as follows:

```

├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources, such as OPEC.
│   ├── processed      <- The final datasets for modeling.
│   └── raw            <- Raw data obtained from the EIA API.
│
│
├── models             <- Trained models and related files
│
├── notebooks          <- Jupyter notebooks for analysis and experimentation
│
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── pipeline.py        <- Script to run the complete process of training and generating a model
│
│
├── config.yaml        <- Configuration file for model parameters and data paths
│
├── plan_deploy_models.pdf    <- Planning to do the models deploy
│
├── app.py             <- Interative dashboard created using Streamlit to show data 
│
│
└── petroleumpriceprediction   <- Main package containing the project logic
    │
    ├── __init__.py             <- Makes petroleumpriceprediction a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── data.py                 <- Scripts to load and process data
    │
    └── model.py                <- Class to implement models functionalities
```

## Running the Project

To train the model and generate predictions, simply run the `pipeline.py` script from the root directory of the project:
```bash
python pipeline.py
```

## Dashboard

You can check the project's dashboard on the link: [Petroleum Price](https://fiap-tc4-petroleumpriceprediction.streamlit.app/), or
run the following command: 
```bash
streamlit run app.py
```


## GitHub

Link to GitHub project: [PetroleumPricePrediction](https://github.com/jessibmoura/PetroleumPricePrediction).
