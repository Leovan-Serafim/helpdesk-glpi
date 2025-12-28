# tests/test_phase3.py

from intelligence.normalizer import normalize_status
from intelligence.classifier import classify_priority
from intelligence.rules import should_escalate

def test_full_flow():
    # Simula dado vindo do banco (Fase 1)
    raw_ticket = {
        "status": "Em andamento",
        "impact": 5,
        "urgency": 4
    }

    # Normalização (Fase 2 + 3)
    status = normalize_status(raw_ticket["status"])
    priority = classify_priority(raw_ticket["impact"], raw_ticket["urgency"])

    ticket = {
        "status": status,
        "priority": priority
    }

    # Regra de negócio (Fase 3)
    escalate = should_escalate(ticket)

    print("Status:", status)
    print("Priority:", priority)
    print("Escalar:", escalate)

# Executar o teste
test_full_flow()
