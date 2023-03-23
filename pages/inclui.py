def run():
    import streamlit as st
    import pymysql
    from sshtunnel import SSHTunnelForwarder
    from datetime import datetime, time

    def conecta_ssh():
        try:
            server = SSHTunnelForwarder(
                    '172.24.173.15',
                    ssh_username='root',
                    ssh_password='ditec_8905',
                    remote_bind_address=('127.0.0.1', 3306),
                    server.start()
                    )
        except:
            pass
        return ok

    def conecta_bd():
        try:
            db = pymysql.connect(
                host="localhost",
                user="root",
                password="Ditec_8905",
                database="dan"
            )
            cursor = db.cursor(pymysql.cursors.DictCursor)
        except:
            pass
        return ok

    def fecha_bd():
        db.close()
        return ok

    def desconecta_ssh():
        server.stop()
        return ok

    
    # Página web com o formulário para inclusão dos dados
    st.write('# Inclusão de dados')

    str_hi = '00:05'
    str_hf = '23:45'
    hora_inicio_padrao = time.fromisoformat(str_hi)
    hora_fim_padrao = time.fromisoformat(str_hf)

    # Recebe os dados do formulário
    causa_banco = st.selectbox('Causa Banco:', [False, True])
    operadora = st.selectbox('Operadora:', ['0', '1', '2'])
    predio = st.selectbox('Prédio:', ['CTA01', 'CTA03', 'CTA05', 'CTA06', 'CTA09'])
    data_inicio = st.date_input('Data de início:')
    hora_inicio = st.time_input('Hora de início:', value=hora_inicio_padrao)
    data_fim = st.date_input('Data de fim:')
    hora_fim = st.time_input('Hora de fim:', value=hora_fim_padrao)
    justificativa = st.text_area('Justificativa:')
    funci = st.text_input('Funcionário:', max_chars=8)

    # Concatena data_inicio e hora_inicio
    inicio = datetime.combine(data_inicio, hora_inicio)

    # Concatena data_fim e hora_fim
    fim = datetime.combine(data_fim, hora_fim)

    # Botão de confirmação para gravar os dados
    if st.button('Gravar'):
            # Insere os dados na tabela
            log_gravado = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conecta_ssh()
            conecta_bd()
            cursor.execute("""
                INSERT INTO manut_prog (causa_banco, operadora, predio, inicio, fim, justificativa, funci, log_gravado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (causa_banco, operadora, predio, inicio, fim, justificativa, funci, log_gravado))
            db.commit()
            fecha_bd()
            desconecta_ssh()

            # Mostra mensagem de sucesso
            st.success('Incluido com sucesso')
