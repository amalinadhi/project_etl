"""For logging helper"""

from datetime import datetime


def timestamp() -> datetime:
    # Return current date and time
    return datetime.now()

def print_debug(message: str) -> None:
    # print the debug message
    print(timestamp(), message)
