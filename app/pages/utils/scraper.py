from pathlib import Path
import pandas as pd
from typing import Optional


def load_data() -> Optional[pd.DataFrame]:
    """
    TODO - Add scraper
    """
    # temp
    
    file_path = Path(__file__).resolve()
    data_path = file_path.parents[2].joinpath('data.csv')

    if not data_path.is_file():
        return None

    df = pd.read_csv(data_path)
    return df