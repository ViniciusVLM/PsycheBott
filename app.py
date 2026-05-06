import os
import markdown
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

app = Flask(__name__)

# Configuração do Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def enviar_email(destinatario, conteudo_html):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = "Seu Parecer Profissional - PsycheBot 🤖"
    mensagem.attach(MIMEText(conteudo_html, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, mensagem.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    analise_html = None
    
    if request.method == 'POST':
        # Capturando os dados (Certifique-se que o 'name' no HTML seja igual a estes)
        p1 = request.form.get('p1', '')
        p2 = request.form.get('p2', '')
        q1 = request.form.get('q1', 'N/A')
        q2 = request.form.get('q2', 'N/A')
        q3 = request.form.get('q3', 'N/A')
        trajetoria = request.form.get('trajetoria', '')
        email_usuario = request.form.get('email') # Ajustado para bater com o HTML

        # Melhorando o Prompt para focar em profissionais de TI e prevenção de Burnout
        prompt = f"""
        Atue como um psicólogo organizacional especializado em saúde mental de profissionais de tecnologia e prevenção de Burnout.
        Analise as seguintes respostas de um profissional da área tech em relação ao seu ambiente de trabalho e estresse:
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
        """

        try:
            # Modelo atualizado (gemini-2.5-flash - mais recente e com cota separada)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            # Converte a resposta da IA para HTML para exibir no site
            analise_html = markdown.markdown(response.text)
            
            if email_usuario:
                enviar_email(email_usuario, analise_html)
        except Exception as e:
            analise_html = f"<p style='color:red;'>Erro ao processar análise: {e}</p>"

    # 'resultado' é a variável que o HTML vai procurar
    return render_template('index.html', resultado=analise_html)

if __name__ == '__main__':
    app.run(debug=True)