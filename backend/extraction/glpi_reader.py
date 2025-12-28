def fetch_all(cursor, table_name: str):

    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    rows = [dict(row) for row in cursor.fetchall()]
    return rows

def read_glpi_data(connection):

    cursor = connection.cursor()

    data = {}
    tables = [
        "clientes",
        "equipamentos",
        "usuarios",
        "chamados",
        "solucoes"
        ]

    for table in tables:
        try:
            data[table] = fetch_all(cursor, table)
        except Exception as e:
            data[table] = []
            print(f"[AVISO] Erro ao ler tabela {table}: {e}")

    return data