import os
import joblib

from dotenv import load_dotenv

from src._config import load_credentials



# DATA LOAD & DUMP RELATED
def load_spreadsheet(sheet_id: str, sheet_name: str, dump_path: str) -> None:
    """
    Load spreadsheet values based on sheet_id & sheet_name
    then dump it to a path as .pkl files

    Parameters
    ----------
    sheet_id : str
        The spreadsheet ID

    sheet_name : str
        The sheet name

    dump_path : str
        The dumped .pkl file

    Returns
    -------
    None
    """
    # Load the credentials
    google_credentials = load_credentials()

    # Open a spreadsheet ID
    spreadsheet = google_credentials.open_by_key(sheet_id)

    # Open a specific sheet
    sheet = spreadsheet.worksheet(sheet_name)

    # Get all the values
    values = sheet.get_all_values()

    # Dump the data
    pickle_dump(values, dump_path)

def pickle_load(file_path: str) -> any:
    """
    Load a pickle file
    
    Parameters
    ----------
    file_path : str
        The file path

    Returns
    --------
    values : any
        The values of loaded .pkl file
    """
    try:
        # Load the file
        values = joblib.load(file_path)
        
        # Log
        print(f'Successfully load the data from {file_path}')
        
        return values
    except Exception as error:
        print(error)

def pickle_dump(data: any, file_path: str) -> None:
    """
    Dump data files to a path
    """
    try:
        # Dump
        joblib.dump(data, file_path)
        
        # Log
        print(f'Successfully dump the data to {file_path}')
    
    except Exception as error:
        print(error)

def is_file_exists(file_path: str) -> bool:
    """
    Check whether a file exists in file_path

    Parameters
    ----------
    file_path : str
        The file path you want to check
    """
    return os.path.isfile(file_path)

