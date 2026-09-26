import logging
import os

import bleach
import markdown
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from google import genai

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY não encontrada.")

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

ALLOWED_TAGS = ["p","strong","em","ul","ol","li","h1","h2","h3","h4","br","blockquote","code","pre"]
MAX_CHARS = 2000

def _limitar(texto: str) -> str:
    return texto.strip()[:MAX_CHARS]

@app.route("/", methods=["GET", "POST"])
def index():
    analise_html = None
    if request.method == "POST":
        p1         = _limitar(request.form.get("p1", ""))
        p2         = _limitar(request.form.get("p2", ""))
        q1         = request.form.get("q1", "N/A")
        q2         = request.form.get("q2", "N/A")
        q3         = request.form.get("q3", "N/A")
        trajetoria = _limitar(request.form.get("trajetoria", ""))
        prompt = (
            "Você é um orientador de carreira gerando feedback construtivo "
            "para um jovem trabalhador. Responda em Markdown simples, sem "
            "tags HTML, com um tom acolhedor e profissional.\n\n"
            f"Como lida com pressão/prazos: {p1}\n"
            f"O que valoriza em trabalho em equipe: {p2}\n"
            f"Reação a erros: {q1}\n"
            f"Reação a críticas: {q2}\n"
            f"Autopercepção de qualidades: {q3}\n"
            f"Trajetória descrita: {trajetoria}"
        )
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            html_bruto   = markdown.markdown(response.text)
            analise_html = bleach.clean(html_bruto, tags=ALLOWED_TAGS, strip=True)
        except Exception:
            logger.exception("Falha ao gerar análise com a IA")
            analise_html = "<p>Não foi possível gerar sua análise agora. Tente novamente.</p>"
    return render_template("index.html", resultado=analise_html)

@app.route("/subscribe", methods=["POST"])
def subscribe():
    return redirect("/")


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)