# intelligence/normalizer.py

def normalize_status(status_raw):
    """
    Recebe um status bruto vindo do banco
    e retorna um status padronizado.
    """

    # Se o status vier vazio ou nulo
    if not status_raw:
        return "DESCONHECIDO"

    # Converte tudo para minúsculo para evitar erro de comparação
    status = status_raw.strip().lower()

    # Mapeamento de possíveis variações para um padrão único
    status_map = {
        "novo": "NOVO",
        "aberto": "ABERTO",
        "em andamento": "EM_ANDAMENTO",
        "andamento": "EM_ANDAMENTO",
        "fechado": "FECHADO",
        "resolvido": "FECHADO"
    }

    # Retorna o status padronizado ou DESCONHECIDO se não existir
    return status_map.get(status, "DESCONHECIDO")
