# backend/intelligence/decision_patterns.py

from enum import Enum
from intelligence.decision_classifier import DecisionType


class DecisionPattern(str, Enum):
    RECORRENCIA_CATEGORIA = "RECORRENCIA_CATEGORIA"
    HISTORICO_ATIVO = "HISTORICO_ATIVO"
    PROBLEMA_CRONICO = "PROBLEMA_CRONICO"
    INDICADOR_GESTAO = "INDICADOR_GESTAO"
    DESCONHECIDO = "DESCONHECIDO"


def detect_pattern(question: str, decision_type: DecisionType) -> DecisionPattern:
    """
    Detecta padrões de decisão com base na pergunta e no tipo.
    Lógica conservadora e determinística.
    """

    q = question.lower()

    if decision_type == DecisionType.ATENDIMENTO:
        if any(k in q for k in ["recorrente", "frequente", "repete", "ocorrência"]):
            return DecisionPattern.RECORRENCIA_CATEGORIA

    if decision_type == DecisionType.ATIVO:
        if any(k in q for k in ["histórico", "ao longo", "este ano", "problemas"]):
            return DecisionPattern.HISTORICO_ATIVO

    if decision_type == DecisionType.PROJETO:
        if any(k in q for k in ["substituir", "trocar", "padronizar"]):
            return DecisionPattern.PROBLEMA_CRONICO

    if decision_type == DecisionType.GESTAO:
        if any(k in q for k in ["indicador", "métrica", "tendência", "gargalo"]):
            return DecisionPattern.INDICADOR_GESTAO

    return DecisionPattern.DESCONHECIDO
