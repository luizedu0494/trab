# app_inteligente_11_arquivos.py

# ==============================================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ==============================================================================
import streamlit as st
import requests

# ==============================================================================
# 2. CONFIGURAÇÃO PRINCIPAL DA PÁGINA
# ==============================================================================
# Cole aqui a URL de 'Production' do seu nó Webhook no n8n.
N8N_WEBHOOK_URL = "URL_DO_SEU_WEBHOOK_AQUI" 

st.set_page_config(layout="wide", page_title="Automação de Compra de VR/VA")

# ==============================================================================
# 3. CONSTRUÇÃO DA INTERFACE DO USUÁRIO
# ==============================================================================
st.title("🤖 Automação para Compra de Benefícios (VR/VA)")
st.markdown("Arraste e solte todas as 11 planilhas de base (incluindo o modelo 'VR MENSAL 05.2025.xlsx') na área abaixo.")

st.header("1. Carregar Pacote de Arquivos")

uploaded_files_list = st.file_uploader(
    "Arraste as 11 planilhas (.xlsx) aqui:",
    type=["xlsx"],
    accept_multiple_files=True
)

# --- MUDANÇA AQUI ---
# Apenas um feedback visual para o usuário, agora esperando 11 arquivos.
if uploaded_files_list:
    st.info(f"Arquivos carregados: {len(uploaded_files_list)} de 11 necessários.")
else:
    st.info("Aguardando os 11 arquivos...")

st.divider()

# ==============================================================================
# 4. LÓGICA DO PROCESSAMENTO (O QUE ACONTECE AO CLICAR NO BOTÃO)
# ==============================================================================
if st.button("🚀 Processar e Gerar Arquivo Final", type="primary", use_container_width=True):
    
    # --- MUDANÇA AQUI ---
    # Verificação de Segurança: Agora garantimos que o usuário enviou EXATAMENTE 11 arquivos.
    if uploaded_files_list and len(uploaded_files_list) == 11:
        
        files_to_send_to_n8n = []
        
        for i, file in enumerate(uploaded_files_list):
            files_to_send_to_n8n.append(
                (f'file_{i}', (file.name, file.getvalue()))
            )

        with st.spinner('Aguarde... O agente n8n está lendo 11 arquivos, calculando e gerando o resultado...'):
            try:
                response = requests.post(N8N_WEBHOOK_URL, files=files_to_send_to_n8n, timeout=300)
                response.raise_for_status() 

                st.success("Processamento concluído com sucesso!")

                st.download_button(
                    label="✅ Baixar Planilha Final para Fornecedor",
                    data=response.content,
                    file_name="VR_MENSAL_PROCESSADO.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")

    else:
        # --- MUDANÇA AQUI ---
        # A mensagem de aviso agora reflete a necessidade dos 11 arquivos.
        st.warning(f"Atenção: Você carregou {len(uploaded_files_list)} arquivo(s). Por favor, carregue todos os 11 arquivos juntos.")