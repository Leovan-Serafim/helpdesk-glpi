import sqlite3
from pathlib import Path

def get_connection(db_path: str):

    database = Path(db_path)

    if not database.exists():
        raise FileNotFoundError(f"Banco não encontrado: {db_path}")
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row

    return connection
    
