# backend/main.py

import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from analytics.insight_engine import InsightEngine
from attendance.llm_client import LLMClient  # Seu cliente robusto e perfeito

app = FastAPI(title="Helpdesk GLPI com Inteligência Artificial (Ollama + Mistral)")

# Configuração de arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Instâncias das engines
insight_engine = InsightEngine()
llm = LLMClient(model="mistral")  # ← Usando o Mistral que você já baixou


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
Você é um analista de helpdesk altamente objetivo e conciso. Responda SEMPRE de forma curta, direta e factual.

Regras obrigatórias:
- Responda sempre de forma curta e objetiva.
- Use no máximo 3 frases.
- Não repita informações já implícitas na pergunta.
- Não explique o raciocínio interno.
- Só detalhe se o usuário pedir explicitamente.

### Análise automatizada atual do helpdesk:
{json.dumps(decision_object, indent=2, ensure_ascii=False, default=str)}

### Pergunta do usuário:
{question}

Responda em português, de forma clara, objetiva e estruturada usando bullet points.
Responda em português, apenas com informações essenciais.
Formato obrigatório:
- Frase 1: resposta direta.
- Frase 2: contexto mínimo (se necessário).
- Frase 3: ação recomendada (opcional).

Seja assertivo, evite rodeios e foque no que precisa ser feito agora.
"""

    try:
        # Chama o método correto do seu LLMClient
        resposta = llm.generate(prompt)
    except Exception as e:
        resposta = (
            "Não foi possível gerar resposta no momento.\n"
            f"Erro técnico: {str(e)}\n\n"
            "Dica: Verifique se o Ollama está rodando com 'ollama serve'"
        )

    # Retorno para o frontend
    return JSONResponse({
        "resposta": resposta,
        "decisao": decision_object  # opcional: útil para debug futuro
    })

from db_connection import get_db_connection

@app.get("/chamados")
def listar_chamados(request: Request):
    """
    Página com tabela de todos os chamados do banco
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, categoria, problema, status, data_abertura FROM chamados ORDER BY data_abertura DESC")
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