import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Buffet Pro Manager", layout="wide")

# Simulação de Banco de Dados (Em um app real, use SQL ou Google Sheets)
if 'estoque' not in st.session_state:
    st.session_state.estoque = pd.DataFrame([
        {"Item": "Café Gourmet", "Categoria": "Café", "Local": "Câmara 1", "Espaço": "Estante A", "Qtd": 50, "Min": 10},
        {"Item": "Filé Mignon", "Categoria": "Almoço", "Local": "Freezer 2", "Espaço": "Gaveta 3", "Qtd": 20, "Min": 5},
        {"Item": "Vinho Tinto", "Categoria": "Coquetelaria", "Local": "Câmara 2", "Espaço": "Estante C", "Qtd": 12, "Min": 6},
        {"Item": "Forno Elétrico", "Categoria": "Equipamento", "Local": "Depósito", "Espaço": "Prateleira 1", "Info": "220V/Industrial", "Status": "Disponível"}
    ])

# --- NAVEGAÇÃO ---
menu = st.sidebar.selectbox("Acesso", ["Cliente (Propostas)", "Funcionário (Estoque & Equipas)"])

# --- INTERFACE DO CLIENTE ---
if menu == "Cliente (Propostas)":
    st.header("🍴 Solicitar Proposta de Serviço")
    servico = st.selectbox("Escolha o Serviço", ["Café da Manhã", "Coffee Break", "Almoço", "Janta", "Coquetelaria"])
    
    # Lógica de verificação automática
    disponivel = st.session_state.estoque[st.session_state.estoque['Categoria'] == servico]
    
    if not disponivel.empty:
        st.success(f"Temos disponibilidade para o serviço de {servico}!")
        st.table(disponivel[['Item', 'Qtd']])
        if st.button("Reservar Data e Itens"):
            st.info("Reserva enviada! O estoque foi pré-bloqueado para os funcionários.")
    else:
        st.error("Insumos insuficientes para este serviço no momento.")

# --- INTERFACE DO FUNCIONÁRIO ---
else:
    st.header("🛠️ Gestão Operacional")
    tabs = st.tabs(["Câmaras (Estantes)", "Freezers (Gavetas)", "Equipamentos", "Entrada/Saída"])

    with tabs[0]:
        st.subheader("📦 Itens em Câmaras")
        camaras = st.session_state.estoque[st.session_state.estoque['Local'].str.contains("Câmara")]
        st.dataframe(camaras)

    with tabs[1]:
        st.subheader("❄️ Itens em Freezers")
        freezers = st.session_state.estoque[st.session_state.estoque['Local'].str.contains("Freezer")]
        st.dataframe(freezers)

    with tabs[2]:
        st.subheader("⚡ Equipamentos Eletrônicos")
        equip = st.session_state.estoque[st.session_state.estoque['Categoria'] == "Equipamento"]
        st.table(equip)

    with tabs[3]:
        st.subheader("🔄 Controle de Movimentação")
        col1, col2 = st.columns(2)
        with col1:
            item_mov = st.selectbox("Selecionar Item", st.session_state.estoque['Item'])
            tipo_mov = st.radio("Ação", ["Entrada (Compra)", "Saída (Uso/Evento)"])
        with col2:
            qtd_mov = st.number_input("Quantidade", min_value=1)
            if st.button("Confirmar Atualização"):
                # Lógica simplificada de atualização de estoque
                idx = st.session_state.estoque.index[st.session_state.estoque['Item'] == item_mov][0]
                if tipo_mov == "Saída (Uso/Evento)":
                    st.session_state.estoque.at[idx, 'Qtd'] -= qtd_mov
                else:
                    st.session_state.estoque.at[idx, 'Qtd'] += qtd_mov
                st.rerun()

# --- ALERTAS DE COMPRA ---
st.sidebar.divider()
st.sidebar.subheader("🚨 Alertas de Reposição")
necessita_compra = st.session_state.estoque[
    (st.session_state.estoque['Qtd'] <= st.session_state.estoque['Min']) & 
    (st.session_state.estoque['Categoria'] != "Equipamento")
]
if not necessita_compra.empty:
    for item in necessita_compra['Item']:
        st.sidebar.warning(f"Comprar urgente: {item}")
else:
    st.sidebar.success("Estoque em dia!")
