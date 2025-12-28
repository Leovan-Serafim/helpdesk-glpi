from analytics.insight_engine2 import generate_insights


def test_phase4():
    insights = generate_insights()

    assert isinstance(insights, list)

    if insights:
        sample = insights[0]

        assert "incidente" in sample
        assert "correlacao" in sample
        assert "decisao" in sample

        assert "classe_decisao" in sample["decisao"]
        assert "acoes_sugeridas" in sample["decisao"]

    print("Fase 4 OK — Correlação e Decisão operacional compatíveis")
