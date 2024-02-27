"""Credentials from Google API"""

import os
import json
import gspread

from dotenv import load_dotenv


# Load the dotenv
load_dotenv()


def spreadsheet():
    # Load Google Spreadsheet API credential
    cred_dict = json.loads(os.getenv('SPREADSHEET_API'))
    return gspread.service_account_from_dict(cred_dict)

