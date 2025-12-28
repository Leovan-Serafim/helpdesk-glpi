from extraction.db_connection import get_connection
from extraction.glpi_reader import read_glpi_data
from extraction.validators import validate_tickets, validate_users

DB_PATH = "mock_glpi.db"

def run():
    print("Iniciando Fase 2 — Extração de Dados do GLPI")

    # 1. Conecta ao banco criado na Fase 1
    connection = get_connection(DB_PATH)

    # 2. Lê os dados brutos
    glpi_data = read_glpi_data(connection)

    # 3. Executa validações básicas
    ticket_issues = validate_tickets(glpi_data.get("tickets", []))
    user_issues = validate_users(glpi_data.get("users", []))

    # 4. Exibe resumo
    print("\n Resumo da Extração")
    for table, rows in glpi_data.items():
        print(f" - {table}: {len(rows)} registros")

    # 5. Exibe problemas encontrados
    print("\n Inconsistências encontradas:")
    for issue in ticket_issues + user_issues:
        print(" -", issue)

    # 6. Fecha conexão
    connection.close()

    print("\n Fase 2 concluída com sucesso")


if __name__ == "__main__":
    run()
