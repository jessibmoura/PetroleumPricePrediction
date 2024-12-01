import pandas as pd
import statsmodels.api as statsmodelapi
import pickle

class SARIMAXPredictor:
    def __init__(self, order, seasonal_order, trend=None):
        """
        Inicializa o modelo SARIMAX.
        
        Args:
        - order (tuple): Parâmetros ARIMA (p, d, q).
        - seasonal_order (tuple): Parâmetros sazonais (P, D, Q, s).
        - trend (str, optional): Componente de tendência ('n', 'c', 't', 'ct').
        """
        self.order = order
        self.seasonal_order = seasonal_order
        self.trend = trend
        self.model = None
        self.results = None

    def fit(self, data):
        """
        Ajusta o modelo SARIMAX aos dados.
        
        Args:
        - data (pd.Series or pd.DataFrame): Série temporal para treinar o modelo.
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
        print("Model was successfully adjusted!")

    def forecast(self, steps):
        """
        Realiza previsões.
        
        Args:
        - steps (int): Número de passos (dias/períodos) para prever.
        
        Returns:
        - pd.Series: Previsões para os próximos períodos.
        """
        if not self.results:
            raise ValueError("Você precisa ajustar o modelo antes de fazer previsões.")
        
        forecast = self.results.get_forecast(steps=steps)
        return forecast.predicted_mean

    def save(self, file_path):
        """
        Salva o modelo treinado em um arquivo.
        
        Args:
        - file_path (str): Caminho para salvar o modelo.
        """
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)
        print(f"Modelo salvo em {file_path}")

    @staticmethod
    def load(file_path):
        """
        Carrega o modelo treinado de um arquivo.
        
        Args:
        - file_path (str): Caminho para o arquivo salvo.
        
        Returns:
        - SARIMAXPredictor: Instância da classe carregada.
        """
        with open(file_path, 'rb') as f:
            return pickle.load(f)
