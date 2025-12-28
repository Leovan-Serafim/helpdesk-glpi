# extraction/glpi_reader.py

import sqlite3  # Ou import mysql.connector / psycopg2 se for MySQL/PostgreSQL
from typing import Dict, Any

def fetch_all(cursor, table_name: str) -> list[Dict[str, Any]]:
    """
    Busca todos os registros de uma tabela e retorna como lista de dicionários.
    """
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    columns = [description[0] for description in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return rows

def read_glpi_data(connection) -> Dict[str, list[Dict[str, Any]]]:
    """
    Lê as principais tabelas do banco GLPI (ou mock) e retorna um dicionário com os dados.
    Ideal para análise offline ou mock durante desenvolvimento.
    """
    cursor = connection.cursor()

    data = {}
    tables = [
        "clientes",
        "equipamentos",
        "usuarios",
        "chamados",    # <- Aqui estão os tickets/chamados
        "solucoes"
    ]

    for table in tables:
        try:
            data[table] = fetch_all(cursor, table)
            print(f"[SUCESSO] Tabela '{table}' carregada com {len(data[table])} registros.")
        except Exception as e:
            data[table] = []
            print(f"[AVISO] Erro ao ler tabela '{table}': {e}")

    cursor.close()
    return data

# Função auxiliar opcional: focada apenas nos chamados (tickets)
def get_incident_history(connection) -> list[Dict[str, Any]]:
    """
    Retorna apenas a lista de chamados (tickets) – útil para o insight_engine.
    """
    data = read_glpi_data(connection)
    return data.get("chamados", [])