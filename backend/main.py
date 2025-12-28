from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from analytics.insight_engine import InsightEngine
from attendance.llm_client import LLMClient

app = FastAPI()

# Static e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Engines
insight_engine = InsightEngine()
llm = LLMClient()


class Pergunta(BaseModel):
    pergunta: str


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/ask")
def ask(pergunta: Pergunta):
    """
    Endpoint único para Web / WhatsApp / API futura
    """

    # Fase 4 — decisão consolidada
    decision_object = insight_engine.run()

    # Fase 5 — linguagem natural
    resposta = llm.generate_response(
        pergunta=pergunta.pergunta,
        decision=decision_object
    )

    return JSONResponse({
        "resposta": resposta,
        "decisao": decision_object
    })
