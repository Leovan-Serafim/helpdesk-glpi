# backend/analytics/insight_engine.py
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
    Orquestrador principal da análise inteligente.
    """

    def __init__(self):
        pass

    def run(self, ticket_id: int | None = None) -> dict:
        """
        Executa o pipeline analítico completo.
        Retorna um objeto consolidado para a Fase 5 (Ollama).
        """
        # 1. Carrega histórico completo
        history = get_incident_history()
        if not history:
            return {"error": "Nenhum chamado encontrado no histórico."}

        # 2. Detecta padrões recorrentes (por categoria)
        recorrencias = detect_recurrence(history)

        # 3. Escolhe o foco da análise: o chamado mais recente
        chamado_foco = max(
            history,
            key=lambda x: x.get('data_abertura') or '1900-01-01'
        )

        # 4. Correlação: passa o chamado bruto + as recorrências detectadas
        correlation = correlate_incident(chamado_foco, recorrencias)

        # 5. Sugestão de ação baseada na correlação
        decision = suggest_action(correlation)

        # 6. Monta resumo de insights para o Ollama
        insights_list = []

        if recorrencias:
            insights_list.append(
                f"Detectados {len(recorrencias)} padrões recorrentes, "
                f"sendo o mais grave: '{recorrencias[0]['categoria']}' com {recorrencias[0]['ocorrencias']} ocorrências."
            )

        insights_list.append(
            f"Chamado atual (ID {chamado_foco.get('id')}): "
            f"categoria '{chamado_foco.get('categoria')}', "
            f"problema: '{chamado_foco.get('problema', '')[:80]}...'"
        )

        if correlation.get('recorrente'):
            insights_list.append("Este tipo de chamado é RECORRENTE e deve ser priorizado.")

        # 7. Decisão final consolidada
        final_decision = {
            "status": decision.get("status", "ANÁLISE CONCLUÍDA"),
            "priority": "ALTA" if correlation.get("impacto") == "ALTO" else "MÉDIA",
            "escalate": correlation.get("risco_operacional") == "CRITICO",
            "insights": insights_list,
            "suggested_actions": decision.get("actions", []),
            "correlacao_analitica": correlation,  # útil para debug ou expansão
            "chamado_analisado": {
                "id": chamado_foco.get('id'),
                "categoria": chamado_foco.get('categoria'),
                "problema": chamado_foco.get('problema'),
                "data_abertura": chamado_foco.get('data_abertura')
            }
        }

        return final_decision