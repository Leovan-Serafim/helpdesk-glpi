"""
Orquestrador da Fase 4.
Integra histórico, recorrência, correlação e decisão.
"""

from analytics.incident_history import get_incident_history
from analytics.recurrence_detector import detect_recurrence
from analytics.correlation_engine import correlate_incident
from analytics.action_suggester import suggest_action


class InsightEngine:
    """
    Orquestrador da Fase 4.
    Retorna um objeto de decisão único para consumo da Fase 5.
    """

    def __init__(self):
        pass

    def run(self, ticket_id: int | None = None) -> dict:
        """
        Executa o pipeline analítico completo.
        O ticket_id fica preparado para uso futuro (API / Web / WhatsApp).
        """

        insights = []

        # Histórico consolidado
        history = get_incident_history()

        # Detecção de recorrência
        incidents = detect_recurrence(history)

        for incident in incidents:
            # Correlação operacional
            correlation = correlate_incident(incident)

            # Decisão explicável
            decision = suggest_action(correlation)

            insights.append({
                "incidente": incident,
                "correlacao": correlation,
                "decisao": decision
            })

        # Consolidação para a Fase 5
        final_decision = {
            "status": decision.get("status"),
            "priority": decision.get("priority"),
            "escalate": decision.get("escalate"),
            "insights": [
                f"Incidente recorrente detectado: {i['incidente']}"
                for i in insights
            ],
            "suggested_actions": decision.get("actions", [])
        }

        return final_decision
