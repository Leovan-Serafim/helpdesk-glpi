# intelligence/classifier.py

def classify_priority(impact, urgency):
    """
    Classifica prioridade baseada em impacto e urgência.
    """

    # Garante que os valores não sejam nulos
    impact = impact or 0
    urgency = urgency or 0

    score = impact + urgency

    # Regras simples e claras (regra de negócio)
    if score >= 8:
        return "CRITICA"
    elif score >= 5:
        return "ALTA"
    elif score >= 3:
        return "MEDIA"
    else:
        return "BAIXA"

def classify_question(question: str) -> str:
    q = question.lower()

    impacto_terms = [
        "gargalo", "principal", "maior", "impacta",
        "crítico", "critico", "trava", "atraso",
        "pior", "mais problema"
    ]

    recorrencia_terms = [
        "recorrente", "frequente", "repetido",
        "quantos chamados", "quantidade"
    ]

    equipamento_terms = [
        "máquina", "equipamento", "computador",
        "notebook", "pc"
    ]

    if any(t in q for t in impacto_terms):
        return "IMPACTO_OPERACIONAL"

    if any(t in q for t in recorrencia_terms):
        return "RECORRENCIA_CATEGORIA"

    if any(t in q for t in equipamento_terms):
        return "ANALISE_EQUIPAMENTO"

    return "ANALISE_GERAL"
