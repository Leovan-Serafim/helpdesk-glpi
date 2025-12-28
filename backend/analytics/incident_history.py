"""
Responsável por fornecer histórico de incidentes
já NORMALIZADOS (Fase 3).
"""

from intelligence.normalizer import normalize_ticket
from extraction.glpi_reader import read_tickets_from_db


def get_incident_history():
    """
    Retorna histórico de incidentes normalizados,
    desacoplando a Fase 4 do schema físico do banco.
    """

    raw_tickets = read_tickets_from_db()

    normalized = []
    for ticket in raw_tickets:
        normalized.append(normalize_ticket(ticket))

    return normalized
