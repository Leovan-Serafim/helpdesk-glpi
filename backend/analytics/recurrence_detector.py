"""
Identificação de recorrência de incidentes.
"""

def detect_recurrence(history, threshold=3):
    recorrencias = []

    for row in history:
        categoria, prioridade, total, primeiro, ultimo = row

        recorrencias.append({
            "categoria": categoria,
            "prioridade": prioridade,
            "recorrente": total >= threshold,
            "ocorrencias": total,
            "primeiro": primeiro,
            "ultimo": ultimo
        })

    return recorrencias
