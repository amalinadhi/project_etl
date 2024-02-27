import psycopg2

from src._config import load_config


# QUERY RELATED
def _fetch_results(cursor):
    """Fetch results from a cursor connection"""
    # Initialize
    results = []

    # Extract results
    for rows in cursor.fetchall():
        result = []
        for row in rows:
            result.append(row)

        results.append(result)

    return results if len(results)>1 else results[0]

def execute_command(command: str, fetch_results: bool = False) -> None:
    """
    Execute Postgresql commands
    
    Parameters
    ----------
    commands : str
        The command

    fetch_results : bool, default = False
        Mau fetch results atau tidak

    Returns
    -------
    results : list
        Results dari query ketika fetch_results = True
    """
    try:
        # Load config
        conn_str = load_config()

        # Execute the commands
        with psycopg2.connect(conn_str) as conn:
            with conn.cursor() as cur:
                # Execute the command
                cur.execute(command)

                # Fetch results
                if fetch_results:
                    results = _fetch_results(cursor = cur)

        if fetch_results:
            return results

    except (psycopg2.DatabaseError, Exception) as error:
        print('Query Error! -', error)

