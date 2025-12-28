from attendance.llm_client import LLMClient
from attendance.prompt_builder import build_prompt


class IAResponder:
    """
    Orquestrador da Fase 5.
    Recebe o objeto decisão das Fases 1–4 e retorna uma resposta humana.
    """

    def __init__(self):
        self.llm_client = LLMClient()

    def respond(self, decision: dict) -> str:
        """
        Executa o fluxo completo:
        - Constrói prompt
        - Envia ao LLM
        - Retorna resposta pronta para WhatsApp ou Web
        """

        prompt = build_prompt(decision)
        response = self.llm_client.generate(prompt)

        return response
