# PsycheBot — Orientação de Carreira com IA

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Uma plataforma de IA que transforma respostas sobre comportamento profissional em feedback construtivo e personalizado para jovens trabalhadores.**

[ Acessar o PsycheBot](https://psychebot.onrender.com) · [ Reportar Bug](https://github.com/ViniciusVLM/PsycheBot/issues) · [ Sugerir Feature](https://github.com/ViniciusVLM/PsycheBot/issues)

</div>

---

## Sobre o Projeto

O **PsycheBot** é uma aplicação web criada para apoiar o desenvolvimento profissional de jovens trabalhadores. Através de um formulário interativo, a plataforma coleta percepções sobre comportamento e desafios no ambiente de trabalho, e utiliza a **API do Google Gemini** para gerar um parecer personalizado com foco em soft skills, pontos de melhoria e orientação de carreira.

O projeto também conta com uma **landing page completa** sobre saúde mental na tecnologia, trazendo estatísticas, estratégias baseadas em evidências e recursos de apoio emocional.

> Criado originalmente para a gincana do **Dia do Jovem Trabalhador no CIEE**.

---

## Demo

<div align="center">

| Landing Page | Formulário de Análise |
|---|---|
| Navegação, vídeo hero, estatísticas e recursos | Perguntas comportamentais + resposta da IA |

**[https://psychebot.onrender.com](https://psychebot.onrender.com)**

</div>

---

## Funcionalidades

- **Análise comportamental com IA** — respostas geradas pelo Google Gemini com tom acolhedor e profissional
- **Landing page informativa** — estatísticas sobre saúde mental na tecnologia com base em pesquisas científicas
- **Formulário inteligente** — perguntas abertas e de múltipla escolha sobre reação a erros, críticas e trabalho em equipe
- **Segurança** — sanitização de HTML, sem exposição de erros internos, variáveis de ambiente para dados sensíveis
- **Responsivo** — adaptado para desktop e mobile
- **Recursos de emergência** — links para CVV, CFP e Setembro Amarelo

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Back-end | Python 3.12 + Flask 3.0 |
| IA Generativa | Google Gemini API (`google-genai`) |
| Servidor WSGI | Gunicorn |
| Front-end | HTML5, CSS3 (Glassmorphism + Dark Theme) |
| Tipografia | Roboto Slab, Inter, Noto Sans |
| Deploy | Render (Free Tier) |
| Segurança | `bleach` (sanitização HTML), `python-dotenv` |

---

## Estrutura do Projeto

```
PsycheBot/
│
├── app.py # Aplicação Flask principal
├── requirements.txt # Dependências do projeto
├── Procfile # Comando de inicialização (Render/Heroku)
├── .env.example # Exemplo de variáveis de ambiente
│
├── templates/
│ └── index.html # Landing page + formulário de análise
│
└── static/
├── style.css # Estilos da landing page
└── index.css # Estilos complementares
```

---

## Como Rodar Localmente

### Pré-requisitos
- Python 3.12+
- Chave de API do Google Gemini ([obter aqui](https://aistudio.google.com/))

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/ViniciusVLM/PsycheBot.git
cd PsycheBot

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env e insira sua GEMINI_API_KEY

# 5. Rode a aplicação
python app.py
```

Acesse em: `http://localhost:5000`

---

## Deploy no Render

1. Faça fork ou conecte este repositório no [Render](https://render.com)
2. Crie um **Web Service** apontando para o repositório
3. Configure as variáveis de ambiente:

| Variável | Valor |
|---|---|
| `GEMINI_API_KEY` | Sua chave da API do Google |
| `GEMINI_MODEL` | `gemini-2.0-flash` |
| `FLASK_DEBUG` | `false` |

4. O Render detecta o `Procfile` automaticamente e faz o deploy 

> O plano gratuito do Render "dorme" após 15 min de inatividade. Abra a URL antes do evento para garantir que o serviço esteja ativo.

---

## Segurança

- Chaves de API carregadas via variáveis de ambiente (nunca no código)
- HTML das respostas da IA sanitizado com `bleach` antes de ser renderizado
- Erros internos logados no servidor, sem exposição ao usuário
- Modo debug desativado em produção

---

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commitar suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. Fazer push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

---

## Autor

**Vinicius Lourenço Martins**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vinicius-lourenço-martins-722287381)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ViniciusVLM)

---

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

<div align="center">
Feito com e por Vinicius Lourenço
</div>
