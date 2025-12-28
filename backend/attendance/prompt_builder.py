def build_prompt(decision: dict) -> str:
    """
    Constrói o prompt em linguagem natural a partir do objeto decisão.
    Nenhuma lógica de decisão ocorre aqui — apenas tradução técnica → humana.
    """

    status = decision.get("status", "DESCONHECIDO")
    priority = decision.get("priority", "NÃO DEFINIDA")
    escalate = decision.get("escalate", False)
    insights = decision.get("insights", [])
    actions = decision.get("suggested_actions", [])

    insights_text = "\n".join(f"- {item}" for item in insights) or "- Nenhuma análise relevante identificada"
    actions_text = "\n".join(f"- {item}" for item in actions) or "- Nenhuma ação imediata recomendada"

    prompt = f"""
Você é um atendente de suporte técnico experiente, profissional e objetivo.

Explique a situação do chamado abaixo em linguagem clara, acessível e humana.
Não utilize termos excessivamente técnicos.
Justifique as decisões tomadas e oriente o próximo passo de forma prática.

INFORMAÇÕES DO CHAMADO
Status: {status}
Prioridade: {priority}
Necessita escalonamento: {"Sim" if escalate else "Não"}

ANÁLISES IDENTIFICADAS
{insights_text}

AÇÕES RECOMENDADAS
{actions_text}

Explique:
1. O que está acontecendo
2. Por que essa decisão foi tomada
3. Qual é o próximo passo esperado
"""

    return prompt.strip()
