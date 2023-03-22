import streamlit as st
# st.set_page_config(layout = "wide")
from pages import inclui
from pages import exclui

# cria o menu e exibe as páginas de acordo com a seleção
itens = ["Selecione","Incluir","Excluir"]
escolha = st.sidebar.selectbox("Selecione uma página", itens)

if escolha == "Selecione":
    st.write('Pagina inicial')
elif escolha == "Incluir":
    inclui.run()
elif escolha == "Excluir":
    exclui.run()