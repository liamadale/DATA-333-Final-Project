import pandas as pd
from typing import Iterable, Union


def export_to_csv(data: Union[pd.DataFrame, Iterable[dict]], file_path: str) -> pd.DataFrame:
    """Save data to a CSV file.

    Parameters
    ----------
    data : Union[pandas.DataFrame, Iterable[dict]]
        The data to export. Can be a DataFrame or an iterable of dictionaries.
    file_path : str
        Destination path for the CSV file.

    Returns
    -------
    pandas.DataFrame
        DataFrame representation of ``data`` that was saved.
    """
    if isinstance(data, pd.DataFrame):
        df = data
    else:
        df = pd.DataFrame(data)

    df.to_csv(file_path, index=False)
    return df
