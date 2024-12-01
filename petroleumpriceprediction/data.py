import pandas as pd

def load(filepath: str) -> pd.DataFrame:
    """Carrega os dados a partir de um arquivo."""
    data = pd.read_csv(filepath,
                       sep=',',
                        parse_dates=['date']
                    )
    return data

def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    """Realiza pré-processamento, como lidar com NaNs e ordenar os dados."""
    data.rename(columns={"id": "unique_id",
                   "date":"ds",
                   "price":"y"}, inplace=True)
    data.sort_values(by='ds', ascending=True, inplace=True)
    data.reset_index(inplace=True)
    data.drop(columns=["index"],inplace=True)
    data = data.dropna()
    return data