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

