# backend/intelligence/decision_classifier.py

from enum import Enum


class DecisionType(str, Enum):
    ATENDIMENTO = "ATENDIMENTO"
    ATIVO = "ATIVO"
    PROJETO = "PROJETO"
    GESTAO = "GESTAO"


def classify_question(question: str) -> DecisionType:
    """
    Classificação determinística e conservadora.
    Não usa LLM.
    """

    q = question.lower()

    if any(k in q for k in ["chamado", "ticket", "recorrente", "sla", "tempo", "resolvido"]):
        return DecisionType.ATENDIMENTO

    if any(k in q for k in ["máquina", "equipamento", "ativo", "computador", "notebook"]):
        return DecisionType.ATIVO

    if any(k in q for k in ["projeto", "padronização", "substituição", "melhoria"]):
        return DecisionType.PROJETO

    if any(k in q for k in ["indicador", "métrica", "tendência", "gargalo", "gestão"]):
        return DecisionType.GESTAO

    # fallback seguro
    return DecisionType.ATENDIMENTO
