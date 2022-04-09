from pathlib import Path
import pandas as pd
from typing import Optional
import pickle

def load_model():
    file_path = Path(__file__).resolve()
    data_path = file_path.parents[3].joinpath('AI','finalizedmodel.sav')
    # print(data_path)
    x = pickle.load(open(data_path, 'rb'))
    return x
    
    
def load_data() -> Optional[pd.DataFrame]:
    """
    TODO - Add scraper
    """
    # temp
    
    file_path = Path(__file__).resolve()
    # print("TU", file_path)
    data_path = file_path.parents[3].joinpath('data','data.csv')
    # print(data_path)
    
    if not data_path.is_file():
        return None

    df = pd.read_csv(data_path)
    return df