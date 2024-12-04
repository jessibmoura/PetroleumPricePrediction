import pandas as pd
import statsmodels.api as statsmodelapi
import pickle

class SARIMAXPredictor:
    """
    A class to build, train, and use a SARIMAX model for time series forecasting.
    """
    def __init__(self, order: tuple, seasonal_order: tuple, trend: str = None):
        """
        Initializes the SARIMAX model with specified parameters.
        
        Parameters
        ----------
        order : tuple
            ARIMA parameters (p, d, q).
        seasonal_order : tuple
            Seasonal ARIMA parameters (P, D, Q, s).
        trend : str, optional
            Trend component ('n', 'c', 't', 'ct'), by default None.
        """
        self.order = order
        self.seasonal_order = seasonal_order
        self.trend = trend
        self.model = None
        self.results = None

    def fit(self, data: pd.DataFrame):
        """
        Fits the SARIMAX model to the provided data.
        
        Parameters
        ----------
        data : pd.DataFrame
            A DataFrame containing the time series to train the model on. 
            It must include a column "y" with the target variable.
        """
        self.model = statsmodelapi.tsa.statespace.SARIMAX(
            endog=data["y"],
            order=self.order,
            seasonal_order=self.seasonal_order, 
            trend=self.trend,
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        self.results = self.model.fit(disp=False)
        print("Model was successfully fitted!")

    def forecast(self, steps: int) -> pd.Series:
        """
        Makes forecasts for the specified number of steps ahead.
        
        Parameters
        ----------
        steps : int
            Number of steps (e.g., days, periods) to forecast.
        
        Returns
        -------
        pd.Series
            Forecasted values for the specified future periods.
        
        Raises
        ------
        ValueError
            If the model has not been fitted yet.
        """
        if not self.results:
            raise ValueError("You must fit the model before making forecasts.")
        
        forecast = self.results.get_forecast(steps=steps)
        return forecast.predicted_mean

    def save(self, file_path: str):
        """
        Saves the trained model to a file.
        
        Parameters
        ----------
        file_path : str
            Path where the model should be saved.
        """
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
        print(f"Model saved to {file_path}")

    @staticmethod
    def load(file_path: str) -> 'SARIMAXPredictor':
        """
        Loads a trained SARIMAX model from a file.
        
        Parameters
        ----------
        file_path : str
            Path to the saved model file.
        
        Returns
        -------
        SARIMAXPredictor
            An instance of the loaded SARIMAXPredictor class.
        """
        with open(file_path, 'rb') as f:
            return pickle.load(f)