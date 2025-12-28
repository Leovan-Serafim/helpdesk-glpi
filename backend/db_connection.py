# backend/db_connection.py

import sqlite3
from pathlib import Path

# Caminho correto: o banco está na mesma pasta do backend
DATABASE_PATH = Path(__file__).parent / "mock_glpi.db"

def get_db_connection():
    """
    Retorna uma conexão com o banco SQLite mock_glpi.db localizado na pasta backend.
    """
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Banco de dados não encontrado: {DATABASE_PATH}")

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas como dict (ex: row['titulo'])
    return conn