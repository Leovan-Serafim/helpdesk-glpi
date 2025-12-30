DECISION_RULES = {
    "RECORRENCIA_CATEGORIA": {
        "allowed_fields": [
            "categoria",
            "ocorrencias",
            "primeiro_incidente",
            "ultimo_incidente"
        ]
    },

    "GARGALO_ATENDIMENTO": {
        "allowed_fields": [
            "categoria",
            "ocorrencias",
            "tempo_atendimento"
        ]
    },

    "ANALISE_EQUIPAMENTO": {
        "allowed_fields": [
            "equipamento",
            "categoria",
            "problema",
            "status_atual"
        ]
    },

    "ANALISE_GERAL": {
        "allowed_fields": []  # fallback controlado
    },

     
    "IMPACTO_OPERACIONAL": {
        "strategy": "max_impact",
        "allowed_fields": ["categoria", "ocorrencias"]
    },

    "RECORRENCIA_CATEGORIA": {
        "strategy": "list",
        "allowed_fields": ["categoria", "ocorrencias"]
    },

    "ANALISE_EQUIPAMENTO": {
        "strategy": "timeline",
        "allowed_fields": ["problema", "data_abertura"]
    },

    "ANALISE_GERAL": {
        "strategy": "summary",
        "allowed_fields": []
    }
}



