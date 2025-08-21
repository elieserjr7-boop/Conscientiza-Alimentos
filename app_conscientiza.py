import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÃO DA PÁGINA ---
# Define o título que aparece na aba do navegador e um ícone.
st.set_page_config(
    page_title="Alimento Salvo",
    page_icon=" cibo"
)

# --- FUNÇÃO PARA ENVIAR O E-MAIL ---
# Esta função será chamada quando o formulário for preenchido e enviado.
def enviar_email(nome, endereco, telefone, alimentos):
    # --- DADOS DO SEU E-MAIL (REMETENTE) ---
    # ATENÇÃO: Use um "app password" (senha de aplicativo) se você usa Gmail com verificação em duas etapas.
    # NUNCA coloque sua senha real diretamente no código em projetos públicos.
    email_remetente = st.secrets["GMAIL_USER"]
    senha_remetente = st.secrets["GMAIL_PASSWORD"]
    email_destinatario = st.secrets["EMAIL_DESTINATARIO"] # E-mail do seu grupo que vai RECEBER a notificação

    # --- MONTANDO O E-MAIL ---
    assunto = f"Nova Doação de Alimentos de: {nome}"
    
    corpo_html = f"""
    <html>
    <body>
        <h2>Nova Notificação de Alimentos para Coleta!</h2>
        <p><strong>Nome do Doador:</strong> {nome}</p>
        <p><strong>Endereço para Coleta:</strong> {endereco}</p>
        <p><strong>Telefone para Contato:</strong> {telefone}</p>
        <hr>
        <h3>Alimentos Disponíveis:</h3>
        <p>{alimentos}</p>
    </body>
    </html>
    """
    
    # Criando o objeto do e-mail
    msg = MIMEMultipart()
    msg['From'] = email_remetente
    msg['To'] = email_destinatario
    msg['Subject'] = assunto
    
    # Anexando o corpo do e-mail em formato HTML para ficar mais bonito
    msg.attach(MIMEText(corpo_html, 'html'))

    # --- ENVIANDO O E-MAIL ---
    try:
        # Conectando ao servidor SMTP do Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Inicia a conexão segura
        # Fazendo login na sua conta
        server.login(email_remetente, senha_remetente)
        # Enviando o e-mail
        server.sendmail(email_remetente, email_destinatario, msg.as_string())
        # Fechando a conexão
        server.quit()
        return True # Retorna True se o e-mail foi enviado com sucesso
    except Exception as e:
        # Se der algum erro, ele será impresso no console onde o Streamlit está rodando
        print(f"Erro ao enviar e-mail: {e}")
        return False # Retorna False se deu erro


# --- INTERFACE DO STREAMLIT ---

# Título da aplicação
st.title("Plataforma de Combate ao Desperdício de Alimentos")

# Texto de introdução
st.write(
    "Tem alimentos sobrando em casa e quer ajudar a combater o desperdício? "
    "Preencha o formulário abaixo que nosso grupo entrará em contato para buscar a doação!"
)

# Criando um formulário para evitar que a página recarregue a cada campo preenchido
with st.form("formulario_doacao"):
    st.subheader("Informações para Coleta")
    
    # Campos do formulário
    nome_pessoa = st.text_input("Seu Nome Completo:")
    endereco_coleta = st.text_input("Endereço Completo (Rua, Número, Bairro, CEP):")
    numero_contato = st.text_input("Seu Telefone/WhatsApp (com DDD):")
    descricao_alimentos = st.text_area("Descreva os alimentos e a quantidade aproximada:")
    
    # Botão de envio do formulário
    submitted = st.form_submit_button("Enviar Notificação")

# Quando o botão "Enviar Notificação" for clicado...
if submitted:
    # Verifica se todos os campos foram preenchidos
    if nome_pessoa and endereco_coleta and numero_contato and descricao_alimentos:
        # Chama a função de enviar e-mail
        if enviar_email(nome_pessoa, endereco_coleta, numero_contato, descricao_alimentos):
            st.success("Notificação enviada com sucesso! Agradecemos muito a sua colaboração. Em breve entraremos em contato.")
            st.balloons() # Uma animação de balões para comemorar!
        else:
            st.error("Desculpe, ocorreu um erro ao enviar sua notificação. Por favor, tente novamente mais tarde.")
    else:
        # Mensagem de aviso se algum campo estiver vazio
        st.warning("Por favor, preencha todos os campos antes de enviar.")
