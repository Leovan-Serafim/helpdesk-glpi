import requests
import time


class LLMClient:
    """
    Cliente centralizado para comunicação com LLM (Ollama).
    Responsável exclusivamente por:
    - Envio de prompts
    - Controle de timeout
    - Controle de retries
    """

    def __init__(
        self,
        model: str = "mistral",
        base_url: str = "http://localhost:11434/api/generate",
        timeout: int = 60,
        retries: int = 3
    ):
        self.model = model
        self.base_url = base_url
        self.timeout = timeout
        self.retries = retries

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        for attempt in range(self.retries):
            try:
                response = requests.post(
                    self.base_url,
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()

                return response.json().get("response", "").strip()

            except requests.RequestException as exc:
                if attempt < self.retries - 1:
                    time.sleep(2)
                else:
                    raise RuntimeError(
                        f"Erro ao comunicar com o LLM após {self.retries} tentativas"
                    ) from exc
