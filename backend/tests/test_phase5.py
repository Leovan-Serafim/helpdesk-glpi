from analytics.insight_engine import InsightEngine
from attendance.responder import IAResponder


def test_phase5_full_flow():
    """
    Teste integrado das Fases 1 → 5
    Valida se o sistema gera uma resposta humana coerente.
    """

    engine = InsightEngine()
    decision = engine.run(ticket_id=1)

    responder = IAResponder()
    response = responder.respond(decision)

    print("\n--- RESPOSTA GERADA PELA IA ---\n")
    print(response)

    assert isinstance(response, str)
    assert len(response) > 50
