# backend/main.py

import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from analytics.insight_engine2 import InsightEngine
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
    prompt = f"""
Você é uma IA de atendimento técnico integrada ao sistema GLPI Inovit.

REGRAS OBRIGATÓRIAS:
- Use APENAS os dados fornecidos abaixo.
- NÃO invente informações ou números.
- Para perguntas sobre quantidade ou lista de chamados em aberto, use EXATAMENTE os dados da seção "CHAMADOS EM ABERTO ATUALIZADOS".
- Responda em português.
- Use no máximo 3 frases.
- Seja direto, profissional e humano.

CHAMADOS EM ABERTO ATUALIZADOS (fonte da verdade - atualizado agora):
Total em aberto: {total_abertos}
Lista completa:
{json.dumps(chamados_abertos, ensure_ascii=False, indent=2)}

ANÁLISE DE RECORRÊNCIA E INSIGHTS (do motor analítico):
{json.dumps(decision_object, ensure_ascii=False)}

PERGUNTA DO USUÁRIO:
{question}

RESPOSTA:
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
