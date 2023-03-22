import streamlit as st
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder

def conecta_ssh():
    try:
        server = SSHTunnelForwarder(
            '172.24.173.15',
            ssh_username='root',
            ssh_password='ditec_8905',
            remote_bind_address=('127.0.0.1', 3306)
        )
        server.start()
        return server
    except Exception as e:
        st.error(f"Não foi possível conectar via SSH: {e}")
        return None

def conecta_bd(server):
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="Ditec_8905",
            database="dan",
            port=server.local_bind_port
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    except Exception as e:
        st.error(f"Não foi possível conectar ao banco de dados: {e}")
        return None, None

def fecha_bd(db):
    try:
        db.close()
    except Exception as e:
        st.warning(f"Erro ao fechar conexão com o banco de dados: {e}")

def desconecta_ssh(server):
    try:
        server.stop()
    except Exception as e:
        st.warning(f"Erro ao desconectar do servidor SSH: {e}")

def run():
    st.title("Exclusão")

    with st.spinner("Conectando ao servidor SSH..."):
        server = conecta_ssh()

    if server:
        with st.spinner("Conectando ao banco de dados..."):
            db, cursor = conecta_bd(server)

        if cursor:
            # Query para selecionar todos os dados da tabela manut_prog
            query = "SELECT * FROM manut_prog ORDER BY log_gravado DESC"

            with st.spinner("Consultando dados..."):
                # Executa a query e armazena o resultado em um DataFrame pandas
                df = pd.read_sql(query, db)

            # Exibe o DataFrame pandas na tela usando o Streamlit
            st.dataframe(df)

            # Adiciona um componente Selectbox para permitir ao usuário selecionar qual linha deseja excluir
            row_to_delete = st.selectbox("Selecione a linha que deseja excluir:", options=df.index.tolist())

            # Adiciona um botão para executar a exclusão da linha selecionada
            if st.button("Excluir linha"):
                # Executa a exclusão da linha selecionada
                id_to_delete = df.loc[row_to_delete]['id']
                delete_query = f"DELETE FROM manut_prog WHERE id = {id_to_delete}"
                cursor.execute(delete_query)
                db.commit()

                # Exibe uma mensagem informando que a linha foi excluída
                st.success(f"Linha {row_to_delete} excluída com sucesso!")

        fecha_bd(db)
        desconecta_ssh(server)

if __name__ == "__main__":
    run()
