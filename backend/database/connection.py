import sqlite3
DB_PATH = "mock_glpi.db"

def get_connection():
    return sqlite3.connect(DB_PATH)