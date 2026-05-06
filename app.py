import os
import markdown
from flask import Flask, render_template, request, make_response
import google.generativeai as genai
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

app = Flask(__name__)

# Configuração do Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def enviar_email(destinatario, conteudo_html):
    """Envia e-mail com o parecer."""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")

    if not remetente or not senha:
        print("Erro: EMAIL_REMETENTE ou EMAIL_SENHA não configurados.")
        return False

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = "Seu Parecer Profissional - PsycheBot 🤖"
    mensagem.attach(MIMEText(conteudo_html, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, mensagem.as_string())
        server.quit()
        print(f"E-mail enviado com sucesso para {destinatario}")
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    analise_html = None
    email_para_enviar = None

    if request.method == 'POST':
        try:
            # Capturando os dados do formulário
            p1 = request.form.get('p1', '')
            p2 = request.form.get('p2', '')
            q1 = request.form.get('q1', 'N/A')
            q2 = request.form.get('q2', 'N/A')
            q3 = request.form.get('q3', 'N/A')
            trajetoria = request.form.get('trajetoria', '')
            email_para_enviar = request.form.get('email', '')

            # Verifica se a API key está configurada
            if not api_key:
                analise_html = "<p style='color:red;'>Erro: GEMINI_API_KEY não está configurada no servidor.</p>"
                return render_template('index.html', resultado=analise_html)

            # Prompt focado em profissionais de TI e prevenção de Burnout
            prompt = f"""
            Atue como um psicólogo organizacional especializado em saúde mental de profissionais de tecnologia e prevenção de Burnout.
            Analise as seguintes respostas de um profissional da área tech:
            - Lida com pressão e prazos: {p1}
            - Visão sobre trabalho em equipe: {p2}
            - Reação ao erro: {q1}
            - Reação à crítica: {q2}
            - Autoavaliação de qualidades: {q3}
            - Trajetória descrita e pontos de melhoria: {trajetoria}
            
            Gere um parecer profissional, empático e acolhedor, formatado em tópicos. O parecer deve conter:
            1. **Perfil Comportamental:** Uma análise do perfil do profissional com base nas respostas.
            2. **Pontos Fortes:** Qualidades identificadas que ajudam o profissional no dia a dia.
            3. **Sinais de Alerta:** Pontos nas respostas que podem indicar risco de Burnout, exaustão emocional ou síndrome do impostor (caso existam).
            4. **Sugestões Práticas de Autocuidado:** Conselhos e estratégias focadas na área de tecnologia (limites, pausas, comunicação) para proteger a saúde mental.
            
            Seja conciso e direto, com no máximo 500 palavras no total.
            """

            # Chamada à API do Gemini (modelo leve e rápido)
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            response = model.generate_content(prompt)

            # Extrai o texto da resposta de forma segura
            texto_resposta = ""
            try:
                texto_resposta = response.text
            except (ValueError, AttributeError):
                try:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text') and part.text:
                            texto_resposta += part.text
                except Exception:
                    texto_resposta = ""

            if texto_resposta:
                analise_html = markdown.markdown(texto_resposta)
            else:
                analise_html = "<p style='color:orange;'>A IA não conseguiu gerar uma resposta. Tente novamente.</p>"

        except Exception as e:
            print(f"Erro no processamento: {e}")
            analise_html = f"<p style='color:red;'>Erro ao processar análise: {e}</p>"

    # Renderiza a página PRIMEIRO, depois envia o e-mail via call_on_close
    resp = make_response(render_template('index.html', resultado=analise_html))

    if email_para_enviar and analise_html:
        conteudo = analise_html
        destino = email_para_enviar
        @resp.call_on_close
        def _enviar():
            enviar_email(destino, conteudo)

    return resp

if __name__ == '__main__':
    app.run(debug=True)