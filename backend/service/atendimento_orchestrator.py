from service.intent_classifier import classificar_intencao
from service.query_router import gerar_consulta
from service.response_builder import gerar_resposta

def atender(pergunta: str, dados_db: str) -> str:
    intencao = classificar_intencao(pergunta)
    consulta = gerar_consulta(intencao)

    # execução da consulta acontece fora da LLM
    resultado = dados_db  # simulação

    resposta = gerar_resposta(pergunta, resultado)
    return resposta
