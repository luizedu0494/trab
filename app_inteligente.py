import streamlit as st
import requests
import io

# --- CONFIGURAÇÃO ---
# COLE AQUI A URL DE PRODUÇÃO DO SEU WEBHOOK N8N (DA FASE 2)
N8N_WEBHOOK_URL = "https://labcesmac.app.n8n.cloud/webhook/be555f04-b1d5-47af-b3d5-71dc45c44c8d" 
# --------------------

# Configuração da Página
st.set_page_config(layout="wide")
st.title("🤖 Automação de Compra de VR/VA")
st.markdown("Faça o upload de todas as bases de dados necessárias para o cálculo do mês.")

# 1. Criação dos File Uploaders
st.subheader("1. Upload das Bases de Dados")
st.warning("Todos os 6 arquivos são obrigatórios.")

col1, col2 = st.columns(2)

with col1:
    file_ativos = st.file_uploader("1. Base de Ativos (Excel)", type=["xlsx"])
    file_ferias = st.file_uploader("2. Base de Férias (Excel)", type=["xlsx"])
    file_desligados = st.file_uploader("3. Base de Desligados (Excel)", type=["xlsx"])

with col2:
    file_admitidos = st.file_uploader("4. Base Cadastral (Admitidos Mês) (Excel)", type=["xlsx"])
    file_sindicatos = st.file_uploader("5. Base Sindicato x Valor (Excel)", type=["xlsx"])
    file_feriados = st.file_uploader("6. Calendário de Feriados (Est/Mun) (Excel)", type=["xlsx"])

st.divider()

# 2. Botão de Processamento e Lógica de Trigger
st.subheader("2. Processar e Baixar")

if st.button("Executar Cálculo de Benefícios", type="primary"):
    
    # Validação: Verifica se todos os 6 arquivos foram enviados
    all_files = [file_ativos, file_ferias, file_desligados, file_admitidos, file_sindicatos, file_feriados]
    
    if not all(all_files):
        st.error("Erro: Todos os 6 arquivos são obrigatórios para o cálculo. Por favor, faça o upload de todos.")
    
    elif N8N_WEBHOOK_URL == "https://SEU_DOMINIO_N8N.com/webhook/ID_DO_WEBHOOK":
         st.error("ERRO DE CONFIGURAÇÃO: Você não atualizou a variável 'N8N_WEBHOOK_URL' no script 'app.py'!")
         
    else:
        # Se tudo estiver OK, executa a automação
        with st.spinner("Processando... Enviando arquivos ao n8n. O n8n está consolidando, aplicando regras e calculando. Isso pode levar um minuto..."):
            try:
                # 3. Preparar arquivos para envio (multipart/form-data)
                # Os nomes ('file_ativos', etc) DEVEM ser os mesmos que o script Python no n8n espera!
                files_to_send = {
                    'file_ativos': (file_ativos.name, file_ativos.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    'file_ferias': (file_ferias.name, file_ferias.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    'file_desligados': (file_desligados.name, file_desligados.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    'file_admitidos': (file_admitidos.name, file_admitidos.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    'file_sindicatos': (file_sindicatos.name, file_sindicatos.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    'file_feriados': (file_feriados.name, file_feriados.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                }

                # 4. Chamar o Webhook do n8n
                response = requests.post(N8N_WEBHOOK_URL, files=files_to_send, timeout=300) # Timeout de 5 minutos

                # 5. Tratamento da Resposta
                # Gera um erro se o n8n retornar status 4xx ou 5xx (ex: se o script Python falhar)
                response.raise_for_status() 

                # Se sucesso (200), o n8n retorna o arquivo excel binário
                st.success("Processamento concluído com sucesso pelo n8n!")

                # 6. Oferecer o arquivo para download
                st.download_button(
                    label="Clique aqui para baixar o Layout de Compra (XLSX)",
                    data=response.content, # O conteúdo binário (o arquivo) retornado pelo n8n
                    file_name="Calculo_VR_Layout_Final.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            except requests.exceptions.HTTPError as http_err:
                st.error(f"Erro do n8n (HTTP {http_err.response.status_code}): {http_err}")
                st.error(f"Resposta completa do servidor (provável erro no script Python): {response.text}")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado na comunicação com o n8n: {e}")