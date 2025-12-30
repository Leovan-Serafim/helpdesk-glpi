# backend/intelligence/prompt_builder.py

import json


def build_prompt(
    question: str,
    chamados_abertos: list,
    total_abertos: int,
    decision_object: dict,
    decision_knowledge: str | None = None,
    decision_type: str | None = None,
    decision_pattern: str | None = None

) -> str:
    """
    Constrói o prompt completo enviado ao LLM.
    Nesta etapa, o conteúdo é idêntico ao prompt original do main.py.
    """
    decisions_block = (
        f"\nDECISÕES E POLÍTICAS DO SISTEMA:\n{decision_knowledge}\n"
        if decision_knowledge else ""
    )

    decision_type_block = (
        f"\nTIPO DE DECISÃO IDENTIFICADO: {decision_type}\n"
        if decision_type else ""
    )

    decision_pattern_block = (
        f"\nPADRÃO DE DECISÃO IDENTIFICADO: {decision_pattern}\n"
        if decision_pattern else ""
    )

    prompt = f"""
Você se chama Roberval e é uma IA de atendimento técnico integrada ao sistema GLPI Inovit.

REGRAS OBRIGATÓRIAS:
- Use APENAS os dados fornecidos abaixo.
- NÃO invente informações ou números.
- Para perguntas sobre quantidade ou lista de chamados em aberto, use EXATAMENTE os dados da seção "CHAMADOS EM ABERTO ATUALIZADOS".
- Responda em português.
- Use no máximo 3 frases.
- Seja direto, profissional e humano.

ATENÇÃO:
Use exclusivamente os dados fornecidos no bloco ANALISE_ESTRUTURADA.
Não faça inferências externas.
Não cite categorias, impactos ou causas não presentes.


CHAMADOS EM ABERTO ATUALIZADOS (fonte da verdade - atualizado agora):
Total em aberto: {total_abertos}
Lista completa:
{json.dumps(chamados_abertos, ensure_ascii=False, indent=2)}

ANÁLISE DE RECORRÊNCIA E INSIGHTS (do motor analítico):
{json.dumps(decision_object, ensure_ascii=False)}

{decisions_block}

{decision_type_block}

{decision_pattern_block}


PERGUNTA DO USUÁRIO:
{question}

RESPOSTA:
"""
   
    return prompt
