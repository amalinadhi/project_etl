"""Load data source"""

import joblib

from src.util import logging


def to_pickle(data: any, filepath: str) -> None:
    """
    Dump data to a .pkl file

    Parameters
    ----------
    data : any
        The data you want to dump

    filepath : str
        The file path
    """
    try:
        joblib.dump(data, filepath)
        logging.print_debug(f"Successfuly dump the data to {filepath}!")

    except Exception as error:
        raise RuntimeError("Path is invalid")
