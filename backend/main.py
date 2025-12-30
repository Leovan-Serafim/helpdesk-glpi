# backend/main.py

import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from intelligence.prompt_builder import build_prompt
from analytics.insight_engine2 import InsightEngine
from attendance.llm_client import LLMClient
from db_connection import get_db_connection
from intelligence.decision_loader import load_decisions
from intelligence.decision_classifier import classify_question
from intelligence.decision_patterns import detect_pattern



app = FastAPI(
    title="Helpdesk GLPI com Inteligência Artificial (Ollama + Mistral)"
)

# Configuração de arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Instâncias das engines
insight_engine = InsightEngine()
llm = LLMClient(model="mistral")


@app.get("/")
def home(request: Request):
    """
    Página inicial com interface web simples e elegante.
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            {"error": "Requisição inválida: envie JSON válido."},
            status_code=400
        )

    question = data.get("question", "").strip()
    if not question:
        return JSONResponse(
            {"error": "A pergunta não pode estar vazia."},
            status_code=400
        )

    decision_knowledge = load_decisions()
    decision_type = classify_question(question)
    decision_pattern = detect_pattern(question, decision_type)


    # === NOVA PARTE: Consulta fresca dos chamados abertos ===
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, categoria, problema, status, data_abertura
            FROM chamados
            WHERE status = 'Aberto'
            ORDER BY data_abertura DESC
            """
        )
        chamados_abertos = [dict(row) for row in cursor.fetchall()]
        total_abertos = len(chamados_abertos)
    except Exception as e:
        chamados_abertos = []
        total_abertos = 0
        print(f"Erro ao ler chamados abertos: {e}")
    finally:
        conn.close()
    # ========================================================

    # Fase 4: Análise completa do histórico de chamados (mantém o que já existe)
    decision_object = insight_engine.run()

    import json
    print("DECISION_OBJECT:")
    print(json.dumps(decision_object, indent=2, ensure_ascii=False))

    # Prompt enriquecido com dados reais e atuais
    prompt = build_prompt(
    question=question,
    chamados_abertos=chamados_abertos,
    total_abertos=total_abertos,
    decision_object=decision_object,
    decision_knowledge=decision_knowledge,
    decision_type=decision_type.value,
    decision_pattern=decision_pattern.value
    )



    try:
        resposta = llm.generate(prompt)
    except Exception as e:
        resposta = (
            "Não foi possível gerar resposta no momento. "
            f"Erro técnico: {str(e)}. "
            "Verifique se o Ollama está rodando com 'ollama serve'."
        )

    return JSONResponse(
        {
            "resposta": resposta,
            "decisao": decision_object
        }
    )


@app.get("/chamados")
def listar_chamados(request: Request):
    """
    Página com tabela de todos os chamados do banco
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, categoria, problema, status, data_abertura
            FROM chamados
            ORDER BY data_abertura DESC
            """
        )
        chamados = [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        chamados = []
        print(f"Erro ao ler chamados: {e}")
    finally:
        conn.close()

    return templates.TemplateResponse(
        "chamados.html",
        {"request": request, "chamados": chamados}
    )
