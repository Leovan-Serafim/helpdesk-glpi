"""
Motor de correlação operacional.

Transforma dados históricos em um CONTEXTO ANALÍTICO
consumido pelo action_suggester.
"""

def correlate_incident(incident):
    """
    Gera o objeto de correlação esperado pelo action_suggester.
    """

    correlation = {
        # Indicadores principais
        "recorrente": incident["recorrente"],
        "impacto": "ALTO" if incident["prioridade"] == "CRITICA" else "BAIXO",

        # Indicadores operacionais
        "risco_operacional": (
            "CRITICO" if incident["prioridade"] == "CRITICA" else "MODERADO"
        ),

        # Indicadores históricos
        "acoes_paliativas_aplicadas": (
            incident["ocorrencias"] - 1 if incident["recorrente"] else 0
        ),

        # Suposições analíticas (heurísticas)
        "sucesso_paliativo": not incident["recorrente"],
        "suspeita_falha_hardware": incident["ocorrencias"] >= 5,

        # Padrão identificado
        "padrao_identificado": (
            f"Recorrência na categoria {incident['categoria']}"
            if incident["recorrente"] else None
        ),

        # Confiança da análise
        "confianca_analise": 0.85 if incident["recorrente"] else 0.65
    }

    return correlation
