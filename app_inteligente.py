# app_inteligente.py

# ==============================================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ==============================================================================
# Streamlit é a biblioteca para criar a interface web (títulos, botões, etc.).
import streamlit as st
# Requests é a biblioteca que nos permite "conversar" com a API do n8n.
import requests

# ==============================================================================
# 2. CONFIGURAÇÃO PRINCIPAL DA PÁGINA
# ==============================================================================
# IMPORTANTE: Esta é a única linha que você PRECISA alterar.
# Cole aqui a URL de 'Production' ou 'Test' que você copiou do seu nó Webhook no n8n.
N8N_WEBHOOK_URL = "URL_DO_SEU_WEBHOOK_AQUI" 

# Configura a página para usar a largura total da tela e define um título na aba do navegador.
st.set_page_config(layout="wide", page_title="Automação de Compra de VR/VA")

# ==============================================================================
# 3. CONSTRUÇÃO DA INTERFACE DO USUÁRIO (O QUE O USUÁRIO VÊ)
# ==============================================================================
st.title("🤖 Automação para Compra de Benefícios (VR/VA)")
st.markdown("Arraste e solte todas as 10 planilhas de base na área abaixo para iniciar o cálculo.")

st.header("1. Carregar Pacote de Arquivos")

# ESTA É A MUDANÇA PRINCIPAL:
# Criamos UMA ÚNICA caixa de upload. 
# 'accept_multiple_files=True' permite que o usuário arraste quantos arquivos quiser.
# O resultado é armazenado em uma LISTA chamada 'uploaded_files_list'.
uploaded_files_list = st.file_uploader(
    "Arraste as 10 planilhas (.xlsx) aqui:",
    type=["xlsx"],  # Aceita apenas arquivos .xlsx
    accept_multiple_files=True
)

# Apenas um feedback visual para o usuário, mostrando quantos arquivos ele já carregou.
if uploaded_files_list:
    st.info(f"Arquivos carregados: {len(uploaded_files_list)} de 10 necessários.")
else:
    st.info("Aguardando os 10 arquivos...")

# Adiciona uma linha horizontal para separar visualmente as seções.
st.divider()

# ==============================================================================
# 4. LÓGICA DO PROCESSAMENTO (O QUE ACONTECE AO CLICAR NO BOTÃO)
# ==============================================================================
# 'st.button' cria o botão principal. O código dentro deste 'if' só será executado
# quando o usuário clicar neste botão.
if st.button("🚀 Processar e Gerar Arquivo Final", type="primary", use_container_width=True):
    
    # Verificação de Segurança: Garantir que o usuário enviou exatamente os 10 arquivos.
    if uploaded_files_list and len(uploaded_files_list) == 10:
        
        # Prepara o "pacote" de arquivos para o n8n.
        # Como o n8n espera arquivos em um formato específico (multipart/form-data),
        # precisamos criar uma lista de tuplas.
        # Cada tupla contém: (nome_generico, (nome_real_do_arquivo, conteudo_do_arquivo))
        files_to_send_to_n8n = []
        
        # Faz um loop por cada arquivo que o usuário carregou
        for i, file in enumerate(uploaded_files_list):
            # A "etiqueta" genérica será 'file_0', 'file_1', 'file_2', etc.
            # O n8n vai usar o 'file.name' (o nome real do arquivo) para saber o que é.
            files_to_send_to_n8n.append(
                (f'file_{i}', (file.name, file.getvalue()))
            )

        # 'st.spinner' mostra uma mensagem amigável de "carregando" para o usuário.
        with st.spinner('Aguarde... O agente n8n está identificando, organizando e calculando os dados...'):
            try:
                # Este é o comando que efetivamente envia os arquivos para o n8n.
                # Ele faz uma requisição do tipo POST para a URL que configuramos.
                # 'files=' anexa nosso pacote de arquivos.
                # 'timeout=300' dá ao n8n 5 minutos para terminar o trabalho.
                response = requests.post(N8N_WEBHOOK_URL, files=files_to_send_to_n8n, timeout=300)
                
                # Se o n8n retornar um erro (ex: status 500), esta linha irá acusar o erro e pular para o 'except'.
                response.raise_for_status()

                # Se tudo deu certo, mostramos uma mensagem de sucesso.
                st.success("Processamento concluído com sucesso!")

                # 'st.download_button' cria o botão de download para o usuário.
                # 'response.content' contém o arquivo Excel binário que o n8n enviou de volta.
                st.download_button(
                    label="✅ Baixar Planilha Final para Fornecedor",
                    data=response.content,
                    file_name="VR_MENSAL_PROCESSADO.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            except requests.exceptions.RequestException as e:
                # Se houver um erro de conexão ou o n8n estiver offline, esta mensagem aparecerá.
                st.error(f"Erro na comunicação com o servidor de automação (n8n): {e}")
                st.info("Verifique se o workflow no n8n está ativo e se a URL do Webhook está correta.")
            except Exception as e:
                # Pega qualquer outro erro inesperado que possa acontecer.
                st.error(f"Ocorreu um erro inesperado durante o processamento: {e}")

    else:
        # Se os 10 arquivos não estiverem lá, avisa o usuário.
        st.warning(f"Atenção: Você carregou {len(uploaded_files_list)} arquivo(s). Por favor, carregue todos os 10 arquivos juntos.")