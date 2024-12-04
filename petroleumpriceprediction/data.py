import pandas as pd

def load(filepath: str) -> pd.DataFrame:
    """Loads data from a CSV file.
    
    Parameters
    ----------
    filepath : str
        Path to the CSV file containing the data.
    
    Returns
    -------
    pd.DataFrame
        The loaded DataFrame with parsed dates.
    """
    data = pd.read_csv(filepath, 
                       sep=',', 
                       parse_dates=['date'])
    return data

def preprocess(data: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses the input data by handling missing values and sorting it.
    
    Parameters
    ----------
    data : pd.DataFrame
        The input DataFrame containing raw data.
    
    Returns
    -------
    pd.DataFrame
        The preprocessed DataFrame with renamed columns, sorted by date, and NaN values removed.
    """
    data.rename(columns={"id": "unique_id",
                         "date": "ds",
                         "price": "y"}, inplace=True)
    data.sort_values(by='ds', ascending=True, inplace=True)
    data.reset_index(inplace=True)
    data.drop(columns=["index"], inplace=True)
    data = data.dropna()
    return data
