#"""
#Identificação de recorrência de incidentes.
#"""
#
#def detect_recurrence(history, threshold=3):
#    recorrencias = []
#
#    for row in history:
#        categoria, prioridade, total, primeiro, ultimo = row
#
#        recorrencias.append({
#            "categoria": categoria,
#            "prioridade": prioridade,
#            "recorrente": total >= threshold,
#            "ocorrencias": total,
#            "primeiro": primeiro,
#            "ultimo": ultimo
#        })
#
#    return recorrencias


# backend/analytics/recurrence_detector.py
"""
Identificação de recorrência de incidentes com base no histórico bruto de chamados.
"""

from collections import defaultdict
from typing import List, Dict, Any

def detect_recurrence(history: List[Dict[str, Any]], threshold: int = 2) -> List[Dict[str, Any]]:
    """
    Detecta problemas recorrentes agrupando por categoria (e opcionalmente por problema).
    
    Args:
        history: Lista de chamados do banco (cada um com chaves como 'categoria', 'data_abertura', etc.)
        threshold: Mínimo de ocorrências para considerar recorrente (padrão: 2)
    
    Returns:
        Lista ordenada de recorrências (mais frequentes primeiro)
    """
    if not history:
        return []

    # Agrupamos por categoria (mais estável) e coletamos datas de abertura
    agrupado = defaultdict(list)

    for chamado in history:
        categoria = chamado.get('categoria', 'Sem categoria').strip() or 'Sem categoria'
        data = chamado.get('data_abertura', 'Desconhecida')

        chave = categoria  # Pode mudar para (categoria, problema) se quiser mais granularidade
        agrupado[chave].append(data)

    # Monta lista de recorrências
    recorrencias = []
    for categoria, datas in agrupado.items():
        total = len(datas)
        if total < threshold:
            continue

        # Ordena datas para pegar primeira e última (assumindo formato YYYY-MM-DD ou similar)
        datas_ordenadas = sorted(datas, key=lambda x: x or '0000-00-00')
        primeiro = datas_ordenadas[0]
        ultimo = datas_ordenadas[-1]

        recorrencias.append({
            "categoria": categoria,
            "recorrente": True,
            "ocorrencias": total,
            "primeiro_incidente": primeiro,
            "ultimo_incidente": ultimo
        })

    # Ordena por número de ocorrências (maior primeiro)
    recorrencias.sort(key=lambda x: x['ocorrencias'], reverse=True)

    return recorrencias