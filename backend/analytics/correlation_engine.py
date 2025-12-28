# backend/analytics/correlation_engine.py
"""
Motor de correlação operacional.

Recebe um chamado individual + lista de recorrências detectadas
e gera um contexto analítico rico para o Ollama (action_suggester).
"""

from typing import List, Dict, Any, Optional

def correlate_incident(
    incident: Dict[str, Any],
    recorrencias: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Gera o objeto de correlação analítica para um incidente específico.
    
    Args:
        incident: Chamado bruto do banco (com 'categoria', 'problema', 'status', etc.)
        recorrencias: Lista de recorrências detectadas por detect_recurrence()
    
    Returns:
        Dicionário com indicadores analíticos para o Ollama
    """
    categoria = incident.get('categoria', 'Desconhecida').strip()
    
    # Verifica se esta categoria é recorrente
    recorrente_info = next(
        (r for r in recorrencias if r['categoria'] == categoria),
        None
    )
    
    is_recorrente = recorrente_info is not None
    ocorrencias = recorrente_info['ocorrencias'] if is_recorrente else 1
    primeiro_incidente = recorrente_info.get('primeiro_incidente') if is_recorrente else incident.get('data_abertura')
    ultimo_incidente = recorrente_info.get('ultimo_incidente') if is_recorrente else incident.get('data_abertura')

    # Heurísticas de impacto (sem coluna prioridade)
    problema = incident.get('problema', '').lower()
    palavras_alto_impacto = ['rede', 'internet', 'servidor', 'sistema', 'erp', 'produção', 'banco de dados', 'falha total', 'indisponível']
    impacto = "ALTO" if any(palavra in problema or palavra in categoria.lower() for palavra in palavras_alto_impacto) else "MÉDIO"

    status = incident.get('status', '').lower()
    risco_operacional = "CRITICO" if impacto == "ALTO" and status in ['aberto', 'em andamento'] else "MODERADO"

    correlation = {
        # Indicadores principais
        "recorrente": is_recorrente,
        "impacto": impacto,
        "ocorrencias": ocorrencias,

        # Indicadores operacionais
        "risco_operacional": risco_operacional,

        # Indicadores históricos
        "acoes_paliativas_aplicadas": max(ocorrencias - 1, 0),
        "primeiro_incidente": primeiro_incidente,
        "ultimo_incidente": ultimo_incidente,

        # Heurísticas
        "sucesso_paliativo": not is_recorrente,
        "suspeita_falha_hardware": ocorrencias >= 4 and 'equipamento' in problema,
        "suspeita_configuracao": ocorrencias >= 3 and any(p in problema for p in ['configuração', 'atualização', 'versão', 'software']),

        # Padrão identificado
        "padrao_identificado": (
            f"Recorrência detectada na categoria '{categoria}' com {ocorrencias} ocorrências desde {primeiro_incidente}"
            if is_recorrente else None
        ),

        # Metadados do incidente atual
        "categoria": categoria,
        "problema_resumo": incident.get('problema', '')[:150],
        "status_atual": incident.get('status', 'Desconhecido'),

        # Confiança da análise
        "confianca_analise": 0.90 if is_recorrente else 0.70
    }

    return correlation