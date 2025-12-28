"""
action_suggester.py

Responsabilidade:
Transformar os INSIGHTS gerados pela Fase 4 (Correlação & Insights)
em uma CLASSE DE DECISÃO operacional, acompanhada de:
- justificativas claras
- nível de confiança
- ações sugeridas (não executadas)

Este módulo NÃO:
- detecta recorrência
- classifica prioridade
- analisa causa raiz
- decide SLA

Ele apenas traduz análise → decisão.
"""

from typing import Dict, List


# ============================================================
# 1. CLASSES DE DECISÃO (estáveis e universais)
# ============================================================

DECISION_CLASSES = [
    "MITIGACAO_IMEDIATA",
    "CORRECAO_DEFINITIVA",
    "ESCALONAMENTO",
    "CONTENCAO_DE_RISCO",
    "ORIENTACAO_USUARIO",
    "OBSERVACAO_MONITORADA",
    "SUBSTITUICAO_ATIVO"
]


# ============================================================
# 2. MAPEAMENTO DE AÇÕES POR CLASSE DE DECISÃO
# (Política operacional – pode variar por cliente)
# ============================================================

DECISION_ACTION_MAP = {
    "MITIGACAO_IMEDIATA": [
        "reiniciar_servico",
        "liberar_acesso_temporario",
        "aplicar_workaround"
    ],
    "CORRECAO_DEFINITIVA": [
        "aplicar_patch",
        "atualizar_driver",
        "reinstalacao_controlada"
    ],
    "ESCALONAMENTO": [
        "escalar_para_infra",
        "abrir_incidente_maior"
    ],
    "CONTENCAO_DE_RISCO": [
        "isolar_maquina",
        "comunicar_gestao",
        "bloquear_acesso_preventivo"
    ],
    "ORIENTACAO_USUARIO": [
        "orientar_usuario",
        "documentar_boas_praticas"
    ],
    "OBSERVACAO_MONITORADA": [
        "manter_monitoramento",
        "reavaliar_em_24h"
    ],
    "SUBSTITUICAO_ATIVO": [
        "trocar_equipamento",
        "providenciar_backup_dados"
    ]
}


# ============================================================
# 3. AVALIAÇÃO DAS CLASSES DE DECISÃO
# ============================================================

def score_decision_classes(correlation: Dict) -> Dict[str, int]:
    """
    Avalia o contexto analisado na Fase 4 e atribui
    pontuação para cada classe de decisão.

    Quanto maior o score, mais adequada é a classe.
    """

    scores = {cls: 0 for cls in DECISION_CLASSES}

    # Impacto alto exige reação imediata
    if correlation.get("impacto") == "ALTO":
        scores["MITIGACAO_IMEDIATA"] += 2
        scores["CONTENCAO_DE_RISCO"] += 1

    # Problema recorrente sem sucesso paliativo
    if correlation.get("recorrente") and not correlation.get("sucesso_paliativo", True):
        scores["CORRECAO_DEFINITIVA"] += 3

    # Risco operacional crítico não deve ficar só no HelpDesk
    if correlation.get("risco_operacional") == "CRITICO":
        scores["ESCALONAMENTO"] += 3
        scores["CONTENCAO_DE_RISCO"] += 2

    # Muitas tentativas paliativas indicam decisão errada anterior
    if correlation.get("acoes_paliativas_aplicadas", 0) >= 3:
        scores["CORRECAO_DEFINITIVA"] += 2

    # Baixo impacto e não recorrente → observar
    if (
        correlation.get("impacto") == "BAIXO"
        and not correlation.get("recorrente")
    ):
        scores["OBSERVACAO_MONITORADA"] += 2

    # Indício de falha física ou degradação contínua
    if correlation.get("suspeita_falha_hardware"):
        scores["SUBSTITUICAO_ATIVO"] += 3

    return scores


# ============================================================
# 4. SELEÇÃO DA CLASSE DE DECISÃO PRINCIPAL
# ============================================================

def select_primary_decision(scores: Dict[str, int]) -> str:
    """
    Seleciona a classe de decisão com maior score.
    Em caso de empate, a primeira maior é escolhida.
    """

    return max(scores, key=scores.get)


# ============================================================
# 5. GERAÇÃO DE JUSTIFICATIVAS HUMANAMENTE EXPLICÁVEIS
# ============================================================

def build_justifications(correlation: Dict, decision_class: str) -> List[str]:
    """
    Constrói justificativas claras e auditáveis,
    baseadas no contexto analisado.
    """

    justifications = []

    if correlation.get("recorrente"):
        justifications.append("Chamado recorrente identificado")

    if correlation.get("impacto") == "ALTO":
        justifications.append("Impacto operacional alto")

    if not correlation.get("sucesso_paliativo", True):
        justifications.append("Ações paliativas anteriores sem sucesso")

    if correlation.get("risco_operacional") == "CRITICO":
        justifications.append("Risco crítico ao ambiente")

    if correlation.get("padrao_identificado"):
        justifications.append(
            f"Padrão identificado: {correlation['padrao_identificado']}"
        )

    if decision_class == "OBSERVACAO_MONITORADA":
        justifications.append("Cenário estável, sem indícios de agravamento")

    return justifications


# ============================================================
# 6. FUNÇÃO PRINCIPAL (INTERFACE DO MÓDULO)
# ============================================================

def suggest_action(correlation_result: Dict) -> Dict:
    """
    Função principal consumida pelos outros módulos.

    Entrada:
    - correlation_result (output da Fase 4)

    Saída:
    - decisão estruturada e explicável
    """

    scores = score_decision_classes(correlation_result)
    decision_class = select_primary_decision(scores)

    response = {
        "classe_decisao": decision_class,
        "confianca": correlation_result.get("confianca_analise", 0.75),
        "justificativas": build_justifications(
            correlation_result, decision_class
        ),
        "acoes_sugeridas": DECISION_ACTION_MAP.get(decision_class, [])
    }

    return response
