# backend/analytics/insight_engine.py

from analytics.incident_history import get_incident_history
from analytics.recurrence_detector import detect_recurrence
from analytics.correlation_engine import correlate_incident
from analytics.action_suggester import suggest_action
from intelligence.decision_rules import DECISION_RULES


class InsightEngine:
    """
    Orquestrador principal da análise inteligente.
    """

    def resolve_strategy(self, recorrencias, strategy):
        if not recorrencias:
            return None

        if strategy == "max_impact":
            return max(recorrencias, key=lambda x: x.get("ocorrencias", 0))

        if strategy == "list":
            return recorrencias

        return None

    def run(self, decision_type: str | None = None) -> dict:
        """
        Executa o pipeline analítico completo com estratégia por pattern.
        """
        history = get_incident_history()
        if not history:
            return {"error": "Nenhum chamado encontrado no histórico."}

        recorrencias = detect_recurrence(history)

        rules = DECISION_RULES.get(decision_type, {})
        strategy = rules.get("strategy")

        resultado = self.resolve_strategy(recorrencias, strategy)

        chamado_foco = max(
            history,
            key=lambda x: x.get("data_abertura") or "1900-01-01"
        )

        correlation = correlate_incident(chamado_foco, recorrencias)
        decision = suggest_action(correlation)

        insights_list = []

        correlacao_analitica = {}

        # DECISÃO REAL AQUI
        if strategy == "max_impact" and resultado:
            correlacao_analitica = {
                "categoria": resultado["categoria"],
                "ocorrencias": resultado["ocorrencias"],
                "impacto": "ALTO"
            }

            insights_list.append(
                f"O principal ponto de impacto do atendimento está na categoria "
                f"'{resultado['categoria']}', com {resultado['ocorrencias']} ocorrências."
            )

        elif strategy == "list" and isinstance(resultado, list):
            correlacao_analitica = resultado
            insights_list.append(
                f"Foram identificados {len(resultado)} padrões recorrentes no atendimento."
            )

        else:
            correlacao_analitica = correlation

        insights_list.append(
            f"Chamado atual (ID {chamado_foco.get('id')}): "
            f"categoria '{chamado_foco.get('categoria')}', "
            f"problema: '{chamado_foco.get('problema', '')[:80]}...'"
        )

        final_decision = {
            "status": decision.get("status", "ANÁLISE CONCLUÍDA"),
            "priority": "ALTA" if correlacao_analitica.get("impacto") == "ALTO" else "MÉDIA",
            "escalate": False,
            "decision_type": decision_type,
            "insights": insights_list,
            "suggested_actions": decision.get("actions", []),
            "correlacao_analitica": correlacao_analitica,
            "chamado_analisado": {
                "id": chamado_foco.get("id"),
                "categoria": chamado_foco.get("categoria"),
                "problema": chamado_foco.get("problema"),
                "data_abertura": chamado_foco.get("data_abertura")
            }
        }

        return final_decision
