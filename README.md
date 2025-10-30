# 📚 Biblioteca Pessoal

Uma aplicação full-stack para gerir os livros que possuo e os que pretendo comprar.  
Desenvolvida em **Python**, com **FastAPI** (backend) e **Streamlit** (frontend).  
Hospedada em **Render** e **Streamlit Cloud**.

---

## 🧩 Estrutura do Projeto

```
biblioteca_pessoal/
│
├── app/                     # Backend FastAPI
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       └── livros.py
│
├── data/                    # Base de dados local (SQLite)
│   └── livros.db
│
├── frontend_app.py          # Interface Streamlit
├── requirements.txt         # Dependências do projeto
├── .gitignore
└── README.md
```

---

## ⚙️ Instalação Local

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/marciacosta2089-web/biblioteca_pessoal.git
cd biblioteca_pessoal
```

### 2️⃣ Criar e ativar o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# .\venv\Scripts\activate  # Windows
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

---

## 🚀 Executar Localmente

### Backend (FastAPI)
```bash
uvicorn app.main:app --reload
```
> O backend ficará disponível em:  
> 👉 http://127.0.0.1:8000  
> 👉 Documentação automática: http://127.0.0.1:8000/docs

### Frontend (Streamlit)
Num segundo terminal:
```bash
streamlit run frontend_app.py
```
> O frontend abrirá em:  
> 👉 http://localhost:8501

---

## ☁️ Deploy

### 🌐 1. Backend no Render

1. Cria conta em [https://render.com](https://render.com)
2. Clica em **New + → Web Service**
3. Escolhe o repositório **biblioteca_pessoal**
4. Define:
   - **Runtime:** Python 3  
   - **Start command:**  
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Root directory:** `.`
5. Cria uma variável de ambiente:
   ```bash
   CORS_ORIGINS=https://<teu_frontend>.streamlit.app
   ```
6. Clica em **Deploy**  

> Após o deploy, o backend ficará acessível, por exemplo:  
> 🔗 https://biblioteca-pessoal-o87r.onrender.com

---

### 💻 2. Frontend no Streamlit Cloud

1. Cria conta em [https://share.streamlit.io](https://share.streamlit.io)
2. Clica em **New app**
3. Preenche:
   - **Repository:** `marciacosta2089-web/biblioteca_pessoal`
   - **Branch:** `main`
   - **Main file path:** `frontend_app.py`
4. Abre **Advanced settings → Secrets**  
   e adiciona:
   ```bash
   API_BASE_URL="https://biblioteca-pessoal-o87r.onrender.com"
   ```
5. Clica em **Deploy app 🚀**

> O frontend ficará disponível em:  
> 🔗https://bibliotecapeappal-pvqtqhsfrffbzq2jiyvtzy.streamlit.app/  

---

## 🧠 Tecnologias Utilizadas

| Componente | Tecnologia |
|-------------|-------------|
| Linguagem   | Python 3 |
| Backend     | FastAPI |
| ORM / DB    | SQLAlchemy + SQLite |
| Frontend    | Streamlit |
| Deploy      | Render (API) + Streamlit Cloud (UI) |

---

## 🧪 Testar API

Endpoints disponíveis em:
```
GET     /livros?lista=meus
GET     /livros?lista=comprar
POST    /livros
PUT     /livros/{id}/mover/{destino}
GET     /export.csv
```

> A documentação interativa está em:  
> 🔗 `https://biblioteca-pessoal-o87r.onrender.com/docs`

---

## 💾 Variáveis de Ambiente

| Serviço | Variável | Valor de exemplo |
|----------|-----------|------------------|
| Render | `CORS_ORIGINS` | `https://bibliotecapessoal-xxxxx.streamlit.app` |
| Streamlit | `API_BASE_URL` | `https://biblioteca-pessoal-o87r.onrender.com` |

---

## 💬 Créditos

Desenvolvido por **Márcia Costa**  
Com apoio técnico de **GPT-5 (OpenAI)** para estruturação do projeto e automação do deploy.  
