# 🧭 GUIA TÉCNICO – BIBLIOTECA PESSOAL

## 📚 Introdução
Este guia explica, de forma detalhada e pedagógica, todo o funcionamento do projeto **Biblioteca Pessoal** — tanto a parte técnica como o raciocínio por trás de cada ficheiro.

---

## 🧩 PARTE 1 – Estrutura Geral do Projeto

```
biblioteca_pessoal/
│
├── app/                ← BACKEND (FastAPI + Base de Dados)
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/livros.py
│
├── frontend_app.py     ← FRONTEND (Streamlit)
├── requirements.txt    ← Dependências
├── data/biblioteca.db  ← Base de dados SQLite
└── README.md
```

---

## ⚙️ PARTE 2 – Backend (API com FastAPI)

### 🔸 main.py
Ponto de entrada da API.

- Cria a aplicação FastAPI
- Define mensagem de boas-vindas (`/`)
- Liga as rotas dos livros (`app.include_router(livros.router)`)
- Ativa o CORS (permite que o frontend comunique com o backend)

```python
app = FastAPI(title="Biblioteca Pessoal API")
app.add_middleware(CORSMiddleware, ...)
```

**Middleware:** camada que intercepta pedidos HTTP — aqui serve para permitir que o Streamlit (que corre noutro domínio) fale com o backend.

---

### 🔸 database.py
Cria e gere a **ligação à base de dados** (SQLite).

```python
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

- `engine`: conecta ao ficheiro `.db`
- `SessionLocal`: cria uma “sessão” (canal de comunicação com a BD)
- `Base`: classe base de onde derivam os modelos
- `get_db()`: função geradora que fornece uma sessão e fecha-a no fim.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
O `yield` funciona como um “abre e fecha automático” — garante que a ligação à BD é libertada depois do uso.

---

### 🔸 models.py
Define o **modelo da tabela** (ORM com SQLAlchemy).

```python
class Livro(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    autor = Column(String)
    classificacao = Column(Integer)
    recomendado_por = Column(String)
    lista = Column(String)
```

Cada atributo → uma **coluna** na tabela `livros`.  
A classe `Livro` representa uma linha da tabela.

---

### 🔸 schemas.py
Define **estruturas de dados (schemas)** com Pydantic.  
Servem para:
- validar dados que vêm do frontend  
- controlar o formato das respostas da API

```python
class LivroBase(BaseModel):
    nome: str
    autor: str
    classificacao: int
    recomendado_por: str
    lista: str
```

Pydantic garante que, por exemplo, `classificacao` é sempre um número inteiro e não texto.

---

### 🔸 routes/livros.py
Contém todas as **rotas (endpoints)** da API.

Cada rota é um “serviço” que o frontend pode pedir:

```python
@router.post("/livros")
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
```

- `@router.post`: define um endpoint HTTP `POST /livros`
- `livro: LivroCreate`: validação automática do corpo do pedido
- `db: Session = Depends(get_db)`: injeta a sessão de BD

O bloco `try/except` captura erros:

```python
try:
    db.add(db_livro)
    db.commit()
except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=str(e))
```

`try` → tenta executar  
`except` → se falhar, desfaz (`rollback`) e devolve erro 500

Outras rotas:
- `GET /livros`: lista todos os livros
- `PUT /livros/{id}/mover/{destino}`: muda o livro de lista
- `DELETE /livros/{id}`: remove um livro

---

## 🎨 PARTE 3 – Frontend (Streamlit)

### 🔸 frontend_app.py
Interface visual do utilizador.

O Streamlit cria páginas interativas em Python:

```python
st.title("📚 Biblioteca Pessoal")
st.text_input("Nome do Livro")
st.number_input("Classificação", 1, 10)
st.button("Adicionar Livro")
```

### Comunicação com a API
O frontend usa `requests` para comunicar com o backend:

```python
API = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
resposta = requests.get(f"{API}/livros")
```

O URL vem da variável de ambiente (no Streamlit Cloud) para apontar para o Render.

Localmente → `127.0.0.1:8000`  
Online → `https://biblioteca-pessoal-o87r.onrender.com`

### Organização da página
- Mostra dois blocos (meus e comprar)
- Botões “Mover” e “Apagar” chamam `requests.put()` e `requests.delete()`
- Usa `st.rerun()` (ou `st.experimental_rerun()`) para atualizar após ação

---

## 🧠 PARTE 4 – Tecnologias Usadas

| Ferramenta | Função |
|-------------|---------|
| Python | Linguagem base |
| FastAPI | Framework para criar APIs |
| Uvicorn | Servidor da API |
| SQLAlchemy | ORM (traduz Python ↔ SQL) |
| Pydantic | Validação e serialização |
| Streamlit | Interface visual interativa |
| requests | Comunicação HTTP |
| SQLite | Base de dados leve |
| Render | Hospedagem da API |
| Streamlit Cloud | Hospedagem do frontend |

---

## 🔄 PARTE 5 – Fluxo do Projeto

```
[ Utilizador ]
     ↓
[ Streamlit UI ]
     ↓ (requests)
[ FastAPI Backend ]
     ↓ (SQLAlchemy)
[ SQLite Database ]
     ↑
 Resposta → devolve JSON → Streamlit mostra na tela
```

---

## 🔐 PARTE 6 – Segurança e Boas Práticas

- Usar variáveis de ambiente (`st.secrets`, `os.getenv`)  
- Usar CORS para permitir apenas domínios autorizados  
- Evitar colocar senhas ou caminhos absolutos no código  

---

## 🌟 PARTE 7 – Próximos Passos

1. Migrar BD para PostgreSQL (Render)
2. Adicionar autenticação (FastAPI Users)
3. Upload de imagem (capas de livros)
4. Exportação CSV / PDF
5. Melhorar design móvel (usar `st.tabs()`)

---

## 🧩 Conclusão
Criaste um **sistema completo full-stack**:  
- API profissional (FastAPI)  
- Base de dados automatizada (SQLite)  
- Interface gráfica intuitiva (Streamlit)  
- Deploy em Render + Streamlit Cloud  

Tudo modular, limpo e pronto a evoluir 💪
