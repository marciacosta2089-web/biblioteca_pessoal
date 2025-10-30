# 🗂️ a_desenvolver.md
## 📚 Biblioteca Pessoal – Márcia Costa

---

### 🧠 Estado Atual do Projeto  
- ✅ **Backend (FastAPI)** hospedado no **Render**  
  - URL: https://biblioteca-pessoal-o87r.onrender.com  
  - Endpoints principais disponíveis em `/docs`  
- ✅ **Frontend (Streamlit)** hospedado no **Streamlit Cloud**  
  - URL: https://bibliotecapeappal-pvqtqhsfrffbzq2jiyvtzy.streamlit.app/  
- ✅ Comunicação via variável segura (`st.secrets`)  
- ✅ Deploy full-stack concluído com sucesso  
- ✅ README completo e atualizado  

---

### 💡 Ideias para a Fase 2  

1. **Autenticação / Login**
   - Contas pessoais (Google ou simples password)
   - Cada utilizador vê apenas os seus livros  

2. **Histórico e Notas**
   - Campo de “comentários pessoais” por livro  
   - Data de leitura / progresso  

3. **Capas de livros**
   - Upload de imagem (capa real do livro)  
   - Exibição em miniaturas no frontend  

4. **Exportações**
   - Exportar para PDF e JSON  
   - Partilhar listas com amigos  

5. **Base de Dados Persistente**
   - Migrar de SQLite → PostgreSQL (Render free tier)  

6. **Interface**
   - Modo escuro / claro  
   - Layout responsivo (tabs em vez de colunas no modo móvel)  

---

### 🧾 A Fazer (quando quiseres retomar)
- Confirmar o domínio exato da app Streamlit e atualizar no Render:
  ```
  CORS_ORIGINS=https://bibliotecapeappal-pvqtqhsfrffbzq2jiyvtzy.streamlit.app
  ```
- Confirmar o `API_BASE_URL` no Streamlit Secrets:
  ```
  API_BASE_URL="https://biblioteca-pessoal-o87r.onrender.com"
  ```

---

### 💬 Notas Pessoais
> “Projeto criado do zero com FastAPI + Streamlit.  
> Hospedado online, integrado e funcional.  
> Próximos passos: autenticação, personalização e exportação.”  

---

### 🧩 Referências Importantes
- Repositório GitHub: https://github.com/marciacosta2089-web/biblioteca_pessoal  
- Render Dashboard: https://dashboard.render.com/  
- Streamlit Cloud: https://share.streamlit.io  
