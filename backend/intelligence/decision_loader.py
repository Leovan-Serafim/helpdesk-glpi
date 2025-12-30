# backend/intelligence/decision_loader.py

from pathlib import Path


DECISIONS_PATH = Path(__file__).resolve().parents[1] / "knowledge" / "Decisions.md"


def load_decisions() -> str | None:
    """
    Carrega o conteúdo do Decisions.md de forma segura.
    Retorna None se o arquivo não existir ou ocorrer erro.
    """
    try:
        if not DECISIONS_PATH.exists():
            return None

        return DECISIONS_PATH.read_text(encoding="utf-8")

    except Exception:
        return None
