import streamlit as st
from agente import inicializar_contexto, interpretar_pergunta_nlp, executar_consulta

# Configuração da página
st.set_page_config(
    page_title="Desafio: Agente Industrial Inteligente",
    layout="centered"
)

# Inicializa contexto e histórico
if "contexto" not in st.session_state:
    st.session_state.contexto = inicializar_contexto()

if "historico" not in st.session_state:
    st.session_state["historico"] = []

# Título e instrução
st.markdown(
    """
    # Desafio: Agente Industrial Inteligente
    """
)

# Espaço para o histórico do chat
with st.container():
    for pergunta, resposta in st.session_state["historico"]:
        st.markdown(f"<div style='margin-top:10px;'><b>Você:</b> {pergunta}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#2E86C1;'><b>SiderTech:</b> {resposta}</div>", unsafe_allow_html=True)

# Campo de entrada com botão de envio
with st.form("pergunta_form", clear_on_submit=True):
    pergunta = st.text_input("Digite sua pergunta:", placeholder="Ex: Qual técnico trabalhou na ordem 32?")
    enviar = st.form_submit_button("Enviar")

# Processamento ao enviar
if enviar and pergunta:
    sql = interpretar_pergunta_nlp(pergunta, st.session_state.contexto)
    resposta = executar_consulta(sql, st.session_state.contexto)
    st.session_state["historico"].append((pergunta, resposta))
    st.rerun()
