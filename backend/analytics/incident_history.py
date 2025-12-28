"""
Responsável por fornecer histórico de incidentes
já NORMALIZADOS (Fase 3).
"""

from intelligence.normalizer import normalize_status
from extraction.glpi_reader import read_glpi_data
from db_connection import get_db_connection

#def get_incident_history():
#    """
#    Retorna histórico de incidentes normalizados,
#    desacoplando a Fase 4 do schema físico do banco.
#    """
#
#    raw_tickets = read_glpi_data()
#
#    normalized = []
#    for ticket in raw_tickets:
#       normalized.append(normalize_status(ticket))
#
#    return normalized

def get_incident_history():
    """
    Carrega o histórico de incidentes (chamados) do banco GLPI mock.
    """
    conn = get_db_connection()
    try:
        data = read_glpi_data(conn)
        chamados = data.get("chamados", [])
        print(f"[INFO] {len(chamados)} chamados carregados do banco.")
        return chamados
    except Exception as e:
        print(f"[ERRO] Falha ao ler dados do GLPI: {e}")
        return []  # Retorna vazio em caso de erro
    finally:
        conn.close()
