# backend/main.py

import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from analytics.insight_engine import InsightEngine
from attendance.llm_client import LLMClient
from db_connection import get_db_connection

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
    """
    Endpoint principal para perguntas do usuário.
    Recebe {"question": "sua pergunta"}
    """
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

    # Fase 4: Análise completa do histórico de chamados
    decision_object = insight_engine.run()

    # Prompt rico e profissional enviado ao Mistral
    prompt = f"""
Você é uma IA de atendimento técnico integrada ao GLPI.

REGRAS OBRIGATÓRIAS:
- Responda com UMA ÚNICA resposta.
- Seja direto, humano e objetivo.
- NÃO invente dados.
- NÃO infira prioridade, recorrência, impacto ou urgência sem campos explícitos.
- Use APENAS as informações presentes nos dados.
- Se não for possível responder com os dados disponíveis, diga claramente que não é possível determinar.
- Para perguntas quantitativas, calcule com precisão.
- Não explique raciocínio interno.
- Não sugira ações sem base nos dados.

### DADOS ATUAIS DO HELPDESK (fonte única da verdade):
{json.dumps(decision_object, ensure_ascii=False, default=str)}

### PERGUNTA DO USUÁRIO:
{question}

INSTRUÇÕES DE RESPOSTA:
- Use no máximo 2 frases.
- Linguagem natural, sem listas ou bullets.
- Responda apenas o que foi perguntado.
"""

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
            "decisao": decision_object  # útil para debug futuro
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
