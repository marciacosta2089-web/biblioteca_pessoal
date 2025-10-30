# frontend_app.py
import os
import requests
import streamlit as st

API = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Biblioteca Pessoal", layout="wide")
st.title("📚 Biblioteca Pessoal")

# --- Estatísticas rápidas ---
try:
    todos = requests.get(f"{API}/livros", timeout=10).json()
    total = len(todos)
    total_meus = len([x for x in todos if x["lista"] == "meus"])
    total_comprar = len([x for x in todos if x["lista"] == "comprar"])
    medias = [x["classificacao"] for x in todos] or [0]
    media = round(sum(medias) / len(medias), 2)
    st.caption(f"📊 Total: {total} | Meus: {total_meus} | Comprar: {total_comprar} | Média de classificação: {media}")
except Exception:
    st.caption("📊 Estatísticas indisponíveis no momento.")

# --- Exportar CSV ---
exp_col1, exp_col2 = st.columns([1, 9])
with exp_col1:
    if st.button("⬇️ Exportar CSV"):
        try:
            r = requests.get(f"{API}/livros/export.csv", timeout=15)
            if r.ok:
                st.download_button("Descarregar livros.csv", r.content, "livros.csv", "text/csv")
            else:
                st.error(f"Falha ao exportar CSV: {r.text}")
        except Exception as e:
            st.error(f"Falha ao exportar CSV: {e}")

st.divider()

# --- Formulário de criação ---
with st.form("novo_livro", clear_on_submit=True):
    st.subheader("Adicionar livro")
    nome = st.text_input("Nome (título)", "")
    autor = st.text_input("Autor", "")
    classificacao = st.number_input("Classificação (1–10)", min_value=1, max_value=10, step=1, value=7)
    recomendado_por = st.text_input("Recomendado por", "")
    lista = st.selectbox("Lista", ["meus", "comprar"], index=1)
    submitted = st.form_submit_button("Adicionar")
    if submitted:
        if not nome.strip() or not autor.strip():
            st.error("Nome e Autor são obrigatórios.")
        else:
            payload = {
                "nome": nome.strip(),
                "autor": autor.strip(),
                "classificacao": int(classificacao),
                "recomendado_por": recomendado_por.strip() or None,
                "lista": lista,
            }
            try:
                r = requests.post(f"{API}/livros", json=payload, timeout=10)
                if r.ok:
                    st.success("Livro adicionado!")
                    st.rerun()
                else:
                    st.error(f"Erro ao adicionar: {r.text}")
            except Exception as e:
                st.error(f"Erro ao adicionar: {e}")

# --- Barra de filtros ---
with st.expander("🔎 Filtros"):
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        filtro_autor = st.text_input("Autor contém", "")
    with f_col2:
        filtro_min = st.number_input("Classificação mínima", 1, 10, 1)
    with f_col3:
        filtro_lista = st.selectbox("Lista", ["todas", "meus", "comprar"], index=0)

def carregar_lista(tipo: str | None = None):
    try:
        params = {"lista": tipo} if tipo else None
        r = requests.get(f"{API}/livros", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Falha ao carregar lista: {e}")
        return []

def aplicar_filtros(dados: list):
    res = []
    for d in dados:
        if filtro_lista != "todas" and d["lista"] != filtro_lista:
            continue
        if filtro_autor and filtro_autor.lower() not in d["autor"].lower():
            continue
        if d["classificacao"] < int(filtro_min):
            continue
        res.append(d)
    return res

def desenhar_tabela(titulo: str, dados: list):
    st.subheader(titulo)
    if not dados:
        st.info("Sem livros aqui ainda.")
        return
    for item in dados:
        with st.container(border=True):
            st.markdown(f"**{item['nome']}** — {item['autor']}")
            st.caption(
                f"Classificação: {item['classificacao']} | "
                f"Recomendado por: {item.get('recomendado_por') or '—'} | "
                f"Lista: {item['lista']} | id: {item['id']}"
            )

            # --- Editor inline ---
            with st.expander("✏️ Editar"):
                novo_nome = st.text_input("Nome", value=item["nome"], key=f"nome_{item['id']}")
                novo_autor = st.text_input("Autor", value=item["autor"], key=f"autor_{item['id']}")
                nova_class = st.number_input("Classificação (1–10)", 1, 10, value=int(item["classificacao"]), key=f"class_{item['id']}")
                novo_rec = st.text_input("Recomendado por", value=item.get("recomendado_por") or "", key=f"rec_{item['id']}")
                if st.button("Guardar alterações", key=f"save_{item['id']}"):
                    payload = {
                        "nome": novo_nome.strip(),
                        "autor": novo_autor.strip(),
                        "classificacao": int(nova_class),
                        "recomendado_por": (novo_rec.strip() or None),
                    }
                    try:
                        resp = requests.put(f"{API}/livros/{item['id']}", json=payload, timeout=10)
                        if resp.ok:
                            st.success("Alterações guardadas.")
                            st.rerun()
                        else:
                            st.error(f"Falha ao editar: {resp.text}")
                    except Exception as e:
                        st.error(f"Falha ao editar: {e}")

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Mover para 'meus'", key=f"mv_meus_{item['id']}"):
                    try:
                        resp = requests.post(f"{API}/livros/{item['id']}/mover", params={"destino": "meus"}, timeout=10)
                        if resp.ok:
                            st.rerun()
                        else:
                            st.error(f"Falha ao mover: {resp.text}")
                    except Exception as e:
                        st.error(f"Falha ao mover: {e}")
            with c2:
                if st.button("Mover para 'comprar'", key=f"mv_comprar_{item['id']}"):
                    try:
                        resp = requests.post(f"{API}/livros/{item['id']}/mover", params={"destino": "comprar"}, timeout=10)
                        if resp.ok:
                            st.rerun()
                        else:
                            st.error(f"Falha ao mover: {resp.text}")
                    except Exception as e:
                        st.error(f"Falha ao mover: {e}")
            with c3:
                if st.button("Apagar", key=f"del_{item['id']}"):
                    try:
                        resp = requests.delete(f"{API}/livros/{item['id']}", timeout=10)
                        if resp.ok:
                            st.rerun()
                        else:
                            st.error(f"Falha ao apagar: {resp.text}")
                    except Exception as e:
                        st.error(f"Falha ao apagar: {e}")

# --- Renderização das duas listas (com filtros aplicados) ---
col1, col2 = st.columns(2)
with col1:
    meus = carregar_lista("meus")
    desenhar_tabela("📗 Meus Livros", aplicar_filtros(meus))

with col2:
    comprar = carregar_lista("comprar")
    desenhar_tabela("🛒 Livros para Comprar", aplicar_filtros(comprar))
