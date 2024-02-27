import os
import gspread
import json

from dotenv import load_dotenv


# CONFIGURATION RELATED
def load_config():
    """Load the config file for Postgresql conn"""
    # Load config
    load_dotenv()

    # Create a connection string
    conn_str = os.getenv('DATABASE_URL')
    
    return conn_str

def load_credentials():
    """Load the google spreadsheet credentials"""
    # Load the credentials
    load_dotenv()
    credentials_json = json.loads(os.getenv('GOOGLE_API'))
    google_credentials = gspread.service_account_from_dict(credentials_json)

    return google_credentials
